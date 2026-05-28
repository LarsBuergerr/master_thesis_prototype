"""Output directory management for quality validation runs."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

import git
from omegaconf import DictConfig, OmegaConf
from hydra.core.hydra_config import HydraConfig

logger = logging.getLogger(__name__)


class OutputManager:
    """Manages structured output for quality validation runs."""

    def __init__(self, cfg: DictConfig):
        """Initialize output manager.

        Args:
            root_dir: Root directory for all output runs
        """
        self.cfg = cfg
        self.root_dir = Path(cfg.state.get("output_dir", "outputs/"))
        self.root_dir.mkdir(parents=True, exist_ok=True)

        # Create run directory with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        hydra_cfg = HydraConfig.get()
        config_name = (hydra_cfg.job.config_name).split("/")[-1].replace("_", "-")

        suffix = (
            cfg.state.get("run_output_dir_suffix", "")
            if cfg.state.get("run_output_dir_suffix")
            else cfg.state.get("directory_path").split("/")[-1]
        )
        self.run_dir = self.root_dir / f"run_{timestamp}_{config_name}_{suffix}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.timestamp = timestamp
        self.file_results: Dict[str, Dict[str, Any]] = {}
        self.file_loggers: Dict[str, logging.Logger] = {}

        logger.info(f"Created output directory: {self.run_dir}")

    def create_file_directory(self, filename: str) -> Path:
        """Create directory for a specific file's results."""
        # Sanitize filename for directory name
        safe_name = Path(filename).stem  # Remove extension
        file_dir = self.run_dir / safe_name
        file_dir.mkdir(parents=True, exist_ok=True)
        return file_dir

    def setup_file_logger(self, filename: str) -> logging.FileHandler:
        """Add a file handler to capture all logs for a specific file.

        Adds a handler to the root logger that writes only this file's logs to its log file.
        Returns the handler so it can be removed later with close_file_logger().
        """
        file_dir = self.create_file_directory(filename)

        # Create handler for this file's logs
        log_path = file_dir / "logs.log"
        handler = logging.FileHandler(log_path, encoding="utf-8", mode="w")
        handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        handler.setLevel(logging.DEBUG)

        # Add handler to root logger so it captures all logs
        root_logger = logging.getLogger()
        root_logger.addHandler(handler)

        # Store for later cleanup
        self.file_loggers[filename] = handler

        logger.info(f"Created file log handler for {filename} at {log_path}")
        return handler

    def close_file_logger(self, filename: str) -> None:
        """Remove and cleanup the file logger handler."""
        if filename in self.file_loggers:
            handler = self.file_loggers[filename]
            root_logger = logging.getLogger()
            root_logger.removeHandler(handler)
            handler.close()
            del self.file_loggers[filename]

    def save_file_result(
        self, filename: str, result: Dict[str, Any], save_intermediate: bool = True
    ) -> None:
        """Save validation result for a single file."""
        file_dir = self.create_file_directory(filename)

        # Convert DictConfig to regular dict for JSON serialization
        result = self._convert_to_serializable(result)

        # Store for later aggregation
        self.file_results[filename] = result

        # Save complete result
        result_path = file_dir / "result.json"
        self._save_json(result_path, result)

    def save_run_summary(
        self, config: Dict[str, Any], input_info: Dict[str, Any]
    ) -> None:
        """Save metadata and aggregated summary for entire run."""
        # Metadata about this run
        if isinstance(config, DictConfig):
            config = OmegaConf.to_container(config, resolve=True)

        repo = git.Repo(search_parent_directories=True)
        commit_hash = repo.head.commit.hexsha

        metadata = {
            "timestamp": self.timestamp,
            "run_directory": str(self.run_dir),
            "config_name": HydraConfig.get().job.config_name,
            "commit_hash": commit_hash,
            "config": config,
            "input": input_info,
        }

        metadata_path = self.run_dir / "metadata.json"
        self._save_json(metadata_path, metadata)

    def save_run_aggregate(self) -> Optional[Path]:
        """Save a compact per-file summary plus run-level aggregates.

        Writes ``run_aggregate.json`` at the run root with one entry per
        processed file plus aggregate statistics. Returns the path written,
        or ``None`` if there are no file results.
        """
        if not self.file_results:
            return None

        files_summary: Dict[str, Dict[str, Any]] = {}
        dim_score_buckets: Dict[str, list] = {}
        overall_scores: list = []
        indicator_counts: Dict[str, Dict[str, int]] = {}

        for filename, result in self.file_results.items():
            summary = result.get("summary", {}) or {}
            dim_scores = summary.get("dimension_scores", {}) or {}
            overall_score = summary.get("overall_score")

            files_summary[filename] = {
                "overall_score": overall_score,
                "overall_pass_rate": summary.get("overall_pass_rate"),
                "quality_grade": summary.get("quality_grade"),
                "dimension_scores": dim_scores,
                "total_indicators": summary.get("total_indicators"),
                "total_pass": summary.get("total_pass"),
                "total_fail": summary.get("total_fail"),
            }

            if isinstance(overall_score, (int, float)):
                overall_scores.append(float(overall_score))

            for dim, score in dim_scores.items():
                if isinstance(score, (int, float)):
                    dim_score_buckets.setdefault(dim, []).append(float(score))

            for dim_data in (result.get("by_dimension", {}) or {}).values():
                for ind in dim_data.get("indicators", []) or []:
                    ind_id = ind.get("indicator_id")
                    if not ind_id:
                        continue
                    status = (ind.get("status") or "unknown").lower()
                    bucket = indicator_counts.setdefault(
                        ind_id,
                        {
                            "dimension": ind.get("dimension"),
                            "pass": 0,
                            "partial": 0,
                            "fail": 0,
                            "error": 0,
                        },
                    )
                    bucket[status] = bucket.get(status, 0) + 1

        def _mean(xs: list) -> Optional[float]:
            return round(sum(xs) / len(xs), 4) if xs else None

        aggregate = {
            "file_count": len(files_summary),
            "overall_score_mean": _mean(overall_scores),
            "overall_score_min": min(overall_scores) if overall_scores else None,
            "overall_score_max": max(overall_scores) if overall_scores else None,
            "dimension_score_means": {
                dim: _mean(scores) for dim, scores in dim_score_buckets.items()
            },
            "indicator_status_counts": indicator_counts,
        }

        aggregate_payload = {
            "timestamp": self.timestamp,
            "run_directory": str(self.run_dir),
            "files": files_summary,
            "aggregate": aggregate,
        }

        aggregate_path = self.run_dir / "run_aggregate.json"
        self._save_json(aggregate_path, aggregate_payload)
        return aggregate_path

    @staticmethod
    def _convert_to_serializable(obj: Any) -> Any:
        """Recursively convert DictConfig objects to regular dicts."""
        if isinstance(obj, DictConfig):
            obj = OmegaConf.to_container(obj, resolve=True)

        if isinstance(obj, dict):
            return {
                k: OutputManager._convert_to_serializable(v) for k, v in obj.items()
            }
        elif isinstance(obj, (list, tuple)):
            return [OutputManager._convert_to_serializable(item) for item in obj]
        else:
            return obj

    @staticmethod
    def _save_json(path: Path, data: Any) -> None:
        """Save data as pretty-printed JSON."""
        try:
            # Recursively convert any DictConfig objects to regular dicts
            data = OutputManager._convert_to_serializable(data)

            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved JSON: {path}")
        except Exception as e:
            logger.error(f"Failed to save {path}: {e}")

    def get_output_path(self) -> Path:
        """Get the run output directory path."""
        return self.run_dir
