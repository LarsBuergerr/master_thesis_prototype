import type { FileResult } from "../../api/types";
import { BatchComparison } from "./BatchComparison";
import { DimensionPanel } from "./DimensionPanel";
import { DimensionRadar } from "./DimensionRadar";
import { OverallScoreCard } from "./OverallScoreCard";

function FileResultCard({ fr }: { fr: FileResult }) {
  if (fr.error || !fr.result) {
    return (
      <div className="panel">
        <h3>{fr.filename}</h3>
        <div className="error-box">{fr.error ?? "Kein Ergebnis"}</div>
      </div>
    );
  }
  const { summary, by_dimension } = fr.result;
  return (
    <div className="panel">
      <h3>{fr.filename}</h3>
      <OverallScoreCard summary={summary} />
      <div style={{ marginTop: 12 }}>
        <DimensionRadar summary={summary} />
      </div>
      <div style={{ marginTop: 8 }}>
        {Object.values(by_dimension).map((dim) => (
          <DimensionPanel key={dim.dimension} dim={dim} />
        ))}
      </div>
    </div>
  );
}

export function ResultsView({ results }: { results: FileResult[] }) {
  if (results.length === 0) return null;
  return (
    <div className="stack">
      <BatchComparison results={results} />
      <div className="cards">
        {results.map((fr) => (
          <FileResultCard key={fr.filename} fr={fr} />
        ))}
      </div>
    </div>
  );
}
