"""Fetch the official data.europa.eu MQA metrics for a dataset.

Pulls the DQV quality report from
``https://data.europa.eu/api/hub/repo/datasets/{id}.jsonld/metrics`` and
extracts the values relevant for comparison:

  * the total score and the five dimension scores (authoritative, as computed
    by data.europa.eu),
  * every individual indicator with met / not-met and its maximum points,
  * SHACL violations (the reason behind dcatApCompliance).

Usage:
    python3 scripts/fetch_mqa_metrics.py <id> [<id> ...]
    python3 scripts/fetch_mqa_metrics.py <id> --json report.json
    python3 scripts/fetch_mqa_metrics.py --csv scores.csv <id1> <id2> ...
    python3 scripts/fetch_mqa_metrics.py --dir data/samples/<sample>_jsonld --csv scores.csv

An <id> is the value of the dataset's ``dct:identifier`` (which equals the
data.europa.eu dataset id), or a full dataset URL. With ``--dir`` the ids are
read straight from the ``dct:identifier`` of every ``.jsonld``/``.rdf`` file in
the directory. Datasets without a published MQA report (HTTP 404) are skipped.
"""

import csv
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict

import requests

URL = "https://data.europa.eu/api/hub/repo/datasets/{id}.jsonld/metrics"

# Official MQA rubric: indicator -> (dimension, max points).
# Source: piveau-metrics-score / piveau-dqv-vocabulary-default-score-values.ttl
INDICATORS = {
    # Findability (100)
    "keywordAvailability": ("findability", 30),
    "categoryAvailability": ("findability", 30),
    "spatialAvailability": ("findability", 20),
    "temporalAvailability": ("findability", 20),
    # Accessibility (100)
    "accessUrlStatusCode": ("accessibility", 50),
    "downloadUrlAvailability": ("accessibility", 20),
    "downloadUrlStatusCode": ("accessibility", 30),
    # Interoperability (110, +30 for the newer formatMatch/syntaxValid)
    "formatAvailability": ("interoperability", 20),
    "mediaTypeAvailability": ("interoperability", 10),
    "formatMediaTypeVocabularyAlignment": ("interoperability", 10),
    "formatMediaTypeNonProprietary": ("interoperability", 20),
    "formatMediaTypeMachineInterpretable": ("interoperability", 20),
    "dcatApCompliance": ("interoperability", 30),
    "formatMatch": ("interoperability", 15),
    "syntaxValid": ("interoperability", 15),
    # Reusability (75)
    "licenceAvailability": ("reusability", 20),
    "knownLicence": ("reusability", 10),
    "accessRightsAvailability": ("reusability", 10),
    "accessRightsVocabularyAlignment": ("reusability", 5),
    "contactPointAvailability": ("reusability", 20),
    "publisherAvailability": ("reusability", 10),
    # Contextuality (20)
    "rightsAvailability": ("contextuality", 5),
    "byteSizeAvailability": ("contextuality", 5),
    "dateIssuedAvailability": ("contextuality", 5),
    "dateModifiedAvailability": ("contextuality", 5),
}

DIMENSIONS = [
    "findability",
    "accessibility",
    "interoperability",
    "reusability",
    "contextuality",
]
SCORE_KEYS = {f"{d}Scoring": d for d in DIMENSIONS}  # findabilityScoring -> findability


def local_name(uri: str) -> str:
    return re.split(r"[#/]", uri.rstrip("/"))[-1]


def extract_id(token: str) -> str:
    """Accept a bare UUID or any data.europa.eu dataset URL/path."""
    m = re.search(r"datasets?/([0-9a-fA-F-]{8,}[0-9a-zA-Z._~-]*)", token)
    return m.group(1) if m else token


def cast_value(value_node):
    """Return a python bool/int/str from a dqv:value JSON-LD node."""
    if isinstance(value_node, dict):
        raw, dtype = value_node.get("@value"), value_node.get("@type", "")
    else:
        raw, dtype = value_node, ""
    if "boolean" in dtype:
        return raw == "true"
    if "int" in dtype or "decimal" in dtype:
        try:
            return int(raw)
        except (TypeError, ValueError):
            return raw
    return raw


