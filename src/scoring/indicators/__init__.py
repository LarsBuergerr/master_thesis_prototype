"""Indicators for all quality dimensions.

All indicators are auto-registered when this module is imported.
"""

# Import all indicator modules to trigger auto-registration
from scoring.indicators import findability
from scoring.indicators import accessibility
from scoring.indicators import reusability
from scoring.indicators import expressiveness

__all__ = [
    "findability",
    "accessibility",
    "reusability",
    "expressiveness",
]
