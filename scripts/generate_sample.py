#!/usr/bin/env python3
"""Generate a stratified GovData reference sample using notebook 07.

Faithfully executes the sampling pipeline defined in
``playground/notebooks/07_fetch_and_analyze_ckan_catalog.ipynb`` — it runs the
notebook's *actual* cell sources (load CKAN snapshot -> detect geo vs non-geo by
distribution format -> stratified draw over geo/non_geo x top-4 publishers ->
fetch each dataset's RDF/XML) and writes ``data/sample_<timestamp>/`` plus a
``sample_manifest.csv``.

Running the real cells (instead of a re-typed copy) keeps it 1:1 with the
notebook while staying reproducible and parameterisable.

Usage (from the repo root):
    python3 scripts/generate_sample.py                 # seed 67, size 50
    python3 scripts/generate_sample.py --size 50 --seed 67
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
NB = REPO / "playground" / "notebooks" / "07_fetch_and_analyze_ckan_catalog.ipynb"
NB_DIR = NB.parent  # the notebook uses paths relative to its own directory

# Dependency chain of cells: load snapshot -> df, geo detection,
# geo_dataset_indices, stratified draw + RDF fetch.
CELLS = [11, 14, 23, 26]

# Imports the above cells rely on having been run earlier in the notebook.
PREAMBLE = "import json\nimport pandas as pd\nfrom pathlib import Path\n"


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate a stratified GovData sample (notebook 07)")
    ap.add_argument("--seed", type=int, default=67, help="RANDOM_SEED (default 67)")
    ap.add_argument("--size", type=int, default=50, help="SAMPLE_SIZE (default 50)")
    ap.add_argument("--per-secondary", type=int, default=5, help="SAMPLES_PER_SECONDARY (default 5)")
    args = ap.parse_args()

    nb = json.loads(NB.read_text(encoding="utf-8"))
    sources = {i: "".join(nb["cells"][i]["source"]) for i in CELLS}

    # Inject the requested sampling parameters into cell 26.
    src26 = sources[26]
    src26 = re.sub(r"RANDOM_SEED\s*=\s*\d+", f"RANDOM_SEED = {args.seed}", src26, count=1)
    src26 = re.sub(r"SAMPLE_SIZE\s*=\s*\d+", f"SAMPLE_SIZE = {args.size}", src26, count=1)
    src26 = re.sub(
        r"SAMPLES_PER_SECONDARY\s*=\s*\d+",
        f"SAMPLES_PER_SECONDARY = {args.per_secondary}",
        src26,
        count=1,
    )
    sources[26] = src26

    ns: dict = {"__name__": "__sample__"}
    exec(compile(PREAMBLE, "<preamble>", "exec"), ns)

    os.chdir(NB_DIR)  # so the cells' relative paths resolve (data/raw, ../../data)
    for i in CELLS:
        print(f"\n{'#' * 20} notebook cell {i} {'#' * 20}")
        exec(compile(sources[i], f"<07_notebook cell {i}>", "exec"), ns)


if __name__ == "__main__":
    main()
