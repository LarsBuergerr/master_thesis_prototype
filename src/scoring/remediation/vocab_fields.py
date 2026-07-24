"""Generic ready/needs-input resolution for a single controlled-vocabulary
field (predicate) on one RDF subject.

Shared by every dataset- and distribution-level vocabulary indicator so the
"remove the invalid value(s), then ask for a valid one if none is left"
logic lives in exactly one place instead of once per indicator.
"""

from __future__ import annotations

import difflib
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


def _local_name(uri: str) -> str:
    """Letztes Pfad-/Fragment-Segment einer URI."""
    return uri.rstrip("/#").replace("#", "/").rsplit("/", 1)[-1]


#: Ab welcher Ähnlichkeit ein Treffer als „gemeint" gilt. Bewusst nahe an 1.0:
#: eine Sortierung, die den falschen Wert nach vorn stellt, ist schlechter als
#: gar keine — sie liest sich wie eine Empfehlung.
_RANK_THRESHOLD = 0.85


def rank_candidates(
    candidates: list[str], current_values: list[str]
) -> tuple[list[str], bool]:
    """Vokabular-Einträge nach Nähe zu den bereits eingetragenen Werten sortieren.

    Liefert die Liste und ob tatsächlich sortiert wurde — nur dann darf eine
    Oberfläche den ersten Eintrag als Vorschlag vorbelegen.

    Ein kontrolliertes Vokabular hat schnell mehrere hundert bis tausend
    Einträge (IANA-Media-Types). Alphabetisch sortiert hilft das niemandem —
    steht im Metadatensatz ``SHP``, ist ``…/file-type/SHP`` gemeint. Die
    Sortierung stellt den wahrscheinlichsten Kandidaten nach vorn, damit
    Oberflächen ihn als Vorschlag zeigen können, ohne selbst raten zu müssen.

    Findet sich kein nahezu deckungsgleicher Eintrag, bleibt die Reihenfolge
    unverändert: dann kennt das Vokabular den vorhandenen Wert schlicht nicht
    (``x-gis/x-shapefile`` ist kein IANA-Typ), und ein „ähnlichster" Treffer
    wäre geraten.
    """
    hints = [_local_name(v).lower() for v in current_values if v]
    if not hints:
        return candidates, False

    def score(uri: str) -> float:
        tail = _local_name(uri).lower()
        return max(difflib.SequenceMatcher(None, tail, hint).ratio() for hint in hints)

    scored = sorted(candidates, key=score, reverse=True)
    if scored and score(scored[0]) >= _RANK_THRESHOLD:
        return scored, True
    return candidates, False


def vocab_change_patch(
    graph: Graph,
    subject: Identifier,
    vfield: VocabField,
    indicator_id: str,
    extra_hints: Optional[list[str]] = None,
) -> Optional[ChangePatch]:
    """``ready``: remove values not in the vocabulary. ``needs_input``: if no
    valid value remains afterwards, offer the vocabulary as candidates.

    Returns ``None`` when this generic logic has nothing to say — e.g. a
    cardinality-only fail where every present value is individually valid
    (multiple contributorIDs, each a real vocab URI). Callers fall back to a
    plain-text recommendation in that case.

    ``extra_hints``: weitere Werte desselben Objekts (Format-Literal,
    Dateiendung der URL), nach denen die Kandidaten sortiert werden, wenn das
    Feld selbst leer ist — dann gibt es keinen eigenen Wert, an dem sich die
    Sortierung orientieren könnte.
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
        # Nach Aehnlichkeit zum aktuell eingetragenen Wert sortiert, damit der
        # erste Kandidat der wahrscheinlich gemeinte ist. ``ranked`` sagt, ob
        # das gelungen ist -- nur dann taugt er als Vorschlag.
        candidates, ranked = rank_candidates(
            sorted(vfield.valid_uris),
            [str(o) for o in current] or list(extra_hints or []),
        )
        needs_input.append(
            FieldSuggestion(
                indicator_id, subject, vfield.predicate,
                candidates=candidates,
                reason=f"{indicator_id}: gueltigen Wert aus dem Vokabular waehlen",
                ranked=ranked,
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
