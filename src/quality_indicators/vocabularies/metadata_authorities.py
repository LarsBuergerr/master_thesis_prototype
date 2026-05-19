"""Additional controlled vocabularies used by metadata profiles (mock subset)."""

from enum import Enum


class LanguageUri(str, Enum):
    DEU = "http://publications.europa.eu/resource/authority/language/DEU"
    ENG = "http://publications.europa.eu/resource/authority/language/ENG"


class PoliticalGeocodingLevelUri(str, Enum):
    INTERNATIONAL = "http://dcat-ap.de/def/politicalGeocoding/Level/international"
    EUROPEAN = "http://dcat-ap.de/def/politicalGeocoding/Level/european"
    FEDERAL = "http://dcat-ap.de/def/politicalGeocoding/Level/federal"
    STATE = "http://dcat-ap.de/def/politicalGeocoding/Level/state"
    ADMINISTRATIVE_DISTRICT = (
        "http://dcat-ap.de/def/politicalGeocoding/Level/administrativeDistrict"
    )
    MUNICIPALITY = "http://dcat-ap.de/def/politicalGeocoding/Level/municipality"


class ContributorIdUri(str, Enum):
    OPEN_DATA_BAYERN = "http://dcat-ap.de/def/contributors/openDataBayern"
    GENESIS_DESTATIS = "http://dcat-ap.de/def/contributors/GenesisDestatis"
