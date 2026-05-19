"""Centralized controlled vocabulary definitions for quality indicators."""

from quality_indicators.vocabularies.base import contains_uri, enum_values, merge_values
from quality_indicators.vocabularies.formats import (
    FileTypeUri,
    IanaMediaTypeUri,
    MachineReadableToken,
)
from quality_indicators.vocabularies.licenses import DcatApDeLicense
from quality_indicators.vocabularies.metadata_authorities import (
    ContributorIdUri,
    LanguageUri,
    PoliticalGeocodingLevelUri,
)
from quality_indicators.vocabularies.themes import EUDataTheme

VALID_THEME_URIS = enum_values(EUDataTheme)
OPEN_LICENSE_URIS = enum_values(DcatApDeLicense)
MACHINE_READABLE_TOKENS = enum_values(MachineReadableToken)
VALID_FILE_TYPE_URIS = enum_values(FileTypeUri)
VALID_MEDIA_TYPE_URIS = enum_values(IanaMediaTypeUri)

__all__ = [
    "contains_uri",
    "enum_values",
    "merge_values",
    "EUDataTheme",
    "DcatApDeLicense",
    "MachineReadableToken",
    "FileTypeUri",
    "IanaMediaTypeUri",
    "LanguageUri",
    "PoliticalGeocodingLevelUri",
    "ContributorIdUri",
    "VALID_THEME_URIS",
    "OPEN_LICENSE_URIS",
    "MACHINE_READABLE_TOKENS",
    "VALID_FILE_TYPE_URIS",
    "VALID_MEDIA_TYPE_URIS",
]
