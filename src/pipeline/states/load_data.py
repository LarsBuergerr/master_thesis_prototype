"""Load data state for the pipeline.

This state handles loading the metadata RDF file and the dataset CSV file.
"""

import rdflib
from pathlib import Path
from typing import TYPE_CHECKING

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
    

    print("Loading data...")

    return state