"""Findability indicators for DCAT-AP-DE metadata.

Validates aspects like keywords, theme, spatial/temporal coverage, etc.
"""

from typing import Optional
from rdflib import Graph, URIRef
from rdflib.namespace import DCTERMS

from core.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from core.dimension import QualityDimension
from extraction.dataset_context import DatasetContext
from utils.datetime_utils import validate_temporal_value


class KeywordsCountIndicator(Indicator):
    """Validates if dataset has appropriate number of keywords (3 ≤ k ≤ 15).

    Per Handreichung zur Metadatenqualität (oc.bydata 12/2025): min 3 keywords.
    PASS: 3-15, PARTIAL: 1-2 or 16-25, FAIL: 0 or >25.
    """

    MIN_KEYWORDS = 3
    MAX_KEYWORDS = 15
    OVER_MAX_PARTIAL = 25

    def __init__(self):
        super().__init__(
            indicator_id="find_keywords_count",
            name_de="Angemessene Anzahl Schlagwörter",
            name_en="Appropriate number of keywords",
            dimension=QualityDimension.FINDABILITY,
            description_de="Mindestens 3 Schlagwörter (Handreichung); optimal 3–15, PARTIAL bei 1–2 oder 16–25",
            description_en="At least 3 keywords (Handreichung); optimal 3–15, PARTIAL for 1–2 or 16–25",
            weight=1.0,
        )

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)
            keywords = context.keywords
            keyword_count = len(keywords)

            if self.MIN_KEYWORDS <= keyword_count <= self.MAX_KEYWORDS:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = f"Optimale Anzahl Keywords: {keyword_count}"
                message_en = f"Optimal number of keywords: {keyword_count}"
            elif (
                0 < keyword_count < self.MIN_KEYWORDS
                or self.MAX_KEYWORDS < keyword_count <= self.OVER_MAX_PARTIAL
            ):
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = f"Suboptimale Anzahl Keywords: {keyword_count}"
                message_en = f"Suboptimal number of keywords: {keyword_count}"
            else:
                status = IndicatorStatus.FAIL
                score = 0.0
                message_de = f"Ungeeignete Anzahl Keywords: {keyword_count}"
                message_en = f"Inappropriate number of keywords: {keyword_count}"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} keywords={keyword_count}"
            )
            self.logger.debug(f"[{self.indicator_id}] values={keywords}")

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
                    "keywords": keywords,
                    "expected_range": f"{self.MIN_KEYWORDS}–{self.MAX_KEYWORDS} keywords (PASS), 1–{self.MIN_KEYWORDS-1} or {self.MAX_KEYWORDS+1}–{self.OVER_MAX_PARTIAL} (PARTIAL)",
                },
            )

        except Exception as e:
            self.logger.exception(
                f"[{self.indicator_id}] Validation failed with exception"
            )
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

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)
            themes = context.themes
            in_vocab = context.themes_in_vocab
            self.logger.debug(f"[{self.indicator_id}] Found themes: {themes}")

            if not themes:
                self.logger.info(f"[{self.indicator_id}] FAIL score=0.00 no themes")
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

            valid_themes = [t for t, ok in zip(themes, in_vocab) if ok]
            invalid_themes = [t for t, ok in zip(themes, in_vocab) if not ok]

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

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"valid={len(valid_themes)}/{len(themes)}"
            )
            if invalid_themes:
                self.logger.debug(
                    f"[{self.indicator_id}] invalid_themes={invalid_themes}"
                )

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
            self.logger.exception(
                f"[{self.indicator_id}] Validation failed with exception"
            )
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

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)
            geometries = context.geometries

            if not geometries:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no locn:geometry"
                )
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

            self.logger.info(
                f"[{self.indicator_id}] PASS score=1.00 geometries={len(geometries)}"
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
                details={"geometries": geometries},
            )

        except Exception as e:
            self.logger.exception(f"[{self.indicator_id}] Indicator validation failed")
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


