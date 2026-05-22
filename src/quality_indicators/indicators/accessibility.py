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
from quality_indicators.vocabularies import (
    VALID_FILE_TYPE_URIS,
    VALID_MEDIA_TYPE_URIS,
)


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
    """Validates dct:format presence and membership in the EU file-type vocabulary."""

    def __init__(self):
        super().__init__(
            indicator_id="acc_format",
            name_de="Format aus kontrolliertem Vokabular",
            name_en="Format from controlled vocabulary",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de="Prüft ob dct:format gesetzt und aus dem EU-File-Type-Vokabular ist",
            description_en="Checks if dct:format is set and from the EU file-type vocabulary",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate format specification against the EU file-type vocabulary."""
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

            valid = [str(f) for f in formats if str(f) in VALID_FILE_TYPE_URIS]
            invalid = [str(f) for f in formats if str(f) not in VALID_FILE_TYPE_URIS]

            if invalid:
                status = IndicatorStatus.PARTIAL if valid else IndicatorStatus.FAIL
                score = 0.5 if valid else 0.0
                message_de = "Nicht alle Formate aus dem kontrollierten Vokabular"
                message_en = "Not all formats are from the controlled vocabulary"
            else:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Alle Formate aus dem kontrollierten Vokabular"
                message_en = "All formats are from the controlled vocabulary"

            self.logger.info(
                f"[{self.indicator_id}] Result: {status.value} | Score: {score:.2f} | {message_de}"
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
                    "valid": valid,
                    "invalid": invalid,
                    "total": len(formats),
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


class MediaTypeIndicator(Indicator):
    """Validates dcat:mediaType against the IANA media-types vocabulary."""

    def __init__(self):
        super().__init__(
            indicator_id="acc_media_type",
            name_de="Media Type aus kontrolliertem Vokabular",
            name_en="Media type from controlled vocabulary",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de="Prüft ob dcat:mediaType aus dem IANA Media-Types-Vokabular ist",
            description_en="Checks if dcat:mediaType is from the IANA media-types vocabulary",
            weight=1.0,
        )

    def validate(self, metadata: Any) -> IndicatorResult:
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

            media_types = list(metadata.objects(predicate=DCAT.mediaType))
            self.logger.debug(
                f"[{self.indicator_id}] Found {len(media_types)} mediaType(s): {[str(m) for m in media_types]}"
            )

            if not media_types:
                self.logger.info(
                    f"[{self.indicator_id}] Result: FAIL | No mediaType specified"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein Media Type angegeben",
                    message_en="No media type specified",
                    details={"media_type_count": 0},
                )

            valid = [str(m) for m in media_types if str(m) in VALID_MEDIA_TYPE_URIS]
            invalid = [
                str(m) for m in media_types if str(m) not in VALID_MEDIA_TYPE_URIS
            ]

            if invalid:
                status = IndicatorStatus.PARTIAL if valid else IndicatorStatus.FAIL
                score = 0.5 if valid else 0.0
                message_de = "Nicht alle Media Types aus dem IANA-Vokabular"
                message_en = "Not all media types are from the IANA vocabulary"
            else:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Alle Media Types aus dem IANA-Vokabular"
                message_en = "All media types are from the IANA vocabulary"

            self.logger.info(
                f"[{self.indicator_id}] Result: {status.value} | Score: {score:.2f} | {message_de}"
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
                    "valid": valid,
                    "invalid": invalid,
                    "total": len(media_types),
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
_media_type_indicator = MediaTypeIndicator()
