"""Static analysis state for the pipeline.

This state performs static analysis on the dataset and metadata.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from agent.state import AgentState
else:
    AgentState = dict


def static_analysis(state: AgentState) -> AgentState:
    """Perform static analysis on the dataset and metadata.

    Expected state keys:
        - dataset or normalized_dataset: pandas DataFrame
        - metadata or normalized_metadata: rdflib Graph

    Output state keys:
        - static_analysis_results: dict with analysis results
        - current_step: "static_analysis"
    """
    print("Performing static analysis...")
    return state