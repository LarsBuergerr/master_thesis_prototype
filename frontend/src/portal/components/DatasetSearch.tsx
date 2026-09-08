// Die „Daten"-Ansicht: Suchleiste, Facetten-Filter und Trefferliste über den
// geladenen Datenbestand. Facetten (Format, Lizenz, Herkunft) und Sortierung
// entsprechen Funktionen, die es auch in der echten GovData-Suche gibt.
//
// Alle Inhalte stammen aus dem Katalog. Die qualitätsbezogenen Teile —
// Notenfacette, Score-Sortierung, Indikator auf der Karte — erscheinen nur,
// wenn eine Bewertung darüberliegt, und verschwinden rückstandslos, wenn man
// sie ausblendet.

import { useMemo, useState } from "react";
import type { CatalogDataset } from "../../api/types";
import type { Navigate } from "../route";
import { gradeLabel, scoreToGrade } from "../lib/quality";
import { DatasetCard } from "./DatasetCard";
import { OverlayBar } from "./OverlayBar";
import { useCatalog, useOverlay, usePortalSource } from "../source";

type SortKey = "relevanz" | "neueste" | "titel" | "score_desc" | "score_asc";

const GRADE_ORDER = ["A", "B", "C", "D", "F"];

function prettySource(p: string): string {
  return p.replace(/-/g, " ").replace(/\b\w/g, (m) => m.toUpperCase());
}

