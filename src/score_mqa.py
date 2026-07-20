"""CLI runner for the MQA baseline scorer (see ``mqa/scorer.py``).

Scores RDF dataset files with the data.europa.eu MQA metric so the result can be
compared against the prototype's own scores on the same input.

Usage (from the repo root):

    python src/score_mqa.py data/extreme_cases
    python src/score_mqa.py data/extreme_cases --no-probe -o outputs/runs/mqa.json
    python src/score_mqa.py data/extreme_cases/good_01.rdf

``--no-probe`` skips all HTTP requests; the URL-status metrics then score 0
(use it for fast, offline runs).
"""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from extraction.dataset_context import DatasetContext
from extraction.distribution_probes import attach_probes
from extraction.rdf_parser import RDFMetadataParser
from mqa.scorer import MqaOptions, score_dataset

logger = logging.getLogger("mqa")


def score_file(path: Path, *, probe: bool, options: MqaOptions) -> dict:
    """Parse one RDF file and return its MQA result dict."""
    graph = RDFMetadataParser.parse_file(str(path))
    context = DatasetContext.from_graph(graph)
    if probe:
        attach_probes(context, logger=logger)
    result = score_dataset(context, options)
    result["file"] = path.name
    return result


def _iter_files(target: Path, extensions: tuple[str, ...]) -> list[Path]:
    if target.is_file():
        return [target]
    return sorted(p for p in target.rglob("*") if p.suffix.lower() in extensions)


def main() -> None:
    parser = argparse.ArgumentParser(description="MQA baseline scorer")
    parser.add_argument("path", type=Path, help="RDF file or directory")
    parser.add_argument(
        "-e",
        "--extensions",
        default=".rdf",
        help="comma-separated file extensions to scan in a directory (default: .rdf)",
    )
    parser.add_argument("--no-probe", action="store_true", help="skip HTTP URL checks")
    parser.add_argument(
        "--dcat-ap-noncompliant",
        action="store_true",
        help="award 0 for dcat_ap_compliance instead of the default 30",
    )
    parser.add_argument("-o", "--output", type=Path, help="write full results as JSON")
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.WARNING, format="%(levelname)s %(name)s: %(message)s"
    )

    extensions = tuple(
        e if e.startswith(".") else f".{e}" for e in args.extensions.split(",")
    )
    files = _iter_files(args.path, extensions)
    if not files:
        parser.error(f"no files matching {extensions} under {args.path}")

    options = MqaOptions(dcat_ap_compliant=not args.dcat_ap_noncompliant)
    results = [score_file(f, probe=not args.no_probe, options=options) for f in files]

    width = max(len(r["file"]) for r in results)
    print(f"{'file':<{width}}  {'score':>7}  {'norm':>5}  rating")
    for r in results:
        print(
            f"{r['file']:<{width}}  {r['total']:>3}/{r['max']:<3}  {r['normalized']:>5}  {r['rating']}"
        )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(
            json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8"
        )
        print(f"\nwrote {len(results)} result(s) to {args.output}")


if __name__ == "__main__":
    main()
