"""Simple example of using the quality metrics service.

No pipeline, no framework - just straightforward validation.
"""

from scoring.service import QualityMetricsService
from core.dimension import QualityDimension
import json
from pathlib import Path


def main():
    """Example: Validate metadata and print results."""

    # Create service
    service = QualityMetricsService(max_workers=4)

    # Example 1: Validate entire metadata file
    print("=" * 80)
    print("EXAMPLE 1: Validate Entire Metadata File")
    print("=" * 80)

    metadata_path = "data/13315/metadata.rdf"
    if not Path(metadata_path).exists():
        print(f"File not found: {metadata_path}")
        return

    results = service.validate_metadata(metadata_path)

    # Print summary
    summary = results.get("summary", {})
    print(f"\n📊 OVERALL QUALITY SCORE")
    print(f"  Score: {summary.get('overall_score', 0):.2f} / 1.0")
    print(f"  Grade: {summary.get('quality_grade', 'N/A')}")
    print(f"  Pass Rate: {summary.get('overall_pass_rate', 0):.1%}")

    # Print dimension scores
    print(f"\n📈 DIMENSION SCORES")
    for dim_name, score in summary.get("dimension_scores", {}).items():
        print(f"  {dim_name:20s}: {score:.2f}")

    # ─────────────────────────────────────────────────────────────────

    # Example 2: Validate single dimension
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Validate Single Dimension")
    print("=" * 80)

    from rdflib import Graph

    # Parse the metadata first
    metadata = Graph()
    metadata.parse(metadata_path)

    # Validate only Findability
    dim_results = service.validate_dimension(metadata, QualityDimension.FINDABILITY)

    print(f"\n{QualityDimension.FINDABILITY.value.upper()}")
    print(f"  Score: {dim_results.get('score'):.2f}")
    print(f"  Pass Rate: {dim_results.get('pass_rate'):.1%}")
    print(f"  Indicators:")

    for indicator in dim_results.get("indicators", []):
        status = indicator.get("status", "unknown")
        ind_id = indicator.get("indicator_id", "unknown")
        score = indicator.get("score", 0)
        print(f"    [{status:8s}] {ind_id:30s} (score: {score:.2f})")

    # ─────────────────────────────────────────────────────────────────

    # Example 3: Validate single indicator
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Validate Single Indicator")
    print("=" * 80)

    indicator_result = service.validate_indicator(metadata, "find_keywords_count")

    print(f"\nIndicator: {indicator_result.get('indicator_id')}")
    print(f"  Status: {indicator_result.get('status')}")
    print(f"  Score: {indicator_result.get('score'):.2f}")
    print(f"  Message: {indicator_result.get('message_de', 'N/A')}")

    if indicator_result.get("details"):
        print(f"  Details:")
        for key, value in indicator_result.get("details").items():
            print(f"    {key}: {value}")

    # ─────────────────────────────────────────────────────────────────

    # Save results to JSON
    print("\n" + "=" * 80)
    results_file = Path("quality_results.json")

    # Prepare JSON-serializable results
    json_results = {"summary": summary, "by_dimension": {}}

    for dim_name, dim_results_data in results.get("by_dimension", {}).items():
        json_results["by_dimension"][dim_name] = {
            "score": dim_results_data.get("score"),
            "pass_rate": dim_results_data.get("pass_rate"),
            "indicator_count": dim_results_data.get("indicator_count"),
            "pass_count": dim_results_data.get("pass_count"),
        }

    with open(results_file, "w") as f:
        json.dump(json_results, f, indent=2)

    print(f"Results saved to: {results_file}")
    print("=" * 80)


if __name__ == "__main__":
    main()
