"""Faithful, minimal re-implementation of the data.europa.eu MQA score.

This is the **comparison baseline** for the evaluation (see
thesis section 6.4). It reproduces the metric set, point values and
aggregation of the original piveau ``metrics`` pipeline (405 points across five
FAIR dimensions) so the prototype's scores can be compared against MQA on the
same RDF input.

Aggregation (matches piveau ``Scoring.kt``):

* **Dataset-level metrics** are scored directly from the dataset.
* **Distribution-level metrics** follow MQA's *single best distribution* rule:
  each distribution is scored in full, the distribution with the highest total
  is selected, and ALL its metric values are used. (MQA assumes every
  distribution carries the same content, so the best one represents the
  dataset.) ``date issued`` / ``date modified`` are taken from that distribution,
  falling back to the dataset level if the distribution lacks them.

Deliberate design choices (documented for the thesis methodology):

* It runs on the prototype's own :class:`~extraction.dataset_context.DatasetContext`
  and the **same vocabularies** under ``extraction/vocabularies`` — identical
  reference data is what makes the two scores comparable.
* ``dcat_ap_compliance`` (30 pts) is **defaulted to True**, like the public
  re-implementations: a real DCAT-AP SHACL run is out of scope. Toggle via
  :class:`MqaOptions`.
* **Formats / media types are matched URI-strict** (no literal normalisation):
  a literal ``<dct:format>CSV</dct:format>`` does NOT count as vocabulary-aligned.
  This deviates from the official MQA, which normalises such literals — even
  though its own SHACL check rejects them as non-conformant. The strict reading
  is definition-true ("must come from the controlled vocabulary"); the deviation
  is intentional and documented.
* ``machine-readable`` / ``non-proprietary`` rely on curated boolean lists that
  are NOT part of the EU file-type vocabulary; the canonical EDP/piveau lists are
  embedded below (source URLs in the constants).
* ``knownLicence`` checks the EU licence authority — national licences
  (``dcat-ap.de/...``) count as "unknown", exactly as data.europa.eu reports.

Point values verified against piveau ``piveau-metrics-score`` (default score TTL)
and ``mjanez/metadata-quality-react`` ``mqa-config.json`` (maxScore 405).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from rdflib import URIRef
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
        "BMP",
        "CSV",
        "DBF",
        "GEOJSON",
        "GZIP",
        "HTML",
        "ICS",
        "JPEG2000",
        "JSON",
        "JSON_LD",
        "KML",
        "KMZ",
        "NETCDF",
        "ODS",
        "PNG",
        "RDF_N_QUADS",
        "RDF_N_TRIPLES",
        "RDF_TRIG",
        "RDF_TURTLE",
        "RDF_XML",
        "RSS",
        "RTF",
        "TAR",
        "TIFF",
        "TSV",
        "TXT",
        "WMS_SRVC",
        "XML",
        "ZIP",
    )
)

MACHINE_READABLE_FORMAT_URIS = frozenset(
    _FT + code
    for code in (
        "CSV",
        "GEOJSON",
        "ICS",
        "JSON",
        "JSON_LD",
        "KML",
        "KMZ",
        "NETCDF",
        "ODS",
        "RDFA",
        "RDF_N_QUADS",
        "RDF_N_TRIPLES",
        "RDF_TRIG",
        "RDF_TURTLE",
        "RDF_XML",
        "RSS",
        "SHP",
        "XLS",
        "XLSX",
        "XML",
    )
)

#: A licence is "known" iff its URI is in the EU Publications Office licence
#: authority — this mirrors the official MQA ``knownLicence``. National licences
#: (e.g. ``http://dcat-ap.de/def/licenses/...``) are NOT in this authority, so
#: they count as "unknown" here exactly as data.europa.eu reports them.
EU_LICENCE_AUTHORITY_PREFIX = (
    "http://publications.europa.eu/resource/authority/licence/"
)


@dataclass(frozen=True)
class MqaOptions:
    """Tunable bits of the MQA baseline."""

    #: Fallback value when ``shacl_validation=False`` or the API call fails.
    dcat_ap_compliant: bool = True
    #: When True, calls the ITB SHACL API (same logic as the prototype indicator)
    #: instead of using the ``dcat_ap_compliant`` default.
    shacl_validation: bool = True


# --- Metric helpers --------------------------------------------------------


def _dcat_ap_compliance(c: "DatasetContext", o: MqaOptions) -> bool:
    """Check DCAT-AP.de compliance — calls the ITB SHACL API when enabled."""
    if not o.shacl_validation:
        return o.dcat_ap_compliant
    try:
        from utils.shacl_client import validate_graph

        return validate_graph(c.graph)["conforms"]
    except Exception:
        return o.dcat_ap_compliant  # fall back to the static default on errors


def _http_ok(code) -> bool:
    return code is not None and 200 <= code < 400


def _format_in(uris: frozenset, dist: DistributionContext) -> bool:
    return any(f in uris for f in dist.formats)


@dataclass
class _DatasetMetric:
    key: str
    dimension: str
    points: int
    check: Callable[[DatasetContext, MqaOptions], bool]


@dataclass
class _DistMetric:
    key: str
    dimension: str
    points: int
    check: Callable[[DistributionContext, DatasetContext, MqaOptions], bool]


#: Metrics measured on the dataset (property noted in the comment).
DATASET_METRICS: list[_DatasetMetric] = [
    _DatasetMetric(
        "keyword_availability", FINDABILITY, 30, lambda c, o: bool(c.keywords)
    ),
    _DatasetMetric(
        "category_availability", FINDABILITY, 30, lambda c, o: bool(c.themes)
    ),
    _DatasetMetric(
        "spatial_availability",
        FINDABILITY,
        20,
        lambda c, o: bool(c.spatial_resources or c.geometries or c.admin_units),
    ),
    _DatasetMetric(
        "temporal_availability",
        FINDABILITY,
        20,
        lambda c, o: bool(c.start_dates or c.end_dates),
    ),
    _DatasetMetric("dcat_ap_compliance", INTEROPERABILITY, 30, _dcat_ap_compliance),
    _DatasetMetric(
        "access_rights_availability",
        REUSABILITY,
        10,
        lambda c, o: bool(c.access_rights),
    ),
    _DatasetMetric(
        "access_rights_vocabulary",
        REUSABILITY,
        5,
        lambda c, o: c.access_rights in VALID_ACCESS_RIGHT_URIS,
    ),
    _DatasetMetric(
        "contact_point_availability",
        REUSABILITY,
        20,
        lambda c, o: bool(c.contact_points),
    ),
    _DatasetMetric(
        "publisher_availability", REUSABILITY, 10, lambda c, o: bool(c.publisher)
    ),
]

#: Metrics measured per distribution; scored from the single best distribution.
DISTRIBUTION_METRICS: list[_DistMetric] = [
    _DistMetric(
        "access_url_status_code",
        ACCESSIBILITY,
        50,
        lambda d, c, o: bool(d.probe) and _http_ok(d.probe.access_status_code),
    ),
    _DistMetric(
        "download_url_availability",
        ACCESSIBILITY,
        20,
        lambda d, c, o: d.has_download_url,
    ),
    _DistMetric(
        "download_url_status_code",
        ACCESSIBILITY,
        30,
        lambda d, c, o: bool(d.probe) and _http_ok(d.probe.download_status_code),
    ),
    _DistMetric(
        "format_availability", INTEROPERABILITY, 20, lambda d, c, o: bool(d.formats)
    ),
    _DistMetric(
        "media_type_availability",
        INTEROPERABILITY,
        10,
        lambda d, c, o: bool(d.media_types),
    ),
    _DistMetric(
        "format_media_type_vocabulary",
        INTEROPERABILITY,
        10,
        lambda d, c, o: any(d.formats_in_vocab) or any(d.media_types_in_vocab),
    ),
    _DistMetric(
        "format_non_proprietary",
        INTEROPERABILITY,
        20,
        lambda d, c, o: _format_in(NON_PROPRIETARY_FORMAT_URIS, d),
    ),
    _DistMetric(
        "format_machine_readable",
        INTEROPERABILITY,
        20,
        lambda d, c, o: _format_in(MACHINE_READABLE_FORMAT_URIS, d),
    ),
    _DistMetric(
        "license_availability", REUSABILITY, 20, lambda d, c, o: bool(d.licenses)
    ),
    _DistMetric(
        "known_license",
        REUSABILITY,
        10,
        lambda d, c, o: any(
            lic.startswith(EU_LICENCE_AUTHORITY_PREFIX) for lic in d.licenses
        ),
    ),
    _DistMetric(
        "rights_availability",
        CONTEXTUALITY,
        5,
        lambda d, c, o: bool(
            list(c.graph.triples((URIRef(d.distribution_uri), DCTERMS.rights, None)))
        ),
    ),
    _DistMetric(
        "byte_size_availability", CONTEXTUALITY, 5, lambda d, c, o: bool(d.byte_size)
    ),
    _DistMetric(
        "date_issued_availability", CONTEXTUALITY, 5, lambda d, c, o: bool(d.issued)
    ),
    _DistMetric(
        "date_modified_availability", CONTEXTUALITY, 5, lambda d, c, o: bool(d.modified)
    ),
]

#: Distribution metrics that fall back to the dataset value when the best
#: distribution lacks them (MQA's issued/modified handling).
_DATASET_FALLBACK = {
    "date_issued_availability": lambda c: bool(c.issued),
    "date_modified_availability": lambda c: bool(c.modified),
}


def _rating(total: int) -> str:
    for threshold, label in RATING_BANDS:
        if total >= threshold:
            return label
    return "bad"


def _best_distribution(context: DatasetContext, opts: MqaOptions) -> dict[str, bool]:
    """Return the passed-flags of the single highest-scoring distribution.

    Each distribution is scored over all distribution-level metrics; the one with
    the highest total points wins (ties keep the earlier distribution, as in
    piveau). With no distributions every distribution metric is ``False``.
    """
    if not context.distributions:
        return {m.key: False for m in DISTRIBUTION_METRICS}

    best_flags: dict[str, bool] | None = None
    best_total = -1
    for dist in context.distributions:
        flags = {
            m.key: bool(m.check(dist, context, opts)) for m in DISTRIBUTION_METRICS
        }
        total = sum(m.points for m in DISTRIBUTION_METRICS if flags[m.key])
        if total > best_total:
            best_total, best_flags = total, flags

    assert best_flags is not None
    # Dataset fallback for issued/modified when the chosen distribution lacks them.
    for key, dataset_check in _DATASET_FALLBACK.items():
        if not best_flags[key] and dataset_check(context):
            best_flags[key] = True
    return best_flags


def score_dataset(context: DatasetContext, options: MqaOptions | None = None) -> dict:
    """Compute the MQA score for one dataset context.

    Returns a JSON-serialisable dict with the total (0..405), the normalised
    score (0..1), the rating band, per-dimension subtotals and every metric's
    awarded points.
    """
    opts = options or MqaOptions()

    metrics: dict[str, dict] = {}
    by_dimension = {dim: 0 for dim in DIMENSION_MAX}

    def record(key: str, dimension: str, points: int, passed: bool) -> None:
        awarded = points if passed else 0
        by_dimension[dimension] += awarded
        metrics[key] = {
            "dimension": dimension,
            "points": awarded,
            "max": points,
            "passed": passed,
        }

    for m in DATASET_METRICS:
        record(m.key, m.dimension, m.points, bool(m.check(context, opts)))

    dist_flags = _best_distribution(context, opts)
    for m in DISTRIBUTION_METRICS:
        record(m.key, m.dimension, m.points, dist_flags[m.key])

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
