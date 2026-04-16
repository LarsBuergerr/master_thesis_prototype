"""Semantic analysis state for the pipeline.

This state performs semantic analysis on the dataset and metadata using LLM.
"""

from typing import TYPE_CHECKING, Optional
from utils.logger import get_logger
from agent.prompt import Prompt

logger = get_logger(__name__)

if TYPE_CHECKING:
    from agent.state import AgentState
else:
    AgentState = dict


prompt: Prompt = Prompt(
    de={
        "semantic_analysis_system_prompt": """Führe eine semantische Analyse des Datensatzes und der Metadaten durch.

        """,
        "semantic_analysis_user_prompt": """Gebe mir in Stichpunkten eine kurze semantische Analyse der Metadaten.
            Die Metadaten können aus folgender Datei geladen werden:
                -Pfad: {metadata_path}
            """,
    },
    en={
        "semantic_analysis_system_prompt": """Perform a semantic analysis of the dataset and metadata.
        """,
        "semantic_analysis_user_prompt": """Perform a semantic analysis of the dataset and metadata.
            The metadata can be loaded from the following file:
                -Path: {metadata_path}
            """,
    },
)


def semantic_analysis(state: AgentState, llm=None) -> AgentState:
    """Perform semantic analysis on the dataset and metadata.

    This uses an optional LLM to provide deeper semantic insights about the data.

    Expected state keys:
        - dataset or normalized_dataset: pandas DataFrame
        - metadata or normalized_metadata: rdflib Graph
        - static_analysis_results: results from static analysis

    Output state keys:
        - semantic_analysis_results: dict with semantic analysis results
        - current_step: "semantic_analysis"
    """
    semantic_analysis_user_prompt = prompt.get_prompt(
        state.get("language"),
        "semantic_analysis_user_prompt",
        directory_path=state.get("directory_path"),
        metadata_path=state.get("metadata_path"),
    )

    logger.debug(f"Semantic analysis prompt: {semantic_analysis_user_prompt}")

    logger.info("Performing semantic analysis...")
    return state
