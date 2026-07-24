"""Meta endpoints: health check and indicator registry."""

from __future__ import annotations

from fastapi import APIRouter

from ..analysis_adapter import (
    list_dimension_info,
    list_dimensions,
    list_indicators,
    score_glossary,
)
from ..schemas import IndicatorsResponse

router = APIRouter(tags=["meta"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/indicators", response_model=IndicatorsResponse)
def indicators() -> IndicatorsResponse:
    """List all registered indicators + dimensions, each with its guidance.

    The frontend uses this twice: to build the config UI dynamically (weights
    sliders, dimension toggles) so it always matches the live registry, and to
    label results in plain German — sprechender Name, betroffenes Feld,
    Handlungsanweisung und Vokabular kommen aus ``core.guidance``.
    """
    return IndicatorsResponse(
        dimensions=list_dimensions(),
        indicators=list_indicators(),
        dimension_info=list_dimension_info(),
        score_glossary=score_glossary(),
    )
