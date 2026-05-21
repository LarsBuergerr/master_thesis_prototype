import os
import logging
import json
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import hydra
from omegaconf import DictConfig, OmegaConf

from langchain_openai import ChatOpenAI

# Import logger after logging is configured
from utils.logger import get_logger
from quality_indicators.service import QualityMetricsService
from pipeline.output_manager import OutputManager

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


def resolve_files_to_process(cfg: DictConfig) -> List[Path]:
    """Resolve which files to process based on config.

    If files list is provided, use those specific files.
    Otherwise, find all files in directory_path matching patterns.
    """
    files_list = cfg.state.get("files", [])
    directory_path = Path(cfg.state.get("directory_path", ""))

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory does not exist: {directory_path}")

    # Specific files provided
    if files_list:
        files = []
        for filename in files_list:
            file_path = directory_path / filename
            if file_path.exists():
                files.append(file_path)
            else:
                logger.warning(f"File not found, skipping: {file_path}")
        return sorted(files)

    # No files specified - scan directory with patterns
    file_filter = cfg.state.get("file_filter", {})
    extensions = file_filter.get("extensions", [".rdf"])
    include_patterns = file_filter.get("include_patterns", [])
    exclude_patterns = file_filter.get("exclude_patterns", [])

    # Find all matching files
    all_files = []
    for ext in extensions:
        all_files.extend(directory_path.glob(f"*{ext}"))

    # Apply include patterns
    if include_patterns:
        all_files = [
            f for f in all_files if any(f.name.startswith(p) for p in include_patterns)
        ]

    # Apply exclude patterns
    if exclude_patterns:
        all_files = [
            f
            for f in all_files
            if not any(f.name.startswith(p) for p in exclude_patterns)
        ]

    return sorted(all_files)


@hydra.main(version_base=None, config_path="../conf", config_name="state/state_1")
def main(cfg: DictConfig) -> None:
    """Main entry point for quality validation.

    Uses all configurable parameters from the Hydra config file.
    Processes either specific files or all files in directory with filtering.
    """
    # Set log level from config
    log_level_str = (
        cfg.state.logging.get("level", "INFO") if cfg.state.logging else "INFO"
    )
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    logging.getLogger().setLevel(log_level)

    logger.info("Starting quality validation run...")
    logger.info(OmegaConf.to_yaml(cfg))

    # Resolve files to process
    try:
        files_to_process = resolve_files_to_process(cfg)
    except FileNotFoundError as e:
        logger.error(str(e))
        return

    if not files_to_process:
        logger.error("No files to process")
        return

    logger.info(f"Found {len(files_to_process)} file(s) to process")

    # Initialize output manager
    output_mgr = OutputManager(cfg=cfg)

    # Create quality service
    quality_cfg = cfg.state.get("quality", {})
    service = QualityMetricsService(
        max_workers=quality_cfg.get("max_workers", 4),
        dimension_weights=quality_cfg.get("dimension_weights", {}),
        indicator_weights=quality_cfg.get("indicator_weights", {}),
    )

    # Process each file
    processed_count = 0
    failed_count = 0
    failed_files = []

    for file_idx, file_path in enumerate(files_to_process, 1):
        logger.info(
            f"[{file_idx}/{len(files_to_process)}] Processing: {file_path.name}"
        )

        # Set up dedicated log file for this file
        output_mgr.setup_file_logger(file_path.name)

        try:
            logger.info(f"Started processing: {file_path.name}")
            result = service.validate_metadata(str(file_path))

            # Save results
            output_mgr.save_file_result(
                filename=file_path.name,
                result=result,
                save_intermediate=True,
            )

            summary = result.get("summary", {})
            logger.info(
                "  ✓ Completed | score=%.2f grade=%s",
                summary.get("overall_score", 0.0),
                summary.get("quality_grade", "N/A"),
            )

            processed_count += 1

        except Exception as e:
            logger.error(f"  ✗ Error processing {file_path.name}: {e}", exc_info=True)
            failed_files.append(file_path.name)
            failed_count += 1

        finally:
            output_mgr.close_file_logger(file_path.name)

    # Save run summary
    input_info = {
        "directory": str(cfg.state.get("directory_path", "")),
        "files_specified": len(cfg.state.get("files", [])),
        "files_found": len(files_to_process),
        "files_processed": processed_count,
        "files_failed": failed_count,
        "failed_files": failed_files,
    }

    output_mgr.save_run_summary(
        config=OmegaConf.to_container(cfg.state),
        input_info=input_info,
    )

    logger.info(
        f"Processed {processed_count}/{len(files_to_process)} files successfully"
    )
    logger.info(f"Output: {output_mgr.get_output_path()}")


if __name__ == "__main__":
    main()
