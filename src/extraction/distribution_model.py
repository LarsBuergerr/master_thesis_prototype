"""Detect how a publisher modelled a dataset's distributions.

The DCAT standard treats distributions as different *representations* of the
same dataset (CSV ↔ JSON ↔ XLSX of identical content). Many publishers
violate this — splitting yearly data across distributions, mixing service
endpoints with data files, or pointing only at an HTML landing page.

This validator classifies each distribution into a structural role and then
asks of the data-file subset: do they look like format variants of the same
content (DCAT-conform), or like split data (would be better as a dataset
series)? Service endpoints and landing pages are reported but excluded from
the variant analysis — they're complementary access modes, not format
variants, and treating them as such would systematically misclassify geo
datasets.

Two cheap, deterministic signals in v1:

* **Signal A — format diversity**: ``(unique_formats - 1) / (n - 1)``
  over the data-file subset. 1.0 when every distribution has a different
  format (variants); 0.0 when they all share one (split / duplicates).
* **Signal B — filename stem identity**: do the data-file URLs share a
  common stem (``data.csv`` vs ``data.json``) or are they all distinct
  (``data-2022.csv`` vs ``data-2023.csv``)?

The composite is a weighted mean over the **available** signals — a signal
that can't be computed (e.g. no parseable filenames) drops out rather than
contributing zero, so datasets with sparse metadata aren't systematically
penalised.

Adding more signals (byteSize variance, modified-date proximity, title
patterns) is a matter of appending to the ``_signal_*`` helpers and
``DistributionModelReport.signals_total``.
"""

from __future__ import annotations

import logging
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from logging import Logger
from typing import Optional
from urllib.parse import urlparse

from extraction.dataset_context import (
    DatasetContext,
    DistributionContext,
)
from extraction.distribution_probes import (
    ARCHIVE_MIMETYPES,
    effective_mime,
)

# EU file-type URIs that denote OGC service endpoints rather than data
# files. Hardcoded explicitly (not derived from ``EU_FILE_TYPE_TO_MIME``)
# because services and plain XML both map to ``application/xml`` — deriving
# from the MIME would also catch ``dct:format = XML`` as a "service" and
# misclassify every XML-output distribution.
_EU_FILE_TYPE_PREFIX = "http://publications.europa.eu/resource/authority/file-type/"
_OGC_SERVICE_SUFFIXES: tuple[str, ...] = (
    "WFS_SRVC",
    "WMS_SRVC",
    "WCS_SRVC",
    "WMTS_SRVC",
    "SOS_SRVC",
    "OGC_WFS",
    "OGC_WMS",
    "OGC_WCS",
    "OGC_WMTS",
)
SERVICE_FILE_TYPE_URIS: frozenset[str] = frozenset(
    _EU_FILE_TYPE_PREFIX + suffix for suffix in _OGC_SERVICE_SUFFIXES
)

# URL-pattern fallbacks for OGC service endpoints — catches publishers who
# declared the wrong dct:format but whose URL still gives them away.
_SERVICE_URL_PATTERNS: tuple[re.Pattern, ...] = (
    re.compile(r"[?&]service=(?:wms|wfs|wcs|wmts|sos)\b", re.IGNORECASE),
    re.compile(r"[?&]request=getcapabilities\b", re.IGNORECASE),
    re.compile(r"/(?:wms|wfs|wcs|wmts|sos)(?:[/?]|$)", re.IGNORECASE),
)

# Score thresholds for the composite → classification mapping.
_VARIANTS_THRESHOLD = 0.75
_SPLIT_THRESHOLD = 0.30

_logger = logging.getLogger(__name__)


class DistributionRole(str, Enum):
    """Structural role a distribution plays for the dataset.

    Inheriting from ``str`` so the role serialises cleanly in JSON reports
    and ``.value`` round-trips with downstream consumers.
    """

    DATA_FILE = "data_file"
    SERVICE_ENDPOINT = "service_endpoint"
    LANDING_PAGE = "landing_page"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"


