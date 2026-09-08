// Das interaktive Analyse-Werkzeug (RDF hochladen, Gewichte/Policy einstellen,
// analysieren, Ergebnisse ansehen). Inhaltlich unverändert aus dem
// ursprünglichen App-Rumpf herausgelöst; die Kopf-/Fußzeile liefert jetzt der
// GovData-Rahmen (GovDataShell), daher hier nur noch der Arbeitsbereich.

import { useEffect, useState } from "react";
import { ConfigPanel } from "./ConfigPanel";
import { JobProgress } from "./JobProgress";
import { ResultsView } from "./results/ResultsView";
import { UploadPanel } from "./UploadPanel";
import {
  useDefaultConfig,
  useIndicators,
  useJob,
  useSubmitAnalysis,
} from "../hooks/useAnalysis";
import type { AnalysisConfigInput } from "../api/types";

export function AnalyzerApp() {
  const indicators = useIndicators();
  const defaults = useDefaultConfig();
  const submit = useSubmitAnalysis();

  const [files, setFiles] = useState<File[]>([]);
  // `null`, bis die Referenz-Konfiguration geladen ist. Vorher gibt es keine
  // sinnvollen Startwerte: Gewichte und Indikator-Menge stammen aus der YAML
  // der Evaluation, nicht aus Konstanten im Frontend.
  const [config, setConfig] = useState<AnalysisConfigInput | null>(null);
  const [jobId, setJobId] = useState<string | null>(null);

  useEffect(() => {
    if (config || !defaults.data) return;
    setConfig(defaults.data.config);
  }, [config, defaults.data]);

  const job = useJob(jobId);

  function handleSubmit() {
    if (!config) return;
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
          Voreingestellt ist die Konfiguration der Evaluation
          {defaults.data?.source && <> (<code>{defaults.data.source}</code>)</>}.
        </p>
      </div>

      <div className="app">
        <aside className="sidebar" aria-label="Konfiguration">
          <UploadPanel
            files={files}
            onFilesChange={setFiles}
            onSubmit={handleSubmit}
            submitting={isRunning || !config}
          />
          {indicators.data && config && (
            <ConfigPanel indicators={indicators.data} config={config} onChange={setConfig} />
          )}
          {defaults.data && defaults.data.source === null && (
            <div className="alert alert-info" role="status">
              Die Referenz-Konfiguration der Evaluation ist auf dem Server nicht lesbar — es
              gelten Standardwerte. Ergebnisse weichen dann von den Zahlen der Arbeit ab.
            </div>
          )}
          {(indicators.isError || defaults.isError) && (
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
