"""Sample endpoints: serve the evaluation sample's RDF files and run them.

The GovData portal mock renders datasets of the evaluation sample (n = 50).
So that the mock does not merely replay canned numbers, it can ask the backend
to score the very same RDF file live — same code path as an upload, only the
bytes come from :data:`settings.SAMPLES_DIR` instead of a multipart request.

Endpoints:
    GET  /samples                 — available sample files
    GET  /samples/{name}/rdf      — raw RDF (the portal shows excerpts of it)
    POST /samples/{name}/analyze  — start an analysis job, returns a job_id
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, ValidationError

from .. import settings
from ..jobs import JobRunner, JobStore
from ..schemas import AnalysisConfig, JobCreatedResponse

logger = logging.getLogger("backend.samples")

router = APIRouter(tags=["samples"], prefix="/samples")

RDF_SUFFIXES = {".rdf", ".xml", ".ttl", ".n3", ".nt", ".jsonld"}


class SampleInfo(BaseModel):
    name: str
    filename: str
    size_bytes: int


def _store(request: Request) -> JobStore:
    return request.app.state.store


def _runner(request: Request) -> JobRunner:
    return request.app.state.runner


def _resolve(name: str) -> Path:
    """Map a sample name to a file inside SAMPLES_DIR.

    ``name`` may carry the suffix or not. Path separators are rejected outright
    and the resolved path is re-checked against the samples directory, so a
    crafted name cannot escape it.
    """
    if "/" in name or "\\" in name or name.startswith("."):
        raise HTTPException(status_code=400, detail="Invalid sample name")

    base = settings.SAMPLES_DIR.resolve()
    candidates = [base / name] if Path(name).suffix else [
        base / f"{name}{suffix}" for suffix in (".rdf", ".xml", ".ttl")
    ]
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved.parent != base or not resolved.is_file():
            continue
        if resolved.suffix.lower() not in RDF_SUFFIXES:
            continue
        return resolved

    raise HTTPException(status_code=404, detail=f"Sample not found: {name}")


@router.get("", response_model=list[SampleInfo])
def list_samples() -> list[SampleInfo]:
    base = settings.SAMPLES_DIR
    if not base.is_dir():
        logger.warning("Samples directory missing: %s", base)
        return []
    return [
        SampleInfo(name=p.stem, filename=p.name, size_bytes=p.stat().st_size)
        for p in sorted(base.iterdir())
        if p.is_file() and p.suffix.lower() in RDF_SUFFIXES
    ]


@router.get("/{name}/rdf", response_class=PlainTextResponse)
def sample_rdf(name: str) -> PlainTextResponse:
    """Raw RDF of one sample — the portal highlights the offending lines."""
    path = _resolve(name)
    return PlainTextResponse(
        path.read_text(encoding="utf-8", errors="replace"),
        media_type="application/rdf+xml",
    )


@router.post("/{name}/analyze", response_model=JobCreatedResponse, status_code=202)
def analyze_sample(request: Request, name: str, config: str = "{}") -> JobCreatedResponse:
    """Score a sample file — identical pipeline to ``POST /analyze``.

    ``config`` is the same JSON string as on the upload route (passed as a
    query parameter here since there is no multipart body).
    """
    path = _resolve(name)
    try:
        cfg = AnalysisConfig.model_validate(json.loads(config or "{}"))
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid config: {e}")

    payload = [(path.name, path.read_bytes())]
    job_id = _store(request).create([path.name], cfg)
    _runner(request).submit(job_id, payload, cfg)
    logger.info("Created sample job %s for %s", job_id, path.name)

    return JobCreatedResponse(job_id=job_id, status="queued")
