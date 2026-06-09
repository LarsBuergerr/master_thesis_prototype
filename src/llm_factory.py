"""Construction of LLM clients from plain parameters.

Single source of truth shared by the CLI (``main.py``, which adapts its Hydra
``DictConfig``) and the web backend (which passes request parameters directly).
Both providers use ``ChatOpenAI`` because llama.cpp's server is OpenAI-compatible
— only the ``base_url`` / headers differ.
"""

from __future__ import annotations

import os
from typing import Optional

from langchain_openai import ChatOpenAI

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
LOCAL_BASE_URL = "http://localhost:8080/v1"


def create_openrouter_llm(
    model: str,
    *,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    api_key: Optional[str] = None,
) -> ChatOpenAI:
    """Create a ChatOpenAI client pointed at OpenRouter.

    ``api_key`` falls back to the ``OPENROUTER_API_KEY`` environment variable.
    Raises ``ValueError`` when no key is available.
    """
    api_key = api_key or os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENROUTER_API_KEY environment variable must be set. "
            "Create a .env file in the project root with: "
            "OPENROUTER_API_KEY=your-key"
        )

    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
        base_url=OPENROUTER_BASE_URL,
        default_headers={
            "HTTP-Referer": "https://github.com/lbuerger/master_thesis_prototype",
            "X-Title": "Master Thesis Prototype",
        },
        # Ask OpenRouter to include real cost accounting in each response's
        # usage block so the run cost summary reports actual USD spend.
        extra_body={"usage": {"include": True}},
    )


def create_local_llm(
    model: str = "qwen3.5",
    *,
    base_url: str = LOCAL_BASE_URL,
    temperature: float = 0.0,
    max_tokens: int = 4096,
) -> ChatOpenAI:
    """Create a ChatOpenAI client for a local llama.cpp server.

    llama.cpp serves whatever model is loaded, so ``model`` is mostly a label.
    No real API key is needed (llama.cpp ignores it), but the OpenAI client
    refuses an empty one — a placeholder is sent. OpenRouter-specific headers
    and the ``usage`` cost accounting are dropped since they don't apply locally.
    """
    return ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key="sk-no-key-required",
        base_url=base_url,
    )


def build_llm_from_params(
    *,
    provider: str = "openrouter",
    model: Optional[str] = None,
    base_url: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 4096,
    api_key: Optional[str] = None,
) -> ChatOpenAI:
    """Build the LLM client selected by ``provider``.

    ``provider="local"`` → local llama.cpp server (:func:`create_local_llm`);
    anything else (default ``"openrouter"``) → OpenRouter
    (:func:`create_openrouter_llm`).
    """
    if str(provider).lower() == "local":
        return create_local_llm(
            model=model or "qwen3.5",
            base_url=base_url or LOCAL_BASE_URL,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    if not model:
        raise ValueError("A model id is required for the OpenRouter provider")
    return create_openrouter_llm(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
    )
