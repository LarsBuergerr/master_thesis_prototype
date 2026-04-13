import json
import sys
from pathlib import Path
from typing import Any, Dict, List

import requests


CKAN_BASE_URL = "https://ckan.govdata.de"
PACKAGE_SHOW_URL = f"{CKAN_BASE_URL}/api/3/action/package_show"


class GovDataCkanClient:
    def __init__(self, base_url: str = CKAN_BASE_URL, timeout: int = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.package_show_url = f"{self.base_url}/api/3/action/package_show"
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "govdata-ckan-client/0.1",
                "Accept": "application/json",
            }
        )

    def fetch_dataset_metadata(self, dataset_id: str) -> Dict[str, Any]:
        """
        Holt die vollständigen Metadaten eines Datensatzes über package_show.
        """
        response = self.session.get(
            self.package_show_url,
            params={"id": dataset_id},
            timeout=self.timeout,
        )
        response.raise_for_status()

        payload = response.json()

        if not payload.get("success", False):
            raise RuntimeError(
                f"CKAN API meldet success=false für Dataset-ID {dataset_id}: {payload}"
            )

        result = payload.get("result")
        if result is None:
            raise RuntimeError(
                f"CKAN API hat kein 'result' für Dataset-ID {dataset_id} geliefert."
            )

        return result

    def fetch_many(self, dataset_ids: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Holt Metadaten für mehrere Dataset-IDs.
        """
        results: Dict[str, Dict[str, Any]] = {}
        for dataset_id in dataset_ids:
            try:
                results[dataset_id] = self.fetch_dataset_metadata(dataset_id)
                print(f"[OK] {dataset_id}")
            except Exception as exc:
                print(f"[FEHLER] {dataset_id}: {exc}", file=sys.stderr)
        return results


def save_json(data: Any, output_path: Path) -> None:
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def print_summary(metadata: Dict[str, Any]) -> None:
    print("=" * 80)
    print(f"ID:          {metadata.get('id')}")
    print(f"Titel:       {metadata.get('title')}")
    print(f"Name:        {metadata.get('name')}")
    print(f"Publisher:   {((metadata.get('organization') or {}).get('title'))}")
    print(f"Erstellt:    {metadata.get('metadata_created')}")
    print(f"Aktualisiert:{metadata.get('metadata_modified')}")
    print(f"Lizenz:      {metadata.get('license_title')}")
    print(f"Anzahl Ressourcen: {len(metadata.get('resources', []))}")
    print()

    for i, resource in enumerate(metadata.get("resources", []), start=1):
        print(f"  Ressource {i}")
        print(f"    ID:      {resource.get('id')}")
        print(f"    Name:    {resource.get('name')}")
        print(f"    Format:  {resource.get('format')}")
        print(f"    URL:     {resource.get('url')}")
        print()


def main() -> None:
    """
    Nutzung:
        python govdata_ckan_fetch.py <dataset_id_1> [<dataset_id_2> ...]

    Beispiel:
        python govdata_ckan_fetch.py 832a64df-be7f-4fb8-8fd4-7190049e5bd4
    """
    if len(sys.argv) < 2:
        print(
            "Bitte mindestens eine Dataset-ID angeben.\n"
            "Beispiel:\n"
            "  python govdata_ckan_fetch.py 832a64df-be7f-4fb8-8fd4-7190049e5bd4"
        )
        sys.exit(1)

    dataset_ids = sys.argv[1:]
    client = GovDataCkanClient()

    results = client.fetch_many(dataset_ids)

    if not results:
        print("Keine Datensätze erfolgreich geladen.", file=sys.stderr)
        sys.exit(2)

    for dataset_id, metadata in results.items():
        print_summary(metadata)
        output_file = Path(f"{dataset_id}.json")
        save_json(metadata, output_file)
        print(f"JSON gespeichert in: {output_file.resolve()}")
        print()


if __name__ == "__main__":
    main()