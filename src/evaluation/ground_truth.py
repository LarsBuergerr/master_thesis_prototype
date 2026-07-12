"""Compare a manual ground-truth rating against the prototype's scores.

Pipeline (used by ``playground/notebooks/10_ground_truth_evaluation.ipynb``):

1. ``run_model_scores(sample_dir, llm)`` — score every RDF with the prototype,
   returning the four dimension scores (0-1) per dataset. Alternatively
   ``load_model_scores(run_path)`` reuses an already-completed run's output
   (run directory or ``run_aggregate.json``) instead of re-scoring.
2. ``load_ground_truth(csv)`` — read the filled rating template (0-5 per
   dimension), derive the overall verdict via :func:`derive_verdict`.
3. ``merge_scores(...)`` — join, rescale model scores to 0-5, round them to the
   integer GT scale and derive the model's verdict with the *same* rule
   (principled mapping on the same discrete scale).
4. ``compare(...)`` — per-dimension rank correlation (Spearman, Kendall τ-b) and
   overall-grade agreement (accuracy, Cohen's κ, weighted κ, PABAK, bootstrap
   CI, confusion matrix).
   Primary metric: Spearman ρ (overall + per dimension, with ceiling analysis).
   Secondary metric: weighted Cohen's κ on the verdict (gut/mittel/schlecht) —
   report with PABAK and bootstrap CI: with a strongly imbalanced verdict
   distribution (real-world sample ⇒ mostly "mittel") κ is structurally capped
   and its point estimate carries little information (kappa paradox,
   Feinstein & Cicchetti 1990).
5. ``make_figures(...)`` — thesis-ready PNGs.

Stats are implemented in pure numpy/pandas (no scipy/sklearn dependency).

Scale: 0–5 per dimension (6 levels, forced-choice, anchored rubric).
See ``docs/methodik_evaluation_ground_truth_v3.md`` for full methodology.
"""

from __future__ import annotations

import math
import os
from pathlib import Path
from typing import Optional

import numpy as np
import pandas as pd

# GT rating column -> model dimension key.
DIM_MAP = {
    "gt_findability": "findability",
    "gt_accessibility": "accessibility",
    "gt_reusability": "reusability",
    "gt_expressiveness": "expressiveness",
}
MODEL_DIMS = list(DIM_MAP.values())
GT_COLS = list(DIM_MAP)
VERDICTS = ["schlecht", "mittel", "gut"]  # ordinal order (low -> high)

# ----------------------------------------------------------------------------
# Verdict rule (identical for human ratings and rescaled model scores)
# ----------------------------------------------------------------------------


def derive_verdict(dims: list[float]) -> Optional[str]:
    """Map four 0-5 dimension values to gut / mittel / schlecht.

    Rules (see docs/methodik_evaluation_ground_truth_v3.md):
      * gut      = Durchschnitt >= 4.0 und keine Dimension unter 3
      * schlecht = Durchschnitt <= 2.0 oder (Durchschnitt < 3.5 und
                   mindestens zwei Dimensionen unter 2)
      * mittel   = sonst
    Returns ``None`` if any dimension is missing (incomplete rating).
    """
    vals = [
        d
        for d in dims
        if d is not None and not (isinstance(d, float) and math.isnan(d))
    ]
    if len(vals) < len(dims):
        return None
    avg = sum(vals) / len(vals)
    below_3 = sum(1 for d in vals if d < 3)
    below_2 = sum(1 for d in vals if d < 2)
    if avg >= 4.0 and below_3 == 0:
        return "gut"
    if avg <= 2.0 or (avg < 3.5 and below_2 >= 2):
        return "schlecht"
    return "mittel"


# ----------------------------------------------------------------------------
# Pure-numpy statistics
# ----------------------------------------------------------------------------


def _clean_pair(x, y):
    x = pd.to_numeric(pd.Series(x).reset_index(drop=True), errors="coerce")
    y = pd.to_numeric(pd.Series(y).reset_index(drop=True), errors="coerce")
    mask = x.notna() & y.notna()
    return x[mask].to_numpy(float), y[mask].to_numpy(float)


