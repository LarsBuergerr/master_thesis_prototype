# encoding: utf-8
"""Validate that a DCAT-AP-DE distribution's declared format / mediaType is
consistent with the actual file behind its ``dcat:downloadURL``.

This is an adaptation of CKAN's ``ckanext-resource-validation``
(``resource_type_validation.py``) for **RDF-based** input. Instead of an
uploaded ``FlaskFileStorage`` we work off an ``rdflib.Graph`` and fetch the
distribution URL over HTTP. We compare up to five MIME-type signals:

1. ``dct:format`` — EU file-type vocabulary URI, normalised to a MIME type
2. ``dcat:mediaType`` — IANA media-type URI (or literal) → MIME type
3. URL filename extension → MIME via ``mimetypes``
4. HTTP ``Content-Type`` response header
5. Magic-byte sniff of the first ~2 KB of the response body

The coalescing / override / equality logic is ported from the CKAN module.
Output is a structured report per distribution rather than a raised
``ValidationError`` — this tool is for *auditing* DCAT records, not for
blocking uploads.

Usage as a script::

    python -m quality_indicators.validators.distribution_type_validation \\
        data/perfect_example_01_updated.rdf
"""

from __future__ import annotations

import argparse
import json
import logging
from logging import Logger
import mimetypes
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional
from urllib.parse import urlparse

import requests
from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCAT, DCTERMS

# ---------------------------------------------------------------------------
# Configuration — inline replacement for CKAN's resources/resource_types.json
# ---------------------------------------------------------------------------

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

# generic types that can be "promoted" to a more specific type
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
    # ``application/json`` is the parent of the ``*+json`` family. Servers
    # often serve a more specific type as plain ``application/json``
    # (especially OGC WFS GetFeature with outputFormat=application/json
    # returns GeoJSON), and ``mimetypes`` resolves ``.json`` filenames the
    # same way.
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

# Types treated as "generic" — a declared generic MIME may be refined to a
# more specific one without triggering a conflict. Per CKAN's
# resource_types.json this is intentionally narrow.
GENERIC_MIMETYPES: list[str] = ["application/octet-stream", "text/plain"]

# OGC / service types whose URLs return XML (GetCapabilities etc.). Treating
# them as application/xml lets the declared format agree with the actual
# response without special-casing.
SERVICE_XML_MIMETYPE = "application/xml"

# EU file-type vocab URI → MIME (so dct:format can be compared with the rest).
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
    # OGC service formats — the endpoint typically returns XML
    # (e.g. ?REQUEST=GetCapabilities), so map them to application/xml.
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
    # additions from CKAN's resource_types.json
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

# Minimal magic-byte table, used when python-magic isn't installed.
_MAGIC_SIGNATURES: list[tuple[bytes, str]] = [
    (b"%PDF-", "application/pdf"),
    (b"PK\x03\x04", "application/zip"),  # also xlsx/docx
    (b"SQLite format 3\x00", "application/x-gpkg"),  # could also be plain SQLite
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"II*\x00", "image/tiff"),
    (b"MM\x00*", "image/tiff"),
    (b"<?xml", "application/xml"),
    (b"<!DOCTYPE html", "text/html"),
    (b"<html", "text/html"),
]

# Try python-magic if available, otherwise fall back to the table above.
try:
    import magic as _magic_lib  # type: ignore

    _MAGIC = _magic_lib.Magic(mime=True)

    def _sniff_mime(sample: bytes) -> Optional[str]:
        if not sample:
            return None
        return _MAGIC.from_buffer(sample) or None

except ImportError:  # pragma: no cover - optional dep
    _MAGIC = None

    def _sniff_mime(sample: bytes) -> Optional[str]:
        if not sample:
            return None
        head = sample[:32]
        stripped = head.lstrip()
        for prefix, mime in _MAGIC_SIGNATURES:
            if head.startswith(prefix) or stripped.startswith(prefix):
                return mime
        # crude text/csv hint: ascii + commas + newline
        try:
            text = sample[:512].decode("utf-8")
        except UnicodeDecodeError:
            return None
        if "," in text and "\n" in text and text.isprintable() is False:
            return None
        return None


