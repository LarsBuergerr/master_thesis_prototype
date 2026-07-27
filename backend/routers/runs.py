"""Run-Endpoints: abgeschlossene Bewertungsläufe als Overlay über den Katalog.

    GET /runs                    — verfügbare Läufe
    GET /runs/{name}             — Kurzbewertung je Datei (Liste/Übersicht)
    GET /runs/{name}/{stem}      — vollständiges Ergebnis einer Datei (Detailseite)

Verknüpft wird ausschließlich über den Dateinamen; ein Lauf trägt keine
beschreibenden Metadaten (siehe backend/runs.py).
"""

from __future__ import annotations

import logging
from typing import Any

from fastapi import APIRouter, HTTPException

from .. import runs
from ..schemas import RunIndexRow, RunInfo

logger = logging.getLogger("backend.runs")

router = APIRouter(tags=["runs"], prefix="/runs")


@router.get("", response_model=list[RunInfo])
def list_runs() -> list[RunInfo]:
    return [RunInfo(**r) for r in runs.list_runs()]


@router.get("/{name}", response_model=list[RunIndexRow])
def run_index(name: str) -> list[RunIndexRow]:
    try:
        return [RunIndexRow(**row) for row in runs.run_index(name)]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{name}/{stem}")
def run_result(name: str, stem: str) -> dict[str, Any]:
    """Vollständiges ``result.json`` einer Datei aus diesem Lauf."""
    try:
        return runs.run_result(name, stem)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
