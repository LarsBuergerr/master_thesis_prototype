#!/usr/bin/env python3
"""Run the indicator-level prototype-vs-MQA join on a sample and write the CSVs.

Scores every ``*.rdf`` in a sample directory with BOTH the prototype and the MQA
baseline on identical input, joins them per indicator via the A/B/C mapping
(``src/evaluation/indicator_map.py``), and writes:

  model_indicators.csv  – prototype, one row per (file, indicator)
  mqa_metrics.csv       – MQA, one row per (file, metric)
  indicator_join.csv    – the joined long table (the core artifact)
  class_b_overestimation.csv / class_c_blindness.csv – evidence tables

It also prints the headline numbers (A agreement, B overestimation, class
counts, unmapped indicators, MQA-only metrics).

Usage (from repo root):
    python3 scripts/build_indicator_join.py                         # newest data/sample_*
    python3 scripts/build_indicator_join.py data/sample_2026-06-18_13-45
    python3 scripts/build_indicator_join.py --no-llm --no-probe     # fast/offline
    python3 scripts/build_indicator_join.py --recompute             # ignore caches

Needs ``OPENROUTER_API_KEY`` (in ``.env``) for the expressiveness (C) indicators;
without it they report not_applicable and the C-blindness table is empty.
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


def main() -> None:
    ap = argparse.ArgumentParser(description="Prototype-vs-MQA indicator join")
    ap.add_argument("sample_dir", nargs="?", default=None, help="sample dir (default: newest data/sample_*)")
    ap.add_argument("--no-llm", action="store_true", help="skip the LLM (expressiveness C-indicators = not_applicable)")
    ap.add_argument("--no-probe", action="store_true", help="skip HTTP probes (URL-status metrics score 0/FAIL)")
    ap.add_argument("--recompute", action="store_true", help="ignore caches and re-score")
    args = ap.parse_args()

    sample_dir = Path(args.sample_dir) if args.sample_dir else _newest_sample()
    if not sample_dir.is_absolute():
        sample_dir = REPO / sample_dir
    if not sample_dir.is_dir():
        raise SystemExit(f"not a directory: {sample_dir}")

    from evaluation import ground_truth as gt
    from evaluation import indicator_join as ij

    llm = None if args.no_llm else gt.make_llm()
    print(f"sample : {sample_dir}")
    print(f"LLM    : {'on' if llm else 'off (expressiveness = N/A)'}")
    print(f"probe  : {'off' if args.no_probe else 'on'}\n")

    res = ij.build_all(sample_dir, llm=llm, probe=not args.no_probe, recompute=args.recompute)
    join = res["join"]

    # Persist the two evidence tables alongside the join.
    res["class_b"].to_csv(sample_dir / "class_b_overestimation.csv", index=False)
    res["class_c"].to_csv(sample_dir / "class_c_blindness.csv", index=False)

    print("\n================ ERGEBNIS ================")
    print(f"join rows         : {len(join)}  ({join['file'].nunique()} datasets × {join['indicator'].nunique()} indicators)")
    print(f"A/B/C indicators  : {res['class_counts']}")
    if res["unmapped_indicators"]:
        print(f"UNMAPPED          : {res['unmapped_indicators']}  ← add to indicator_map.py")

    a = res["class_a"]
    print(f"\n[A] Konvergenz (H1): {a['agreement']:.1%} Übereinstimmung über n={a['n']} (file×indicator)" if a["n"] else "\n[A] keine vergleichbaren Fälle")
    if a["n"]:
        print(f"    both_pass={a['both_pass']}  both_fail={a['both_fail']}  "
              f"MQA-PASS/Modell-FAIL={a['mqa_pass_model_fail']}  Modell-PASS/MQA-FAIL={a['model_pass_mqa_fail']}")

    print("\n[B] Überschätzung (H2): MQA PASS & Prototyp FAIL/PARTIAL je Indikator")
    if res["class_b"].empty:
        print("    (keine B-Fälle)")
    else:
        for _, r in res["class_b"].iterrows():
            flag = " *review*" if r["review"] else ""
            print(f"    {r['indicator']:<28} {int(r['mqa_pass_model_fail']):>3}/{int(r['n']):<3} "
                  f"({r['overestimation_rate']:.0%}){flag}")

    print("\n[C] Blindheit (H2): Prototyp-Score-Verteilung, MQA hat keine Metrik")
    if res["class_c"].empty:
        print("    (keine C-Scores — LLM aus?)")
    else:
        for _, r in res["class_c"].iterrows():
            print(f"    {r['indicator']:<32} mean={r['model_score_mean']:.2f} "
                  f"std={r['model_score_std']:.2f}  <0.5: {int(r['n_below_0_5'])}/{int(r['n'])}")

    print(f"\n[Balance] MQA prüft, Prototyp nicht: {res['mqa_only_metrics']}")
    print(f"\ngeschrieben nach: {sample_dir}/  (indicator_join.csv u. a.)")


if __name__ == "__main__":
    main()
