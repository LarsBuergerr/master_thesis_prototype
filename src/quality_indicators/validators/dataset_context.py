"""Per-dataset facts derived once from the RDF graph.

Several accessibility indicators look at the same data — every
``dcat:Distribution``'s download URL, access URL, declared ``dct:format`` and
``dcat:mediaType``, plus their membership in the EU file-type / IANA media-type
vocabularies. Recomputing this in each indicator wastes work and risks the
indicators drifting out of sync.

This module builds a single ``DatasetContext`` once per validation run:

* ``DistributionFacts``  — RDF-level facts for one distribution (URLs,
  declared formats / media-types, vocabulary membership).
* ``DatasetContext``     — collection of distribution facts plus the source
  graph, with convenience aggregates (any download URL, any format, etc.).

The context contains **no HTTP probe results** — it is cheap to compute and
indicators that need network access (e.g. ``FormatCongruenceIndicator``) do
their own probing on top.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from rdflib import Graph, URIRef
from rdflib.namespace import DCAT, DCTERMS

from quality_indicators.vocabularies import (
    IANA_MEDIA_TYPE_PREFIX,
    VALID_FILE_TYPE_URIS,
    VALID_MEDIA_TYPE_TEMPLATES,
)


@dataclass
class DistributionFacts:
    """RDF-level facts for a single ``dcat:Distribution``."""

    distribution_uri: str
    title: Optional[str] = None
    download_url: Optional[str] = None
    access_url: Optional[str] = None
    # Raw values straight from the graph (may be URIs or literals).
    format_values: list[str] = field(default_factory=list)
    media_type_values: list[str] = field(default_factory=list)
    # Vocabulary membership, parallel to the *_values lists.
    formats_in_vocab: list[bool] = field(default_factory=list)
    media_types_form_valid: list[bool] = field(default_factory=list)
    media_types_in_vocab: list[bool] = field(default_factory=list)

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


@dataclass
class DatasetContext:
    """All distribution-level facts for a dataset graph."""

    graph: Graph
    distributions: list[DistributionFacts] = field(default_factory=list)

    # ------- aggregates (cheap derived properties) ----------------------

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
    def all_format_values(self) -> list[str]:
        return [v for d in self.distributions for v in d.format_values]

    @property
    def all_media_type_values(self) -> list[str]:
        return [v for d in self.distributions for v in d.media_type_values]

    @property
    def distributions_with_download_url(self) -> int:
        return sum(1 for d in self.distributions if d.has_download_url)

    # ------- factory ----------------------------------------------------

    @classmethod
    def from_graph(cls, graph: Graph) -> "DatasetContext":
        distributions = [_facts_from_distribution(graph, dist) for dist in _iter_distributions(graph)]
        return cls(graph=graph, distributions=distributions)


# ---------- helpers (internal) ---------------------------------------------


def _iter_distributions(graph: Graph):
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


def _first_value(graph: Graph, subject: URIRef, predicate) -> Optional[str]:
    for obj in graph.objects(subject, predicate):
        return str(obj)
    return None


def _all_values(graph: Graph, subject: URIRef, predicate) -> list[str]:
    return [str(obj) for obj in graph.objects(subject, predicate)]


def _facts_from_distribution(graph: Graph, distribution: URIRef) -> DistributionFacts:
    format_values = _all_values(graph, distribution, DCTERMS.format)
    media_type_values = _all_values(graph, distribution, DCAT.mediaType)
    return DistributionFacts(
        distribution_uri=str(distribution),
        title=_first_value(graph, distribution, DCTERMS.title),
        download_url=_first_value(graph, distribution, DCAT.downloadURL),
        access_url=_first_value(graph, distribution, DCAT.accessURL),
        format_values=format_values,
        media_type_values=media_type_values,
        formats_in_vocab=[v in VALID_FILE_TYPE_URIS for v in format_values],
        media_types_form_valid=[
            v.startswith(IANA_MEDIA_TYPE_PREFIX) for v in media_type_values
        ],
        media_types_in_vocab=[
            v.startswith(IANA_MEDIA_TYPE_PREFIX)
            and v[len(IANA_MEDIA_TYPE_PREFIX) :] in VALID_MEDIA_TYPE_TEMPLATES
            for v in media_type_values
        ],
    )
