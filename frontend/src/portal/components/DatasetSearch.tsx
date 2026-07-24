// Die „Daten"-Ansicht: Suchleiste, Facetten-Filter und Trefferliste über die
// 50 Datensätze der Evaluationsstichprobe. Facetten (Kategorie, Format,
// Qualitätsstufe) und Sortierung entsprechen Funktionen, die es auch in der
// echten GovData-Suche gibt — keine künstlichen Zusatz-Regler.

import { useMemo, useState } from "react";
import { DATASETS } from "../data/evaluation";
import type { Dataset } from "../data/evaluation";
import type { Navigate } from "../route";
import { gradeLabel, scoreToGrade } from "../lib/quality";
import { DatasetCard } from "./DatasetCard";

type SortKey = "relevanz" | "neueste" | "titel" | "score_desc" | "score_asc";

const STRATA: { key: Dataset["stratum"]; label: string }[] = [
  { key: "geo", label: "Geodaten" },
  { key: "non_geo", label: "Fachdaten" },
];

const GRADE_ORDER = ["A", "B", "C", "D", "F"];

function prettyPublisher(p: string): string {
  return p.replace(/-/g, " ").replace(/\b\w/g, (m) => m.toUpperCase());
}

export function DatasetSearch({ onNavigate }: { onNavigate: Navigate }) {
  const [query, setQuery] = useState("");
  const [stratum, setStratum] = useState<Dataset["stratum"] | null>(null);
  const [format, setFormat] = useState<string | null>(null);
  const [license, setLicense] = useState<string | null>(null);
  const [grade, setGrade] = useState<string | null>(null);
  const [sort, setSort] = useState<SortKey>("relevanz");

  const formatCounts = useMemo(() => {
    const m = new Map<string, number>();
    DATASETS.forEach((d) => d.formats.forEach((f) => m.set(f, (m.get(f) ?? 0) + 1)));
    return [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 8);
  }, []);

  const gradeCounts = useMemo(() => {
    const m = new Map<string, number>();
    DATASETS.forEach((d) => {
      const g = scoreToGrade(d.overall);
      m.set(g, (m.get(g) ?? 0) + 1);
    });
    return GRADE_ORDER.filter((g) => m.has(g)).map((g) => [g, m.get(g)!] as const);
  }, []);

  const licenseCounts = useMemo(() => {
    const m = new Map<string, number>();
    DATASETS.forEach((d) => {
      if (d.license) m.set(d.license, (m.get(d.license) ?? 0) + 1);
    });
    return [...m.entries()].sort((a, b) => b[1] - a[1]);
  }, []);

  const publisherCounts = useMemo(() => {
    const m = new Map<string, number>();
    DATASETS.forEach((d) => m.set(d.publisher, (m.get(d.publisher) ?? 0) + 1));
    return [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 7);
  }, []);

  const results = useMemo(() => {
    const q = query.trim().toLowerCase();
    let list = DATASETS.filter((d) => {
      if (stratum && d.stratum !== stratum) return false;
      if (format && !d.formats.includes(format)) return false;
      if (license && d.license !== license) return false;
      if (grade && scoreToGrade(d.overall) !== grade) return false;
      if (q) {
        const hay = `${d.title} ${d.description} ${d.keywords.join(" ")} ${d.publisherName}`.toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });
    list = [...list];
    if (sort === "score_desc") list.sort((a, b) => b.overall - a.overall);
    else if (sort === "score_asc") list.sort((a, b) => a.overall - b.overall);
    else if (sort === "neueste") list.sort((a, b) => (b.modified || "").localeCompare(a.modified || ""));
    else if (sort === "titel") list.sort((a, b) => a.title.localeCompare(b.title, "de"));
    return list;
  }, [query, stratum, format, license, grade, sort]);

  const activeFilters = [stratum, format, license, grade].filter(Boolean).length;

  return (
    <>
      <section className="gd-hero">
        <div className="gd-hero-inner">
          <h1>Datensätze durchsuchen</h1>
          <p className="gd-hero-sub">
            Evaluationsstichprobe · {DATASETS.length} Datensätze aus 10 Datenbereitstellern
          </p>
          <div className="gd-searchbar" role="search">
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
          </div>
          <div className="gd-hero-actions" aria-hidden="true">
            <span className="gd-hero-action">Erweiterte Suche</span>
            <span className="gd-hero-action">Kartensuche</span>
          </div>
        </div>
      </section>

      <div className="gd-search-layout gd-portal-container">
        <aside className="gd-facets" aria-label="Filter">
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

          <FacetGroup title="Datenart">
            {STRATA.map((s) => (
              <FacetItem
                key={s.key}
                label={s.label}
                count={DATASETS.filter((d) => d.stratum === s.key).length}
                active={stratum === s.key}
                onClick={() => setStratum(stratum === s.key ? null : s.key)}
              />
            ))}
          </FacetGroup>

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

          <FacetGroup title="Datenbereitsteller">
            {publisherCounts.map(([p, c]) => (
              <FacetItem key={p} label={prettyPublisher(p)} count={c} static />
            ))}
          </FacetGroup>
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
                <option value="score_desc">Metadaten-Qualität absteigend</option>
                <option value="score_asc">Metadaten-Qualität aufsteigend</option>
              </select>
            </label>
          </div>

          <div className="gd-results">
            {results.map((d) => (
              <DatasetCard key={d.id} dataset={d} onNavigate={onNavigate} />
            ))}
            {results.length === 0 && (
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
        <span>{label}</span>
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
        <span>{label}</span>
        <span className="gd-facet-count">{count}</span>
      </button>
    </li>
  );
}