DCATDE = Namespace("http://dcat-ap.de/def/dcatde/")

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class TypeSignal:
    """One source of MIME-type information for a distribution."""

    source: str
    raw_value: Optional[str]
    mime_type: Optional[str]


@dataclass
class _ProbeResult:
    """Everything we extract from one HTTP probe."""

    content_type: Optional[str]
    content_disposition: Optional[str]
    attachment_filename: Optional[str]
    final_url: Optional[str]
    sniffed: Optional[str]
    sample: bytes
    status: Optional[int]
    error: Optional[str]


@dataclass
class DistributionReport:
    distribution_uri: str
    title: Optional[str] = None
    download_url: Optional[str] = None
    access_url: Optional[str] = None
    fetched: bool = False
    status_code: Optional[int] = None
    fetch_error: Optional[str] = None
    final_url: Optional[str] = None
    content_disposition: Optional[str] = None
    attachment_filename: Optional[str] = None
    signals: list[TypeSignal] = field(default_factory=list)
    coalesced_mime: Optional[str] = None
    is_consistent: bool = True
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Validator
# ---------------------------------------------------------------------------


class DistributionTypeValidator:
    """Adapts ``ResourceTypeValidator`` to RDF-based DCAT distributions."""

    def __init__(
        self,
        *,
        timeout: tuple[float, float] = (5.0, 15.0),
        sample_bytes: int = 2048,
        equal_types: Optional[list[list[str]]] = None,
        allowed_overrides: Optional[dict[str, list[str]]] = None,
        archive_mimetypes: Optional[list[str]] = None,
        generic_mimetypes: Optional[list[str]] = None,
        fetch_enabled: bool = True,
        logger: Logger,
    ) -> None:
        self.timeout = timeout
        self.sample_bytes = sample_bytes
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

    # ---- public entry points --------------------------------------------------

    def validate_file(self, rdf_path: str | Path) -> list[DistributionReport]:
        """Parse the given RDF file and validate all of its distributions."""
        graph = Graph()
        graph.parse(str(rdf_path))
        return self.validate_graph(graph)

    def validate_graph(self, graph: Graph) -> list[DistributionReport]:
        reports: list[DistributionReport] = []
        for dist in self._iter_distributions(graph):
            reports.append(self.validate_distribution(graph, dist))
        return reports

    def validate_distribution(
        self, graph: Graph, distribution: URIRef
    ) -> DistributionReport:
        report = DistributionReport(distribution_uri=str(distribution))

        # ---- declared signals from the RDF
        report.title = self._first_literal(graph, distribution, DCTERMS.title)
        report.download_url = self._first_uri(graph, distribution, DCAT.downloadURL)
        report.access_url = self._first_uri(graph, distribution, DCAT.accessURL)

        # Prefer downloadURL for fetching; fall back to accessURL when the
        # distribution only declares an access endpoint (common for OGC
        # services, landing pages, ...).
        fetch_url = report.download_url or report.access_url
        fetch_source = "downloadURL" if report.download_url else "accessURL"

        format_signal = self._signal_from_format(graph, distribution)
        media_signal = self._signal_from_media_type(graph, distribution)
        report.signals.append(format_signal)
        report.signals.append(media_signal)
        if format_signal.raw_value and not format_signal.mime_type:
            report.warnings.append(
                f"dct:format={format_signal.raw_value!r} has no known MIME mapping; not comparable"
            )
        if media_signal.raw_value and not media_signal.mime_type:
            report.warnings.append(
                f"dcat:mediaType={media_signal.raw_value!r} is not a recognised IANA media type"
            )

        # ---- URL extension
        report.signals.append(self._signal_from_url(fetch_url))

        # ---- HTTP + sniff
        if self.fetch_enabled and fetch_url:
            probe = self._probe(fetch_url)
            report.status_code = probe.status
            report.fetch_error = probe.error
            report.fetched = probe.status is not None and probe.error is None
            report.final_url = probe.final_url
            report.content_disposition = probe.content_disposition
            report.attachment_filename = probe.attachment_filename
            report.signals.append(
                TypeSignal(
                    "http_content_type",
                    probe.content_type,
                    _strip_charset(probe.content_type),
                )
            )
            report.signals.append(
                self._signal_from_attachment(
                    probe.attachment_filename, probe.content_disposition
                )
            )
            report.signals.append(
                TypeSignal("sniff", _hex_preview(probe.sample), probe.sniffed)
            )
            if probe.status is not None and probe.status >= 400:
                report.warnings.append(
                    f"{fetch_source} returned HTTP {probe.status}; remaining checks rely on declared metadata only"
                )
            elif probe.error or not report.fetched:
                report.warnings.append(
                    f"{fetch_source} could not be fetched ({probe.error or 'no response'}); "
                    "content-based checks skipped"
                )
        else:
            if not fetch_url:
                report.warnings.append(
                    "no dcat:downloadURL or dcat:accessURL — content-based checks skipped"
                )
            report.signals.append(TypeSignal("http_content_type", None, None))
            report.signals.append(TypeSignal("attachment_filename", None, None))
            report.signals.append(TypeSignal("sniff", None, None))

        # ---- coalesce
        report.coalesced_mime, report.issues = self._coalesce(report.signals)
        report.is_consistent = not report.issues

        # archive-vs-format relaxation, mirroring CKAN's archive branch
        if report.is_consistent:
            sniffed_mime = self._signal_value(report.signals, "sniff")
            if sniffed_mime in self.archive_mimetypes:
                report.warnings.append(
                    "underlying file is an archive — declared format describes archive contents"
                )

        # Make the attachment-based demotion (in ``_coalesce``) visible in the
        # report: if ``http_content_type`` disagreed with the coalesced MIME
        # but the attachment filename agreed, surface that as a warning.
        attachment_mime = self._signal_value(report.signals, "attachment_filename")
        http_mime = self._signal_value(report.signals, "http_content_type")
        if (
            report.coalesced_mime
            and attachment_mime
            and http_mime
            and self._type_equals(attachment_mime, report.coalesced_mime)
            and not self._type_equals(http_mime, report.coalesced_mime)
        ):
            report.warnings.append(
                f"HTTP Content-Type {http_mime!r} disagrees with attachment "
                f"filename ({report.attachment_filename!r} → {attachment_mime!r}); "
                "treating Content-Type as advisory"
            )

        self.logger.debug(_format_report(report))

        return report

    # ---- helpers --------------------------------------------------------------

    def _iter_distributions(self, graph: Graph) -> Iterable[URIRef]:
        seen: set = set()
        for _, _, dist in graph.triples((None, DCAT.distribution, None)):
            if isinstance(dist, URIRef) and dist not in seen:
                seen.add(dist)
                yield dist
        # fall back: anything typed as dcat:Distribution
        for s, _, _ in graph.triples((None, None, DCAT.Distribution)):
            if isinstance(s, URIRef) and s not in seen:
                seen.add(s)
                yield s

    def _first_uri(self, graph: Graph, subject: URIRef, predicate) -> Optional[str]:
        for obj in graph.objects(subject, predicate):
            return str(obj)
        return None

    def _first_literal(self, graph: Graph, subject: URIRef, predicate) -> Optional[str]:
        for obj in graph.objects(subject, predicate):
            return str(obj)
        return None

    def _signal_from_format(self, graph: Graph, subject: URIRef) -> TypeSignal:
        for obj in graph.objects(subject, DCTERMS.format):
            raw = str(obj)
            mime = EU_FILE_TYPE_TO_MIME.get(raw)
            if mime is None and not raw.startswith("http"):
                # plain string like "CSV" → guess MIME from a fake filename
                mime = mimetypes.guess_type(f"example.{raw.lower()}")[0]
            return TypeSignal("dct:format", raw, mime)
        return TypeSignal("dct:format", None, None)

    def _signal_from_media_type(self, graph: Graph, subject: URIRef) -> TypeSignal:
        for obj in graph.objects(subject, DCAT.mediaType):
            raw = str(obj)
            mime = _normalize_media_type(raw)
            return TypeSignal("dcat:mediaType", raw, mime)
        return TypeSignal("dcat:mediaType", None, None)

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
        The raw value stays useful for diagnostics; the ``mime_type`` is
        derived from the filename's extension via ``mimetypes``.
        """
        if not attachment_filename:
            return TypeSignal("attachment_filename", None, None)
        guess, _ = mimetypes.guess_type(attachment_filename, strict=False)
        # Keep a hint about *why* this signal exists — disposition vs.
        # final-URL fallback — in the raw value, useful when reading the
        # report manually.
        raw = attachment_filename
        if not content_disposition:
            raw = f"{attachment_filename} (from final URL)"
        return TypeSignal("attachment_filename", raw, guess)

    def _probe(self, url: str) -> "_ProbeResult":
        content_type: Optional[str] = None
        content_disposition: Optional[str] = None
        final_url: Optional[str] = None
        sample = b""
        status: Optional[int] = None
        error: Optional[str] = None

        try:
            # HEAD first for size/type without downloading the body.
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
                # Prefer the GET response headers — some servers omit
                # Content-Disposition / Content-Type on HEAD or compute them
                # differently from the actual GET body.
                if resp.headers.get("Content-Type"):
                    content_type = resp.headers.get("Content-Type")
                if resp.headers.get("Content-Disposition"):
                    content_disposition = resp.headers.get("Content-Disposition")
                chunks: list[bytes] = []
                received = 0
                for chunk in resp.iter_content(chunk_size=self.sample_bytes):
                    if not chunk:
                        continue
                    chunks.append(chunk)
                    received += len(chunk)
                    if received >= self.sample_bytes:
                        break
                sample = b"".join(chunks)[: self.sample_bytes]
                # CKAN trick: some old libmagic outputs need more data
                if sample and sample[:5] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"[:5]:
                    # OLE compound document → read the full body once
                    sample = resp.content
        except requests.RequestException as exc:
            error = (error + " | " if error else "") + f"GET failed: {exc}"

        sniffed = _sniff_mime(sample)
        attachment_filename = _filename_from_content_disposition(content_disposition)
        # Fallback: derive a filename from the final URL's path when the
        # server didn't set Content-Disposition. This catches CDN-style
        # downloads that redirect to ``…/file.csv`` with a generic
        # Content-Type.
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
            sniffed=sniffed,
            sample=sample,
            status=status,
            error=error,
        )

    # ---- coalesce + equality, ported from CKAN's ResourceTypeValidator -------

    # Priority order used for both coalescing iteration and message
    # stability. ``attachment_filename`` sits ahead of ``http_content_type``
    # because the server's ``Content-Disposition: attachment; filename=...``
    # is a stronger assertion about what's in the body than the
    # ``Content-Type`` header (which servers often leave generic / wrong on
    # download endpoints).
    _SIGNAL_PRIORITY = (
        "dct:format",
        "dcat:mediaType",
        "url_extension",
        "attachment_filename",
        "http_content_type",
        "sniff",
    )

    def _coalesce(self, signals: list[TypeSignal]) -> tuple[Optional[str], list[str]]:
        """Pick the most specific MIME that is consistent with every signal.

        Returns ``(best_mime, issues)``. ``issues`` is empty when all non-None
        signals agree under the equality / override rules.
        """
        mime_types = [s.mime_type for s in signals if s.mime_type]
        if not mime_types:
            return None, []

        # In CKAN, ``allow_override`` is gated on whether the *upload* signals
        # are generic. We replicate that here from the dct:format /
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
        # produce stable order for the message
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
                # Two override directions:
                #   * downward: new signal is a less specific superset of
                #     ``best`` (e.g. best=application/gml+xml, new=application/xml).
                #     This is always compatible — keep ``best``, no upgrade.
                #   * upward: new signal would promote ``best`` to something more
                #     specific. Only do this when ``allow_override`` says the
                #     declared metadata was generic / unspecified to begin with.
                if more_specific == best:
                    continue
                if allow_override:
                    best = more_specific
                    continue
            # Demotion: when ``http_content_type`` disagrees with ``best`` but
            # the attachment evidence (Content-Disposition / final-URL
            # filename) agrees with ``best``, the server's Content-Type is
            # misleading download-portal noise — drop the conflict. The
            # caller still has the raw signal in the report for diagnostics.
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

    @staticmethod
    def _signal_value(signals: list[TypeSignal], source: str) -> Optional[str]:
        for sig in signals:
            if sig.source == source:
                return sig.mime_type
        return None


# ---------------------------------------------------------------------------
# Module-level helpers
# ---------------------------------------------------------------------------


_CONTENT_DISPOSITION_FILENAME_RE = re.compile(
    r'filename\*?=(?:UTF-8\'\')?"?([^";]+)"?',
    flags=re.IGNORECASE,
)


def _filename_from_content_disposition(value: Optional[str]) -> Optional[str]:
    """Extract the ``filename=`` (or ``filename*=``) parameter from a
    ``Content-Disposition`` header value.

    The regex covers the common forms — quoted, unquoted, and the RFC 5987
    ``filename*=UTF-8''…`` extension. Returns ``None`` for headers without a
    parseable filename (including missing headers).
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


