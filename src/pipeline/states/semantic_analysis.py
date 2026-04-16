"""Semantic analysis state for the pipeline.

This state performs semantic analysis on the dataset and metadata using LLM.
"""

from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from utils.logger import get_logger
from agent.prompt import Prompt

logger = get_logger(__name__)


class SemanticAnalysisResult(BaseModel):
    """Pydantic DTO for semantic analysis results."""

    summary: str = Field(description="Brief summary of the dataset and its purpose")
    key_columns: list[str] = Field(
        description="List of important columns and their meaning"
    )
    potential_issues: list[str] = Field(
        description="Potential data quality issues identified"
    )
    recommendations: list[str] = Field(
        description="Recommendations for improving data quality"
    )


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


def semantic_analysis(state: AgentState) -> AgentState:
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

    semantic_analysis_user_message = HumanMessage(content=semantic_analysis_user_prompt)

    llm_agent = create_agent(
        model=state.get("llm"),
        response_format=SemanticAnalysisResult,
        system_prompt="Du bist ein Experte im Bereich Open Data und Datenanalyse. Du bist ein Experte darin, die Qualität von Datensätzen zu bewerten und Verbesserungsvorschläge zu machen.",
    )

    llm_response = llm_agent.invoke({"messages": [semantic_analysis_user_message]})

    state["result"]["semantic_analysis_results"] = llm_response

    logger.debug(f"Semantic analysis response: {state.get('result')}")

    logger.info("Performing semantic analysis...")
    return state
