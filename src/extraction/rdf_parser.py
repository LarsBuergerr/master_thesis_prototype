"""RDF metadata parsing and normalization utilities."""

from pathlib import Path
from typing import Optional, Union
import rdflib
from rdflib import Graph, RDF, Namespace

from utils.logger import get_logger

logger = get_logger(__name__)

DCAT = Namespace("http://www.w3.org/ns/dcat#")
DCTERMS = Namespace("http://purl.org/dc/terms/")
DCATDE = Namespace("http://dcat-ap.de/def/dcatde/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


class RDFMetadataParser:
    """Handles parsing and normalization of RDF metadata in various formats."""

    # Supported RDF formats for parsing
    SUPPORTED_FORMATS = {
        "xml": "xml",  # RDF/XML
        "ttl": "turtle",  # Turtle
        "turtle": "turtle",
        "n3": "n3",  # N3
        "nt": "nt",  # N-Triples
        "ntriples": "nt",
        "rdf": "xml",  # Default to RDF/XML
        "jsonld": "json-ld",  # JSON-LD
    }

    @staticmethod
    def parse_file(
        filepath: Union[str, Path],
        format_hint: Optional[str] = None,
        normalize_to_nt: bool = False,
    ) -> Graph:
        """Parse RDF metadata file into rdflib Graph.

        Args:
            filepath: Path to the metadata file
            format_hint: Optional format hint (xml, ttl, n3, etc.)
                        If None, guesses from file extension
            normalize_to_nt: If True, normalizes graph to N-Triples
                           (useful for SPARQL queries)

        Returns:
            rdflib Graph object

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If format is not supported
            rdflib.exceptions.ParserError: If parsing fails
        """
        filepath = Path(filepath)

        if not filepath.exists():
            raise FileNotFoundError(f"Metadata file not found: {filepath}")

        # Determine format
        if format_hint:
            fmt = RDFMetadataParser.SUPPORTED_FORMATS.get(format_hint.lower())
            if not fmt:
                raise ValueError(
                    f"Unsupported format: {format_hint}. "
                    f"Supported: {list(RDFMetadataParser.SUPPORTED_FORMATS.keys())}"
                )
        else:
            # Guess from extension
            ext = filepath.suffix.lstrip(".").lower()
            fmt = RDFMetadataParser.SUPPORTED_FORMATS.get(
                ext, RDFMetadataParser.SUPPORTED_FORMATS.get("rdf")
            )

        logger.info(f"Parsing RDF metadata from {filepath} using format: {fmt}")

        try:
            g = Graph()
            g.parse(str(filepath), format=fmt)
            logger.info(f"Successfully parsed {len(g)} triples")

            if normalize_to_nt:
                # Normalize graph to N-Triples for consistent SPARQL queries
                return RDFMetadataParser._normalize_to_graph(g)

            return g

        except Exception as e:
            logger.error(f"Failed to parse RDF metadata: {e}")
            raise

    @staticmethod
    def parse_string(
        rdf_string: str,
        format_hint: str = "xml",
        normalize_to_nt: bool = False,
    ) -> Graph:
        """Parse RDF metadata from string.

        Args:
            rdf_string: RDF content as string
            format_hint: Format (xml, ttl, n3, etc.)
            normalize_to_nt: If True, normalizes to N-Triples

        Returns:
            rdflib Graph object
        """
        fmt = RDFMetadataParser.SUPPORTED_FORMATS.get(format_hint.lower(), format_hint)

        logger.info(f"Parsing RDF metadata from string using format: {fmt}")

        try:
            g = Graph()
            g.parse(data=rdf_string, format=fmt)
            logger.info(f"Successfully parsed {len(g)} triples")

            if normalize_to_nt:
                return RDFMetadataParser._normalize_to_graph(g)

            return g

        except Exception as e:
            logger.error(f"Failed to parse RDF string: {e}")
            raise

    @staticmethod
    def _normalize_to_graph(g: Graph) -> Graph:
        """Normalize graph to canonical form.

        This ensures consistent handling across different RDF serializations.

        Args:
            g: Original graph

        Returns:
            Normalized graph (in N-Triples internally)
        """
        # Create new graph and add all triples
        # This normalizes blank nodes and URIs
        normalized = Graph()
        for s, p, o in g:
            normalized.add((s, p, o))
        return normalized

    @staticmethod
    def to_n_triples(g: Graph) -> str:
        """Convert graph to N-Triples format.

        N-Triples is a line-based format, ideal for SPARQL queries.

        Args:
            g: rdflib Graph

        Returns:
            N-Triples string representation
        """
        return g.serialize(format="nt").decode("utf-8")

    @staticmethod
    def to_turtle(g: Graph) -> str:
        """Convert graph to Turtle format.

        Turtle is human-readable and compact.

        Args:
            g: rdflib Graph

        Returns:
            Turtle string representation
        """
        return g.serialize(format="turtle").decode("utf-8")

    @staticmethod
    def get_dataset_subjects(g: Graph) -> list:
        """Extract all dcat:Dataset subjects from graph.

        Args:
            g: rdflib Graph

        Returns:
            List of dataset URIs
        """
        datasets = list(g.subjects(predicate=RDF.type, object=DCAT.Dataset))
        return datasets

    @staticmethod
    def statistics(g: Graph) -> dict:
        """Get statistics about the RDF graph.

        Args:
            g: rdflib Graph

        Returns:
            Dictionary with graph statistics
        """
        return {
            "triple_count": len(g),
            "subject_count": len(set(g.subjects())),
            "predicate_count": len(set(g.predicates())),
            "object_count": len(set(g.objects())),
            "dataset_count": len(RDFMetadataParser.get_dataset_subjects(g)),
            "namespaces": dict(g.namespaces()),
        }
