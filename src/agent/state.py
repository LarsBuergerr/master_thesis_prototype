from typing import Any, TypedDict, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

from utils.enums.language import Language
from utils.enums.llm_model import LLMModel


class AgentState(TypedDict):
    """LangGraph state for the agent pipeline.

    Contains all relevant information about the current processing state
    """

    messages: list[Union[HumanMessage, SystemMessage, AIMessage]]
    directory_path: str
    metadata_path: str
    dataset_path: Optional[str]
    dataset_df: Optional[Any]
    metadata: list[Any]
    language: Optional[Language]
    llm: ChatOpenAI
    llm_model: LLMModel
    result: dict[str, Any]
    errors: list[str]
    quality_metadata: Optional[Any]
    quality_results: Optional[dict[str, Any]]
    quality_summary: Optional[dict[str, Any]]

    def __init__(self):
        self.messages = []
        self.directory_path = ""
        self.metadata_path = ""
        self.dataset_path = None
        self.dataset_df = None
        self.metadata = []
        self.language = None
        self.llm = None
        self.llm_model = None
        self.result = {}
        self.errors = []
        self.quality_metadata = None
        self.quality_results = None
        self.quality_summary = None

    def __getitem__(self, key):
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
