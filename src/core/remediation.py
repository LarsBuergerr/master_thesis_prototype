"""Structured remediation attached to FAIL/PARTIAL IndicatorResults.

Two shapes, chosen per indicator:

- ``ChangePatch``    — a concrete fix. ``ready`` ops can be applied as-is;
  ``needs_input`` names a location that still needs a human-supplied value and
  describes the *form* that value must have (see :class:`FieldSuggestion`).
- ``Recommendation`` — free-text guidance, for everything where no
  automatic vocabulary-backed fix exists (real content, LLM judgement,
  reachability, ...).

Every FAIL/PARTIAL result gets one or the other -- never neither -- so a
frontend can render *something* for every failing indicator without
special-casing per indicator_id (see ``scoring.remediation.attach_remediation``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional, Union

from rdflib import Literal as RdfLiteral, URIRef
from rdflib.term import Identifier


def _term_to_dict(term: Identifier) -> dict:
    """JSON-serialisable view of an RDF term that keeps enough type
    information to reconstruct it later (URIRef vs. Literal vs. blank node)."""
    if isinstance(term, URIRef):
        kind = "uri"
    elif isinstance(term, RdfLiteral):
        kind = "literal"
    else:
        kind = "bnode"
    return {"type": kind, "value": str(term)}


@dataclass(frozen=True)
class ChangeOp:
    """One triple-level operation, ready to apply as-is (subject/predicate =
    location in the graph, object = the value to add or remove)."""

    op: Literal["add", "remove"]
    subject: Identifier
    predicate: Identifier
    object: Identifier
    reason: str = ""

    def to_dict(self) -> dict:
        return {
            "op": self.op,
            "subject": str(self.subject),
            "predicate": str(self.predicate),
            "object": _term_to_dict(self.object),
            "reason": self.reason,
        }


@dataclass(frozen=True)
class FieldSuggestion:
    """A known location in the graph that needs a value a human must supply.

    Beschrieben wird die **Form** des erwarteten Werts, nicht die Menge der
    zulässigen Werte: ein kontrolliertes Vokabular hat schnell mehrere tausend
    Einträge (IANA-Media-Types), und diese Liste mitzuschleppen bläht jedes
    Ergebnis auf, ohne dass sie jemand durchsieht. Wer den Wert einträgt,
    braucht die Stelle (``predicate``), das erwartete Format (``expected_de``)
    und ein Beispiel für die Schreibweise (``example``) — die vollständige
    Liste steht im verlinkten Vokabular (``vocabulary_url``).
    """

    indicator_id: str
    subject: Identifier
    predicate: Identifier
    reason: str = ""
    #: Erwartete Form in einem Satz, z. B. „URI aus dem EU-Vokabular
    #: Dateiformate".
    expected_de: str = ""
    expected_en: str = ""
    #: Ein Wert, der die Schreibweise zeigt — ausdrücklich ein Formbeispiel und
    #: keine inhaltliche Empfehlung.
    example: Optional[str] = None
    #: Das maßgebliche Vokabular, in dem die zulässigen Werte nachzuschlagen sind.
    vocabulary_label: Optional[str] = None
    vocabulary_url: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "indicator_id": self.indicator_id,
            "subject": str(self.subject),
            "predicate": str(self.predicate),
            "reason": self.reason,
            "expected_de": self.expected_de,
            "expected_en": self.expected_en,
            "example": self.example,
            "vocabulary_label": self.vocabulary_label,
            "vocabulary_url": self.vocabulary_url,
        }


@dataclass(frozen=True)
class ChangePatch:
    """Structured fix: at least one of ``ready`` / ``needs_input`` is set."""

    ready: list[ChangeOp] = field(default_factory=list)
    needs_input: list[FieldSuggestion] = field(default_factory=list)
    summary_de: str = ""
    summary_en: str = ""
    kind: Literal["change_patch"] = "change_patch"

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "ready": [c.to_dict() for c in self.ready],
            "needs_input": [s.to_dict() for s in self.needs_input],
            "summary_de": self.summary_de,
            "summary_en": self.summary_en,
        }


@dataclass(frozen=True)
class Recommendation:
    """Free-text guidance when no structural patch can be derived."""

    message_de: str = ""
    message_en: str = ""
    findings: list[str] = field(default_factory=list)
    see_also: list[str] = field(default_factory=list)
    kind: Literal["recommendation"] = "recommendation"

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "message_de": self.message_de,
            "message_en": self.message_en,
            "findings": list(self.findings),
            "see_also": list(self.see_also),
        }


Remediation = Union[ChangePatch, Recommendation]