class PoliticalGeocodingIndicator(Indicator):
    """Checks political/administrative coverage against the DCAT-AP-DE geocoding
    vocabulary.

    DCAT-AP.de's normative field is ``dcatde:politicalGeocodingURI``
    (Konvention 08, MUSS where a geographic reference applies); this indicator
    reads it **primarily** and only falls back to the generic
    ``locn:adminUnitL2`` when no dcatde field is present — so a dataset that
    correctly uses the dcatde field is no longer false-FAILed.
    """

    def __init__(self):
        super().__init__(
            indicator_id="find_political_geocoding",
            name_de="Politische Geokodierung aus kontrolliertem Vokabular",
            name_en="Political geocoding from controlled vocabulary",
            dimension=QualityDimension.FINDABILITY,
            description_de=(
                "Prüft primär ob dcatde:politicalGeocodingURI auf das dcat-ap.de "
                "Geocoding-Vokabular verweist; ersatzweise locn:adminUnitL2"
            ),
            description_en=(
                "Checks primarily that dcatde:politicalGeocodingURI references the "
                "dcat-ap.de geocoding vocabulary; falls back to locn:adminUnitL2"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            if not (context.political_geocoding or context.admin_units):
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 "
                    "no politicalGeocodingURI / adminUnitL2"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine politische Geokodierung angegeben",
                    message_en="No political geocoding specified",
                    details={"geocoding_count": 0},
                )

            if context.political_geocoding:
                # Primary, normative field (Konvention 08).
                units = context.political_geocoding
                first = units[0]
                source = "dcatde:politicalGeocodingURI"
                is_valid = first.is_in_vocab
                status = IndicatorStatus.PASS if is_valid else IndicatorStatus.PARTIAL
                score = 1.0 if is_valid else 0.5
            else:
                # Only the generic locn:adminUnitL2 present — secondary fallback
                # signal, capped at PARTIAL: full credit requires the DCAT-AP.de
                # field.
                units = context.admin_units
                first = units[0]
                source = "locn:adminUnitL2 (fallback)"
                is_valid = first.is_in_vocab
                status = IndicatorStatus.PARTIAL
                score = 0.5

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"source={source} uri={first.uri} segment={first.segment}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=(
                    f"Geokodierung ({source}) verweist auf dcat-ap.de"
                    if is_valid
                    else f"Geokodierung ({source}) ist nicht aus dcat-ap.de"
                ),
                message_en=(
                    f"Geocoding ({source}) references dcat-ap.de"
                    if is_valid
                    else f"Geocoding ({source}) is not from dcat-ap.de"
                ),
                details={
                    "source": source,
                    "uri": first.uri,
                    "segment": first.segment,
                    "is_valid": is_valid,
                    "geocoding_count": len(units),
                },
            )

        except Exception as e:
            self.logger.exception(f"[{self.indicator_id}] Indicator validation failed")
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


