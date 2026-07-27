// Ein Treffer in der Datensatz-Liste im GovData-Stil: Titel (Link zur
// Detailseite), Kurzbeschreibung, Metazeile und Format-Chips — alles aus den
// Metadaten des Katalogs.
//
// Der Qualitäts-Indikator rechts erscheint nur, wenn eine Bewertung über dem
// Katalog liegt. Ohne sie ist die Karte vollständig; das Portal soll nicht so
// aussehen, als fehle etwas.

import type { CatalogDataset } from "../../api/types";
import type { Navigate } from "../route";
import { ScoreIndicator } from "./ScoreIndicator";

function formatDate(iso: string): string {
  const parts = iso.split("-");
  return parts.length === 3 ? `${parts[2]}.${parts[1]}.${parts[0]}` : iso || "—";
}

export function DatasetCard({
  dataset,
  score,
  onNavigate,
}: {
  dataset: CatalogDataset;
  /** Gesamtscore aus der überlagerten Bewertung, sonst `undefined`/`null`. */
  score?: number | null;
  onNavigate: Navigate;
}) {
  const open = () => onNavigate({ view: "detail", id: dataset.id });

  return (
    <article className="ds-card design-box">
      <div className="ds-card-body">
        <div className="ds-card-top">
          <span className="ds-card-kind">Datensatz</span>
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
        <button
          type="button"
          className="ds-card-score button-reset"
          onClick={open}
          aria-label={`Qualität von ${dataset.title} ansehen`}
        >
          <ScoreIndicator score={score} />
        </button>
      )}
    </article>
  );
}
