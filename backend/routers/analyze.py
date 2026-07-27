"""Analysis endpoints: submit a job, poll status/results, list history."""

from __future__ import annotations

import json
import logging

from fastapi import APIRouter, File, Form, HTTPException, Request, UploadFile
from pydantic import ValidationError

from .. import settings
from ..jobs import JobRunner, JobStore
from ..schemas import (
    AnalysisConfig,
    JobCreatedResponse,
    JobDetail,
    JobSummary,
)

logger = logging.getLogger("backend.analyze")

router = APIRouter(tags=["analyze"])


def _store(request: Request) -> JobStore:
    return request.app.state.store


def _runner(request: Request) -> JobRunner:
    return request.app.state.runner


@router.post("/analyze", response_model=JobCreatedResponse, status_code=202)
async def analyze(
    request: Request,
    files: list[UploadFile] = File(...),
    config: str = Form("{}"),
) -> JobCreatedResponse:
    """Submit RDF files for scoring.

    ``files``: one or more RDF uploads (multipart).
    ``config``: a JSON string matching :class:`AnalysisConfig` (weights, score
    policy, LLM settings, whitelists). Returns a ``job_id`` to poll.
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    if len(files) > settings.MAX_FILES_PER_JOB:
        raise HTTPException(
            status_code=400,
            detail=f"Too many files ({len(files)} > {settings.MAX_FILES_PER_JOB})",
        )

    # Parse + validate the config JSON.
    try:
        cfg = AnalysisConfig.model_validate(json.loads(config or "{}"))
    except (json.JSONDecodeError, ValidationError) as e:
        raise HTTPException(status_code=422, detail=f"Invalid config: {e}")

    # Read uploads into memory (with a per-file size guard).
    payload: list[tuple[str, bytes]] = []
    for f in files:
        content = await f.read()
        if len(content) > settings.MAX_UPLOAD_BYTES:
            raise HTTPException(
                status_code=413,
                detail=f"File too large: {f.filename} ({len(content)} bytes)",
            )
        payload.append((f.filename or "unnamed.rdf", content))

    filenames = [name for name, _ in payload]
    job_id = _store(request).create(filenames, cfg)
    _runner(request).submit(job_id, payload, cfg)
    logger.info("Created job %s with %d file(s)", job_id, len(payload))

    return JobCreatedResponse(job_id=job_id, status="queued")


@router.get("/jobs", response_model=list[JobSummary])
def list_jobs(request: Request, limit: int = 50) -> list[JobSummary]:
    return [JobSummary.model_validate(j) for j in _store(request).list(limit=limit)]


@router.get("/jobs/{job_id}", response_model=JobDetail)
def get_job(request: Request, job_id: str, results: bool = True) -> JobDetail:
    """Job state, per Vorgabe mit den Ergebnissen der bereits fertigen Dateien.

    ``results=false`` liefert nur Status und Fortschritt. Das ist die
    sinnvolle Form fürs Pollen eines Laufs über viele Dateien: die Ergebnisse
    summieren sich auf etliche Megabyte, und sie jede Sekunde erneut zu
    übertragen kostet mehr, als der Zwischenstand wert ist.
    """
    job = _store(request).get(job_id, include_results=results)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobDetail.model_validate(job)
