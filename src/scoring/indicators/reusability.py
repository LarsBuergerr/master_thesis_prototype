"""Reusability indicators for DCAT-AP-DE metadata.

Validates aspects like license, access rights, publisher info, etc.
"""

import re
from typing import Any, Iterable, Optional
from urllib.parse import urlparse

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCAT, DCTERMS, FOAF, RDF

from core.indicator import (
    Indicator,
    IndicatorResult,
    IndicatorStatus,
)
from core.dimension import QualityDimension
from extraction.dataset_context import DatasetContext
from extraction.vocabularies import (
    OPEN_LICENSE_URIS,
    RESTRICTED_LICENSE_URIS,
    VALID_ACCESS_RIGHT_URIS,
    VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS,
)

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
DCT_RIGHTS_STATEMENT = DCTERMS.RightsStatement

# Permissive mail-address regex — covers the vast majority of real
# addresses without trying to be RFC-5322 complete. Used after the
# ``mailto:`` prefix has been stripped.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_MAILTO_PREFIX = "mailto:"

# vcard properties that aren't part of the core "must-have" set — each
# present property adds a small bonus to the contact-point score so richer
# metadata is rewarded.
_VCARD_BONUS_PROPERTIES = (
    VCARD.fn,
    VCARD["organization-name"],
    VCARD.hasTelephone,
    VCARD.hasAddress,
    VCARD.hasUID,
    VCARD.role,
    VCARD.title,
    VCARD.note,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _is_valid_email(value: str) -> bool:
    """Check that ``value`` looks like ``mailto:<address>`` with a plausible
    e-mail after the prefix."""
    if not value.startswith(_MAILTO_PREFIX):
        return False
    address = value[len(_MAILTO_PREFIX) :].strip()
    return bool(_EMAIL_RE.match(address))


def _is_valid_url(value: str) -> bool:
    """Check that ``value`` parses as an absolute http(s) URL."""
    try:
        parsed = urlparse(value)
    except ValueError:
        return False
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _objects(graph: Graph, predicate: URIRef) -> Iterable:
    """Yield every object value for the given predicate across the graph.

    Datasets occasionally repeat predicates across multiple subjects
    (Dataset + Distribution); a flat sweep is the simplest way to collect
    all candidates without re-deriving subject lists per indicator.
    """
    for _, _, obj in graph.triples((None, predicate, None)):
        yield obj


# ---------------------------------------------------------------------------
# Indicators
# ---------------------------------------------------------------------------


class LicenseIndicator(Indicator):
    """Validates ``dct:license`` against the DCAT-AP-DE controlled vocabulary.

    Scores:

    * 1.0 — at least one license URI is in the vocab AND classified as
      ``Freie Nutzung`` (free use)
    * 0.5 — at least one license URI is in the vocab but only as
      ``Eingeschränkte Nutzung`` (restricted use)
    * 0.0 — license set but no URI matches the vocab, or no license at all

    Match is against ``skos:exactMatch`` URIs from ``licenses.rdf``. Best
    license across all dataset / distribution declarations wins (the
    indicator is "at least one acceptable license").
    """

    def __init__(self):
        super().__init__(
            indicator_id="reuse_license",
            name_de="Lizenz aus kontrolliertem Vokabular",
            name_en="License from controlled vocabulary",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Prüft ob dct:license eine URI aus dem DCAT-AP-DE-Lizenz-Vokabular "
                "(skos:exactMatch) ist; volle Punkte bei freier Nutzung, halbe bei "
                "eingeschränkter Nutzung"
            ),
            description_en=(
                "Checks that dct:license is a URI from the DCAT-AP-DE licenses vocab "
                "(via skos:exactMatch); full credit for free use, half credit for "
                "restricted use"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            sourced = context.collect_licenses()
            dataset_count = sum(1 for sv in sourced if sv.source_kind == "dataset")
            dist_count = sum(1 for sv in sourced if sv.source_kind == "distribution")

            if not sourced:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no license set"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Lizenz angegeben",
                    message_en="No license specified",
                    details={
                        "license_count": 0,
                        "dataset_count": 0,
                        "distribution_count": 0,
                    },
                )

            classified = []
            for sv in sourced:
                if sv.value in OPEN_LICENSE_URIS:
                    tier = "free"
                    score = 1.0
                elif sv.value in RESTRICTED_LICENSE_URIS:
                    tier = "restricted"
                    score = 0.5
                else:
                    tier = "unknown"
                    score = 0.0
                classified.append(
                    {
                        "value": sv.value,
                        "source_kind": sv.source_kind,
                        "source_uri": sv.source_uri,
                        "tier": tier,
                        "score": score,
                    }
                )

            best = max(c["score"] for c in classified)
            best_tier = next(c["tier"] for c in classified if c["score"] == best)

            if best >= 1.0:
                status = IndicatorStatus.PASS
                message_de = "Freie Lizenz aus dem Vokabular gefunden"
                message_en = "Free-use license from the vocabulary found"
            elif best >= 0.5:
                status = IndicatorStatus.PARTIAL
                message_de = (
                    "Lizenz aus dem Vokabular, aber Nutzung eingeschränkt"
                )
                message_en = "License from the vocabulary but use is restricted"
            else:
                status = IndicatorStatus.FAIL
                message_de = (
                    "Lizenz angegeben, aber URI nicht im kontrollierten Vokabular"
                )
                message_en = (
                    "License specified but URI is not in the controlled vocabulary"
                )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={best:.2f} "
                f"best_tier={best_tier} licenses={len(sourced)} "
                f"(dataset={dataset_count} distribution={dist_count})"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=best,
                message_de=message_de,
                message_en=message_en,
                details={
                    "license_count": len(sourced),
                    "dataset_count": dataset_count,
                    "distribution_count": dist_count,
                    "best_tier": best_tier,
                    "licenses": classified,
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


class AccessRightsIndicator(Indicator):
    """Validates ``dct:accessRights`` against the access-rights vocabularies.

    The value must reference a ``dct:RightsStatement`` whose URI is in
    either ``access-right.rdf`` (EU publications office) or
    ``LimitationsOnPublicAccess.de.rdf`` (INSPIRE limitations). A typing
    triple ``?ar a dct:RightsStatement`` is awarded as a bonus but the
    vocab membership is the load-bearing check — many publishers serialise
    the URI directly without explicit typing.

    Scores:

    * 1.0 — at least one accessRights URI is in either vocab
    * 0.5 — accessRights set but URI not in vocab
    * 0.0 — no accessRights
    """

    def __init__(self):
        super().__init__(
            indicator_id="reuse_access_rights",
            name_de="accessRights mit RightsStatement aus Vokabular",
            name_en="accessRights via RightsStatement from vocabulary",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Prüft ob dct:accessRights gesetzt ist und auf einen "
                "dct:RightsStatement aus access-right.rdf oder "
                "LimitationsOnPublicAccess.de.rdf verweist"
            ),
            description_en=(
                "Checks that dct:accessRights is set and references a "
                "dct:RightsStatement from access-right.rdf or "
                "LimitationsOnPublicAccess.de.rdf"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            graph = context.graph
            valid_uris = (
                VALID_ACCESS_RIGHT_URIS | VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS
            )

            entries: list[dict[str, Any]] = []
            for obj in _objects(graph, DCTERMS.accessRights):
                uri = str(obj)
                in_vocab = uri in valid_uris
                typed = (obj, RDF.type, DCT_RIGHTS_STATEMENT) in graph
                if in_vocab:
                    score = 1.0
                    tier = "in-vocab"
                else:
                    score = 0.5
                    tier = "set-but-unknown"
                entries.append(
                    {
                        "value": uri,
                        "in_vocab": in_vocab,
                        "typed_as_rights_statement": typed,
                        "tier": tier,
                        "score": score,
                    }
                )

            if not entries:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no accessRights set"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein accessRights angegeben",
                    message_en="No accessRights specified",
                    details={"access_rights_count": 0},
                )

            best = max(e["score"] for e in entries)
            best_tier = next(e["tier"] for e in entries if e["score"] == best)

            if best >= 1.0:
                status = IndicatorStatus.PASS
                message_de = "accessRights verweist auf bekannten RightsStatement"
                message_en = "accessRights references a known RightsStatement"
            elif best >= 0.5:
                status = IndicatorStatus.PARTIAL
                message_de = "accessRights gesetzt, aber URI nicht im Vokabular"
                message_en = "accessRights set but URI not in the vocabulary"
            else:
                status = IndicatorStatus.FAIL
                message_de = "accessRights ohne erkennbare RightsStatement"
                message_en = "accessRights without recognisable RightsStatement"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={best:.2f} "
                f"best_tier={best_tier} entries={len(entries)}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=best,
                message_de=message_de,
                message_en=message_en,
                details={
                    "access_rights_count": len(entries),
                    "best_tier": best_tier,
                    "access_rights": entries,
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


class PublisherIndicator(Indicator):
    """Validates ``dct:publisher`` is modelled as a structured ``foaf:Agent``
    with a ``foaf:name``.

    Scores:

    * 1.0 — at least one publisher is typed as ``foaf:Agent`` AND has a
      ``foaf:name`` literal
    * 0.5 — publisher set but missing one of the two requirements
      (e.g. typed but no name, or name but no typing)
    * 0.0 — no publisher

    Best publisher across all declarations wins.
    """

    def __init__(self):
        super().__init__(
            indicator_id="reuse_publisher",
            name_de="Herausgeber als strukturierter Agent",
            name_en="Publisher modelled as structured agent",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Prüft ob dct:publisher als foaf:Agent typisiert ist und "
                "ein foaf:name-Literal trägt"
            ),
            description_en=(
                "Checks that dct:publisher is typed as foaf:Agent and "
                "carries a foaf:name literal"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            graph = context.graph
            entries: list[dict[str, Any]] = []
            for obj in _objects(graph, DCTERMS.publisher):
                typed = (obj, RDF.type, FOAF.Agent) in graph
                names = [str(n) for n in graph.objects(obj, FOAF.name)]
                has_name = bool(names)
                if typed and has_name:
                    score = 1.0
                elif typed or has_name:
                    score = 0.5
                else:
                    score = 0.0
                entries.append(
                    {
                        "value": str(obj),
                        "typed_as_agent": typed,
                        "names": names,
                        "score": score,
                    }
                )

            if not entries:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no publisher set"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein Herausgeber angegeben",
                    message_en="No publisher specified",
                    details={"publisher_count": 0},
                )

            best = max(e["score"] for e in entries)

            if best >= 1.0:
                status = IndicatorStatus.PASS
                message_de = "Herausgeber als foaf:Agent mit foaf:name modelliert"
                message_en = "Publisher modelled as foaf:Agent with foaf:name"
            elif best >= 0.5:
                status = IndicatorStatus.PARTIAL
                message_de = "Herausgeber teilweise strukturiert"
                message_en = "Publisher only partially structured"
            else:
                status = IndicatorStatus.FAIL
                message_de = "Herausgeber ohne Struktur (kein Agent / kein Name)"
                message_en = "Publisher lacks structure (no Agent / no name)"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={best:.2f} "
                f"publishers={len(entries)}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=best,
                message_de=message_de,
                message_en=message_en,
                details={
                    "publisher_count": len(entries),
                    "publishers": entries,
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


class ContactPointIndicator(Indicator):
    """Validates ``dcat:contactPoint`` is a structured ``vcard:Organization``
    with a valid ``vcard:hasEmail`` (``mailto:``) and ``vcard:hasURL``.

    Score composition per contact point:

    * 0.25 — typed as ``vcard:Organization`` (or any ``vcard:Kind`` subclass)
    * 0.25 — at least one ``vcard:hasEmail`` is a valid ``mailto:`` address
    * 0.25 — at least one ``vcard:hasURL`` is a valid http(s) URL
    * up to +0.25 — bonus 0.05 per additional vcard property present
      (``fn``, ``organization-name``, ``hasTelephone``, ``hasAddress``,
      ``hasUID``, ``role``, ``title``, ``note``)

    Best contact point across all declarations wins.
    """

    BASE_TYPE = 0.25
    BASE_EMAIL = 0.25
    BASE_URL = 0.25
    BONUS_PER_FIELD = 0.05
    BONUS_CAP = 0.25
    PASS_THRESHOLD = 0.85
    PARTIAL_THRESHOLD = 0.5

    def __init__(self):
        super().__init__(
            indicator_id="reuse_contact",
            name_de="Kontaktpunkt als vcard:Organization",
            name_en="Contact point as vcard:Organization",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Prüft ob dcat:contactPoint als vcard:Organization mit "
                "vcard:hasEmail (mailto:) und vcard:hasURL modelliert ist; "
                "zusätzliche vcard-Felder erhöhen den Score"
            ),
            description_en=(
                "Checks that dcat:contactPoint is modelled as a vcard:Organization "
                "with vcard:hasEmail (mailto:) and vcard:hasURL; extra vcard "
                "properties increase the score"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            graph = context.graph
            entries: list[dict[str, Any]] = []
            for obj in _objects(graph, DCAT.contactPoint):
                typed = (obj, RDF.type, VCARD.Organization) in graph or (
                    obj,
                    RDF.type,
                    VCARD.Kind,
                ) in graph
                emails = [str(e) for e in graph.objects(obj, VCARD.hasEmail)]
                urls = [str(u) for u in graph.objects(obj, VCARD.hasURL)]
                valid_emails = [e for e in emails if _is_valid_email(e)]
                valid_urls = [u for u in urls if _is_valid_url(u)]
                bonus_fields = [
                    str(prop).rsplit("#", 1)[-1]
                    for prop in _VCARD_BONUS_PROPERTIES
                    if (obj, prop, None) in graph
                ]

                score = 0.0
                if typed:
                    score += self.BASE_TYPE
                if valid_emails:
                    score += self.BASE_EMAIL
                if valid_urls:
                    score += self.BASE_URL
                bonus = min(
                    self.BONUS_CAP, self.BONUS_PER_FIELD * len(bonus_fields)
                )
                score = min(1.0, score + bonus)

                entries.append(
                    {
                        "value": str(obj),
                        "typed_as_vcard": typed,
                        "emails": emails,
                        "valid_emails": valid_emails,
                        "urls": urls,
                        "valid_urls": valid_urls,
                        "bonus_fields": bonus_fields,
                        "score": round(score, 4),
                    }
                )

            if not entries:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no contactPoint set"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Kein Kontaktpunkt angegeben",
                    message_en="No contact point specified",
                    details={"contact_count": 0},
                )

            best = max(e["score"] for e in entries)

            if best >= self.PASS_THRESHOLD:
                status = IndicatorStatus.PASS
            elif best >= self.PARTIAL_THRESHOLD:
                status = IndicatorStatus.PARTIAL
            else:
                status = IndicatorStatus.FAIL

            message_de = (
                f"Bester Kontaktpunkt: Score {best:.2f} "
                f"über {len(entries)} Kontakt(e)"
            )
            message_en = (
                f"Best contact point: score {best:.2f} "
                f"across {len(entries)} contact(s)"
            )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={best:.2f} "
                f"contacts={len(entries)}"
            )

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=best,
                message_de=message_de,
                message_en=message_en,
                details={
                    "contact_count": len(entries),
                    "contacts": entries,
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
_license_indicator = LicenseIndicator()
_access_rights_indicator = AccessRightsIndicator()
_publisher_indicator = PublisherIndicator()
_contact_point_indicator = ContactPointIndicator()
