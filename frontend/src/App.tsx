import { useEffect, useState } from "react";
import { ConfigPanel } from "./components/ConfigPanel";
import { JobProgress } from "./components/JobProgress";
import { ResultsView } from "./components/results/ResultsView";
import { ThemeToggle } from "./components/ThemeToggle";
import { UploadPanel } from "./components/UploadPanel";
import { useIndicators, useJob, useSubmitAnalysis } from "./hooks/useAnalysis";
import type { AnalysisConfigInput } from "./api/types";

function defaultConfig(): AnalysisConfigInput {
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

export default function App() {
  const indicators = useIndicators();
  const submit = useSubmitAnalysis();

  const [files, setFiles] = useState<File[]>([]);
  const [config, setConfig] = useState<AnalysisConfigInput>(defaultConfig);
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
    submit.mutate(
      { files, config },
      { onSuccess: (res) => setJobId(res.job_id) },
    );
  }

  const jobData = job.data;
  const isRunning = jobData
    ? jobData.status === "queued" || jobData.status === "running"
    : submit.isPending;

  return (
    <>
      <a className="skip-link" href="#main-content">
        Zum Hauptinhalt springen
      </a>
      <header className="site-header">
        <div>
          <h1>DCAT-AP-DE Quality Analyzer</h1>
          <p className="muted tagline">
            RDF hochladen, Gewichte/Policy einstellen, analysieren.
          </p>
        </div>
        <ThemeToggle />
      </header>

      <div className="app">
        <aside className="sidebar" aria-label="Konfiguration">
          <UploadPanel
            files={files}
            onFilesChange={setFiles}
            onSubmit={handleSubmit}
            submitting={isRunning}
          />
          {indicators.data && (
            <ConfigPanel
              indicators={indicators.data}
              config={config}
              onChange={setConfig}
            />
          )}
          {indicators.isError && (
            <div className="panel error-box" role="alert">
              Backend nicht erreichbar. Läuft uvicorn auf{" "}
              {import.meta.env.VITE_API_BASE ?? "http://localhost:8000"}?
            </div>
          )}
        </aside>

        <main className="main stack" id="main-content">
          {submit.isError && (
            <div className="panel error-box" role="alert">
              Analyse fehlgeschlagen: {(submit.error as Error).message}
            </div>
          )}
          {jobData && jobData.status !== "done" && <JobProgress job={jobData} />}
          {jobData && jobData.results.length > 0 && (
            <ResultsView results={jobData.results} />
          )}
          {!jobData && !submit.isPending && (
            <div className="panel muted">
              Noch keine Analyse. Wähle links RDF-Dateien und starte die Analyse.
            </div>
          )}
        </main>
      </div>
    </>
  );
}
