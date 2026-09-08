"""Glue between the API layer and the core ``QualityMetricsService``.

Builds a service instance from an :class:`AnalysisConfig` and runs it against
uploaded RDF bytes. Keeps all core-construction knowledge (LLM gating, score
policy, weights) in one place so the routers stay thin.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Optional

# ``backend`` package import puts ``src`` on sys.path (see backend/__init__.py).
from core.indicator import Indicator
from core.dimension import QualityDimension
from core.guidance import DIMENSION_GUIDANCE, SCORE_GLOSSARY
from extraction.rdf_parser import RDFMetadataParser
from scoring.service import QualityMetricsService
from scoring.score_policy import ScorePolicy
from llm_factory import build_llm_from_params

from .schemas import AnalysisConfig, DimensionInfo, GuidanceInfo, IndicatorInfo

logger = logging.getLogger("backend.analysis")


def _format_for_filename(filename: str) -> str:
    """Map a filename extension to an RDFMetadataParser format hint."""
    ext = Path(filename).suffix.lstrip(".").lower()
    return ext or "rdf"


def _expressiveness_active(config: AnalysisConfig) -> bool:
    wl = config.dimension_whitelist
    return not wl or "expressiveness" in wl


def _maybe_build_llm(config: AnalysisConfig):
    """Build the LLM only when expressiveness will run and the LLM is enabled.

    Degrades gracefully: on any construction error (e.g. missing API key) we log
    and return ``None`` so expressiveness indicators report NOT_APPLICABLE
    instead of failing the whole job.
    """
    if not config.llm.enabled or not _expressiveness_active(config):
        return None
    try:
        return build_llm_from_params(
            provider=config.llm.provider,
            model=config.llm.model,
            base_url=config.llm.base_url,
            temperature=config.llm.temperature,
            max_tokens=config.llm.max_tokens,
        )
    except ValueError as e:
        logger.warning("LLM enabled but unavailable (%s); expressiveness → N/A", e)
        return None


def build_service(config: AnalysisConfig) -> QualityMetricsService:
    """Construct a ``QualityMetricsService`` from an API config.

    Reused across all files of one job — weights, score policy and the LLM
    client are identical per run; each file gets a fresh context internally.
    """
    score_policy: Optional[ScorePolicy] = None
    if config.scoring is not None:
        score_policy = ScorePolicy.from_config(config.scoring.model_dump())

    return QualityMetricsService(
        max_workers=config.max_workers,
        dimension_weights=config.dimension_weights,
        indicator_weights=config.indicator_weights,
        dimension_whitelist=config.dimension_whitelist,
        indicator_blacklist=config.indicator_blacklist,
        indicator_whitelist=config.indicator_whitelist,
        llm=_maybe_build_llm(config),
        language=config.language,
        score_policy=score_policy,
    )


def analyze_bytes(
    service: QualityMetricsService, content: bytes, filename: str
) -> dict[str, Any]:
    """Parse RDF ``content`` and score it. Raises on parse failure."""
    text = content.decode("utf-8")
    graph = RDFMetadataParser.parse_string(
        text, format_hint=_format_for_filename(filename)
    )
    return service.validate_metadata_graph(graph)


def list_indicators() -> list[IndicatorInfo]:
    """Snapshot the indicator registry for the config-building frontend."""
    # Importing the package triggers auto-registration of all indicators.
    import scoring.indicators  # noqa: F401

    infos: list[IndicatorInfo] = []
    for ind_id, ind in sorted(Indicator.all().items()):
        guidance = ind.guidance
        infos.append(
            IndicatorInfo(
                indicator_id=ind_id,
                name_de=ind.name_de,
                name_en=ind.name_en,
                dimension=ind.dimension.value,
                description_de=ind.description_de,
                description_en=ind.description_en,
                default_weight=ind.weight,
                graded=type(ind).GRADED,
                guidance=(
                    GuidanceInfo.model_validate(guidance.to_dict()) if guidance else None
                ),
            )
        )
    return infos


def list_dimensions() -> list[str]:
    return [d.value for d in QualityDimension]


def list_dimension_info() -> list[DimensionInfo]:
    """Deutsche Bezeichnung und Erklärung je Dimension."""
    return [
        DimensionInfo(
            dimension=d.value,
            label_de=DIMENSION_GUIDANCE.get(d.value, {}).get("label_de", d.value),
            what_de=DIMENSION_GUIDANCE.get(d.value, {}).get("what_de", ""),
        )
        for d in QualityDimension
    ]


def score_glossary() -> dict[str, str]:
    """Erklärung der Kennzahlen neben jedem Indikator."""
    return dict(SCORE_GLOSSARY)