export function DatasetSearch({ onNavigate }: { onNavigate: Navigate }) {
  const { presenting } = usePortalSource();
  const { datasets, loading, error } = useCatalog();
  const overlay = useOverlay();

  const [query, setQuery] = useState("");
  const [format, setFormat] = useState<string | null>(null);
  const [license, setLicense] = useState<string | null>(null);
  const [grade, setGrade] = useState<string | null>(null);
  const [sort, setSort] = useState<SortKey>("relevanz");

  const scoreOf = (d: CatalogDataset) => overlay.rows.get(d.id)?.overall ?? null;

  const formatCounts = useMemo(() => {
    const m = new Map<string, number>();
    datasets.forEach((d) => d.formats.forEach((f) => m.set(f, (m.get(f) ?? 0) + 1)));
    return [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  }, [datasets]);

  const gradeCounts = useMemo(() => {
    const m = new Map<string, number>();
    datasets.forEach((d) => {
      const score = overlay.rows.get(d.id)?.overall;
      if (score == null) return;
      const g = scoreToGrade(score);
      m.set(g, (m.get(g) ?? 0) + 1);
    });
    return GRADE_ORDER.filter((g) => m.has(g)).map((g) => [g, m.get(g)!] as const);
  }, [datasets, overlay.rows]);

  const licenseCounts = useMemo(() => {
    const m = new Map<string, number>();
    datasets.forEach((d) => {
      if (d.license) m.set(d.license, (m.get(d.license) ?? 0) + 1);
    });
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, [datasets]);

  const sourceCounts = useMemo(() => {
    const m = new Map<string, number>();
    datasets.forEach((d) => {
      if (d.source) m.set(d.source, (m.get(d.source) ?? 0) + 1);
    });
    return [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 7);
  }, [datasets]);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    let list = datasets.filter((d) => {
      if (format && !d.formats.includes(format)) return false;
      if (license && d.license !== license) return false;
      if (grade) {
        const score = overlay.rows.get(d.id)?.overall;
        if (score == null || scoreToGrade(score) !== grade) return false;
      }
      if (q) {
        const hay = `${d.title} ${d.description} ${d.keywords.join(" ")} ${d.publisher_name}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
    list = [...list];
    if (sort === "score_desc") list.sort((a, b) => (scoreOf(b) ?? -1) - (scoreOf(a) ?? -1));
    else if (sort === "score_asc") list.sort((a, b) => (scoreOf(a) ?? 2) - (scoreOf(b) ?? 2));
    else if (sort === "neueste") list.sort((a, b) => (b.modified || "").localeCompare(a.modified || ""));
    else if (sort === "titel") list.sort((a, b) => a.title.localeCompare(b.title, "de"));
    return list;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [datasets, query, format, license, grade, sort, overlay.rows]);

  const activeFilters = [format, license, grade].filter(Boolean).length;

  return (
    <>
      <section className="gd-hero">
        <div className="gd-hero-inner">
          {/* Überschrift, Feld und Aktionen teilen sich ein Raster, damit ihre
              Kanten zwangsläufig fluchten — siehe .gd-hero-search. */}
          <div className="gd-hero-search" role="search">
            <h1>Datensätze durchsuchen</h1>
            <input
              type="search"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Suchbegriff, z. B. Flächennutzungsplan, Haushalt, Verkehr …"
              aria-label="Datensätze durchsuchen"
              className="gd-input"
            />
            <button type="button" className="gd-button gd-button-primary">
              Suchen
            </button>
            <span className="gd-hero-action" aria-hidden="true">
              Erweiterte Suche
            </span>
            <span className="gd-hero-action" aria-hidden="true">
              Kartensuche
            </span>
          </div>
        </div>
      </section>

      {!presenting && (
        <div className="gd-portal-container">
          <OverlayBar datasetCount={datasets.length} />
        </div>
      )}

      {loading && <div className="gd-portal-container"><p className="muted">Metadaten werden gelesen…</p></div>}
      {error && (
        <div className="gd-portal-container">
          <div className="alert gd-alert-danger" role="alert">
            Datenbestand konnte nicht geladen werden.
          </div>
        </div>
      )}

      <div className="gd-search-layout gd-portal-container">
        <aside className="gd-facets" aria-label="Filter">
          {overlay.active && gradeCounts.length > 0 && (
            <FacetGroup title="Metadaten-Qualität">
              {gradeCounts.map(([g, c]) => (
                <FacetItem
                  key={g}
                  label={`${gradeLabel(g)} (${g})`}
                  count={c}
                  active={grade === g}
                  onClick={() => setGrade(grade === g ? null : g)}
                />
              ))}
            </FacetGroup>
          )}

          <FacetGroup title="Dateiformate">
            {formatCounts.map(([f, c]) => (
              <FacetItem
                key={f}
                label={f}
                count={c}
                active={format === f}
                onClick={() => setFormat(format === f ? null : f)}
              />
            ))}
          </FacetGroup>

          <FacetGroup title="Lizenzen">
            {licenseCounts.map(([l, c]) => (
              <FacetItem
                key={l}
                label={l}
                count={c}
                active={license === l}
                onClick={() => setLicense(license === l ? null : l)}
              />
            ))}
          </FacetGroup>

          {sourceCounts.length > 0 && (
            <FacetGroup title="Herkunft">
              {sourceCounts.map(([p, c]) => (
                <FacetItem key={p} label={prettySource(p)} count={c} static />
              ))}
            </FacetGroup>
          )}
        </aside>

        <div className="gd-results-col">
          <div className="gd-results-head">
            <p className="gd-results-count">
              <strong>{results.length}</strong> Datensätze
              {activeFilters > 0 && (
                <span className="muted"> · {activeFilters} Filter aktiv</span>
              )}
            </p>
            <label className="gd-sort">
              <span className="visually-hidden">Sortierung</span>
              <select
                className="gd-input gd-select"
                value={sort}
                onChange={(e) => setSort(e.target.value as SortKey)}
              >
                <option value="relevanz">Relevanz</option>
                <option value="neueste">Neueste zuerst</option>
                <option value="titel">Titel A–Z</option>
                {overlay.active && (
                  <>
                    <option value="score_desc">Metadaten-Qualität absteigend</option>
                    <option value="score_asc">Metadaten-Qualität aufsteigend</option>
                  </>
                )}
              </select>
            </label>
          </div>

          <div className="gd-results">
            {results.map((d) => (
              <DatasetCard
              key={d.id}
              dataset={d}
              quality={overlay.rows.get(d.id) ?? null}
              onNavigate={onNavigate}
            />
            ))}
            {results.length === 0 && !loading && (
              <div className="alert alert-info">
                Keine Datensätze passen zu den aktuellen Filtern.
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

function FacetGroup({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div className="gd-facet design-box">
      <h2 className="gd-facet-title">{title}</h2>
      <ul className="gd-facet-list">{children}</ul>
    </div>
  );
}

function FacetItem({
  label,
  count,
  active,
  onClick,
  static: isStatic,
}: {
  label: string;
  count: number;
  active?: boolean;
  onClick?: () => void;
  static?: boolean;
}) {
  if (isStatic) {
    return (
      <li className="gd-facet-item is-static">
        <span className="gd-facet-label">{label}</span>
        <span className="gd-facet-count">{count}</span>
      </li>
    );
  }
  return (
    <li>
      <button
        type="button"
        className={`gd-facet-item button-reset${active ? " active" : ""}`}
        aria-pressed={active}
        onClick={onClick}
      >
        <span className="gd-facet-label">{label}</span>
        <span className="gd-facet-count">{count}</span>
      </button>
    </li>
  );
}
