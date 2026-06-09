"""Configurable status → score mapping.

Indicators emit two things: a ``status`` (PASS / PARTIAL / FAIL / …) and a raw
numeric ``score``. By default the service uses the raw score directly. A
:class:`ScorePolicy` lets an operator *re-derive* the numeric score from the
status, so the points awarded for PASS / PARTIAL / FAIL become tunable from the
Hydra config — without touching any indicator.

Design (agreed with the thesis author):

* **Ternary indicators** (PASS=1.0 / one PARTIAL level / FAIL=0.0 — the
  majority) are fully governed by the policy: PASS → ``pass_score``,
  PARTIAL → ``partial_score``, FAIL → ``fail_score``.
* **Graded indicators** (``Indicator.GRADED = True`` — continuous or multi-tier
  scores such as the LLM expressiveness criteria, ``acc_machine_readable_access``
  tiers, ``acc_format_congruence``, ``reuse_contributor_id``) keep their *raw*
  score for PASS / PARTIAL so their fine gradation is preserved. ``fail_score``
  still applies to them when the status is FAIL, so a negative-penalty policy
  works uniformly.
* ``allow_partial = False`` collapses every PARTIAL to FAIL (strict mode: only a
  full PASS earns credit).
* ``fail_score`` may be **negative** to actively penalise failures.
* NOT_APPLICABLE / ERROR results are never remapped — they keep their raw score.

Everything is overridable per indicator id, mirroring ``indicator_weights``.

The policy is **opt-in**: :meth:`from_config` returns ``None`` when the config
has no ``scoring`` block, in which case the service uses raw scores (fully
backward compatible with existing configs).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from core.indicator import IndicatorStatus

# Statuses the policy is allowed to remap. NOT_APPLICABLE / ERROR are left
# untouched — penalising "no LLM available" with a negative fail score would be
# wrong.
_REMAPPABLE = {
    IndicatorStatus.PASS,
    IndicatorStatus.PARTIAL,
    IndicatorStatus.FAIL,
}


@dataclass(frozen=True)
class ScorePolicy:
    """A status → score mapping with optional per-indicator overrides."""

    pass_score: float = 1.0
    partial_score: float = 0.5
    fail_score: float = 0.0
    allow_partial: bool = True
    #: Per-indicator overrides, e.g. ``{"find_keywords_count": {"partial_score": 0.7}}``.
    #: Any of the four keys above may appear in an override dict.
    overrides: Dict[str, Dict[str, Any]] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        # frozen dataclass: assign through object.__setattr__
        if self.overrides is None:
            object.__setattr__(self, "overrides", {})

    def _param(self, indicator_id: str, key: str) -> Any:
        """Resolve a single parameter for ``indicator_id`` (override → global).

        A ``None`` value in an override means "not set" (e.g. a serialised
        ``ScoringOverride`` carries explicit ``None`` for unspecified fields),
        so it falls through to the global value rather than overriding with
        ``None``.
        """
        override = self.overrides.get(indicator_id)
        if override is not None and override.get(key) is not None:
            return override[key]
        return getattr(self, key)

    def evaluate(
        self,
        indicator_id: str,
        status: IndicatorStatus,
        raw_score: float,
        graded: bool,
    ) -> tuple[IndicatorStatus, float]:
        """Return the effective ``(status, score)`` for one indicator result.

        The status is remapped too — not just the score — so the output
        reflects the policy decision. In strict mode (``allow_partial=False``) a
        PARTIAL becomes a genuine FAIL (status *and* score), instead of leaving
        a misleading "partial / 0.5" in the result.

        Args:
            indicator_id: indicator id (for per-indicator overrides)
            status: the indicator's emitted status
            raw_score: the indicator's own computed score
            graded: ``True`` if the indicator emits continuous / multi-tier
                scores (``Indicator.GRADED``); such indicators keep their raw
                score for PASS / PARTIAL.
        """
        if status not in _REMAPPABLE:
            # NOT_APPLICABLE / ERROR — leave as the indicator reported it.
            return status, raw_score

        allow_partial = self._param(indicator_id, "allow_partial")

        # Strict mode: a partial result counts as a failure (status + score).
        if status == IndicatorStatus.PARTIAL and not allow_partial:
            status = IndicatorStatus.FAIL

        if status == IndicatorStatus.FAIL:
            return status, self._param(indicator_id, "fail_score")

        if status == IndicatorStatus.PASS:
            score = raw_score if graded else self._param(indicator_id, "pass_score")
            return status, score

        # PARTIAL (and allow_partial is True)
        score = raw_score if graded else self._param(indicator_id, "partial_score")
        return status, score

    def score_for(
        self,
        indicator_id: str,
        status: IndicatorStatus,
        raw_score: float,
        graded: bool,
    ) -> float:
        """Convenience wrapper around :meth:`evaluate` returning only the score."""
        return self.evaluate(indicator_id, status, raw_score, graded)[1]

    @classmethod
    def from_config(cls, scoring_cfg: Optional[Dict[str, Any]]) -> Optional["ScorePolicy"]:
        """Build a policy from a ``quality.scoring`` config dict.

        Returns ``None`` when ``scoring_cfg`` is falsy, so callers can fall back
        to raw scores (backward-compatible default).
        """
        if not scoring_cfg:
            return None

        raw_overrides = scoring_cfg.get("overrides") or {}
        # Normalise nested OmegaConf/dict values to plain dicts.
        overrides = {
            str(ind_id): {str(k): v for k, v in (params or {}).items()}
            for ind_id, params in raw_overrides.items()
        }

        return cls(
            pass_score=float(scoring_cfg.get("pass_score", 1.0)),
            partial_score=float(scoring_cfg.get("partial_score", 0.5)),
            fail_score=float(scoring_cfg.get("fail_score", 0.0)),
            allow_partial=bool(scoring_cfg.get("allow_partial", True)),
            overrides=overrides,
        )
