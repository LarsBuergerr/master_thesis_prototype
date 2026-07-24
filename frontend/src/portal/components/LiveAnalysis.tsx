// Live-Bewertung eines Portal-Datensatzes.
//
// Die Portalseite zeigt zunächst das hinterlegte Ergebnis des Referenzlaufs
// (damit sie auch ohne laufendes Backend vollständig ist). Über diese Leiste
// lässt sich dieselbe RDF-Datei vom Backend neu bewerten — gleiche Pipeline
// wie beim Upload im Analyse-Werkzeug. So zeigt der Mock echte Ergebnisse in
// einer Umgebung, die dem GovData-Portal entspricht.

import { useEffect, useState } from "react";
import type { AnalysisResult } from "../../api/types";
import { useAnalyzeSample, useJob } from "../../hooks/useAnalysis";
import { defaultAnalysisConfig } from "../../lib/config";

export type ResultSource = "stored" | "live";

export function LiveAnalysis({
  sampleName,
  source,
  onResult,
  onShowStored,
}: {
  /** Dateiname der Stichprobe, z. B. "geo_gdi-de_02.rdf". */
  sampleName: string;
  source: ResultSource;
  onResult: (result: AnalysisResult) => void;
  onShowStored: () => void;
}) {
  const [jobId, setJobId] = useState<string | null>(null);
  const [useLlm, setUseLlm] = useState(false);
  const analyze = useAnalyzeSample();
  const job = useJob(jobId);

  // Jobwechsel: sobald der Lauf fertig ist, das Ergebnis nach oben reichen.
  useEffect(() => {
    if (job.data?.status !== "done") return;
    const result = job.data.results[0]?.result;
    if (result) onResult(result);
    // onResult ist in DatasetDetail stabil (useCallback), daher unkritisch.
  }, [job.data, onResult]);

  function start() {
    const config = defaultAnalysisConfig();
    config.llm = { ...config.llm, enabled: useLlm };
    analyze.mutate(
      { name: sampleName, config },
      { onSuccess: (res) => setJobId(res.job_id) },
    );
  }

  const status = job.data?.status;
  const running = analyze.isPending || status === "queued" || status === "running";
  const failed = analyze.isError || status === "error";

  return (
    <div className="live-bar">
      <div className="live-bar-main">
        <p className="live-bar-state">
          {source === "live" ? (
            <>
              <span className="gd-tag pass">
                <span aria-hidden="true">✓</span>Live-Ergebnis
              </span>
              Soeben vom Backend berechnet — Datei <code>{sampleName}</code>.
            </>
          ) : (
            <>
              <span className="gd-tag not_applicable">Hinterlegtes Ergebnis</span>
              Aus dem Referenzlauf der Masterarbeit. Datei <code>{sampleName}</code> jetzt neu
              bewerten lassen?
            </>
          )}
        </p>
        {running && (
          <p className="live-bar-progress muted" role="status">
            Analyse läuft — Indikatoren werden geprüft, URLs abgerufen
            {useLlm && " und Texte durch das Sprachmodell bewertet"}…
          </p>
        )}
        {failed && (
          <p className="live-bar-error" role="alert">
            Bewertung fehlgeschlagen — läuft das Backend unter{" "}
            {import.meta.env.VITE_API_BASE ?? "http://localhost:8000"}?{" "}
            {job.data?.error ?? (analyze.error as Error | undefined)?.message}
          </p>
        )}
      </div>

      <div className="live-bar-actions">
        <label className="live-bar-llm" title="Bewertet Titel, Beschreibung und Schlagwörter durch ein Sprachmodell. Benötigt einen konfigurierten API-Schlüssel und dauert deutlich länger.">
          <input
            type="checkbox"
            checked={useLlm}
            onChange={(e) => setUseLlm(e.target.checked)}
            disabled={running}
          />
          Aussagekraft per Sprachmodell prüfen
        </label>
        {source === "live" && (
          <button type="button" className="gd-button gd-button-secondary" onClick={onShowStored}>
            Hinterlegtes Ergebnis
          </button>
        )}
        <button
          type="button"
          className="gd-button gd-button-primary"
          onClick={start}
          disabled={running}
        >
          {running ? "Bewertung läuft…" : "Jetzt neu bewerten"}
        </button>
      </div>
    </div>
  );
}
