"""Befund zu einem nicht erfüllten Indikator.

``details`` eines Indikator-Ergebnisses enthält die Belege der Prüfung
(``per_distribution``, ``violations``, ``keywords`` …) — technisch vollständig,
aber pro Indikator anders geformt und damit für eine Oberfläche nicht direkt
verwendbar. Ein :class:`Finding` bringt genau diese Belege in eine einheitliche,
für Menschen lesbare Form:

    headline  – ein Satz, der das Problem benennt
    current   – was aktuell im Metadatensatz steht, mit Fundstelle
    target    – wie es aussehen müsste
    notes     – Einzelbefunde (tote Links, Schema-Verstöße, LLM-Kritik)

Gebaut wird er in :mod:`scoring.findings`, angehängt an
:attr:`core.indicator.IndicatorResult.finding`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

#: Bewertung einer einzelnen Ist-Angabe — steuert die farbliche Auszeichnung.
Tone = str  # "bad" | "warn" | "good" | "neutral"


@dataclass
class FactLine:
    """Eine Ist-Angabe aus dem Metadatensatz."""

    label: str
    value: str
    tone: Tone = "neutral"
    #: Fundstelle, an der der Wert steht (Distributions-URI, SHACL-Pfad …).
    where: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label": self.label,
            "value": self.value,
            "tone": self.tone,
            "where": self.where,
        }


@dataclass
class Finding:
    """Aufbereiteter Befund eines FAIL/PARTIAL-Indikators."""

    headline: str
    current: List[FactLine] = field(default_factory=list)
    target: Optional[str] = None
    notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "headline": self.headline,
            "current": [c.to_dict() for c in self.current],
            "target": self.target,
            "notes": self.notes,
        }
