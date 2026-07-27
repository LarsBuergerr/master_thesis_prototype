"""FastAPI application entry point.

Run locally with:
    uvicorn backend.app:app --reload --port 8000
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load .env (OPENROUTER_API_KEY etc.) before anything reads the environment.
load_dotenv()

from . import settings  # noqa: E402
from .jobs import JobRunner, JobStore  # noqa: E402
from .routers import analyze, catalogs, meta, runs  # noqa: E402

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.store = JobStore(settings.DB_PATH)
    app.state.runner = JobRunner(app.state.store, max_workers=settings.JOB_WORKERS)
    logger.info("Analyzer backend ready (db=%s)", settings.DB_PATH)
    try:
        yield
    finally:
        app.state.runner.shutdown()


app = FastAPI(
    title="DCAT-AP-DE Quality Analyzer API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meta.router)
app.include_router(analyze.router)
app.include_router(catalogs.router)
app.include_router(runs.router)
