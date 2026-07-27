// Detailseite eines Datensatzes im GovData-Stil (Metadaten-Steckbrief) mit
// optional eingeblendetem Qualitäts-Dashboard.
//
// Die Metadaten stammen aus dem Katalog und stehen immer. Der Qualitätsteil
// erscheint nur, wenn eine Bewertung über dem Katalog liegt — er kommt
// entweder aus dem gewählten Lauf (wird für diese eine Datei nachgeladen) oder
// aus einer Berechnung dieser Sitzung. Beide Quellen haben dieselbe Form, die
// Anzeige unterscheidet sie nicht.
//
// Unabhängig davon lässt sich hier ein einzelner Datensatz neu bewerten, ohne
// den ganzen Bestand durchzurechnen.

import { useEffect, useState } from "react";
import type { AnalysisResult } from "../../api/types";
import type { Navigate } from "../route";
import { useCatalogRdf, useRunResult, useAnalyzeCatalogFile } from "../../hooks/usePortal";
import { useDefaultConfig, useJob } from "../../hooks/useAnalysis";
import { withExpressiveness } from "../../lib/config";
import { OverallScoreCard } from "../../components/results/OverallScoreCard";
import { DimensionRadar } from "../../components/results/DimensionRadar";
import { DimensionPanel } from "../../components/results/DimensionPanel";
import { ResultToolbar } from "../../components/results/ResultToolbar";
import { useCatalog, useOverlay, usePortalSource } from "../source";

function formatDate(iso: string): string {
  const parts = iso.split("-");
  return parts.length === 3 ? `${parts[2]}.${parts[1]}.${parts[0]}` : iso || "—";
}

