"""Per-dataset facts derived once from the RDF graph.

The shape of this context **mirrors the RDF graph**:

* ``DatasetContext``       — one DCAT-AP-DE dataset. Holds the dataset-level
  fields directly (title, description, keywords, themes, modified, issued,
  spatial / temporal facts, license, contact point, …) and a list of
  ``DistributionContext`` for its distributions.
* ``DistributionContext``  — one ``dcat:Distribution``. Holds the
  distribution-level fields directly (title, downloadURL, accessURL,
  formats, media types, modified, issued, license, byteSize, …).

Indicators that care about *dataset* metadata read ``context.<field>``;
indicators that care about *distribution* metadata iterate
``context.distributions`` and read ``dist.<field>``. Indicators that have to
check both levels (e.g. ``dct:modified`` can appear on Dataset *and*
Distribution) iterate both and log which subject each value came from.

The context contains **no HTTP probe results** — it is cheap to compute and
any indicator that needs network access does its own probing on top.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field, fields as dataclass_fields, is_dataclass
from typing import TYPE_CHECKING, Any, Iterable, Optional

from pydantic import BaseModel
from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import DCAT, DCTERMS, RDF

if TYPE_CHECKING:
    from extraction.semantic_assessment import (
        ExpressivenessAssessment,
    )

from extraction.vocabularies import (
    IANA_MEDIA_TYPE_PREFIX,
    OPEN_LICENSE_URIS,
    VALID_CONTRIBUTOR_ID_URIS,
    VALID_FILE_TYPE_URIS,
    VALID_FREQUENCY_URIS,
    VALID_MEDIA_TYPE_TEMPLATES,
    VALID_POLITICAL_GEOCODING_LEVEL_URIS,
    VALID_THEME_URIS,
    get_geocoding_vocabulary_for_uri,
)

LOCN = Namespace("http://www.w3.org/ns/locn#")
DCATDE = Namespace("http://dcat-ap.de/def/dcatde/")
DCATAP = Namespace("http://data.europa.eu/r5r/")
_LANGUAGE = DCTERMS.language
_ACCESS_RIGHTS = DCTERMS.accessRights
_PUBLISHER = DCTERMS.publisher
_DCAT_START_DATE = URIRef(str(DCAT) + "startDate")
_DCAT_END_DATE = URIRef(str(DCAT) + "endDate")
_DCAT_BYTE_SIZE = URIRef(str(DCAT) + "byteSize")


@dataclass
class AdminUnitFact:
    """One ``locn:adminUnitL2`` URI with its geocoding-vocab classification."""

    uri: str
    segment: Optional[str]
    is_in_vocab: bool


@dataclass
class SourcedValue:
    """A single value tagged with which subject it came from.

    Used by indicators that aggregate over both Dataset and Distribution
    subjects (e.g. ``dct:modified`` checks) so they can show the source in
    logs and result details.
    """

    source_kind: str  # "dataset" | "distribution"
    source_uri: Optional[str]
    value: str


@dataclass
class TypeSignal:
    """One source of MIME-type information for a distribution.

    Declared signals (``dct:format``, ``dcat:mediaType``, URL extension) come
    from the RDF context; probe signals (``http_content_type``,
    ``attachment_filename``) are populated by the HTTP probe.
    """

    source: str
    raw_value: Optional[str]
    mime_type: Optional[str]


@dataclass
class DistributionProbe:
    """Everything the format/MIME probing pass learned about one distribution.

    Attached to ``DistributionContext.probe`` after
    ``attach_probes(context)`` runs. ``probe is None`` means probing was not
    attempted (e.g. distribution skipped by the per-dataset cap, or no
    fetchable URL); ``probe.fetched is False`` with ``fetch_error`` /
    ``status_code`` set means probing was attempted but the HTTP call did
    not succeed.

    The full ``signals`` list is preserved so downstream consumers (agents,
    reports, debug tooling) can see *every* MIME hint we collected — not just
    the coalesced winner.
    """

    signals: list[TypeSignal] = field(default_factory=list)
    coalesced_mime: Optional[str] = None
    issues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    fetched: bool = False
    status_code: Optional[int] = None
    fetch_error: Optional[str] = None
    download_status_code: Optional[int] = None
    download_fetch_error: Optional[str] = None
    access_status_code: Optional[int] = None
    access_fetch_error: Optional[str] = None
    final_url: Optional[str] = None
    content_disposition: Optional[str] = None
    attachment_filename: Optional[str] = None
    # Format-quality classifications — set by distribution_probes after coalescing.
    machine_readable_tier: str = "none"  # "high" | "mid" | "none"
    is_non_proprietary: bool = False

    @property
    def is_consistent(self) -> bool:
        return not self.issues


@dataclass
class DistributionContext:
    """All facts for a single ``dcat:Distribution``."""

    distribution_uri: str
    titles: list[str] = field(default_factory=list)
    descriptions: list[str] = field(default_factory=list)
    download_url: Optional[str] = None
    access_url: Optional[str] = None
    formats: list[str] = field(default_factory=list)
    formats_in_vocab: list[bool] = field(default_factory=list)
    media_types: list[str] = field(default_factory=list)
    media_types_form_valid: list[bool] = field(default_factory=list)
    media_types_in_vocab: list[bool] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    issued: list[str] = field(default_factory=list)
    licenses: list[str] = field(default_factory=list)
    licenses_open: list[bool] = field(default_factory=list)
    byte_size: Optional[str] = None
    availability: list[str] = field(default_factory=list)
    probe: Optional[DistributionProbe] = None  # Populated by attach_probes(context)

    @property
    def title(self) -> Optional[str]:
        return self.titles[0] if self.titles else None

    @property
    def has_download_url(self) -> bool:
        return bool(self.download_url)

    @property
    def has_access_url(self) -> bool:
        return bool(self.access_url)

    @property
    def fetch_url(self) -> Optional[str]:
        return self.download_url or self.access_url


@dataclass
class DatasetContext:
    """All facts for a ``dcat:Dataset`` + its distributions."""

    graph: Graph
    dataset_uri: Optional[str] = None
    titles: list[str] = field(default_factory=list)
    descriptions: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    themes: list[str] = field(default_factory=list)
    themes_in_vocab: list[bool] = field(default_factory=list)
    languages: list[str] = field(default_factory=list)
    modified: list[str] = field(default_factory=list)
    issued: list[str] = field(default_factory=list)
    accrual_periodicity: Optional[str] = None  # dct:accrualPeriodicity is 0..1
    accrual_periodicity_in_vocab: Optional[bool] = None
    start_dates: list[str] = field(default_factory=list)
    end_dates: list[str] = field(default_factory=list)
    geometries: list[str] = field(default_factory=list)
    spatial_resources: list[str] = field(default_factory=list)
    admin_units: list[AdminUnitFact] = field(default_factory=list)
    political_geocoding: list[AdminUnitFact] = field(default_factory=list)
    political_geocoding_level: list[str] = field(default_factory=list)
    political_geocoding_level_in_vocab: list[bool] = field(default_factory=list)
    availability: list[str] = field(default_factory=list)
    licenses: list[str] = field(default_factory=list)
    licenses_open: list[bool] = field(default_factory=list)
    access_rights: Optional[str] = None  # dct:accessRights is 0..1
    publisher: Optional[str] = None  # dct:publisher is 0..1
    contact_points: list[str] = field(default_factory=list)
    contributor_ids: list[str] = field(default_factory=list)
    contributor_ids_in_vocab: list[bool] = field(default_factory=list)
    distributions: list[DistributionContext] = field(default_factory=list)
    semantic_assessment: Optional["ExpressivenessAssessment"] = None
    #: Forensic record of the expressiveness LLM call: the model's raw tool-call
    #: arguments plus any parse/repair detail. Populated on every call, not just
    #: failures, so a run's result.json always shows what the model actually
    #: returned — independent of whether it validated.
    semantic_assessment_raw: Optional[dict] = None
    llm_usage: list[dict] = field(default_factory=list)

    @property
    def distribution_count(self) -> int:
        return len(self.distributions)

    @property
    def all_download_urls(self) -> list[str]:
        return [d.download_url for d in self.distributions if d.download_url]

    @property
    def all_access_urls(self) -> list[str]:
        return [d.access_url for d in self.distributions if d.access_url]

    @property
    def all_distribution_formats(self) -> list[str]:
        return [v for d in self.distributions for v in d.formats]

    @property
    def all_distribution_media_types(self) -> list[str]:
        return [v for d in self.distributions for v in d.media_types]

    @property
    def distributions_with_download_url(self) -> int:
        return sum(1 for d in self.distributions if d.has_download_url)

    def collect_modified(self) -> list[SourcedValue]:
        """All ``dct:modified`` values, tagged with their source subject."""
        out: list[SourcedValue] = [
            SourcedValue("dataset", self.dataset_uri, v) for v in self.modified
        ]
        for dist in self.distributions:
            out.extend(
                SourcedValue("distribution", dist.distribution_uri, v)
                for v in dist.modified
            )
        return out

    def collect_issued(self) -> list[SourcedValue]:
        """All ``dct:issued`` values, tagged with their source subject."""
        out: list[SourcedValue] = [
            SourcedValue("dataset", self.dataset_uri, v) for v in self.issued
        ]
        for dist in self.distributions:
            out.extend(
                SourcedValue("distribution", dist.distribution_uri, v)
                for v in dist.issued
            )
        return out

    def collect_licenses(self) -> list[SourcedValue]:
        """All ``dct:license`` values, tagged with their source subject."""
        out: list[SourcedValue] = [
            SourcedValue("dataset", self.dataset_uri, v) for v in self.licenses
        ]
        for dist in self.distributions:
            out.extend(
                SourcedValue("distribution", dist.distribution_uri, v)
                for v in dist.licenses
            )
        return out

    def to_dict(self) -> dict[str, Any]:
        """JSON-serialisable view of every fact in this context."""
        data = {
            f.name: _to_jsonable(getattr(self, f.name))
            for f in dataclass_fields(self)
            if f.name != "graph"
        }
        data["distribution_count"] = self.distribution_count
        return data

    def to_json(self, *, indent: Optional[int] = 2) -> str:
        """Serialise :meth:`to_dict` to a JSON string (UTF-8, non-ASCII kept)."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_agent_dict(self) -> dict[str, Any]:
        """Token-lean view for the semantic-evaluation agent."""
        return {
            "dataset": {
                "uri": self.dataset_uri,
                "titles": list(self.titles),
                "descriptions": list(self.descriptions),
                "keywords": list(self.keywords),
                "themes": list(self.themes),
                "languages": list(self.languages),
                "modified": list(self.modified),
                "issued": list(self.issued),
                "accrual_periodicity": self.accrual_periodicity,
                "temporal": {
                    "start_dates": list(self.start_dates),
                    "end_dates": list(self.end_dates),
                },
                "spatial": {
                    "resources": list(self.spatial_resources),
                    "geometries": list(self.geometries),
                    "admin_units": [a.uri for a in self.admin_units],
                },
                "licenses": list(self.licenses),
                "access_rights": self.access_rights,
                "publisher": self.publisher,
                "contact_points": list(self.contact_points),
            },
        }

    def to_agent_json(self, *, indent: Optional[int] = 2) -> str:
        """Serialise :meth:`to_agent_dict` to JSON (UTF-8, non-ASCII kept)."""
        return json.dumps(self.to_agent_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_graph(cls, graph: Graph) -> "DatasetContext":
        dataset_subjects = list(graph.subjects(RDF.type, DCAT.Dataset))
        dataset_uri = str(dataset_subjects[0]) if dataset_subjects else None
        distributions = [
            _distribution_from_graph(graph, dist) for dist in _iter_distributions(graph)
        ]
        themes = _multi(graph, dataset_subjects, DCAT.theme)
        accrual = _single(graph, dataset_subjects, DCTERMS.accrualPeriodicity)
        licenses = _multi(graph, dataset_subjects, DCTERMS.license)
        contributor_ids = _multi(graph, dataset_subjects, DCATDE.contributorID)
        # adminUnitL2 sits on the nested ``dct:Location`` blank node inside
        # ``dct:spatial``, not directly on the dataset — collect globally
        # (same robustness reason as for geometries / start_dates).
        admin_units = [
            _admin_unit_fact(str(o)) for o in graph.objects(predicate=LOCN.adminUnitL2)
        ]
        # DCAT-AP.de's normative field for political/administrative coverage is
        # ``dcatde:politicalGeocodingURI`` (Konvention 08, MUSS where applicable);
        # ``locn:adminUnitL2`` is the generic DCAT-AP fallback.
        political_geocoding = [
            _admin_unit_fact(str(o))
            for s in dataset_subjects
            for o in graph.objects(s, DCATDE.politicalGeocodingURI)
        ]
        geocoding_level = _multi(
            graph, dataset_subjects, DCATDE.politicalGeocodingLevelURI
        )
        return cls(
            graph=graph,
            dataset_uri=dataset_uri,
            titles=_multi(graph, dataset_subjects, DCTERMS.title),
            descriptions=_multi(graph, dataset_subjects, DCTERMS.description),
            keywords=_multi(graph, dataset_subjects, DCAT.keyword),
            themes=themes,
            themes_in_vocab=[t in VALID_THEME_URIS for t in themes],
            languages=_multi(graph, dataset_subjects, _LANGUAGE),
            modified=_multi(graph, dataset_subjects, DCTERMS.modified),
            issued=_multi(graph, dataset_subjects, DCTERMS.issued),
            accrual_periodicity=accrual,
            accrual_periodicity_in_vocab=(
                accrual in VALID_FREQUENCY_URIS if accrual is not None else None
            ),
            start_dates=[str(o) for o in graph.objects(predicate=_DCAT_START_DATE)],
            end_dates=[str(o) for o in graph.objects(predicate=_DCAT_END_DATE)],
            geometries=[str(o) for o in graph.objects(predicate=LOCN.geometry)],
            spatial_resources=_multi(graph, dataset_subjects, DCTERMS.spatial),
            admin_units=admin_units,
            political_geocoding=political_geocoding,
            political_geocoding_level=geocoding_level,
            political_geocoding_level_in_vocab=[
                u in VALID_POLITICAL_GEOCODING_LEVEL_URIS for u in geocoding_level
            ],
            availability=_multi(graph, dataset_subjects, DCATAP.availability),
            licenses=licenses,
            licenses_open=[lic in OPEN_LICENSE_URIS for lic in licenses],
            access_rights=_single(graph, dataset_subjects, _ACCESS_RIGHTS),
            publisher=_single(graph, dataset_subjects, _PUBLISHER),
            contact_points=_multi(graph, dataset_subjects, DCAT.contactPoint),
            contributor_ids=contributor_ids,
            contributor_ids_in_vocab=[
                c in VALID_CONTRIBUTOR_ID_URIS for c in contributor_ids
            ],
            distributions=distributions,
        )


def _to_jsonable(value: Any) -> Any:
    """Recursively convert dataclasses / containers into JSON-friendly values.

    Dataclass *instances* become plain dicts (properties are not included —
    only declared fields); lists/tuples and dicts are walked element-wise;
    every other value is returned unchanged (the context only ever holds
    ``str`` / ``bool`` / ``int`` / ``None`` leaves).
    """
    if is_dataclass(value) and not isinstance(value, type):
        return {
            f.name: _to_jsonable(getattr(value, f.name))
            for f in dataclass_fields(value)
        }
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, (list, tuple)):
        return [_to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _to_jsonable(item) for key, item in value.items()}
    return value


