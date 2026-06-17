"""Faithful, minimal re-implementation of the data.europa.eu MQA score.

This is the **comparison baseline** for the evaluation (see
``docs/evaluation_vs_mqa.md``). It reproduces the metric set and point values of
the original piveau ``metrics`` pipeline (405 points across five FAIR
dimensions) so the prototype's scores can be compared against MQA on the same
RDF input.

Deliberate design choices (documented for the thesis methodology):

* It runs on the prototype's own :class:`~extraction.dataset_context.DatasetContext`
  and the **same vocabularies** under ``extraction/vocabularies`` — this is what
  makes the two scores comparable (identical reference data).
* ``dcat_ap_compliance`` (30 pts) is **defaulted to True**, like the public
  re-implementations: a real DCAT-AP SHACL run is out of scope. Toggle via
  :class:`MqaOptions`.
* ``machine-readable`` and ``non-proprietary`` rely on curated boolean lists that
  are NOT part of the EU file-type vocabulary; the canonical EDP/piveau lists are
  embedded below (source URLs in the constants).
* ``licence`` / ``date issued`` / ``date modified`` presence is taken across
  dataset *and* distribution level (``collect_*``). Where MQA is strictly
  distribution-level this is, if anything, generous to the MQA baseline — the
  conservative direction for an "our model is better" argument.

Point values verified against piveau ``piveau-metrics-score`` (default score TTL)
and ``mjanez/metadata-quality-react`` ``mqa-config.json`` (maxScore 405).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from rdflib.namespace import DCTERMS

from extraction.dataset_context import DatasetContext, DistributionContext
from extraction.vocabularies import VALID_ACCESS_RIGHT_URIS

# --- Dimensions ------------------------------------------------------------

FINDABILITY = "findability"
ACCESSIBILITY = "accessibility"
INTEROPERABILITY = "interoperability"
REUSABILITY = "reusability"
CONTEXTUALITY = "contextuality"

#: Per-dimension maxima (sum = 405), as used by data.europa.eu.
DIMENSION_MAX = {
    FINDABILITY: 100,
    ACCESSIBILITY: 100,
    INTEROPERABILITY: 110,
    REUSABILITY: 75,
    CONTEXTUALITY: 20,
}
MQA_MAX = sum(DIMENSION_MAX.values())  # 405

#: Rating bands from piveau ``PiveauScoring`` (code boundaries, not the prose).
RATING_BANDS = (
    (351, "excellent"),
    (221, "good"),
    (120, "sufficient"),
    (0, "bad"),
)

# --- Curated format lists (EDP/piveau, not in the EU file-type vocab) -------
# Source: gitlab.com/european-data-portal/edp-vocabularies @ master
#   edp-non-proprietary-format.rdf / edp-machine-readable-format.rdf
_FT = "http://publications.europa.eu/resource/authority/file-type/"

NON_PROPRIETARY_FORMAT_URIS = frozenset(
    _FT + code
    for code in (
        "BMP", "CSV", "DBF", "GEOJSON", "GZIP", "HTML", "ICS", "JPEG2000",
        "JSON", "JSON_LD", "KML", "KMZ", "NETCDF", "ODS", "PNG", "RDF_N_QUADS",
        "RDF_N_TRIPLES", "RDF_TRIG", "RDF_TURTLE", "RDF_XML", "RSS", "RTF",
        "TAR", "TIFF", "TSV", "TXT", "WMS_SRVC", "XML", "ZIP",
    )
)

MACHINE_READABLE_FORMAT_URIS = frozenset(
    _FT + code
    for code in (
        "CSV", "GEOJSON", "ICS", "JSON", "JSON_LD", "KML", "KMZ", "NETCDF",
        "ODS", "RDFA", "RDF_N_QUADS", "RDF_N_TRIPLES", "RDF_TRIG", "RDF_TURTLE",
        "RDF_XML", "RSS", "SHP", "XLS", "XLSX", "XML",
    )
)

#: A licence is "known" iff its URI is in the EU Publications Office licence
#: authority — this mirrors the official MQA ``knownLicence``. NOTE: national
#: licences (e.g. ``http://dcat-ap.de/def/licenses/...``) are NOT in this
#: authority, so they count as "unknown" here exactly as data.europa.eu reports
#: them — a known MQA limitation for national portals.
EU_LICENCE_AUTHORITY_PREFIX = "http://publications.europa.eu/resource/authority/licence/"


@dataclass(frozen=True)
class MqaOptions:
    """Tunable bits of the MQA baseline."""

    #: Awarded for ``dcatApCompliance`` (30 pts) when no real SHACL run is done.
    dcat_ap_compliant: bool = True


# --- Metric helpers --------------------------------------------------------


def _http_ok(code) -> bool:
    return code is not None and 200 <= code < 400


def _any_dist(ctx: DatasetContext, pred: Callable[[DistributionContext], bool]) -> bool:
    """True if any distribution satisfies ``pred`` (MQA 'best distribution')."""
    return any(pred(d) for d in ctx.distributions)


def _format_in(uris: frozenset, dist: DistributionContext) -> bool:
    return any(f in uris for f in dist.formats)


@dataclass
class _Metric:
    key: str
    dimension: str
    points: int
    check: Callable[[DatasetContext, MqaOptions], bool]


#: The 22 MQA metrics, with the property they inspect noted in the comment.
METRICS: list[_Metric] = [
    # Findability (100)
    _Metric("keyword_availability", FINDABILITY, 30, lambda c, o: bool(c.keywords)),
    _Metric("category_availability", FINDABILITY, 30, lambda c, o: bool(c.themes)),
    _Metric("spatial_availability", FINDABILITY, 20,
            lambda c, o: bool(c.spatial_resources or c.geometries or c.admin_units)),
    _Metric("temporal_availability", FINDABILITY, 20,
            lambda c, o: bool(c.start_dates or c.end_dates)),
    # Accessibility (100) — distribution level, best distribution
    _Metric("access_url_status_code", ACCESSIBILITY, 50,
            lambda c, o: _any_dist(c, lambda d: bool(d.probe) and _http_ok(d.probe.access_status_code))),
    _Metric("download_url_availability", ACCESSIBILITY, 20,
            lambda c, o: _any_dist(c, lambda d: d.has_download_url)),
    _Metric("download_url_status_code", ACCESSIBILITY, 30,
            lambda c, o: _any_dist(c, lambda d: bool(d.probe) and _http_ok(d.probe.download_status_code))),
    # Interoperability (110)
    _Metric("format_availability", INTEROPERABILITY, 20,
            lambda c, o: _any_dist(c, lambda d: bool(d.formats))),
    _Metric("media_type_availability", INTEROPERABILITY, 10,
            lambda c, o: _any_dist(c, lambda d: bool(d.media_types))),
    _Metric("format_media_type_vocabulary", INTEROPERABILITY, 10,
            lambda c, o: _any_dist(c, lambda d: any(d.formats_in_vocab) or any(d.media_types_in_vocab))),
    _Metric("format_non_proprietary", INTEROPERABILITY, 20,
            lambda c, o: _any_dist(c, lambda d: _format_in(NON_PROPRIETARY_FORMAT_URIS, d))),
    _Metric("format_machine_readable", INTEROPERABILITY, 20,
            lambda c, o: _any_dist(c, lambda d: _format_in(MACHINE_READABLE_FORMAT_URIS, d))),
    _Metric("dcat_ap_compliance", INTEROPERABILITY, 30, lambda c, o: o.dcat_ap_compliant),
    # Reusability (75)
    _Metric("license_availability", REUSABILITY, 20, lambda c, o: bool(c.collect_licenses())),
    _Metric("known_license", REUSABILITY, 10,
            lambda c, o: any(sv.value.startswith(EU_LICENCE_AUTHORITY_PREFIX) for sv in c.collect_licenses())),
    _Metric("access_rights_availability", REUSABILITY, 10, lambda c, o: bool(c.access_rights)),
    _Metric("access_rights_vocabulary", REUSABILITY, 5,
            lambda c, o: any(a in VALID_ACCESS_RIGHT_URIS for a in c.access_rights)),
    _Metric("contact_point_availability", REUSABILITY, 20, lambda c, o: bool(c.contact_points)),
    _Metric("publisher_availability", REUSABILITY, 10, lambda c, o: bool(c.publishers)),
    # Contextuality (20)
    _Metric("rights_availability", CONTEXTUALITY, 5,
            lambda c, o: bool(list(c.graph.triples((None, DCTERMS.rights, None))))),
    _Metric("byte_size_availability", CONTEXTUALITY, 5,
            lambda c, o: _any_dist(c, lambda d: bool(d.byte_size))),
    _Metric("date_issued_availability", CONTEXTUALITY, 5, lambda c, o: bool(c.collect_issued())),
    _Metric("date_modified_availability", CONTEXTUALITY, 5, lambda c, o: bool(c.collect_modified())),
]


def _rating(total: int) -> str:
    for threshold, label in RATING_BANDS:
        if total >= threshold:
            return label
    return "bad"


def score_dataset(context: DatasetContext, options: MqaOptions | None = None) -> dict:
    """Compute the MQA score for one dataset context.

    Returns a JSON-serialisable dict with the total (0..405), the normalised
    score (0..1), the rating band, per-dimension subtotals and every metric's
    awarded points.
    """
    opts = options or MqaOptions()

    metrics: dict[str, dict] = {}
    by_dimension = {dim: 0 for dim in DIMENSION_MAX}
    for m in METRICS:
        passed = bool(m.check(context, opts))
        awarded = m.points if passed else 0
        by_dimension[m.dimension] += awarded
        metrics[m.key] = {
            "dimension": m.dimension,
            "points": awarded,
            "max": m.points,
            "passed": passed,
        }

    total = sum(by_dimension.values())
    return {
        "total": total,
        "max": MQA_MAX,
        "normalized": round(total / MQA_MAX, 4),
        "rating": _rating(total),
        "by_dimension": {
            dim: {"score": by_dimension[dim], "max": DIMENSION_MAX[dim]}
            for dim in DIMENSION_MAX
        },
        "metrics": metrics,
    }
