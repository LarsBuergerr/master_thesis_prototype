"""Die Referenz-Konfiguration der Evaluation, als API-Konfiguration gelesen.

Die Bewertung in der Masterarbeit lief mit ``conf/state/state_evaluation_final.yaml``
(Gewichte, Score-Policy, Indikator-Blacklist, LLM-Modell). Oberfläche und
Portal-Livelauf müssen dieselben Einstellungen fahren, sonst weicht ein Lauf im
Frontend von den ausgewiesenen Zahlen ab — bei anderen Gewichten oder einer
anderen Indikator-Menge ist der Gesamtscore schlicht nicht derselbe.

Statt die Werte im Frontend zu spiegeln (zwei Quellen, die auseinanderlaufen,
ohne dass es jemand merkt) liest dieses Modul die YAML und übersetzt ihren
``quality``-Block in eine :class:`AnalysisConfig`. Das Frontend holt sie über
``GET /config/default``.

Bewusst mit ``yaml.safe_load`` statt über Hydra gelesen: gebraucht wird nur ein
statischer Block, und der Server soll nicht die Hydra-Initialisierung des CLI
mitschleppen.
"""

from __future__ import annotations

import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from . import settings
from .schemas import AnalysisConfig, LLMConfig, ScoringConfig, ScoringOverride

logger = logging.getLogger("backend.eval_config")


def _scoring(block: dict[str, Any] | None) -> ScoringConfig | None:
    """``quality.scoring`` übersetzen. Fehlt der Block, gelten die Roh-Scores."""
    if not block:
        return None
    overrides = {
        indicator_id: ScoringOverride(**(values or {}))
        for indicator_id, values in (block.get("overrides") or {}).items()
    }
    return ScoringConfig(
        pass_score=block.get("pass_score", 1.0),
        partial_score=block.get("partial_score", 0.5),
        fail_score=block.get("fail_score", 0.0),
        allow_partial=block.get("allow_partial", True),
        overrides=overrides,
    )


def _listing(value: Any) -> list[str] | None:
    """Leere Listen bedeuten in der YAML „kein Filter" — hier also ``None``."""
    if not value:
        return None
    return [str(v) for v in value]


def _weights(value: Any) -> dict[str, float]:
    if not value:
        return {}
    return {str(k): float(v) for k, v in value.items()}


def build_config(path: Path) -> AnalysisConfig:
    """Eine Hydra-State-YAML als :class:`AnalysisConfig` lesen."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    quality = raw.get("quality") or {}
    llm = raw.get("llm") or {}

    return AnalysisConfig(
        dimension_whitelist=_listing(quality.get("dimension_whitelist")),
        indicator_blacklist=_listing(quality.get("indicator_blacklist")),
        indicator_whitelist=_listing(quality.get("indicator_whitelist")),
        dimension_weights=_weights(quality.get("dimension_weights")),
        indicator_weights=_weights(quality.get("indicator_weights")),
        scoring=_scoring(quality.get("scoring")),
        llm=LLMConfig(
            enabled=bool(llm.get("enabled", False)),
            provider=llm.get("provider", "openrouter"),
            model=llm.get("model"),
            base_url=llm.get("base_url"),
            temperature=float(llm.get("temperature", 0.0)),
            max_tokens=int(llm.get("max_tokens", 4096)),
        ),
        language=raw.get("language", "de"),
        max_workers=int(quality.get("max_workers", 4)),
    )


@lru_cache(maxsize=1)
def default_config() -> AnalysisConfig:
    """Referenz-Konfiguration der Evaluation (gecacht, die Datei ist statisch).

    Ist die Datei nicht lesbar, liefert die Funktion die Feld-Defaults der
    :class:`AnalysisConfig`. Das ist bewusst kein Fehler: die Oberfläche bleibt
    bedienbar, und die Antwort trägt ``source: null``, damit das Frontend
    kenntlich machen kann, dass hier nicht die Evaluationskonfiguration läuft.
    """
    path = settings.EVAL_CONFIG_PATH
    try:
        config = build_config(path)
        logger.info("Loaded reference configuration from %s", path)
        return config
    except (OSError, yaml.YAMLError, TypeError, ValueError) as e:
        logger.warning("Reference configuration %s unusable (%s); using defaults", path, e)
        return AnalysisConfig()


def default_config_source() -> str | None:
    """Dateiname der geladenen Referenz-Konfiguration, ``None`` wenn Fallback."""
    return settings.EVAL_CONFIG_PATH.name if settings.EVAL_CONFIG_PATH.is_file() else None
