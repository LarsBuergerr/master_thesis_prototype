"""Backend configuration — environment-driven with sensible local defaults."""

from __future__ import annotations

import os
from pathlib import Path

# Project root (one level above this file's package).
ROOT = Path(__file__).resolve().parent.parent

# SQLite database file for job persistence.
DB_PATH = Path(os.environ.get("ANALYZER_DB_PATH", ROOT / "backend" / "analyzer.db"))

# How many analysis jobs run concurrently (each job processes its files
# sequentially; the analyzer parallelises dimensions internally per file).
JOB_WORKERS = int(os.environ.get("ANALYZER_JOB_WORKERS", "2"))

# Upload guard rails.
MAX_UPLOAD_BYTES = int(os.environ.get("ANALYZER_MAX_UPLOAD_BYTES", str(25 * 1024 * 1024)))
MAX_FILES_PER_JOB = int(os.environ.get("ANALYZER_MAX_FILES", "50"))

# CORS origins allowed to call the API (comma-separated). Defaults cover the
# Vite dev server.
CORS_ORIGINS = [
    o.strip()
    for o in os.environ.get(
        "ANALYZER_CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if o.strip()
]
