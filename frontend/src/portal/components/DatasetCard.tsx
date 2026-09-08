// Ein Treffer in der Datensatz-Liste im GovData-Stil: Titel (Link zur
// Detailseite), Kurzbeschreibung, Metazeile und Format-Chips — alles aus den
// Metadaten des Katalogs.
//
// Die Kopfzeile führt links zusammen, was den Eintrag einordnet — Art,
// Kategorie und Änderungsdatum. Zuvor stand das Datum am rechten Rand und
// stand damit weiter von seinem Bezugspunkt entfernt als von dem der
// Nachbarspalte.
//
// Der Qualitäts-Indikator rechts erscheint nur, wenn eine Bewertung über dem
// Katalog liegt. Ohne sie ist die Karte vollständig; das Portal soll nicht so
// aussehen, als fehle etwas.

import type { CatalogDataset, RunIndexRow } from "../../api/types";
import type { Navigate } from "../route";
import { ScoreIndicator } from "./ScoreIndicator";
import { themeLabel } from "../lib/quality";

function formatDate(iso: string): string {
  const parts = iso.split("-");
  return parts.length === 3 ? `${parts[2]}.${parts[1]}.${parts[0]}` : iso || "—";
}

export function DatasetCard({
  dataset,
  quality,
  onNavigate,
}: {
  dataset: CatalogDataset;
  /** Kurzbewertung aus der überlagerten Bewertung, sonst `undefined`/`null`. */
  quality?: RunIndexRow | null;
  onNavigate: Navigate;
}) {
  const open = () => onNavigate({ view: "detail", id: dataset.id });
  const score = quality?.overall;

  return (
    <article className="ds-card design-box">
      <div className="ds-card-body">
        <div className="ds-card-top">
          <span className="ds-card-kind">Datensatz</span>
          {/* Kategorien sagen in einem Wort, worum es geht — die Beschreibung
              braucht dafür zwei Zeilen, die hier abgeschnitten werden. */}
          {dataset.themes.slice(0, 2).map((t) => (
            <span key={t} className="ds-card-theme">
              {themeLabel(t)}
            </span>
          ))}
          <span className="ds-card-changed">
            Letzte Änderung: <span className="tnum">{formatDate(dataset.modified)}</span>
          </span>
        </div>
        <h3 className="ds-card-title">
          <button type="button" className="link-reset ds-card-link" onClick={open}>
            {dataset.title}
          </button>
        </h3>
        <p className="ds-card-desc">
          {dataset.description || <em>Keine Beschreibung hinterlegt.</em>}
        </p>
        <div className="ds-card-formats">
          {dataset.formats.slice(0, 8).map((f) => (
            <span key={f} className="ds-format">
              {f}
            </span>
          ))}
          <span className="ds-card-source">
            <span className="ds-card-pub">{dataset.publisher_name}</span>
            {dataset.license && ` · ${dataset.license}`}
          </span>
        </div>
      </div>
      {score != null && (
        <div className="ds-card-score">
          <ScoreIndicator
            score={score}
            detail={quality}
            onOpen={open}
            openLabel={`Qualität von ${dataset.title} ansehen`}
          />
        </div>
      )}
    </article>
  );
}
