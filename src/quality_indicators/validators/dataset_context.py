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

from dataclasses import dataclass, field
from typing import Iterable, Optional

from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import DCAT, DCTERMS, RDF

from quality_indicators.vocabularies import (
    IANA_MEDIA_TYPE_PREFIX,
    OPEN_LICENSE_URIS,
    VALID_FILE_TYPE_URIS,
    VALID_FREQUENCY_URIS,
    VALID_MEDIA_TYPE_TEMPLATES,
    VALID_THEME_URIS,
    get_geocoding_vocabulary_for_uri,
)

LOCN = Namespace("http://www.w3.org/ns/locn#")
_LANGUAGE = DCTERMS.language
_ACCESS_RIGHTS = DCTERMS.accessRights
_PUBLISHER = DCTERMS.publisher
_DCAT_START_DATE = URIRef(str(DCAT) + "startDate")
_DCAT_END_DATE = URIRef(str(DCAT) + "endDate")
_DCAT_BYTE_SIZE = URIRef(str(DCAT) + "byteSize")


# ---------------------------------------------------------------------------
# Small value types
# ---------------------------------------------------------------------------


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
    ``attachment_filename``, ``sniff``) are populated by the HTTP probe.
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
    final_url: Optional[str] = None
    content_disposition: Optional[str] = None
    attachment_filename: Optional[str] = None
    sniffed_mime: Optional[str] = None

    @property
    def is_consistent(self) -> bool:
        return not self.issues


# ---------------------------------------------------------------------------
# Distribution
# ---------------------------------------------------------------------------


@dataclass
class DistributionContext:
    """All facts for a single ``dcat:Distribution``."""

    distribution_uri: str
    titles: list[str] = field(default_factory=list)
    descriptions: list[str] = field(default_factory=list)
    download_url: Optional[str] = None
    access_url: Optional[str] = None
    # Vocabulary-driven lists are stored alongside parallel-indexed
    # ``_in_vocab`` / ``_form_valid`` boolean lists so consumers don't have
    # to re-import the vocab modules.
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
    # Populated by ``attach_probes(context)`` (see
    # ``distribution_type_validation``). ``None`` = not attempted.
    probe: Optional[DistributionProbe] = None

    @property
    def title(self) -> Optional[str]:
        """First title (compatibility helper)."""
        return self.titles[0] if self.titles else None

    @property
    def has_download_url(self) -> bool:
        return bool(self.download_url)

    @property
    def has_access_url(self) -> bool:
        return bool(self.access_url)

    @property
    def fetch_url(self) -> Optional[str]:
        """Preferred URL for fetching the underlying resource."""
        return self.download_url or self.access_url


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------


@dataclass
class DatasetContext:
    """All facts for a ``dcat:Dataset`` + its distributions.

    If the graph contains multiple ``dcat:Dataset`` subjects, dataset-level
    fields are aggregated across all of them (the existing semantics) and
    ``dataset_uri`` exposes the first one.
    """

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
    accrual_periodicity: list[str] = field(default_factory=list)
    accrual_periodicity_in_vocab: list[bool] = field(default_factory=list)
    start_dates: list[str] = field(default_factory=list)
    end_dates: list[str] = field(default_factory=list)
    geometries: list[str] = field(default_factory=list)
    spatial_resources: list[str] = field(default_factory=list)
    admin_units: list[AdminUnitFact] = field(default_factory=list)
    licenses: list[str] = field(default_factory=list)
    licenses_open: list[bool] = field(default_factory=list)
    access_rights: list[str] = field(default_factory=list)
    publishers: list[str] = field(default_factory=list)
    contact_points: list[str] = field(default_factory=list)
    distributions: list[DistributionContext] = field(default_factory=list)

    # ------- distribution-level aggregates (cheap derived properties) ---

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

    # ------- cross-level aggregates (for indicators that check both) ----

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

    # ------- factory ----------------------------------------------------

    @classmethod
    def from_graph(cls, graph: Graph) -> "DatasetContext":
        dataset_subjects = list(graph.subjects(RDF.type, DCAT.Dataset))
        dataset_uri = str(dataset_subjects[0]) if dataset_subjects else None
        distributions = [
            _distribution_from_graph(graph, dist) for dist in _iter_distributions(graph)
        ]
        themes = _multi(graph, dataset_subjects, DCAT.theme)
        accrual = _multi(graph, dataset_subjects, DCTERMS.accrualPeriodicity)
        licenses = _multi(graph, dataset_subjects, DCTERMS.license)
        # adminUnitL2 sits on the nested ``dct:Location`` blank node inside
        # ``dct:spatial``, not directly on the dataset — collect globally
        # (same robustness reason as for geometries / start_dates).
        admin_units = [
            _admin_unit_fact(str(o)) for o in graph.objects(predicate=LOCN.adminUnitL2)
        ]
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
            accrual_periodicity_in_vocab=[v in VALID_FREQUENCY_URIS for v in accrual],
            # startDate / endDate are nested under dct:temporal — collect
            # them globally to remain robust against blank-node nesting.
            start_dates=[str(o) for o in graph.objects(predicate=_DCAT_START_DATE)],
            end_dates=[str(o) for o in graph.objects(predicate=_DCAT_END_DATE)],
            # geometries / adminUnits are nested under dct:spatial — also
            # collect them globally (same robustness reason).
            geometries=[str(o) for o in graph.objects(predicate=LOCN.geometry)],
            spatial_resources=_multi(graph, dataset_subjects, DCTERMS.spatial),
            admin_units=admin_units,
            licenses=licenses,
            licenses_open=[lic in OPEN_LICENSE_URIS for lic in licenses],
            access_rights=_multi(graph, dataset_subjects, _ACCESS_RIGHTS),
            publishers=_multi(graph, dataset_subjects, _PUBLISHER),
            contact_points=_multi(graph, dataset_subjects, DCAT.contactPoint),
            distributions=distributions,
        )


# ---------------------------------------------------------------------------
# Helpers (internal)
# ---------------------------------------------------------------------------


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
    for obj in graph.objects(subject, predicate):
        return str(obj)
    return None


def _admin_unit_fact(uri: str) -> AdminUnitFact:
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
    )
