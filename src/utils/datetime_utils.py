"""Utilities for validating xs:date and xs:dateTime literal values.

Provides ``is_valid_xs_date``, ``is_valid_xs_datetime`` and a dispatcher
``validate_temporal_value`` that picks the right form based on either an
rdflib Literal's ``xsd:datatype`` or — when no datatype is set — on the
string's shape.
"""

from datetime import date, datetime
import re
from typing import Any, Tuple

from rdflib.namespace import XSD


# xs:dateTime: 2001-10-26T21:32:52[.fff][Z|±HH:MM]
ISO_DATETIME_RE = re.compile(
    r"^-?\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$"
)

# xs:date: 2001-10-26[Z|±HH:MM]
ISO_DATE_RE = re.compile(r"^-?\d{4}-\d{2}-\d{2}(?:Z|[+-]\d{2}:\d{2})?$")

_TZ_SUFFIX_RE = re.compile(r"(Z|[+-]\d{2}:\d{2})$")


def is_valid_xs_datetime(value: str) -> bool:
    """Return True if ``value`` matches the xs:dateTime lexical form."""
    if not isinstance(value, str) or not ISO_DATETIME_RE.match(value):
        return False
    norm = value.replace("Z", "+00:00") if value.endswith("Z") else value
    try:
        datetime.fromisoformat(norm)
        return True
    except Exception:
        return False


def is_valid_xs_date(value: str) -> bool:
    """Return True if ``value`` matches the xs:date lexical form."""
    if not isinstance(value, str) or not ISO_DATE_RE.match(value):
        return False
    core = _TZ_SUFFIX_RE.sub("", value)
    try:
        date.fromisoformat(core)
        return True
    except Exception:
        return False


def validate_temporal_value(literal_or_str: Any) -> Tuple[str, bool]:
    """Validate a temporal value as xs:date or xs:dateTime.

    Format selection order:
    1. ``literal.datatype`` if it equals ``xsd:date`` or ``xsd:dateTime``
    2. Otherwise inferred from the string: presence of ``T`` ⇒ dateTime, else date

    Returns ``(format_name, is_valid)`` where ``format_name`` is
    ``"date"`` or ``"dateTime"``.
    """
    value = str(literal_or_str)
    datatype = getattr(literal_or_str, "datatype", None)

    if datatype == XSD.dateTime:
        return "dateTime", is_valid_xs_datetime(value)
    if datatype == XSD.date:
        return "date", is_valid_xs_date(value)

    if "T" in value:
        return "dateTime", is_valid_xs_datetime(value)
    return "date", is_valid_xs_date(value)
