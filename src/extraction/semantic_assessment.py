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
        ..., description="Diskretes Urteil für dieses Kriterium (pass/partial/fail)."
    )
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalisierter Qualitätswert, 0.0 (schlechtest) bis 1.0 (voll).",
    )
    reasoning: str = Field(
        ..., description="Kurze, sachliche Begründung des Scores (auf Deutsch)."
    )
    findings: list[str] = Field(
        default_factory=list,
        description="Konkrete beobachtete Stärken/Schwächen für dieses Kriterium.",
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
            "Titel-Qualität. GUT: spezifisch, prägnant, von ähnlichen Datensätzen "
            "anderer Stellen unterscheidbar; Zeit-/Ortsbezug im Titel ist erlaubt "
            "und oft hilfreich (z. B. Datenreihen), wenn er dem Verständnis dient "
            "(Konvention 1.7). ABWERTEN: zu generisch ohne Orts-/Zeitkontext; "
            "Methodik/Erklärungen im Titel (gehören in die Beschreibung); "
            "unerklärte Abkürzungen oder Codes als Hauptkennzeichnung; reine "
            "Wiederholung des Herausgebernamens (wird separat angezeigt)."
        ),
    )
    description_quality: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Beschreibungs-Qualität. Eine gute Beschreibung beantwortet: "
            "1) Was ist enthalten? 2) Wie ist es strukturiert (Format, "
            "Tabellenaufbau, Kategorien, Kodierung)? 3) Wie und warum wurden die "
            "Daten erhoben (Methode, Quelle, Stichprobengröße)? 4) Wozu / welcher "
            "Zweck? 5) Besonderheiten (Stichtag, vorläufige/geschätzte Daten, "
            "Qualitäts-Disclaimer, KI-Unterstützung, Links zur Dokumentation)? "
            "Bei CSV zusätzlich Trennzeichen und Zeichenkodierung. ABWERTEN: "
            "wiederholt nur den Titel; sehr kurz ohne strukturelle Information; "
            "enthält HTML-/Markdown-Formatierung (GovData zeigt Beschreibungen als "
            "Rohtext an)."
        ),
    )
    title_description_coherence: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Kohärenz von Titel und Beschreibung: müssen inhaltlich zusammenpassen "
            "und sich gegenseitig stützen; Widersprüche (anderes Thema, anderer "
            "Ort/Zeitraum) abwerten."
        ),
    )
    keyword_quality: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Schlagwort-Qualität. GUT: kurze, "
            "singularische, laienverständliche Begriffe ('Museum', 'Kultur', nicht "
            "'Museumskulturangebot'); inhaltlich spezifisch; mehrsprachige Varianten "
            "sind ein Plus. ABWERTEN: Komposita statt "
            "atomarer Begriffe; Pluralformen ('Veranstaltungen' → 'Veranstaltung'); "
            "reiner Jargon/Abkürzungen ('BauGB' statt 'Baugesetzbuch'); Redundanz "
            "mit dem Titel; formale/offensichtliche Tags ('Gemeinde', Jahreszahl, "
            "Herausgebername — stehen bereits in eigenen Feldern); übermäßig viele "
            "(>15, meist Füllwerk)."
        ),
    )
    thematic_consistency: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Thematische Konsistenz: Thema (dcat:theme), Schlagwörter, Titel und "
            "Beschreibung müssen ein kohärentes Themenbild ergeben. "
            "Beispiel-Inkonsistenz: als ECON (Wirtschaft/Finanzen) kategorisiert, "
            "aber die Schlagwörter sind rein geografisch ohne Wirtschaftsbezug. "
            "Off-topic-Signale in irgendeinem Feld senken den Score."
        ),
    )
    contextual_qualifiers: ExpressivenessCriterion = Field(
        ...,
        description=(
            "Kontextuelle Qualifizierer — nur bewerten, wenn der Inhalt sie "
            "erfordert: Zeitreihen/Statistiken → Jahr oder Bezugszeitraum; Geodaten "
            "→ räumliche Abdeckung, wo nicht offensichtlich; Erhebungs-/"
            "Verwaltungsdaten → Stichtag; geschätzte/vorläufige Daten → "
            "'vorläufig'/'geschätzt'/'hochgerechnet'; Entwurfsdaten → 'Entwurf' "
            "gekennzeichnet; regelmäßig aktualisierte Daten → Aktualisierungszyklus; "
            "abgeleitete/aggregierte Daten → Aggregationsmethode. Ein einmaliger, "
            "statischer Datensatz braucht keinen Stichtag — Fehlen nur abwerten, "
            "wenn der Datentyp den Qualifizierer klar verlangt."
        ),
    )
    overall_summary: str = Field(
        ...,
        description="Ein- bis zweisätziges Gesamturteil zur Aussagekraft (auf Deutsch).",
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
# Prompt (German only; expressiveness-only). The concrete per-criterion rubric
# lives in the ``ExpressivenessAssessment`` field descriptions above, which the
# structured-output (function-calling) schema passes to the model — so the
# system prompt only carries the role and the general rules.
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = (
    "Du bist ein strenger Auditor für die *Aussagekraft* von "
    "DCAT-AP-DE-Metadaten. Du bewertest ausschließlich, ob die Metadaten "
    "inhaltlich aussagekräftig, verständlich und in sich widerspruchsfrei sind "
    "— nicht ihre technische Zugänglichkeit, Lizenzierung oder Auffindbarkeit.\n\n"
    "Regeln:\n"
    "- Wende für jedes Kriterium die Bewertungsregeln aus dessen Feldbeschreibung "
    "an (belegt durch DCAT-AP.de Konventionenhandbuch v2.0 Kap. 1.7/3.4 und die "
    "Handreichung zur Metadatenqualität).\n"
    "- Feldpräsenz allein genügt nicht; vorhandene, aber generische, kryptische "
    "oder widersprüchliche Angaben werden abgewertet.\n"
    "- Begründe jede Abwertung kurz und sachlich; erfinde keine Informationen, "
    "bewerte nur die beobachtbare Evidenz.\n"
    "- Verfasse `reasoning`, `findings` und `overall_summary` auf Deutsch.\n"
    "- score: 1.0 = vollständig aussagekräftig, 0.0 = unbrauchbar; status "
    "entsprechend pass/partial/fail."
)

_USER_PROMPT = (
    "Bewerte die Aussagekraft der folgenden Metadaten und gib das Ergebnis als "
    "`ExpressivenessAssessment` zurück.\n\nMetadaten (JSON):\n{context}"
)


def _build_messages(context: "DatasetContext") -> list[tuple[str, str]]:
    payload = context.to_agent_json()
    return [
        ("system", _SYSTEM_PROMPT),
        ("human", _USER_PROMPT.format(context=payload)),
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
        result = structured.invoke(_build_messages(context))
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