def classify_distribution_role(dist: DistributionContext) -> DistributionRole:
    """Assign a structural role to a single distribution.

    Precedence: declared service file-type > URL service pattern >
    MIME-based role (landing page → archive → data file). Falls back to
    ``UNKNOWN`` when nothing is recognisable.
    """
    if any(fmt in SERVICE_FILE_TYPE_URIS for fmt in dist.formats):
        return DistributionRole.SERVICE_ENDPOINT

    url = dist.fetch_url or ""
    if url and any(p.search(url) for p in _SERVICE_URL_PATTERNS):
        return DistributionRole.SERVICE_ENDPOINT

    mime = effective_mime(dist)
    if mime in {"text/html", "application/xhtml+xml"}:
        return DistributionRole.LANDING_PAGE
    if mime in ARCHIVE_MIMETYPES:
        return DistributionRole.ARCHIVE
    if mime is not None and mime != "application/octet-stream":
        # Recognised, non-generic MIME → treat as data. ``application/
        # octet-stream`` is the probe's "I have no idea" fallback and
        # would otherwise contaminate the data_file bucket.
        return DistributionRole.DATA_FILE

    return DistributionRole.UNKNOWN


@dataclass
class DistributionModelReport:
    """Per-dataset analysis output. Returned by ``analyze_distribution_model``."""

    roles: dict[str, DistributionRole] = field(default_factory=dict)
    data_file_count: int = 0
    service_endpoint_count: int = 0
    landing_page_count: int = 0
    archive_count: int = 0
    unknown_count: int = 0

    # Per-signal scores in [0, 1] — ``None`` when the signal could not be
    # computed
    format_diversity_score: Optional[float] = None
    filename_stem_score: Optional[float] = None

    # Per-signal evidence (for the agent / debug consumer).
    unique_formats: list[str] = field(default_factory=list)
    filename_stems: dict[str, Optional[str]] = field(default_factory=dict)

    composite_score: Optional[float] = None
    classification: str = "unknown"
    has_service_with_data: bool = False

    signals_evaluated: int = 0
    signals_total: int = 2


def analyze_distribution_model(
    context: DatasetContext,
    *,
    logger: Optional[Logger] = None,
) -> DistributionModelReport:
    """Classify distributions by role and score variants vs. split-data.

    The signal computation runs only over the ``DATA_FILE`` subset. Service
    endpoints, landing pages, and archives are counted (and exposed in the
    report) but don't contribute to the variant analysis.

    A multi-line debug log is emitted at the end showing per-distribution
    role assignments, signal scores, and the final classification — mirroring
    the format produced by ``distribution_probes`` so the two layers
    read consistently in a single log stream.
    """
    log = logger or _logger
    report = DistributionModelReport()
    data_files: list[DistributionContext] = []

    for dist in context.distributions:
        role = classify_distribution_role(dist)
        report.roles[dist.distribution_uri] = role
        if role == DistributionRole.DATA_FILE:
            report.data_file_count += 1
            data_files.append(dist)
        elif role == DistributionRole.SERVICE_ENDPOINT:
            report.service_endpoint_count += 1
        elif role == DistributionRole.LANDING_PAGE:
            report.landing_page_count += 1
        elif role == DistributionRole.ARCHIVE:
            report.archive_count += 1
        else:
            report.unknown_count += 1

    report.has_service_with_data = (
        report.service_endpoint_count > 0 and report.data_file_count > 0
    )

    n = report.data_file_count

    if n == 0:
        report.classification = (
            "service-only" if report.service_endpoint_count > 0 else "no-data"
        )
    elif n == 1:
        report.classification = "single"
    else:
        # Compute signals over the data-file subset.
        diversity = _signal_format_diversity(data_files)
        if diversity is not None:
            report.format_diversity_score = diversity[0]
            report.unique_formats = diversity[1]
            report.signals_evaluated += 1

        stem = _signal_filename_stem(data_files)
        if stem is not None:
            report.filename_stem_score = stem[0]
            report.filename_stems = stem[1]
            report.signals_evaluated += 1

        available = [
            s
            for s in (report.format_diversity_score, report.filename_stem_score)
            if s is not None
        ]
        if available:
            report.composite_score = sum(available) / len(available)
            if report.composite_score >= _VARIANTS_THRESHOLD:
                report.classification = "format-variants"
            elif report.composite_score <= _SPLIT_THRESHOLD:
                report.classification = "split-data"
            else:
                report.classification = "mixed-or-ambiguous"
        else:
            # n >= 2 but neither signal applied — both formats unknown AND
            # no parseable filenames.
            report.classification = "mixed-or-ambiguous"

    log.debug(_format_report(report, context))
    return report


