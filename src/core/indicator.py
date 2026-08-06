"""Base indicator model and result classes."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
from datetime import datetime

from core.dimension import QualityDimension
from core.finding import Finding
from core.guidance import IndicatorGuidance, guidance_for
from utils.logger import get_logger


class IndicatorStatus(Enum):
    """Status of an indicator validation."""

    PASS = "pass"
    FAIL = "fail"
    PARTIAL = "partial"
    NOT_APPLICABLE = "not_applicable"
    ERROR = "error"


@dataclass
class IndicatorResult:
    """Result of a single indicator validation."""

    indicator_id: str
    name_de: str
    name_en: str
    dimension: QualityDimension
    status: IndicatorStatus
    score: float  # 0.0 to 1.0
    message_de: str = ""
    message_en: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    #: Set (post-hoc, see scoring.findings.attach_finding) for FAIL / PARTIAL /
    #: ERROR results: ``details`` aufbereitet als Ist-/Soll-Gegenüberstellung.
    finding: Optional[Finding] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "indicator_id": self.indicator_id,
            "name_de": self.name_de,
            "name_en": self.name_en,
            "dimension": self.dimension.value,
            "status": self.status.value,
            "score": self.score,
            "message_de": self.message_de,
            "message_en": self.message_en,
            "details": self.details,
            "error": self.error,
            "timestamp": self.timestamp.isoformat(),
            "finding": self.finding.to_dict() if self.finding else None,
        }


class Indicator(ABC):
    """Base class for all quality indicators.

    Each indicator:
    - Belongs to one quality dimension
    - Has a unique identifier
    - Validates a specific aspect of DCAT-AP-DE metadata
    - Produces a score (0.0 to 1.0)
    - Can be partially applicable (not all datasets have all fields)
    """

    # Registry to store all indicators
    _registry: Dict[str, "Indicator"] = {}

    #: Whether this indicator emits continuous / multi-tier scores (as opposed
    #: to a ternary PASS=1.0 / PARTIAL / FAIL=0.0 pattern). Under a
    #: ``ScorePolicy`` graded indicators always contribute their raw continuous
    #: score regardless of status (the PASS / PARTIAL / FAIL label is
    #: presentational), so the aggregate score stays cliff-free; only an
    #: explicit per-indicator ``fail_score`` override can penalise a FAIL.
    #: Override to ``True`` in graded subclasses.
    GRADED: bool = False

    def __init__(
        self,
        indicator_id: str,
        name_de: str,
        name_en: str,
        dimension: QualityDimension,
        description_de: str = "",
        description_en: str = "",
        weight: float = 1.0,
    ):
        """Initialize an indicator.

        Args:
            indicator_id: Unique identifier (e.g., "find_keywords_count")
            name_de: German name
            name_en: English name
            dimension: The quality dimension
            description_de: German description of what is validated
            description_en: English description
            weight: Weight in scoring (1.0 by default)
        """
        self.indicator_id = indicator_id
        self.name_de = name_de
        self.name_en = name_en
        self.dimension = dimension
        self.description_de = description_de
        self.description_en = description_en
        self.weight = weight
        self.logger = get_logger(f"scoring.indicator.{self.indicator_id}")

        # Auto-register the indicator
        self._register()

    def _register(self) -> None:
        """Register this indicator in the global registry."""
        if self.indicator_id in self._registry:
            raise ValueError(
                f"Indicator with ID '{self.indicator_id}' is already registered"
            )
        self._registry[self.indicator_id] = self

    @property
    def guidance(self) -> Optional[IndicatorGuidance]:
        """Klartext-Beschreibung für Endnutzer (Name, Feld, Handlungsanweisung).

        Die Texte liegen als Beiwagen-Registry in :mod:`core.guidance`, damit
        die 27 Indikator-Konstruktoren unverändert bleiben — über diese
        Property hängen sie trotzdem am Indikator und werden von
        ``GET /indicators`` mit ausgeliefert.
        """
        return guidance_for(self.indicator_id)

    @classmethod
    def get(cls, indicator_id: str) -> Optional["Indicator"]:
        """Get an indicator by ID from the registry."""
        return cls._registry.get(indicator_id)

    @classmethod
    def all(cls) -> Dict[str, "Indicator"]:
        """Get all registered indicators."""
        return cls._registry.copy()

    @classmethod
    def by_dimension(cls, dimension: QualityDimension) -> Dict[str, "Indicator"]:
        """Get all indicators for a specific dimension."""
        return {
            ind_id: ind
            for ind_id, ind in cls._registry.items()
            if ind.dimension == dimension
        }

    @abstractmethod
    def validate(self, metadata: Any) -> IndicatorResult:
        """Validate the indicator against metadata.

        Args:
            metadata: The metadata to validate (rdflib Graph or dict)

        Returns:
            IndicatorResult with validation result
        """
        pass

    def __repr__(self) -> str:
        return f"<Indicator {self.indicator_id}: {self.name_de}>"
