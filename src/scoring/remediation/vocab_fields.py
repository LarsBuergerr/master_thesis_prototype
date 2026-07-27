"""Generic ready/needs-input resolution for a single controlled-vocabulary
field (predicate) on one RDF subject.

Shared by every dataset- and distribution-level vocabulary indicator so the
"remove the invalid value(s), then ask for a valid one if none is left"
logic lives in exactly one place instead of once per indicator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from rdflib import Graph
from rdflib.namespace import URIRef
from rdflib.term import Identifier

from core.guidance import guidance_for
from core.remediation import ChangeOp, ChangePatch, FieldSuggestion


@dataclass(frozen=True)
class VocabField:
    """A dataset/distribution field whose value must come from a fixed,
    small controlled vocabulary (indicator pattern: PASS in vocab /
    PARTIAL or FAIL otherwise)."""

    predicate: URIRef
    valid_uris: frozenset[str]


def _local_name(uri: str) -> str:
    """Letztes Pfad-/Fragment-Segment einer URI."""
    return uri.rstrip("/#").replace("#", "/").rsplit("/", 1)[-1]


def _syntax_example(valid_uris: frozenset[str]) -> Optional[str]:
    """Ein Eintrag des Vokabulars, der die Schreibweise zeigt.

    Gewählt wird der mit dem kürzesten lokalen Namen (bei Gleichstand
    alphabetisch) — kurz und damit gut lesbar, und vor allem deterministisch:
    das Beispiel soll die *Form* belegen (``…/file-type/CSV``) und darf nicht
    wie eine inhaltliche Empfehlung wirken, die sich von Lauf zu Lauf ändert.

    Einbuchstabige Kürzel (``file-type/Z``) sind zwar am kürzesten, taugen aber
    schlecht als Muster; ab drei Zeichen sieht ein Eintrag wie ein echter Wert
    aus. Gibt es keinen solchen, zählt wieder die reine Länge.
    """
    if not valid_uris:
        return None
    readable = {uri for uri in valid_uris if len(_local_name(uri)) >= 3}
    return min(readable or valid_uris, key=lambda uri: (len(_local_name(uri)), uri))


def _expected_text(indicator_id: str) -> tuple[str, str, Optional[str], Optional[str]]:
    """Erwartete Form plus Vokabular-Verweis, aus der Guidance des Indikators."""
    guidance = guidance_for(indicator_id)
    vocab = guidance.vocabulary if guidance else None
    if vocab is not None:
        return (
            f"URI aus dem kontrollierten Vokabular „{vocab.label_de}“",
            f"URI from the controlled vocabulary “{vocab.label_de}”",
            vocab.label_de,
            vocab.url,
        )
    return (
        "URI aus dem für dieses Feld vorgeschriebenen Vokabular",
        "URI from the vocabulary prescribed for this field",
        None,
        None,
    )


def vocab_change_patch(
    graph: Graph,
    subject: Identifier,
    vfield: VocabField,
    indicator_id: str,
) -> Optional[ChangePatch]:
    """``ready``: remove values not in the vocabulary. ``needs_input``: if no
    valid value remains afterwards, name the field and the form its value needs.

    Returns ``None`` when this generic logic has nothing to say — e.g. a
    cardinality-only fail where every present value is individually valid
    (multiple contributorIDs, each a real vocab URI). Callers fall back to a
    plain-text recommendation in that case.
    """
    current = list(graph.objects(subject, vfield.predicate))
    invalid = [o for o in current if str(o) not in vfield.valid_uris]

    ready = [
        ChangeOp(
            "remove", subject, vfield.predicate, o,
            reason=f"{indicator_id}: Wert nicht im kontrollierten Vokabular",
        )
        for o in invalid
    ]

    still_missing = len(invalid) == len(current)  # kein gueltiger Wert uebrig
    needs_input = []
    if still_missing:
        expected_de, expected_en, vocab_label, vocab_url = _expected_text(indicator_id)
        needs_input.append(
            FieldSuggestion(
                indicator_id, subject, vfield.predicate,
                reason=f"{indicator_id}: gueltigen Wert aus dem Vokabular eintragen",
                expected_de=expected_de,
                expected_en=expected_en,
                example=_syntax_example(vfield.valid_uris),
                vocabulary_label=vocab_label,
                vocabulary_url=vocab_url,
            )
        )

    if not ready and not needs_input:
        return None

    return ChangePatch(
        ready=ready,
        needs_input=needs_input,
        summary_de=(
            f"{len(ready)} ungueltige(r) Wert(e) entfernbar"
            + (" · gueltiger Wert erforderlich" if needs_input else "")
        ),
        summary_en=(
            f"{len(ready)} invalid value(s) removable"
            + (" · a valid value is required" if needs_input else "")
        ),
    )
