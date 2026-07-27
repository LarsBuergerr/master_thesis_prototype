"""Per-indicator remediation resolvers.

Only registers a resolver where a structured ``ChangePatch`` (or, for
expressiveness/SHACL, a richer ``Recommendation``) can be derived
mechanically from already-available data — no LLM calls, no HTTP calls, no
guessing at "the right value". Every other FAIL/PARTIAL indicator falls back
to a plain ``Recommendation`` built from its own message
(see ``scoring.remediation.attach_remediation``), so every indicator says
*something*, but only some get an actual patch.
"""

from __future__ import annotations

from typing import Callable, Optional

from rdflib.namespace import DCAT, DCTERMS
from rdflib.term import URIRef

from core.indicator import IndicatorResult
from core.remediation import ChangeOp, ChangePatch, Recommendation, Remediation
from extraction.dataset_context import DCATAP, DCATDE, DatasetContext
from extraction.vocabularies import (
    VALID_ACCESS_RIGHT_URIS,
    VALID_CONTRIBUTOR_ID_URIS,
    VALID_FILE_TYPE_URIS,
    VALID_FREQUENCY_URIS,
    VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS,
    VALID_MEDIA_TYPE_URIS,
    VALID_PLANNED_AVAILABILITY_URIS,
    VALID_POLITICAL_GEOCODING_LEVEL_URIS,
    VALID_THEME_URIS,
    get_geocoding_vocabulary_for_uri,
)
from scoring.remediation.vocab_fields import VocabField, vocab_change_patch

Resolver = Callable[[DatasetContext, IndicatorResult], Optional[Remediation]]

# --- Tier A: dataset-level controlled-vocabulary fields --------------------

_DATASET_VOCAB_FIELDS: dict[str, VocabField] = {
    "find_theme_valid": VocabField(DCAT.theme, VALID_THEME_URIS),
    "find_accrual_periodicity": VocabField(
        DCTERMS.accrualPeriodicity, VALID_FREQUENCY_URIS
    ),
    "find_geocoding_level": VocabField(
        DCATDE.politicalGeocodingLevelURI, VALID_POLITICAL_GEOCODING_LEVEL_URIS
    ),
    "reuse_contributor_id": VocabField(
        DCATDE.contributorID, VALID_CONTRIBUTOR_ID_URIS
    ),
    # Also accepts the INSPIRE LimitationsOnPublicAccess vocab as a fallback
    # (see reusability.AccessRightsIndicator) -- the union avoids flagging
    # those values as invalid.
    "reuse_access_rights": VocabField(
        DCTERMS.accessRights,
        VALID_ACCESS_RIGHT_URIS | VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS,
    ),
}


def _resolve_dataset_vocab_field(
    context: DatasetContext, result: IndicatorResult
) -> Optional[ChangePatch]:
    if context.dataset_uri is None:
        return None
    vfield = _DATASET_VOCAB_FIELDS[result.indicator_id]
    subject = URIRef(context.dataset_uri)
    return vocab_change_patch(context.graph, subject, vfield, result.indicator_id)


# --- Tier A': same pattern, one field per distribution ---------------------

_DISTRIBUTION_VOCAB_FIELDS: dict[str, VocabField] = {
    "acc_format": VocabField(DCTERMS.format, VALID_FILE_TYPE_URIS),
    "acc_media_type": VocabField(DCAT.mediaType, VALID_MEDIA_TYPE_URIS),
    "reuse_availability": VocabField(
        DCATAP.availability, VALID_PLANNED_AVAILABILITY_URIS
    ),
}


