// Konfiguration eines Analyselaufs.
//
// Maßgeblich ist die Referenz-Konfiguration der Evaluation
// (conf/state/state_evaluation_final.yaml), die das Backend über
// `GET /config/default` ausliefert — Gewichte, Score-Policy, Indikator-Menge
// und LLM-Modell. Das Frontend hält bewusst *keine* eigene Kopie davon: eine
// gespiegelte Konstante würde von der YAML abweichen, sobald jemand die YAML
// ändert, und ein Lauf im Frontend läge dann still neben den Zahlen der Arbeit.
//
// Hier liegen daher nur Ableitungen auf der geladenen Konfiguration.

import type { AnalysisConfigInput } from "../api/types";

/** Die einzige Dimension, die ein Sprachmodell braucht — und damit Tokens kostet. */
export const EXPRESSIVENESS = "expressiveness";

const ALL_DIMENSIONS = ["findability", "accessibility", "reusability", EXPRESSIVENESS];

/**
 * Ist die Dimension „Aussagekraft" in dieser Konfiguration aktiv? Aktiv heißt:
 * in der Dimensions-Whitelist *und* mit eingeschaltetem Sprachmodell — ohne
 * LLM melden die expr_*-Indikatoren `not_applicable`, die Dimension liefe also
 * leer mit.
 */
export function expressivenessEnabled(config: AnalysisConfigInput): boolean {
  const active = config.dimension_whitelist ?? ALL_DIMENSIONS;
  return config.llm.enabled && active.includes(EXPRESSIVENESS);
}

/**
 * „Aussagekraft" an- oder abschalten, ohne die übrige Konfiguration anzufassen.
 *
 * Abschalten nimmt die Dimension aus der Whitelist **und** schaltet das
 * Sprachmodell ab (sonst würden Tokens für ein Ergebnis ausgegeben, das
 * niemand sieht). Die Gewichte bleiben unberührt: das Backend normiert die
 * Dimensionsgewichte über die tatsächlich gelaufenen Dimensionen, ein
 * ungenutztes Gewicht stört also nicht.
 *
 * `llmDefaults` sind die LLM-Einstellungen der Referenz-Konfiguration (Modell,
 * Provider, Temperatur). Sie werden beim Einschalten wiederhergestellt, damit
 * ein Aus/An-Wechsel nicht ein anderes Modell zurücklässt als die Evaluation.
 */
export function withExpressiveness(
  config: AnalysisConfigInput,
  enabled: boolean,
  llmDefaults: AnalysisConfigInput["llm"],
): AnalysisConfigInput {
  const active = config.dimension_whitelist ?? ALL_DIMENSIONS;
  const next = enabled
    ? Array.from(new Set([...active, EXPRESSIVENESS]))
    : active.filter((d) => d !== EXPRESSIVENESS);
  return {
    ...config,
    dimension_whitelist: next,
    llm: enabled ? { ...llmDefaults, enabled: true } : { ...config.llm, enabled: false },
  };
}
