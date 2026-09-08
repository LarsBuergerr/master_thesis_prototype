import { useState } from "react";
import type { FileResult } from "../../api/types";
import { BatchComparison } from "./BatchComparison";
import { DimensionPanel, type ExpandSignal } from "./DimensionPanel";
import { DimensionRadar } from "./DimensionRadar";
import { OverallScoreCard } from "./OverallScoreCard";
import { ResultToolbar } from "./ResultToolbar";

function FileResultCard({
  fr,
  hidePassing,
  expand,
}: {
  fr: FileResult;
  hidePassing: boolean;
  expand?: ExpandSignal;
}) {
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
    <div className="design-box design-box-padding ind-box">
      <h3>{fr.filename}</h3>
      <div className="score-row">
        <OverallScoreCard summary={summary} />
        <div className="score-row-radar">
          <DimensionRadar summary={summary} />
        </div>
      </div>
      <div className="dim-panels">
        {Object.values(by_dimension).map((dim) => (
          <DimensionPanel
            key={dim.dimension}
            dim={dim}
            hidePassing={hidePassing}
            expand={expand}
          />
        ))}
      </div>
    </div>
  );
}

export function ResultsView({ results }: { results: FileResult[] }) {
  // Ein Schalter für alle Dateien des Laufs: wer den Handlungsbedarf sucht,
  // sucht ihn in allen Ergebnissen, nicht in einem einzelnen. Dasselbe gilt für
  // das Aufklappen — der Auftrag geht an jede Datei des Laufs.
  const [hidePassing, setHidePassing] = useState(false);
  const [expand, setExpand] = useState<ExpandSignal>({ open: false, nonce: 0 });

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
          allExpanded={expand.open}
          onToggleAll={() => setExpand((p) => ({ open: !p.open, nonce: p.nonce + 1 }))}
        />
      )}
      <div className="cards">
        {results.map((fr) => (
          <FileResultCard
            key={fr.filename}
            fr={fr}
            hidePassing={hidePassing}
            expand={expand}
          />
        ))}
      </div>
    </div>
  );
}
