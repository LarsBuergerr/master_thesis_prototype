#!/usr/bin/env python3
"""Export the indicator guidance for offline use in the frontend.

The portal page must stay readable when no backend is running (it then shows
the stored evaluation results). Since Klarnamen, Feldangaben und
Handlungsanweisungen ab sofort aus :mod:`core.guidance` kommen, wird hier ein
Abzug erzeugt, den das Frontend bündelt und benutzt, solange
``GET /indicators`` nicht erreichbar ist.

Der Abzug ist ein *generiertes Artefakt* — Quelle der Wahrheit bleibt
``src/core/guidance.py``. Nach Textänderungen neu ausführen:

    python3 scripts/export_indicator_guidance.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from core.dimension import QualityDimension  # noqa: E402
from core.guidance import (  # noqa: E402
    DIMENSION_GUIDANCE,
    SCORE_GLOSSARY,
    guidance_for,
)
from core.indicator import Indicator  # noqa: E402

DEFAULT_OUT = ROOT / "frontend" / "src" / "portal" / "data" / "indicator_guidance.json"


def build_payload() -> dict:
    """Same shape as the ``GET /indicators`` response (subset)."""
    import scoring.indicators  # noqa: F401  (triggers auto-registration)

    indicators = []
    for ind_id, ind in sorted(Indicator.all().items()):
        guidance = guidance_for(ind_id)
        indicators.append(
            {
                "indicator_id": ind_id,
                "name_de": ind.name_de,
                "dimension": ind.dimension.value,
                "default_weight": ind.weight,
                "guidance": guidance.to_dict() if guidance else None,
            }
        )

    return {
        "indicators": indicators,
        "dimension_info": [
            {
                "dimension": d.value,
                "label_de": DIMENSION_GUIDANCE.get(d.value, {}).get("label_de", d.value),
                "what_de": DIMENSION_GUIDANCE.get(d.value, {}).get("what_de", ""),
            }
            for d in QualityDimension
        ],
        "score_glossary": dict(SCORE_GLOSSARY),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    payload = build_payload()
    args.out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )
    missing = [i["indicator_id"] for i in payload["indicators"] if not i["guidance"]]
    print(f"Exported {len(payload['indicators'])} indicators → {args.out}")
    if missing:
        print(f"WARNING: no guidance for {len(missing)}: {missing}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
