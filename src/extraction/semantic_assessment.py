"""LLM-backed semantic assessment for the *expressiveness* dimension.

Expressiveness is the one dimension that can't be scored deterministically —
it's about whether the metadata is *meaningful and self-consistent* (is the
title descriptive, does the description match it, are tags/themes coherent,
are contextual qualifiers present). Those are judgement calls, so a single LLM
call produces the whole dimension's assessment up front and the individual
expressiveness indicators each read their own slice from it.

This mirrors the ``attach_probes`` pattern in
``distribution_probes``: one expensive shared resource is computed
once per dataset and stashed on the :class:`DatasetContext`; the indicators
that consume it stay pure functions of the context and never touch the LLM.
"""

from __future__ import annotations

import logging
import time
from logging import Logger
from typing import TYPE_CHECKING, Any, Literal, Optional

from pydantic import BaseModel, Field

if TYPE_CHECKING:  # avoid an import cycle with dataset_context
    from extraction.dataset_context import DatasetContext


class ExpressivenessCriterion(BaseModel):
    """One scored expressiveness criterion.

    ``score`` is normalised to 0.0–1.0 so it drops straight into an
    :class:`IndicatorResult`; ``status`` is the discrete verdict the indicator
    surfaces; ``reasoning`` / ``findings`` justify the score (the auditor must
    explain every deduction).
    """

    status: Literal["pass", "partial", "fail"] = Field(
        ..., description="Discrete verdict for this criterion."
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalised quality score, 0.0 (worst) to 1.0 (full).",
    )
    reasoning: str = Field(
        ..., description="Short, factual justification for the score."
    )
    findings: list[str] = Field(
        default_factory=list,
        description="Concrete strengths/weaknesses observed for this criterion.",
    )


class ExpressivenessAssessment(BaseModel):
    """Holistic, one-call expressiveness assessment of a dataset's metadata.

    Each field maps 1:1 to an ``expr_*`` indicator; the field names are the
    contract between this schema and :data:`CRITERION_KEYS` /
    ``LLMBackedExpressivenessIndicator.criterion`` in the indicators module.
    """

    title_quality: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Is the title descriptive and specific, free of unexplained "
            "abbreviations or cryptic codes?"
        ),
    )
    description_quality: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Is the description substantive and informative — does it explain "
            "what the data actually contains, not just restate the title?"
        ),
    )
    title_description_coherence: ExpressivenessCriterion = Field(
        ...,
        description="Do the title and the description agree and reinforce each other?",
    )
    keyword_quality: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Are the keywords/tags relevant, specific, consistently formatted, "
            "and non-redundant?"
        ),
    )
    thematic_consistency: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Are themes, keywords, title and description mutually consistent "
            "(no off-topic or contradictory signals)?"
        ),
    )
    contextual_qualifiers: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Are needed contextual qualifiers (version, reference period, "
            "provisional/estimated/aggregated/draft/archived, coverage) present "
            "where the content clearly calls for them?"
        ),
    )
    overall_summary: str = Field(
        ..., description="One- or two-sentence overall verdict on expressiveness."
    )


# Field names on ExpressivenessAssessment that represent a scored criterion
# (everything except the free-text summary). Single source of truth shared
# with the indicators module so the two can't drift.
CRITERION_KEYS: tuple[str, ...] = (
    "title_quality",
    "description_quality",
    "title_description_coherence",
    "keyword_quality",
    "thematic_consistency",
    "contextual_qualifiers",
)


