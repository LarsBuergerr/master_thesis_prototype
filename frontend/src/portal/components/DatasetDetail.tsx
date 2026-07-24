// Detailseite eines Datensatzes im GovData-Stil (Metadaten-Steckbrief) mit
// eingebettetem Qualitäts-Dashboard. Das Dashboard nutzt die bestehenden
// Analyzer-Komponenten (OverallScoreCard, DimensionRadar, DimensionPanel)
// unverändert.
//
// Zwei Ergebnisquellen, gleiche Darstellung: das hinterlegte Ergebnis des
// Referenzlaufs (buildAnalysisResult) und — über LiveAnalysis — ein echter
// Lauf des Backends über dieselbe RDF-Datei. Liegt der RDF-Quelltext vor,
// zeigen die Befunde zusätzlich die betroffene Stelle der Datei.

import { useCallback, useMemo, useState } from "react";
import { datasetById } from "../data/evaluation";
import type { Navigate } from "../route";
import { buildAnalysisResult, scorePct } from "../lib/quality";
import { useSampleRdf } from "../../hooks/useAnalysis";
import type { AnalysisResult } from "../../api/types";
import { OverallScoreCard } from "../../components/results/OverallScoreCard";
import { DimensionRadar } from "../../components/results/DimensionRadar";
import { DimensionPanel } from "../../components/results/DimensionPanel";
import { LiveAnalysis, type ResultSource } from "./LiveAnalysis";

function formatDate(iso: string): string {
  const parts = iso.split("-");
  return parts.length === 3 ? `${parts[2]}.${parts[1]}.${parts[0]}` : iso || "—";
}

export function DatasetDetail({ id, onNavigate }: { id: string; onNavigate: Navigate }) {
  const dataset = datasetById(id);
  const stored = useMemo(() => (dataset ? buildAnalysisResult(dataset) : null), [dataset]);

  const [live, setLive] = useState<AnalysisResult | null>(null);
  const [source, setSource] = useState<ResultSource>("stored");
  const rdf = useSampleRdf(dataset?.file ?? null);

  const handleResult = useCallback((res: AnalysisResult) => {
    setLive(res);
    setSource("live");
  }, []);
  const showStored = useCallback(() => setSource("stored"), []);

  const result = source === "live" && live ? live : stored;

  if (!dataset || !result) {
    return (
      <div className="gd-portal-container gd-detail">
        <div className="alert gd-alert-danger">Datensatz nicht gefunden.</div>
      </div>
    );
  }

  const { by_dimension, summary } = result;

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
          <span className={`gd-tag ${dataset.stratum === "geo" ? "green" : "not_applicable"} gd-stratum-tag`}>
            {dataset.stratum === "geo" ? "Geodaten" : "Fachdaten"}
          </span>
          <h1 className="gd-detail-title">{dataset.title}</h1>
          <p className="gd-detail-pub">{dataset.publisherName}</p>
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
                Automatische Bewertung durch den Prototyp ({Object.keys(by_dimension).length}{" "}
                Dimensionen, {summary.total_indicators} Indikatoren). Jeder nicht erfüllte
                Indikator lässt sich aufklappen und zeigt, was im Metadatensatz steht und wie es
                aussehen müsste.
                {dataset.mqaNorm != null && (
                  <> MQA-Referenzscore (data.europa.eu): <strong>{scorePct(dataset.mqaNorm)} / 100</strong>.</>
                )}
              </p>
            </div>

            <LiveAnalysis
              sampleName={dataset.file}
              source={source}
              onResult={handleResult}
              onShowStored={showStored}
            />

            <OverallScoreCard summary={summary} />
            <div style={{ marginTop: 12 }}>
              <DimensionRadar summary={summary} />
            </div>
            <div style={{ marginTop: 8 }}>
              {Object.values(by_dimension).map((dim) => (
                <DimensionPanel key={dim.dimension} dim={dim} rdfSource={rdf.data} />
              ))}
            </div>
          </section>
        </div>

        <aside className="gd-detail-side">
          <div className="design-box design-box-padding">
            <h2 className="gd-side-title">Metadaten</h2>
            <dl className="gd-meta-list">
              <dt>Herausgeber</dt>
              <dd>{dataset.publisherName}</dd>
              <dt>Datenbereitsteller</dt>
              <dd>{dataset.publisher.replace(/-/g, " ")}</dd>
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