def spearman(x, y) -> float:
    """Spearman rank correlation (rho)."""
    x, y = _clean_pair(x, y)
    if len(x) < 3 or len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        return float("nan")
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    return float(np.corrcoef(rx, ry)[0, 1])


def kendall_tau(x, y) -> float:
    """Kendall's tau-b (handles ties), O(n^2) — fine for sample sizes here."""
    x, y = _clean_pair(x, y)
    n = len(x)
    if n < 3:
        return float("nan")
    nc = nd = 0
    for i in range(n):
        dx = x[i] - x[i + 1 :]
        dy = y[i] - y[i + 1 :]
        s = np.sign(dx) * np.sign(dy)
        nc += int((s > 0).sum())
        nd += int((s < 0).sum())

    def tie_pairs(a):
        _, counts = np.unique(a, return_counts=True)
        return sum(c * (c - 1) / 2 for c in counts)

    n0 = n * (n - 1) / 2
    denom = math.sqrt((n0 - tie_pairs(x)) * (n0 - tie_pairs(y)))
    return (nc - nd) / denom if denom > 0 else float("nan")


def ceiling_spearman(model_scores, gt_scores) -> float:
    """Maximum achievable Spearman ρ given the observed GT value distribution.

    The GT scale is coarse (0-5 integers, often only 2-3 levels actually used)
    and the sample contains near-duplicate datasets, so even a *perfectly*
    monotone model cannot reach ρ = 1: ties and coarse binning attenuate the
    rank correlation. This computes that ceiling by assigning the observed GT
    value multiset to the datasets in perfect model-score order (best possible
    monotone alignment) and measuring the resulting Spearman.

    Reporting observed ρ against this ceiling separates "model disagrees with
    the human" from "the scale cannot express finer agreement". Within model-
    score ties the assignment is arbitrary, but Spearman is invariant to it
    (tied ranks are averaged), so the result is deterministic.
    """
    x, y = _clean_pair(model_scores, gt_scores)
    if len(x) < 3 or len(np.unique(x)) < 2 or len(np.unique(y)) < 2:
        return float("nan")
    order = np.argsort(x, kind="stable")
    y_best = np.empty_like(y)
    y_best[order] = np.sort(y)  # observed GT values, monotone in model score
    return spearman(x, y_best)


def cronbach_alpha(items: pd.DataFrame) -> float:
    """Cronbach's α over item columns (internal consistency of a composite).

    Used as the reliability estimate of ``gt_overall`` / ``model_overall``
    (mean of the four dimension values) for the classical disattenuation
    formula. Entirely-empty items (e.g. expressiveness scored without an LLM)
    are ignored; remaining rows with any missing item are dropped; needs
    >= 2 items.
    """
    items = items.dropna(axis=1, how="all").dropna()
    k = items.shape[1]
    if k < 2 or len(items) < 3:
        return float("nan")
    item_var = items.var(axis=0, ddof=1).sum()
    total_var = items.sum(axis=1).var(ddof=1)
    if total_var <= 0:
        return float("nan")
    return float(k / (k - 1) * (1 - item_var / total_var))


def disattenuated_correlation(r: float, rel_x: float, rel_y: float) -> float:
    """Spearman's classical correction for attenuation: r / sqrt(rel_x*rel_y).

    Estimates the correlation between the *latent* qualities given the
    unreliability of both measurements. Capped at 1.0 (the correction can
    overshoot with noisy reliability estimates).
    """
    if any(math.isnan(v) for v in (r, rel_x, rel_y)) or rel_x <= 0 or rel_y <= 0:
        return float("nan")
    return float(min(1.0, r / math.sqrt(rel_x * rel_y)))


