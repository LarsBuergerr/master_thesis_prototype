"""Fetch a sample as JSON-LD instead of RDF/XML.

Reads the `sample_manifest.csv` produced by notebook 01 and downloads each
dataset from the GovData CKAN DCAT endpoint as JSON-LD, mirroring the RDF
file names (``*.rdf`` -> ``*.jsonld``).

Usage:
    python3 scripts/fetch_sample_jsonld.py data/samples/sample_2026-06-03_13-33
"""

import csv
import re
import sys
from pathlib import Path

import requests

URL_PATTERNS = [
    "https://www.govdata.de/dataset/{name}.jsonld",
    "https://www.govdata.de/ckan/dataset/{name}.jsonld",
    "https://govdata.de/dataset/{name}.jsonld",
    "https://govdata.de/ckan/dataset/{name}.jsonld",
]


def create_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "govdata-jsonld-sampler/0.1",
            "Accept": "application/ld+json, application/json;q=0.9, */*;q=0.1",
        }
    )
    return session


def fetch_dataset_jsonld(session: requests.Session, name: str, timeout: int = 60) -> bytes:
    for pattern in URL_PATTERNS:
        url = pattern.format(name=name)
        try:
            response = session.get(url, timeout=timeout, allow_redirects=True)
        except requests.RequestException:
            continue

        if response.status_code != 200:
            continue

        body = response.content[:200].lstrip().lower()
        content_type = (response.headers.get("Content-Type") or "").lower()
        if body.startswith(b"{") or "json" in content_type:
            return response.content

    raise RuntimeError(f"Kein JSON-LD-Endpunkt erfolgreich fuer Dataset '{name}'.")


def main() -> None:
    sample_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "data/samples/sample_2026-06-03_13-33")
    manifest_path = sample_dir / "sample_manifest.csv"
    if not manifest_path.exists():
        raise FileNotFoundError(f"{manifest_path} nicht gefunden.")

    out_dir = sample_dir.parent / f"{sample_dir.name}_jsonld"
    out_dir.mkdir(parents=True, exist_ok=True)

    with manifest_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    session = create_session()
    saved, failed = 0, []

    for i, row in enumerate(rows, 1):
        name = row["dataset_name"].strip()
        # Mirror the RDF file name: *.rdf -> *.jsonld
        rdf_name = Path(row["file_path"]).name
        out_path = out_dir / (Path(rdf_name).stem + ".jsonld")

        try:
            data = fetch_dataset_jsonld(session, name)
            out_path.write_bytes(data)
            saved += 1
            print(f"[{i:2d}/{len(rows)}] OK   {name} -> {out_path.name}")
        except Exception as exc:
            failed.append((name, str(exc)))
            print(f"[{i:2d}/{len(rows)}] FAIL {name} ({exc})")

    print()
    print(f"Gespeichert: {saved}/{len(rows)} JSON-LD-Dateien in {out_dir}")
    if failed:
        print("Fehler:")
        for name, err in failed:
            print(f"  - {name}: {err}")


if __name__ == "__main__":
    main()