def is_met(indicator: str, value) -> bool:
    """Whether an indicator counts as fulfilled."""
    if indicator.endswith("StatusCode"):
        return isinstance(value, int) and 200 <= value < 400
    return value is True


class NoReport(Exception):
    """The dataset has no published MQA report (HTTP 404)."""


def fetch_metrics(dataset_id: str) -> dict:
    """Fetch the metrics report, retrying with a lowercased id.

    data.europa.eu stores ids lowercased, so an uppercase UUID 404s as-is.
    """
    for candidate in dict.fromkeys([dataset_id, dataset_id.lower()]):
        resp = requests.get(
            URL.format(id=candidate),
            timeout=60,
            headers={"Accept": "application/ld+json"},
        )
        if resp.status_code == 404:
            continue
        resp.raise_for_status()
        return resp.json()
    raise NoReport(f"no MQA report for '{dataset_id}'")


def identifier_from_file(path: str) -> str:
    """Read the dataset-level dct:identifier from a .jsonld or .rdf file."""
    if path.endswith(".jsonld") or path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            doc = json.load(f)
        nodes = doc.get("@graph", doc if isinstance(doc, list) else [doc])
        datasets = [n for n in nodes if "Dataset" in str(n.get("@type", ""))]
        node = datasets[0] if datasets else nodes[0]
        ident = node.get("dct:identifier") or node.get(
            "http://purl.org/dc/terms/identifier"
        )
        if isinstance(ident, list):
            ident = ident[0]
        if isinstance(ident, dict):
            # A literal is used as-is; an @id URI -> trailing path segment.
            if ident.get("@value") is not None:
                return ident["@value"]
            return local_name(ident["@id"]) if ident.get("@id") else None
        return ident

    # RDF/XML: first dct:identifier under a dcat:Dataset.
    dct, dcat = "http://purl.org/dc/terms/", "http://www.w3.org/ns/dcat#"
    rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
    root = ET.parse(path).getroot()
    for dataset in root.iter(f"{{{dcat}}}Dataset"):
        ident = dataset.find(f"{{{dct}}}identifier")
        if ident is None:
            continue
        if ident.text and ident.text.strip():
            return ident.text.strip()
        resource = ident.get(f"{{{rdf}}}resource")  # @id form
        if resource:
            return local_name(resource)
    return None


def parse_report(doc: dict, dataset_id: str) -> dict:
    graph = doc.get("@graph", [])

    dimension_scores = {}
    total = None
    indicators = defaultdict(list)  # name -> [values across dataset/distributions]
    shacl_violations = []

    for node in graph:
        ntype = node.get("@type")
        if ntype == "dqv:QualityMeasurement":
            name = local_name(node.get("dqv:isMeasurementOf", {}).get("@id", ""))
            value = cast_value(node.get("dqv:value"))
            if name == "scoring":
                total = value
            elif name in SCORE_KEYS:
                dimension_scores[SCORE_KEYS[name]] = value
            elif name in INDICATORS:
                indicators[name].append(value)
        elif ntype == "shacl:ValidationResult":
            shacl_violations.append(
                {
                    "focusNode": _ref(node.get("shacl:focusNode")),
                    "path": local_name(_ref(node.get("shacl:resultPath")) or ""),
                    "message": _text(node.get("shacl:resultMessage")),
                    "severity": local_name(
                        _ref(node.get("shacl:resultSeverity")) or ""
                    ),
                }
            )

    # Build per-indicator summary with met/not-met and points.
    per_indicator = {}
    earned_by_dim = defaultdict(int)
    for name, (dim, maxpts) in INDICATORS.items():
        if name not in indicators:
            continue
        values = indicators[name]
        met_count = sum(1 for v in values if is_met(name, v))
        met = met_count > 0  # MQA awards points on the best-scoring distribution
        per_indicator[name] = {
            "dimension": dim,
            "met": met,
            "met_count": met_count,
            "total_count": len(values),
            "max_points": maxpts,
            "raw_values": values,
        }

    return {
        "dataset_id": dataset_id,
        "source_file": None,
        "total_score": total,
        "dimension_scores": {d: dimension_scores.get(d) for d in DIMENSIONS},
        "indicators": per_indicator,
        "shacl_violations": shacl_violations,
    }


def _ref(node):
    return node.get("@id") if isinstance(node, dict) else node