class GeocodingLevelIndicator(Indicator):
    """Checks ``dcatde:politicalGeocodingLevelURI`` against the DCAT-AP.de
    geocoding-level vocabulary (Konvention 09, SOLL).

    * PASS    — level present and every value is in the vocabulary
    * PARTIAL — level present but at least one value is not in the vocabulary
    * FAIL    — no level set
    """

    def __init__(self):
        super().__init__(
            indicator_id="find_geocoding_level",
            name_de="Geokodierungs-Ebene aus kontrolliertem Vokabular",
            name_en="Geocoding level from controlled vocabulary",
            dimension=QualityDimension.FINDABILITY,
            description_de=(
                "Prüft ob dcatde:politicalGeocodingLevelURI aus dem dcat-ap.de "
                "Level-Vokabular stammt (Konvention 09)"
            ),
            description_en=(
                "Checks that dcatde:politicalGeocodingLevelURI is from the dcat-ap.de "
                "level vocabulary (Konvention 09)"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)
            levels = context.political_geocoding_level
            in_vocab = context.political_geocoding_level_in_vocab

            if not levels:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 "
                    "no politicalGeocodingLevelURI"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine politische Geokodierungs-Ebene angegeben",
                    message_en="No political geocoding level specified",
                    details={"level_count": 0},
                )

            valid = [u for u, ok in zip(levels, in_vocab) if ok]
            invalid = [u for u, ok in zip(levels, in_vocab) if not ok]

            if invalid:
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = "Nicht alle Ebenen aus dem kontrollierten Vokabular"
                message_en = "Not all levels are from the controlled vocabulary"
            else:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Ebene aus dem kontrollierten Vokabular"
                message_en = "Level from the controlled vocabulary"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"valid={len(valid)}/{len(levels)}"
            )
            if invalid:
                self.logger.debug(f"[{self.indicator_id}] invalid_levels={invalid}")

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
                    "valid": valid,
                    "invalid": invalid,
                    "total": len(levels),
                },
            )

        except Exception as e:
            self.logger.exception(f"[{self.indicator_id}] Indicator validation failed")
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
    """Checks for temporal coverage via dcat:startDate/endDate (xs:date or xs:dateTime)."""

    def __init__(self):
        super().__init__(
            indicator_id="find_temporal_coverage",
            name_de="Zeitliche Abdeckung angegeben",
            name_en="Temporal coverage specified",
            dimension=QualityDimension.FINDABILITY,
            description_de="Prüft ob dcat:startDate/endDate gesetzt und als xs:date oder xs:dateTime gültig sind",
            description_en="Checks if dcat:startDate/endDate are set and valid as xs:date or xs:dateTime",
            weight=1.0,
        )

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)
            start = context.start_dates
            end = context.end_dates

            self.logger.debug(
                f"[{self.indicator_id}] Found startDate: {start}, endDate: {end}"
            )

            start_format, start_valid = (
                validate_temporal_value(start[0]) if start else (None, False)
            )
            end_format, end_valid = (
                validate_temporal_value(end[0]) if end else (None, False)
            )

            if start_valid or end_valid:
                self.logger.info(
                    f"[{self.indicator_id}] PASS score=1.00 "
                    f"start={start_format}/{start_valid} end={end_format}/{end_valid}"
                )
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
                        "start_count": len(start),
                        "end_count": len(end),
                        "start_format": start_format,
                        "end_format": end_format,
                        "start_valid": start_valid,
                        "end_valid": end_valid,
                    },
                )

            self.logger.info(
                f"[{self.indicator_id}] FAIL score=0.00 no temporal coverage found or invalid date format"
            )
            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.FAIL,
                score=0.0,
                message_de="Keine zeitliche Abdeckung gefunden oder ungültiges Datumsformat",
                message_en="No temporal coverage found or invalid date format",
                details={
                    "start_count": len(start),
                    "end_count": len(end),
                    "start_format": start_format,
                    "end_format": end_format,
                    "start_valid": start_valid,
                    "end_valid": end_valid,
                },
            )

        except Exception as e:
            self.logger.exception(f"[{self.indicator_id}] Indicator validation failed")
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
    """Generic validator for issued/modified date fields (xs:date or xs:dateTime)."""

    def __init__(
        self, field_uri: URIRef, indicator_id: str, name_de: str, name_en: str
    ):
        super().__init__(
            indicator_id=indicator_id,
            name_de=name_de,
            name_en=name_en,
            dimension=QualityDimension.FINDABILITY,
            description_de=f"Prüft ob {field_uri} als xs:date oder xs:dateTime vorliegt",
            description_en=f"Checks if {field_uri} is a valid xs:date or xs:dateTime",
            weight=1.0,
        )
        self.field_uri = field_uri

    def _collect_sourced(self, context: DatasetContext):
        """Collect (source_kind, source_uri, value) tuples for this field
        across both the Dataset and all Distributions.

        ``dct:modified`` and ``dct:issued`` are valid on both subject types
        in DCAT-AP-DE — datasets typically have one each, distributions
        often have their own. The indicator checks all of them and shows
        which subject each value came from.
        """
        if self.field_uri == DCTERMS.modified:
            return context.collect_modified()
        if self.field_uri == DCTERMS.issued:
            return context.collect_issued()
        # Unknown field — fall back to a flat graph scan. Source is unknown
        # so we record it as ``"unknown"`` to keep the log shape consistent.
        from extraction.dataset_context import SourcedValue

        return [
            SourcedValue("unknown", None, str(o))
            for o in context.graph.objects(predicate=self.field_uri)
        ]

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)
            sourced = self._collect_sourced(context)

            if not sourced:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 field {self.field_uri} not set"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Feld nicht gesetzt",
                    message_en="Field not set",
                    details={"count": 0, "dataset_count": 0, "distribution_count": 0},
                )

            valid: list[dict] = []
            invalid: list[dict] = []
            for sv in sourced:
                fmt, ok = validate_temporal_value(sv.value)
                entry = {
                    "value": sv.value,
                    "format": fmt,
                    "source_kind": sv.source_kind,
                    "source_uri": sv.source_uri,
                }
                (valid if ok else invalid).append(entry)

            status = IndicatorStatus.PASS if not invalid else IndicatorStatus.PARTIAL
            score = 1.0 if not invalid else 0.5

            dataset_count = sum(1 for s in sourced if s.source_kind == "dataset")
            dist_count = sum(1 for s in sourced if s.source_kind == "distribution")

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"valid={len(valid)}/{len(sourced)} "
                f"dataset={dataset_count} distribution={dist_count} "
                f"field={self.field_uri}"
            )
            for sv in sourced:
                self.logger.debug(
                    f"[{self.indicator_id}]   [{sv.source_kind}] {sv.source_uri} = {sv.value}"
                )
            if invalid:
                self.logger.debug(f"[{self.indicator_id}] invalid_values={invalid}")

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=(
                    f"Alle {len(valid)} Werte gültig (Dataset: {dataset_count}, "
                    f"Distribution: {dist_count})"
                    if not invalid
                    else f"{len(invalid)} ungültige(r) Wert(e) "
                    f"(Dataset: {dataset_count}, Distribution: {dist_count})"
                ),
                message_en=(
                    f"All {len(valid)} values valid (Dataset: {dataset_count}, "
                    f"Distribution: {dist_count})"
                    if not invalid
                    else f"{len(invalid)} invalid value(s) "
                    f"(Dataset: {dataset_count}, Distribution: {dist_count})"
                ),
                details={
                    "valid": valid,
                    "invalid": invalid,
                    "total": len(sourced),
                    "dataset_count": dataset_count,
                    "distribution_count": dist_count,
                },
            )

        except Exception as e:
            self.logger.exception(f"[{self.indicator_id}] Indicator validation failed")
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

    def validate(
        self, metadata: Graph, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)
            values = context.accrual_periodicity
            in_vocab = context.accrual_periodicity_in_vocab

            if not values:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 dct:accrualPeriodicity not set"
                )
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

            valid = [v for v, ok in zip(values, in_vocab) if ok]
            invalid = [v for v, ok in zip(values, in_vocab) if not ok]

            status = IndicatorStatus.PASS if not invalid else IndicatorStatus.PARTIAL
            score = 1.0 if not invalid else 0.5

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"valid={len(valid)}/{len(values)}"
            )
            if invalid:
                self.logger.debug(f"[{self.indicator_id}] invalid_values={invalid}")

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
            self.logger.exception(f"[{self.indicator_id}] Indicator validation failed")
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


# Instantiate indicators
_keywords_indicator = KeywordsCountIndicator()
_theme_indicator = ThemeIndicator()
_locn_geometry = LocnGeometryIndicator()
_political_geocoding = PoliticalGeocodingIndicator()
_geocoding_level = GeocodingLevelIndicator()
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