def _resolve_distribution_vocab_field(
    context: DatasetContext, result: IndicatorResult
) -> Optional[ChangePatch]:
    vfield = _DISTRIBUTION_VOCAB_FIELDS[result.indicator_id]
    ready: list[ChangeOp] = []
    needs_input = []
    for dist in context.distributions:
        patch = vocab_change_patch(
            context.graph,
            URIRef(dist.distribution_uri),
            vfield,
            result.indicator_id,
        )
        if patch is None:
            continue
        ready += patch.ready
        needs_input += patch.needs_input

    if not ready and not needs_input:
        return None

    return ChangePatch(
        ready=ready,
        needs_input=needs_input,
        summary_de=(
            f"{len(ready)} ungueltige(r) Wert(e) entfernbar"
            + (f" · {len(needs_input)} Distribution(en) brauchen einen Wert" if needs_input else "")
        ),
        summary_en=(
            f"{len(ready)} invalid value(s) removable"
            + (f" · {len(needs_input)} distribution(s) need a value" if needs_input else "")
        ),
    )


# --- Tier A'': political geocoding -- ready-only, vocabulary is too large --
# (~11k municipality keys) to offer as a picklist, so no needs_input.


def _resolve_political_geocoding(
    context: DatasetContext, result: IndicatorResult
) -> Optional[ChangePatch]:
    if context.dataset_uri is None:
        return None
    subject = URIRef(context.dataset_uri)
    ready = []
    for o in context.graph.objects(subject, DCATDE.politicalGeocodingURI):
        _, valid_uris = get_geocoding_vocabulary_for_uri(str(o))
        if valid_uris is not None and str(o) not in valid_uris:
            ready.append(ChangeOp(
                "remove", subject, DCATDE.politicalGeocodingURI, o,
                reason="find_political_geocoding: URI nicht im dcat-ap.de Vokabular",
            ))
    if not ready:
        return None
    return ChangePatch(
        ready=ready,
        summary_de=f"{len(ready)} ungueltige Geocoding-URI(s) entfernbar",
        summary_en=f"{len(ready)} invalid geocoding URI(s) removable",
    )


# --- Tier B: expressiveness -- reuse the LLM's own reasoning/findings ------

_EXPR_CRITERIA: dict[str, str] = {
    "expr_title_quality": "title_quality",
    "expr_description_quality": "description_quality",
    "expr_title_description_coherence": "title_description_coherence",
    "expr_keyword_quality": "keyword_quality",
    "expr_thematic_consistency": "thematic_consistency",
    "expr_contextual_qualifiers": "contextual_qualifiers",
}


def _resolve_expressiveness(
    context: DatasetContext, result: IndicatorResult
) -> Optional[Recommendation]:
    assessment = context.semantic_assessment
    if assessment is None:
        return None
    crit = getattr(assessment, _EXPR_CRITERIA[result.indicator_id])
    return Recommendation(
        message_de=crit.reasoning,
        message_en=crit.reasoning,
        findings=list(crit.findings),
    )


# --- Tier C: SHACL compliance -- turn violations into readable findings ----


def _resolve_shacl_compliance(
    context: DatasetContext, result: IndicatorResult
) -> Optional[Recommendation]:
    violations = (result.details or {}).get("violations") or []
    if not violations:
        return None
    findings = [str(v.get("message") or v) for v in violations[:10]]
    return Recommendation(
        message_de=f"{len(violations)} SHACL-Verletzung(en) gegen DCAT-AP.de gefunden",
        message_en=f"{len(violations)} SHACL violation(s) against DCAT-AP.de found",
        findings=findings,
    )


# --- Registry ----------------------------------------------------------------

RESOLVERS: dict[str, Resolver] = {}
RESOLVERS.update({k: _resolve_dataset_vocab_field for k in _DATASET_VOCAB_FIELDS})
RESOLVERS.update(
    {k: _resolve_distribution_vocab_field for k in _DISTRIBUTION_VOCAB_FIELDS}
)
RESOLVERS["find_political_geocoding"] = _resolve_political_geocoding
RESOLVERS.update({k: _resolve_expressiveness for k in _EXPR_CRITERIA})
RESOLVERS["reuse_dcat_ap_de_compliance"] = _resolve_shacl_compliance
