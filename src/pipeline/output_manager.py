"""Output directory management for quality validation runs."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from omegaconf import DictConfig, OmegaConf

logger = logging.getLogger(__name__)


class OutputManager:
    """Manages structured output for quality validation runs."""

    def __init__(self, root_dir: str = "outputs/"):
        """Initialize output manager.

        Args:
            root_dir: Root directory for all output runs
        """
        self.root_dir = Path(root_dir)
        self.root_dir.mkdir(parents=True, exist_ok=True)

        # Create run directory with timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.run_dir = self.root_dir / f"run_{timestamp}"
        self.run_dir.mkdir(parents=True, exist_ok=True)

        self.timestamp = timestamp
        self.file_results: Dict[str, Dict[str, Any]] = {}

        logger.info(f"Created output directory: {self.run_dir}")

    def create_file_directory(self, filename: str) -> Path:
        """Create directory for a specific file's results."""
        # Sanitize filename for directory name
        safe_name = Path(filename).stem  # Remove extension
        file_dir = self.run_dir / safe_name
        file_dir.mkdir(parents=True, exist_ok=True)
        return file_dir

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

        logger.info(f"Saved results for {filename} to {file_dir}")

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

        logger.info(f"Saved run metadata to {self.run_dir}")

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
