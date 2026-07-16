import type {
  AnalysisConfigInput,
  IndicatorsResponse,
  ScoringConfig,
} from "../api/types";

interface Props {
  indicators: IndicatorsResponse;
  config: AnalysisConfigInput;
  onChange: (next: AnalysisConfigInput) => void;
}

const DEFAULT_SCORING: ScoringConfig = {
  pass_score: 1.0,
  partial_score: 0.5,
  fail_score: 0.0,
  allow_partial: true,
  overrides: {},
};

function num(value: string, fallback: number): number {
  const n = parseFloat(value);
  return Number.isNaN(n) ? fallback : n;
}

export function ConfigPanel({ indicators, config, onChange }: Props) {
  const allDims = indicators.dimensions;
  const activeDims = config.dimension_whitelist ?? allDims;

  function patch(p: Partial<AnalysisConfigInput>) {
    onChange({ ...config, ...p });
  }

  function toggleDimension(dim: string) {
    const active = new Set(activeDims);
    if (active.has(dim)) active.delete(dim);
    else active.add(dim);
    const next = allDims.filter((d) => active.has(d));
    // null means "all dimensions" — keeps payload clean when nothing excluded.
    patch({ dimension_whitelist: next.length === allDims.length ? null : next });
  }

  function setDimWeight(dim: string, value: number) {
    patch({ dimension_weights: { ...config.dimension_weights, [dim]: value } });
  }

  function setIndicatorWeight(id: string, value: number) {
    patch({ indicator_weights: { ...config.indicator_weights, [id]: value } });
  }

  function patchScoring(p: Partial<ScoringConfig>) {
    const base = config.scoring ?? DEFAULT_SCORING;
    patch({ scoring: { ...base, ...p } });
  }

  function patchLLM(p: Partial<AnalysisConfigInput["llm"]>) {
    patch({ llm: { ...config.llm, ...p } });
  }

  const scoring = config.scoring;

  return (
    <div className="design-box design-box-padding gd-input">
      <h2>Konfiguration</h2>

      {/* Dimensions */}
      <div className="section-sub">Dimensionen &amp; Gewichte</div>
      {allDims.map((dim) => (
        <div className="gd-row between" key={dim} style={{ marginBottom: 6 }}>
          <label style={{ margin: 0, display: "flex", gap: 6, alignItems: "center" }}>
            <input
              type="checkbox"
              checked={activeDims.includes(dim)}
              onChange={() => toggleDimension(dim)}
            />
            {dim}
          </label>
          <input
            type="number"
            step="0.1"
            className="compact-number"
            value={config.dimension_weights[dim] ?? 1}
            onChange={(e) => setDimWeight(dim, num(e.target.value, 1))}
          />
        </div>
      ))}

      {/* Score policy */}
      <div className="section-sub">Score-Policy</div>
      <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
        <input
          type="checkbox"
          checked={scoring != null}
          onChange={(e) => patch({ scoring: e.target.checked ? DEFAULT_SCORING : null })}
        />
        Policy aktiv (sonst Roh-Scores)
      </label>
      {scoring && (
        <>
          <div className="grid2">
            <div>
              <label>pass</label>
              <input
                type="number"
                step="0.1"
                value={scoring.pass_score}
                onChange={(e) => patchScoring({ pass_score: num(e.target.value, 1) })}
              />
            </div>
            <div>
              <label>partial</label>
              <input
                type="number"
                step="0.1"
                value={scoring.partial_score}
                onChange={(e) => patchScoring({ partial_score: num(e.target.value, 0.5) })}
              />
            </div>
            <div>
              <label>fail (darf negativ sein)</label>
              <input
                type="number"
                step="0.1"
                value={scoring.fail_score}
                onChange={(e) => patchScoring({ fail_score: num(e.target.value, 0) })}
              />
            </div>
            <div style={{ display: "flex", alignItems: "flex-end" }}>
              <label style={{ display: "flex", gap: 6, alignItems: "center", margin: 0 }}>
                <input
                  type="checkbox"
                  checked={scoring.allow_partial}
                  onChange={(e) => patchScoring({ allow_partial: e.target.checked })}
                />
                allow_partial
              </label>
            </div>
          </div>
        </>
      )}

      {/* LLM */}
      <div className="section-sub">Expressiveness (LLM)</div>
      <label style={{ display: "flex", gap: 6, alignItems: "center" }}>
        <input
          type="checkbox"
          checked={config.llm.enabled}
          onChange={(e) => patchLLM({ enabled: e.target.checked })}
        />
        LLM aktiv
      </label>
      {config.llm.enabled && (
        <>
          <label>Provider</label>
          <select
            value={config.llm.provider}
            onChange={(e) => patchLLM({ provider: e.target.value })}
          >
            <option value="openrouter">OpenRouter</option>
            <option value="local">Lokal (llama.cpp)</option>
          </select>
          <label>Modell</label>
          <input
            type="text"
            value={config.llm.model ?? ""}
            onChange={(e) => patchLLM({ model: e.target.value })}
          />
          {config.llm.provider === "local" && (
            <>
              <label>base_url</label>
              <input
                type="text"
                value={config.llm.base_url ?? ""}
                onChange={(e) => patchLLM({ base_url: e.target.value })}
              />
            </>
          )}
        </>
      )}

      {/* Indicator weights */}
      <div className="section-sub">Indikator-Gewichte</div>
      <div className="scroll">
        {allDims.map((dim) => {
          const inds = indicators.indicators.filter((i) => i.dimension === dim);
          if (inds.length === 0) return null;
          return (
            <div key={dim} style={{ marginBottom: 10 }}>
              <div className="muted" style={{ fontWeight: 600, marginBottom: 4 }}>
                {dim}
              </div>
              {inds.map((ind) => (
                <div className="weight-grid" key={ind.indicator_id}>
                  <span className="ind-name" title={ind.name_de}>
                    {ind.indicator_id}
                    {ind.graded ? " ●" : ""}
                  </span>
                  <input
                    type="number"
                    step="0.05"
                    value={
                      config.indicator_weights[ind.indicator_id] ?? ind.default_weight
                    }
                    onChange={(e) =>
                      setIndicatorWeight(
                        ind.indicator_id,
                        num(e.target.value, ind.default_weight),
                      )
                    }
                  />
                </div>
              ))}
            </div>
          );
        })}
        <p className="muted" style={{ marginTop: 0 }}>● = gestufter Indikator (behält Roh-Score)</p>
      </div>
    </div>
  );
}