# ---------------------------------------------------------------------------
# Prompt (localised; expressiveness-only, not the full 5-category audit)
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = {
    "de": (
        "Du bist ein strenger Auditor für die *Aussagekraft* von "
        "DCAT-AP-DE-Metadaten. Du bewertest ausschließlich, ob die Metadaten "
        "inhaltlich aussagekräftig, verständlich und in sich widerspruchsfrei "
        "sind — nicht ihre technische Zugänglichkeit, Lizenzierung oder "
        "Auffindbarkeit.\n\n"
        "Regeln:\n"
        "- Feldpräsenz allein genügt nicht; vorhandene, aber generische, "
        "kryptische oder widersprüchliche Angaben werden abgewertet.\n"
        "- Begründe jede Abwertung kurz und sachlich.\n"
        "- Erfinde keine Informationen; bewerte nur die beobachtbare Evidenz.\n"
        "- Verfasse `reasoning` und `findings` auf Deutsch.\n"
        "- score: 1.0 = vollständig aussagekräftig, 0.0 = unbrauchbar; "
        "status entsprechend pass/partial/fail."
    ),
    "en": (
        "You are a strict auditor for the *expressiveness* of DCAT-AP-DE "
        "metadata. You judge only whether the metadata is meaningful, "
        "understandable and internally consistent — not its technical "
        "accessibility, licensing or findability.\n\n"
        "Rules:\n"
        "- Field presence alone is not enough; present-but-generic, cryptic or "
        "contradictory values must be marked down.\n"
        "- Justify every deduction briefly and factually.\n"
        "- Do not invent information; assess only observable evidence.\n"
        "- Write `reasoning` and `findings` in English.\n"
        "- score: 1.0 = fully expressive, 0.0 = unusable; set status "
        "accordingly to pass/partial/fail."
    ),
}

_USER_PROMPT = {
    "de": (
        "Bewerte die Aussagekraft der folgenden Metadaten und gib das Ergebnis "
        "als `ExpressivenessAssessment` zurück.\n\nMetadaten (JSON):\n{context}"
    ),
    "en": (
        "Assess the expressiveness of the following metadata and return the "
        "result as `ExpressivenessAssessment`.\n\nMetadata (JSON):\n{context}"
    ),
}


def _build_messages(context: "DatasetContext", language: str) -> list[tuple[str, str]]:
    lang = language if language in _SYSTEM_PROMPT else "de"
    payload = context.to_agent_json()
    return [
        ("system", _SYSTEM_PROMPT[lang]),
        ("human", _USER_PROMPT[lang].format(context=payload)),
    ]


def attach_semantic_assessment(
    context: "DatasetContext",
    llm,
    *,
    language: str = "de",
    logger: Optional[Logger] = None,
) -> None:
    """Run the one-shot expressiveness LLM call and stash it on ``context``.

    On success ``context.semantic_assessment`` holds a validated
    :class:`ExpressivenessAssessment`. On any failure it is left as ``None``
    and the error is logged — the expressiveness indicators then report
    ``NOT_APPLICABLE`` rather than crashing the run.
    """
    log = logger or logging.getLogger(__name__)
    try:
        structured = llm.with_structured_output(
            ExpressivenessAssessment, method="function_calling", include_raw=True
        )
        started = time.perf_counter()
        result = structured.invoke(_build_messages(context, language))
        latency = time.perf_counter() - started

        assessment = result.get("parsed") if isinstance(result, dict) else result
        raw = result.get("raw") if isinstance(result, dict) else None
        context.semantic_assessment = assessment
        context.llm_usage.append(
            _extract_usage(raw, latency, fallback_model=_model_name(llm))
        )
        log.debug(
            "Attached expressiveness assessment "
            f"(summary: {assessment.overall_summary[:120]!r})"
        )
    except Exception:
        log.exception(
            "Expressiveness LLM assessment failed; leaving context.semantic_assessment unset"
        )


def _model_name(llm) -> Optional[str]:
    return getattr(llm, "model_name", None) or getattr(llm, "model", None)


def _extract_usage(raw: Any, latency: float, *, fallback_model: Optional[str]) -> dict:
    """Pull token counts and (OpenRouter) cost off a raw LLM response message.

    Token counts come from the normalised ``usage_metadata``; the cost (USD) is
    non-standard and only present when OpenRouter usage accounting is enabled
    (``extra_body={"usage": {"include": true}}``) — we scan the raw usage block
    for it and leave ``cost_usd`` as ``None`` when unavailable.
    """
    usage_md = getattr(raw, "usage_metadata", None) or {}
    resp_md = getattr(raw, "response_metadata", None) or {}
    token_usage = resp_md.get("token_usage") or resp_md.get("usage") or {}

    cost = None
    for src in (token_usage, resp_md):
        if isinstance(src, dict) and src.get("cost") is not None:
            cost = src.get("cost")
            break

    return {
        "model": resp_md.get("model_name") or fallback_model,
        "input_tokens": usage_md.get("input_tokens"),
        "output_tokens": usage_md.get("output_tokens"),
        "total_tokens": usage_md.get("total_tokens"),
        "cost_usd": cost,
        "latency_seconds": round(latency, 3),
    }
