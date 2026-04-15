import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import hydra
from omegaconf import DictConfig, OmegaConf
import logging

from langchain_openai import ChatOpenAI

from agent.state import AgentState
from utils.enums.language import Language
from utils.enums.llm_model import LLMModel
from pipeline.builder import create_pipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_llm(cfg: DictConfig) -> ChatOpenAI:
    """Create an LLM client from the config.

    Args:
        cfg: Hydra configuration

    Returns:
        Configured ChatOpenAI instance for OpenRouter
    """
    print(cfg)
    model = cfg.state.llm.model
    temperature = cfg.state.llm.get("temperature", 0.0) if cfg.state.llm else 0.0
    max_tokens = cfg.state.llm.get("max_tokens", 4096) if cfg.state.llm else 4096
    base_url = "https://openrouter.ai/api/v1"

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable must be set. "
            "Create a .env file in the project root with: OPENROUTER_API_KEY=your-key"
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

def create_agent(cfg: DictConfig, llm: ChatOpenAI) -> AgentState:
    """Create an AgentState from the state config.

    Args:
        cfg: Hydra configuration (state config)
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


@hydra.main(version_base=None, config_path="../conf", config_name="state/state_1")
def main(cfg: DictConfig) -> None:
    """Main entry point for the pipeline.

    Uses all configurable parameters from the Hydra config file.
    The config file (state_1.yaml) contains all agent state variables
    and pipeline configuration.
    """
    logger.info("Starting pipeline...")
    logger.info(OmegaConf.to_yaml(cfg))

    llm = create_llm(cfg)
    agent = create_agent(cfg, llm)
    pipeline = create_pipeline()

    logger.info(f"Data directory: {agent.get('directory_path')}")

    # Process all subdirectories in the data directory
    if not Path(agent.get('directory_path')).exists():
        logger.error(f"Data directory does not exist: {agent.get('directory_path')}")
        return

    results = []

    for directory in sorted(Path(agent.get('directory_path')).iterdir()):
        if not directory.is_dir():
            continue

        # Check for valid data files
        has_metadata = (directory / "metadata.rdf").exists()
        has_dataset = (directory / "dataset.csv").exists()

        if not has_metadata or not has_dataset:
            logger.debug(f"Skipping invalid directory: {directory}")
            continue

        logger.info(f"Processing directory: {directory}")

        try:
            # Create initial state for this directory
            initial_state = AgentState(
                messages=[],
                directory_path=str(directory),
                metadata_path=str(directory / "metadata.rdf"),
                dataset_path=str(directory / "dataset.csv"),
                dataset_df=None,
                metadata=[],
                language=Language.DE if cfg.get("language", "de") == "de" else Language.EN,
                llm_model=LLMModel(cfg.get("llm_model", "anthropic/claude-sonnet-4.5")),
                result={},
                errors=[],
            )

            # Run the pipeline
            result = pipeline.invoke(initial_state)

            results.append({
                "directory": str(directory),
                "state": result,
            })

            logger.info(f"Completed: {directory}")

        except Exception as e:
            logger.error(f"Error processing {directory}: {e}")

    logger.info(f"Processed {len(results)} directories successfully")

    # Summary of results
    for r in results:
        dir_path = r["directory"]
        state = r["state"]
        errors = state.get("errors", [])
        logger.info(f"  {Path(dir_path).name}: {'OK' if not errors else f'Errors: {errors}'}")


if __name__ == "__main__":
    main()