def confusion_matrix(true_labels, pred_labels, labels=VERDICTS) -> pd.DataFrame:
    """Counts with rows=ground truth, cols=model. Fixed label order."""
    idx = {l: i for i, l in enumerate(labels)}
    m = np.zeros((len(labels), len(labels)), dtype=int)
    for t, p in zip(true_labels, pred_labels):
        if t in idx and p in idx:
            m[idx[t], idx[p]] += 1
    return pd.DataFrame(
        m, index=[f"GT:{l}" for l in labels], columns=[f"M:{l}" for l in labels]
    )


def cohen_kappa(
    true_labels, pred_labels, labels=VERDICTS, weights: Optional[str] = None
) -> float:
    """Cohen's kappa. ``weights='linear'`` gives the ordinal weighted kappa."""
    cm = confusion_matrix(true_labels, pred_labels, labels).to_numpy(float)
    n = cm.sum()
    if n == 0:
        return float("nan")
    k = len(labels)
    row, col = cm.sum(1), cm.sum(0)
    expected = np.outer(row, col) / n
    if weights == "linear":
        w = np.abs(np.subtract.outer(np.arange(k), np.arange(k))) / (k - 1)
    else:  # unweighted: disagreement weight 1, agreement 0
        w = 1 - np.eye(k)
    obs = (w * cm).sum()
    exp = (w * expected).sum()
    return 1 - obs / exp if exp > 0 else float("nan")


def pabak(true_labels, pred_labels, labels=VERDICTS) -> float:
    """Prevalence- and bias-adjusted kappa (Byrt, Bishop & Carlin 1993).

    ``(k·p_o − 1) / (k − 1)`` — kappa under uniform marginals, i.e. what κ
    would be without the prevalence problem. Reported alongside κ because a
    dominant verdict class (here: "mittel") inflates chance agreement and
    structurally caps κ regardless of model quality.
    """
    cm = confusion_matrix(true_labels, pred_labels, labels).to_numpy(float)
    n = cm.sum()
    if n == 0:
        return float("nan")
    k = len(labels)
    p_o = np.trace(cm) / n
    return float((k * p_o - 1) / (k - 1))


def kappa_bootstrap_ci(
    true_labels,
    pred_labels,
    labels=VERDICTS,
    weights: Optional[str] = "linear",
    n_boot: int = 4000,
    ci: float = 0.95,
    seed: int = 67,
) -> tuple[float, float]:
    """Percentile bootstrap CI for (weighted) Cohen's κ, resampling rated pairs.

    With few cases outside the dominant class the κ point estimate is highly
    unstable — the CI width makes that visible (rationale for demoting κ to a
    secondary metric on homogeneous samples).
    """
    t = pd.Series(list(true_labels)).reset_index(drop=True)
    p = pd.Series(list(pred_labels)).reset_index(drop=True)
    mask = t.notna() & p.notna()
    t, p = t[mask].to_numpy(), p[mask].to_numpy()
    if len(t) < 2:
        return (float("nan"), float("nan"))
    rng = np.random.default_rng(seed)
    stats = []
    for _ in range(n_boot):
        idx = rng.integers(0, len(t), len(t))
        k = cohen_kappa(t[idx], p[idx], labels=labels, weights=weights)
        if not math.isnan(k):
            stats.append(k)
    if not stats:
        return (float("nan"), float("nan"))
    lo, hi = (1 - ci) / 2 * 100, (1 + ci) / 2 * 100
    return (float(np.percentile(stats, lo)), float(np.percentile(stats, hi)))


# ----------------------------------------------------------------------------
# Model scoring
# ----------------------------------------------------------------------------


