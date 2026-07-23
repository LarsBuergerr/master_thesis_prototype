// Ein Treffer in der Datensatz-Liste im GovData-Stil: Titel (Link zur
// Detailseite), Kurzbeschreibung, Metazeile, Format-/Schlagwort-Chips und
// rechts der kompakte Qualitäts-Indikator.

import type { Dataset } from "../data/evaluation";
import type { Navigate } from "../route";
import { ScoreIndicator } from "./ScoreIndicator";

function formatDate(iso: string): string {
  const parts = iso.split("-");
  return parts.length === 3 ? `${parts[2]}.${parts[1]}.${parts[0]}` : iso || "—";
}

export function DatasetCard({
  dataset,
  onNavigate,
}: {
  dataset: Dataset;
  onNavigate: Navigate;
}) {
  const open = () => onNavigate({ view: "detail", id: dataset.id });

  return (
    <article className="ds-card design-box">
      <div className="ds-card-body">
        <h3 className="ds-card-title">
          <button type="button" className="link-reset ds-card-link" onClick={open}>
            {dataset.title}
          </button>
        </h3>
        <p className="ds-card-desc">
          {dataset.description || <em>Keine Beschreibung hinterlegt.</em>}
        </p>
        <div className="ds-card-meta">
          <span className="ds-card-pub">{dataset.publisherName}</span>
          <span>
            Letzte Änderung: <span className="tnum">{formatDate(dataset.modified)}</span>
          </span>
          {dataset.license && <span>{dataset.license}</span>}
        </div>
        <div className="ds-card-chips">
          {dataset.formats.slice(0, 6).map((f) => (
            <span key={f} className="ds-format">
              {f}
            </span>
          ))}
          {dataset.keywords.slice(0, 3).map((k) => (
            <span key={k} className="ds-keyword">
              {k}
            </span>
          ))}
        </div>
      </div>
      <button
        type="button"
        className="ds-card-score button-reset"
        onClick={open}
        aria-label={`Qualität von ${dataset.title} ansehen`}
      >
        <ScoreIndicator score={dataset.overall} />
      </button>
    </article>
  );
}
