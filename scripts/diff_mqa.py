"""List the differences between the local MQA baseline and the official MQA.

Compares the local scorer output (``src/score_mqa.py`` → e.g. ``run_output_mqa``)
against the official data.europa.eu report (``scripts/fetch_mqa_metrics.py`` →
e.g. ``mqa_output/extreme_cases_03.json``), per dataset:

  * total score and the five dimension scores, and
  * every individual metric (local ``passed`` vs. official ``met``).

Only differences are printed. Use it to validate that the local re-implementation
matches the original MQA.

Usage:
    python3 scripts/diff_mqa.py
    python3 scripts/diff_mqa.py run_output_mqa mqa_output/extreme_cases_03.json
"""

from __future__ import annotations

import json
import sys

# local metric key (score_mqa) -> official metric name (data.europa.eu)
LOCAL_TO_OFFICIAL = {
    "keyword_availability": "keywordAvailability",
    "category_availability": "categoryAvailability",
    "spatial_availability": "spatialAvailability",
    "temporal_availability": "temporalAvailability",
    "access_url_status_code": "accessUrlStatusCode",
    "download_url_availability": "downloadUrlAvailability",
    "download_url_status_code": "downloadUrlStatusCode",
    "format_availability": "formatAvailability",
    "media_type_availability": "mediaTypeAvailability",
    "format_media_type_vocabulary": "formatMediaTypeVocabularyAlignment",
    "format_non_proprietary": "formatMediaTypeNonProprietary",
    "format_machine_readable": "formatMediaTypeMachineInterpretable",
    "dcat_ap_compliance": "dcatApCompliance",
    "license_availability": "licenceAvailability",
    "known_license": "knownLicence",
    "access_rights_availability": "accessRightsAvailability",
    "access_rights_vocabulary": "accessRightsVocabularyAlignment",
    "contact_point_availability": "contactPointAvailability",
    "publisher_availability": "publisherAvailability",
    "rights_availability": "rightsAvailability",
    "byte_size_availability": "byteSizeAvailability",
    "date_issued_availability": "dateIssuedAvailability",
    "date_modified_availability": "dateModifiedAvailability",
}

DIMENSIONS = ["findability", "accessibility", "interoperability", "reusability", "contextuality"]


def _by_file(records: list[dict], key: str) -> dict[str, dict]:
    return {r[key]: r for r in records if r.get(key)}


def main() -> None:
    local_path = sys.argv[1] if len(sys.argv) > 1 else "run_output_mqa"
    official_path = sys.argv[2] if len(sys.argv) > 2 else "mqa_output/extreme_cases_03.json"

    local = _by_file(json.load(open(local_path)), "file")
    official_raw = json.load(open(official_path))
    official = _by_file(official_raw if isinstance(official_raw, list) else [official_raw], "source_file")

    only_local = sorted(set(local) - set(official))
    only_official = sorted(set(official) - set(local))
    common = sorted(set(local) & set(official))

    if only_local:
        print(f"Only in local ({local_path}): {', '.join(only_local)}")
    if only_official:
        print(f"Only in official ({official_path}): {', '.join(only_official)}")
    print(f"Comparing {len(common)} dataset(s) present in both.\n")

    total_mismatches = 0
    for fname in common:
        lo, of = local[fname], official[fname]
        lines: list[str] = []

        # total score (both on the 0..405 scale)
        if lo["total"] != of["total_score"]:
            lines.append(f"  total: local={lo['total']} official={of['total_score']} (Δ {lo['total'] - of['total_score']:+})")

        # dimension scores
        for dim in DIMENSIONS:
            l = lo["by_dimension"].get(dim, {}).get("score")
            o = of["dimension_scores"].get(dim)
            if l != o:
                lines.append(f"  dim {dim}: local={l} official={o}")

        # per-metric: local 'passed' vs official 'met'
        for lkey, okey in LOCAL_TO_OFFICIAL.items():
            l_passed = lo["metrics"].get(lkey, {}).get("passed")
            o_info = of["indicators"].get(okey)
            if o_info is None:
                continue  # not measured officially (e.g. no distribution)
            o_met = o_info["met"]
            if bool(l_passed) != bool(o_met):
                extra = ""
                if o_info.get("total_count", 1) > 1:
                    extra = f" [official {o_info['met_count']}/{o_info['total_count']} dists]"
                lines.append(f"  metric {lkey}: local={'PASS' if l_passed else 'fail'} official={'met' if o_met else 'not-met'}{extra}")

        if lines:
            total_mismatches += len(lines)
            print(f"### {fname}")
            print("\n".join(lines))
            print()

    print(f"{total_mismatches} difference(s) across {len(common)} dataset(s).")


if __name__ == "__main__":
    main()
