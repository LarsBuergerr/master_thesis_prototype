"""Expressiveness indicators for DCAT-AP-DE metadata.

Expressiveness — is the metadata *meaningful and self-consistent*? — can't be
judged by field presence or regexes, so this whole dimension is scored by a
single LLM call per dataset. ``attach_semantic_assessment`` (run up-front by
``QualityMetricsService``) stores one validated
:class:`ExpressivenessAssessment` on the ``DatasetContext``; each indicator
below is just a *view* onto one criterion of that shared result.

The indicators never call the LLM themselves — they're pure functions of the
context, exactly like the accessibility indicators that read ``dist.probe``.
When no assessment is attached (no LLM configured, or the call failed), they
report NOT_APPLICABLE instead of crashing.
"""

from typing import Any, Optional

from rdflib import Graph

from core.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from core.dimension import QualityDimension
from extraction.dataset_context import DatasetContext
from extraction.semantic_assessment import ExpressivenessCriterion


_STATUS_MAP = {
    "pass": IndicatorStatus.PASS,
    "partial": IndicatorStatus.PARTIAL,
    "fail": IndicatorStatus.FAIL,
}


class LLMBackedExpressivenessIndicator(Indicator):
    """Base for expressiveness indicators backed by the shared LLM assessment.

    A subclass only declares its identity and which criterion field it reads
    (``criterion``); this base handles fetching the assessment from the
    context, the not-attached fallback, and mapping the criterion to an
    :class:`IndicatorResult`.
    """

    #: Field name on ``ExpressivenessAssessment`` this indicator surfaces.
    criterion: str = ""

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                if not isinstance(metadata, Graph):
                    return self._error("Metadata is not an rdflib Graph")
                context = DatasetContext.from_graph(metadata)

            assessment = context.semantic_assessment
            if assessment is None:
                # No LLM configured or the one-shot call failed. Distinct from
                # a genuine low score — surfaced as NOT_APPLICABLE.
                self.logger.info(
                    f"[{self.indicator_id}] NOT_APPLICABLE | no LLM assessment attached"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.NOT_APPLICABLE,
                    score=0.0,
                    message_de="Keine LLM-Bewertung verfügbar",
                    message_en="No LLM assessment available",
                    details={"criterion": self.criterion},
                )

            crit: ExpressivenessCriterion = getattr(assessment, self.criterion)
            status = _STATUS_MAP.get(crit.status, IndicatorStatus.PARTIAL)
            self.logger.info(
                f"[{self.indicator_id}] {status.value} | score={crit.score:.2f} | "
                f"{crit.reasoning[:120]}"
            )
            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=crit.score,
                message_de=crit.reasoning,
                message_en=crit.reasoning,
                details={
                    "criterion": self.criterion,
                    "llm_status": crit.status,
                    "findings": crit.findings,
                    "overall_summary": assessment.overall_summary,
                },
            )

        except Exception as e:
            self.logger.exception(
                f"[{self.indicator_id}] Validation failed with exception"
            )
            return self._error(str(e))

    def _error(self, error: str) -> IndicatorResult:
        return IndicatorResult(
            indicator_id=self.indicator_id,
            name_de=self.name_de,
            name_en=self.name_en,
            dimension=self.dimension,
            status=IndicatorStatus.ERROR,
            score=0.0,
            message_de="Fehler bei der Validierung",
            message_en="Validation error",
            error=error,
        )


class TitleQualityIndicator(LLMBackedExpressivenessIndicator):
    criterion = "title_quality"

    def __init__(self):
        super().__init__(
            indicator_id="expr_title_quality",
            name_de="Titel-Qualität",
            name_en="Title quality",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de="Ist der Titel aussagekräftig, spezifisch und ohne kryptische Abkürzungen?",
            description_en="Is the title descriptive, specific and free of cryptic abbreviations?",
            weight=1.0,
        )


class DescriptionQualityIndicator(LLMBackedExpressivenessIndicator):
    criterion = "description_quality"

    def __init__(self):
        super().__init__(
            indicator_id="expr_description_quality",
            name_de="Beschreibungs-Qualität",
            name_en="Description quality",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de="Ist die Beschreibung inhaltlich substanziell und informativ?",
            description_en="Is the description substantive and informative?",
            weight=1.0,
        )


class TitleDescriptionCoherenceIndicator(LLMBackedExpressivenessIndicator):
    criterion = "title_description_coherence"

    def __init__(self):
        super().__init__(
            indicator_id="expr_title_description_coherence",
            name_de="Kohärenz von Titel und Beschreibung",
            name_en="Title–description coherence",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de="Passen Titel und Beschreibung inhaltlich zusammen?",
            description_en="Do the title and description agree with each other?",
            weight=1.0,
        )


class KeywordQualityIndicator(LLMBackedExpressivenessIndicator):
    criterion = "keyword_quality"

    def __init__(self):
        super().__init__(
            indicator_id="expr_keyword_quality",
            name_de="Schlagwort-Qualität",
            name_en="Keyword quality",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de="Sind die Schlagwörter relevant, spezifisch und konsistent formatiert?",
            description_en="Are keywords relevant, specific and consistently formatted?",
            weight=1.0,
        )


class ThematicConsistencyIndicator(LLMBackedExpressivenessIndicator):
    criterion = "thematic_consistency"

    def __init__(self):
        super().__init__(
            indicator_id="expr_thematic_consistency",
            name_de="Thematische Konsistenz",
            name_en="Thematic consistency",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de="Sind Themen, Schlagwörter, Titel und Beschreibung widerspruchsfrei?",
            description_en="Are themes, keywords, title and description mutually consistent?",
            weight=1.0,
        )


class ContextualQualifiersIndicator(LLMBackedExpressivenessIndicator):
    criterion = "contextual_qualifiers"

    def __init__(self):
        super().__init__(
            indicator_id="expr_contextual_qualifiers",
            name_de="Kontextuelle Qualifizierer",
            name_en="Contextual qualifiers",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de=(
                "Sind nötige Kontextangaben (Version, Bezugszeitraum, vorläufig/"
                "geschätzt/aggregiert/Entwurf) vorhanden, wo der Inhalt sie erfordert?"
            ),
            description_en=(
                "Are needed contextual qualifiers (version, reference period, "
                "provisional/estimated/aggregated/draft) present where the content requires them?"
            ),
            weight=1.0,
        )


# Auto-register indicators when imported
_title_quality_indicator = TitleQualityIndicator()
_description_quality_indicator = DescriptionQualityIndicator()
_title_description_coherence_indicator = TitleDescriptionCoherenceIndicator()
_keyword_quality_indicator = KeywordQualityIndicator()
_thematic_consistency_indicator = ThematicConsistencyIndicator()
_contextual_qualifiers_indicator = ContextualQualifiersIndicator()