def make_llm():
    """OpenRouter LLM (like ``main.py``); ``None`` if no key — expressiveness
    then reports NOT_APPLICABLE and is excluded from the comparison."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        return None
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model="anthropic/claude-sonnet-4.5",
        temperature=0.0,
        max_tokens=10000,
        base_url="https://openrouter.ai/api/v1",
        api_key=key,
    )


def _dimension_row(filename: str, result: dict) -> dict:
    """Extract ``model_<dimension>`` values (0-1) from one validation result.

    Shared by live scoring (:func:`run_model_scores`) and run-file loading
    (:func:`load_model_scores`) so both paths apply identical semantics: a
    dimension whose indicators are all NOT_APPLICABLE (e.g. expressiveness
    without an LLM) is NaN — not measured — rather than a genuine low score.
    """
    by_dim = result.get("by_dimension", {}) or {}
    row = {"file": filename}
    for dim in MODEL_DIMS:
        d = by_dim.get(dim)
        if not d:
            row[f"model_{dim}"] = np.nan
            continue
        inds = d.get("indicators", [])
        statuses = [i.get("status") for i in inds]
        if inds and all(s == "not_applicable" for s in statuses):
            row[f"model_{dim}"] = np.nan  # dimension not measured (no LLM)
        else:
            row[f"model_{dim}"] = d.get("score")
    return row


def _finalise_model_df(rows: list[dict]) -> pd.DataFrame:
    df = pd.DataFrame(rows)
    df["model_overall"] = df[[f"model_{d}" for d in MODEL_DIMS]].mean(
        axis=1, skipna=True
    )
    return df


def run_model_scores(sample_dir, llm=None, **service_kwargs) -> pd.DataFrame:
    """Score every ``*.rdf`` in ``sample_dir`` with the prototype.

    Returns one row per file with ``model_<dimension>`` in 0-1 (NaN when a
    dimension's indicators are all NOT_APPLICABLE, e.g. expressiveness without an
    LLM) plus ``model_overall`` = mean of the available dimension scores.
    """
    from scoring.service import QualityMetricsService

    service = QualityMetricsService(llm=llm, **service_kwargs)
    rows = []
    files = sorted(Path(sample_dir).glob("*.rdf"))
    for i, path in enumerate(files, 1):
        result = service.validate_metadata(str(path))
        rows.append(_dimension_row(path.name, result))
        print(f"[{i:2d}/{len(files)}] scored {path.name}")
    return _finalise_model_df(rows)


def load_model_scores(run_path) -> pd.DataFrame:
    """Reuse an already-completed run's output instead of re-scoring.

    ``run_path`` is either a run directory (``run_<timestamp>_.../``) or a
    direct path to its ``run_aggregate.json``. Per-file ``result.json`` files
    are preferred because they carry indicator statuses, so the
    NOT_APPLICABLE→NaN semantics match :func:`run_model_scores` exactly; files
    without one fall back to the aggregate's ``dimension_scores`` (which can't
    distinguish "not measured" from a genuine score).

    Returns the same frame shape as :func:`run_model_scores` (``file`` +
    ``model_<dimension>`` in 0-1 + ``model_overall``), so it drops straight
    into :func:`merge_scores`.
    """
    import json

    run_path = Path(run_path)
    if run_path.is_file():
        aggregate_path, run_dir = run_path, run_path.parent
    else:
        aggregate_path, run_dir = run_path / "run_aggregate.json", run_path

    # Canonical filenames (incl. ".rdf") come from the aggregate; per-file
    # subdirectories are named by stem only.
    aggregate_files: dict = {}
    if aggregate_path.is_file():
        with open(aggregate_path, encoding="utf-8") as f:
            aggregate_files = json.load(f).get("files", {}) or {}

    if aggregate_files:
        names = list(aggregate_files)
    else:  # no aggregate — discover per-file result.json subdirs instead
        names = sorted(
            f"{p.parent.name}.rdf" for p in run_dir.glob("*/result.json")
        )
    if not names:
        raise FileNotFoundError(
            f"No run_aggregate.json or */result.json found under {run_dir}"
        )

    rows = []
    for name in names:
        result_path = run_dir / Path(name).stem / "result.json"
        if result_path.is_file():
            with open(result_path, encoding="utf-8") as f:
                rows.append(_dimension_row(name, json.load(f)))
            continue
        # Fallback: aggregate summary only (no indicator statuses available).
        dim_scores = (aggregate_files.get(name) or {}).get(
            "dimension_scores", {}
        ) or {}
        row = {"file": name}
        for dim in MODEL_DIMS:
            row[f"model_{dim}"] = (
                dim_scores[dim] if dim_scores.get(dim) is not None else np.nan
            )
        rows.append(row)
    print(f"loaded {len(rows)} scored files from {run_dir}")
    return _finalise_model_df(rows)


# ----------------------------------------------------------------------------
# Load ground truth & merge
# ----------------------------------------------------------------------------


def load_ground_truth(csv_path) -> pd.DataFrame:
    """Read the filled rating template; derive ``gt_overall`` (0-5 mean) and
    ``gt_verdict``. Rows with incomplete ratings get ``gt_verdict = None``.
    Validates that all GT values are in [0, 5]; warns on out-of-range entries.
    """
    df = pd.read_csv(csv_path)
    for col in GT_COLS:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
        out_of_range = df[col].dropna().between(0, 5, inclusive="both") == False  # noqa: E712
        if out_of_range.any():
            print(f"WARNING: {col} has {out_of_range.sum()} values outside [0, 5]")
    df["gt_overall"] = df[GT_COLS].mean(axis=1, skipna=False)
    df["gt_verdict"] = df[GT_COLS].apply(
        lambda r: derive_verdict(list(r.values)), axis=1
    )
    df["gt_rated"] = df[GT_COLS].notna().all(axis=1)
    return df


def merge_scores(gt_df: pd.DataFrame, model_df: pd.DataFrame) -> pd.DataFrame:
    """Join GT and model by ``file``; rescale model dims to 0-5 and derive the
    model verdict with the same rule as the manual GT (principled mapping).

    For the verdict the model dimensions are first rounded to the integer GT
    scale: the rule's thresholds are calibrated on integer ratings, and a
    continuous 2.86 expresses the same judgement as a manual 3 — applying the
    conjunctive "no dimension below 3" clause to unrounded values would be
    systematically harsher on the model (discretisation asymmetry). The
    continuous 0-5 columns stay unrounded for the correlation/error metrics.
    """
    merged = gt_df.merge(model_df, on="file", how="inner")
    for dim in MODEL_DIMS:
        merged[f"model_{dim}_0_5"] = merged[f"model_{dim}"] * 5
    merged["model_overall_0_5"] = merged[[f"model_{d}_0_5" for d in MODEL_DIMS]].mean(
        axis=1, skipna=True
    )
    merged["model_verdict"] = merged[[f"model_{d}_0_5" for d in MODEL_DIMS]].apply(
        lambda r: derive_verdict(list(np.round(r.values))), axis=1
    )
    return merged


# ----------------------------------------------------------------------------
# Comparison metrics
# ----------------------------------------------------------------------------


def auc_binary(scores, labels, pos_label: str) -> float:
    """AUC (Wilcoxon-Mann-Whitney) for a binary split of a 3-class verdict.

    Works without scipy: counts concordant pairs between the positive class
    and all other cases, with ties counted as 0.5.
    """
    s = pd.to_numeric(pd.Series(scores).reset_index(drop=True), errors="coerce")
    l = pd.Series(labels).reset_index(drop=True)
    mask = s.notna() & l.notna()
    s, l = s[mask].to_numpy(float), l[mask].to_numpy()
    pos = s[l == pos_label]
    neg = s[l != pos_label]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    u = sum(
        float(p > n) + 0.5 * float(p == n)
        for p in pos
        for n in neg
    )
    return float(u / (len(pos) * len(neg)))


def compare(merged: pd.DataFrame) -> dict:
    """Per-dimension rank correlations + overall-grade agreement.

    Primary metric: Spearman ρ (overall + per dimension; 0-1 model vs 0-5 GT).
    Secondary: verdict agreement (gut/mittel/schlecht) — accuracy, weighted κ
    with bootstrap CI, PABAK, AUC gut-vs-rest. κ is structurally capped on
    homogeneous samples (kappa paradox), hence CI + PABAK alongside.
    Additional: MAE, RMSE, Bias (0-5 scale), mean Spearman.
    See docs/methodik_evaluation_ground_truth_v3.md §5 for rationale.
    """
    per_dim = {}
    for gt_col, dim in DIM_MAP.items():
        x, y = merged[f"model_{dim}"], merged[gt_col]
        n = int(
            (
                pd.to_numeric(x, errors="coerce").notna()
                & pd.to_numeric(y, errors="coerce").notna()
            ).sum()
        )
        per_dim[dim] = {
            "spearman": spearman(x, y),
            "kendall_tau": kendall_tau(x, y),
            "n": n,
        }

    graded = merged[merged["gt_verdict"].notna() & merged["model_verdict"].notna()]

    # ── Continuous agreement on 0-5 scale ───────────────────────────────────
    cont = merged[
        merged["model_overall_0_5"].notna() & merged["gt_overall"].notna()
    ]
    diffs = cont["model_overall_0_5"].to_numpy(float) - cont["gt_overall"].to_numpy(float)
    mae  = float(np.abs(diffs).mean())  if len(diffs) else float("nan")
    rmse = float(np.sqrt((diffs ** 2).mean())) if len(diffs) else float("nan")
    bias = float(diffs.mean())          if len(diffs) else float("nan")

    # ── Summary across dimensions ────────────────────────────────────────────
    dim_spearmans = [
        v["spearman"] for v in per_dim.values()
        if not math.isnan(v["spearman"])
    ]
    mean_spearman_dims = float(np.mean(dim_spearmans)) if dim_spearmans else float("nan")

    overall = {
        "n_total": int(len(merged)),
        "n_graded": int(len(graded)),
        # ── Verdict-level (classification) ───────────────────────────────────
        "accuracy": (
            float((graded["gt_verdict"] == graded["model_verdict"]).mean())
            if len(graded) else float("nan")
        ),
        "weighted_kappa": cohen_kappa(
            graded["gt_verdict"], graded["model_verdict"], weights="linear"
        ),
        "weighted_kappa_ci": kappa_bootstrap_ci(
            graded["gt_verdict"], graded["model_verdict"], weights="linear"
        ),
        "pabak": pabak(graded["gt_verdict"], graded["model_verdict"]),
        "cohen_kappa": cohen_kappa(             # unweighted for reference
            graded["gt_verdict"], graded["model_verdict"]
        ),
        "auc_gut_vs_rest": auc_binary(          # binary: gut vs. mittel+schlecht
            graded["model_overall_0_5"], graded["gt_verdict"], pos_label="gut"
        ),
        # ── Rank correlation on continuous overall score ──────────────────────
        "spearman_overall": spearman(
            merged["model_overall_0_5"], merged["gt_overall"]
        ),
        "kendall_overall": kendall_tau(
            merged["model_overall_0_5"], merged["gt_overall"]
        ),
        "mean_spearman_dims": mean_spearman_dims,
        # ── Continuous error on 0-5 scale ────────────────────────────────────
        "mae":  mae,   # Ø Abweichung in Skalenpunkten
        "rmse": rmse,
        "bias": bias,  # positiv = Modell überschätzt systematisch
    }
    return {
        "per_dimension": pd.DataFrame(per_dim).T,
        "overall": overall,
        "confusion": confusion_matrix(graded["gt_verdict"], graded["model_verdict"]),
    }


def summary_table(result: dict) -> pd.DataFrame:
    """One compact per-dimension table (Spearman, Kendall, n) for the thesis."""
    return result["per_dimension"].round(3)


# ----------------------------------------------------------------------------
# Figures (matplotlib only)
# ----------------------------------------------------------------------------

_VERDICT_COLOR = {
    "gut": "#2ca02c",
    "mittel": "#ff7f0e",
    "schlecht": "#d62728",
    None: "#999999",
}


def make_figures(
    merged: pd.DataFrame, result: dict, outdir, stratum: str = ""
) -> list[Path]:
    """Write thesis-ready PNGs to ``outdir``; returns the saved paths."""
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    outdir = Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    suffix = f"_{stratum}" if stratum else ""
    paths: list[Path] = []

    def save(fig, name):
        p = outdir / f"{name}{suffix}.png"
        fig.savefig(p, dpi=150, bbox_inches="tight")
        plt.close(fig)
        paths.append(p)

    # 1. Overall scatter (both on 0-5), coloured by GT verdict.
    fig, ax = plt.subplots(figsize=(6, 6))
    for v in VERDICTS:
        sub = merged[merged["gt_verdict"] == v]
        ax.scatter(
            sub["model_overall_0_5"],
            sub["gt_overall"],
            label=v,
            color=_VERDICT_COLOR[v],
            s=45,
            alpha=0.8,
        )
    ax.plot([0, 5], [0, 5], "k--", lw=1, alpha=0.5)
    ax.set_xlabel("Modell-Gesamtscore (0–5, reskaliert)")
    ax.set_ylabel("Ground-Truth Gesamt (0–5)")
    ax.set_xlim(-0.1, 5.1)
    ax.set_ylim(-0.1, 5.1)
    ax.set_title("Modell vs. Ground Truth (gesamt)")
    ax.legend(title="GT-Urteil")
    save(fig, "overall_scatter")

    # 2. Per-dimension scatter (model 0-1 vs GT 0-5).
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    for ax, (gt_col, dim) in zip(axes.flat, DIM_MAP.items()):
        ax.scatter(
            merged[f"model_{dim}"], merged[gt_col], s=35, alpha=0.7, color="#1f77b4"
        )
        rho = result["per_dimension"].loc[dim, "spearman"]
        ax.set_title(f"{dim}  (Spearman ρ = {rho:.2f})")
        ax.set_xlabel("Modell-Score (0–1)")
        ax.set_ylabel("GT-Bewertung (0–5)")
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.2, 5.2)
    fig.suptitle("Pro Dimension: Modell-Score vs. manuelle Bewertung")
    fig.tight_layout()
    save(fig, "per_dimension_scatter")

    # 3. Boxplots of model overall score grouped by GT verdict (separation).
    fig, ax = plt.subplots(figsize=(7, 5))
    groups = [
        merged.loc[merged["gt_verdict"] == v, "model_overall"].dropna().to_numpy()
        for v in VERDICTS
    ]
    if any(len(g) for g in groups):
        bp = ax.boxplot(groups, labels=VERDICTS, patch_artist=True)
        for patch, v in zip(bp["boxes"], VERDICTS):
            patch.set_facecolor(_VERDICT_COLOR[v])
            patch.set_alpha(0.6)
    ax.set_xlabel("Ground-Truth Urteil")
    ax.set_ylabel("Modell-Gesamtscore (0-1)")
    ax.set_title("Trennschärfe: Modell-Score je GT-Urteil")
    save(fig, "separation_boxplot")

    # 4. Confusion matrix heatmap.
    cm = result["confusion"]
    fig, ax = plt.subplots(figsize=(5.5, 5))
    im = ax.imshow(cm.to_numpy(), cmap="Blues")
    ax.set_xticks(range(len(cm.columns)), cm.columns, rotation=20)
    ax.set_yticks(range(len(cm.index)), cm.index)
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(
                j,
                i,
                int(cm.iloc[i, j]),
                ha="center",
                va="center",
                color="white" if cm.iloc[i, j] > cm.to_numpy().max() / 2 else "black",
            )
    ax.set_title("Konfusionsmatrix (Urteil)")
    fig.colorbar(im, fraction=0.046, pad=0.04)
    save(fig, "confusion_matrix")

    # 5. Spearman per dimension (bar).
    fig, ax = plt.subplots(figsize=(7, 4.5))
    pdf = result["per_dimension"]
    ax.bar(pdf.index, pdf["spearman"].to_numpy(float), color="#1f77b4", alpha=0.85)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylim(-1, 1)
    ax.set_ylabel("Spearman ρ")
    ax.set_title("Rangkorrelation Modell ↔ Ground Truth je Dimension")
    save(fig, "spearman_per_dimension")

    return paths