def _distribution_agent_view(dist: "DistributionContext") -> dict[str, Any]:
    """Compact, agent-facing view of one distribution."""
    probe = dist.probe
    return {
        "uri": dist.distribution_uri,
        "titles": list(dist.titles),
        "descriptions": list(dist.descriptions),
        "download_url": dist.download_url,
        "access_url": dist.access_url,
        "formats": list(dist.formats),
        "media_types": list(dist.media_types),
        "licenses": list(dist.licenses),
        "byte_size": dist.byte_size,
        "effective_mime": probe.coalesced_mime if probe else None,
        "format_congruent": probe.is_consistent if probe else None,
        "reachable": _probe_reachable(probe),
    }


def _probe_reachable(probe: Optional["DistributionProbe"]) -> Optional[bool]:
    """``True``/``False`` if any declared URL was fetched (HTTP < 400), else None.

    ``None`` distinguishes "not probed" (no network attempt, e.g. sampling cap
    or no fetchable URL) from a genuine "unreachable" verdict.
    """
    if probe is None:
        return None
    codes = [
        code
        for code in (probe.download_status_code, probe.access_status_code)
        if code is not None
    ]
    if not codes:
        return None
    return any(200 <= code < 400 for code in codes)


def _iter_distributions(graph: Graph) -> Iterable[URIRef]:
    """Yield each ``dcat:Distribution`` URIRef in the graph (deduplicated)."""
    seen: set = set()
    for _, _, dist in graph.triples((None, DCAT.distribution, None)):
        if isinstance(dist, URIRef) and dist not in seen:
            seen.add(dist)
            yield dist
    for s, _, _ in graph.triples((None, None, DCAT.Distribution)):
        if isinstance(s, URIRef) and s not in seen:
            seen.add(s)
            yield s