def _hex_preview(sample: bytes, limit: int = 32) -> Optional[str]:
    if not sample:
        return None
    head = sample[:limit]
    try:
        return head.decode("utf-8")
    except UnicodeDecodeError:
        return head.hex()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def _format_report(report: DistributionReport) -> str:
    lines: list[str] = []
    status = "OK   " if report.is_consistent else "ERROR"
    title_part = f" — {report.title}" if report.title else ""
    lines.append(f"[{status}] {report.distribution_uri}{title_part}")
    if report.download_url:
        lines.append(f"  downloadURL : {report.download_url}")
    if report.access_url and report.access_url != report.download_url:
        lines.append(f"  accessURL   : {report.access_url}")
    if report.fetched:
        lines.append(f"  HTTP        : {report.status_code}")
    elif report.fetch_error:
        lines.append(f"  HTTP error  : {report.fetch_error}")
    if report.final_url and report.final_url != (
        report.download_url or report.access_url
    ):
        lines.append(f"  final URL   : {report.final_url}")
    if report.attachment_filename:
        lines.append(f"  attachment  : {report.attachment_filename}")
    lines.append("  signals     :")
    for sig in report.signals:
        lines.append(
            f"    {sig.source:20s} raw={_short(sig.raw_value):40s} mime={sig.mime_type or '-'}"
        )
    lines.append(f"  coalesced   : {report.coalesced_mime or '-'}")
    for warn in report.warnings:
        lines.append(f"  warning     : {warn}")
    for issue in report.issues:
        lines.append(f"  issue       : {issue}")
    return "\n".join(lines)


