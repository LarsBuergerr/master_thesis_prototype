import os
import logging
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import hydra
from omegaconf import DictConfig, OmegaConf

from langchain_openai import ChatOpenAI

# Import logger after logging is configured
from utils.logger import get_logger
from agent.state import AgentState
from utils.enums.language import Language
from utils.enums.llm_model import LLMModel
from pipeline.builder import create_pipeline

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


def create_agent_state(cfg: DictConfig, llm: ChatOpenAI) -> AgentState:
    """Create an AgentState from the state config.

    Args:
        cfg: Hydra configuration
        llm: Initialized ChatOpenAI instance

    Returns:
        Initialized AgentState
    """
    # Parse language from config
    lang = cfg.get("language", "de")
    language = Language.DE if lang == "de" else Language.EN

    # Parse LLM model from config
    model_name = cfg.state.llm.get("model", "anthropic/claude-sonnet-4.5")
    llm_model = LLMModel(model_name)

    return AgentState(
        messages=[],
        directory_path=cfg.state.get("directory_path", ""),
        metadata_path=cfg.state.get("metadata_path", ""),
        dataset_path=cfg.state.get("dataset_path", None),
        dataset_df=None,
        metadata=[],
        language=language,
        llm=llm,
        llm_model=llm_model,
        result={},
        errors=[],
    )


def create_agent_state_for_directory(
    cfg: DictConfig, llm: ChatOpenAI, directory: Path
) -> AgentState:
    """Create an AgentState for a specific data directory.

    Args:
        cfg: Hydra configuration
        llm: Initialized ChatOpenAI instance
        directory: Directory to process

    Returns:
        AgentState configured for the given directory
    """
    state = create_agent_state(cfg, llm)

    metadata_relative_path = cfg.state.get("metadata_path", "")
    dataset_relative_path = cfg.state.get("dataset_path", None)

    state["directory_path"] = str(directory)
    state["metadata_path"] = str(directory / metadata_relative_path)
    state["dataset_path"] = (
        str(directory / dataset_relative_path) if dataset_relative_path else None
    )

    return state


@hydra.main(version_base=None, config_path="../conf", config_name="state/state_1")
def main(cfg: DictConfig) -> None:
    """Main entry point for the pipeline.

    Uses all configurable parameters from the Hydra config file.
    The config file (state_1.yaml) contains all agent state variables
    and pipeline configuration.
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

    logger.info("Starting pipeline...")
    logger.info(OmegaConf.to_yaml(cfg))

    llm = create_llm(cfg)
    base_state = create_agent_state(cfg, llm)
    pipeline = create_pipeline()

    logger.info(f"Data directory: {base_state.get('directory_path')}")

    data_dir = Path(base_state.get("directory_path"))
    if not data_dir.exists():
        logger.error(f"Data directory does not exist: {data_dir}")
        return

    has_subdirs = any(d.is_dir() for d in data_dir.iterdir())

    results = []

    if has_subdirs:
        directories = sorted(data_dir.iterdir())
    else:
        directories = [data_dir]

    metadata_relative_path = cfg.state.get("metadata_path", "")
    dataset_relative_path = cfg.state.get("dataset_path", None)

    for directory in directories:
        if not directory.is_dir():
            continue

        has_metadata = (
            bool(metadata_relative_path)
            and (directory / metadata_relative_path).exists()
        )
        has_dataset = (
            bool(dataset_relative_path) and (directory / dataset_relative_path).exists()
        )

        if not has_metadata or not has_dataset:
            logger.debug(f"Skipping invalid directory: {directory}")
            continue

        logger.info(f"Processing directory: {directory}")

        try:
            initial_state = create_agent_state_for_directory(cfg, llm, directory)

            result = pipeline.invoke(initial_state)

            results.append(
                {
                    "directory": str(directory),
                    "state": result,
                }
            )

            logger.info(f"Completed: {directory}")

        except Exception as e:
            logger.error(f"Error processing {directory}: {e}")

    logger.info(f"Processed {len(results)} directories successfully")

    # Summary of results
    for r in results:
        dir_path = r["directory"]
        state = r["state"]
        errors = state.get("errors", [])
        logger.info(
            f"  {Path(dir_path).name}: {'OK' if not errors else f'Errors: {errors}'}"
        )


if __name__ == "__main__":
    main()
