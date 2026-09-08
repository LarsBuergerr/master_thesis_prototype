"""Beschreibende Metadaten eines Datenverzeichnisses — die Portalebene.

Ein Metadatenportal zeigt Datensätze: Titel, Beschreibung, Schlagwörter,
Formate, Lizenz, Herausgeber. Das steht alles im RDF und hat mit der
Qualitätsbewertung nichts zu tun — deshalb liest dieses Modul die RDF-Dateien
eines Verzeichnisses direkt und unabhängig von jedem Lauf aus.

Die Trennung ist Absicht: das Portal ist ohne Bewertung vollständig, und eine
Bewertung legt sich später darüber (siehe backend/runs.py). Ein Lauf-Ergebnis
muss deshalb keine Titel oder Schlagwörter mitschleppen — es kennt nur
Dateinamen und Indikatoren.

Geparst wird mit demselben ``RDFMetadataParser``, den auch die Bewertung
benutzt; gecacht wird je Datei über ihre mtime, damit das Blättern im Portal
nicht jedes Mal 50 Graphen neu aufbaut.
"""

from __future__ import annotations

import logging
import re
import unicodedata
from pathlib import Path
from typing import Any, Optional

from rdflib import Graph, Namespace, RDF, URIRef
from rdflib.namespace import DCTERMS, FOAF

from core.dimension import QualityDimension  # noqa: F401  (hält sys.path-Setup konsistent)
from extraction.rdf_parser import RDFMetadataParser

from . import settings

logger = logging.getLogger("backend.catalog")

DCAT = Namespace("http://www.w3.org/ns/dcat#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

RDF_SUFFIXES = {".rdf", ".xml", ".ttl", ".n3", ".nt", ".jsonld"}

#: file -> (mtime, extrahierte Metadaten)
_CACHE: dict[Path, tuple[float, dict[str, Any]]] = {}

_LICENSE_LABELS: Optional[dict[str, str]] = None


def _license_labels() -> dict[str, str]:
    """URI -> deutsches Label aus dem Lizenz-Vokabular (einmalig geladen)."""
    global _LICENSE_LABELS
    if _LICENSE_LABELS is not None:
        return _LICENSE_LABELS

    labels: dict[str, str] = {}
    vocab = Path(__file__).resolve().parent.parent / "src" / "extraction" / "vocabularies" / "licenses.rdf"
    try:
        graph = Graph()
        graph.parse(str(vocab), format="xml")
        for concept in graph.subjects(RDF.type, SKOS.Concept):
            for label in graph.objects(concept, SKOS.prefLabel):
                if getattr(label, "language", None) in ("de", None):
                    labels[str(concept)] = str(label)
                    break
    except Exception as e:  # Vokabular fehlt/kaputt: Kurzform der URI reicht
        logger.warning("License vocabulary unreadable (%s); falling back to URI tails", e)

    _LICENSE_LABELS = labels
    return labels


def _local_name(uri: str) -> str:
    return uri.rstrip("/#").replace("#", "/").rsplit("/", 1)[-1]


def _slugify(text: str) -> str:
    """Kleingeschriebener ASCII-Slug, wie ihn ein Portal in der URL führt."""
    normalized = unicodedata.normalize("NFKD", text)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text).strip("-")
    return slug[:80] or "datensatz"


def _first_literal(graph: Graph, subject: URIRef, predicate: URIRef) -> str:
    for value in graph.objects(subject, predicate):
        text = str(value).strip()
        if text:
            return text
    return ""


def _date_only(value: str) -> str:
    """``2026-06-18T18:06:11.667310`` -> ``2026-06-18``."""
    return value[:10] if len(value) >= 10 else value


def _dataset_subject(graph: Graph) -> Optional[URIRef]:
    for subject in graph.subjects(RDF.type, DCAT.Dataset):
        if isinstance(subject, URIRef):
            return subject
    return None


def _publisher_name(graph: Graph, dataset: URIRef) -> str:
    for publisher in graph.objects(dataset, DCTERMS.publisher):
        name = _first_literal(graph, publisher, FOAF.name)
        if name:
            return name
        if isinstance(publisher, URIRef):
            return _local_name(str(publisher))
    return ""


def _formats_and_license(graph: Graph, dataset: URIRef) -> tuple[list[str], Optional[str], Optional[str]]:
    """Formate aller Distributionen sowie Lizenz (Label und URI)."""
    formats: list[str] = []
    license_uri: Optional[str] = None

    for value in graph.objects(dataset, DCTERMS.license):
        license_uri = str(value)

    for dist in graph.objects(dataset, DCAT.distribution):
        for predicate in (DCTERMS["format"], DCAT.mediaType):
            for value in graph.objects(dist, predicate):
                label = _local_name(str(value)) if str(value).startswith("http") else str(value)
                label = label.strip()
                if label and label not in formats:
                    formats.append(label)
        if license_uri is None:
            for value in graph.objects(dist, DCTERMS.license):
                license_uri = str(value)

    label = None
    if license_uri:
        label = _license_labels().get(license_uri) or _local_name(license_uri)
    return formats, label, license_uri


