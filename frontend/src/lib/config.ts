// Standard-Konfiguration eines Analyselaufs. Von Analyse-Werkzeug und
// Portal-Livelauf gemeinsam genutzt, damit beide Wege dieselbe Bewertung
// fahren und nicht auseinanderlaufen.

import type { AnalysisConfigInput } from "../api/types";

export function defaultAnalysisConfig(): AnalysisConfigInput {
  return {
    dimension_whitelist: null,
    indicator_blacklist: null,
    indicator_whitelist: null,
    dimension_weights: {},
    indicator_weights: {},
    scoring: {
      pass_score: 1.0,
      partial_score: 0.5,
      fail_score: 0.0,
      allow_partial: true,
      overrides: {},
    },
    llm: {
      enabled: false,
      provider: "openrouter",
      model: "anthropic/claude-sonnet-4.5",
      base_url: "http://localhost:8080/v1",
      temperature: 0.0,
      max_tokens: 10000,
    },
    language: "de",
    max_workers: 4,
  };
}
