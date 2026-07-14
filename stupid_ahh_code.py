# This program will contain some really stupid shit. Better not look at it.
#
# Demo: RDF-Datei -> Triples -> RDF-Datei (Roundtrip).
#
# Antwort auf die Frage "kann man aus den Triplen die RDF-Datei rekonstruieren?":
# JA, semantisch verlustfrei -- der Graph (die Menge der Triples) ist die
# eigentliche Information, die Datei ist nur eine Serialisierung davon.
# ABER nicht byte-identisch: Prefixe, Reihenfolge, Formatierung und
# Blank-Node-Labels duerfen sich aendern. Ob nichts verloren ging, prueft
# man deshalb mit Graph-Isomorphie statt mit Text-Vergleich.

from pathlib import Path

from rdflib import Graph
from rdflib.compare import isomorphic
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

SAMPLE_FILE = Path(__file__).parent / "data" / "perfect_example_01.rdf"


class OrderedGraph(Graph):
    """Graph, der sich die Reihenfolge merkt, in der der Parser die Triples
    aus der Datei liest (= Dokument-Reihenfolge).

    Noetig, weil ein RDF-Graph eine MENGE ist: nach g.parse() ist die
    Dateireihenfolge weg und list(g) liefert irgendeine Reihenfolge.
    Der Parser ruft aber fuer jedes gelesene Triple add() auf -- den
    fangen wir ab. Achtung: rdflibs Serializer ignorieren diese
    Reihenfolge beim Zurueckschreiben (pretty-xml gruppiert nach
    Subjekt); sie ist nur fuer die Weiterverarbeitung der Liste nutzbar.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ordered: list[tuple] = []

    def add(self, triple):
        self.ordered.append(triple)
        return super().add(triple)


def rdf_to_triples(path: Path) -> list[tuple]:
    """Datei parsen; Triple-Liste kommt in Dokument-Reihenfolge zurueck."""
    g = OrderedGraph()
    g.parse(path)  # Format wird an Endung/Inhalt erkannt
    return g.ordered


def triples_to_rdf(triples: list[tuple], fmt: str = "turtle") -> str:
    """Aus der Triple-Liste wieder eine serialisierte RDF-Datei bauen."""
    g = Graph()
    for s, p, o in triples:
        g.add((s, p, o))
    return g.serialize(format=fmt)


def main() -> None:
    triples = rdf_to_triples(SAMPLE_FILE)
    print(f"{SAMPLE_FILE.name}: {len(triples)} Triples extrahiert")
    print("Erste 3 Triples in Dokument-Reihenfolge:")
    for s, p, o in triples[:3]:
        print(f"  {p} -> {str(o)[:60]}")

    # Rekonstruktion wieder als RDF/XML, wie das Original
    rebuilt = triples_to_rdf(triples, fmt="pretty-xml")
    out_path = SAMPLE_FILE.with_suffix(".rebuilt.rdf")
    out_path.write_text(rebuilt, encoding="utf-8")
    print(f"Rekonstruiert nach {out_path.name} ({len(rebuilt)} Zeichen)")

    # Beide Versionen huebsch in die Konsole (rich/pygments)
    console = Console()
    original_text = SAMPLE_FILE.read_text(encoding="utf-8")
    console.print(
        Panel(
            Syntax(original_text, "xml", line_numbers=True, word_wrap=True),
            title=f"Original: {SAMPLE_FILE.name} (RDF/XML)",
            border_style="cyan",
        )
    )
    console.print(
        Panel(
            Syntax(rebuilt, "xml", line_numbers=True, word_wrap=True),
            title=f"Rekonstruiert: {out_path.name} (RDF/XML)",
            border_style="green",
        )
    )

    # Beweis: Original und Rekonstruktion sind semantisch identisch.
    # isomorphic() vergleicht die Graphen inkl. Blank-Node-Struktur.
    original = Graph()
    original.parse(SAMPLE_FILE)

    # RDF/XML behaelt die lexikalischen Formen -> Roundtrip exakt isomorph:
    reparsed_xml = Graph()
    reparsed_xml.parse(data=rebuilt, format="xml")
    print("RDF/XML-Roundtrip isomorph:", isomorphic(original, reparsed_xml))

    # Achtung, Turtle-Falle: rdflib schreibt "786432"^^xsd:decimal als
    # Kurzform 786432.0 -- gleicher WERT, andere lexikalische Form. Die
    # strenge Isomorphie-Pruefung vergleicht lexikalisch und meldet dann
    # False, obwohl semantisch nichts verloren ging:
    reparsed_ttl = Graph()
    reparsed_ttl.parse(data=triples_to_rdf(triples, fmt="turtle"), format="turtle")
    print("Turtle-Roundtrip isomorph:", isomorphic(original, reparsed_ttl))


if __name__ == "__main__":
    main()
