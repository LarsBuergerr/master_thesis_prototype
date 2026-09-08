// Startbildschirm: das Portal ist leer, bis ein Datenverzeichnis geladen wird.
//
// Das ist die Reihenfolge, die der Architektur entspricht — erst die Inhalte
// (ein Verzeichnis mit RDF-Metadaten), dann optional eine Bewertung darüber.
// Wer nur das Portal sehen will, hört nach Schritt 1 auf.
//
// Für Vorführungen gibt es oben zwei Direktwege, die beide Schritte in einem
// Klick erledigen.

import { useMemo } from "react";
import { useCatalogs, useRuns } from "../../hooks/usePortal";
import { usePortalSource } from "../source";

/** Datenverzeichnis der Evaluationsstichprobe — Ziel des Demo-Knopfes. */
const DEMO_CATALOG = "sample_2026-06-25_09-57";

export function SourcePicker() {
  const catalogs = useCatalogs();
  const runs = useRuns();
  const { setCatalog, setOverlay } = usePortalSource();

  // Der jüngste Lauf über die Stichprobe — für den Demo-Knopf „mit Bewertung".
  const demoRun = useMemo(() => {
    const list = runs.data ?? [];
    const match = list.find((r) => (r.directory ?? "").endsWith(DEMO_CATALOG));
    return match ?? null;
  }, [runs.data]);

  const hasDemoCatalog = (catalogs.data ?? []).some((c) => c.name === DEMO_CATALOG);

  function loadDemo(withRun: boolean) {
    setCatalog(DEMO_CATALOG);
    if (withRun && demoRun) setOverlay({ kind: "run", run: demoRun.name });
  }

  return (
    <div className="gd-portal-container gd-empty">
      <header className="gd-empty-head">
        <p className="gd-dash-eyebrow">Portal-Mock · Metadatenqualität</p>
        <h1>Kein Datenbestand geladen</h1>
        <p className="gd-empty-lead">
          Das Portal baut seine Inhalte aus einem Verzeichnis mit DCAT-AP.de-Metadaten.
          Wählen Sie zuerst einen Datenbestand — eine Qualitätsbewertung lässt sich
          anschließend darüberlegen, ist aber nicht Voraussetzung.
        </p>
      </header>

      {hasDemoCatalog && (
        <section className="gd-empty-demo design-box design-box-padding">
          <h2 className="gd-panel-title">Direkt vorführen</h2>
          <p className="gd-panel-hint muted">
            Lädt die Evaluationsstichprobe (n&nbsp;=&nbsp;50)
            {demoRun ? " – wahlweise mit dem Ergebnis des letzten Laufs darüber." : "."}
          </p>
          <div className="gd-row" style={{ gap: 8, flexWrap: "wrap" }}>
            <button
              type="button"
              className="gd-button gd-button-secondary"
              onClick={() => loadDemo(false)}
            >
              Nur Portal
            </button>
            {demoRun && (
              <button
                type="button"
                className="gd-button gd-button-primary"
                onClick={() => loadDemo(true)}
              >
                Portal + Bewertung
              </button>
            )}
          </div>
        </section>
      )}

      <section className="gd-empty-list">
        <h2 className="gd-panel-title">Datenbestand wählen</h2>
        {catalogs.isLoading && <p className="muted">Verzeichnisse werden gelesen…</p>}
        {catalogs.isError && (
          <div className="alert gd-alert-danger" role="alert">
            Backend nicht erreichbar. Läuft uvicorn auf{" "}
            {import.meta.env.VITE_API_BASE ?? "http://localhost:8000"}?
          </div>
        )}
        {catalogs.data?.length === 0 && (
          <div className="alert alert-info">
            Unter dem konfigurierten Datenverzeichnis liegt kein Ordner mit RDF-Dateien.
          </div>
        )}
        <ul className="gd-source-list">
          {(catalogs.data ?? []).map((c) => (
            <li key={c.name}>
              <button
                type="button"
                className="gd-source-item button-reset"
                onClick={() => setCatalog(c.name)}
              >
                <span className="gd-source-name">{c.name}</span>
                <span className="gd-source-count muted">{c.dataset_count} Datensätze</span>
              </button>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
