"""DCAT-AP.de Specification.

This module contains the DCAT-AP.de metadata specification, including
required fields, optional fields, and quality requirements.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class ResourceType(Enum):
    """DCAT-AP.de resource types."""
    CATALOG = "catalog"
    DATASET = "dataset"
    DISTRIBUTION = "distribution"
    SERVICE = "service"
    CONCEPT = "concept"
    STANDARD = "standard"


@dataclass
class FieldRequirement:
    """Represents a DCAT-AP.de field requirement."""
    name: str
    uri: str
    required: bool
    description: str
    cardinality_min: int = 0
    cardinality_max: Optional[int] = None  # None = unlimited


@dataclass
class QualityRequirement:
    """Represents a DCAT-AP.de quality requirement."""
    id: str
    name: str
    description: str
    applicable_types: list[ResourceType]
    required_fields: list[str]
    recommended_fields: list[str]


# DCAT-AP.de required fields by resource type
DATASET_REQUIRED_FIELDS = [
    "dct:title",
    "dct:description",
    "dct:identifier",
    "dcat:theme",
    "dct:publisher",
    "dct:issued",
    "dct:modified",
]

DATASET_RECOMMENDED_FIELDS = [
    "dct:creator",
    "dct:contributor",
    "dcat:keyword",
    "dct:language",
    "dct:spatial",
    "dct:temporal",
    "dcat:landingPage",
    "dcat:contactPoint",
    "dct:accrualPeriodicity",
    "dcat:version",
    "dcat:qualifiedAttribution",
    "dct:conformsTo",
    "dcat:hasCurrentOrLatestDistribution",
]

DISTRIBUTION_REQUIRED_FIELDS = [
    "dcat:accessURL",
    "dct:format",
]

DISTRIBUTION_RECOMMENDED_FIELDS = [
    "dcat:downloadURL",
    "dct:title",
    "dct:description",
    "dcat:byteSize",
    "dcat:license",
    "dct:conformsTo",
    "dcat:compressionFormat",
    "dcat:packageFormat",
]

# Quality Requirements based on DCAT-AP.de
QUALITY_REQUIREMENTS = {
    ResourceType.DATASET: QualityRequirement(
        id="QR-DATASET-001",
        name="Minimal Metadata Quality",
        description="Dataset must have all required fields populated",
        applicable_types=[ResourceType.DATASET],
        required_fields=DATASET_REQUIRED_FIELDS,
        recommended_fields=DATASET_RECOMMENDED_FIELDS,
    ),
    ResourceType.DISTRIBUTION: QualityRequirement(
        id="QR-DIST-001",
        name="Distribution Accessibility",
        description="Distribution must have accessible access and format",
        applicable_types=[ResourceType.DISTRIBUTION],
        required_fields=DISTRIBUTION_REQUIRED_FIELDS,
        recommended_fields=DISTRIBUTION_RECOMMENDED_FIELDS,
    ),
}

# All DCAT-AP.de fields with their requirements
DCAT_FIELDS = {
    # Dataset fields
    "dct:title": FieldRequirement(
        name="title",
        uri="http://purl.org/dc/terms/title",
        required=True,
        description="A name given to the dataset",
        cardinality_min=1,
        cardinality_max=None,
    ),
    "dct:description": FieldRequirement(
        name="description",
        uri="http://purl.org/dc/terms/description",
        required=True,
        description="Free-text account of the dataset",
        cardinality_min=1,
        cardinality_max=None,
    ),
    "dct:identifier": FieldRequirement(
        name="identifier",
        uri="http://purl.org/dc/terms/identifier",
        required=True,
        description="A unique identifier for the dataset",
        cardinality_min=1,
        cardinality_max=1,
    ),
    "dcat:theme": FieldRequirement(
        name="theme",
        uri="http://www.w3.org/ns/dcat#theme",
        required=True,
        description="A category of the dataset",
        cardinality_min=1,
        cardinality_max=None,
    ),
    "dct:publisher": FieldRequirement(
        name="publisher",
        uri="http://purl.org/dc/terms/publisher",
        required=True,
        description="The entity that makes the dataset available",
        cardinality_min=1,
        cardinality_max=1,
    ),
    "dct:issued": FieldRequirement(
        name="issued",
        uri="http://purl.org/dc/terms/issued",
        required=True,
        description="Date of formal issuance of the dataset",
        cardinality_min=1,
        cardinality_max=1,
    ),
    "dct:modified": FieldRequirement(
        name="modified",
        uri="http://purl.org/dc/terms/modified",
        required=True,
        description="Date on which the dataset was last modified",
        cardinality_min=1,
        cardinality_max=1,
    ),
    # Recommended dataset fields
    "dct:creator": FieldRequirement(
        name="creator",
        uri="http://purl.org/dc/terms/creator",
        required=False,
        description="An entity that created the dataset",
        cardinality_min=0,
        cardinality_max=None,
    ),
    "dcat:keyword": FieldRequirement(
        name="keyword",
        uri="http://www.w3.org/ns/dcat#keyword",
        required=False,
        description="A keyword or tag describing the dataset",
        cardinality_min=0,
        cardinality_max=None,
    ),
    "dct:language": FieldRequirement(
        name="language",
        uri="http://purl.org/dc/terms/language",
        required=False,
        description="A language of the dataset",
        cardinality_min=0,
        cardinality_max=None,
    ),
    "dct:spatial": FieldRequirement(
        name="spatial",
        uri="http://purl.org/dc/terms/spatial",
        required=False,
        description="Spatial extent of the dataset",
        cardinality_min=0,
        cardinality_max=None,
    ),
    "dct:temporal": FieldRequirement(
        name="temporal",
        uri="http://purl.org/dc/terms/temporal",
        required=False,
        description="Temporal extent of the dataset",
        cardinality_min=0,
        cardinality_max=None,
    ),
    "dcat:landingPage": FieldRequirement(
        name="landingPage",
        uri="http://www.w3.org/ns/dcat#landingPage",
        required=False,
        description="A web page that provides access to the dataset",
        cardinality_min=0,
        cardinality_max=None,
    ),
    "dcat:contactPoint": FieldRequirement(
        name="contactPoint",
        uri="http://www.w3.org/ns/dcat#contactPoint",
        required=False,
        description="Contact information for the dataset",
        cardinality_min=0,
        cardinality_max=None,
    ),
    # Distribution fields
    "dcat:accessURL": FieldRequirement(
        name="accessURL",
        uri="http://www.w3.org/ns/dcat#accessURL",
        required=True,
        description="A URL that gives access to the distribution",
        cardinality_min=1,
        cardinality_max=None,
    ),
    "dct:format": FieldRequirement(
        name="format",
        uri="http://purl.org/dc/terms/format",
        required=True,
        description="The file format of the distribution",
        cardinality_min=1,
        cardinality_max=1,
    ),
    "dcat:downloadURL": FieldRequirement(
        name="downloadURL",
        uri="http://www.w3.org/ns/dcat#downloadURL",
        required=False,
        description="A direct link to the downloadable distribution",
        cardinality_min=0,
        cardinality_max=None,
    ),
    "dcat:byteSize": FieldRequirement(
        name="byteSize",
        uri="http://www.w3.org/ns/dcat#byteSize",
        required=False,
        description="The size of the distribution in bytes",
        cardinality_min=0,
        cardinality_max=1,
    ),
    "dcat:license": FieldRequirement(
        name="license",
        uri="http://www.w3.org/ns/dcat#license",
        required=False,
        description="The license under which the distribution is available",
        cardinality_min=0,
        cardinality_max=1,
    ),
}


def get_quality_requirement(resource_type: ResourceType) -> Optional[QualityRequirement]:
    """Get the quality requirement for a resource type."""
    return QUALITY_REQUIREMENTS.get(resource_type)


def check_required_fields(
    metadata: dict,
    resource_type: ResourceType
) -> tuple[list[str], list[str]]:
    """
    Check which required fields are present and which are missing.

    Args:
        metadata: DCAT-AP.de metadata dictionary
        resource_type: Type of resource (dataset, distribution, etc.)

    Returns:
        Tuple of (present_fields, missing_fields)
    """
    req = get_quality_requirement(resource_type)
    if not req:
        return [], []

    present = []
    missing = []

    for field in req.required_fields:
        # Check various possible field names (with/without prefix)
        field_name = field.split(":")[-1] if ":" in field else field
        if field in metadata or field_name in metadata:
            present.append(field)
        else:
            missing.append(field)

    return present, missing


def get_all_required_fields() -> list[str]:
    """Get list of all required fields across all resource types."""
    fields = []
    for req in QUALITY_REQUIREMENTS.values():
        for field in req.required_fields:
            if field not in fields:
                fields.append(field)
    return fields


def get_all_recommended_fields() -> list[str]:
    """Get list of all recommended fields across all resource types."""
    fields = []
    for req in QUALITY_REQUIREMENTS.values():
        for field in req.recommended_fields:
            if field not in fields:
                fields.append(field)
    return fields