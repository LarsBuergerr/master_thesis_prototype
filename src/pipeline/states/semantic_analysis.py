"""Semantic analysis state for the pipeline.

This state performs semantic analysis on the dataset and metadata using LLM.
"""

from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dtos.dto_loader import import_language_dto
from utils.logger import get_logger
from prompts.semantic_analysis import semantic_analysis_prompt
from dtos.base.semantic_analysis_base import SemanticAnalysisBase

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
    SemanticAnalysis = import_language_dto(state.get("language"), SemanticAnalysisBase)

    semantic_analysis_system_prompt = semantic_analysis_prompt.get_prompt(
        state.get("language"), "semantic_analysis_system_prompt"
    )

    semantic_analysis_user_prompt = semantic_analysis_prompt.get_prompt(
        state.get("language"),
        "semantic_analysis_user_prompt",
        metadata_content=state.get("metadata"),
    )

    logger.debug(semantic_analysis_system_prompt)
    logger.debug(semantic_analysis_user_prompt)

    semantic_analysis_user_message = HumanMessage(content=semantic_analysis_user_prompt)

    llm_agent = create_agent(
        model=state.get("llm"),
        response_format=SemanticAnalysis,
        system_prompt=semantic_analysis_system_prompt,
    )

    llm_response = llm_agent.invoke({"messages": [semantic_analysis_user_message]})

    logger.debug(f"LLM response for semantic analysis: {llm_response}")

    state["result"]["semantic_analysis_results"] = llm_response

    logger.debug(f"Semantic analysis response: {state.get('result')}")

    logger.info("Performing semantic analysis...")
    return state
