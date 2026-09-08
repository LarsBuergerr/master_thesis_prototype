// Steuerleiste der Bewertungsebene.
//
// Der Katalog steht bereits; hier entscheidet sich, ob und welche Bewertung
// sich darüberlegt. Drei Wege, bewusst nebeneinander sichtbar:
//
//   1. ein abgeschlossener Lauf aus outputs/runs (kostet nichts, ist der
//      Stand, auf den sich die Arbeit bezieht),
//   2. neu berechnen mit allen vier Dimensionen (braucht ein Sprachmodell),
//   3. neu berechnen ohne Aussagekraft (rein formale Prüfung, kein LLM).
//
// Gefahren wird immer die Konfiguration der Evaluation (`GET /config/default`);
// die einzige Stellschraube ist die Dimension „Aussagekraft".

import { useMemo, useState } from "react";
import { useDefaultConfig } from "../../hooks/useAnalysis";
import { useAnalyzeCatalog, useRuns } from "../../hooks/usePortal";
import { withExpressiveness } from "../../lib/config";
import { usePortalSource, useOverlay } from "../source";

export function OverlayBar({ datasetCount }: { datasetCount: number }) {
  const { catalog, overlay, setOverlay } = usePortalSource();
  const state = useOverlay();
  const runs = useRuns();
  const defaults = useDefaultConfig();
  const analyze = useAnalyzeCatalog();
  const [open, setOpen] = useState(false);

  // Läufe, die zu diesem Datenbestand gehören, zuerst — ein Lauf über ein
  // anderes Verzeichnis passt schlicht nicht zu den geladenen Dateien.
  const { fitting, others } = useMemo(() => {
    const list = runs.data ?? [];
    const fits = (dir?: string | null) => !!dir && !!catalog && dir.endsWith(catalog);
    return {
      fitting: list.filter((r) => fits(r.directory)),
      others: list.filter((r) => !fits(r.directory)),
    };
  }, [runs.data, catalog]);

  function start(withExpr: boolean) {
    const config = defaults.data?.config;
    if (!config || !catalog) return;
    const next = withExpressiveness(config, withExpr, config.llm);
    analyze.mutate(
      { catalog, config: next },
      {
        onSuccess: (res) =>
          setOverlay({
            kind: "job",
            jobId: res.job_id,
            label: withExpr ? "Neuberechnung (alle Dimensionen)" : "Neuberechnung (ohne Aussagekraft)",
          }),
      },
    );
    setOpen(false);
  }

  const busy = analyze.isPending || (overlay?.kind === "job" && state.loading);

  return (
    <div className="gd-overlay-bar">
      <div className="gd-overlay-state">
        {overlay === null && (
          <>
            <span className="gd-tag not_applicable">Ohne Bewertung</span>
            <span className="muted">
              {datasetCount} Datensätze aus <code>{catalog}</code>. Qualitätsangaben erscheinen,
              sobald eine Bewertung darüberliegt.
            </span>
          </>
        )}
        {overlay?.kind === "run" && (
          <>
            <span className="gd-tag pass">Bewertung</span>
            <span className="muted">
              Lauf <code>{overlay.run}</code> · {state.rows.size} von {datasetCount} Datensätzen
              bewertet
            </span>
          </>
        )}
        {overlay?.kind === "job" && (
          <>
            <span className={`gd-tag ${state.loading ? "partial" : "pass"}`}>
              {state.loading ? "Berechnung läuft" : "Bewertung"}
            </span>
            <span className="muted">
              {overlay.label}
              {state.progress && state.loading
                ? ` · ${state.progress.done} von ${state.progress.total} Dateien`
                : ` · ${state.rows.size} Datensätze bewertet`}
            </span>
          </>
        )}
        {state.error && (
          <span className="gd-overlay-error" role="alert">
            Bewertung fehlgeschlagen.
          </span>
        )}
      </div>

      <div className="gd-overlay-actions">
        {overlay !== null && (
          <button
            type="button"
            className="gd-button gd-button-secondary"
            onClick={() => setOverlay(null)}
            disabled={busy}
          >
            Bewertung ausblenden
          </button>
        )}
        <button
          type="button"
          className="gd-button gd-button-primary"
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          disabled={busy}
        >
          {busy ? "Berechnung läuft…" : overlay === null ? "Bewertung überlagern" : "Bewertung wechseln"}
        </button>
      </div>

      {open && (
        <div className="gd-overlay-menu design-box design-box-padding">
          <div className="gd-overlay-group">
            <h3 className="gd-overlay-h3">Abgeschlossenen Lauf verwenden</h3>
            {runs.isLoading && <p className="muted">Läufe werden gelesen…</p>}
            {fitting.length === 0 && others.length === 0 && !runs.isLoading && (
              <p className="muted">Unter dem Lauf-Verzeichnis liegt kein auswertbarer Lauf.</p>
            )}
            <ul className="gd-source-list">
              {fitting.map((r) => (
                <li key={r.name}>
                  <button
                    type="button"
                    className="gd-source-item button-reset"
                    onClick={() => {
                      setOverlay({ kind: "run", run: r.name });
                      setOpen(false);
                    }}
                  >
                    <span className="gd-source-name">{r.name}</span>
                    <span className="gd-source-count muted">
                      {r.dataset_count} Dateien · {r.llm_model ?? "ohne Sprachmodell"}
                    </span>
                  </button>
                </li>
              ))}
            </ul>
            {others.length > 0 && (
              <p className="muted gd-overlay-note">
                {others.length} weitere Läufe liegen vor, gehören aber zu einem anderen
                Datenbestand.
              </p>
            )}
          </div>

          <div className="gd-overlay-group">
            <h3 className="gd-overlay-h3">Neu berechnen</h3>
            <p className="muted gd-overlay-note">
              Bewertet alle {datasetCount} Dateien mit der Konfiguration der Evaluation
              {defaults.data?.source && <> (<code>{defaults.data.source}</code>)</>}.
            </p>
            <div className="gd-row" style={{ gap: 8, flexWrap: "wrap" }}>
              <button
                type="button"
                className="gd-button gd-button-secondary"
                onClick={() => start(false)}
                disabled={!defaults.data}
              >
                Ohne Aussagekraft
              </button>
              <button
                type="button"
                className="gd-button gd-button-secondary"
                onClick={() => start(true)}
                disabled={!defaults.data}
                title="Bewertet Titel, Beschreibung und Schlagwörter durch ein Sprachmodell — dauert deutlich länger und verbraucht Tokens."
              >
                Alle vier Dimensionen
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
