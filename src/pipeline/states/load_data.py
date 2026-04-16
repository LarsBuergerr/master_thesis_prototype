"""Load data state for the pipeline.

This state handles loading the metadata RDF file and the dataset CSV file.
"""

import rdflib
from pathlib import Path
from typing import TYPE_CHECKING
from utils.logger import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from agent.state import AgentState
else:
    AgentState = dict


def load_data(state: AgentState) -> AgentState:
    """Load the metadata and dataset files.

    Expected state keys:
        - metadata_path: path to the RDF metadata file
        - dataset_path: path to the dataset file

    Output state keys:
        - dataset: loaded dataset (pandas DataFrame or similar)
        - metadata: loaded metadata (rdflib Graph or similar)
        - current_step: "load_data"
    """
    metadata_path = state.get("metadata_path")
    dataset_path = state.get("dataset_path")

    if metadata_path:
        try:
            g = rdflib.Graph()
            g.parse(metadata_path, format=rdflib.util.guess_format(metadata_path))
            state["metadata"] = g
            logger.info(f"Loaded metadata from {metadata_path}")
        except Exception as e:
            error_msg = f"Failed to load metadata from {metadata_path}: {e}"
            logger.error(error_msg)
            state["errors"].append(error_msg)

    for triple in state.get("metadata"):
        print(triple)

    return state
