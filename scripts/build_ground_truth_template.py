#!/usr/bin/env python3
"""Build a BLIND ground-truth rating template for a sample.

For every RDF dataset in a sample directory this extracts the facts a human
needs to rate quality (title, description, keywords, themes, formats, licence,
URLs, distribution count) and writes ``ground_truth_template.csv`` with empty
0-3 rating columns. It deliberately does NOT include the model's scores, so the
manual rating stays blind (no anchoring bias) — see
``docs/methodik_evaluation_ground_truth``.

Rating columns to fill (0=nicht, 1=schwach, 2=teilweise, 3=gut erfüllt):
  gt_findability, gt_accessibility, gt_reusability, gt_expressiveness, gt_notes

Usage (from repo root):
    python3 scripts/build_ground_truth_template.py                       # newest data/sample_*
    python3 scripts/build_ground_truth_template.py data/sample_2026-06-18_13-45
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from extraction.dataset_context import DatasetContext  # noqa: E402
from extraction.rdf_parser import RDFMetadataParser  # noqa: E402


def _last_segment(uri: str) -> str:
    return uri.rstrip("/").rsplit("/", 1)[-1] if uri else uri


def _license_label(uri: str) -> str:
    """Readable licence label: last two path segments (e.g. 'dl-by-de/2.0')."""
    parts = uri.rstrip("/").rsplit("/", 2)
    return "/".join(parts[-2:]) if len(parts) >= 2 else uri


def _short(text: str, n: int = 300) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= n else text[: n - 1] + "…"


def _facts(path: Path) -> dict:
    ctx = DatasetContext.from_graph(RDFMetadataParser.parse_file(str(path)))
    return {
        "title": _short(ctx.titles[0] if ctx.titles else "", 160),
        "description": _short(ctx.descriptions[0] if ctx.descriptions else "", 400),
        "keywords": ", ".join(ctx.keywords[:15]),
        "themes": ", ".join(_last_segment(t) for t in ctx.themes),
        "n_distributions": ctx.distribution_count,
        "formats": ", ".join(sorted({_last_segment(f) for f in ctx.all_distribution_formats})),
        "licenses": ", ".join(sorted({_license_label(sv.value) for sv in ctx.collect_licenses()})),
        "access_rights": ", ".join(_last_segment(a) for a in ctx.access_rights),
        "has_download_url": bool(ctx.all_download_urls),
        "has_access_url": bool(ctx.all_access_urls),
        "example_url": (ctx.all_download_urls or ctx.all_access_urls or [""])[0],
        "publisher": ", ".join(_last_segment(p) for p in ctx.publishers),
        "has_contact": bool(ctx.contact_points),
    }


def _load_manifest(sample_dir: Path) -> dict:
    """Map .rdf filename -> manifest row (strata, dataset_id, name), if present."""
    manifest = sample_dir / "sample_manifest.csv"
    if not manifest.exists():
        return {}
    out = {}
    with manifest.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fp = row.get("file_path", "")
            out[Path(fp).name] = row
    return out


def _newest_sample() -> Path:
    samples = sorted((REPO / "data").glob("sample_*"))
    if not samples:
        raise SystemExit("no data/sample_* directory found")
    return samples[-1]


RATING_COLS = ["gt_findability", "gt_accessibility", "gt_reusability", "gt_expressiveness", "gt_notes"]


def _landing_page(manifest_row: dict) -> str:
    """GovData landing page for the dataset, if its name is known."""
    name = manifest_row.get("dataset_name")
    return f"https://www.govdata.de/dataset/{name}" if name else ""


def main() -> None:
    ap = argparse.ArgumentParser(description="Build a ground-truth rating template")
    ap.add_argument("sample_dir", nargs="?", default=None, help="sample dir (default: newest data/sample_*)")
    ap.add_argument(
        "--slim",
        action="store_true",
        help="minimal template: only file, rdf_path, landing_page + empty rating columns",
    )
    args = ap.parse_args()

    sample_dir = Path(args.sample_dir) if args.sample_dir else _newest_sample()
    if not sample_dir.is_absolute():
        sample_dir = REPO / sample_dir
    files = sorted(sample_dir.glob("*.rdf"))
    if not files:
        raise SystemExit(f"no .rdf files in {sample_dir}")

    manifest = _load_manifest(sample_dir)
    rows = []
    for path in files:
        m = manifest.get(path.name, {})
        # Direct pointers to the actual record (the RDF the model sees + the
        # human-facing GovData page), so rating from the real dataset is easy.
        base = {
            "file": path.name,
            "rdf_path": str(path.relative_to(REPO)),
            "landing_page": _landing_page(m),
        }
        if args.slim:
            rows.append({**base, **{c: "" for c in RATING_COLS}})
            continue
        try:
            facts = _facts(path)
        except Exception as exc:  # keep the row, flag the parse error
            facts = {"title": f"<parse error: {exc}>"}
        rows.append(
            {
                **base,
                "dataset_id": m.get("dataset_id", ""),
                "primary_stratum": m.get("primary_stratum", ""),
                "secondary_stratum": m.get("secondary_stratum", ""),
                **facts,
                **{c: "" for c in RATING_COLS},
            }
        )

    fieldnames = list(rows[0].keys())
    name = "ground_truth_template_slim.csv" if args.slim else "ground_truth_template.csv"
    out_path = sample_dir / name
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"wrote {len(rows)} rows -> {out_path}")
    print(f"fill the 0-3 columns: {', '.join(RATING_COLS[:-1])} (+ gt_notes)")


if __name__ == "__main__":
    main()