def _text(node):
    if isinstance(node, dict):
        return node.get("@value")
    return node


def print_report(report: dict) -> None:
    print("=" * 72)
    if report.get("source_file"):
        print(f"File:    {report['source_file']}")
    print(f"Dataset: {report['dataset_id']}")
    print(f"TOTAL SCORE: {report['total_score']} / 405")
    print("=" * 72)
    for dim in DIMENSIONS:
        score = report["dimension_scores"].get(dim)
        print(f"\n{dim.upper()}: {score}")
        for name, info in report["indicators"].items():
            if info["dimension"] != dim:
                continue
            mark = "✓" if info["met"] else "✗"
            detail = ""
            if info["total_count"] > 1:
                detail = f"  ({info['met_count']}/{info['total_count']} distributions)"
            raw = info["raw_values"]
            raw_str = raw[0] if len(raw) == 1 else raw
            print(
                f"  [{mark}] {name:<38} {info['max_points']:>3}p   value={raw_str}{detail}"
            )

    if report["shacl_violations"]:
        print(f"\nSHACL violations ({len(report['shacl_violations'])}):")
        for v in report["shacl_violations"]:
            print(f"  - {v['severity']:<8} path={v['path']:<20} {v['message']}")
    print()


def to_flat_row(report: dict) -> dict:
    row = {
        "source_file": report.get("source_file") or "",
        "dataset_id": report["dataset_id"],
        "total_score": report["total_score"],
    }
    for d in DIMENSIONS:
        row[d] = report["dimension_scores"].get(d)
    for name, info in report["indicators"].items():
        row[name] = int(info["met"])
    return row


def main() -> None:
    args = sys.argv[1:]
    json_path = csv_path = sample_dir = None
    if "--json" in args:
        i = args.index("--json")
        json_path = args[i + 1]
        del args[i : i + 2]
    if "--csv" in args:
        i = args.index("--csv")
        csv_path = args[i + 1]
        del args[i : i + 2]
    if "--dir" in args:
        i = args.index("--dir")
        sample_dir = args[i + 1]
        del args[i : i + 2]

    # Build the work list of (id, source_file). Prefer .jsonld over .rdf.
    work = []
    if sample_dir:
        files = sorted(
            glob.glob(os.path.join(sample_dir, "*.jsonld"))
            or glob.glob(os.path.join(sample_dir, "*.rdf"))
        )
        for path in files:
            try:
                ident = identifier_from_file(path)
            except Exception as exc:
                print(
                    f"SKIP {os.path.basename(path)}: kann identifier nicht lesen ({exc})",
                    file=sys.stderr,
                )
                continue
            if not ident:
                print(
                    f"SKIP {os.path.basename(path)}: kein dct:identifier",
                    file=sys.stderr,
                )
                continue
            work.append((ident, os.path.basename(path)))
    work += [(extract_id(a), None) for a in args]

    if not work:
        print(__doc__)
        sys.exit(1)

    reports, no_report = [], []
    for dataset_id, source in work:
        try:
            report = parse_report(fetch_metrics(dataset_id), dataset_id)
        except NoReport:
            no_report.append((dataset_id, source))
            print(f"--   kein MQA-Bericht: {source or dataset_id}", file=sys.stderr)
            continue
        except Exception as exc:
            print(f"FAIL {source or dataset_id}: {exc}", file=sys.stderr)
            continue
        report["source_file"] = source
        reports.append(report)
        print_report(report)

    print(f"\n{len(reports)} Berichte geladen, {len(no_report)} ohne Bericht (404).")

    if json_path:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(
                reports if len(reports) > 1 else reports[0],
                f,
                indent=2,
                ensure_ascii=False,
            )
        print(f"JSON geschrieben: {json_path}")

    if csv_path and reports:
        rows = [to_flat_row(r) for r in reports]
        fieldnames = list({k for row in rows for k in row})
        # stable column order: meta, dimensions, then indicators
        ordered = ["source_file", "dataset_id", "total_score", *DIMENSIONS]
        ordered += [k for k in INDICATORS if k in fieldnames]
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=ordered)
            writer.writeheader()
            writer.writerows(rows)
        print(f"CSV geschrieben: {csv_path}")


if __name__ == "__main__":
    main()
