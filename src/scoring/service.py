"""Quality Metrics Service - Standalone module for metadata validation.

No pipeline, no framework - just a simple utility to validate metadata
and calculate quality scores for DCAT-AP-DE datasets.
"""

import inspect
from typing import Any, Dict, Optional
from rdflib import Graph
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.indicator import Indicator, IndicatorStatus
from core.dimension import QualityDimension
from extraction.dataset_context import DatasetContext
from extraction.distribution_probes import attach_probes
from extraction.semantic_assessment import (
    attach_semantic_assessment,
)
from extraction.rdf_parser import RDFMetadataParser
from scoring.score_policy import ScorePolicy
from utils.logger import get_logger

logger = get_logger(__name__)


class QualityMetricsService:
    """Simple service to validate metadata quality."""

    def __init__(
        self,
        max_workers: int = 4,
        dimension_weights: Optional[Dict[str, float]] = None,
        indicator_weights: Optional[Dict[str, float]] = None,
        dimension_whitelist: Optional[list] = None,
        indicator_blacklist: Optional[list] = None,
        indicator_whitelist: Optional[list] = None,
        llm: Optional[Any] = None,
        language: str = "de",
        score_policy: Optional[ScorePolicy] = None,
    ):
        """Initialize the service.

        Args:
            max_workers: Number of parallel workers for dimension processing
            dimension_weights: Optional weights per dimension key
                (for example {"expressiveness": 0.3, "findability": 0.1})
            indicator_weights: Optional weights per indicator id
                (for example {"find_keywords_count": 2.0})
            dimension_whitelist: Optional list of dimension names to include
                (if empty/None, all dimensions are included)
            indicator_blacklist: Optional list of indicator IDs to exclude
                (if empty/None, no indicators are excluded)
            llm: Optional LangChain chat model. Required for the expressiveness
                dimension — its indicators read a single per-dataset LLM
                assessment. When ``None``, expressiveness indicators report
                NOT_APPLICABLE and no LLM call is made.
            language: Output language for the LLM assessment ("de" | "en").
            score_policy: Optional :class:`ScorePolicy` remapping each
                indicator's status to a configurable score (tunable PASS /
                PARTIAL / FAIL points, optional negative fails). When ``None``
                the indicators' raw scores are used unchanged.
        """
        self.max_workers = max_workers
        self.llm = llm
        self.language = language
        self.score_policy = score_policy
        self.dimension_weights = dimension_weights or {}
        self.indicator_weights = indicator_weights or {}
        self.dimension_whitelist = (
            set(dimension_whitelist) if dimension_whitelist else None
        )
        self.indicator_blacklist = (
            set(indicator_blacklist) if indicator_blacklist else set()
        )
        self.indicator_whitelist = (
            set(indicator_whitelist) if indicator_whitelist else None
        )

        # Ensure all indicators are loaded and registered
        self._load_indicators()

    def _load_indicators(self) -> None:
        """Load all indicator modules to trigger auto-registration."""
        try:
            # Import all indicator modules - this triggers __init__() and registration
            from scoring import indicators  # noqa: F401

            logger.debug("Indicators loaded and registered")
        except Exception as e:
            logger.error(f"Failed to load indicators: {e}")
            raise

    def validate_metadata(self, metadata_path: str) -> Dict[str, Any]:
        """Validate metadata file against all quality dimensions.

        This is the main entry point - validates everything at once.

        Args:
            metadata_path: Path to RDF metadata file

        Returns:
            Dictionary with validation results for all dimensions
        """
        logger.info(f"Validating metadata: {metadata_path}")

        try:
            # Step 1: Parse metadata
            metadata = RDFMetadataParser.parse_file(metadata_path)
            logger.info(f"Parsed {len(metadata)} triples")

            # Step 2: Validate all dimensions
            results = self._validate_all_dimensions(metadata)

            return results

        except Exception as e:
            logger.error(f"Validation failed: {e}", exc_info=True)
            return {
                "error": str(e),
                "by_dimension": {},
                "summary": {},
            }

    def validate_metadata_graph(self, metadata: Graph) -> Dict[str, Any]:
        """Validate a metadata Graph object.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            Dictionary with validation results
        """
        return self._validate_all_dimensions(metadata)

    def validate_dimension(
        self, metadata: Graph, dimension: QualityDimension
    ) -> Dict[str, Any]:
        """Validate a single quality dimension.

        Args:
            metadata: rdflib Graph with DCAT metadata
            dimension: The dimension to validate

        Returns:
            Dictionary with dimension results
        """
        logger.info(f"Validating dimension: {dimension.value}")

        # Get indicators for this dimension
        indicators = Indicator.by_dimension(dimension)

        if not indicators:
            logger.warning(f"No indicators registered for {dimension.value}")
            return {
                "dimension": dimension.value,
                "indicators": [],
                "score": 0.0,
                "error": "No indicators found",
            }

        context = DatasetContext.from_graph(metadata)
        self._maybe_attach_probes(context, {dimension: indicators})
        self._maybe_attach_semantic_assessment(context, {dimension: indicators})
        return self._process_dimension(dimension, indicators, metadata, context)

    def validate_indicator(self, metadata: Graph, indicator_id: str) -> Dict[str, Any]:
        """Validate a single indicator.

        Args:
            metadata: rdflib Graph with DCAT metadata
            indicator_id: ID of the indicator to validate

        Returns:
            Validation result
        """
        indicator = Indicator.get(indicator_id)

        if not indicator:
            return {
                "error": f"Indicator '{indicator_id}' not found",
                "indicator_id": indicator_id,
            }

        logger.debug(f"Validating indicator: {indicator_id}")

        try:
            context = DatasetContext.from_graph(metadata)
            self._maybe_attach_probes(
                context, {indicator.dimension: {indicator_id: indicator}}
            )
            self._maybe_attach_semantic_assessment(
                context, {indicator.dimension: {indicator_id: indicator}}
            )
            result = self._invoke_indicator(indicator, metadata, context)
            return result.to_dict()

        except Exception as e:
            logger.error(f"Indicator validation failed: {e}")
            return {
                "indicator_id": indicator_id,
                "status": IndicatorStatus.ERROR.value,
                "error": str(e),
            }

    # ─────────────────────────────────────────────────────────────────

    def _validate_all_dimensions(self, metadata: Graph) -> Dict[str, Any]:
        """Internal: Validate all dimensions in parallel.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            Results from all dimensions
        """
        # Build per-dataset facts once. Indicators that need
        # distribution-level data (URLs, formats, media-types) can read it
        # from here instead of re-querying the graph.
        context = DatasetContext.from_graph(metadata)
        logger.debug(
            f"DatasetContext built: {context.distribution_count} distribution(s)"
        )

        results = {
            "by_dimension": {},
            "summary": {},
            "errors": [],
            "weights": {
                "dimension_weights": self.dimension_weights,
                "indicator_weights": self.indicator_weights,
            },
        }

        # Filter dimensions based on whitelist
        dimensions_to_process = []
        for dim in QualityDimension:
            if (
                self.dimension_whitelist is None
                or dim.value in self.dimension_whitelist
            ):
                dimensions_to_process.append(dim)
            else:
                logger.debug(f"Skipping dimension (not in whitelist): {dim.value}")

        # Get indicators for each dimension
        dimensions_indicators = {
            dim: Indicator.by_dimension(dim) for dim in dimensions_to_process
        }

        # Attach distribution probes once up-front when the accessibility
        # dimension will run. Indicators that consume ``dist.probe`` (e.g.
        # FormatCongruenceIndicator) then read pre-computed data instead of
        # each one HTTP-probing on its own.
        self._maybe_attach_probes(context, dimensions_indicators)

        # Likewise, run the single expressiveness LLM call up-front (before the
        # parallel fan-out) so the expr_* indicators just read their slice.
        self._maybe_attach_semantic_assessment(context, dimensions_indicators)

        # Process dimensions in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_dimension = {
                executor.submit(
                    self._process_dimension,
                    dim,
                    indicators,
                    metadata,
                    context,
                ): dim
                for dim, indicators in dimensions_indicators.items()
            }

            for future in as_completed(future_to_dimension):
                dimension = future_to_dimension[future]
                try:
                    dim_results = future.result()
                    results["by_dimension"][dimension.value] = dim_results
                    logger.info(
                        f"✓ {dimension.value}: {len(dim_results['indicators'])} indicators"
                    )
                except Exception as e:
                    error_msg = f"Error processing {dimension.value}: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)

        # Calculate summary
        results["summary"] = self._calculate_summary(results)

        # Surface per-dataset LLM usage (tokens/cost/latency) so the caller can
        # persist it and aggregate run-level cost.
        results["llm_usage"] = context.llm_usage

        logger.debug(context.to_json())

        return results

    def _process_dimension(
        self,
        dimension: QualityDimension,
        indicators: Dict[str, Indicator],
        metadata: Graph,
        context: Optional[DatasetContext] = None,
    ) -> Dict[str, Any]:
        """Internal: Process a single dimension.

        Args:
            dimension: The dimension
            indicators: Indicators for this dimension
            metadata: RDF metadata graph
            context: Optional pre-computed dataset facts shared across
                indicators.

        Returns:
            Dimension results
        """
        indicator_results = []
        total_score = 0.0
        total_indicator_weight = 0.0
        pass_count = 0

        for indicator_id, indicator in indicators.items():
            # Skip blacklisted indicators
            if indicator_id in self.indicator_blacklist:
                logger.debug(f"Skipping indicator (blacklisted): {indicator_id}")
                continue

            if (
                self.indicator_whitelist
                and indicator_id not in self.indicator_whitelist
            ):
                logger.debug(f"Skipping indicator (not in whitelist): {indicator_id}")
                continue

            try:
                result = self._invoke_indicator(indicator, metadata, context)

                effective_weight = self.indicator_weights.get(
                    indicator_id, indicator.weight
                )
                # Remap the raw status+score through the configured policy
                # (tunable PASS/PARTIAL/FAIL points; strict mode turns PARTIAL
                # into FAIL). Without a policy the raw values are used unchanged.
                if self.score_policy is not None:
                    eff_status, effective_score = self.score_policy.evaluate(
                        indicator_id=indicator_id,
                        status=result.status,
                        raw_score=result.score,
                        graded=type(indicator).GRADED,
                    )
                else:
                    eff_status, effective_score = result.status, result.score

                total_score += effective_score * effective_weight
                total_indicator_weight += effective_weight

                result_dict = result.to_dict()
                result_dict["default_weight"] = indicator.weight
                result_dict["effective_weight"] = effective_weight
                # The output shows the *effective* (policy-applied) status and
                # score; the indicator's untouched values are preserved as
                # ``raw_status`` / ``raw_score`` for transparency.
                result_dict["raw_status"] = result.status.value
                result_dict["raw_score"] = result.score
                result_dict["status"] = eff_status.value
                result_dict["score"] = effective_score
                result_dict["effective_score"] = effective_score

                if (
                    self.score_policy is not None
                    and (eff_status != result.status or effective_score != result.score)
                ):
                    logger.info(
                        "[%s] policy remap: %s/%.2f -> %s/%.2f (weight %.2f)",
                        indicator_id,
                        result.status.value,
                        result.score,
                        eff_status.value,
                        effective_score,
                        effective_weight,
                    )

                indicator_results.append(result_dict)

                if eff_status == IndicatorStatus.PASS:
                    pass_count += 1

            except Exception as e:
                logger.error(f"Indicator {indicator_id} failed: {e}")
                indicator_results.append(
                    {
                        "indicator_id": indicator_id,
                        "status": IndicatorStatus.ERROR.value,
                        "error": str(e),
                        "default_weight": indicator.weight,
                        "effective_weight": self.indicator_weights.get(
                            indicator_id, indicator.weight
                        ),
                    }
                )

        avg_score = (
            total_score / total_indicator_weight if total_indicator_weight > 0 else 0.0
        )
        # Negative fail_score penalties can push a dimension below zero. Floor it
        # at 0 so no dimension — and therefore no overall score — can go negative.
        avg_score = max(0.0, avg_score)
        dimension_weight = self.dimension_weights.get(dimension.value, 1.0)

        return {
            "dimension": dimension.value,
            "indicators": indicator_results,
            "score": avg_score,
            "dimension_weight": dimension_weight,
            "total_indicator_weight": total_indicator_weight,
            "indicator_count": len(indicator_results),
            "pass_count": pass_count,
            "pass_rate": (
                pass_count / len(indicator_results) if indicator_results else 0.0
            ),
        }

    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Internal: Calculate overall quality summary.

        Args:
            results: Results from all dimensions

        Returns:
            Summary statistics
        """
        dimension_scores = {}
        total_indicators = 0
        total_pass = 0

        for dim_value, dim_results in results.get("by_dimension", {}).items():
            dimension_scores[dim_value] = dim_results.get("score", 0.0)
            total_indicators += dim_results.get("indicator_count", 0)
            total_pass += dim_results.get("pass_count", 0)

        weighted_score_sum = 0.0
        total_dimension_weight = 0.0

        for dim_value, dim_score in dimension_scores.items():
            dim_weight = self.dimension_weights.get(dim_value, 1.0)
            weighted_score_sum += dim_score * dim_weight
            total_dimension_weight += dim_weight

        overall_score = (
            weighted_score_sum / total_dimension_weight
            if total_dimension_weight > 0
            else 0.0
        )

        overall_pass_rate = (
            total_pass / total_indicators if total_indicators > 0 else 0.0
        )

        return {
            "overall_score": overall_score,
            "overall_pass_rate": overall_pass_rate,
            "dimension_scores": dimension_scores,
            "dimension_weights": {
                dim: self.dimension_weights.get(dim, 1.0)
                for dim in dimension_scores.keys()
            },
            "total_dimension_weight": total_dimension_weight,
            "total_indicators": total_indicators,
            "total_pass": total_pass,
            "total_fail": total_indicators - total_pass,
            "quality_grade": self._score_to_grade(overall_score),
        }

    def _maybe_attach_probes(
        self,
        context: DatasetContext,
        dimensions_indicators: Dict[QualityDimension, Dict[str, Indicator]],
    ) -> None:
        """Attach distribution probes if any indicator about to run consumes them.

        Looking up the indicator IDs (rather than the dimension) keeps the
        trigger precise: blacklisting every consumer skips the HTTP work
        entirely.
        """
        probe_consumers = {
            "acc_format_congruence",
            "acc_download_url_response",
            "acc_access_url_response",
            "acc_machine_readable_access",
        }
        will_run_consumer = any(
            ind_id in probe_consumers and ind_id not in self.indicator_blacklist
            for inds in dimensions_indicators.values()
            for ind_id in inds.keys()
        )
        if not will_run_consumer:
            return
        if context.distribution_count == 0:
            return

        # Import lazily to keep the indicator's tuned defaults in one place.
        from scoring.indicators.accessibility import (
            FormatCongruenceIndicator,
        )

        attach_probes(
            context,
            max_probes=FormatCongruenceIndicator.MAX_DISTRIBUTIONS,
            parallel=FormatCongruenceIndicator.PARALLEL_WORKERS,
            logger=logger,
        )
        attached = sum(1 for d in context.distributions if d.probe is not None)
        logger.debug(
            f"Attached probes to {attached}/{context.distribution_count} distribution(s)"
        )

    def _maybe_attach_semantic_assessment(
        self,
        context: DatasetContext,
        dimensions_indicators: Dict[QualityDimension, Dict[str, Indicator]],
    ) -> None:
        """Run the one-shot expressiveness LLM call if it will actually be read.

        Mirrors :meth:`_maybe_attach_probes`: an all-or-nothing guard. The call
        is skipped entirely when no LLM is configured or when every
        expressiveness indicator about to run is filtered out — the LLM scores
        the whole dimension holistically, so the blacklist can't make it
        cheaper per-criterion, only skip the call when the dimension is off.
        """
        if self.llm is None:
            return

        expr_indicators = dimensions_indicators.get(QualityDimension.EXPRESSIVENESS)
        if not expr_indicators:
            return

        will_run = any(
            ind_id not in self.indicator_blacklist
            and (
                self.indicator_whitelist is None
                or ind_id in self.indicator_whitelist
            )
            for ind_id in expr_indicators.keys()
        )
        if not will_run:
            return

        attach_semantic_assessment(
            context, self.llm, language=self.language, logger=logger
        )
        logger.debug(
            "Expressiveness assessment "
            f"{'attached' if context.semantic_assessment is not None else 'unavailable'}"
        )

    @staticmethod
    def _invoke_indicator(
        indicator: Indicator,
        metadata: Graph,
        context: Optional[DatasetContext],
    ):
        """Call ``indicator.validate``, passing ``context`` only when the
        indicator's signature accepts it. Indicators opt in by declaring a
        ``context`` keyword argument.
        """
        if context is not None:
            try:
                sig = inspect.signature(indicator.validate)
                if "context" in sig.parameters:
                    return indicator.validate(metadata, context=context)
            except (TypeError, ValueError):
                pass
        return indicator.validate(metadata)

    @staticmethod
    def _score_to_grade(score: float) -> str:
        """Convert score to grade.

        Args:
            score: Score between 0.0 and 1.0

        Returns:
            Grade (A, B, C, D, F)
        """
        if score >= 0.9:
            return "A"
        elif score >= 0.75:
            return "B"
        elif score >= 0.6:
            return "C"
        elif score >= 0.4:
            return "D"
        else:
            return "F"
