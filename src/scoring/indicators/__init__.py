"""Indicators for all quality dimensions.

All indicators are auto-registered when this module is imported.
"""

# Import all indicator modules to trigger auto-registration
from quality_indicators.indicators import findability
from quality_indicators.indicators import accessibility
from quality_indicators.indicators import reusability
from quality_indicators.indicators import expressiveness

__all__ = [
    "findability",
    "accessibility",
    "reusability",
    "expressiveness",
]
