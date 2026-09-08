"""RDF-Changeset: strukturierte Aenderungen an einer RDF-Datei anwenden und
das Ergebnis als Tripel-Diff anzeigen.

Hintergrund: Text-Diff auf serialisierten RDF-Dateien ist nicht robust --
Praefixe, Tripel-Reihenfolge und Blank-Node-Labels duerfen sich bei jeder
Serialisierung aendern, ohne dass sich am Inhalt etwas aendert. Der Diff muss
deshalb auf Tripel-Ebene laufen: rdflib.compare.graph_diff() liefert
(gemeinsam, nur_alt, nur_neu) als Tripel-Mengen -- das Aequivalent zu
+/- Zeilen in git diff, aber robust gegen Formatierung.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

from rdflib import Graph, Literal as RdfLiteral, Namespace
from rdflib.compare import graph_diff
from rdflib.namespace import RDF
from rdflib.term import Identifier
from rich.console import Console

DCAT = Namespace("http://www.w3.org/ns/dcat#")
SAMPLE_FILE = Path(__file__).parent / "data" / "perfect_example_01.rdf"


@dataclass(frozen=True)
class ChangeOp:
    """Eine Tripel-Operation, wie sie aus einem behobenen FAIL/PARTIAL-Indikator
    entstehen wuerde: subject/predicate = Ort im Graph, object = Wert."""

    op: Literal["add", "remove"]
    subject: Identifier
    predicate: Identifier
    object: Identifier
    reason: str = ""


@dataclass(frozen=True)
class FieldSuggestion:
    """Ein Ort im Graph, an dem ein Wert fehlt oder ungueltig ist, der
    richtige Wert sich aber nicht automatisch bestimmen laesst -- der Mensch
    waehlt ihn aus (z.B. im Frontend per Dropdown), erst danach wird daraus
    ein konkreter ``ChangeOp``."""

    indicator_id: str
    subject: Identifier
    predicate: Identifier
    candidates: list[str] = field(default_factory=list)  # Vokabular-URIs; leer = Freitext
    reason: str = ""


def apply_changeset(graph: Graph, changes: list[ChangeOp]) -> Graph:
    """Wendet Tripel-Operationen an, ohne den Original-Graphen zu veraendern."""
    patched = Graph()
    for triple in graph:
        patched.add(triple)
    for change in changes:
        triple = (change.subject, change.predicate, change.object)
        (patched.add if change.op == "add" else patched.remove)(triple)
    return patched


def print_triple_diff(original: Graph, patched: Graph, console: Console) -> None:
    """Zeigt den Unterschied zweier Graphen tripelweise, im git-diff-Stil."""
    _, only_original, only_patched = graph_diff(original, patched)
    for s, p, o in only_original:
        console.print(f"[red]- {p.n3()} {o.n3()}[/red]  ({s.n3()})")
    for s, p, o in only_patched:
        console.print(f"[green]+ {p.n3()} {o.n3()}[/green]  ({s.n3()})")


def main() -> None:
    original = Graph()
    original.parse(SAMPLE_FILE)
    dataset = next(original.subjects(RDF.type, DCAT.Dataset))

    # Beispiel-Changeset, wie es aus einem gefixten Indikator entstehen koennte:
    # expr_keyword_quality bemaengelt ein zusammengesetztes, unleserliches
    # Keyword -- Ersatz durch eine praegnantere Variante (remove + add).
    bad_keyword = RdfLiteral("fortschreibung-des-bevölkerungsstandes")
    changes = [ 
        ChangeOp(
            "remove", dataset, DCAT.keyword, bad_keyword,
            reason="expr_keyword_quality: Keyword ist kein eigenstaendiger Begriff",
        ),
        ChangeOp(
            "add", dataset, DCAT.keyword, RdfLiteral("bevölkerungsfortschreibung"),
            reason="expr_keyword_quality: praegnanterer Ersatzbegriff",
        ),
    ]

    patched = apply_changeset(original, changes)

    console = Console()
    print_triple_diff(original, patched, console)

    out_path = SAMPLE_FILE.with_suffix(".patched.rdf")
    out_path.write_text(patched.serialize(format="pretty-xml"), encoding="utf-8")
    console.print(f"\nPatched RDF geschrieben nach {out_path.name}")


if __name__ == "__main__":
    main()
