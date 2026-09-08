# encoding: utf-8
"""Probe a DCAT-AP-DE distribution and check that its declared format /
mediaType is consistent with the actual file behind its ``dcat:downloadURL``.

This is an adaptation of CKAN's ``ckanext-resource-validation``
(``resource_type_validation.py``) for **RDF-based** input.
Source: https://github.com/qld-gov-au/ckanext-resource-type-validation/tree/main
Declared signals are read from the pre-computed :class:`DistributionContext`;
probe signals are obtained by HTTPing the distribution URL. The validator
coalesces up to five MIME-type signals:

1. ``dct:format`` — EU file-type vocabulary URI, normalised to a MIME type
2. ``dcat:mediaType`` — IANA media-type URI (or literal) → MIME type
3. URL filename extension → MIME via ``mimetypes``
4. HTTP ``Content-Type`` response header
5. ``Content-Disposition`` attachment filename → MIME via ``mimetypes``

The coalescing / override / equality logic is ported from the CKAN module.
Output is attached to the context as :class:`DistributionProbe` — this tool
is for *auditing* DCAT records, not for blocking uploads.
"""

from __future__ import annotations

import argparse
import json
import logging
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass
from logging import Logger
import mimetypes
import os
import re
import sys
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urlparse

import requests
from rdflib import Graph

from extraction.dataset_context import (
    DatasetContext,
    DistributionContext,
    DistributionProbe,
    TypeSignal,
)