def _multi(graph: Graph, subjects: Iterable[URIRef], predicate) -> list[str]:
    """Collect all object values for the given predicate across the given subjects."""
    out: list[str] = []
    for subj in subjects:
        out.extend(str(o) for o in graph.objects(subj, predicate))
    return out


def _first_value(graph: Graph, subject: URIRef, predicate) -> Optional[str]:
    """Return the first object value for the given subject and predicate, or None."""
    for obj in graph.objects(subject, predicate):
        return str(obj)
    return None


def _single(graph: Graph, subjects: Iterable[URIRef], predicate) -> Optional[str]:
    """First object value for a 0..1 predicate across the given subjects, or None.

    Counterpart to :func:`_multi` for DCAT-AP.de properties with cardinality
    ``0..1``. Should a non-conformant record illegally carry more than one
    value, only the first is used; the cardinality violation itself is reported
    separately by the SHACL conformance indicator (``reuse_dcat_ap_de_compliance``).
    """
    for subj in subjects:
        for obj in graph.objects(subj, predicate):
            return str(obj)
    return None


def _admin_unit_fact(uri: str) -> AdminUnitFact:
    """Get the geocoding vocabulary classification for one ``locn:adminUnitL2`` URI."""
    segment, valid_uris = get_geocoding_vocabulary_for_uri(uri)
    return AdminUnitFact(
        uri=uri,
        segment=segment,
        is_in_vocab=valid_uris is not None and uri in valid_uris,
    )


