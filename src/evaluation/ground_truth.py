"""Compare a manual ground-truth rating against the prototype's scores.

Pipeline (used by ``playground/notebooks/10_ground_truth_evaluation.ipynb``):

1. ``run_model_scores(sample_dir, llm)`` — score every RDF with the prototype,
   returning the four dimension scores (0-1) per dataset.
2. ``load_ground_truth(csv)`` — read the filled rating template (0-3 per
   dimension), derive the overall verdict via :func:`derive_verdict`.
3. ``merge_scores(...)`` — join, rescale model scores to 0-3 and derive the
   model's verdict with the *same* rule (principled mapping).
4. ``compare(...)`` — per-dimension rank correlation (Spearman, Kendall τ-b) and
   overall-grade agreement (accuracy, Cohen's κ, weighted κ, confusion matrix).
5. ``make_figures(...)`` — thesis-ready PNGs.

Stats are implemented in pure numpy/pandas (no scipy/sklearn dependency).
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
    """Map four 0-3 dimension values to gut / mittel / schlecht.

    Rules (see docs/methodik_evaluation_ground_truth):
      * gut      = Durchschnitt >= 2.25 und keine Dimension unter 2
      * schlecht = Durchschnitt <= 1.25 oder mindestens zwei Dimensionen unter 1.5
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
    below_2 = sum(1 for d in vals if d < 2)
    below_15 = sum(1 for d in vals if d < 1.5)
    if avg >= 2.25 and below_2 == 0:
        return "gut"
    if avg <= 1.25 or below_15 >= 2:
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
        by_dim = result.get("by_dimension", {})
        row = {"file": path.name}
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
        rows.append(row)
        print(f"[{i:2d}/{len(files)}] scored {path.name}")
    df = pd.DataFrame(rows)
    df["model_overall"] = df[[f"model_{d}" for d in MODEL_DIMS]].mean(
        axis=1, skipna=True
    )
    return df


# ----------------------------------------------------------------------------
# Load ground truth & merge
# ----------------------------------------------------------------------------


def load_ground_truth(csv_path) -> pd.DataFrame:
    """Read the filled rating template; derive ``gt_overall`` (0-3 mean) and
    ``gt_verdict``. Rows with incomplete ratings get ``gt_verdict = None``."""
    df = pd.read_csv(csv_path)
    for col in GT_COLS:
        if col not in df.columns:
            df[col] = np.nan
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["gt_overall"] = df[GT_COLS].mean(axis=1, skipna=False)
    df["gt_verdict"] = df[GT_COLS].apply(
        lambda r: derive_verdict(list(r.values)), axis=1
    )
    df["gt_rated"] = df[GT_COLS].notna().all(axis=1)
    return df


def merge_scores(gt_df: pd.DataFrame, model_df: pd.DataFrame) -> pd.DataFrame:
    """Join GT and model by ``file``; rescale model dims to 0-3 and derive the
    model verdict with the same rule."""
    merged = gt_df.merge(model_df, on="file", how="inner")
    for dim in MODEL_DIMS:
        merged[f"model_{dim}_0_3"] = merged[f"model_{dim}"] * 3
    merged["model_overall_0_3"] = merged[[f"model_{d}_0_3" for d in MODEL_DIMS]].mean(
        axis=1, skipna=True
    )
    merged["model_verdict"] = merged[[f"model_{d}_0_3" for d in MODEL_DIMS]].apply(
        lambda r: derive_verdict(list(r.values)), axis=1
    )
    return merged


# ----------------------------------------------------------------------------
# Comparison metrics
# ----------------------------------------------------------------------------


def compare(merged: pd.DataFrame) -> dict:
    """Per-dimension rank correlations + overall-grade agreement."""
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
    overall = {
        "n_graded": int(len(graded)),
        "accuracy": (
            float((graded["gt_verdict"] == graded["model_verdict"]).mean())
            if len(graded)
            else float("nan")
        ),
        "cohen_kappa": cohen_kappa(graded["gt_verdict"], graded["model_verdict"]),
        "weighted_kappa": cohen_kappa(
            graded["gt_verdict"], graded["model_verdict"], weights="linear"
        ),
        "spearman_overall": spearman(merged["model_overall"], merged["gt_overall"]),
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

    # 1. Overall scatter (both on 0-3), coloured by GT verdict.
    fig, ax = plt.subplots(figsize=(6, 6))
    for v in VERDICTS:
        sub = merged[merged["gt_verdict"] == v]
        ax.scatter(
            sub["model_overall_0_3"],
            sub["gt_overall"],
            label=v,
            color=_VERDICT_COLOR[v],
            s=45,
            alpha=0.8,
        )
    ax.plot([0, 3], [0, 3], "k--", lw=1, alpha=0.5)
    ax.set_xlabel("Modell-Gesamtscore (0-3, reskaliert)")
    ax.set_ylabel("Ground-Truth Gesamt (0-3)")
    ax.set_title("Modell vs. Ground Truth (gesamt)")
    ax.legend(title="GT-Urteil")
    save(fig, "overall_scatter")

    # 2. Per-dimension scatter (model 0-1 vs GT 0-3).
    fig, axes = plt.subplots(2, 2, figsize=(11, 9))
    for ax, (gt_col, dim) in zip(axes.flat, DIM_MAP.items()):
        ax.scatter(
            merged[f"model_{dim}"], merged[gt_col], s=35, alpha=0.7, color="#1f77b4"
        )
        rho = result["per_dimension"].loc[dim, "spearman"]
        ax.set_title(f"{dim}  (Spearman ρ={rho:.2f})")
        ax.set_xlabel("Modell-Score (0-1)")
        ax.set_ylabel("GT-Bewertung (0-3)")
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.2, 3.2)
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
