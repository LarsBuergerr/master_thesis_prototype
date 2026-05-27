"""Controlled vocabularies loaded from RDF/XML and CSV files."""

from quality_indicators.vocabularies.loader import (
    IANA_MEDIA_TYPE_PREFIX,
    get_geocoding_vocabulary_for_uri,
    get_political_geocoding_segment,
    load_iana_media_type_templates,
    load_iana_media_type_uris,
    load_open_license_uris,
    load_skos_concept_uris,
)

VALID_THEME_URIS = load_skos_concept_uris("data_theme.rdf")
VALID_FREQUENCY_URIS = load_skos_concept_uris("frequency.rdf")
VALID_FILE_TYPE_URIS = load_skos_concept_uris("file_type.rdf")
VALID_POLITICAL_GEOCODING_LEVEL_URIS = load_skos_concept_uris(
    "political_geocoding_level.rdf"
)
OPEN_LICENSE_URIS = load_open_license_uris()
VALID_MEDIA_TYPE_URIS = load_iana_media_type_uris()
VALID_MEDIA_TYPE_TEMPLATES = load_iana_media_type_templates()

__all__ = [
    "IANA_MEDIA_TYPE_PREFIX",
    "VALID_THEME_URIS",
    "VALID_FREQUENCY_URIS",
    "VALID_FILE_TYPE_URIS",
    "VALID_POLITICAL_GEOCODING_LEVEL_URIS",
    "OPEN_LICENSE_URIS",
    "VALID_MEDIA_TYPE_URIS",
    "VALID_MEDIA_TYPE_TEMPLATES",
    "get_geocoding_vocabulary_for_uri",
    "get_political_geocoding_segment",
    "load_skos_concept_uris",
]