def _signal_format_diversity(
    data_files: list[DistributionContext],
) -> Optional[tuple[float, list[str]]]:
    """Signal A — diversity of distinct MIME types across data distributions.

    Returns ``(score, unique_formats)`` or ``None`` when fewer than two of
    the data distributions have a known MIME (the signal isn't meaningful
    with one or zero data points).
    """
    mimes = [effective_mime(d) for d in data_files]
    known = [m for m in mimes if m]
    if len(known) < 2:
        return None
    unique = sorted(set(known))
    score = (len(unique) - 1) / (len(known) - 1)
    return score, unique


def _signal_filename_stem(
    data_files: list[DistributionContext],
) -> Optional[tuple[float, dict[str, Optional[str]]]]:
    """Signal B — do the data distributions share a filename stem?

    Returns ``(score, {uri: stem_or_None})``. Distributions whose URL has
    no parseable filename stem are recorded as ``None`` in the dict but
    excluded from the comparison. ``None`` is returned when fewer than two
    distributions have a parseable stem.
    """
    stems: dict[str, Optional[str]] = {
        d.distribution_uri: _extract_stem(d.fetch_url) for d in data_files
    }
    parsed = [s for s in stems.values() if s]
    if len(parsed) < 2:
        return None
    unique = set(parsed)
    score = 1.0 - (len(unique) - 1) / (len(parsed) - 1)
    return score, stems


def _extract_stem(url: Optional[str]) -> Optional[str]:
    """Pull the filename stem out of a URL, lowercased for comparison.

    Returns ``None`` when the URL has no basename, no extension, or is
    empty. Query parameters and fragments are ignored (we only look at the
    path).
    """
    if not url:
        return None
    path = urlparse(url).path
    basename = os.path.basename(path)
    if not basename or "." not in basename:
        return None
    stem, _ = os.path.splitext(basename)
    return stem.lower() or None


def _format_report(
    report: DistributionModelReport,
    context: DatasetContext,
) -> str:
    """Multi-line human-readable summary of an analysis result."""
    lines: list[str] = []
    lines.append(
        f"[distribution_model] {context.distribution_count} distribution(s) "
        f"→ {report.classification}"
    )
    lines.append("  roles       :")
    for dist in context.distributions:
        role = report.roles.get(dist.distribution_uri, DistributionRole.UNKNOWN)
        fmt_short = _short_format(dist.formats[0]) if dist.formats else "-"
        url_short = _short(dist.fetch_url, 70)
        lines.append(f"    {role.value:18s} fmt={fmt_short:12s} url={url_short}")
    lines.append(
        f"  role_counts : data={report.data_file_count} "
        f"service={report.service_endpoint_count} "
        f"landing={report.landing_page_count} "
        f"archive={report.archive_count} "
        f"unknown={report.unknown_count}"
    )
    if report.has_service_with_data:
        lines.append("  service-with-data flag: yes")
    lines.append("  signals     :")
    lines.append(f"    format_diversity   {_format_signal_a(report)}")
    lines.append(f"    filename_stem      {_format_signal_b(report)}")
    composite = (
        f"{report.composite_score:.3f}"
        if report.composite_score is not None
        else "- (n/a)"
    )
    lines.append(f"  composite   : {composite}")
    lines.append(
        f"  signals_evaluated: {report.signals_evaluated}/{report.signals_total}"
    )
    return "\n".join(lines)


def _format_signal_a(report: DistributionModelReport) -> str:
    if report.format_diversity_score is None:
        return "score=-     (n/a, <2 known formats)"
    return (
        f"score={report.format_diversity_score:.3f} "
        f"unique={[_short_format(m) for m in report.unique_formats]}"
    )


def _format_signal_b(report: DistributionModelReport) -> str:
    if report.filename_stem_score is None:
        return "score=-     (n/a, <2 parseable filenames)"
    stems = [s for s in report.filename_stems.values() if s]
    unparsed = sum(1 for s in report.filename_stems.values() if not s)
    suffix = f" (+{unparsed} unparsed)" if unparsed else ""
    return f"score={report.filename_stem_score:.3f} " f"stems={stems}{suffix}"


def _short(value: Optional[str], width: int = 70) -> str:
    if not value:
        return "-"
    if len(value) <= width:
        return value
    return value[: width - 1] + "…"


def _short_format(value: Optional[str]) -> str:
    """Shorten an EU file-type URI down to its identifier tail (e.g. CSV)."""
    if not value:
        return "-"
    if "/" in value:
        return value.rsplit("/", 1)[-1]
    return value
