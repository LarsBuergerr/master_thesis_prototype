#!/usr/bin/env python3
"""Attach real indicator findings to the portal's bundled evaluation data.

``frontend/src/portal/data/evaluation.json`` carries the scores of the
evaluation sample (n = 50). Scores alone cannot tell a data provider *what* is
wrong, so this script copies the ``message_de``, ``details`` and
``remediation`` payloads of the reference run onto every indicator entry — the
same fields the backend returns live. The portal therefore shows identical,
fully explained findings whether or not the API is reachable.

Der aufbereitete Befund (``finding``) wird dabei nicht kopiert, sondern mit
:func:`scoring.findings.build_finding` **aus den Details erzeugt** — also mit
demselben Backend-Code, den ein Live-Lauf benutzt. Der Referenzlauf ist älter
als dieses Feld, und eine zweite Implementierung würde auseinanderlaufen.

Payloads are trimmed (long lists capped, vocabulary candidates reduced to the
ones closest to the offending value) to keep the bundle small.

Usage (from repo root):
    python3 scripts/enrich_portal_evaluation.py
    python3 scripts/enrich_portal_evaluation.py --run outputs/runs/<run_dir>
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from core.dimension import QualityDimension  # noqa: E402
from core.indicator import IndicatorResult, IndicatorStatus  # noqa: E402
from scoring.findings import build_finding  # noqa: E402
from scoring.remediation.vocab_fields import rank_candidates  # noqa: E402

PORTAL_JSON = ROOT / "frontend" / "src" / "portal" / "data" / "evaluation.json"
DEFAULT_RUN = ROOT / "outputs" / "runs" / "run_2026-07-16_11-10-53_state-evaluation-final_EVAL_gpt5-5"

# Cap list-valued details so a single dataset cannot blow up the bundle.
MAX_LIST_ITEMS = 8
MAX_CANDIDATES = 8
MAX_SUGGESTIONS = 3
MAX_TEXT = 600


# details are shallow (dict → per_distribution list → entry dict → value list),
# so the guard only has to stop pathological nesting, not the payload itself.
MAX_DEPTH = 6


def _truncate(value: Any, depth: int = 0) -> Any:
    """Shrink a details payload: cap lists, strings and nesting depth."""
    if isinstance(value, str):
        return value if len(value) <= MAX_TEXT else value[:MAX_TEXT] + "…"
    if isinstance(value, list):
        if depth >= MAX_DEPTH:
            return []
        return [_truncate(v, depth + 1) for v in value[:MAX_LIST_ITEMS]]
    if isinstance(value, dict):
        if depth >= MAX_DEPTH:
            return {}
        return {k: _truncate(v, depth + 1) for k, v in value.items()}
    return value


def _shortlist(candidates: list[str], hints: list[str]) -> tuple[list[str], bool]:
    """Shortlist of vocabulary entries for the bundle, plus whether it is ranked.

    A controlled vocabulary can hold thousands of URIs (IANA media types) —
    far too many to bundle. Sorting uses the backend's own ``rank_candidates``
    so the stored suggestion matches what a live run would propose.
    """
    ranked_list, ranked = rank_candidates(candidates, hints)
    return ranked_list[:MAX_CANDIDATES], ranked


def _hints_from_details(details: dict[str, Any]) -> list[str]:
    """Values currently present in the metadata, used to rank candidates."""
    hints: list[str] = []
    for key in ("formats", "invalid", "values", "media_types"):
        value = details.get(key)
        if isinstance(value, list):
            hints += [v for v in value if isinstance(v, str)]
    for entry in details.get("per_distribution", []) or []:
        if isinstance(entry, dict):
            for key in ("formats", "media_types", "licenses", "availability"):
                value = entry.get(key)
                if isinstance(value, list):
                    hints += [v for v in value if isinstance(v, str)]
    return [h.rsplit("/", 1)[-1] for h in hints][:6]


def _trim_remediation(rem: dict[str, Any] | None, details: dict[str, Any]) -> dict[str, Any] | None:
    if not rem:
        return None
    rem = json.loads(json.dumps(rem))  # copy
    if rem.get("kind") == "change_patch":
        hints = _hints_from_details(details)
        rem["ready"] = rem.get("ready", [])[:MAX_LIST_ITEMS]
        trimmed = []
        for suggestion in rem.get("needs_input", [])[:MAX_SUGGESTIONS]:
            candidates = suggestion.get("candidates", [])
            suggestion["candidate_total"] = len(candidates)
            suggestion["candidates"], suggestion["ranked"] = _shortlist(candidates, hints)
            trimmed.append(suggestion)
        rem["needs_input"] = trimmed
    else:
        rem["findings"] = [_truncate(f) for f in rem.get("findings", [])[:MAX_LIST_ITEMS]]
        rem["message_de"] = _truncate(rem.get("message_de", ""))
        rem["message_en"] = _truncate(rem.get("message_en", ""))
    return rem


def _finding_for(source: dict[str, Any], details: dict[str, Any]) -> dict[str, Any] | None:
    """Befund über den Backend-Builder erzeugen (siehe Modul-Docstring)."""
    try:
        status = IndicatorStatus(source.get("status", "fail"))
    except ValueError:
        return None
    result = IndicatorResult(
        indicator_id=source["indicator_id"],
        name_de=source.get("name_de", ""),
        name_en=source.get("name_en", ""),
        dimension=QualityDimension(source.get("dimension", "findability")),
        status=status,
        score=source.get("score") or 0.0,
        message_de=source.get("message_de", ""),
        details=details,
        error=source.get("error"),
    )
    finding = build_finding(result)
    return finding.to_dict() if finding else None


def _load_run(run_dir: Path) -> dict[str, dict[str, dict[str, Any]]]:
    """run-directory name -> indicator_id -> indicator result."""
    by_file: dict[str, dict[str, dict[str, Any]]] = {}
    for result_path in run_dir.glob("*/result.json"):
        data = json.loads(result_path.read_text(encoding="utf-8"))
        indicators: dict[str, dict[str, Any]] = {}
        for dim in data.get("by_dimension", {}).values():
            for ind in dim.get("indicators", []):
                indicators[ind["indicator_id"]] = ind
        by_file[result_path.parent.name] = indicators
    return by_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, default=DEFAULT_RUN, help="reference run directory")
    parser.add_argument("--portal-json", type=Path, default=PORTAL_JSON)
    args = parser.parse_args()

    if not args.run.is_dir():
        print(f"Run directory not found: {args.run}", file=sys.stderr)
        return 1

    portal = json.loads(args.portal_json.read_text(encoding="utf-8"))
    runs = _load_run(args.run)
    print(f"Loaded {len(runs)} result files from {args.run.name}")

    missing_files: list[str] = []
    enriched = 0
    for dataset in portal["datasets"]:
        key = Path(dataset["file"]).stem
        indicators = runs.get(key)
        if indicators is None:
            missing_files.append(dataset["file"])
            continue
        for entry in dataset["indicators"]:
            source = indicators.get(entry["id"])
            if source is None:
                continue
            details = source.get("details") or {}
            entry["message"] = source.get("message_de", "")
            # Only failing/partial indicators need the full evidence — for a
            # passing one the message is the whole story, and carrying its
            # details would double the bundle for no user-visible gain.
            if source.get("status") in ("partial", "fail", "error"):
                # ``details`` selbst wandern nicht ins Bundle: die Oberfläche
                # liest sie nicht mehr, seit der Befund im Backend entsteht.
                trimmed = _truncate(details)
                entry["remediation"] = _trim_remediation(source.get("remediation"), details)
                entry["finding"] = _finding_for(source, trimmed)
            entry["weight"] = source.get("effective_weight", source.get("default_weight", 1.0))
            entry["rawScore"] = source.get("raw_score", entry.get("score"))
            entry["rawStatus"] = source.get("raw_status", entry.get("status"))
            enriched += 1

    if missing_files:
        print(f"WARNING: no run result for {len(missing_files)} file(s): {missing_files[:3]}")

    portal["source_run"] = args.run.name
    args.portal_json.write_text(
        json.dumps(portal, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    size_kb = args.portal_json.stat().st_size / 1024
    print(f"Enriched {enriched} indicator entries → {args.portal_json} ({size_kb:.0f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
