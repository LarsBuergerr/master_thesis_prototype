"""Validate the local MQA baseline against the official report on IDENTICAL input.

The official report scores the data.europa.eu *harvested* copy of a dataset,
which differs from the local source files (the harvest drops properties). To
validate the metric LOGIC rather than the metadata, this fetches each dataset's
harvested ``.jsonld`` from data.europa.eu, scores it with the local baseline and
compares per metric.

Expected residual divergences (NOT logic bugs), reported separately:
  * dcat_ap_compliance   -> local defaults True vs official real SHACL
  * *_url_status_code     -> not probed here (offline) vs official harvest probe
  * format literals       -> intentional URI-strict handling (see scorer docstring)

Usage:
  python3 scripts/validate_mqa.py mqa_output/sample_2026-06-03_13-33.json
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import requests
from rdflib import Graph

from extraction.dataset_context import DatasetContext
from mqa.scorer import MqaOptions, score_dataset

DATASET_URL = "https://data.europa.eu/api/hub/repo/datasets/{id}.jsonld"

LOCAL_TO_OFFICIAL = {
    "keyword_availability": "keywordAvailability", "category_availability": "categoryAvailability",
    "spatial_availability": "spatialAvailability", "temporal_availability": "temporalAvailability",
    "access_url_status_code": "accessUrlStatusCode", "download_url_availability": "downloadUrlAvailability",
    "download_url_status_code": "downloadUrlStatusCode", "format_availability": "formatAvailability",
    "media_type_availability": "mediaTypeAvailability", "format_media_type_vocabulary": "formatMediaTypeVocabularyAlignment",
    "format_non_proprietary": "formatMediaTypeNonProprietary", "format_machine_readable": "formatMediaTypeMachineInterpretable",
    "dcat_ap_compliance": "dcatApCompliance", "license_availability": "licenceAvailability", "known_license": "knownLicence",
    "access_rights_availability": "accessRightsAvailability", "access_rights_vocabulary": "accessRightsVocabularyAlignment",
    "contact_point_availability": "contactPointAvailability", "publisher_availability": "publisherAvailability",
    "rights_availability": "rightsAvailability", "byte_size_availability": "byteSizeAvailability",
    "date_issued_availability": "dateIssuedAvailability", "date_modified_availability": "dateModifiedAvailability",
}

# Divergences that are expected by design (network timing / SHACL default).
EXPECTED = {"access_url_status_code", "download_url_status_code", "dcat_ap_compliance"}


def fetch_graph(dataset_id: str):
    for cand in dict.fromkeys([dataset_id, dataset_id.lower()]):
        resp = requests.get(DATASET_URL.format(id=cand), timeout=60,
                            headers={"Accept": "application/ld+json"})
        if resp.status_code == 404:
            continue
        resp.raise_for_status()
        g = Graph()
        g.parse(data=resp.text, format="json-ld")
        return g
    return None


def main() -> None:
    official = json.load(open(sys.argv[1]))
    if isinstance(official, dict):
        official = [official]

    core_agree = core_total = 0
    core_mismatch = Counter()        # metric -> count (logic-relevant only)
    expected_mismatch = Counter()    # metric -> count (dcat_ap / url-status)
    n = skipped = 0

    for rec in official:
        graph = fetch_graph(rec["dataset_id"])
        if graph is None:
            skipped += 1
            continue
        n += 1
        # offline: no probes -> url-status local=fail (expected divergence)
        local = score_dataset(DatasetContext.from_graph(graph), MqaOptions())
        for lk, ok in LOCAL_TO_OFFICIAL.items():
            oi = rec["indicators"].get(ok)
            if oi is None:
                continue
            lp = bool(local["metrics"].get(lk, {}).get("passed"))
            om = bool(oi["met"])
            if lk in EXPECTED:
                if lp != om:
                    expected_mismatch[lk] += 1
                continue
            core_total += 1
            if lp == om:
                core_agree += 1
            else:
                src = rec.get("source_file") or rec["dataset_id"]
                core_mismatch[lk] += 1

    print(f"Validated {n} dataset(s) on harvested .jsonld ({skipped} skipped: no report).\n")
    pct = 100 * core_agree / core_total if core_total else 0
    print(f"Core (logic) metrics agreement: {core_agree}/{core_total}  ({pct:.1f}%)")
    if core_mismatch:
        print("\nCore mismatches (potential logic gaps — investigate):")
        for k, c in core_mismatch.most_common():
            print(f"  {k:34} {c}/{n}")
    else:
        print("  -> no logic mismatches. Baseline matches official MQA on identical input.")
    print("\nExpected divergences (by design, not logic):")
    for k in EXPECTED:
        print(f"  {k:34} {expected_mismatch.get(k, 0)}/{n}")


if __name__ == "__main__":
    main()
