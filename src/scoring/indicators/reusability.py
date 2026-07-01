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
    VALID_CONTRIBUTOR_ID_URIS,
    VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS,
    VALID_PLANNED_AVAILABILITY_URIS,
)

VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")
DCT_RIGHTS_STATEMENT = DCTERMS.RightsStatement

# Permissive mail-address regex — covers the vast majority of real
# addresses without trying to be RFC-5322 complete. Used after the
# ``mailto:`` prefix has been stripped.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_MAILTO_PREFIX = "mailto:"


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
    * 0.0 — otherwise: only ``Eingeschränkte Nutzung`` (restricted use), a URI
      not in the vocab, or no license at all

    A restricted-use license is treated as a FAIL — only free-use licenses earn
    credit. Match is against ``skos:exactMatch`` URIs from ``licenses.rdf``.
    Best license across all distribution declarations wins (the indicator is
    "at least one free-use license").
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

            sourced = [
                sv
                for sv in context.collect_licenses()
                if sv.source_kind == "distribution"
            ]
            dist_count = len(sourced)

            if not sourced:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no distribution license set"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine Lizenz auf Distributionsebene angegeben",
                    message_en="No license specified at distribution level",
                    details={
                        "license_count": 0,
                        "distribution_count": 0,
                    },
                )

            classified = []
            for sv in sourced:
                if sv.value in OPEN_LICENSE_URIS:
                    tier = "free"
                    score = 1.0
                elif sv.value in RESTRICTED_LICENSE_URIS:
                    # Restricted use is not accepted — treated as FAIL.
                    tier = "restricted"
                    score = 0.0
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
            has_free = any(c["tier"] == "free" for c in classified)
            has_restricted = any(c["tier"] == "restricted" for c in classified)

            if has_free:
                status = IndicatorStatus.PASS
                best_tier = "free"
                message_de = "Freie Lizenz aus dem Vokabular gefunden"
                message_en = "Free-use license from the vocabulary found"
            elif has_restricted:
                status = IndicatorStatus.FAIL
                best_tier = "restricted"
                message_de = "Nur eingeschränkte Lizenz — nicht akzeptiert"
                message_en = "Only a restricted-use license — not accepted"
            else:
                status = IndicatorStatus.FAIL
                best_tier = "unknown"
                message_de = (
                    "Lizenz angegeben, aber URI nicht im kontrollierten Vokabular"
                )
                message_en = (
                    "License specified but URI is not in the controlled vocabulary"
                )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={best:.2f} "
                f"best_tier={best_tier} distribution_licenses={len(sourced)}"
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
    """Validates ``dcat:contactPoint`` carries at least one usable contact
    channel — ``vcard:hasEmail`` or ``vcard:hasURL`` — per DCAT-AP.de
    Konvention 01 (contactPoint MUST contain hasEmail OR hasURL).

    Ternary scoring:

    * PASS    — a contactPoint is present and carries at least one valid
      ``vcard:hasEmail`` (``mailto:``) or ``vcard:hasURL`` (http/https)
    * PARTIAL — a contactPoint is present but carries neither a valid email
      nor a valid URL
    * FAIL    — no contactPoint at all

    Best contact point across all declarations wins.
    """

    def __init__(self):
        super().__init__(
            indicator_id="reuse_contact",
            name_de="Kontaktpunkt mit E-Mail oder URL",
            name_en="Contact point with email or URL",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Prüft ob dcat:contactPoint mindestens eine vcard:hasEmail "
                "(mailto:) oder vcard:hasURL trägt (DCAT-AP.de Konvention 01)"
            ),
            description_en=(
                "Checks that dcat:contactPoint carries at least one "
                "vcard:hasEmail (mailto:) or vcard:hasURL (DCAT-AP.de Konvention 01)"
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
                emails = [str(e) for e in graph.objects(obj, VCARD.hasEmail)]
                urls = [str(u) for u in graph.objects(obj, VCARD.hasURL)]
                valid_emails = [e for e in emails if _is_valid_email(e)]
                valid_urls = [u for u in urls if _is_valid_url(u)]
                entries.append(
                    {
                        "value": str(obj),
                        "emails": emails,
                        "valid_emails": valid_emails,
                        "urls": urls,
                        "valid_urls": valid_urls,
                        "has_channel": bool(valid_emails or valid_urls),
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

            with_channel = sum(1 for e in entries if e["has_channel"])

            if with_channel:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Kontaktpunkt mit E-Mail oder URL vorhanden"
                message_en = "Contact point with email or URL present"
            else:
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = "Kontaktpunkt vorhanden, aber ohne valide E-Mail oder URL"
                message_en = "Contact point present but without a valid email or URL"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"contacts={len(entries)} with_channel={with_channel}"
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
                details={
                    "contact_count": len(entries),
                    "contacts_with_channel": with_channel,
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


class ContributorIDIndicator(Indicator):
    """Validates ``dcatde:contributorID`` per DCAT-AP-DE rules K12 & K13.

    The rule is twofold:

    * ``dcatde:contributorID`` **MUST** be present on the ``dcat:Dataset``.
    * It **MAY only** carry exactly one IRI, and that IRI must come from the
      controlled contributors vocabulary
      (``http://dcat-ap.de/def/contributors/``).

    Two independent requirements — cardinality (exactly one) and vocabulary
    membership — so the score reflects which of them is met:

    * 1.0 — exactly one contributorID and it is in the vocabulary
    * 0.5 — set, but only one requirement met: either a single value that is
      not in the vocabulary, or several values that are all in the vocabulary
      (cardinality violated)
    * 0.25 — several values **and** not all of them are in the vocabulary
    * 0.0 — no contributorID at all (MUST violated)
    """

    def __init__(self):
        super().__init__(
            indicator_id="reuse_contributor_id",
            name_de="contributorID aus kontrolliertem Vokabular",
            name_en="contributorID from controlled vocabulary",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Prüft ob dcatde:contributorID gesetzt ist und genau eine IRI "
                "aus http://dcat-ap.de/def/contributors/ verwendet (DCAT-AP-DE K12/K13)"
            ),
            description_en=(
                "Checks that dcatde:contributorID is set and uses exactly one IRI "
                "from http://dcat-ap.de/def/contributors/ (DCAT-AP-DE K12/K13)"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            values = context.contributor_ids
            in_vocab_flags = context.contributor_ids_in_vocab
            count = len(values)

            if count == 0:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no contributorID set"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine contributorID angegeben (MUSS-Anforderung)",
                    message_en="No contributorID specified (mandatory requirement)",
                    details={"contributor_id_count": 0},
                )

            valid = [v for v, ok in zip(values, in_vocab_flags) if ok]
            invalid = [v for v, ok in zip(values, in_vocab_flags) if not ok]

            if count == 1:
                if in_vocab_flags[0]:
                    status = IndicatorStatus.PASS
                    score = 1.0
                    message_de = "Genau eine contributorID aus dem Vokabular"
                    message_en = "Exactly one contributorID from the vocabulary"
                else:
                    status = IndicatorStatus.FAIL
                    score = 0.0
                    message_de = (
                        "contributorID angegeben, aber IRI nicht aus dem "
                        "kontrollierten Vokabular"
                    )
                    message_en = (
                        "contributorID specified but IRI is not from the "
                        "controlled vocabulary"
                    )
            else:
                # count > 1 — Kardinalität verletzt ("DARF nur genau einmal").
                status = IndicatorStatus.FAIL
                score = 0.0

                self.logger.debug(
                    f"[{self.indicator_id}] contributorID cardinality violated: "
                    f"{count} values found"
                )

                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=status,
                    score=score,
                    message_de=(
                        f"Mehrere contributorIDs angegeben ({count}), "
                        "Kardinalität verletzt (DARF nur genau einmal)"
                    ),
                    message_en=(
                        f"Multiple contributorIDs specified ({count}), "
                        "cardinality violated (MUST only be exactly one)"
                    ),
                    details={
                        "contributor_id_count": count,
                        "valid": valid,
                        "invalid": invalid,
                        "values": values,
                    },
                )

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"count={count} valid={len(valid)}/{count}"
            )
            if invalid:
                self.logger.debug(f"[{self.indicator_id}] invalid_values={invalid}")

            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=status,
                score=score,
                message_de=message_de,
                message_en=message_en,
                details={
                    "contributor_id_count": count,
                    "valid": valid,
                    "invalid": invalid,
                    "values": values,
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


class DcatApDeValidationIndicator(Indicator):
    """Validates metadata against DCAT-AP.de SHACL rules via the ITB API.

    Binary scoring only — no partial:
      PASS  — sh:conforms true  (zero violations of any severity)
      FAIL  — at least one sh:ValidationResult
    """

    def __init__(self):
        super().__init__(
            indicator_id="reuse_dcat_ap_de_compliance",
            name_de="DCAT-AP.de Schema-Konformität (SHACL)",
            name_en="DCAT-AP.de schema compliance (SHACL)",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Validiert die Metadaten via ITB SHACL-API gegen DCAT-AP.de v2.0; "
                "PASS bei null Verletzungen, FAIL bei mindestens einer"
            ),
            description_en=(
                "Validates metadata via ITB SHACL API against DCAT-AP.de v2.0; "
                "PASS for zero violations, FAIL for at least one"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            from utils.shacl_client import validate_graph

            result = validate_graph(metadata)
            conforms = result["conforms"]
            violations = result["violations"]

            if conforms:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Keine SHACL-Verletzungen — DCAT-AP.de konform"
                message_en = "No SHACL violations — DCAT-AP.de compliant"
            else:
                status = IndicatorStatus.FAIL
                score = 0.0
                message_de = f"{len(violations)} SHACL-Verletzung(en) gefunden"
                message_en = f"{len(violations)} SHACL violation(s) found"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"conforms={conforms} violations={len(violations)}"
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
                details={
                    "conforms": conforms,
                    "violation_count": len(violations),
                    "violations": violations[:20],
                },
            )

        except Exception as e:
            self.logger.exception(f"[{self.indicator_id}] SHACL validation failed")
            return IndicatorResult(
                indicator_id=self.indicator_id,
                name_de=self.name_de,
                name_en=self.name_en,
                dimension=self.dimension,
                status=IndicatorStatus.ERROR,
                score=0.0,
                message_de="Fehler bei der SHACL-Validierung",
                message_en="SHACL validation error",
                error=str(e),
            )


class AvailabilityIndicator(Indicator):
    """Validates ``dcatap:availability`` against the DCAT-AP Planned Availability
    vocabulary (``planned-availability.rdf``).

    The field is collected from the ``dcat:Dataset`` **and** every
    ``dcat:Distribution`` and evaluated together in a single indicator.

    * PASS    — availability present and every value is in the vocabulary
    * PARTIAL — availability present but at least one value is not in the vocabulary
    * FAIL    — no availability set anywhere
    """

    def __init__(self):
        super().__init__(
            indicator_id="reuse_availability",
            name_de="Verfügbarkeit aus kontrolliertem Vokabular",
            name_en="Availability from controlled vocabulary",
            dimension=QualityDimension.REUSABILITY,
            description_de=(
                "Prüft ob dcatap:availability (Dataset und Distributionen) aus dem "
                "Planned-Availability-Vokabular stammt"
            ),
            description_en=(
                "Checks that dcatap:availability (dataset and distributions) is from "
                "the Planned Availability vocabulary"
            ),
            weight=1.0,
        )

    def validate(
        self, metadata: Any, context: Optional[DatasetContext] = None
    ) -> IndicatorResult:
        try:
            if context is None:
                context = DatasetContext.from_graph(metadata)

            entries: list[dict[str, Any]] = []
            for value in context.availability:
                entries.append({"value": value, "source": "dataset"})
            for dist in context.distributions:
                for value in dist.availability:
                    entries.append(
                        {
                            "value": value,
                            "source": "distribution",
                            "distribution_uri": dist.distribution_uri,
                        }
                    )

            if not entries:
                self.logger.info(
                    f"[{self.indicator_id}] FAIL score=0.00 no dcatap:availability"
                )
                return IndicatorResult(
                    indicator_id=self.indicator_id,
                    name_de=self.name_de,
                    name_en=self.name_en,
                    dimension=self.dimension,
                    status=IndicatorStatus.FAIL,
                    score=0.0,
                    message_de="Keine dcatap:availability angegeben",
                    message_en="No dcatap:availability specified",
                    details={"availability_count": 0},
                )

            for e in entries:
                e["in_vocab"] = e["value"] in VALID_PLANNED_AVAILABILITY_URIS
            valid = [e for e in entries if e["in_vocab"]]
            invalid = [e for e in entries if not e["in_vocab"]]

            if not invalid:
                status = IndicatorStatus.PASS
                score = 1.0
                message_de = "Alle Verfügbarkeitswerte aus dem Vokabular"
                message_en = "All availability values from the vocabulary"
            else:
                status = IndicatorStatus.PARTIAL
                score = 0.5
                message_de = "Nicht alle Verfügbarkeitswerte aus dem Vokabular"
                message_en = "Not all availability values from the vocabulary"

            self.logger.info(
                f"[{self.indicator_id}] {status.value} score={score:.2f} "
                f"valid={len(valid)}/{len(entries)}"
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
                details={
                    "availability_count": len(entries),
                    "valid_count": len(valid),
                    "invalid_count": len(invalid),
                    "entries": entries,
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
_contributor_id_indicator = ContributorIDIndicator()
_dcat_ap_de_validation = DcatApDeValidationIndicator()
_availability_indicator = AvailabilityIndicator()
