import os
import logging
import json
import git
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
from utils.enums.language import Language
from scoring.service import QualityMetricsService
from scoring.score_policy import ScorePolicy
from reporting.output_manager import OutputManager
from reporting.run_visualizer import generate_run_charts_from_file

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
        # Ask OpenRouter to include real cost accounting in each response's
        # usage block so the run cost summary reports actual USD spend.
        extra_body={"usage": {"include": True}},
    )


def create_local_llm(cfg: DictConfig) -> ChatOpenAI:
    """Create an LLM client for a local llama.cpp server.

    llama.cpp's ``server`` exposes an OpenAI-compatible API (``/v1``), so the
    same ``ChatOpenAI`` client works — only the ``base_url`` changes and no real
    API key is needed (llama.cpp ignores it, but the client requires a
    non-empty string). The OpenRouter-specific headers and the ``usage`` cost
    accounting are dropped since they don't apply locally.

    Config keys (all optional, under ``llm``):
        base_url: server endpoint, default ``http://localhost:8080/v1``
        model:    model name to send; llama.cpp serves whatever is loaded, so
                  this is mostly a label, default ``"qwen3.5"``

    Args:
        cfg: Hydra configuration

    Returns:
        Configured ChatOpenAI instance pointed at the local server
    """
    model = cfg.state.llm.get("model", "qwen3.5") if cfg.state.llm else "qwen3.5"
    temperature = cfg.state.llm.get("temperature", 0.0) if cfg.state.llm else 0.0
    max_tokens = cfg.state.llm.get("max_tokens", 4096) if cfg.state.llm else 4096
    base_url = (
        cfg.state.llm.get("base_url", "http://localhost:8080/v1")
        if cfg.state.llm
        else "http://localhost:8080/v1"
    )

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        # llama.cpp doesn't validate the key, but the OpenAI client refuses an
        # empty one.
        api_key="sk-no-key-required",
        base_url=base_url,
    )


def build_llm(cfg: DictConfig) -> ChatOpenAI:
    """Build the LLM client selected by ``llm.provider``.

    ``provider: "local"`` → local llama.cpp server (:func:`create_local_llm`);
    anything else (default ``"openrouter"``) → OpenRouter (:func:`create_llm`).
    """
    provider = (
        cfg.state.llm.get("provider", "openrouter") if cfg.state.llm else "openrouter"
    )
    if str(provider).lower() == "local":
        return create_local_llm(cfg)
    return create_llm(cfg)


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


@hydra.main(version_base=None, config_path="../conf", config_name="state/state_default")
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

    # Even at root DEBUG, keep third-party libraries quiet. Without this
    # matplotlib's font_manager / PIL / urllib3 / rdflib dump thousands of
    # lines per run (font cache scans, PNG chunk decoding, RDF parsing).
    for noisy in (
        "matplotlib",
        "PIL",
        "urllib3",
        "requests",
        "rdflib",
        "httpx",
        "httpcore",
    ):
        logging.getLogger(noisy).setLevel(logging.WARNING)

    session_handler = None

    logger.info("Starting quality validation run...")
    logger.info(OmegaConf.to_yaml(cfg))

    run_output_enabled = cfg.state.get("run_output_enabled", False)

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

    output_mgr = None
    if run_output_enabled:
        # Initialize output manager only when run output is enabled.
        output_mgr = OutputManager(cfg=cfg)

        # Set up session-wide log file in run directory
        session_log_path = output_mgr.run_dir / "session.log"
        session_handler = logging.FileHandler(
            session_log_path, encoding="utf-8", mode="w"
        )
        session_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        session_handler.setLevel(logging.DEBUG)
        logging.getLogger().addHandler(session_handler)

    # Create quality service
    quality_cfg = cfg.state.get("quality", {})
    language = Language(cfg.state.get("language", "de"))

    # The expressiveness dimension is scored by a single LLM call per dataset.
    # Build the LLM only when (a) the operator explicitly opted in via
    # ``llm.enabled`` and (b) that dimension will actually run — otherwise we
    # never spend tokens. If the key is missing we degrade gracefully:
    # expressiveness indicators then report NOT_APPLICABLE instead of aborting.
    dimension_whitelist = quality_cfg.get("dimension_whitelist")
    expressiveness_active = (
        not dimension_whitelist or "expressiveness" in dimension_whitelist
    )
    llm_enabled = bool(cfg.state.llm.get("enabled", False)) if cfg.state.llm else False
    llm = None
    if llm_enabled and expressiveness_active:
        try:
            llm = build_llm(cfg)
        except ValueError as e:
            logger.warning(
                f"Expressiveness enabled but LLM unavailable ({e}); "
                "expressiveness indicators will report NOT_APPLICABLE"
            )
    elif expressiveness_active and not llm_enabled:
        logger.info(
            "Expressiveness dimension active but llm.enabled=false; "
            "skipping the LLM call (indicators report NOT_APPLICABLE)"
        )

    # Optional configurable status→score mapping (tunable PASS/PARTIAL/FAIL
    # points, optional negative fails). Absent ``quality.scoring`` block →
    # None → indicators' raw scores are used unchanged.
    scoring_cfg = quality_cfg.get("scoring")
    if scoring_cfg is not None:
        scoring_cfg = OmegaConf.to_container(scoring_cfg, resolve=True)
    score_policy = ScorePolicy.from_config(scoring_cfg)
    if score_policy is not None:
        logger.info(
            "Score policy active: pass=%.2f partial=%.2f fail=%.2f "
            "allow_partial=%s overrides=%d",
            score_policy.pass_score,
            score_policy.partial_score,
            score_policy.fail_score,
            score_policy.allow_partial,
            len(score_policy.overrides),
        )

    service = QualityMetricsService(
        max_workers=quality_cfg.get("max_workers", 4),
        dimension_weights=quality_cfg.get("dimension_weights", {}),
        indicator_weights=quality_cfg.get("indicator_weights", {}),
        dimension_whitelist=dimension_whitelist,
        indicator_blacklist=quality_cfg.get("indicator_blacklist"),
        indicator_whitelist=quality_cfg.get("indicator_whitelist"),
        llm=llm,
        language=language,
        score_policy=score_policy,
    )

    # Process each file
    processed_count = 0
    failed_count = 0
    failed_files = []

    for file_idx, file_path in enumerate(files_to_process, 1):
        logger.info(
            f"[{file_idx}/{len(files_to_process)}] Processing: {file_path.name}"
        )

        if output_mgr is not None:
            # Set up dedicated log file for this file
            output_mgr.setup_file_logger(file_path.name)

        try:
            logger.info(f"Started processing: {file_path.name}")
            result = service.validate_metadata(str(file_path))

            # Save results
            if output_mgr is not None:
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
            if output_mgr is not None:
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

    if output_mgr is not None:
        output_mgr.save_run_summary(
            config=OmegaConf.to_container(cfg.state),
            input_info=input_info,
        )
        aggregate_path = output_mgr.save_run_aggregate()
        if aggregate_path is not None:
            try:
                generate_run_charts_from_file(aggregate_path)
            except Exception:
                logger.exception("Failed to generate run summary chart")

        cost_path = output_mgr.save_run_cost_summary()
        if cost_path is not None:
            logger.info(f"Saved run cost summary to {cost_path}")

    logger.info(
        f"Processed {processed_count}/{len(files_to_process)} files successfully"
    )
    if output_mgr is not None:
        logger.info(f"Output: {output_mgr.get_output_path()}")

    # Cleanup session log handler
    if output_mgr is not None and session_handler:
        logging.getLogger().removeHandler(session_handler)
        session_handler.close()


if __name__ == "__main__":
    main()
