"""Render PNG chart summaries from a run's aggregate JSON.

Produces four images at the run root:

- ``run_summary.png`` — overall-score histogram + average score per dimension.
- ``run_overall_by_file.png`` — overall score (Gesamtscore) per file, side by
  side in a single bar chart.
- ``run_scores_by_file.png`` — per-file scores, one subplot per active dimension.
- ``run_indicator_outcomes.png`` — stacked pass/partial/fail/error counts per
  indicator, one subplot per active dimension.

All layouts adapt to whichever dimensions / indicators are active.
"""

from __future__ import annotations

import json
import logging
import math
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)

_STATUS_ORDER = ["pass", "partial", "fail", "error"]
_STATUS_COLORS = {
    "pass": "#4c9f70",
    "partial": "#e2b13c",
    "fail": "#c0504d",
    "error": "#7f7f7f",
}


def generate_run_charts(
    aggregate: Dict[str, Any], output_dir: Path
) -> List[Path]:
    """Render all three PNGs for a run. Returns the list of files written."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    written: List[Path] = []
    files = aggregate.get("files") or {}
    if not files:
        logger.warning("No file results to plot; skipping chart generation")
        return written

    summary_path = output_dir / "run_summary.png"
    _render_overview(aggregate, summary_path)
    written.append(summary_path)

    overall_path = output_dir / "run_overall_by_file.png"
    if _render_overall_by_file(aggregate, overall_path):
        written.append(overall_path)

    scores_path = output_dir / "run_scores_by_file.png"
    if _render_scores_by_dimension(aggregate, scores_path):
        written.append(scores_path)

    indicators_path = output_dir / "run_indicator_outcomes.png"
    if _render_indicators_by_dimension(aggregate, indicators_path):
        written.append(indicators_path)

    return written


def generate_run_charts_from_file(
    aggregate_path: Path, output_dir: Optional[Path] = None
) -> List[Path]:
    """Load ``run_aggregate.json`` and render all charts to its directory."""
    aggregate_path = Path(aggregate_path)
    with aggregate_path.open("r", encoding="utf-8") as fh:
        aggregate = json.load(fh)
    return generate_run_charts(aggregate, output_dir or aggregate_path.parent)


def _render_overview(aggregate: Dict[str, Any], output_path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Run summary", fontsize=14, fontweight="bold")

    _plot_overall_distribution(axes[0], aggregate.get("files") or {})
    _plot_dimension_means(
        axes[1],
        (aggregate.get("aggregate") or {}).get("dimension_score_means") or {},
    )

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved overview chart to {output_path}")


def _render_overall_by_file(aggregate: Dict[str, Any], output_path: Path) -> bool:
    files = aggregate.get("files") or {}
    scored = {
        name: entry.get("overall_score")
        for name, entry in files.items()
        if isinstance(entry.get("overall_score"), (int, float))
    }
    if not scored:
        logger.warning("No overall scores present; skipping overall-by-file chart")
        return False

    file_names = sorted(scored.keys())
    scores = [float(scored[name]) for name in file_names]

    # Widen the figure with the file count so bars/labels stay legible.
    width = max(8.0, 0.6 * len(file_names) + 2.0)
    fig, ax = plt.subplots(figsize=(width, 5))
    fig.suptitle("Overall score per file", fontsize=14, fontweight="bold")

    x = np.arange(len(file_names))
    bars = ax.bar(x, scores, color="#4c72b0")
    for bar, value in zip(bars, scores):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.01,
            f"{value:.2f}",
            ha="center",
            va="bottom",
            fontsize=8,
        )

    mean = float(np.mean(scores))
    ax.axhline(
        mean,
        color="#c0504d",
        linestyle="--",
        linewidth=1.2,
        label=f"mean={mean:.2f}",
    )
    ax.set_ylabel("Overall score")
    ax.set_ylim(0, 1.05)
    ax.set_xticks(x)
    ax.set_xticklabels(
        [_shorten(name) for name in file_names], rotation=45, ha="right", fontsize=7
    )
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved overall-by-file chart to {output_path}")
    return True


def _render_scores_by_dimension(aggregate: Dict[str, Any], output_path: Path) -> bool:
    files = aggregate.get("files") or {}
    dimensions = sorted(_collect_dimensions(files.values()))
    if not dimensions:
        logger.warning("No dimensions present; skipping per-dimension score chart")
        return False

    file_names = sorted(files.keys())
    rows, cols = _grid_for(len(dimensions))
    fig, axes = plt.subplots(
        rows, cols, figsize=(7 * cols, 4 * rows), squeeze=False, sharey=True
    )
    fig.suptitle("Score per file by dimension", fontsize=14, fontweight="bold")

    for idx, dim in enumerate(dimensions):
        ax = axes[idx // cols][idx % cols]
        _plot_dimension_scores_for_files(ax, dim, file_names, files)

    for idx in range(len(dimensions), rows * cols):
        axes[idx // cols][idx % cols].set_axis_off()

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved per-dimension score chart to {output_path}")
    return True


def _render_indicators_by_dimension(
    aggregate: Dict[str, Any], output_path: Path
) -> bool:
    indicator_counts = (aggregate.get("aggregate") or {}).get(
        "indicator_status_counts"
    ) or {}
    if not indicator_counts:
        logger.warning("No indicator data; skipping per-dimension indicator chart")
        return False

    by_dim: Dict[str, Dict[str, Dict[str, int]]] = {}
    unknown_bucket: Dict[str, Dict[str, int]] = {}
    for iid, counts in indicator_counts.items():
        dim = counts.get("dimension") or "unknown"
        target = by_dim.setdefault(dim, {}) if dim != "unknown" else unknown_bucket
        target[iid] = counts
    if unknown_bucket:
        by_dim["unknown"] = unknown_bucket

    dimensions = sorted(by_dim.keys())
    rows, cols = _grid_for(len(dimensions))
    fig, axes = plt.subplots(
        rows, cols, figsize=(7 * cols, 4 * rows), squeeze=False
    )
    fig.suptitle(
        "Indicator outcomes across all files (by dimension)",
        fontsize=14,
        fontweight="bold",
    )

    for idx, dim in enumerate(dimensions):
        ax = axes[idx // cols][idx % cols]
        ax.set_title(dim)
        _plot_indicator_status_counts(ax, by_dim[dim])

    for idx in range(len(dimensions), rows * cols):
        axes[idx // cols][idx % cols].set_axis_off()

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    logger.info(f"Saved per-dimension indicator chart to {output_path}")
    return True


def _collect_dimensions(file_entries: Iterable[Dict[str, Any]]) -> Iterable[str]:
    seen: set = set()
    for entry in file_entries:
        for dim in (entry.get("dimension_scores") or {}).keys():
            seen.add(dim)
    return seen


def _grid_for(n: int) -> Tuple[int, int]:
    if n <= 1:
        return 1, 1
    if n == 2:
        return 1, 2
    if n <= 4:
        return 2, 2
    cols = 2
    return math.ceil(n / cols), cols


def _plot_dimension_scores_for_files(ax, dim, file_names, files) -> None:
    ax.set_title(dim)
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.05)

    scores = [
        files[name].get("dimension_scores", {}).get(dim) or 0.0 for name in file_names
    ]
    x = np.arange(len(file_names))
    ax.bar(x, scores, color="#4c72b0")
    ax.set_xticks(x)
    ax.set_xticklabels(
        [_shorten(name) for name in file_names], rotation=45, ha="right", fontsize=7
    )
    ax.grid(axis="y", linestyle="--", alpha=0.4)


def _plot_overall_distribution(ax, files) -> None:
    ax.set_title("Distribution of overall scores")
    ax.set_xlabel("Overall score")
    ax.set_ylabel("Files")

    scores = [
        f.get("overall_score")
        for f in files.values()
        if isinstance(f.get("overall_score"), (int, float))
    ]
    if not scores:
        ax.text(0.5, 0.5, "No overall scores", ha="center", va="center")
        ax.set_axis_off()
        return

    bins = np.linspace(0, 1, 11)
    ax.hist(scores, bins=bins, color="#4c72b0", edgecolor="white")
    ax.set_xlim(0, 1)
    ax.axvline(
        float(np.mean(scores)),
        color="#c0504d",
        linestyle="--",
        linewidth=1.2,
        label=f"mean={np.mean(scores):.2f}",
    )
    ax.legend(loc="upper left", fontsize=8)
    ax.grid(axis="y", linestyle="--", alpha=0.4)


def _plot_indicator_status_counts(ax, indicator_counts) -> None:
    ax.set_xlabel("Count")

    if not indicator_counts:
        ax.text(0.5, 0.5, "No indicator data", ha="center", va="center")
        ax.set_axis_off()
        return

    ind_ids = sorted(indicator_counts.keys())
    y = np.arange(len(ind_ids))
    left = np.zeros(len(ind_ids))

    for status in _STATUS_ORDER:
        counts = np.array(
            [indicator_counts[iid].get(status, 0) for iid in ind_ids], dtype=float
        )
        if counts.sum() == 0:
            continue
        ax.barh(
            y,
            counts,
            left=left,
            label=status,
            color=_STATUS_COLORS.get(status, "#888888"),
        )
        left += counts

    ax.set_yticks(y)
    ax.set_yticklabels(ind_ids, fontsize=8)
    ax.invert_yaxis()
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(axis="x", linestyle="--", alpha=0.4)


def _plot_dimension_means(ax, dim_means) -> None:
    ax.set_title("Average score per dimension")
    ax.set_ylabel("Mean score")
    ax.set_ylim(0, 1.05)

    if not dim_means:
        ax.text(0.5, 0.5, "No dimension data", ha="center", va="center")
        ax.set_axis_off()
        return

    dims = sorted(dim_means.keys())
    values = [dim_means.get(d) or 0.0 for d in dims]
    x = np.arange(len(dims))
    bars = ax.bar(x, values, color="#4c9f70")
    for bar, value in zip(bars, values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.02,
            f"{value:.2f}",
            ha="center",
            fontsize=9,
        )
    ax.set_xticks(x)
    ax.set_xticklabels(dims, rotation=20, ha="right")
    ax.grid(axis="y", linestyle="--", alpha=0.4)


def _shorten(name: str, limit: int = 28) -> str:
    if len(name) <= limit:
        return name
    return name[: limit - 1] + "…"
