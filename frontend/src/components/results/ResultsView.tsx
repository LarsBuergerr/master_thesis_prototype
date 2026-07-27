import { useState } from "react";
import type { FileResult } from "../../api/types";
import { BatchComparison } from "./BatchComparison";
import { DimensionPanel } from "./DimensionPanel";
import { DimensionRadar } from "./DimensionRadar";
import { OverallScoreCard } from "./OverallScoreCard";
import { ResultToolbar } from "./ResultToolbar";

function FileResultCard({ fr, hidePassing }: { fr: FileResult; hidePassing: boolean }) {
  if (fr.error || !fr.result) {
    return (
      <div className="design-box design-box-padding">
        <h3>{fr.filename}</h3>
        <div className="alert gd-alert-danger">{fr.error ?? "Kein Ergebnis"}</div>
      </div>
    );
  }
  const { summary, by_dimension } = fr.result;
  return (
    <div className="design-box design-box-padding">
      <h3>{fr.filename}</h3>
      <div className="score-row">
        <OverallScoreCard summary={summary} />
        <div className="score-row-radar">
          <DimensionRadar summary={summary} />
        </div>
      </div>
      <div style={{ marginTop: 8 }}>
        {Object.values(by_dimension).map((dim) => (
          <DimensionPanel key={dim.dimension} dim={dim} hidePassing={hidePassing} />
        ))}
      </div>
    </div>
  );
}

export function ResultsView({ results }: { results: FileResult[] }) {
  // Ein Schalter für alle Dateien des Laufs: wer den Handlungsbedarf sucht,
  // sucht ihn in allen Ergebnissen, nicht in einem einzelnen.
  const [hidePassing, setHidePassing] = useState(false);

  if (results.length === 0) return null;

  const scored = results.filter((fr) => fr.result);
  const total = scored.reduce((acc, fr) => acc + (fr.result?.summary.total_indicators ?? 0), 0);
  const actionable = scored.reduce(
    (acc, fr) =>
      acc +
      Object.values(fr.result!.by_dimension).reduce(
        (inner, dim) => inner + dim.indicators.filter((i) => i.status !== "pass").length,
        0,
      ),
    0,
  );

  return (
    <div className="stack">
      <BatchComparison results={results} />
      {scored.length > 0 && (
        <ResultToolbar
          hidePassing={hidePassing}
          onChange={setHidePassing}
          actionable={actionable}
          total={total}
        />
      )}
      <div className="cards">
        {results.map((fr) => (
          <FileResultCard key={fr.filename} fr={fr} hidePassing={hidePassing} />
        ))}
      </div>
    </div>
  );
}
