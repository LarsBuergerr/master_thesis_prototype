"""Katalog-Endpoints: Datenverzeichnisse als Portalinhalt.

Diese Ebene kennt keine Bewertung. Sie liefert, was ein Metadatenportal ohne
jeden Analyselauf anzeigen kann — und erlaubt zusätzlich, für die geladenen
Dateien einen Lauf anzustoßen (dasselbe Job-Handling wie beim Upload).

    GET  /catalogs                              — verfügbare Datenverzeichnisse
    GET  /catalogs/{name}/datasets              — Metadaten je Datei
    GET  /catalogs/{name}/files/{file}/rdf      — RDF-Quelltext einer Datei
    POST /catalogs/{name}/analyze               — Lauf über das ganze Verzeichnis
    POST /catalogs/{name}/files/{file}/analyze  — Lauf über eine Datei
"""

from __future__ import annotations

import json
import logging

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import ValidationError

from .. import catalog, settings
from ..jobs import JobRunner, JobStore
from ..schemas import AnalysisConfig, CatalogDataset, CatalogInfo, JobCreatedResponse

logger = logging.getLogger("backend.catalogs")

router = APIRouter(tags=["catalogs"], prefix="/catalogs")


def _store(request: Request) -> JobStore:
    return request.app.state.store


def _runner(request: Request) -> JobRunner:
    return request.app.state.runner


def _parse_config(config: str) -> AnalysisConfig:
    try:
        return AnalysisConfig.model_validate(json.loads(config or "{}"))
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid config: {e}")


@router.get("", response_model=list[CatalogInfo])
def list_catalogs() -> list[CatalogInfo]:
    return [CatalogInfo(**c) for c in catalog.list_catalogs()]


@router.get("/{name}/datasets", response_model=list[CatalogDataset])
def catalog_datasets(name: str) -> list[CatalogDataset]:
    """Beschreibende Metadaten aller RDF-Dateien des Verzeichnisses."""
    try:
        return [CatalogDataset(**d) for d in catalog.load_catalog(name)]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{name}/files/{filename}/rdf", response_class=PlainTextResponse)
def catalog_file_rdf(name: str, filename: str) -> PlainTextResponse:
    """RDF-Quelltext einer Datei — die Detailseite hebt Fundstellen darin hervor."""
    try:
        path = catalog.resolve_file(name, filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return PlainTextResponse(
        path.read_text(encoding="utf-8", errors="replace"),
        media_type="application/rdf+xml",
    )


@router.post("/{name}/analyze", response_model=JobCreatedResponse, status_code=202)
def analyze_catalog(request: Request, name: str, config: str = "{}") -> JobCreatedResponse:
    """Alle Dateien des Verzeichnisses bewerten — ein Job über den ganzen Katalog."""
    try:
        directory = catalog.resolve_catalog(name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    cfg = _parse_config(config)
    paths = [
        p for p in sorted(directory.iterdir())
        if p.is_file() and p.suffix.lower() in catalog.RDF_SUFFIXES
    ]
    if not paths:
        raise HTTPException(status_code=404, detail=f"No RDF files in catalog {name}")
    if len(paths) > settings.MAX_FILES_PER_JOB:
        raise HTTPException(
            status_code=400,
            detail=f"Too many files ({len(paths)} > {settings.MAX_FILES_PER_JOB})",
        )

    payload = [(p.name, p.read_bytes()) for p in paths]
    job_id = _store(request).create([p.name for p in paths], cfg)
    _runner(request).submit(job_id, payload, cfg)
    logger.info("Created catalog job %s for %s (%d files)", job_id, name, len(paths))
    return JobCreatedResponse(job_id=job_id, status="queued")


@router.post("/{name}/files/{filename}/analyze", response_model=JobCreatedResponse, status_code=202)
def analyze_catalog_file(
    request: Request, name: str, filename: str, config: str = "{}"
) -> JobCreatedResponse:
    """Eine einzelne Datei bewerten — identische Pipeline wie ``POST /analyze``."""
    try:
        path = catalog.resolve_file(name, filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

    cfg = _parse_config(config)
    job_id = _store(request).create([path.name], cfg)
    _runner(request).submit(job_id, [(path.name, path.read_bytes())], cfg)
    logger.info("Created file job %s for %s/%s", job_id, name, path.name)
    return JobCreatedResponse(job_id=job_id, status="queued")
