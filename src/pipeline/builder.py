"""LangGraph pipeline orchestration.

This module creates a LangGraph state machine that orchestrates the
pipeline states (load_data, normalize_data, static_analysis, semantic_analysis).
dsl = 
"""

from typing import Sequence

from langgraph.graph import StateGraph, END, START
from langgraph.pregel import CompiledGraph

from agent.state import AgentState
from pipeline.states import (
    load_data,
    static_analysis,
    semantic_analysis,
)


def create_pipeline():
    graph = StateGraph(AgentState)

    graph.add_node(load_data, name="load_data")
    graph.add_edge(START, load_data)
    graph.add_node(static_analysis, name="static_analysis")
    graph.add_edge(load_data, static_analysis)
    graph.add_node(semantic_analysis, name="semantic_analysis")
    graph.add_edge(static_analysis, semantic_analysis)
    graph.add_edge(semantic_analysis, END)

    return CompiledGraph(graph)
