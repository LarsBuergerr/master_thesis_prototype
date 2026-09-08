"""SQLite-backed job store and a thread-pool runner for analysis jobs.

An analysis job processes one or more uploaded RDF files with a shared config.
Jobs run in a background thread pool (the work is blocking: rdflib parsing, HTTP
probes, LLM calls) and report progress that the frontend polls. State is
persisted to SQLite so the run history survives — and a restart shows queued/
running jobs as stale rather than losing them silently.
"""

from __future__ import annotations

import json
import logging
import sqlite3
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from .analysis_adapter import analyze_bytes, build_service
from .schemas import AnalysisConfig

logger = logging.getLogger("backend.jobs")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class JobStore:
    """Thread-safe persistence for jobs (one SQLite file)."""

    def __init__(self, db_path: Path):
        self._db_path = Path(db_path)
        self._db_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self._db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def _init_schema(self) -> None:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS jobs (
                    id           TEXT PRIMARY KEY,
                    status       TEXT NOT NULL,
                    created_at   TEXT NOT NULL,
                    updated_at   TEXT NOT NULL,
                    total        INTEGER NOT NULL DEFAULT 0,
                    done         INTEGER NOT NULL DEFAULT 0,
                    current_file TEXT,
                    error        TEXT,
                    config_json  TEXT NOT NULL,
                    files_json   TEXT NOT NULL,
                    results_json TEXT NOT NULL DEFAULT '[]'
                )
                """
            )

    # -- writes --------------------------------------------------------------

    def create(self, files: list[str], config: AnalysisConfig) -> str:
        job_id = uuid.uuid4().hex
        now = _now()
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO jobs (id, status, created_at, updated_at, total, done,
                                  current_file, error, config_json, files_json, results_json)
                VALUES (?, 'queued', ?, ?, ?, 0, NULL, NULL, ?, ?, '[]')
                """,
                (
                    job_id,
                    now,
                    now,
                    len(files),
                    config.model_dump_json(),
                    json.dumps(files),
                ),
            )
        return job_id

    def _set(self, job_id: str, **fields: Any) -> None:
        if not fields:
            return
        fields["updated_at"] = _now()
        cols = ", ".join(f"{k} = ?" for k in fields)
        with self._lock, self._connect() as conn:
            conn.execute(
                f"UPDATE jobs SET {cols} WHERE id = ?",
                (*fields.values(), job_id),
            )

    def mark_running(self, job_id: str, current_file: Optional[str]) -> None:
        self._set(job_id, status="running", current_file=current_file)

    def set_current_file(self, job_id: str, filename: Optional[str]) -> None:
        self._set(job_id, current_file=filename)

    def append_result(
        self,
        job_id: str,
        filename: str,
        result: Optional[dict[str, Any]],
        error: Optional[str],
    ) -> None:
        """Append one file's result and bump the done counter atomically."""
        with self._lock, self._connect() as conn:
            row = conn.execute(
                "SELECT done, results_json FROM jobs WHERE id = ?", (job_id,)
            ).fetchone()
            if row is None:
                return
            results = json.loads(row["results_json"])
            results.append(
                {"filename": filename, "result": result, "error": error}
            )
            conn.execute(
                "UPDATE jobs SET done = ?, results_json = ?, updated_at = ? WHERE id = ?",
                (row["done"] + 1, json.dumps(results), _now(), job_id),
            )

    def mark_done(self, job_id: str) -> None:
        self._set(job_id, status="done", current_file=None)

    def mark_error(self, job_id: str, error: str) -> None:
        self._set(job_id, status="error", error=error, current_file=None)

    # -- reads ---------------------------------------------------------------

    @staticmethod
    def _row_to_dict(row: sqlite3.Row, *, include_results: bool) -> dict[str, Any]:
        data: dict[str, Any] = {
            "job_id": row["id"],
            "status": row["status"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "progress": {
                "done": row["done"],
                "total": row["total"],
                "current_file": row["current_file"],
            },
            "files": json.loads(row["files_json"]),
            "error": row["error"],
        }
        if include_results:
            data["config"] = json.loads(row["config_json"])
            data["results"] = json.loads(row["results_json"])
        return data

    def get(self, job_id: str, *, include_results: bool = True) -> Optional[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        return self._row_to_dict(row, include_results=include_results) if row else None

    def list(self, limit: int = 50) -> list[dict[str, Any]]:
        with self._lock, self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM jobs ORDER BY created_at DESC LIMIT ?", (limit,)
            ).fetchall()
        return [self._row_to_dict(r, include_results=False) for r in rows]


class JobRunner:
    """Submits jobs to a thread pool and drives the store updates."""

    def __init__(self, store: JobStore, max_workers: int):
        self._store = store
        self._executor = ThreadPoolExecutor(
            max_workers=max_workers, thread_name_prefix="analysis"
        )

    def submit(
        self,
        job_id: str,
        files: list[tuple[str, bytes]],
        config: AnalysisConfig,
    ) -> None:
        self._executor.submit(self._run, job_id, files, config)

    def _run(
        self, job_id: str, files: list[tuple[str, bytes]], config: AnalysisConfig
    ) -> None:
        try:
            service = build_service(config)
        except Exception as e:  # construction (e.g. bad config) — whole job fails
            logger.exception("Job %s: failed to build service", job_id)
            self._store.mark_error(job_id, f"Service construction failed: {e}")
            return

        first = files[0][0] if files else None
        self._store.mark_running(job_id, current_file=first)

        for filename, content in files:
            self._store.set_current_file(job_id, filename)
            try:
                result = analyze_bytes(service, content, filename)
                self._store.append_result(job_id, filename, result, None)
                logger.info("Job %s: scored %s", job_id, filename)
            except Exception as e:
                logger.exception("Job %s: failed on %s", job_id, filename)
                self._store.append_result(job_id, filename, None, str(e))

        self._store.mark_done(job_id)

    def shutdown(self) -> None:
        self._executor.shutdown(wait=False, cancel_futures=True)
