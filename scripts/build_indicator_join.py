#!/usr/bin/env python3
"""Run the indicator-level prototype-vs-MQA join on a sample and write the CSVs.

Scores every ``*.rdf`` in a sample directory with BOTH the prototype and the MQA
baseline on identical input, joins them per indicator via the A/B/C mapping
(``src/evaluation/indicator_map.py``), and writes all output into a named
subdirectory of ``outputs/mqa_comparison/``:

  outputs/mqa_comparison/<name>/model_indicators.csv      – prototype, one row per (file, indicator)
  outputs/mqa_comparison/<name>/mqa_metrics.csv           – MQA, one row per (file, metric)
  outputs/mqa_comparison/<name>/indicator_join.csv        – the joined long table (core artifact)
  outputs/mqa_comparison/<name>/class_b_overestimation.csv
  outputs/mqa_comparison/<name>/class_c_blindness.csv

It also prints the headline numbers (A agreement, B overestimation, class
counts, unmapped indicators, MQA-only metrics).

Usage (from repo root):
    python3 scripts/build_indicator_join.py                              # newest data/sample_*
    python3 scripts/build_indicator_join.py data/sample_2026-06-18_13-45
    python3 scripts/build_indicator_join.py --output-name my_run_01      # custom output name
    python3 scripts/build_indicator_join.py --output-dir results         # custom output dir
    python3 scripts/build_indicator_join.py --no-llm --no-probe          # fast/offline
    python3 scripts/build_indicator_join.py --no-shacl                   # skip ITB API calls
    python3 scripts/build_indicator_join.py --recompute                  # ignore caches

Needs ``OPENROUTER_API_KEY`` (in ``.env``) for the expressiveness (C) indicators;
without it they report not_applicable and the C-blindness table is empty.

The ITB SHACL API (https://www.itb.ec.europa.eu/shacl/dcat-ap.de/api/validate) is
called for both the prototype ``reuse_dcat_ap_de_compliance`` indicator and the MQA
``dcat_ap_compliance`` metric. Use ``--no-shacl`` to skip both and fall back to the
MQA default (awarded = True).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "src"))

from dotenv import load_dotenv  # noqa: E402

load_dotenv(REPO / ".env")


def _newest_sample() -> Path:
    samples = sorted((REPO / "data").glob("sample_*"))
    if not samples:
        raise SystemExit("no data/sample_* directory found")
    return samples[-1]


def _default_output_name(sample_dir: Path) -> str:
    return sample_dir.name


def main() -> None:
    ap = argparse.ArgumentParser(description="Prototype-vs-MQA indicator join")
    ap.add_argument(
        "sample_dir",
        nargs="?",
        default=None,
        help="sample dir (default: newest data/sample_*)",
    )
    ap.add_argument(
        "--output-name",
        default=None,
        help="name of the subdirectory inside --output-dir (default: sample dir name)",
    )
    ap.add_argument(
        "--output-dir",
        default="outputs/mqa_comparison",
        help="root output directory (default: outputs/mqa_comparison)",
    )
    ap.add_argument(
        "--no-llm",
        action="store_true",
        help="skip the LLM (expressiveness C-indicators = not_applicable)",
    )
    ap.add_argument(
        "--no-probe",
        action="store_true",
        help="skip HTTP probes (URL-status metrics score 0/FAIL)",
    )
    ap.add_argument(
        "--no-shacl",
        action="store_true",
        help="skip ITB SHACL API calls — MQA dcat_ap_compliance defaults to True",
    )
    ap.add_argument(
        "--recompute",
        action="store_true",
        help="ignore caches and re-score",
    )
    args = ap.parse_args()

    sample_dir = Path(args.sample_dir) if args.sample_dir else _newest_sample()
    if not sample_dir.is_absolute():
        sample_dir = REPO / sample_dir
    if not sample_dir.is_dir():
        raise SystemExit(f"not a directory: {sample_dir}")

    output_name = args.output_name or _default_output_name(sample_dir)
    output_root = Path(args.output_dir)
    if not output_root.is_absolute():
        output_root = REPO / output_root
    output_dir = output_root / output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    from evaluation import ground_truth as gt
    from evaluation import indicator_join as ij
    from mqa.scorer import MqaOptions

    llm = None if args.no_llm else gt.make_llm()
    mqa_opts = MqaOptions(
        dcat_ap_compliant=True,
        shacl_validation=not args.no_shacl,
    )

    print(f"sample     : {sample_dir}")
    print(f"output     : {output_dir}")
    print(f"LLM        : {'on' if llm else 'off (expressiveness = N/A)'}")
    print(f"probe      : {'off' if args.no_probe else 'on'}")
    print(f"SHACL API  : {'off (MQA default=True)' if args.no_shacl else 'on (ITB API)'}\n")

    res = ij.build_all(
        sample_dir,
        llm=llm,
        probe=not args.no_probe,
        recompute=args.recompute,
        output_dir=output_dir,
        mqa_options=mqa_opts,
    )
    join = res["join"]

    res["class_b"].to_csv(output_dir / "class_b_overestimation.csv", index=False)
    res["class_c"].to_csv(output_dir / "class_c_blindness.csv", index=False)

    print("\n================ ERGEBNIS ================")
    print(
        f"join rows         : {len(join)}  "
        f"({join['file'].nunique()} datasets × {join['indicator'].nunique()} indicators)"
    )
    print(f"A/B/C indicators  : {res['class_counts']}")
    if res["unmapped_indicators"]:
        print(
            f"UNMAPPED          : {res['unmapped_indicators']}  ← add to indicator_map.py"
        )

    a = res["class_a"]
    if a["n"]:
        print(
            f"\n[A] Konvergenz (H1): {a['agreement']:.1%} Übereinstimmung "
            f"über n={a['n']} (file×indicator)"
        )
        print(
            f"    both_pass={a['both_pass']}  both_fail={a['both_fail']}  "
            f"MQA-PASS/Modell-FAIL={a['mqa_pass_model_fail']}  "
            f"Modell-PASS/MQA-FAIL={a['model_pass_mqa_fail']}"
        )
    else:
        print("\n[A] keine vergleichbaren Fälle")

    print("\n[B] Überschätzung (H2): MQA PASS & Prototyp FAIL/PARTIAL je Indikator")
    if res["class_b"].empty:
        print("    (keine B-Fälle)")
    else:
        for _, r in res["class_b"].iterrows():
            flag = " *review*" if r["review"] else ""
            print(
                f"    {r['indicator']:<32} {int(r['mqa_pass_model_fail']):>3}/{int(r['n']):<3} "
                f"({r['overestimation_rate']:.0%}){flag}"
            )

    print("\n[C] Blindheit (H2): Prototyp-Score-Verteilung, MQA hat keine Metrik")
    if res["class_c"].empty:
        print("    (keine C-Scores — LLM aus?)")
    else:
        for _, r in res["class_c"].iterrows():
            print(
                f"    {r['indicator']:<36} mean={r['model_score_mean']:.2f} "
                f"std={r['model_score_std']:.2f}  <0.5: {int(r['n_below_0_5'])}/{int(r['n'])}"
            )

    print(f"\n[Balance] MQA prüft, Prototyp nicht: {res['mqa_only_metrics']}")
    print(f"\ngeschrieben nach: {output_dir}/")


if __name__ == "__main__":
    main()
