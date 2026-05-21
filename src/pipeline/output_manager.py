"""Output directory management for quality validation runs."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from omegaconf import DictConfig, OmegaConf

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
        suffix = (
            cfg.state.get("run_output_dir_suffix", "")
            if cfg.state.get("run_output_dir_suffix")
            else cfg.state.get("directory_path").split("/")[-1]
        )
        self.run_dir = self.root_dir / f"run_{timestamp}_{suffix}"
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

        metadata = {
            "timestamp": self.timestamp,
            "run_directory": str(self.run_dir),
            "config": config,
            "input": input_info,
        }

        metadata_path = self.run_dir / "metadata.json"
        self._save_json(metadata_path, metadata)

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
