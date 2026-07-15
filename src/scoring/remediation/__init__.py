"""Attach a Remediation (ChangePatch or Recommendation) to FAIL/PARTIAL
IndicatorResults. See core.remediation for the two shapes and
scoring.remediation.resolvers for which indicators get a structured patch.
"""

from core.indicator import IndicatorResult, IndicatorStatus
from core.remediation import Recommendation
from extraction.dataset_context import DatasetContext
from scoring.remediation.resolvers import RESOLVERS

__all__ = ["attach_remediation"]


def _fallback_recommendation(result: IndicatorResult) -> Recommendation:
    """Every indicator already produces a human-readable message -- reuse it
    when no more specific resolver applies (or the specific one found
    nothing), so no failing indicator is ever left without any guidance."""
    return Recommendation(
        message_de=result.message_de or "Kein spezifischer Hinweis verfügbar.",
        message_en=result.message_en or "No specific guidance available.",
    )


def attach_remediation(result: IndicatorResult, context: DatasetContext) -> None:
    """Sets ``result.remediation`` in place for FAIL/PARTIAL results.

    No-op for PASS / NOT_APPLICABLE / ERROR -- there is nothing to remediate.
    """
    if result.status not in (IndicatorStatus.FAIL, IndicatorStatus.PARTIAL):
        return
    resolver = RESOLVERS.get(result.indicator_id)
    remediation = resolver(context, result) if resolver else None
    result.remediation = remediation or _fallback_recommendation(result)
