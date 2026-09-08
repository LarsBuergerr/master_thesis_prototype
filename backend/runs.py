"""Zugriff auf abgeschlossene Bewertungsläufe — die Qualitätsebene.

Ein Lauf unter ``outputs/runs/<run>/`` enthält je verarbeiteter Datei ein
``result.json`` (``by_dimension`` + ``summary``). Genau das ist die Bewertung,
die sich über den Katalog legt (siehe backend/catalog.py) — verknüpft wird über
den **Dateinamen**, sonst nichts. Ein Lauf kennt keine Titel und Schlagwörter,
ein Katalog keine Scores.

Zwei Granularitäten, absichtlich getrennt:

``run_index``   — je Datei nur Gesamtscore, Dimensionswerte und Statuszählung.
                  Das braucht die Liste bzw. das Dashboard, und es bleibt klein
                  genug, um es am Stück auszuliefern.
``run_result``  — das vollständige Ergebnis einer Datei, für die Detailseite.
                  Einzelergebnisse sind je nach Datensatz einige hundert KB;
                  alle 50 zusammen will niemand übertragen.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Optional

from . import settings

logger = logging.getLogger("backend.runs")

#: run-Verzeichnis -> Index. Läufe sind nach dem Schreiben unveränderlich,
#: der Cache braucht daher keine Invalidierung.
_INDEX_CACHE: dict[str, list[dict[str, Any]]] = {}


def resolve_run(name: str) -> Path:
    """Laufnamen auf ein Verzeichnis unterhalb von RUNS_ROOT abbilden."""
    if "/" in name or "\\" in name or name.startswith("."):
        raise ValueError(f"Invalid run name: {name}")
    root = settings.RUNS_ROOT.resolve()
    path = (root / name).resolve()
    if path.parent != root or not path.is_dir():
        raise FileNotFoundError(f"Run not found: {name}")
    return path


def _result_paths(run_dir: Path) -> list[Path]:
    return sorted(run_dir.glob("*/result.json"))


def _summary_row(result_path: Path, data: dict[str, Any]) -> dict[str, Any]:
    """Indexzeile einer Datei: Score, Dimensionen, Statuszählung."""
    summary = data.get("summary") or {}
    counts = {"pass": 0, "partial": 0, "fail": 0, "other": 0}
    for dim in (data.get("by_dimension") or {}).values():
        for indicator in dim.get("indicators", []):
            status = indicator.get("status")
            counts[status if status in counts else "other"] += 1

    return {
        # Der Lauf legt je Datei ein Verzeichnis mit dem Dateistamm an; der
        # Katalog kennt den vollen Dateinamen. Beide Formen mitgeben, damit die
        # Zuordnung nicht von der Endung abhängt.
        "stem": result_path.parent.name,
        "overall": summary.get("overall_score"),
        "grade": summary.get("quality_grade"),
        "dims": summary.get("dimension_scores") or {},
        "dim_weights": summary.get("effective_dimension_weights")
        or summary.get("dimension_weights")
        or {},
        "total_indicators": summary.get("total_indicators", 0),
        "n_pass": counts["pass"],
        "n_partial": counts["partial"],
        "n_fail": counts["fail"] + counts["other"],
    }


def run_index(name: str) -> list[dict[str, Any]]:
    """Kompakte Bewertungsübersicht aller Dateien eines Laufs."""
    if name in _INDEX_CACHE:
        return _INDEX_CACHE[name]

    run_dir = resolve_run(name)
    rows = []
    for result_path in _result_paths(run_dir):
        try:
            data = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            logger.warning("Unreadable result %s (%s)", result_path, e)
            continue
        rows.append(_summary_row(result_path, data))

    _INDEX_CACHE[name] = rows
    return rows


def run_result(name: str, stem: str) -> dict[str, Any]:
    """Vollständiges Ergebnis einer Datei aus einem Lauf."""
    run_dir = resolve_run(name)
    if "/" in stem or "\\" in stem or stem.startswith("."):
        raise ValueError(f"Invalid file name: {stem}")
    # Der Katalog liefert Dateinamen mit Endung, der Lauf legt Verzeichnisse
    # ohne an — beide Schreibweisen akzeptieren.
    candidates = [stem, Path(stem).stem]
    for candidate in candidates:
        path = (run_dir / candidate / "result.json").resolve()
        if path.is_file() and path.parent.parent == run_dir.resolve():
            return json.loads(path.read_text(encoding="utf-8"))
    raise FileNotFoundError(f"No result for {stem} in run {name}")


#: run-Verzeichnis -> Mängelstatistik. Wie der Index unveränderlich.
_DEFICIT_CACHE: dict[str, list[dict[str, Any]]] = {}


def deficits(name: str) -> list[dict[str, Any]]:
    """Je Indikator, wie oft er über den Lauf hinweg nicht erfüllt wurde.

    Die Rangliste der häufigsten Mängel braucht die Indikator-Ebene, die der
    Index bewusst nicht trägt. Sie hier zu aggregieren kostet einmal das Lesen
    des Laufs und liefert ein paar Kilobyte — die Alternative wäre, im Frontend
    50 Einzelergebnisse zu laden, nur um sie zu zählen.
    """
    if name in _DEFICIT_CACHE:
        return _DEFICIT_CACHE[name]

    run_dir = resolve_run(name)
    counts: dict[str, dict[str, Any]] = {}
    for result_path in _result_paths(run_dir):
        try:
            data = json.loads(result_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for dim in (data.get("by_dimension") or {}).values():
            for indicator in dim.get("indicators", []):
                entry = counts.setdefault(
                    indicator["indicator_id"],
                    {
                        "indicator_id": indicator["indicator_id"],
                        "dimension": dim.get("dimension"),
                        "fail": 0,
                        "partial": 0,
                        "total": 0,
                    },
                )
                entry["total"] += 1
                status = indicator.get("status")
                if status == "fail":
                    entry["fail"] += 1
                elif status == "partial":
                    entry["partial"] += 1

    rows = sorted(
        counts.values(),
        key=lambda e: (e["fail"] + e["partial"]) / e["total"] if e["total"] else 0,
        reverse=True,
    )
    _DEFICIT_CACHE[name] = rows
    return rows


def _run_meta(run_dir: Path) -> dict[str, Any]:
    """Konfigurationseckdaten eines Laufs aus seiner ``metadata.json``."""
    meta_path = run_dir / "metadata.json"
    info: dict[str, Any] = {"directory": None, "llm_model": None, "dimensions": []}
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return info

    state = (meta.get("config") or {}).get("state") or meta.get("config") or {}
    quality = state.get("quality") or {}
    llm = state.get("llm") or {}
    info["directory"] = (meta.get("input") or {}).get("directory")
    info["llm_model"] = llm.get("model") if llm.get("enabled") else None
    info["dimensions"] = list(quality.get("dimension_whitelist") or [])
    return info


def list_runs() -> list[dict[str, Any]]:
    """Verfügbare Läufe, neueste zuerst.

    Mitgeliefert wird, was für die Auswahl zählt: über welches Verzeichnis der
    Lauf lief, wie viele Dateien er umfasst und ob ein Sprachmodell beteiligt
    war — sonst wählt man einen Lauf aus, der gar nicht zum geladenen Katalog
    passt.
    """
    root = settings.RUNS_ROOT
    if not root.is_dir():
        logger.warning("Runs root missing: %s", root)
        return []

    runs = []
    for entry in sorted(root.iterdir(), key=lambda p: p.name, reverse=True):
        if not entry.is_dir():
            continue
        results = _result_paths(entry)
        if not results:
            continue
        meta = _run_meta(entry)
        runs.append(
            {
                "name": entry.name,
                "dataset_count": len(results),
                "directory": meta["directory"],
                "llm_model": meta["llm_model"],
                "dimensions": meta["dimensions"],
            }
        )
    return runs


def _timestamp_from_name(name: str) -> Optional[str]:
    """``run_2026-07-27_09-54-46_…`` -> ``2026-07-27 09:54``."""
    parts = name.split("_")
    if len(parts) < 3:
        return None
    date, clock = parts[1], parts[2].replace("-", ":")
    return f"{date} {clock[:5]}"


def trend(catalog_directory: str) -> list[dict[str, Any]]:
    """Mittlerer Gesamtscore je Lauf über dieses Datenverzeichnis, chronologisch.

    Für einen Portalbetreiber ist die interessante Frage nicht der Stand eines
    einzelnen Laufs, sondern die Richtung: Wird die Metadatenqualität besser
    oder schlechter? Solange dieselbe Momentaufnahme mehrfach bewertet wird,
    zeigt die Kurve allerdings die Streuung des Verfahrens und nicht die des
    Portals — erst wiederholte Ernten desselben Bestands machen daraus einen
    Qualitätsverlauf. Die Oberfläche weist genau darauf hin.
    """
    rows = []
    for run in list_runs():
        directory = run.get("directory") or ""
        if not directory or Path(directory).name != Path(catalog_directory).name:
            continue
        index = run_index(run["name"])
        scores = [r["overall"] for r in index if r.get("overall") is not None]
        if not scores:
            continue
        rows.append(
            {
                "run": run["name"],
                "timestamp": _timestamp_from_name(run["name"]),
                "dataset_count": len(scores),
                "mean_overall": sum(scores) / len(scores),
                "min_overall": min(scores),
                "max_overall": max(scores),
                "llm_model": run.get("llm_model"),
            }
        )
    # list_runs liefert absteigend; für einen Verlauf ist aufsteigend richtig.
    return sorted(rows, key=lambda r: r["run"])


def matching_run(catalog_directory: str) -> Optional[str]:
    """Neuester Lauf, der über dieses Datenverzeichnis lief (oder ``None``)."""
    for run in list_runs():
        directory = run.get("directory") or ""
        if directory and Path(directory).name == Path(catalog_directory).name:
            return run["name"]
    return None
