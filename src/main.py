import os
import logging
import json
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import hydra
from omegaconf import DictConfig, OmegaConf

from langchain_openai import ChatOpenAI

# Import logger after logging is configured
from utils.logger import get_logger
from quality_indicators.service import QualityMetricsService

# Set up logging early - this will be read from config in main()
# Default to INFO, will be overridden in main()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = get_logger(__name__)


def create_llm(cfg: DictConfig) -> ChatOpenAI:
    """Create an LLM client from the config.

    Args:
        cfg: Hydra configuration

    Returns:
        Configured ChatOpenAI instance for OpenRouter
    """
    model = cfg.state.llm.model
    temperature = cfg.state.llm.get("temperature", 0.0) if cfg.state.llm else 0.0
    max_tokens = cfg.state.llm.get("max_tokens", 4096) if cfg.state.llm else 4096
    base_url = "https://openrouter.ai/api/v1"

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable must be set. "
            "Create a .env file in the project root with: "
            "OPENROUTER_API_KEY=your-key"
        )

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        base_url=base_url,
        default_headers={
            "HTTP-Referer": "https://github.com/lbuerger/master_thesis_prototype",
            "X-Title": "Master Thesis Prototype",
        },
    )


@hydra.main(version_base=None, config_path="../conf", config_name="state/state_1")
def main(cfg: DictConfig) -> None:
    """Main entry point for quality validation.

    Uses all configurable parameters from the Hydra config file.
    The config file (state_1.yaml) contains directory and validation configuration.
    """
    # Set log level from config
    log_level_str = (
        cfg.state.logging.get("level", "INFO") if cfg.state.logging else "INFO"
    )
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logging.getLogger().setLevel(log_level)

    # Also update all existing loggers
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    logger.info("Starting quality validation run...")
    logger.info(OmegaConf.to_yaml(cfg))

    data_dir = Path(cfg.state.get("directory_path", ""))
    if not data_dir.exists():
        logger.error(f"Data directory does not exist: {data_dir}")
        return

    quality_cfg = cfg.state.get("quality", {})
    service = QualityMetricsService(
        max_workers=quality_cfg.get("max_workers", 4),
        dimension_weights=quality_cfg.get("dimension_weights", {}),
        indicator_weights=quality_cfg.get("indicator_weights", {}),
    )

    has_subdirs = any(d.is_dir() for d in data_dir.iterdir())

    results = []

    if has_subdirs:
        directories = sorted(data_dir.iterdir())
    else:
        directories = [data_dir]

    metadata_relative_path = cfg.state.get("metadata_path", "")

    print(metadata_relative_path)

    for directory in directories:
        if not directory.is_dir():
            continue

        has_metadata = (
            bool(metadata_relative_path)
            and (directory / metadata_relative_path).exists()
        )

        if not has_metadata:
            logger.debug(f"Skipping invalid directory: {directory}")
            continue

        logger.info(f"Processing directory: {directory}")

        try:
            metadata_path = directory / metadata_relative_path
            result = service.validate_metadata(str(metadata_path))

            results.append(
                {
                    "directory": str(directory),
                    "result": result,
                }
            )

            summary = result.get("summary", {})
            logger.info(
                "Completed %s | score=%.2f grade=%s",
                directory.name,
                summary.get("overall_score", 0.0),
                summary.get("quality_grade", "N/A"),
            )

            logger.info(f"Completed: {directory}")

        except Exception as e:
            logger.error(f"Error processing {directory}: {e}")

    logger.info(f"Processed {len(results)} directories successfully")

    # Summary of results
    for r in results:
        dir_path = r["directory"]
        state = r["result"]
        errors = state.get("errors", [])
        logger.info(
            f"  {Path(dir_path).name}: {'OK' if not errors else f'Errors: {errors}'}"
        )

    output_path = Path("quality_validation_results.json")
    serializable_results = []
    for item in results:
        serializable_results.append(
            {
                "directory": item["directory"],
                "summary": item["result"].get("summary", {}),
                "errors": item["result"].get("errors", []),
                "by_dimension": item["result"].get("by_dimension", {}),
            }
        )

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serializable_results, f, indent=2, ensure_ascii=False)

    logger.info(f"Wrote validation results to {output_path}")


if __name__ == "__main__":
    main()
