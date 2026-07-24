// Das interaktive Analyse-Werkzeug (RDF hochladen, Gewichte/Policy einstellen,
// analysieren, Ergebnisse ansehen). Inhaltlich unverändert aus dem
// ursprünglichen App-Rumpf herausgelöst; die Kopf-/Fußzeile liefert jetzt der
// GovData-Rahmen (GovDataShell), daher hier nur noch der Arbeitsbereich.

import { useEffect, useState } from "react";
import { ConfigPanel } from "./ConfigPanel";
import { JobProgress } from "./JobProgress";
import { ResultsView } from "./results/ResultsView";
import { UploadPanel } from "./UploadPanel";
import { useIndicators, useJob, useSubmitAnalysis } from "../hooks/useAnalysis";
import { defaultAnalysisConfig } from "../lib/config";
import type { AnalysisConfigInput } from "../api/types";

export function AnalyzerApp() {
  const indicators = useIndicators();
  const submit = useSubmitAnalysis();

  const [files, setFiles] = useState<File[]>([]);
  const [config, setConfig] = useState<AnalysisConfigInput>(defaultAnalysisConfig);
  const [jobId, setJobId] = useState<string | null>(null);
  const [seeded, setSeeded] = useState(false);

  // Seed weights from the live registry once indicators are loaded.
  useEffect(() => {
    if (seeded || !indicators.data) return;
    const dimWeights: Record<string, number> = {};
    indicators.data.dimensions.forEach((d) => (dimWeights[d] = 1));
    const indWeights: Record<string, number> = {};
    indicators.data.indicators.forEach((i) => (indWeights[i.indicator_id] = i.default_weight));
    setConfig((c) => ({
      ...c,
      dimension_weights: dimWeights,
      indicator_weights: indWeights,
    }));
    setSeeded(true);
  }, [indicators.data, seeded]);

  const job = useJob(jobId);

  function handleSubmit() {
    submit.mutate({ files, config }, { onSuccess: (res) => setJobId(res.job_id) });
  }

  const jobData = job.data;
  const isRunning = jobData
    ? jobData.status === "queued" || jobData.status === "running"
    : submit.isPending;

  return (
    <div className="gd-portal-container">
      <div className="gd-analyzer-intro">
        <h1>Analyse-Werkzeug</h1>
        <p className="muted">
          Eigene DCAT-AP.de-Metadaten (RDF/XML) hochladen, Gewichte und Policy einstellen und
          dieselbe Qualitätsbewertung ausführen, die den Portal-Datensätzen zugrunde liegt.
        </p>
      </div>

      <div className="app">
        <aside className="sidebar" aria-label="Konfiguration">
          <UploadPanel
            files={files}
            onFilesChange={setFiles}
            onSubmit={handleSubmit}
            submitting={isRunning}
          />
          {indicators.data && (
            <ConfigPanel indicators={indicators.data} config={config} onChange={setConfig} />
          )}
          {indicators.isError && (
            <div className="alert gd-alert-danger" role="alert">
              Backend nicht erreichbar. Läuft uvicorn auf{" "}
              {import.meta.env.VITE_API_BASE ?? "http://localhost:8000"}?
            </div>
          )}
        </aside>

        <main className="main stack" id="analyzer-content">
          {submit.isError && (
            <div className="alert gd-alert-danger" role="alert">
              Analyse fehlgeschlagen: {(submit.error as Error).message}
            </div>
          )}
          {jobData && jobData.status !== "done" && <JobProgress job={jobData} />}
          {jobData && jobData.results.length > 0 && <ResultsView results={jobData.results} />}
          {!jobData && !submit.isPending && (
            <div className="alert alert-info">
              Noch keine Analyse. Wähle links RDF-Dateien und starte die Analyse.
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
