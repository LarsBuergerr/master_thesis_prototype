"""Findability indicators for DCAT-AP-DE metadata.

Validates aspects like keywords, theme, spatial/temporal coverage, etc.
"""

from typing import Any, Dict, List
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import DCAT, DCTERMS, XSD

from quality_indicators.models.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from quality_indicators.models.dimension import QualityDimension
from quality_indicators.vocabularies import (
    VALID_THEME_URIS,
    VALID_FREQUENCY_URIS,
)
from utils.datetime_utils import is_valid_xs_datetime

# locn namespace
LOCN = Namespace("http://www.w3.org/ns/locn#")


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


class ThemeIndicator(Indicator):
    """Validates if dcat:theme is set and from controlled vocabulary."""

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

            themes = list(metadata.objects(predicate=DCAT.theme))
            print(themes)

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

            valid_themes = [str(t) for t in themes if str(t) in VALID_THEME_URIS]
            invalid_themes = [str(t) for t in themes if str(t) not in VALID_THEME_URIS]

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
_keywords_indicator = KeywordsCountIndicator()
_theme_indicator = ThemeIndicator()


class ThemePresenceIndicator(Indicator):
    """Validates presence of dcat:theme (non-empty)."""

    def __init__(self):
        super().__init__(
            indicator_id="find_theme_present",
            name_de="Theme angegeben",
            name_en="Theme present",
            dimension=QualityDimension.FINDABILITY,
            description_de="dcat:theme sollte gesetzt und nicht leer sein",
            description_en="dcat:theme should be set and not empty",
            weight=0.8,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
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

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.PASS,
                score=1.0,
                message_de=f"{len(themes)} Theme(s) angegeben",
                message_en=f"{len(themes)} theme(s) present",
                details={"theme_count": len(themes)},
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


class LocnGeometryIndicator(Indicator):
    """Checks presence of locn:geometry and non-empty value."""

    def __init__(self):
        super().__init__(
            indicator_id="find_locn_geometry",
            name_de="Räumliche Suchangabe (Geometrie)",
            name_en="Spatial search term (geometry)",
            dimension=QualityDimension.FINDABILITY,
            description_de="Prüft ob locn:geometry gesetzt ist",
            description_en="Checks if locn:geometry is set",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
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

            geometries = list(metadata.objects(predicate=LOCN.geometry))

            if not geometries:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine locn:geometry gefunden",
                    message_en="No locn:geometry found",
                    details={"geometry_count": 0},
                )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.PASS,
                score=1.0,
                message_de=f"{len(geometries)} geometrische Angabe(n) gefunden",
                message_en=f"{len(geometries)} geometry value(s) found",
                details={"geometries": [str(g) for g in geometries]},
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


class AdminUnitL2Indicator(Indicator):
    """Checks locn:adminUnitL2 references are present and plausible."""

    def __init__(self):
        super().__init__(
            indicator_id="find_adminunitl2",
            name_de="Räumliche Suche aus kontrolliertem Vokabular",
            name_en="Spatial search from controlled vocabulary",
            dimension=QualityDimension.FINDABILITY,
            description_de="Prüft ob locn:adminUnitL2 auf dcat-ap politische Kodierung verweist",
            description_en="Checks if locn:adminUnitL2 references dcat-ap political geocoding",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
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

            admin_units = list(metadata.objects(predicate=LOCN.adminUnitL2))

            if not admin_units:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein locn:adminUnitL2 angegeben",
                    message_en="No locn:adminUnitL2 specified",
                    details={"admin_unit_count": 0},
                )

            # Plausibility: should start with dcat-ap politicalGeocoding base
            valid = [
                str(a)
                for a in admin_units
                if str(a).startswith("http://dcat-ap.de/def/politicalGeocoding/")
            ]
            invalid = [
                str(a)
                for a in admin_units
                if not str(a).startswith("http://dcat-ap.de/def/politicalGeocoding/")
            ]

            status = IndicatorStatus.PASS if invalid == [] else IndicatorStatus.PARTIAL
            score = 1.0 if invalid == [] else 0.5

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=(
                    "Alle adminUnitL2 verweisen auf dcat-ap"
                    if invalid == []
                    else "Einige adminUnitL2 sind nicht aus dcat-ap"
                ),
                message_en=(
                    "All adminUnitL2 reference dcat-ap"
                    if invalid == []
                    else "Some adminUnitL2 are not from dcat-ap"
                ),
                details={"valid": valid, "invalid": invalid, "total": len(admin_units)},
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


class TemporalCoverageIndicator(Indicator):
    """Checks for temporal coverage via dct:temporal or dcat:startDate/endDate."""

    def __init__(self):
        super().__init__(
            indicator_id="find_temporal_coverage",
            name_de="Zeitliche Abdeckung angegeben",
            name_en="Temporal coverage specified",
            dimension=QualityDimension.FINDABILITY,
            description_de="Prüft ob dct:temporal / dcat:startDate|endDate gesetzt sind",
            description_en="Checks if dct:temporal or dcat:startDate/endDate are set",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
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

            temporal = list(metadata.objects(predicate=DCTERMS.temporal))
            start = list(metadata.objects(predicate=URIRef(str(DCAT) + "startDate")))
            end = list(metadata.objects(predicate=URIRef(str(DCAT) + "endDate")))

            if temporal or start or end:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.PASS,
                    score=1.0,
                    message_de="Zeitliche Abdeckung vorhanden",
                    message_en="Temporal coverage present",
                    details={
                        "temporal_count": len(temporal),
                        "start_count": len(start),
                        "end_count": len(end),
                    },
                )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.FAIL,
                score=0.0,
                message_de="Keine zeitliche Abdeckung gefunden",
                message_en="No temporal coverage found",
                details={"temporal_count": 0, "start_count": 0, "end_count": 0},
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


class DateTimeFieldIndicator(Indicator):
    """Generic validator for issued/modified dateTime fields (xs:dateTime)."""

    def __init__(
        self, field_uri: URIRef, indicator_id: str, name_de: str, name_en: str
    ):
        super().__init__(
            indicator_id=indicator_id,
            name_de=name_de,
            name_en=name_en,
            dimension=QualityDimension.FINDABILITY,
            description_de=f"Prüft ob {field_uri} als xs:dateTime vorliegt",
            description_en=f"Checks if {field_uri} is a xs:dateTime",
            weight=1.0,
        )
        self.field_uri = field_uri

    def validate(self, metadata: Any) -> IndicatorResult:
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

            values = list(metadata.objects(predicate=self.field_uri))

            if not values:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Feld nicht gesetzt",
                    message_en="Field not set",
                    details={"count": 0},
                )

            valid = []
            invalid = []
            for v in values:
                text = str(v)
                if is_valid_xs_datetime(text):
                    valid.append(text)
                else:
                    invalid.append(text)

            status = IndicatorStatus.PASS if not invalid else IndicatorStatus.PARTIAL
            score = 1.0 if not invalid else 0.5

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=(
                    "Alle Werte sind gültige xs:dateTime"
                    if not invalid
                    else "Einige Werte sind keine gültigen xs:dateTime"
                ),
                message_en=(
                    "All values are valid xs:dateTime"
                    if not invalid
                    else "Some values are not valid xs:dateTime"
                ),
                details={"valid": valid, "invalid": invalid, "total": len(values)},
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


