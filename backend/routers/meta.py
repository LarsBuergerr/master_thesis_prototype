"""Meta endpoints: health check and indicator registry."""

from __future__ import annotations

from fastapi import APIRouter

from ..analysis_adapter import list_dimensions, list_indicators
from ..schemas import IndicatorsResponse

router = APIRouter(tags=["meta"])


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/indicators", response_model=IndicatorsResponse)
def indicators() -> IndicatorsResponse:
    """List all registered indicators + dimensions.

    The frontend uses this to build the config UI dynamically (weights sliders,
    dimension toggles) so it always matches the live registry.
    """
    return IndicatorsResponse(
        dimensions=list_dimensions(),
        indicators=list_indicators(),
    )
