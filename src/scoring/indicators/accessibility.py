"""Accessibility indicators for DCAT-AP-DE metadata.

Validates aspects like downloadURL, format, mediaType, etc.
"""

from typing import Any, Optional

from core.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from core.dimension import QualityDimension
from extraction.dataset_context import (
    DatasetContext,
    DistributionContext,
    DistributionProbe,
)
from extraction.distribution_model import (
    DistributionModelReport,
    DistributionRole,
    analyze_distribution_model,
    classify_distribution_role,
)
from extraction.distribution_probes import (
    attach_probes,
    effective_mime,
    format_tier_for_dist,
    is_non_proprietary_for_dist,
)


class DownloadURLIndicator(Indicator):
    """Fraction of distributions that declare a ``dcat:downloadURL``.

    Per distribution: has a downloadURL → +1.0, else 0.0 (no malus). Score is
    the mean over all distributions — consistent with the other per-distribution
    indicators. PASS ≥ 0.9, PARTIAL ≥ 0.5, FAIL below.
    """

    GRADED = True

    PASS_THRESHOLD = 0.9
    PARTIAL_THRESHOLD = 0.5

    def __init__(self):
        super().__init__(
            indicator_id="acc_download_url",
            name_de="Download-URL je Distribution",
            name_en="Download URL per distribution",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de="Anteil der Distributionen mit dcat:downloadURL",
            description_en="Fraction of distributions declaring a dcat:downloadURL",
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if context is None:
                context = DatasetContext.from_graph(metadata)

            total = context.distribution_count
            if total == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distributions"
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
                    details={"total_distributions": 0},
                )

            with_download = context.distributions_with_download_url
            score = with_download / total

            if score >= self.PASS_THRESHOLD:
                status = IndicatorStatus.PASS
            elif score >= self.PARTIAL_THRESHOLD:
                status = IndicatorStatus.PARTIAL
            else:
                status = IndicatorStatus.FAIL

            message_de = f"{with_download}/{total} Distribution(en) mit Download-URL"
            message_en = f"{with_download}/{total} distribution(s) with a download URL"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"with_download={with_download}/{total}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=round(score, 4),
                message_de=message_de,
                message_en=message_en,
                details={
                    "total_distributions": total,
                    "distributions_with_download_url": with_download,
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
    """Fraction of distributions with a ``dct:format`` from the EU file-type vocab.

    Per distribution: has ≥1 format URI in the EU file-type vocabulary → +1.0,
    else 0.0 (no malus). Score is the mean over all distributions — consistent
    with the other per-distribution indicators. PASS ≥ 0.9, PARTIAL ≥ 0.5.
    """

    GRADED = True

    PASS_THRESHOLD = 0.9
    PARTIAL_THRESHOLD = 0.5

    def __init__(self):
        super().__init__(
            indicator_id="acc_format",
            name_de="Format aus kontrolliertem Vokabular (je Distribution)",
            name_en="Format from controlled vocabulary (per distribution)",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de="Anteil der Distributionen mit dct:format aus dem EU-File-Type-Vokabular",
            description_en="Fraction of distributions with a dct:format from the EU file-type vocabulary",
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if context is None:
                context = DatasetContext.from_graph(metadata)

            total = context.distribution_count
            if total == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distributions"
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
                    details={"total_distributions": 0},
                )

            per_distribution: list[dict[str, Any]] = []
            for dist in context.distributions:
                passes = any(dist.formats_in_vocab)
                per_distribution.append(
                    {
                        "uri": dist.distribution_uri,
                        "formats": list(dist.formats),
                        "passes": passes,
                    }
                )

            passing = sum(1 for d in per_distribution if d["passes"])
            score = passing / total

            if score >= self.PASS_THRESHOLD:
                status = IndicatorStatus.PASS
            elif score >= self.PARTIAL_THRESHOLD:
                status = IndicatorStatus.PARTIAL
            else:
                status = IndicatorStatus.FAIL

            message_de = (
                f"{passing}/{total} Distribution(en) mit Format aus dem Vokabular"
            )
            message_en = (
                f"{passing}/{total} distribution(s) with a format from the vocabulary"
            )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"passing={passing}/{total}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=round(score, 4),
                message_de=message_de,
                message_en=message_en,
                details={
                    "total_distributions": total,
                    "passing_count": passing,
                    "per_distribution": per_distribution,
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
    """Fraction of distributions with a valid ``dcat:mediaType`` (IANA URI + vocab).

    Per distribution: has ≥1 mediaType that is an IANA URI *and* in the IANA
    media-types vocabulary → +1.0, else 0.0 (no malus). Score is the mean over
    all distributions — consistent with the other per-distribution indicators.
    PASS ≥ 0.9, PARTIAL ≥ 0.5.
    """

    GRADED = True

    PASS_THRESHOLD = 0.9
    PARTIAL_THRESHOLD = 0.5

    def __init__(self):
        super().__init__(
            indicator_id="acc_media_type",
            name_de="Media Type aus kontrolliertem Vokabular (je Distribution)",
            name_en="Media type from controlled vocabulary (per distribution)",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de="Anteil der Distributionen mit dcat:mediaType als IANA-URI aus dem Vokabular",
            description_en="Fraction of distributions with a dcat:mediaType as an IANA URI from the vocabulary",
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            self.logger.debug(f"[{self.indicator_id}] Starting validation")
            if context is None:
                context = DatasetContext.from_graph(metadata)

            total = context.distribution_count
            if total == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distributions"
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
                    details={"total_distributions": 0},
                )

            # A distribution passes if any of its mediaTypes is an IANA URI AND
            # in the IANA media-type vocabulary (DistributionContext precomputes
            # ``media_types_in_vocab`` with exactly this two-step check).
            per_distribution: list[dict[str, Any]] = []
            for dist in context.distributions:
                passes = any(dist.media_types_in_vocab)
                per_distribution.append(
                    {
                        "uri": dist.distribution_uri,
                        "media_types": list(dist.media_types),
                        "passes": passes,
                    }
                )

            passing = sum(1 for d in per_distribution if d["passes"])
            score = passing / total

            if score >= self.PASS_THRESHOLD:
                status = IndicatorStatus.PASS
            elif score >= self.PARTIAL_THRESHOLD:
                status = IndicatorStatus.PARTIAL
            else:
                status = IndicatorStatus.FAIL

            message_de = (
                f"{passing}/{total} Distribution(en) mit gültigem Media Type"
            )
            message_en = (
                f"{passing}/{total} distribution(s) with a valid media type"
            )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"passing={passing}/{total}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=round(score, 4),
                message_de=message_de,
                message_en=message_en,
                details={
                    "total_distributions": total,
                    "passing_count": passing,
                    "per_distribution": per_distribution,
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
    """Score per-distribution format/MIME congruence from pre-attached probes.

    Reads ``DistributionContext.probe`` — populated by ``attach_probes`` —
    rather than running its own HTTP probing. When the orchestrator has not
    yet attached probes, this indicator attaches them itself so it remains
    usable standalone.

    Each probed distribution contributes one score:

    * 0.0 — declared and observed MIME types conflict
    * 0.7 — consistent but with warnings (unknown MIME mapping, HTTP error, …)
    * 1.0 — full congruence

    Distributions whose ``probe is None`` (skipped by the per-dataset cap,
    or no fetchable URL) are not counted.
    """

    GRADED = True  # per-distribution scores averaged into a continuous value

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
                "Prüft pro Distribution, ob dct:format, dcat:mediaType, URL-Endung "
                "und HTTP Content-Type übereinstimmen "
                f"(Stichprobe von max. {self.MAX_DISTRIBUTIONS} Distributionen)"
            ),
            description_en=(
                "Checks per distribution that dct:format, dcat:mediaType, URL extension "
                "and HTTP Content-Type agree "
                f"(sample of up to {self.MAX_DISTRIBUTIONS} distributions)"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            total = context.distribution_count
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

            # Standalone-friendly: if the orchestrator hasn't probed yet, do
            # it here. The shared-context path skips this entirely.
            if all(d.probe is None for d in context.distributions):
                attach_probes(
                    context,
                    max_probes=self.MAX_DISTRIBUTIONS,
                    parallel=self.PARALLEL_WORKERS,
                    logger=self.logger,
                )

            probed = [d for d in context.distributions if d.probe is not None]
            sampled_count = len(probed)
            self.logger.debug(
                f"[{self.indicator_id}] scoring {sampled_count}/{total} probed distribution(s)"
            )

            per_scores: list[float] = []
            inconsistent: list[dict[str, Any]] = []
            warning_only: list[dict[str, Any]] = []
            for dist in probed:
                probe = dist.probe
                per_scores.append(self._score_probe(probe))
                summary = {
                    "uri": dist.distribution_uri,
                    "download_url": dist.download_url,
                    "access_url": dist.access_url,
                    "coalesced": probe.coalesced_mime,
                    "download_status_code": probe.download_status_code,
                    "download_fetch_error": probe.download_fetch_error,
                    "access_status_code": probe.access_status_code,
                    "access_fetch_error": probe.access_fetch_error,
                    "issues": probe.issues,
                    "warnings": probe.warnings,
                }
                if not probe.is_consistent:
                    inconsistent.append(summary)
                elif probe.warnings:
                    warning_only.append(summary)

            overall = sum(per_scores) / len(per_scores) if per_scores else 0.0

            if inconsistent:
                status = (
                    IndicatorStatus.PARTIAL
                    if overall >= self.PARTIAL_THRESHOLD
                    else IndicatorStatus.FAIL
                )
            elif warning_only:
                status = (
                    IndicatorStatus.PASS
                    if overall >= self.PASS_THRESHOLD
                    else IndicatorStatus.PARTIAL
                )
            else:
                status = IndicatorStatus.PASS

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

    @staticmethod
    def _score_probe(probe: DistributionProbe) -> float:
        if not probe.is_consistent:
            return 0.0
        if probe.warnings:
            return 0.7
        return 1.0


class ResponseCodeIndicator(Indicator):
    """Generic per-URL HTTP response-code validator.

    Reads ``probe.download_status_code`` / ``probe.access_status_code``
    (populated by ``attach_probes``) and scores per probed distribution:
    a reachable URL (``HTTP < 400``) contributes ``+1.0``, a dead one
    (``>= 400`` or fetch error) contributes ``DEAD_URL_MALUS`` (a negative
    penalty). The indicator score is the mean over all probed distributions,
    so a dead link actively drags the score down proportionally instead of
    just scoring low. Falls back to attaching probes itself when run
    standalone, mirroring ``FormatCongruenceIndicator``.

    Instantiated once per URL kind (``download`` and ``access``); the
    ``url_kind`` argument selects which probe field to evaluate.
    Distributions that don't declare the relevant URL are excluded — they
    contribute nothing to the score either way.

    Note: the malus lives here (pre-``/dist_count``) rather than in the
    ``ScorePolicy`` because the policy only sees the aggregated result — a
    proportional per-distribution penalty must be applied before averaging.
    """

    GRADED = True  # per-distribution +1 / malus, averaged — continuous

    PASS_THRESHOLD = 0.9
    PARTIAL_THRESHOLD = 0.5
    #: Penalty per dead URL (HTTP >= 400 or unreachable), applied per
    #: distribution before averaging. Reachable URLs score +1.0.
    DEAD_URL_MALUS = -0.5

    def __init__(self, url_kind: str, indicator_id: str, name_de: str, name_en: str):
        url_label_de = "Download-URL" if url_kind == "download" else "Access-URL"
        url_label_en = "download URL" if url_kind == "download" else "access URL"
        super().__init__(
            indicator_id=indicator_id,
            name_de=name_de,
            name_en=name_en,
            dimension=QualityDimension.ACCESSIBILITY,
            description_de=(
                f"Prüft, ob die {url_label_de} jeder Distribution einen "
                "gültigen HTTP-Statuscode (< 400) zurückgibt"
            ),
            description_en=(
                f"Checks that each distribution's {url_label_en} returns "
                "a valid HTTP status code (< 400)"
            ),
            weight=1.0,
        )
        self.url_kind = url_kind

    def _url_of(self, dist) -> Optional[str]:
        return dist.download_url if self.url_kind == "download" else dist.access_url

    def _status_of(self, probe: DistributionProbe) -> Optional[int]:
        return (
            probe.download_status_code
            if self.url_kind == "download"
            else probe.access_status_code
        )

    def _error_of(self, probe: DistributionProbe) -> Optional[str]:
        return (
            probe.download_fetch_error
            if self.url_kind == "download"
            else probe.access_fetch_error
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            total = context.distribution_count
            relevant = [d for d in context.distributions if self._url_of(d)]

            if not relevant:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 "
                    f"no distribution declares a {self.url_kind} URL"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Distribution mit entsprechender URL",
                    message_en="No distribution declares the relevant URL",
                    details={
                        "total_distributions": total,
                        "relevant_distributions": 0,
                    },
                )

            # Standalone-friendly: probe if nothing has been attached yet.
            if all(d.probe is None for d in relevant):
                attach_probes(
                    context,
                    max_probes=FormatCongruenceIndicator.MAX_DISTRIBUTIONS,
                    parallel=FormatCongruenceIndicator.PARALLEL_WORKERS,
                    logger=self.logger,
                )

            probed = [d for d in relevant if d.probe is not None]
            sampled_count = len(probed)

            if not probed:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no probes attempted"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Probe durchgeführt",
                    message_en="No probe attempted",
                    details={
                        "total_distributions": total,
                        "relevant_distributions": len(relevant),
                        "sampled_distributions": 0,
                    },
                )

            valid: list[dict[str, Any]] = []
            invalid: list[dict[str, Any]] = []
            for dist in probed:
                status_code = self._status_of(dist.probe)
                error = self._error_of(dist.probe)
                entry = {
                    "uri": dist.distribution_uri,
                    "url": self._url_of(dist),
                    "status_code": status_code,
                    "fetch_error": error,
                }
                if status_code is not None and status_code < 400:
                    valid.append(entry)
                else:
                    invalid.append(entry)

            # Reachable URLs score +1.0, dead ones the (negative) malus, then
            # average — so dead links pull the score below 0 proportionally.
            overall = (
                len(valid) * 1.0 + len(invalid) * self.DEAD_URL_MALUS
            ) / sampled_count

            if overall >= self.PASS_THRESHOLD:
                status = IndicatorStatus.PASS
            elif overall >= self.PARTIAL_THRESHOLD:
                status = IndicatorStatus.PARTIAL
            else:
                status = IndicatorStatus.FAIL

            url_label_de = (
                "Download-URL" if self.url_kind == "download" else "Access-URL"
            )
            url_label_en = (
                "download URL" if self.url_kind == "download" else "access URL"
            )
            message_de = (
                f"{len(valid)}/{sampled_count} {url_label_de}(s) "
                "mit gültigem HTTP-Statuscode"
            )
            message_en = (
                f"{len(valid)}/{sampled_count} {url_label_en}(s) "
                "with valid HTTP status code"
            )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={overall:.2f} "
                f"valid={len(valid)}/{sampled_count} "
                f"relevant={len(relevant)}/{total}"
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
                    "relevant_distributions": len(relevant),
                    "sampled_distributions": sampled_count,
                    "valid_count": len(valid),
                    "invalid_count": len(invalid),
                    "dead_url_malus": self.DEAD_URL_MALUS,
                    "valid": valid,
                    "invalid": invalid,
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


class MachineReadableAccessIndicator(Indicator):
    """Score machine-readable access across ALL distributions (mean tier).

    Each distribution receives a flat 3-level tier from its role and
    effective MIME type, then the indicator score is the mean over all
    distributions — every distribution counts, not just the best one.

    Tiers (anchored on the data.europa.eu format-rating table 1–3, with a malus
    for non-machine-readable distributions so they drag the mean down — like the
    other per-distribution indicators):

    * +1.0 (high) — machine-readable AND open: XML/JSON/CSV/ODS/XLSX, RDF,
      Parquet, GeoJSON/GML/KML/KMZ/GPKG/NetCDF/GPX/TopoJSON,
      OGC service endpoints (WFS/WMS/WCS/…)
    * +0.5 (mid)  — partially ok: XLS, SHP/Esri family, archives (ZIP/TAR/…)
    * −0.5 (none) — HTML, PDF, images, TIFF/GeoTIFF, unknown MIME (malus)

    Score = mean(tier_i for all distributions).
    PASS ≥ 0.8, PARTIAL ≥ 0.4, FAIL below.
    """

    GRADED = True

    TIER_HIGH = 1.0
    TIER_MID = 0.5
    TIER_NONE = -0.5  # malus: a non-machine-readable distribution pulls the mean down

    PASS_THRESHOLD = 0.8
    PARTIAL_THRESHOLD = 0.4

    def __init__(self):
        super().__init__(
            indicator_id="acc_machine_readable_access",
            name_de="Maschinenlesbarer Zugang (alle Distributionen)",
            name_en="Machine-readable access (all distributions)",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de=(
                "Bewertet jede Distribution anhand ihres Formats (hoch/mittel/keine "
                "Maschinenlesbarkeit) und bildet den Mittelwert über alle Distributionen"
            ),
            description_en=(
                "Rates each distribution by its format (high/mid/none machine-readability) "
                "and reports the mean across all distributions"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            total = context.distribution_count
            if total == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distributions"
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
                    details={"total_distributions": 0},
                )

            per_distribution: list[dict[str, Any]] = []
            for dist in context.distributions:
                tier_label = format_tier_for_dist(dist)
                tier = (
                    self.TIER_HIGH
                    if tier_label == "high"
                    else (self.TIER_MID if tier_label == "mid" else self.TIER_NONE)
                )
                per_distribution.append(
                    {
                        "uri": dist.distribution_uri,
                        "effective_mime": effective_mime(dist),
                        "tier": tier,
                        "tier_label": tier_label,
                    }
                )

            score = sum(d["tier"] for d in per_distribution) / total
            high = sum(1 for d in per_distribution if d["tier"] >= self.TIER_HIGH)
            mid = sum(1 for d in per_distribution if d["tier"] == self.TIER_MID)
            none_ = total - high - mid

            if score >= self.PASS_THRESHOLD:
                status = IndicatorStatus.PASS
            elif score >= self.PARTIAL_THRESHOLD:
                status = IndicatorStatus.PARTIAL
            else:
                status = IndicatorStatus.FAIL

            message_de = (
                f"{high}/{total} hoch maschinenlesbar, {mid}/{total} mittel, "
                f"{none_}/{total} keine (Score {score:.2f})"
            )
            message_en = (
                f"{high}/{total} high machine-readable, {mid}/{total} mid, "
                f"{none_}/{total} none (score {score:.2f})"
            )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"high={high} mid={mid} none={none_} total={total}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=round(score, 4),
                message_de=message_de,
                message_en=message_en,
                details={
                    "total_distributions": total,
                    "high_count": high,
                    "mid_count": mid,
                    "none_count": none_,
                    "per_distribution": per_distribution,
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


class DistributionModelIndicator(Indicator):
    """Detect whether the dataset's distributions follow DCAT's
    "same content, different formats" pattern.

    Classifies each distribution into a structural role (data file, service
    endpoint, landing page, archive, unknown) and then asks of the
    data-file subset whether they look like format variants of the same
    content or like split data spread across distributions.

    The composite is a mean over two cheap, independent signals:

    * Format diversity across the data-file subset
    * Filename-stem identity across the data-file subset URLs

    Service endpoints and landing pages are counted but **excluded** from
    the variant analysis — they're complementary access modes, not format
    variants, so a WMS + GeoJSON dataset isn't falsely penalised.

    Score mapping:

    * 1.0 — ``format-variants``, ``single``, or ``service-only``
    * 0.6 — ``mixed-or-ambiguous``
    * 0.4 — ``split-data`` (anti-pattern; should be a dataset series)
    * 0.0 — ``no-data`` (no recognisable data distributions)
    """

    GRADED = True  # multi-tier (1.0/0.6/0.4/0.0)

    SCORES: dict[str, float] = {
        "format-variants": 1.0,
        "single": 1.0,
        "service-only": 1.0,
        "mixed-or-ambiguous": 0.6,
        "split-data": 0.4,
        "no-data": 0.0,
    }

    def __init__(self):
        super().__init__(
            indicator_id="acc_distribution_model",
            name_de="Distributionsmodell",
            name_en="Distribution model coherence",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de=(
                "Prüft ob die Distributionen das gleiche Dataset in "
                "verschiedenen Formaten abbilden (DCAT-konform) oder eher "
                "eine Aufteilung der Daten darstellen. Service-Endpunkte "
                "(WMS/WFS) und Landing-Pages werden separat ausgewiesen "
                "und nicht in die Varianten-Analyse einbezogen."
            ),
            description_en=(
                "Detects whether the distributions follow DCAT's "
                "same-dataset-different-formats pattern, or whether the "
                "publisher split the data across distributions. Service "
                "endpoints (WMS/WFS) and landing pages are reported but "
                "excluded from the variant analysis."
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            if context.distribution_count == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distributions"
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

            report = analyze_distribution_model(context)
            score = self.SCORES.get(report.classification, 0.0)
            status = self._status_for_score(score)
            message_de, message_en = self._messages_for(report)

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"class={report.classification} "
                f"data={report.data_file_count} "
                f"service={report.service_endpoint_count} "
                f"landing={report.landing_page_count} "
                f"archive={report.archive_count} "
                f"unknown={report.unknown_count} "
                f"signals={report.signals_evaluated}/{report.signals_total}"
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
                details=self._details_for(report),
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

    @staticmethod
    def _status_for_score(score: float) -> IndicatorStatus:
        if score >= 0.9:
            return IndicatorStatus.PASS
        if score >= 0.5:
            return IndicatorStatus.PARTIAL
        return IndicatorStatus.FAIL

    @staticmethod
    def _messages_for(report: DistributionModelReport) -> tuple[str, str]:
        suffix_de = (
            " (zusätzlich Service-Endpunkt vorhanden)"
            if report.has_service_with_data
            else ""
        )
        suffix_en = (
            " (additional service endpoint present)"
            if report.has_service_with_data
            else ""
        )
        match report.classification:
            case "format-variants":
                return (
                    f"Distributionen wirken wie Format-Varianten desselben Datensatzes{suffix_de}",
                    f"Distributions look like format variants of the same dataset{suffix_en}",
                )
            case "split-data":
                return (
                    "Distributionen scheinen eine Aufteilung der Daten zu sein (eher dataset-series)",
                    "Distributions look like split data (would be better as a dataset series)",
                )
            case "mixed-or-ambiguous":
                return (
                    f"Distributionsmodell uneindeutig{suffix_de}",
                    f"Distribution model is ambiguous{suffix_en}",
                )
            case "single":
                return (
                    "Nur eine Distribution — keine Modellierungsfrage",
                    "Only one distribution — no modelling question to answer",
                )
            case "service-only":
                return (
                    "Nur Service-Endpunkte (z.B. WMS/WFS), keine direkten Datendateien",
                    "Service endpoints only (e.g. WMS/WFS), no direct data files",
                )
            case "no-data":
                return (
                    "Keine erkennbaren Datendateien",
                    "No recognisable data distributions",
                )
            case _:
                return ("Unbekannte Klassifikation", "Unknown classification")

    @staticmethod
    def _details_for(report: DistributionModelReport) -> dict[str, Any]:
        return {
            "classification": report.classification,
            "composite_score": report.composite_score,
            "has_service_with_data": report.has_service_with_data,
            "role_counts": {
                "data_file": report.data_file_count,
                "service_endpoint": report.service_endpoint_count,
                "landing_page": report.landing_page_count,
                "archive": report.archive_count,
                "unknown": report.unknown_count,
            },
            "roles": {uri: role.value for uri, role in report.roles.items()},
            "signals": {
                "format_diversity": {
                    "score": report.format_diversity_score,
                    "unique_formats": report.unique_formats,
                },
                "filename_stem": {
                    "score": report.filename_stem_score,
                    "stems": report.filename_stems,
                },
            },
            "signals_evaluated": report.signals_evaluated,
            "signals_total": report.signals_total,
        }


class FormatNonProprietaryIndicator(Indicator):
    """Checks what fraction of distributions declare a non-proprietary format.

    Uses the same non-proprietary EU file-type URI set as the MQA baseline
    (``format_non_proprietary`` metric). Score = distributions with ≥ 1
    non-proprietary format URI / total distributions.

    PASS ≥ 0.9, PARTIAL ≥ 0.5, FAIL < 0.5.
    """

    GRADED = True

    PASS_THRESHOLD = 0.9
    PARTIAL_THRESHOLD = 0.5

    def __init__(self):
        super().__init__(
            indicator_id="acc_format_non_proprietary",
            name_de="Nicht-proprietäres Format (alle Distributionen)",
            name_en="Non-proprietary format (all distributions)",
            dimension=QualityDimension.ACCESSIBILITY,
            description_de=(
                "Prüft, welcher Anteil der Distributionen ein nicht-proprietäres "
                "Format-URI aus dem EU-File-Type-Vokabular deklariert"
            ),
            description_en=(
                "Checks what fraction of distributions declare a non-proprietary "
                "format URI from the EU file-type vocabulary"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            total = context.distribution_count
            if total == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distributions"
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
                    details={"total_distributions": 0},
                )

            per_distribution: list[dict[str, Any]] = []
            for dist in context.distributions:
                passes = is_non_proprietary_for_dist(dist)
                per_distribution.append(
                    {
                        "uri": dist.distribution_uri,
                        "formats": dist.formats,
                        "passes": passes,
                    }
                )

            passing = sum(1 for d in per_distribution if d["passes"])
            score = passing / total

            if score >= self.PASS_THRESHOLD:
                status = IndicatorStatus.PASS
            elif score >= self.PARTIAL_THRESHOLD:
                status = IndicatorStatus.PARTIAL
            else:
                status = IndicatorStatus.FAIL

            message_de = (
                f"{passing}/{total} Distribution(en) mit nicht-proprietärem Format"
            )
            message_en = (
                f"{passing}/{total} distribution(s) with non-proprietary format"
            )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"passing={passing}/{total}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=round(score, 4),
                message_de=message_de,
                message_en=message_en,
                details={
                    "total_distributions": total,
                    "passing_count": passing,
                    "per_distribution": per_distribution,
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
_format_congruence_indicator = FormatCongruenceIndicator()
_download_url_response = ResponseCodeIndicator(
    "download",
    "acc_download_url_response",
    "Download-URL Antwortcode",
    "Download URL response code",
)
_access_url_response = ResponseCodeIndicator(
    "access",
    "acc_access_url_response",
    "Access-URL Antwortcode",
    "Access URL response code",
)
_machine_readable_access_indicator = MachineReadableAccessIndicator()
_format_non_proprietary_indicator = FormatNonProprietaryIndicator()
_distribution_model_indicator = DistributionModelIndicator()
