"""Accessibility indicators for DCAT-AP-DE metadata.

Validates aspects like downloadURL, format, mediaType, etc.
"""

from concurrent.futures import ThreadPoolExecutor
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
from quality_indicators.validators.distribution_type_validation import (
    DistributionReport,
    DistributionTypeValidator,
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


class FormatCongruenceIndicator(Indicator):
    """Validates that each distribution's declared format / mediaType matches
    the actual download content.

    For each ``dcat:Distribution`` we collect up to five MIME-type signals
    (``dct:format``, ``dcat:mediaType``, URL extension, HTTP ``Content-Type``,
    magic-byte sniff) and coalesce them. When the signals conflict the
    distribution scores 0; full congruence scores 1.0; consistent but with
    warnings (e.g. an unknown MIME mapping or an HTTP error) scores 0.7.

    To keep the indicator bounded we sample at most ``MAX_DISTRIBUTIONS`` per
    dataset (dedup by URL, deterministic sort, cap). Each probe runs in its
    own thread.
    """

    MAX_DISTRIBUTIONS = 20
    PARALLEL_WORKERS = 4
    PASS_THRESHOLD = 0.9
    PARTIAL_THRESHOLD = 0.5
    HTTP_TIMEOUT = (5.0, 10.0)

    def __init__(self):
        super().__init__(
            indicator_id="acc_format_congruence",
            name_de="Format-Kongruenz der Distributionen",
            name_en="Format congruence of distributions",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de=(
                "Prüft pro Distribution, ob dct:format, dcat:mediaType, URL-Endung, "
                "HTTP Content-Type und Magic-Bytes übereinstimmen "
                f"(Stichprobe von max. {self.MAX_DISTRIBUTIONS} Distributionen)"
            ),
            description_en=(
                "Checks per distribution that dct:format, dcat:mediaType, URL extension, "
                "HTTP Content-Type and magic-byte sniffing agree "
                f"(sample of up to {self.MAX_DISTRIBUTIONS} distributions)"
            ),
            weight=1.0,
        )
        self._validator = DistributionTypeValidator(
            timeout=self.HTTP_TIMEOUT, logger=self.logger
        )

    def validate(self, metadata: Any) -> IndicatorResult:
        try:
            distributions = self._collect_distributions(metadata)
            total = len(distributions)

            if total == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distributions to check"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Distributionen vorhanden",
                    message_en="No distributions present",
                    details={"distribution_count": 0},
                )

            sampled = distributions[: self.MAX_DISTRIBUTIONS]
            self.logger.debug(
                f"[{self.indicator_id}] checking {len(sampled)}/{total} distribution(s)"
            )

            reports = self._probe_in_parallel(metadata, sampled)

            per_scores: list[float] = []
            inconsistent: list[dict[str, Any]] = []
            warning_only: list[dict[str, Any]] = []
            for report in reports:
                score = self._score_report(report)
                per_scores.append(score)
                summary = {
                    "uri": report.distribution_uri,
                    "download_url": report.download_url,
                    "coalesced": report.coalesced_mime,
                    "issues": report.issues,
                    "warnings": report.warnings,
                }
                if not report.is_consistent:
                    inconsistent.append(summary)
                elif report.warnings:
                    warning_only.append(summary)

            overall = sum(per_scores) / len(per_scores) if per_scores else 0.0

            if inconsistent:
                if overall >= self.PARTIAL_THRESHOLD:
                    status = IndicatorStatus.PARTIAL
                else:
                    status = IndicatorStatus.FAIL
            elif warning_only:
                status = (
                    IndicatorStatus.PASS
                    if overall >= self.PASS_THRESHOLD
                    else IndicatorStatus.PARTIAL
                )
            else:
                status = IndicatorStatus.PASS

            sampled_count = len(sampled)
            message_de = (
                f"{sampled_count - len(inconsistent)}/{sampled_count} "
                "Distributionen format-kongruent"
            )
            message_en = (
                f"{sampled_count - len(inconsistent)}/{sampled_count} "
                "distributions format-congruent"
            )
            if total > sampled_count:
                message_de += f" (Stichprobe aus {total})"
                message_en += f" (sample from {total})"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={overall:.2f} "
                f"sampled={sampled_count}/{total} "
                f"inconsistent={len(inconsistent)} warnings={len(warning_only)}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=round(overall, 4),
                message_de=message_de,
                message_en=message_en,
                details={
                    "total_distributions": total,
                    "sampled_distributions": sampled_count,
                    "consistent_count": sampled_count - len(inconsistent),
                    "inconsistent_count": len(inconsistent),
                    "warning_only_count": len(warning_only),
                    "inconsistent": inconsistent,
                    "warning_only": warning_only,
                    "max_distributions": self.MAX_DISTRIBUTIONS,
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

    def _collect_distributions(self, graph: Graph) -> list:
        """Return a deterministic, deduplicated list of distribution nodes.

        Dedup key prefers the downloadURL (since two distribution nodes with
        the same download URL produce identical probes); falls back to the
        distribution URI when no downloadURL is set.
        """
        seen_keys: set = set()
        ordered: list = []
        for distribution in self._validator._iter_distributions(graph):
            download_url = self._validator._first_uri(
                graph, distribution, DCAT.downloadURL
            )
            key = download_url or str(distribution)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            ordered.append((key, distribution))
        ordered.sort(key=lambda item: item[0])
        return [dist for _, dist in ordered]

    def _probe_in_parallel(
        self, graph: Graph, distributions: list
    ) -> list[DistributionReport]:
        if len(distributions) <= 1:
            return [
                self._validator.validate_distribution(graph, dist)
                for dist in distributions
            ]
        with ThreadPoolExecutor(max_workers=self.PARALLEL_WORKERS) as pool:
            return list(
                pool.map(
                    lambda dist: self._validator.validate_distribution(graph, dist),
                    distributions,
                )
            )

    def _score_report(self, report: DistributionReport) -> float:
        if not report.is_consistent:
            return 0.0
        if report.warnings:
            return 0.7
        return 1.0


# Auto-register indicators when imported
_download_url_indicator = DownloadURLIndicator()
_format_indicator = FormatIndicator()
_media_type_indicator = MediaTypeIndicator()
_format_congruence_indicator = FormatCongruenceIndicator()
