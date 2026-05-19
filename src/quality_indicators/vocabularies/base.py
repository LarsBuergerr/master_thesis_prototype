"""Base helpers for controlled vocabularies.

This module keeps vocabulary handling simple and reusable for indicators.
"""

from enum import Enum
from typing import Iterable, Set


def enum_values(enum_cls: type[Enum]) -> Set[str]:
    """Return all enum values as a string set."""
    return {str(member.value) for member in enum_cls}


def contains_uri(enum_cls: type[Enum], uri: str) -> bool:
    """Check whether a URI belongs to the given vocabulary enum."""
    return uri in enum_values(enum_cls)


def merge_values(*collections: Iterable[str]) -> Set[str]:
    """Merge multiple string collections into one set."""
    merged: Set[str] = set()
    for collection in collections:
        merged.update(collection)
    return merged
