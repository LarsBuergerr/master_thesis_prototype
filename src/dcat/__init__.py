"""DCAT-AP.de module for metadata quality measurement."""

from .specification import (
    ResourceType,
    FieldRequirement,
    QualityRequirement,
    DCAT_FIELDS,
    QUALITY_REQUIREMENTS,
    get_quality_requirement,
    check_required_fields,
    get_all_required_fields,
    get_all_recommended_fields,
)

__all__ = [
    "ResourceType",
    "FieldRequirement",
    "QualityRequirement",
    "DCAT_FIELDS",
    "QUALITY_REQUIREMENTS",
    "get_quality_requirement",
    "check_required_fields",
    "get_all_required_fields",
    "get_all_recommended_fields",
]