class AccrualPeriodicityIndicator(Indicator):
    """Checks for dct:accrualPeriodicity presence and (optionally) controlled vocabulary."""

    def __init__(self):
        super().__init__(
            indicator_id="find_accrual_periodicity",
            name_de="Aktualisierungsfrequenz angegeben",
            name_en="Accrual periodicity specified",
            dimension=QualityDimension.FINDABILITY,
            description_de="Prüft ob dct:accrualPeriodicity gesetzt ist und ggf. aus kontrolliertem Vokabular stammt",
            description_en="Checks if dct:accrualPeriodicity is set and optionally from controlled vocabulary",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
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

            values = list(metadata.objects(predicate=DCTERMS.accrualPeriodicity))

            if not values:
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="dct:accrualPeriodicity nicht angegeben",
                    message_en="dct:accrualPeriodicity not specified",
                    details={"count": 0},
                )

            valid = [str(v) for v in values if str(v) in VALID_FREQUENCY_URIS]
            invalid = [str(v) for v in values if str(v) not in VALID_FREQUENCY_URIS]

            status = IndicatorStatus.PASS if not invalid else IndicatorStatus.PARTIAL
            score = 1.0 if not invalid else 0.5

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=(
                    "Alle Werte aus kontrolliertem Vokabular"
                    if not invalid
                    else "Nicht alle Werte aus kontrolliertem Vokabular"
                ),
                message_en=(
                    "All values from controlled vocabulary"
                    if not invalid
                    else "Not all values from controlled vocabulary"
                ),
                details={"valid": valid, "invalid": invalid, "total": len(values)},
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


# Register new indicators
_theme_presence = ThemePresenceIndicator()
_locn_geometry = LocnGeometryIndicator()
_admin_unit = AdminUnitL2Indicator()
_temporal = TemporalCoverageIndicator()
_issued = DateTimeFieldIndicator(
    DCTERMS.issued,
    "find_issued_datetime",
    "Issued Datum (xs:dateTime)",
    "Issued date (xs:dateTime)",
)
_modified = DateTimeFieldIndicator(
    DCTERMS.modified,
    "find_modified_datetime",
    "Modified Datum (xs:dateTime)",
    "Modified date (xs:dateTime)",
)
_accrual = AccrualPeriodicityIndicator()
