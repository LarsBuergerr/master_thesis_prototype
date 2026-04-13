import requests
import json
from collections import defaultdict

ENDPOINT = "https://www.govdata.de/shacl/validation/mqa"

URI = "https://ckan.govdata.de/dataset/57df0dfa-2a77-42f4-b52b-2469de320bc5"

QUERY = """
PREFIX shacl: <http://www.w3.org/ns/shacl#>
PREFIX rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dqv:   <http://www.w3.org/ns/dqv#>

SELECT ?report ?result ?p ?o
WHERE {
  ?report rdf:type shacl:ValidationReport ;
          dqv:computedOn <""" + URI + """> ;
          shacl:result ?result .

  ?result ?p ?o .
}
ORDER BY ?report ?result ?p
"""

print(QUERY)

def run_query():
    response = requests.get(
        ENDPOINT,
        params={"query": QUERY},
        headers={
            "Accept": "application/sparql-results+json",
            "User-Agent": "govdata-validation-fetcher/1.0",
        },
        timeout=60,
    )

    print("HTTP status:", response.status_code)

    response.raise_for_status()
    return response.json()


def print_results(data):
    bindings = data.get("results", {}).get("bindings", [])
    print(f"Rows: {len(bindings)}")

    for row in bindings:
        report = row["report"]["value"]
        result = row["result"]["value"]
        p = row["p"]["value"]
        o = row["o"]["value"]

        print(f"report={report}")
        print(f"result={result}")
        print(f"{p} -> {o}")
        print()



def group_results(data):
    grouped = defaultdict(dict)

    for row in data["results"]["bindings"]:
        print(row["result"]["value"], row["p"]["value"], row["o"]["value"])

    # for row in data["results"]["bindings"]:
    #     result = row["result"]["value"]
    #     p = row["p"]["value"]
    #     o = row["o"]["value"]

    #     grouped[result][p] = o

    # for result, values in grouped.items():
    #     print()

    #     print("FocusNode:", values.get("http://www.w3.org/ns/shacl#focusNode"))
    #     print("Message:", values.get("http://www.w3.org/ns/shacl#resultMessage"))
    #     print("Severity:", values.get("http://www.w3.org/ns/shacl#resultSeverity"))
    #     print("Path:", values.get("http://www.w3.org/ns/shacl#resultPath"))
    #     print("Constraint:", values.get("http://www.w3.org/ns/shacl#sourceConstraintComponent"))

    # print("Total unique results:", len(grouped))

if __name__ == "__main__":
    data = run_query()
    group_results(data)
