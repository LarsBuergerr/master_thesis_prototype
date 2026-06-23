"""Thin client for the ITB SHACL validation API (DCAT-AP.de)."""

import requests
from rdflib import Graph, Namespace, RDF

ITB_API_URL = "https://www.itb.ec.europa.eu/shacl/dcat-ap.de/api/validate"
VALIDATION_TYPE = "v20_de_spec"

SH = Namespace("http://www.w3.org/ns/shacl#")


def validate_graph(graph: Graph, *, timeout: int = 120) -> dict:
    """Validate an rdflib Graph against DCAT-AP.de v2.0 via the ITB SHACL API.

    Returns a dict::

        {
            "conforms": bool,
            "violation_count": int,
            "violations": [{"severity", "message", "focus", "path"}, ...]
        }

    Raises ``requests.HTTPError`` on non-2xx responses and
    ``requests.Timeout`` when the server does not respond in time.
    """
    content = graph.serialize(format="turtle")

    resp = requests.post(
        ITB_API_URL,
        json={
            "contentToValidate": content,
            "embeddingMethod": "STRING",
            "validationType": VALIDATION_TYPE,
            "contentSyntax": "text/turtle",
        },
        headers={"Content-Type": "application/json", "Accept": "text/turtle"},
        timeout=timeout,
    )
    resp.raise_for_status()

    report = Graph()
    report.parse(data=resp.text, format="turtle")

    conforms = next(
        (bool(o.toPython()) for o in report.objects(None, SH.conforms)),
        True,
    )

    violations = []
    for result in report.subjects(RDF.type, SH.ValidationResult):
        severity = next(report.objects(result, SH.resultSeverity), None)
        sev_label = str(severity).split("#")[-1] if severity else "?"
        message = str(next(report.objects(result, SH.resultMessage), ""))
        focus = str(next(report.objects(result, SH.focusNode), ""))
        path = next(report.objects(result, SH.resultPath), None)
        violations.append(
            {
                "severity": sev_label,
                "message": message,
                "focus": focus,
                "path": str(path) if path else None,
            }
        )

    return {
        "conforms": conforms,
        "violation_count": len(violations),
        "violations": violations,
    }
