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

from core.remediation import ChangeOp, ChangePatch, FieldSuggestion


@dataclass(frozen=True)
class VocabField:
    """A dataset/distribution field whose value must come from a fixed,
    small controlled vocabulary (indicator pattern: PASS in vocab /
    PARTIAL or FAIL otherwise)."""

    predicate: URIRef
    valid_uris: frozenset[str]


def vocab_change_patch(
    graph: Graph, subject: Identifier, vfield: VocabField, indicator_id: str
) -> Optional[ChangePatch]:
    """``ready``: remove values not in the vocabulary. ``needs_input``: if no
    valid value remains afterwards, offer the vocabulary as candidates.

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
    needs_input = (
        [FieldSuggestion(
            indicator_id, subject, vfield.predicate,
            candidates=sorted(vfield.valid_uris),
            reason=f"{indicator_id}: gueltigen Wert aus dem Vokabular waehlen",
        )]
        if still_missing else []
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
