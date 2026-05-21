"""Quality Metrics Service - Standalone module for metadata validation.

No pipeline, no framework - just a simple utility to validate metadata
and calculate quality scores for DCAT-AP-DE datasets.
"""

from typing import Any, Dict, Optional
from rdflib import Graph
from concurrent.futures import ThreadPoolExecutor, as_completed

from quality_indicators.models.indicator import Indicator, IndicatorStatus
from quality_indicators.models.dimension import QualityDimension
from quality_indicators.validators.rdf_parser import RDFMetadataParser
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
        """
        self.max_workers = max_workers
        self.dimension_weights = dimension_weights or {}
        self.indicator_weights = indicator_weights or {}
        self.dimension_whitelist = (
            set(dimension_whitelist) if dimension_whitelist else None
        )
        self.indicator_blacklist = (
            set(indicator_blacklist) if indicator_blacklist else set()
        )

        # Ensure all indicators are loaded and registered
        self._load_indicators()

    def _load_indicators(self) -> None:
        """Load all indicator modules to trigger auto-registration."""
        try:
            # Import all indicator modules - this triggers __init__() and registration
            from quality_indicators import indicators  # noqa: F401

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

        return self._process_dimension(dimension, indicators, metadata)

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
            result = indicator.validate(metadata)
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

        # Process dimensions in parallel
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_dimension = {
                executor.submit(
                    self._process_dimension,
                    dim,
                    indicators,
                    metadata,
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

        return results

    def _process_dimension(
        self,
        dimension: QualityDimension,
        indicators: Dict[str, Indicator],
        metadata: Graph,
    ) -> Dict[str, Any]:
        """Internal: Process a single dimension.

        Args:
            dimension: The dimension
            indicators: Indicators for this dimension
            metadata: RDF metadata graph

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

            try:
                result = indicator.validate(metadata)

                effective_weight = self.indicator_weights.get(
                    indicator_id, indicator.weight
                )
                total_score += result.score * effective_weight
                total_indicator_weight += effective_weight

                result_dict = result.to_dict()
                result_dict["default_weight"] = indicator.weight
                result_dict["effective_weight"] = effective_weight
                indicator_results.append(result_dict)

                if result.status == IndicatorStatus.PASS:
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
