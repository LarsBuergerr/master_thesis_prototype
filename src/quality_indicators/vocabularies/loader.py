"""Loaders for controlled vocabularies stored as RDF/XML and CSV files."""

from __future__ import annotations

import csv
import xml.etree.ElementTree as ET
from functools import lru_cache
from pathlib import Path
from typing import Optional

VOCAB_DIR = Path(__file__).parent

_NS = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dct": "http://purl.org/dc/terms/",
}

_RDF_ABOUT = f'{{{_NS["rdf"]}}}about'

_POLITICAL_GEOCODING_PREFIX = "http://dcat-ap.de/def/politicalGeocoding/"

_GEOCODING_FILE_MAP = {
    "level": "political_geocoding_level.rdf",
    "statekey": "political_geocoding_state_key.rdf",
    "districtkey": "political_geocoding_district_key.rdf",
    "governmentdistrictkey": "political_geocoding_government_district_key.rdf",
    "municipalassociationkey": "political_geocoding_municipal_association_key.rdf",
    "municipalitykey": "political_geocoding_municipality_key.rdf",
    "regionalkey": "political_geocoding_regional_key.rdf",
}


@lru_cache(maxsize=None)
def load_skos_concept_uris(filename: str) -> frozenset[str]:
    """Return all SKOS concept URIs from an RDF/XML vocabulary file.

    A concept is identified as any top-level element that declares
    ``skos:inScheme`` — works for both ``skos:Concept`` and ``rdf:Description``
    entries used across the EU and DCAT-AP-DE vocabulary files.
    """
    tree = ET.parse(VOCAB_DIR / filename)
    uris: set[str] = set()
    for element in tree.getroot():
        if element.find("skos:inScheme", _NS) is None:
            continue
        about = element.get(_RDF_ABOUT)
        if about:
            uris.add(about)
    return frozenset(uris)


@lru_cache(maxsize=None)
def load_open_license_uris(filename: str = "licenses.rdf") -> frozenset[str]:
    """Return DCAT-AP-DE license URIs categorised as ``Freie Nutzung``."""
    tree = ET.parse(VOCAB_DIR / filename)
    uris: set[str] = set()
    for element in tree.getroot():
        type_el = element.find("dct:type", _NS)
        if type_el is None or (type_el.text or "").strip() != "Freie Nutzung":
            continue
        about = element.get(_RDF_ABOUT)
        if about:
            uris.add(about)
    return frozenset(uris)


@lru_cache(maxsize=None)
def load_iana_media_type_uris(filename: str = "media_types.csv") -> frozenset[str]:
    """Return IANA media type URIs derived from the IANA media-types CSV."""
    base = "https://www.iana.org/assignments/media-types/"
    uris: set[str] = set()
    with (VOCAB_DIR / filename).open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            template = (row.get("Template") or "").strip()
            if template:
                uris.add(f"{base}{template}")
    return frozenset(uris)


def get_political_geocoding_segment(uri: str) -> Optional[str]:
    """Extract the segment (level/key kind) from a politicalGeocoding URI."""
    if not uri.startswith(_POLITICAL_GEOCODING_PREFIX):
        return None
    remainder = uri[len(_POLITICAL_GEOCODING_PREFIX) :]
    if not remainder:
        return None
    return remainder.split("/", 1)[0]


def get_geocoding_vocabulary_for_uri(
    uri: str,
) -> tuple[Optional[str], Optional[frozenset[str]]]:
    """Return ``(segment, valid_uris)`` for a politicalGeocoding URI.

    - ``(None, None)`` if the URI is not under the politicalGeocoding namespace.
    - ``(segment, None)`` if the URI's segment has no known vocabulary file.
    - ``(segment, frozenset)`` with the valid URI set otherwise.
    """
    segment = get_political_geocoding_segment(uri)
    if segment is None:
        return None, None
    filename = _GEOCODING_FILE_MAP.get(segment.lower())
    if filename is None:
        return segment, None
    return segment, load_skos_concept_uris(filename)
