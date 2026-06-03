"""Controlled vocabularies loaded from RDF/XML and CSV files."""

from extraction.vocabularies.loader import (
    IANA_MEDIA_TYPE_PREFIX,
    get_geocoding_vocabulary_for_uri,
    get_political_geocoding_segment,
    load_iana_media_type_templates,
    load_iana_media_type_uris,
    load_license_exact_match_by_type,
    load_open_license_uris,
    load_restricted_license_uris,
    load_skos_concept_uris,
)

VALID_THEME_URIS = load_skos_concept_uris("data_theme.rdf")
VALID_FREQUENCY_URIS = load_skos_concept_uris("frequency.rdf")
VALID_FILE_TYPE_URIS = load_skos_concept_uris("file_type.rdf")
VALID_POLITICAL_GEOCODING_LEVEL_URIS = load_skos_concept_uris(
    "political_geocoding_level.rdf"
)
VALID_ACCESS_RIGHT_URIS = load_skos_concept_uris("access-right.rdf")
VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS = load_skos_concept_uris(
    "LimitationsOnPublicAccess.de.rdf"
)
OPEN_LICENSE_URIS = load_open_license_uris()
RESTRICTED_LICENSE_URIS = load_restricted_license_uris()
LICENSE_URIS_BY_TYPE = load_license_exact_match_by_type()
VALID_MEDIA_TYPE_URIS = load_iana_media_type_uris()
VALID_MEDIA_TYPE_TEMPLATES = load_iana_media_type_templates()

__all__ = [
    "IANA_MEDIA_TYPE_PREFIX",
    "VALID_THEME_URIS",
    "VALID_FREQUENCY_URIS",
    "VALID_FILE_TYPE_URIS",
    "VALID_POLITICAL_GEOCODING_LEVEL_URIS",
    "VALID_ACCESS_RIGHT_URIS",
    "VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS",
    "OPEN_LICENSE_URIS",
    "RESTRICTED_LICENSE_URIS",
    "LICENSE_URIS_BY_TYPE",
    "VALID_MEDIA_TYPE_URIS",
    "VALID_MEDIA_TYPE_TEMPLATES",
    "get_geocoding_vocabulary_for_uri",
    "get_political_geocoding_segment",
    "load_skos_concept_uris",
]
