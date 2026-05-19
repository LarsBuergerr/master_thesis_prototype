"""Findability indicators for DCAT-AP-DE metadata.

Validates aspects like keywords, theme, spatial/temporal coverage, etc.
"""

from typing import Any, Dict, List
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import DCAT, DCTERMS

from quality_indicators.models.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from quality_indicators.models.dimension import QualityDimension


class KeywordsCountIndicator(Indicator):
    """Validates if dataset has appropriate number of keywords (2 < k < 6)."""

    def __init__(self):
        super().__init__(
            indicator_id="find_keywords_count",
            name_de="Angemessene Anzahl Schlagwörter",
            name_en="Appropriate number of keywords",
            dimension=QualityDimension.FINDABILITY,
            description_de="Schlagwörter sollten zwischen 2 und 6 vorhanden sein",
            description_en="Keywords should be between 2 and 6",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate keyword count.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on keyword count
        """
        try:
            if not isinstance(metadata, Graph):
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

            # Query for all keywords in the dataset
            keywords = list(metadata.objects(predicate=DCAT.keyword))

            keyword_count = len(keywords)

            # Score calculation:
            # Pass: 2 < k < 6 (k = 3, 4, 5)
            # Partial: k == 2 or k == 6 or 6 < k < 10
            # Fail: k == 1 or k > 10

            if 2 < keyword_count < 6:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = f"Optimale Anzahl Keywords: {keyword_count}"
                message_en = f"Optimal number of keywords: {keyword_count}"

            elif keyword_count in [2, 6] or (6 <= keyword_count < 10):
                status = IndicatorStatus.PARTIAL
                score = 0.7
                message_de = f"Suboptimale Anzahl Keywords: {keyword_count}"
                message_en = f"Suboptimal number of keywords: {keyword_count}"

            else:
                status = IndicatorStatus.FAIL
                score = 0.0
                message_de = f"Ungeeignete Anzahl Keywords: {keyword_count}"
                message_en = f"Inappropriate number of keywords: {keyword_count}"

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
                    "keyword_count": keyword_count,
                    "keywords": [str(kw) for kw in keywords],
                    "expected_range": "2 < k < 6",
                },
            )

        except Exception as e:
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


class ThemeIndicator(Indicator):
    """Validates if dcat:theme is set and from controlled vocabulary."""

    VALID_THEMES = {
        "http://publications.europa.eu/resource/authority/data-theme/AGRI",
        "http://publications.europa.eu/resource/authority/data-theme/ECON",
        "http://publications.europa.eu/resource/authority/data-theme/EDUC",
        "http://publications.europa.eu/resource/authority/data-theme/ENVI",
        "http://publications.europa.eu/resource/authority/data-theme/GOVE",
        "http://publications.europa.eu/resource/authority/data-theme/HEAL",
        "http://publications.europa.eu/resource/authority/data-theme/INTR",
        "http://publications.europa.eu/resource/authority/data-theme/JUST",
        "http://publications.europa.eu/resource/authority/data-theme/REGI",
        "http://publications.europa.eu/resource/authority/data-theme/SOCI",
        "http://publications.europa.eu/resource/authority/data-theme/TECH",
        "http://publications.europa.eu/resource/authority/data-theme/TRAN",
    }

    def __init__(self):
        super().__init__(
            indicator_id="find_theme_valid",
            name_de="Theme aus kontrolliertem Vokabular",
            name_en="Theme from controlled vocabulary",
            dimension=QualityDimension.FINDABILITY,
            description_de="dcat:theme sollte aus dem europäischen Daten-Thesaurus sein",
            description_en="dcat:theme should be from EU data theme vocabulary",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate theme against controlled vocabulary.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on theme validity
        """
        try:
            if not isinstance(metadata, Graph):
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

            themes = list(metadata.objects(predicate=DCAT.theme))

            if not themes:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein Theme angegeben",
                    message_en="No theme specified",
                    details={"theme_count": 0},
                )

            valid_themes = [str(t) for t in themes if str(t) in self.VALID_THEMES]
            invalid_themes = [str(t) for t in themes if str(t) not in self.VALID_THEMES]

            if invalid_themes:
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = (
                    f"Einige Themes sind nicht aus dem kontrollierten Vokabular"
                )
                message_en = f"Some themes are not from controlled vocabulary"
            else:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = f"Alle Themes sind aus dem kontrollierten Vokabular"
                message_en = f"All themes are from controlled vocabulary"

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
                    "valid_themes": valid_themes,
                    "invalid_themes": invalid_themes,
                    "valid_count": len(valid_themes),
                    "total_count": len(themes),
                },
            )

        except Exception as e:
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
_keywords_indicator = KeywordsCountIndicator()
_theme_indicator = ThemeIndicator()
