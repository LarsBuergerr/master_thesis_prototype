"""LangGraph pipeline orchestration.

This module creates a LangGraph state machine that orchestrates the
pipeline states (load_data, normalize_data, static_analysis, semantic_analysis).
dsl =
"""

from langgraph.graph import END, START, StateGraph
from omegaconf import DictConfig

from agent.state import AgentState
from pipeline.states import (
    load_data,
    semantic_analysis,
    static_analysis,
)
from pipeline.states import quality_validation


def create_pipeline(cfg: DictConfig):
    graph = StateGraph(AgentState)

    steps = [
        ("load_data", load_data, cfg.state.pipeline.get("load_data", True)),
        (
            "static_analysis",
            static_analysis,
            cfg.state.pipeline.get("static_analysis", True),
        ),
        (
            "quality_validation",
            quality_validation,
            cfg.state.pipeline.get("quality_validation", True),
        ),
        (
            "semantic_analysis",
            semantic_analysis,
            cfg.state.pipeline.get("semantic_analysis", True),
        ),
    ]

    enabled_steps = [(name, fn) for name, fn, enabled in steps if enabled]

    if not enabled_steps:
        raise ValueError("At least one pipeline step must be enabled.")

    previous = START
    for name, fn in enabled_steps:
        graph.add_node(name, fn)
        graph.add_edge(previous, name)
        previous = name

    graph.add_edge(previous, END)

    return graph.compile()