def _extract(path: Path) -> dict[str, Any]:
    """Portal-Metadaten einer RDF-Datei. Wirft nicht: eine unlesbare Datei
    erscheint mit ihrem Dateinamen als Titel, statt den Katalog zu kippen."""
    stem = path.stem
    base: dict[str, Any] = {
        "file": path.name,
        "id": stem,
        "slug": _slugify(stem),
        "uri": None,
        "title": stem,
        "description": "",
        "keywords": [],
        "themes": [],
        "formats": [],
        "license": None,
        "license_uri": None,
        "modified": "",
        "issued": "",
        "publisher_name": "",
        # Aus dem Dateinamen der Stichprobe abgeleitet: Präfix ``geo_`` /
        # ``non_geo_`` und der Rest als Herkunftsportal. Rein deskriptiv — für
        # ein beliebiges Verzeichnis bleibt ``category`` schlicht None.
        "category": None,
        "source": None,
    }

    if stem.startswith("geo_"):
        base["category"] = "geo"
        base["source"] = re.sub(r"_\d+$", "", stem[len("geo_"):])
    elif stem.startswith("non_geo_"):
        base["category"] = "non_geo"
        base["source"] = re.sub(r"_\d+$", "", stem[len("non_geo_"):])

    try:
        graph = RDFMetadataParser.parse_file(path)
    except Exception as e:
        logger.warning("Cannot parse %s (%s)", path.name, e)
        return base

    dataset = _dataset_subject(graph)
    if dataset is None:
        return base

    title = _first_literal(graph, dataset, DCTERMS.title)
    formats, license_label, license_uri = _formats_and_license(graph, dataset)

    base.update(
        {
            "uri": str(dataset),
            "title": title or stem,
            "slug": _slugify(title or stem),
            "description": _first_literal(graph, dataset, DCTERMS.description),
            "keywords": sorted({str(k).strip() for k in graph.objects(dataset, DCAT.keyword) if str(k).strip()}),
            "themes": sorted({_local_name(str(t)) for t in graph.objects(dataset, DCAT.theme)}),
            "formats": formats,
            "license": license_label,
            "license_uri": license_uri,
            "modified": _date_only(_first_literal(graph, dataset, DCTERMS.modified)),
            "issued": _date_only(_first_literal(graph, dataset, DCTERMS.issued)),
            "publisher_name": _publisher_name(graph, dataset),
        }
    )
    return base


def _rdf_files(directory: Path) -> list[Path]:
    return sorted(
        p for p in directory.iterdir()
        if p.is_file() and p.suffix.lower() in RDF_SUFFIXES
    )


def list_catalogs() -> list[dict[str, Any]]:
    """Datenverzeichnisse unter ``settings.DATA_ROOT``, die RDF-Dateien enthalten."""
    root = settings.DATA_ROOT
    if not root.is_dir():
        logger.warning("Data root missing: %s", root)
        return []

    catalogs = []
    for entry in sorted(root.iterdir()):
        if not entry.is_dir():
            continue
        files = _rdf_files(entry)
        if files:
            catalogs.append({"name": entry.name, "dataset_count": len(files)})
    return catalogs


def resolve_catalog(name: str) -> Path:
    """Verzeichnisnamen auf einen Pfad unterhalb von DATA_ROOT abbilden.

    Pfadtrenner werden abgewiesen und der aufgelöste Pfad noch einmal gegen die
    Wurzel geprüft, damit ein konstruierter Name nicht aus ihr herausführt.
    """
    if "/" in name or "\\" in name or name.startswith("."):
        raise ValueError(f"Invalid catalog name: {name}")
    root = settings.DATA_ROOT.resolve()
    path = (root / name).resolve()
    if path.parent != root or not path.is_dir():
        raise FileNotFoundError(f"Catalog not found: {name}")
    return path


def load_catalog(name: str) -> list[dict[str, Any]]:
    """Alle Datensätze eines Verzeichnisses, je Datei über die mtime gecacht."""
    directory = resolve_catalog(name)
    datasets = []
    for path in _rdf_files(directory):
        mtime = path.stat().st_mtime
        cached = _CACHE.get(path)
        if cached is None or cached[0] != mtime:
            cached = (mtime, _extract(path))
            _CACHE[path] = cached
        datasets.append(cached[1])
    return datasets


def resolve_file(catalog: str, filename: str) -> Path:
    """Eine einzelne RDF-Datei innerhalb eines Katalogs auflösen."""
    directory = resolve_catalog(catalog)
    if "/" in filename or "\\" in filename or filename.startswith("."):
        raise ValueError(f"Invalid file name: {filename}")
    path = (directory / filename).resolve()
    if path.parent != directory.resolve() or not path.is_file():
        raise FileNotFoundError(f"File not found: {filename}")
    if path.suffix.lower() not in RDF_SUFFIXES:
        raise FileNotFoundError(f"Not an RDF file: {filename}")
    return path
