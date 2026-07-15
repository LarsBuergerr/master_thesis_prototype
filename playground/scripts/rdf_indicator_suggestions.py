"""Erzeugt Patch-Vorschlaege aus Indikator-Fails -- aber nur fuer die
Indikatoren, bei denen sich ein Vorschlag rein aus dem kontrollierten
Vokabular ableiten laesst (kein LLM, keine inhaltliche Entscheidung noetig).

Zwei Stufen pro betroffenem Feld (siehe ChangeOp/FieldSuggestion in
rdf_changeset.py):
  - ready:       aktueller Wert ist nicht im Vokabular -> als ChangeOp sicher
                 entfernbar, ohne dass jemand etwas entscheiden muss.
  - needs_input: danach ist kein gueltiger Wert mehr uebrig -> FieldSuggestion
                 mit den gueltigen Vokabular-URIs zur Auswahl (Dropdown statt
                 Freitext).

Bewusst NICHT abgedeckt: Felder, die einen echten inhaltlichen Wert brauchen
(Geometrie, Kontakt, Datum, Keywords, ...), Kardinalitaets-Fails (z.B. zwei
gueltige contributorIDs statt einer) und alles LLM-bewertete (expressiveness).
Dafuer gibt es keinen mechanischen Vorschlag -- nur die Indikator-Diagnose
selbst geht ans Frontend, ohne Patch-Angebot.
"""

import sys
from dataclasses import dataclass
from pathlib import Path

from rdflib import Graph, Namespace, URIRef
from rdflib.namespace import DCAT, DCTERMS, RDF
from rdflib.term import Identifier

from rdf_changeset import ChangeOp, FieldSuggestion, apply_changeset, print_triple_diff

# extraction.vocabularies ist dependency-leicht (nur stdlib xml/csv), daher
# gezielt nur dieses Teilpaket auf den Pfad nehmen statt das ganze src/.
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from extraction.vocabularies import (  # noqa: E402
    VALID_ACCESS_RIGHT_URIS,
    VALID_CONTRIBUTOR_ID_URIS,
    VALID_FREQUENCY_URIS,
    VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS,
    VALID_POLITICAL_GEOCODING_LEVEL_URIS,
    VALID_THEME_URIS,
    get_geocoding_vocabulary_for_uri,
)

DCATDE = Namespace("http://dcat-ap.de/def/dcatde/")
SAMPLE_FILE = (
    Path(__file__).resolve().parents[2] / "data" / "extreme_cases_03" / "bad_05.rdf"
)


@dataclass(frozen=True)
class VocabField:
    """Ein Dataset-Feld, dessen Wert aus einem festen, kleinen kontrollierten
    Vokabular stammen muss (Indikator-Muster: PASS in vocab / PARTIAL oder
    FAIL sonst)."""

    indicator_id: str
    predicate: URIRef
    valid_uris: frozenset[str]


# reuse_access_rights akzeptiert zusaetzlich das INSPIRE-LimitationsOnPublicAccess-
# Vokabular als Fallback (siehe reusability.AccessRightsIndicator) -- deshalb
# hier die Vereinigung beider Sets, sonst wuerden gueltige Werte faelschlich
# als "ungueltig" markiert.
VOCAB_FIELDS = [
    VocabField("find_theme_valid", DCAT.theme, VALID_THEME_URIS),
    VocabField(
        "find_accrual_periodicity", DCTERMS.accrualPeriodicity, VALID_FREQUENCY_URIS
    ),
    VocabField(
        "find_geocoding_level",
        DCATDE.politicalGeocodingLevelURI,
        VALID_POLITICAL_GEOCODING_LEVEL_URIS,
    ),
    VocabField(
        "reuse_access_rights",
        DCTERMS.accessRights,
        VALID_ACCESS_RIGHT_URIS | VALID_LIMITATIONS_ON_PUBLIC_ACCESS_URIS,
    ),
    VocabField("reuse_contributor_id", DCATDE.contributorID, VALID_CONTRIBUTOR_ID_URIS),
]


def suggest_for_vocab_field(
    graph: Graph, dataset: Identifier, vfield: VocabField
) -> tuple[list[ChangeOp], list[FieldSuggestion]]:
    """ready: ungueltige Werte entfernen. needs_input: falls danach kein
    gueltiger Wert mehr uebrig ist, Vokabular-Kandidaten zur Auswahl anbieten."""
    current = list(graph.objects(dataset, vfield.predicate))
    invalid = [o for o in current if str(o) not in vfield.valid_uris]

    ready = [
        ChangeOp(
            "remove", dataset, vfield.predicate, o,
            reason=f"{vfield.indicator_id}: Wert nicht im kontrollierten Vokabular",
        )
        for o in invalid
    ]

    still_missing = len(invalid) == len(current)  # kein einziger gueltiger Wert
    suggestion = (
        [FieldSuggestion(
            vfield.indicator_id, dataset, vfield.predicate,
            candidates=sorted(vfield.valid_uris),
            reason=f"{vfield.indicator_id}: gueltigen Wert aus dem Vokabular waehlen",
        )]
        if still_missing else []
    )
    return ready, suggestion


def suggest_for_political_geocoding(graph: Graph, dataset: Identifier) -> list[ChangeOp]:
    """Nur ready-Fix: das Vokabular ist schluessel-abhaengig und zu gross
    (~11.000 Gemeindeschluessel) fuer eine Auswahlliste -- kein FieldSuggestion."""
    ready = []
    for o in graph.objects(dataset, DCATDE.politicalGeocodingURI):
        _, valid_uris = get_geocoding_vocabulary_for_uri(str(o))
        if valid_uris is not None and str(o) not in valid_uris:
            ready.append(ChangeOp(
                "remove", dataset, DCATDE.politicalGeocodingURI, o,
                reason="find_political_geocoding: URI nicht im dcat-ap.de Vokabular",
            ))
    return ready


def suggest_for_dataset(graph: Graph) -> tuple[list[ChangeOp], list[FieldSuggestion]]:
    """Alle mechanischen Vorschlaege fuer ein Dataset gebuendelt."""
    dataset = next(graph.subjects(RDF.type, DCAT.Dataset))
    ready: list[ChangeOp] = []
    suggestions: list[FieldSuggestion] = []
    for vfield in VOCAB_FIELDS:
        r, s = suggest_for_vocab_field(graph, dataset, vfield)
        ready += r
        suggestions += s
    ready += suggest_for_political_geocoding(graph, dataset)
    return ready, suggestions


def main() -> None:
    from rich.console import Console

    graph = Graph()
    graph.parse(SAMPLE_FILE)

    ready, suggestions = suggest_for_dataset(graph)

    console = Console()
    console.print(
        f"[bold]{SAMPLE_FILE.name}: {len(ready)} ready fix(es), "
        f"{len(suggestions)} needs-input suggestion(s)[/bold]\n"
    )

    if ready:
        patched = apply_changeset(graph, ready)
        print_triple_diff(graph, patched, console)

    for s in suggestions:
        console.print(
            f"\n[yellow]? {s.indicator_id}[/yellow]: {s.predicate.n3()} braucht einen "
            f"Wert ({len(s.candidates)} Vokabular-Kandidaten, z.B. {s.candidates[0]})"
        )


if __name__ == "__main__":
    main()
