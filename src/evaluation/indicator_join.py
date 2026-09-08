"""Indicator-level join harness: prototype vs. MQA on the same RDF input.

This builds the central comparison artifact for thesis section 6.4:
a **long table with one row per (file × prototype indicator)** carrying both the
prototype's verdict and the corresponding MQA metric's verdict, tagged by the
A/B/C class from :mod:`evaluation.indicator_map`. From that single table the
three pieces of evidence fall out:

* **A** — agreement rate (do the shared checks converge? H1).
* **B** — the ``MQA PASS & Prototyp FAIL/PARTIAL`` contingency per indicator
  (where MQA *assumes* quality the prototype rejects → overestimation, H2).
* **C** — MQA has no metric; the prototype's score varies while MQA is flat
  (structural blindness, H2).

Both scorers read the prototype's own :class:`DatasetContext` with the **same**
probes attached, so the input is identical — the only difference is the check.

Stats/aggregation are pure pandas. The model side reuses
:func:`evaluation.ground_truth.make_llm` for the expressiveness (C) indicators.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from evaluation.indicator_map import MAPPING, mapping_df, mqa_only_metrics

# status → "full pass" boolean for the contingency analysis.
#   pass → True ; fail/partial → False ; not_applicable/error → NaN (excluded)
_PASS = "pass"
_NOT_COUNTED = {"not_applicable", "error"}


# ---------------------------------------------------------------------------
# 1. Score both models on the same input
# ---------------------------------------------------------------------------


def _context_with_probes(path: Path, probe: bool):
    """Parse one RDF into a DatasetContext, optionally attaching HTTP probes."""
    import logging

    from extraction.dataset_context import DatasetContext
    from extraction.distribution_probes import attach_probes
    from extraction.rdf_parser import RDFMetadataParser

    ctx = DatasetContext.from_graph(RDFMetadataParser.parse_file(str(path)))
    if probe and ctx.distribution_count:
        attach_probes(ctx, logger=logging.getLogger("indicator_join"))
    return ctx


def run_mqa_metrics(
    sample_dir, *, probe: bool = True, dcat_ap_compliant: bool = True, mqa_options=None
) -> pd.DataFrame:
    """Long MQA table: one row per (file, mqa_metric) with ``mqa_passed``."""
    from mqa.scorer import MqaOptions, score_dataset

    if mqa_options is not None:
        opts = mqa_options
    else:
        opts = MqaOptions(dcat_ap_compliant=dcat_ap_compliant)
    files = sorted(Path(sample_dir).glob("*.rdf"))
    rows = []
    for i, path in enumerate(files, 1):
        ctx = _context_with_probes(path, probe)
        res = score_dataset(ctx, opts)
        for key, m in res["metrics"].items():
            rows.append(
                {
                    "file": path.name,
                    "mqa_metric": key,
                    "mqa_dimension": m["dimension"],
                    "mqa_passed": bool(m["passed"]),
                    "mqa_points": m["points"],
                    "mqa_max": m["max"],
                }
            )
        print(f"[MQA {i:2d}/{len(files)}] {path.name}")
    return pd.DataFrame(rows)


def run_model_indicators(
    sample_dir, llm=None, *, probe: bool = True, **service_kwargs
) -> pd.DataFrame:
    """Long prototype table: one row per (file, indicator) with status & score.

    ``model_pass`` is the binarised "full pass" (status==pass), with NaN for
    not_applicable/error so those are excluded from agreement counts.
    """
    from scoring.service import QualityMetricsService

    service = QualityMetricsService(llm=llm, **service_kwargs)
    files = sorted(Path(sample_dir).glob("*.rdf"))
    rows = []
    for i, path in enumerate(files, 1):
        result = service.validate_metadata(str(path))
        overall = result.get("summary", {}).get("overall_score")
        for dim, d in result.get("by_dimension", {}).items():
            for ind in d.get("indicators", []):
                status = ind.get("status")
                if status in _NOT_COUNTED or status is None:
                    model_pass = np.nan
                else:
                    model_pass = float(status == _PASS)
                rows.append(
                    {
                        "file": path.name,
                        "indicator": ind.get("indicator_id"),
                        "model_dimension": dim,
                        "model_status": status,
                        "model_score": ind.get("score"),
                        "model_pass": model_pass,
                        "model_overall": overall,
                    }
                )
        print(f"[model {i:2d}/{len(files)}] {path.name}")
    return pd.DataFrame(rows)


def load_model_indicators_from_run(run_dir, *, file_suffix: str = ".rdf") -> pd.DataFrame:
    """Load an **already-completed** prototype run into the same long table as
    :func:`run_model_indicators` — so the MQA comparison can reuse a finished run
    instead of re-scoring every file.

    Reads each ``<run_dir>/<dataset>/result.json`` (the per-dataset output written
    by a normal ``main.py`` run). ``file`` is set to ``<dataset><file_suffix>`` so
    it matches the MQA side, which keys on the RDF filename (default ``.rdf``).
    """
    import json

    run_dir = Path(run_dir)
    rows = []
    for result_path in sorted(run_dir.glob("*/result.json")):
        data = json.loads(result_path.read_text())
        file = result_path.parent.name + file_suffix
        overall = data.get("summary", {}).get("overall_score")
        for dim, d in data.get("by_dimension", {}).items():
            for ind in d.get("indicators", []):
                status = ind.get("status")
                if status in _NOT_COUNTED or status is None:
                    model_pass = np.nan
                else:
                    model_pass = float(status == _PASS)
                rows.append(
                    {
                        "file": file,
                        "indicator": ind.get("indicator_id"),
                        "model_dimension": dim,
                        "model_status": status,
                        "model_score": ind.get("score"),
                        "model_pass": model_pass,
                        "model_overall": overall,
                    }
                )
    if not rows:
        raise FileNotFoundError(
            f"No <dataset>/result.json found under {run_dir} — is this an outputs/runs run dir?"
        )
    n_files = len({r["file"] for r in rows})
    print(f"loaded model indicators from existing run: {run_dir} ({n_files} files)")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Join indicator ↔ MQA via the A/B/C mapping
# ---------------------------------------------------------------------------


def _agg_mqa(passed: list[bool], how: str):
    if not passed:
        return np.nan
    return float(all(passed)) if how == "all" else float(any(passed))


def build_join(model_long: pd.DataFrame, mqa_long: pd.DataFrame) -> pd.DataFrame:
    """Join the two long tables into one row per (file × prototype indicator).

    For each mapped indicator the MQA side is the aggregated PASS of its mapped
    MQA metric(s) (``any``/``all`` per the mapping). C-indicators have no MQA
    metric → ``mqa_pass = NaN``. Indicators present in the model output but not
    in the mapping are kept and flagged ``abc='?'`` (so nothing is dropped).
    """
    mqa_by_file: dict[str, dict[str, bool]] = {}
    for file, grp in mqa_long.groupby("file"):
        mqa_by_file[file] = dict(zip(grp["mqa_metric"], grp["mqa_passed"]))

    by_ind = {row["indicator"]: row for row in MAPPING}
    out = []
    for _, r in model_long.iterrows():
        file, ind = r["file"], r["indicator"]
        spec = by_ind.get(ind)
        metrics_for_file = mqa_by_file.get(file, {})
        if spec is None:
            abc, mqa_keys, agg, review, rationale = (
                "?",
                [],
                "any",
                False,
                "UNMAPPED — add to indicator_map",
            )
        else:
            abc, mqa_keys, agg = spec["abc"], spec["mqa"], spec["mqa_agg"]
            review, rationale = spec["review"], spec["rationale"]
        mqa_flags = [
            bool(metrics_for_file[k]) for k in mqa_keys if k in metrics_for_file
        ]
        out.append(
            {
                "file": file,
                "indicator": ind,
                "abc": abc,
                "dimension": r["model_dimension"],
                "model_status": r["model_status"],
                "model_score": r["model_score"],
                "model_pass": r["model_pass"],
                "mqa_metrics": ";".join(mqa_keys),
                "mqa_pass": _agg_mqa(mqa_flags, agg),
                "review": review,
                "rationale": rationale,
            }
        )
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------
# 3. Per-class evidence
# ---------------------------------------------------------------------------


def class_a_agreement(join: pd.DataFrame) -> dict:
    """H1: on shared (A) checks, how often do MQA and prototype agree?"""
    a = join[
        (join["abc"] == "A") & join["model_pass"].notna() & join["mqa_pass"].notna()
    ]
    if a.empty:
        return {"n": 0, "agreement": float("nan")}
    agree = (a["model_pass"] == a["mqa_pass"]).mean()
    both = int(((a["model_pass"] == 1) & (a["mqa_pass"] == 1)).sum())
    neither = int(((a["model_pass"] == 0) & (a["mqa_pass"] == 0)).sum())
    mqa_only = int(((a["model_pass"] == 0) & (a["mqa_pass"] == 1)).sum())
    model_only = int(((a["model_pass"] == 1) & (a["mqa_pass"] == 0)).sum())
    return {
        "n": int(len(a)),
        "agreement": float(agree),
        "both_pass": both,
        "both_fail": neither,
        "mqa_pass_model_fail": mqa_only,
        "model_pass_mqa_fail": model_only,
    }


def class_b_overestimation(join: pd.DataFrame) -> pd.DataFrame:
    """H2: per B-indicator contingency. ``mqa_pass_model_fail`` = the count of
    datasets where MQA awards points but the prototype rejects (overestimation).
    """
    b = join[
        (join["abc"] == "B") & join["model_pass"].notna() & join["mqa_pass"].notna()
    ]
    rows = []
    for ind, g in b.groupby("indicator"):
        mp, qp = g["model_pass"], g["mqa_pass"]
        rows.append(
            {
                "indicator": ind,
                "n": int(len(g)),
                "mqa_pass_model_fail": int(
                    ((qp == 1) & (mp == 0)).sum()
                ),  # overestimation
                "both_pass": int(((qp == 1) & (mp == 1)).sum()),
                "both_fail": int(((qp == 0) & (mp == 0)).sum()),
                "model_pass_mqa_fail": int(((qp == 0) & (mp == 1)).sum()),
                "review": bool(g["review"].iloc[0]),
            }
        )
    df = pd.DataFrame(rows)
    if not df.empty:
        df["overestimation_rate"] = df["mqa_pass_model_fail"] / df["n"]
        df = df.sort_values("mqa_pass_model_fail", ascending=False, ignore_index=True)
    return df


def class_c_blindness(join: pd.DataFrame) -> pd.DataFrame:
    """H2: per C-indicator, the prototype's score distribution while MQA is flat
    (no metric). A wide spread / low mean = the prototype reacts where MQA can't.
    """
    c = join[(join["abc"] == "C") & join["model_score"].notna()]
    rows = []
    for ind, g in c.groupby("indicator"):
        s = pd.to_numeric(g["model_score"], errors="coerce").dropna()
        if s.empty:
            continue
        rows.append(
            {
                "indicator": ind,
                "n": int(len(s)),
                "model_score_mean": float(s.mean()),
                "model_score_std": float(s.std(ddof=0)),
                "model_score_min": float(s.min()),
                "model_score_max": float(s.max()),
                "n_below_0_5": int((s < 0.5).sum()),
                "mqa_metric": "—",
            }
        )
    return (
        pd.DataFrame(rows).sort_values("model_score_mean", ignore_index=True)
        if rows
        else pd.DataFrame()
    )


def summarise(join: pd.DataFrame) -> dict:
    """All three evidence tables + the MQA-only balance, in one dict."""
    return {
        "class_a": class_a_agreement(join),
        "class_b": class_b_overestimation(join),
        "class_c": class_c_blindness(join),
        "mqa_only_metrics": mqa_only_metrics(),
        "unmapped_indicators": sorted(
            join.loc[join["abc"] == "?", "indicator"].unique().tolist()
        ),
        "class_counts": join.drop_duplicates("indicator")["abc"]
        .value_counts()
        .to_dict(),
    }


# ---------------------------------------------------------------------------
# 4. One-call pipeline with caching
# ---------------------------------------------------------------------------


def build_all(
    sample_dir,
    llm=None,
    *,
    probe: bool = True,
    recompute: bool = False,
    output_dir=None,
    mqa_options=None,
    model_run_dir=None,
    **service_kwargs,
) -> dict:
    """Score both models (cached), join, and compute the evidence tables.

    Caches and writes all CSVs to ``output_dir`` (defaults to ``sample_dir``).
    Returns ``{"join": df, **summarise(join)}``.

    Only MQA is ever scored here. For the prototype side there are three sources
    (first available wins): the ``model_indicators.csv`` cache → an already-run
    prototype run (``model_run_dir``, no re-scoring) → a fresh in-process scoring
    of ``sample_dir`` via :class:`QualityMetricsService`.
    """
    sample_dir = Path(sample_dir)
    out = Path(output_dir) if output_dir is not None else sample_dir
    out.mkdir(parents=True, exist_ok=True)

    model_csv = out / "model_indicators.csv"
    mqa_csv = out / "mqa_metrics.csv"

    if model_csv.exists() and not recompute:
        model_long = pd.read_csv(model_csv)
        print(f"cache: {model_csv}")
        # Older caches predate the model_overall column; refresh from the run
        # dir if one is available so the overall-score comparison has data.
        if "model_overall" not in model_long.columns and model_run_dir is not None:
            print("cache lacks model_overall — reloading from run dir")
            model_long = load_model_indicators_from_run(model_run_dir)
            model_long.to_csv(model_csv, index=False)
    elif model_run_dir is not None:
        model_long = load_model_indicators_from_run(model_run_dir)
        model_long.to_csv(model_csv, index=False)
    else:
        model_long = run_model_indicators(
            sample_dir, llm=llm, probe=probe, **service_kwargs
        )
        model_long.to_csv(model_csv, index=False)

    if mqa_csv.exists() and not recompute:
        mqa_long = pd.read_csv(mqa_csv)
        print(f"cache: {mqa_csv}")
    else:
        mqa_long = run_mqa_metrics(sample_dir, probe=probe, mqa_options=mqa_options)
        mqa_long.to_csv(mqa_csv, index=False)

    join = build_join(model_long, mqa_long)
    join.to_csv(out / "indicator_join.csv", index=False)
    return {"join": join, **summarise(join)}
