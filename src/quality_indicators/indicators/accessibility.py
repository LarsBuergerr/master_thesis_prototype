"""Accessibility indicators for DCAT-AP-DE metadata.

Validates aspects like downloadURL, format, mediaType, etc.
"""

from typing import Any
from rdflib import Graph
from rdflib.namespace import DCAT, DCTERMS

from quality_indicators.models.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from quality_indicators.models.dimension import QualityDimension


class DownloadURLIndicator(Indicator):
    """Validates if dcat:downloadURL is set and not empty."""

    def __init__(self):
        super().__init__(
            indicator_id="acc_download_url",
            name_de="Download-URL angegeben",
            name_en="Download URL specified",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de="Prüft ob dcat:downloadURL gesetzt und nicht leer ist",
            description_en="Checks if dcat:downloadURL is set and not empty",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate download URL presence.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on URL presence
        """
        try:
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if not isinstance(metadata, Graph):
                self.logger.warning(
                    f"[{self.indicator_id}] Invalid metadata format: expected rdflib Graph"
                )
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

            download_urls = list(metadata.objects(predicate=DCAT.downloadURL))
            self.logger.debug(
                f"[{self.indicator_id}] Found {len(download_urls)} download URL(s): {[str(url) for url in download_urls]}"
            )

            if not download_urls:
                self.logger.info(
                    f"[{self.indicator_id}] Result: FAIL | No download URLs"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Download-URL angegeben",
                    message_en="No download URL specified",
                    details={"url_count": 0},
                )

            self.logger.debug(
                f"[{self.indicator_id}] Score calculation: PASS (download URLs found)"
            )
            self.logger.info(
                f"[{self.indicator_id}] Result: PASS | Score: 1.00 | {len(download_urls)} URL(s) found"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.PASS,
                score=1.0,
                message_de=f"Download-URL vorhanden: {len(download_urls)} URL(s)",
                message_en=f"Download URL present: {len(download_urls)} URL(s)",
                details={
                    "url_count": len(download_urls),
                    "urls": [str(url) for url in download_urls],
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


class FormatIndicator(Indicator):
    """Validates if dct:format is set and not empty."""

    MACHINE_READABLE_FORMATS = {
        "CSV",
        "JSON",
        "XML",
        "RDF",
        "TTL",
        "GEOJSON",
        "PARQUET",
    }

    def __init__(self):
        super().__init__(
            indicator_id="acc_format",
            name_de="Format angegeben",
            name_en="Format specified",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de="Prüft ob dct:format gesetzt ist",
            description_en="Checks if dct:format is set",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate format specification.

        Args:
            metadata: rdflib Graph with DCAT metadata

        Returns:
            IndicatorResult with score based on format specification
        """
        try:
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if not isinstance(metadata, Graph):
                self.logger.warning(
                    f"[{self.indicator_id}] Invalid metadata format: expected rdflib Graph"
                )
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

            formats = list(metadata.objects(predicate=DCTERMS.format))
            self.logger.debug(
                f"[{self.indicator_id}] Found {len(formats)} format(s): {[str(fmt) for fmt in formats]}"
            )

            if not formats:
                self.logger.info(
                    f"[{self.indicator_id}] Result: FAIL | No formats specified"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein Format angegeben",
                    message_en="No format specified",
                    details={"format_count": 0},
                )

            self.logger.debug(
                f"[{self.indicator_id}] Score calculation: PASS (formats found)"
            )
            self.logger.info(
                f"[{self.indicator_id}] Result: PASS | Score: 1.00 | {len(formats)} format(s) found"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.PASS,
                score=1.0,
                message_de=f"Format(e) angegeben: {len(formats)}",
                message_en=f"Format(s) specified: {len(formats)}",
                details={
                    "format_count": len(formats),
                    "formats": [str(fmt) for fmt in formats],
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


# Auto-register indicators when imported
_download_url_indicator = DownloadURLIndicator()
_format_indicator = FormatIndicator()