EQUAL_TYPES: list[list[str]] = [
    ["text/xml", "application/xml"],
    ["application/x-zip-compressed", "application/zip"],
    ["application/csv", "text/csv"],
    ["text/json", "application/json"],
    ["application/x-pdf", "application/pdf"],
    ["application/vnd.ms-excel", "application/excel", "text/xlsx"],
    [
        "application/geopackage+sqlite3",
        "application/x-gpkg",
        "application/x-sqlite3",
        "application/vnd.sqlite3",
    ],
    ["text/rtf", "text/richtext", "application/rtf", "application/x-rtf"],
    ["application/x-cdf", "application/x-netcdf"],
    [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ],
    [
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
    [
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.ms-powerpoint",
    ],
    [
        "application/msaccess",
        "application/x-msaccess",
        "application/vnd.msaccess",
        "application/vnd.ms-access",
        "application/mdb",
        "application/x-mdb",
    ],
    ["application/CDFV2", "application/CDFV2-unknown"],
]

ALLOWED_OVERRIDES: dict[str, list[str]] = {
    "text/plain": [
        "text/csv",
        "text/tab-separated-values",
        "text/turtle",
        "application/json",
        "application/xml",
        "application/rdf+xml",
        "application/geo+json",
        "application/gml+xml",
        "application/sparql-query",
        "application/x-ascii-grid",
        "application/csv",
        "application/vnd.google-earth.kml+xml",
        "model/mtl",
        "text/*",
    ],
    "application/octet-stream": ["*"],
    "application/xml": [
        "application/rdf+xml",
        "application/gml+xml",
        "application/vnd.google-earth.kml+xml",
        "application/xhtml+xml",
    ],
    "application/json": [
        "application/geo+json",
        "application/ld+json",
        "application/hal+json",
        "application/vnd.api+json",
        "application/topojson",
    ],
    "application/x-ole-storage": [
        "application/msword",
        "application/vnd.ms-powerpoint",
        "application/vnd.ms-excel",
    ],
    "text/csv": ["application/csv"],
    "text/x-fortran": ["text/csv"],
    "application/zip": [
        "application/vnd.google-earth.kmz",
        "application/x-filegdb",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ],
    "application/CDFV2": [
        "application/vnd.ms-excel",
        "application/msword",
        "application/vnd.ms-powerpoint",
    ],
}

ARCHIVE_MIMETYPES: list[str] = [
    "application/zip",
    "application/gzip",
    "application/x-7z-compressed",
    "application/x-tar",
]

# Per CKAN's resource_types.json this list is intentionally narrow — a
# declared generic MIME may be refined to a more specific one without
# triggering a conflict.
GENERIC_MIMETYPES: list[str] = ["application/octet-stream", "text/plain"]

# OGC / service types whose URLs return XML (GetCapabilities etc.). Treating
# them as application/xml lets the declared format agree with the actual
# response without special-casing.
SERVICE_XML_MIMETYPE = "application/xml"

EU_FILE_TYPE_TO_MIME: dict[str, str] = {
    "http://publications.europa.eu/resource/authority/file-type/CSV": "text/csv",
    "http://publications.europa.eu/resource/authority/file-type/JSON": "application/json",
    "http://publications.europa.eu/resource/authority/file-type/XML": "application/xml",
    "http://publications.europa.eu/resource/authority/file-type/RDF_XML": "application/rdf+xml",
    "http://publications.europa.eu/resource/authority/file-type/RDF": "application/rdf+xml",
    "http://publications.europa.eu/resource/authority/file-type/TTL": "text/turtle",
    "http://publications.europa.eu/resource/authority/file-type/PDF": "application/pdf",
    "http://publications.europa.eu/resource/authority/file-type/XLSX": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "http://publications.europa.eu/resource/authority/file-type/XLS": "application/vnd.ms-excel",
    "http://publications.europa.eu/resource/authority/file-type/HTML": "text/html",
    "http://publications.europa.eu/resource/authority/file-type/ZIP": "application/zip",
    "http://publications.europa.eu/resource/authority/file-type/GEOJSON": "application/geo+json",
    "http://publications.europa.eu/resource/authority/file-type/GML": "application/gml+xml",
    "http://publications.europa.eu/resource/authority/file-type/KML": "application/vnd.google-earth.kml+xml",
    "http://publications.europa.eu/resource/authority/file-type/KMZ": "application/vnd.google-earth.kmz",
    "http://publications.europa.eu/resource/authority/file-type/GEOTIFF": "image/tiff",
    "http://publications.europa.eu/resource/authority/file-type/TIFF": "image/tiff",
    "http://publications.europa.eu/resource/authority/file-type/PNG": "image/png",
    "http://publications.europa.eu/resource/authority/file-type/JPEG": "image/jpeg",
    "http://publications.europa.eu/resource/authority/file-type/TXT": "text/plain",
    "http://publications.europa.eu/resource/authority/file-type/GPKG": "application/x-gpkg",
    "http://publications.europa.eu/resource/authority/file-type/DXF": "image/vnd.dxf",
    "http://publications.europa.eu/resource/authority/file-type/SHP": "application/x-esri-shape",
    "http://publications.europa.eu/resource/authority/file-type/ATOM": "application/atom+xml",
    "http://publications.europa.eu/resource/authority/file-type/GPX": "application/gpx+xml",
    "http://publications.europa.eu/resource/authority/file-type/N3": "text/n3",
    "http://publications.europa.eu/resource/authority/file-type/NETCDF": "application/x-netcdf",
    "http://publications.europa.eu/resource/authority/file-type/SPARQLQ": "application/sparql-query",
    "http://publications.europa.eu/resource/authority/file-type/SHP": "x-gis/x-shapefile",
    "http://publications.europa.eu/resource/authority/file-type/WFS_SRVC": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/WMS_SRVC": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/WCS_SRVC": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/WMTS_SRVC": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/SOS_SRVC": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/OGC_WFS": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/OGC_WMS": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/OGC_WCS": SERVICE_XML_MIMETYPE,
    "http://publications.europa.eu/resource/authority/file-type/OGC_WMTS": SERVICE_XML_MIMETYPE,
}

IANA_MEDIA_PREFIX = "https://www.iana.org/assignments/media-types/"

# ---------------------------------------------------------------------------
# Format-quality classification sets
# ---------------------------------------------------------------------------

_FT = "http://publications.europa.eu/resource/authority/file-type/"

#: EU file-type URIs for OGC / INSPIRE service endpoints.
_SERVICE_FORMAT_URIS: frozenset[str] = frozenset(
    _FT + code
    for code in (
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
)

#: Non-proprietary EU file-type URIs — open standard or de-facto open format.
NON_PROPRIETARY_FORMAT_URIS: frozenset[str] = frozenset(
    _FT + code
    for code in (
        "BMP",
        "CSV",
        "DBF",
        "GEOJSON",
        "GML",
        "GPKG",
        "GPX",
        "GZIP",
        "HTML",
        "ICS",
        "JSON",
        "KML",
        "KMZ",
        "NETCDF",
        "N3",
        "ODS",
        "PNG",
        "RDF_N_QUADS",
        "RDF_N_TRIPLES",
        "RDF_TRIG",
        "RDF_TURTLE",
        "RDF_XML",
        "RSS",
        "RTF",
        "SPARQLQ",
        "TAR",
        "TIFF",
        "TSV",
        "TXT",
        "XML",
        "ZIP",
        "WFS_SRVC",
        "WMS_SRVC",
        "WCS_SRVC",
        "WMTS_SRVC",
        "SOS_SRVC",
        "OGC_WFS",
        "OGC_WMS",
        "OGC_WCS",
        "OGC_WMTS",
        "ATOM",
    )
)

#: Machine-readable AND open (tier high = 1.0).
#: Fully machine-readable (tier high = 1.0). Base formats mirror the "Machine
#: readable = Yes" row of the data.europa.eu Data Quality Guidelines (Table 5:
#: RDF, XML, JSON, CSV) plus their structured-data variants; the geo formats are
#: an addition for geospecific data types not covered by that table.
_HIGH_MIMES: frozenset[str] = frozenset(
    {
        "application/xml",
        "text/xml",
        "application/json",
        "application/ld+json",
        "application/hal+json",
        "application/vnd.api+json",
        "text/csv",
        "application/csv",
        "text/tab-separated-values",
        "application/rdf+xml",
        "text/turtle",
        "text/n3",
        "application/sparql-query",
        "application/vnd.apache.parquet",
        # Geo open standards (addition, not in Table 5)
        "application/geo+json",
        "application/gml+xml",
        "application/vnd.google-earth.kml+xml",
        "application/vnd.google-earth.kmz",
        "application/x-gpkg",
        "application/geopackage+sqlite3",
        "application/x-netcdf",
        "application/x-cdf",
        "application/gpx+xml",
        "application/atom+xml",
        "application/topojson",
    }
)

#: Predominantly machine-readable (tier mid = 0.5). Base formats mirror the
#: "Machine readable = Predominantly" row of the Data Quality Guidelines (Table 5:
#: ODS, XLSX, XLS, TXT, HTML); the geo formats are an addition for geospecific
#: data types not covered by that table.
_MID_MIMES: frozenset[str] = frozenset(
    {
        "application/vnd.oasis.opendocument.spreadsheet",  # ODS
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # XLSX
        "application/vnd.ms-excel",
        "application/excel",  # XLS
        "text/plain",  # TXT
        "text/html",
        "application/xhtml+xml",  # HTML
        # Geo formats (addition, not in Table 5)
        "x-gis/x-shapefile",
        "application/x-esri-shape",
        "application/x-filegdb",
    }
)

#: Not usefully machine-readable (tier none = 0.0). Mirrors the "Machine
#: readable = No" row of the Data Quality Guidelines (Table 5: PDF, DOCX, ODT,
#: DOC, PNG, GIF, JPG/JPEG, TIFF). Not consulted by the classifier (anything not
#: in high/mid falls through to "none") — kept for documentation.
_LOW_MIMES: frozenset[str] = frozenset(
    {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # DOCX
        "application/vnd.oasis.opendocument.text",  # ODT
        "application/msword",  # DOC
        "image/png",
        "image/gif",
        "image/jpeg",
        "image/tiff",
    }
)


def _classify_machine_readable_tier(mime: Optional[str], formats: list[str]) -> str:
    """Return 'high' / 'mid' / 'none' for a distribution's format quality."""
    if any(f in _SERVICE_FORMAT_URIS for f in formats):
        return "high"
    if mime in ARCHIVE_MIMETYPES:
        return "mid"
    if mime in _HIGH_MIMES:
        return "high"
    if mime in _MID_MIMES:
        return "mid"
    return "none"


def format_tier_for_dist(dist: "DistributionContext") -> str:
    """Machine-readable tier for a distribution — probe-first, declared fallback.

    Returns ``'high'`` / ``'mid'`` / ``'none'``.  Uses ``dist.probe`` when
    available (populated by :func:`attach_probes`), otherwise classifies from
    declared signals via :func:`declared_mime`.
    """
    if dist.probe is not None:
        return dist.probe.machine_readable_tier
    return _classify_machine_readable_tier(declared_mime(dist), dist.formats)


def is_non_proprietary_for_dist(dist: "DistributionContext") -> bool:
    """Return True when the distribution declares a non-proprietary format URI.

    Uses ``dist.probe`` when available; falls back to ``dist.formats``.
    """
    if dist.probe is not None:
        return dist.probe.is_non_proprietary
    return any(f in NON_PROPRIETARY_FORMAT_URIS for f in dist.formats)


# Make sure mimetypes knows about the formats we care about even on minimal systems.
for ext, mime in {
    ".geojson": "application/geo+json",
    ".gpkg": "application/x-gpkg",
    ".gml": "application/gml+xml",
    ".kml": "application/vnd.google-earth.kml+xml",
    ".kmz": "application/vnd.google-earth.kmz",
    ".ttl": "text/turtle",
    ".rdf": "application/rdf+xml",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".parquet": "application/vnd.apache.parquet",
    ".accdb": "application/msaccess",
    ".asc": "application/x-ascii-grid",
    ".ecw": "application/octet-stream",
    ".esri": "x-gis/x-shapefile",
    ".fgdb": "application/x-filegdb",
    ".gdb": "application/x-filegdb",
    ".geotiff": "image/tiff",
    ".mtl": "model/mtl",
    ".n3": "text/n3",
    ".obj": "text/plain",
    ".pqt": "application/vnd.apache.parquet",
    ".shp": "x-gis/x-shapefile",
    ".sparql": "application/sparql-query",
    ".tab": "text/plain",
    ".topojson": "application/json",
    ".ttf": "text/plain",
    ".wfs": "application/xml",
    ".wmts": "application/xml",
}.items():
    mimetypes.add_type(mime, ext)


@dataclass
class _ProbeResult:
    """Everything to extract from one HTTP probe."""

    content_type: Optional[str]
    content_disposition: Optional[str]
    attachment_filename: Optional[str]
    final_url: Optional[str]
    status: Optional[int]
    error: Optional[str]


class DistributionTypeValidator:
    """Probe a single distribution and coalesce its MIME-type signals.

    Adapted from CKAN's ``ResourceTypeValidator`` for RDF-based DCAT input.
    Declared signals (``dct:format``, ``dcat:mediaType``, URL extension) are
    read directly from the :class:`DistributionContext`; probe signals are
    obtained by HTTPing :attr:`DistributionContext.fetch_url`.
    """

    def __init__(
        self,
        *,
        timeout: tuple[float, float] = (5.0, 8.0),
        equal_types: Optional[list[list[str]]] = None,
        allowed_overrides: Optional[dict[str, list[str]]] = None,
        archive_mimetypes: Optional[list[str]] = None,
        generic_mimetypes: Optional[list[str]] = None,
        fetch_enabled: bool = True,
        logger: Logger,
    ) -> None:
        self.timeout = timeout
        self.equal_types = equal_types if equal_types is not None else EQUAL_TYPES
        self.allowed_overrides = (
            allowed_overrides if allowed_overrides is not None else ALLOWED_OVERRIDES
        )
        self.archive_mimetypes = (
            archive_mimetypes if archive_mimetypes is not None else ARCHIVE_MIMETYPES
        )
        self.generic_mimetypes = (
            generic_mimetypes if generic_mimetypes is not None else GENERIC_MIMETYPES
        )
        self.fetch_enabled = fetch_enabled
        self.logger = logger

    def probe_distribution(self, dist: DistributionContext) -> DistributionProbe:
        """Build a :class:`DistributionProbe` for one distribution.

        Reads declared signals from ``dist`` (no graph traversal), HTTP-probes
        ``dist.fetch_url`` when enabled, and coalesces everything into a
        single MIME verdict.
        """
        probe = DistributionProbe()
        fetch_url = dist.fetch_url
        fetch_source = (
            "downloadURL"
            if dist.download_url
            else "accessURL" if dist.access_url else None
        )

        format_signal = self._signal_from_declared_format(dist)
        media_signal = self._signal_from_declared_media_type(dist)
        probe.signals.append(format_signal)
        probe.signals.append(media_signal)
        if format_signal.raw_value and not format_signal.mime_type:
            probe.warnings.append(
                f"dct:format={format_signal.raw_value!r} has no known MIME mapping; not comparable"
            )
        if media_signal.raw_value and not media_signal.mime_type:
            probe.warnings.append(
                f"dcat:mediaType={media_signal.raw_value!r} is not a recognised IANA media type"
            )

        probe.signals.append(self._signal_from_url(fetch_url))

        download_result: Optional[_ProbeResult] = None
        access_result: Optional[_ProbeResult] = None
        if self.fetch_enabled:
            if dist.download_url:
                download_result = self._probe(dist.download_url)
                probe.download_status_code = download_result.status
                probe.download_fetch_error = download_result.error
            if dist.access_url:
                if dist.access_url == dist.download_url and download_result is not None:
                    access_result = download_result
                else:
                    access_result = self._probe(dist.access_url)
                probe.access_status_code = access_result.status
                probe.access_fetch_error = access_result.error

        primary_result = download_result if dist.download_url else access_result

        if self.fetch_enabled and fetch_url and primary_result is not None:
            result = primary_result
            probe.status_code = result.status
            probe.fetch_error = result.error
            probe.fetched = result.status is not None and result.error is None
            probe.final_url = result.final_url
            probe.content_disposition = result.content_disposition
            probe.attachment_filename = result.attachment_filename
            probe.signals.append(
                TypeSignal(
                    "http_content_type",
                    result.content_type,
                    _strip_charset(result.content_type),
                )
            )
            probe.signals.append(
                self._signal_from_attachment(
                    result.attachment_filename, result.content_disposition
                )
            )
            if result.status is not None and result.status >= 400:
                probe.warnings.append(
                    f"{fetch_source} returned HTTP {result.status}; "
                    "remaining checks rely on declared metadata only"
                )
            elif result.error or not probe.fetched:
                probe.warnings.append(
                    f"{fetch_source} could not be fetched "
                    f"({result.error or 'no response'}); "
                    "content-based checks skipped"
                )
        else:
            if not fetch_url:
                probe.warnings.append(
                    "no dcat:downloadURL or dcat:accessURL — content-based checks skipped"
                )
            probe.signals.append(TypeSignal("http_content_type", None, None))
            probe.signals.append(TypeSignal("attachment_filename", None, None))

        probe.coalesced_mime, probe.issues = self._coalesce(probe.signals)
        probe.machine_readable_tier = _classify_machine_readable_tier(
            probe.coalesced_mime, dist.formats
        )
        probe.is_non_proprietary = any(
            f in NON_PROPRIETARY_FORMAT_URIS for f in dist.formats
        )

        attachment_mime = _signal_value(probe.signals, "attachment_filename")
        if (
            probe.coalesced_mime
            and attachment_mime
            and self._type_equals(attachment_mime, probe.coalesced_mime)
        ):
            for body_source, label in (("http_content_type", "HTTP Content-Type"),):
                body_mime = _signal_value(probe.signals, body_source)
                if body_mime and not self._type_equals(body_mime, probe.coalesced_mime):
                    probe.warnings.append(
                        f"{label} {body_mime!r} disagrees with attachment "
                        f"filename ({probe.attachment_filename!r} → "
                        f"{attachment_mime!r}); treating as advisory"
                    )

        self.logger.debug(_format_probe(dist, probe))
        return probe

    def _signal_from_declared_format(self, dist: DistributionContext) -> TypeSignal:
        if not dist.formats:
            return TypeSignal("dct:format", None, None)
        raw = dist.formats[0]
        mime = EU_FILE_TYPE_TO_MIME.get(raw)
        if mime is None and not raw.startswith("http"):
            mime = mimetypes.guess_type(f"example.{raw.lower()}")[0]
        return TypeSignal("dct:format", raw, mime)

    def _signal_from_declared_media_type(self, dist: DistributionContext) -> TypeSignal:
        if not dist.media_types:
            return TypeSignal("dcat:mediaType", None, None)
        raw = dist.media_types[0]
        return TypeSignal("dcat:mediaType", raw, _normalize_media_type(raw))

    def _signal_from_url(self, url: Optional[str]) -> TypeSignal:
        if not url:
            return TypeSignal("url_extension", None, None)
        path = urlparse(url).path
        guess, _ = mimetypes.guess_type(path, strict=False)
        return TypeSignal("url_extension", os.path.basename(path) or None, guess)

    def _signal_from_attachment(
        self,
        attachment_filename: Optional[str],
        content_disposition: Optional[str],
    ) -> TypeSignal:
        """Signal from an ``attachment`` filename.

        Reflects what the server claims it is *actually* delivering — the
        body of an HTTP response that says ``Content-Disposition: attachment;
        filename=foo.csv`` IS the CSV file, even if the ``Content-Type`` header
        is misconfigured (e.g. ``text/html`` from a download portal wrapper).
        """
        if not attachment_filename:
            return TypeSignal("attachment_filename", None, None)
        guess, _ = mimetypes.guess_type(attachment_filename, strict=False)
        raw = attachment_filename
        if not content_disposition:
            raw = f"{attachment_filename} (from final URL)"
        return TypeSignal("attachment_filename", raw, guess)

    def _probe(self, url: str) -> "_ProbeResult":
        content_type: Optional[str] = None
        content_disposition: Optional[str] = None
        final_url: Optional[str] = None
        status: Optional[int] = None
        error: Optional[str] = None

        try:
            head = requests.head(url, allow_redirects=True, timeout=self.timeout)
            status = head.status_code
            content_type = head.headers.get("Content-Type")
            content_disposition = head.headers.get("Content-Disposition")
            final_url = head.url
        except requests.RequestException as exc:
            error = f"HEAD failed: {exc.__class__.__name__}"

        try:
            with requests.get(
                url, stream=True, allow_redirects=True, timeout=self.timeout
            ) as resp:
                status = resp.status_code
                final_url = resp.url
                if resp.headers.get("Content-Type"):
                    content_type = resp.headers.get("Content-Type")
                if resp.headers.get("Content-Disposition"):
                    content_disposition = resp.headers.get("Content-Disposition")
        except requests.RequestException as exc:
            error = (error + " | " if error else "") + f"GET failed: {exc}"

        attachment_filename = _filename_from_content_disposition(content_disposition)
        # Fallback: derive a filename from the final URL's path when the
        # server didn't set Content-Disposition. Catches CDN-style downloads
        # that redirect to ``…/file.csv`` with a generic Content-Type.
        if not attachment_filename and final_url:
            path = urlparse(final_url).path
            basename = os.path.basename(path)
            if basename and "." in basename:
                attachment_filename = basename
        return _ProbeResult(
            content_type=content_type,
            content_disposition=content_disposition,
            attachment_filename=attachment_filename,
            final_url=final_url,
            status=status,
            error=error,
        )

    _SIGNAL_PRIORITY = (
        "dct:format",
        "dcat:mediaType",
        "attachment_filename",
        "url_extension",
        "http_content_type",
    )

    def _coalesce(self, signals: list[TypeSignal]) -> tuple[Optional[str], list[str]]:
        """Pick the most specific MIME consistent with every signal.

        Returns ``(best_mime, issues)``. ``issues`` is empty when all non-None
        signals agree under the equality / override rules.
        """
        mime_types = [s.mime_type for s in signals if s.mime_type]
        if not mime_types:
            return None, []

        # In CKAN, ``allow_override`` is gated on whether the *upload*
        # signals are generic. We replicate that here from the dct:format /
        # dcat:mediaType / url_extension signals.
        declared_mimes = [
            s.mime_type
            for s in signals
            if s.source in {"dct:format", "dcat:mediaType", "url_extension"}
            and s.mime_type
        ]
        any_declared_generic = any(m in self.generic_mimetypes for m in declared_mimes)
        allow_override = (
            any_declared_generic
            or any(m in self.archive_mimetypes for m in declared_mimes)
            or not declared_mimes
        )

        # Pre-compute attachment evidence — used to demote a misleading
        # ``http_content_type`` when ``Content-Disposition`` told us the
        # filename and ``mimetypes`` knows its MIME.
        attachment_mime = next(
            (s.mime_type for s in signals if s.source == "attachment_filename"),
            None,
        )

        best: Optional[str] = None
        issues: list[str] = []
        priority = self._SIGNAL_PRIORITY
        ordered_signals = sorted(
            (s for s in signals if s.mime_type),
            key=lambda s: (priority.index(s.source) if s.source in priority else 99),
        )
        for sig in ordered_signals:
            mime = sig.mime_type
            if best is None:
                best = mime
                continue
            if self._type_equals(mime, best):
                continue
            valid, more_specific = self._is_valid_override(best, mime)
            if valid:
                # downward: new signal is a less specific superset of
                # ``best`` (e.g. best=application/gml+xml, new=application/xml).
                # Always compatible — keep ``best``.
                # upward: new signal would promote ``best`` to something
                # more specific. Only do this when ``allow_override`` says
                # the declared metadata was generic / unspecified to begin with.
                if more_specific == best:
                    continue
                if allow_override:
                    best = more_specific
                    continue
            # Demotion: the body-based ``http_content_type`` signal describes
            # the HTTP response body. When the attachment evidence
            # (Content-Disposition / final-URL filename) agrees with ``best``,
            # the body is misleading — typically an HTTP error page (404/5xx),
            # a download-portal HTML wrapper, or a server with a wrong default
            # Content-Type. Demote it so the conflict doesn't poison the
            # score; the caller surfaces the demotion as a warning so the
            # disagreement remains visible.
            if (
                sig.source == "http_content_type"
                and attachment_mime is not None
                and self._type_equals(attachment_mime, best)
            ):
                continue
            issues.append(
                f"{sig.source}={mime!r} conflicts with previously coalesced {best!r}"
            )

        return best or "application/octet-stream", issues

    def _type_equals(self, t1: Optional[str], t2: Optional[str]) -> bool:
        if t1 == t2:
            return True
        for group in self.equal_types:
            if t1 in group and t2 in group:
                return True
        return False

    def _is_valid_override(
        self, mime1: Optional[str], mime2: Optional[str]
    ) -> tuple[bool, Optional[str]]:
        if self._type_equals(mime1, mime2):
            return True, mime1

        def matches(mime: Optional[str], overrides: list[str]) -> bool:
            for override in overrides:
                if override == "*" or self._type_equals(override, mime):
                    return True
                if mime and "/" in override:
                    o_main, o_sub = override.split("/", 1)
                    if o_sub == "*" and mime.split("/", 1)[0] == o_main:
                        return True
            return False

        for generic, overrides in self.allowed_overrides.items():
            if self._type_equals(generic, mime1) and matches(mime2, overrides):
                return True, mime2
            if self._type_equals(generic, mime2) and matches(mime1, overrides):
                return True, mime1
        return False, None


def attach_probes(
    context: DatasetContext,
    *,
    validator: Optional[DistributionTypeValidator] = None,
    max_probes: Optional[int] = None,
    parallel: int = 4,
    dedup_by_url: bool = True,
    logger: Optional[Logger] = None,
) -> None:
    """Populate ``context.distributions[i].probe`` in parallel.

    Selection rules:

    * Distributions are sorted deterministically by fetch URL (falling back
      to distribution URI). This gives stable sampling when ``max_probes``
      is set.
    * With ``dedup_by_url=True`` (default), distributions that share a
      fetch URL produce a single probe; the same :class:`DistributionProbe`
      object is attached to all of them.
    * ``max_probes`` caps how many *unique probes* are run. Distributions
      beyond the cap (or with no fetch URL when probing requires one) keep
      ``probe = None`` — the indicator can tell apart "not attempted" from
      "attempted, failed".
    """
    log = logger or logging.getLogger(__name__)
    if validator is None:
        validator = DistributionTypeValidator(logger=log)

    # Order distributions by a stable key so capping is deterministic.
    keyed = [
        ((dist.fetch_url or dist.distribution_uri), dist)
        for dist in context.distributions
    ]
    keyed.sort(key=lambda item: item[0])

    # Group by dedup key so shared-URL distributions get one probe.
    groups: dict[str, list[DistributionContext]] = {}
    group_order: list[str] = []
    for key, dist in keyed:
        bucket_key = key if dedup_by_url else dist.distribution_uri
        if bucket_key not in groups:
            groups[bucket_key] = []
            group_order.append(bucket_key)
        groups[bucket_key].append(dist)

    selected_keys = group_order if max_probes is None else group_order[:max_probes]
    log.debug(
        f"attach_probes: {len(selected_keys)}/{len(group_order)} unique fetch keys, "
        f"{sum(len(groups[k]) for k in selected_keys)} distribution(s) covered"
    )

    def _probe_first_of(key: str) -> tuple[str, DistributionProbe]:
        # Probe using the first distribution in the group — its declared
        # signals are representative (siblings sharing the same URL should
        # have the same declared signals, but if not, the first is fine).
        return key, validator.probe_distribution(groups[key][0])

    if len(selected_keys) <= 1:
        results = [_probe_first_of(k) for k in selected_keys]
    else:
        with ThreadPoolExecutor(max_workers=parallel) as pool:
            results = list(pool.map(_probe_first_of, selected_keys))

    for key, probe in results:
        for dist in groups[key]:
            dist.probe = probe


_CONTENT_DISPOSITION_FILENAME_RE = re.compile(
    r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?',
    flags=re.IGNORECASE,
)


def _filename_from_content_disposition(value: Optional[str]) -> Optional[str]:
    """Extract the ``filename=`` (or ``filename*=``) parameter from a
    ``Content-Disposition`` header value.
    """
    if not value:
        return None
    match = _CONTENT_DISPOSITION_FILENAME_RE.search(value)
    if not match:
        return None
    return match.group(1).strip() or None


def _normalize_media_type(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    raw = raw.strip()
    if raw.startswith(IANA_MEDIA_PREFIX):
        return raw[len(IANA_MEDIA_PREFIX) :]
    if "/" in raw and not raw.startswith("http"):
        return raw
    return None


def _strip_charset(content_type: Optional[str]) -> Optional[str]:
    if not content_type:
        return None
    return content_type.split(";", 1)[0].strip().lower() or None


def _signal_value(signals: list[TypeSignal], source: str) -> Optional[str]:
    for sig in signals:
        if sig.source == source:
            return sig.mime_type
    return None


def declared_mime(dist: DistributionContext) -> Optional[str]:
    """MIME derivable from declared signals alone (no HTTP).

    Resolution order: ``dct:format`` via EU file-type vocab → ``dct:format``
    as a string suffix → ``dcat:mediaType`` (IANA URI or literal) → URL
    extension. Returns ``None`` when no signal yields a recognised MIME.
    """
    if dist.formats:
        raw = dist.formats[0]
        mime = EU_FILE_TYPE_TO_MIME.get(raw)
        if mime is not None:
            return mime
        if not raw.startswith("http"):
            guess = mimetypes.guess_type(f"example.{raw.lower()}")[0]
            if guess is not None:
                return guess
    if dist.media_types:
        normalised = _normalize_media_type(dist.media_types[0])
        if normalised is not None:
            return normalised
    if dist.fetch_url:
        guess, _ = mimetypes.guess_type(urlparse(dist.fetch_url).path, strict=False)
        if guess is not None:
            return guess
    return None


def effective_mime(dist: DistributionContext) -> Optional[str]:
    """Best-known MIME: ``probe.coalesced_mime`` if attached, declared otherwise.

    Use this whenever an indicator needs to know "what is this distribution".
    It transparently uses the verified probe result when available and falls
    back to declared signals when not — so indicators work both with and
    without ``attach_probes`` having been called.
    """
    if dist.probe and dist.probe.coalesced_mime:
        return dist.probe.coalesced_mime
    return declared_mime(dist)


def _format_probe(dist: DistributionContext, probe: DistributionProbe) -> str:
    lines: list[str] = []
    status = "OK   " if probe.is_consistent else "ERROR"
    title_part = f" — {dist.title}" if dist.title else ""
    lines.append(f"[{status}] {dist.distribution_uri}{title_part}")
    if dist.download_url:
        lines.append(f"  downloadURL : {dist.download_url}")
    if dist.access_url and dist.access_url != dist.download_url:
        lines.append(f"  accessURL   : {dist.access_url}")
    if probe.fetched:
        lines.append(f"  HTTP        : {probe.status_code}")
    elif probe.fetch_error:
        lines.append(f"  HTTP error  : {probe.fetch_error}")
    if probe.final_url and probe.final_url != (dist.download_url or dist.access_url):
        lines.append(f"  final URL   : {probe.final_url}")
    if probe.attachment_filename:
        lines.append(f"  attachment  : {probe.attachment_filename}")
    lines.append("  signals     :")
    for sig in probe.signals:
        lines.append(
            f"    {sig.source:20s} raw={_short(sig.raw_value):40s} mime={sig.mime_type or '-'}"
        )
    lines.append(f"  coalesced   : {probe.coalesced_mime or '-'}")
    for warn in probe.warnings:
        lines.append(f"  warning     : {warn}")
    for issue in probe.issues:
        lines.append(f"  issue       : {issue}")
    return "\n".join(lines)


def _short(value: Optional[str], width: int = 40) -> str:
    if value is None:
        return "-"
    if len(value) <= width:
        return value
    return value[: width - 1] + "…"
