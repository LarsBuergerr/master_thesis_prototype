from pathlib import Path
from rdflib import Graph
from pyshacl import validate


DATA_FILE = Path("~/masterthesis/master_thesis_prototype/playground/scripts/data/example_metadata.ttl").expanduser().resolve();
SHAPES_FILE = Path("~/masterthesis/master_thesis_prototype/playground/scripts/data/shapes_DCAT-AP.de 2.0 - Spezifikation & Konventionen (2023-01-23).ttl").expanduser().resolve();


def main() -> None:
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Data file not found: {DATA_FILE}")

    if not SHAPES_FILE.exists():
        raise FileNotFoundError(f"Shapes file not found: {SHAPES_FILE}")

    data_graph = Graph()
    data_graph.parse(DATA_FILE, format="turtle")

    shapes_graph = Graph()
    shapes_graph.parse(SHAPES_FILE, format="turtle")


    conforms, results_graph, results_text = validate(
        data_graph=data_graph,
        shacl_graph=shapes_graph,
        inference="rdfs",
        abort_on_first=False,
        allow_infos=True,
        allow_warnings=True,
        meta_shacl=False,
        advanced=False,
        js=False,
        debug=False,
    )

    print("=" * 80)
    print(f"Conforms: {conforms}")
    print("=" * 80)
    print(results_text)

    output_file = Path("validation_report.ttl")
    results_graph.serialize(destination=output_file, format="turtle")
    print("=" * 80)
    print(f"Validation report written to: {output_file.resolve()}")


if __name__ == "__main__":
    main()