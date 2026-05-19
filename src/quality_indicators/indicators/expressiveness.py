"""Expressiveness indicators for DCAT-AP-DE metadata.

Validates semantic quality aspects like title quality, description quality, etc.
This dimension often requires NLP/LLM analysis for deeper insights.
"""

from typing import Any
from rdflib import Graph
from rdflib.namespace import DCTERMS

from quality_indicators.models.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from quality_indicators.models.dimension import QualityDimension


class TitleQualityIndicator(Indicator):
    """Validates if dct:title is set and has minimum length."""

    MIN_LENGTH = 5
    RECOMMENDED_LENGTH = 15

    def __init__(self):
        super().__init__(
            indicator_id="expr_title_quality",
            name_de="Titel-Qualität",
            name_en="Title quality",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de="Prüft ob Titel aussagekräftig ist (Mindestlänge)",
            description_en="Checks if title is expressive (minimum length)",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate title quality.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on title quality
        """
        try:
            self.logger.debug("Running indicator validation")
            if not isinstance(metadata, Graph):
                self.logger.warning("Invalid metadata format: expected rdflib Graph")
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.ERROR,
                    score=0.0,
                    message_de="Metadaten sind kein rdflib Graph",
                    message_en="Metadata is not an rdflib Graph",
                    error="Invalid metadata format",
                )

            titles = list(metadata.objects(predicate=DCTERMS.title))

            if not titles:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein Titel angegeben",
                    message_en="No title specified",
                    details={"title_count": 0},
                )

            title = str(titles[0])
            title_length = len(title)

            if title_length >= self.RECOMMENDED_LENGTH:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = f"Guter Titel ({title_length} Zeichen)"
                message_en = f"Good title ({title_length} characters)"
            elif title_length >= self.MIN_LENGTH:
                status = IndicatorStatus.PARTIAL
                score = 0.7
                message_de = f"Kurzer Titel ({title_length} Zeichen)"
                message_en = f"Short title ({title_length} characters)"
            else:
                status = IndicatorStatus.FAIL
                score = 0.0
                message_de = f"Sehr kurzer Titel ({title_length} Zeichen)"
                message_en = f"Very short title ({title_length} characters)"

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=message_de,
                message_en=message_en,
                details={
                    "title": title,
                    "title_length": title_length,
                    "min_length": self.MIN_LENGTH,
                    "recommended_length": self.RECOMMENDED_LENGTH,
                },
            )

        except Exception as e:
            self.logger.exception("Indicator validation failed")
            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.ERROR,
                score=0.0,
                message_de="Fehler bei der Validierung",
                message_en="Validation error",
                error=str(e),
            )


class DescriptionQualityIndicator(Indicator):
    """Validates if dct:description is set and has minimum length."""

    MIN_LENGTH = 20
    RECOMMENDED_LENGTH = 100

    def __init__(self):
        super().__init__(
            indicator_id="expr_description_quality",
            name_de="Beschreibungs-Qualität",
            name_en="Description quality",
            dimension=QualityDimension.EXPRESSIVENESS,
            description_de="Prüft ob Beschreibung aussagekräftig ist",
            description_en="Checks if description is expressive",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate description quality.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on description quality
        """
        try:
            self.logger.debug("Running indicator validation")
            if not isinstance(metadata, Graph):
                self.logger.warning("Invalid metadata format: expected rdflib Graph")
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.ERROR,
                    score=0.0,
                    message_de="Metadaten sind kein rdflib Graph",
                    message_en="Metadata is not an rdflib Graph",
                    error="Invalid metadata format",
                )

            descriptions = list(metadata.objects(predicate=DCTERMS.description))

            if not descriptions:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Beschreibung angegeben",
                    message_en="No description specified",
                    details={"description_count": 0},
                )

            description = str(descriptions[0])
            desc_length = len(description)

            if desc_length >= self.RECOMMENDED_LENGTH:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = f"Gute Beschreibung ({desc_length} Zeichen)"
                message_en = f"Good description ({desc_length} characters)"
            elif desc_length >= self.MIN_LENGTH:
                status = IndicatorStatus.PARTIAL
                score = 0.7
                message_de = f"Kurze Beschreibung ({desc_length} Zeichen)"
                message_en = f"Short description ({desc_length} characters)"
            else:
                status = IndicatorStatus.FAIL
                score = 0.0
                message_de = f"Sehr kurze Beschreibung ({desc_length} Zeichen)"
                message_en = f"Very short description ({desc_length} characters)"

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=message_de,
                message_en=message_en,
                details={
                    "description": (
                        description[:100] + "..."
                        if len(description) > 100
                        else description
                    ),
                    "description_length": desc_length,
                    "min_length": self.MIN_LENGTH,
                    "recommended_length": self.RECOMMENDED_LENGTH,
                },
            )

        except Exception as e:
            self.logger.exception("Indicator validation failed")
            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.ERROR,
                score=0.0,
                message_de="Fehler bei der Validierung",
                message_en="Validation error",
                error=str(e),
            )


# Auto-register indicators when imported
_title_quality_indicator = TitleQualityIndicator()
_description_quality_indicator = DescriptionQualityIndicator()
