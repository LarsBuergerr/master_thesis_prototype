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

# Logger names whose records (request/response bodies, token usage) are
# mirrored into each file's dedicated ``openai.log``. The OpenAI SDK logs the
# full request options and raw response under the ``openai`` logger at DEBUG.
OPENAI_LOG_SOURCES = ("openai", "httpx", "httpcore")


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

        suffix = ""

        if cfg.state.get("run_output_dir_suffix"):
            suffix = cfg.state.get("run_output_dir_suffix")
        elif cfg.state.get("files") and len(list(cfg.state.get("files"))) == 1:
            suffix = list(cfg.state.get("files"))[0].split(".")[0]
        else:
            suffix = cfg.state.get("directory_path").split("/")[-1]

        self.run_dir = self.root_dir / f"run_{timestamp}_{config_name}_{suffix}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.timestamp = timestamp
        self.file_results: Dict[str, Dict[str, Any]] = {}
        self.file_loggers: Dict[str, logging.Logger] = {}
        self.openai_loggers: Dict[str, logging.Handler] = {}

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

        # Dedicated openai.log: full LLM request/response bodies + HTTP traffic
        # for this file. We temporarily route the OpenAI/HTTP loggers here only
        # (level=DEBUG, propagate=False) so their verbose output lands in this
        # focused file instead of flooding logs.log / session.log, then restore
        # their prior state in close_file_logger(). Files loop sequentially, so
        # this never mixes calls between files.
        openai_handler = logging.FileHandler(
            file_dir / "openai.log", encoding="utf-8", mode="w"
        )
        openai_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        openai_handler.setLevel(logging.DEBUG)
        saved_state = {}
        for source in OPENAI_LOG_SOURCES:
            src_logger = logging.getLogger(source)
            saved_state[source] = (src_logger.level, src_logger.propagate)
            src_logger.setLevel(logging.DEBUG)
            src_logger.propagate = False
            src_logger.addHandler(openai_handler)
        self.openai_loggers[filename] = (openai_handler, saved_state)

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

        if filename in self.openai_loggers:
            openai_handler, saved_state = self.openai_loggers[filename]
            for source in OPENAI_LOG_SOURCES:
                src_logger = logging.getLogger(source)
                src_logger.removeHandler(openai_handler)
                level, propagate = saved_state[source]
                src_logger.setLevel(level)
                src_logger.propagate = propagate
            openai_handler.close()
            del self.openai_loggers[filename]

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

    def save_run_cost_summary(self) -> Optional[Path]:
        """Write ``run_cost_summary.json`` at the run root.

        Aggregates the per-file ``llm_usage`` records (one per LLM call) into
        run-level token and cost totals plus a per-file breakdown. Always
        written when there are file results, even with zero LLM calls (an
        explicit "no LLM was used / cost 0" record is itself a useful fact).
        """
        if not self.file_results:
            return None

        per_file: Dict[str, Dict[str, Any]] = {}
        models: set = set()
        total_calls = 0
        sum_input = sum_output = sum_total = 0
        sum_cost = 0.0
        cost_complete = True  # any call missing cost → totals are a lower bound

        for filename, result in self.file_results.items():
            usages = result.get("llm_usage") or []
            f_in = sum(u.get("input_tokens") or 0 for u in usages)
            f_out = sum(u.get("output_tokens") or 0 for u in usages)
            f_total = sum(
                (u.get("total_tokens") or 0)
                or ((u.get("input_tokens") or 0) + (u.get("output_tokens") or 0))
                for u in usages
            )
            f_cost = 0.0
            f_cost_known = True
            for u in usages:
                models.add(u.get("model"))
                if u.get("cost_usd") is None:
                    f_cost_known = False
                else:
                    f_cost += float(u["cost_usd"])
            f_latency = round(sum(u.get("latency_seconds") or 0.0 for u in usages), 3)

            per_file[filename] = {
                "calls": len(usages),
                "input_tokens": f_in,
                "output_tokens": f_out,
                "total_tokens": f_total,
                "cost_usd": round(f_cost, 6) if f_cost_known else None,
                "latency_seconds": f_latency,
            }

            total_calls += len(usages)
            sum_input += f_in
            sum_output += f_out
            sum_total += f_total
            sum_cost += f_cost
            if usages and not f_cost_known:
                cost_complete = False

        files_with_llm = sum(1 for v in per_file.values() if v["calls"] > 0)
        summary = {
            "timestamp": self.timestamp,
            "run_directory": str(self.run_dir),
            "models": sorted(m for m in models if m),
            "files_processed": len(per_file),
            "files_with_llm_call": files_with_llm,
            "total_llm_calls": total_calls,
            "total_input_tokens": sum_input,
            "total_output_tokens": sum_output,
            "total_tokens": sum_total,
            "total_cost_usd": round(sum_cost, 6),
            "cost_is_complete": cost_complete,
            "avg_cost_per_file_usd": (
                round(sum_cost / files_with_llm, 6) if files_with_llm else 0.0
            ),
            "avg_tokens_per_call": (
                round(sum_total / total_calls, 1) if total_calls else 0
            ),
            "per_file": per_file,
        }
        if not cost_complete:
            summary["note"] = (
                "Some LLM calls reported no cost (OpenRouter usage accounting "
                "disabled or unavailable); total_cost_usd is a lower bound."
            )

        cost_path = self.run_dir / "run_cost_summary.json"
        self._save_json(cost_path, summary)
        return cost_path

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