export function DatasetDetail({ id, onNavigate }: { id: string; onNavigate: Navigate }) {
  const { catalog, overlay } = usePortalSource();
  const { datasets } = useCatalog();
  const overlayState = useOverlay();
  const dataset = datasets.find((d) => d.id === id);

  // Ergebnis aus dem gewählten Lauf — gezielt für diese eine Datei geladen.
  const fromRun = useRunResult(overlay?.kind === "run" ? overlay.run : null, id);
  // Ergebnis aus einer Berechnung dieser Sitzung liegt bereits im Speicher.
  const fromJob = overlayState.resultFor(id);

  // Einzelne Neubewertung dieses Datensatzes.
  const [singleJobId, setSingleJobId] = useState<string | null>(null);
  const [single, setSingle] = useState<AnalysisResult | null>(null);
  const defaults = useDefaultConfig();
  const analyzeFile = useAnalyzeCatalogFile();
  const singleJob = useJob(singleJobId);

  useEffect(() => {
    if (singleJob.data?.status !== "done") return;
    const result = singleJob.data.results[0]?.result;
    if (result) setSingle(result);
  }, [singleJob.data]);

  // Datensatzwechsel: ein Einzelergebnis gehört zur vorherigen Datei.
  useEffect(() => {
    setSingle(null);
    setSingleJobId(null);
  }, [id]);

  const rdf = useCatalogRdf(catalog, dataset?.file ?? null);
  const result = single ?? fromJob ?? (overlay?.kind === "run" ? fromRun.data : undefined);

  const [hidePassing, setHidePassing] = useState(false);
  const actionableCount = result
    ? Object.values(result.by_dimension).reduce(
        (acc, dim) => acc + dim.indicators.filter((i) => i.status !== "pass").length,
        0,
      )
    : 0;

  function reanalyze(withExpr: boolean) {
    const config = defaults.data?.config;
    if (!config || !catalog || !dataset) return;
    analyzeFile.mutate(
      { catalog, file: dataset.file, config: withExpressiveness(config, withExpr, config.llm) },
      { onSuccess: (res) => setSingleJobId(res.job_id) },
    );
  }

  if (!dataset) {
    return (
      <div className="gd-portal-container gd-detail">
        <div className="alert gd-alert-danger">Datensatz nicht gefunden.</div>
      </div>
    );
  }

  const singleRunning =
    analyzeFile.isPending ||
    singleJob.data?.status === "queued" ||
    singleJob.data?.status === "running";

  return (
    <div className="gd-portal-container gd-detail">
      <nav className="gd-breadcrumb" aria-label="Brotkrumen">
        <button type="button" className="link-reset" onClick={() => onNavigate({ view: "list" })}>
          Daten
        </button>
        <span aria-hidden="true"> / </span>
        <span className="muted">{dataset.title}</span>
      </nav>

      <div className="gd-detail-grid">
        <div className="gd-detail-main">
          {dataset.category && (
            <span
              className={`gd-tag ${dataset.category === "geo" ? "green" : "not_applicable"} gd-stratum-tag`}
            >
              {dataset.category === "geo" ? "Geodaten" : "Fachdaten"}
            </span>
          )}
          <h1 className="gd-detail-title">{dataset.title}</h1>
          <p className="gd-detail-pub">{dataset.publisher_name}</p>
          <p className="gd-detail-desc">
            {dataset.description || <em>Für diesen Datensatz ist keine Beschreibung hinterlegt.</em>}
          </p>

          <h2 className="gd-detail-h2">Ressourcen &amp; Formate</h2>
          <div className="ds-card-chips">
            {dataset.formats.map((f) => (
              <span key={f} className="ds-format">
                {f}
              </span>
            ))}
            {dataset.formats.length === 0 && <span className="muted">Keine Distributionen.</span>}
          </div>

          {dataset.keywords.length > 0 && (
            <>
              <h2 className="gd-detail-h2">Schlagwörter</h2>
              <div className="ds-card-chips">
                {dataset.keywords.map((k) => (
                  <span key={k} className="ds-keyword">
                    {k}
                  </span>
                ))}
              </div>
            </>
          )}

          <section className="gd-quality design-box design-box-padding" aria-label="Metadaten-Qualität">
            <div className="gd-quality-head">
              <h2>Metadaten-Qualität</h2>
              <p className="muted">
                {result ? (
                  <>
                    Automatische Bewertung durch den Prototyp (
                    {Object.keys(result.by_dimension).length} Dimensionen,{" "}
                    {result.summary.total_indicators} Indikatoren). Jeder nicht erfüllte Indikator
                    lässt sich aufklappen und zeigt, was im Metadatensatz steht und wie es aussehen
                    müsste.
                  </>
                ) : (
                  <>
                    Für diesen Datensatz liegt keine Bewertung vor. Legen Sie in der Liste einen
                    Lauf über den Datenbestand — oder bewerten Sie nur diesen Datensatz.
                  </>
                )}
              </p>
            </div>

            <div className="live-bar">
              <div className="live-bar-main">
                <p className="live-bar-state">
                  {single ? (
                    <>
                      <span className="gd-tag pass">Soeben berechnet</span>
                      Ergebnis dieser Sitzung für <code>{dataset.file}</code>.
                    </>
                  ) : result ? (
                    <>
                      <span className="gd-tag not_applicable">
                        {overlay?.kind === "run" ? "Aus Lauf" : "Aus Berechnung"}
                      </span>
                      {overlay?.kind === "run" ? (
                        <>
                          Lauf <code>{overlay.run}</code>.
                        </>
                      ) : (
                        <>{overlay?.kind === "job" ? overlay.label : null}</>
                      )}
                    </>
                  ) : (
                    <>
                      <span className="gd-tag not_applicable">Ohne Bewertung</span>
                      Datei <code>{dataset.file}</code>.
                    </>
                  )}
                </p>
                {singleRunning && (
                  <p className="live-bar-progress muted" role="status">
                    Bewertung läuft — Indikatoren werden geprüft, URLs abgerufen…
                  </p>
                )}
                {(analyzeFile.isError || singleJob.data?.status === "error") && (
                  <p className="live-bar-error" role="alert">
                    Bewertung fehlgeschlagen —{" "}
                    {singleJob.data?.error ?? (analyzeFile.error as Error | undefined)?.message}
                  </p>
                )}
              </div>

              <div className="live-bar-actions">
                <button
                  type="button"
                  className="gd-button gd-button-secondary"
                  onClick={() => reanalyze(false)}
                  disabled={singleRunning || !defaults.data}
                >
                  Ohne Aussagekraft bewerten
                </button>
                <button
                  type="button"
                  className="gd-button gd-button-primary"
                  onClick={() => reanalyze(true)}
                  disabled={singleRunning || !defaults.data}
                  title="Bewertet zusätzlich Titel, Beschreibung und Schlagwörter durch ein Sprachmodell."
                >
                  {singleRunning ? "Bewertung läuft…" : "Vollständig bewerten"}
                </button>
              </div>
            </div>

            {result && (
              <>
                <div className="score-row">
                  <OverallScoreCard summary={result.summary} />
                  <div className="score-row-radar">
                    <DimensionRadar summary={result.summary} />
                  </div>
                </div>
                <ResultToolbar
                  hidePassing={hidePassing}
                  onChange={setHidePassing}
                  actionable={actionableCount}
                  total={result.summary.total_indicators}
                />
                <div style={{ marginTop: 8 }}>
                  {Object.values(result.by_dimension).map((dim) => (
                    <DimensionPanel
                      key={dim.dimension}
                      dim={dim}
                      rdfSource={rdf.data}
                      hidePassing={hidePassing}
                    />
                  ))}
                </div>
              </>
            )}
          </section>
        </div>

        <aside className="gd-detail-side">
          <div className="design-box design-box-padding">
            <h2 className="gd-side-title">Metadaten</h2>
            <dl className="gd-meta-list">
              <dt>Herausgeber</dt>
              <dd>{dataset.publisher_name || "—"}</dd>
              {dataset.source && (
                <>
                  <dt>Herkunft</dt>
                  <dd>{dataset.source.replace(/-/g, " ")}</dd>
                </>
              )}
              <dt>Letzte Änderung</dt>
              <dd className="tnum">{formatDate(dataset.modified)}</dd>
              <dt>Lizenz</dt>
              <dd>{dataset.license ?? "—"}</dd>
              {dataset.themes.length > 0 && (
                <>
                  <dt>Kategorien</dt>
                  <dd>{dataset.themes.join(", ")}</dd>
                </>
              )}
              <dt>Kennung</dt>
              <dd className="gd-meta-id">{dataset.id}</dd>
            </dl>
          </div>
        </aside>
      </div>
    </div>
  );
}
