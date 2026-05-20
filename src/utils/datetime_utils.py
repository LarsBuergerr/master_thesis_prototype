"""Utilities for validating xs:dateTime values per ISO 8601 (xs:dateTime).

Provides `is_valid_xs_datetime` used by indicators to validate dateTime strings.
"""

from datetime import datetime
import re

# Accepts formats like: 2001-10-26T21:32:52, with optional fractional seconds and timezone
# This is a pragmatic validator using datetime.fromisoformat where possible.

ISO_DATETIME_RE = re.compile(
    r"^-?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$"
)


def is_valid_xs_datetime(value: str) -> bool:
    """Return True if `value` matches a valid xs:dateTime lexical form.

    Uses a regex for basic lexical validation then attempts to parse with
    datetime.fromisoformat (after normalizing a trailing Z to +00:00).
    """
    if not isinstance(value, str):
        return False

    if not ISO_DATETIME_RE.match(value):
        return False

    # Normalize Z to +00:00 for fromisoformat
    norm = value.replace("Z", "+00:00") if value.endswith("Z") else value

    try:
        # datetime.fromisoformat supports the patterns with offset and fractional seconds
        datetime.fromisoformat(norm)
        return True
    except Exception:
        return False
