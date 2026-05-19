"""File format controlled vocabulary (mock subset)."""

from enum import Enum


class FileTypeUri(str, Enum):
    CSV = "http://publications.europa.eu/resource/authority/file-type/CSV"
    XLS = "http://publications.europa.eu/resource/authority/file-type/XLS"
    XML = "http://publications.europa.eu/resource/authority/file-type/XML"
    RDF = "http://publications.europa.eu/resource/authority/file-type/RDF"
    JSON = "http://publications.europa.eu/resource/authority/file-type/JSON"


class IanaMediaTypeUri(str, Enum):
    TEXT_CSV = "https://www.iana.org/assignments/media-types/text/csv"
    TEXT_XML = "https://www.iana.org/assignments/media-types/text/xml"
    TEXT_XLSX = "https://www.iana.org/assignments/media-types/text/xlsx"
    APP_JSON = "https://www.iana.org/assignments/media-types/application/json"


class MachineReadableToken(str, Enum):
    CSV = "CSV"
    JSON = "JSON"
    XML = "XML"
    RDF = "RDF"
    TTL = "TTL"
    GEOJSON = "GEOJSON"
    PARQUET = "PARQUET"