def _short(value: Optional[str], width: int = 40) -> str:
    if value is None:
        return "-"
    if len(value) <= width:
        return value
    return value[: width - 1] + "…"


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate DCAT distribution type signals in RDF files."
    )
    parser.add_argument("rdf_files", nargs="+", help="One or more RDF/XML files.")
    parser.add_argument(
        "--no-fetch",
        action="store_true",
        help="Skip HTTP fetching; only compare declared signals (dct:format, dcat:mediaType, URL extension).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output a JSON report instead of the human-readable one.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10.0,
        help="HTTP timeout (seconds, applied to connect and read).",
    )
    args = parser.parse_args(argv)

    validator = DistributionTypeValidator(
        timeout=(args.timeout, args.timeout),
        fetch_enabled=not args.no_fetch,
        logger=logging.getLogger(__name__),
    )

    all_reports: dict[str, list[dict[str, Any]]] = {}
    exit_code = 0
    for rdf_file in args.rdf_files:
        reports = validator.validate_file(rdf_file)
        if args.json:
            all_reports[rdf_file] = [_report_to_dict(r) for r in reports]
        else:
            print(f"=== {rdf_file} — {len(reports)} distribution(s) ===")
            for report in reports:
                print(_format_report(report))
                print()
        if any(not r.is_consistent for r in reports):
            exit_code = 1

    if args.json:
        json.dump(all_reports, sys.stdout, indent=2, ensure_ascii=False)
        sys.stdout.write("\n")

    return exit_code


def _report_to_dict(report: DistributionReport) -> dict[str, Any]:
    data = asdict(report)
    data["signals"] = [asdict(s) for s in report.signals]
    return data


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