def _distribution_from_graph(graph: Graph, distribution: URIRef) -> DistributionContext:
    titles = [str(o) for o in graph.objects(distribution, DCTERMS.title)]
    descriptions = [str(o) for o in graph.objects(distribution, DCTERMS.description)]
    formats = [str(o) for o in graph.objects(distribution, DCTERMS.format)]
    media_types = [str(o) for o in graph.objects(distribution, DCAT.mediaType)]
    modified = [str(o) for o in graph.objects(distribution, DCTERMS.modified)]
    issued = [str(o) for o in graph.objects(distribution, DCTERMS.issued)]
    licenses = [str(o) for o in graph.objects(distribution, DCTERMS.license)]
    availability = [str(o) for o in graph.objects(distribution, DCATAP.availability)]
    return DistributionContext(
        distribution_uri=str(distribution),
        titles=titles,
        descriptions=descriptions,
        download_url=_first_value(graph, distribution, DCAT.downloadURL),
        access_url=_first_value(graph, distribution, DCAT.accessURL),
        formats=formats,
        formats_in_vocab=[v in VALID_FILE_TYPE_URIS for v in formats],
        media_types=media_types,
        media_types_form_valid=[
            v.startswith(IANA_MEDIA_TYPE_PREFIX) for v in media_types
        ],
        media_types_in_vocab=[
            v.startswith(IANA_MEDIA_TYPE_PREFIX)
            and v[len(IANA_MEDIA_TYPE_PREFIX) :] in VALID_MEDIA_TYPE_TEMPLATES
            for v in media_types
        ],
        modified=modified,
        issued=issued,
        licenses=licenses,
        licenses_open=[lic in OPEN_LICENSE_URIS for lic in licenses],
        byte_size=_first_value(graph, distribution, _DCAT_BYTE_SIZE),
        availability=availability,
    )
