// Zustand der beiden Portalebenen und ihre Verknüpfung.
//
// Ebene 1 ist der **Katalog**: ein Datenverzeichnis, aus dem das Portal seine
// Inhalte baut (Titel, Beschreibung, Schlagwörter, Formate, Lizenz). Ohne
// Bewertung ist es vollständig — genau wie ein echtes Metadatenportal.
//
// Ebene 2 ist das **Overlay**: eine Bewertung, die sich darüberlegt. Sie kommt
// entweder aus einem abgeschlossenen Lauf (`kind: "run"`) oder aus einer
// Berechnung, die gerade in dieser Sitzung lief (`kind: "job"`). Beide Fälle
// liefern dieselben zwei Dinge — eine Kurzbewertung je Datei für Liste und
// Übersicht, und ein vollständiges Ergebnis für die Detailseite.
//
// Verknüpft wird ausschließlich über den Dateistamm. Der Katalog kennt keine
// Scores, der Lauf keine Titel; nichts davon muss der jeweils anderen Ebene
// bekannt sein.

import { createContext, useCallback, useContext, useMemo, useState } from "react";
import type { ReactNode } from "react";
import type { AnalysisResult, CatalogDataset, RunIndexRow } from "../api/types";
import { useCatalogDatasets, useRunIndex } from "../hooks/usePortal";
import { useJob } from "../hooks/useAnalysis";

/** Woher die Bewertung stammt, die gerade über dem Katalog liegt. */
export type Overlay =
  | { kind: "run"; run: string }
  | { kind: "job"; jobId: string; label: string }
  | null;

interface PortalSource {
  catalog: string | null;
  setCatalog: (name: string | null) => void;
  overlay: Overlay;
  setOverlay: (overlay: Overlay) => void;
  reset: () => void;
  /**
   * Vorführmodus. Blendet die Bedienelemente aus, die es nur gibt, weil der
   * Prototyp seine Datenquelle und seine Bewertung zur Laufzeit wählen lässt —
   * Quellen- und Laufauswahl, Neuberechnung, Herkunftsangabe des Ergebnisses.
   * In einem echten Portal existieren sie nicht; für Screenshots stören sie.
   * Was bleibt, ist die Portalansicht mit ihrer Bewertung.
   */
  presenting: boolean;
  setPresenting: (next: boolean) => void;
}

const SourceContext = createContext<PortalSource | null>(null);

export function PortalSourceProvider({ children }: { children: ReactNode }) {
  const [catalog, setCatalogState] = useState<string | null>(null);
  const [overlay, setOverlay] = useState<Overlay>(null);
  const [presenting, setPresenting] = useState(false);

  // Katalogwechsel verwirft die Bewertung: ein Lauf gehört immer zu genau
  // einem Datenverzeichnis, über einem anderen wäre er sinnlos.
  const setCatalog = useCallback((name: string | null) => {
    setCatalogState(name);
    setOverlay(null);
  }, []);

  const reset = useCallback(() => {
    setCatalogState(null);
    setOverlay(null);
    // Ohne Datenbestand gibt es nichts vorzuführen — und der Vorführmodus
    // würde die Quellenauswahl verbergen, die jetzt gebraucht wird.
    setPresenting(false);
  }, []);

  const value = useMemo(
    () => ({ catalog, setCatalog, overlay, setOverlay, reset, presenting, setPresenting }),
    [catalog, setCatalog, overlay, reset, presenting],
  );

  return <SourceContext.Provider value={value}>{children}</SourceContext.Provider>;
}

export function usePortalSource(): PortalSource {
  const ctx = useContext(SourceContext);
  if (!ctx) throw new Error("usePortalSource outside PortalSourceProvider");
  return ctx;
}

/** Die Datensätze des geladenen Katalogs. */
export function useCatalog(): {
  datasets: CatalogDataset[];
  loading: boolean;
  error: boolean;
} {
  const { catalog } = usePortalSource();
  const query = useCatalogDatasets(catalog);
  return {
    datasets: query.data ?? [],
    loading: query.isLoading,
    error: query.isError,
  };
}

/** Kurzbewertung je Dateistamm aus einem Job-Ergebnis ableiten. */
function rowFromResult(stem: string, result: AnalysisResult): RunIndexRow {
  const counts = { pass: 0, partial: 0, fail: 0 };
  for (const dim of Object.values(result.by_dimension)) {
    for (const indicator of dim.indicators) {
      if (indicator.status === "pass") counts.pass += 1;
      else if (indicator.status === "partial") counts.partial += 1;
      else counts.fail += 1;
    }
  }
  return {
    stem,
    overall: result.summary.overall_score,
    grade: result.summary.quality_grade,
    dims: result.summary.dimension_scores,
    dim_weights: result.summary.dimension_weights,
    total_indicators: result.summary.total_indicators,
    n_pass: counts.pass,
    n_partial: counts.partial,
    n_fail: counts.fail,
  };
}

export interface OverlayState {
  /** Kurzbewertung je Dateistamm; leer, solange keine Bewertung anliegt. */
  rows: Map<string, RunIndexRow>;
  /** Vollständiges Ergebnis, sofern es *ohne Nachladen* vorliegt (Job-Fall). */
  resultFor: (stem: string) => AnalysisResult | undefined;
  active: boolean;
  loading: boolean;
  error: boolean;
  /** Fortschritt einer laufenden Berechnung, sonst null. */
  progress: { done: number; total: number; current?: string | null } | null;
}

/**
 * Die aktuell anliegende Bewertung, unabhängig von ihrer Herkunft.
 *
 * Der Lauf-Fall lädt nur den Index; das vollständige Ergebnis einer Datei holt
 * die Detailseite gezielt nach (`useRunResult`), weil Einzelergebnisse einige
 * hundert Kilobyte groß sind und niemand 50 davon auf einmal braucht.
 */
export function useOverlay(): OverlayState {
  const { overlay } = usePortalSource();
  const runIndex = useRunIndex(overlay?.kind === "run" ? overlay.run : null);
  // Ein Overlay-Job läuft über den ganzen Bestand; nur Fortschritt pollen und
  // die Ergebnisse am Ende einmal holen (siehe useJob).
  const job = useJob(overlay?.kind === "job" ? overlay.jobId : null, true);

  return useMemo(() => {
    if (overlay?.kind === "run") {
      const rows = new Map((runIndex.data ?? []).map((row) => [row.stem, row]));
      return {
        rows,
        resultFor: () => undefined,
        active: true,
        loading: runIndex.isLoading,
        error: runIndex.isError,
        progress: null,
      };
    }

    if (overlay?.kind === "job") {
      const results = new Map<string, AnalysisResult>();
      const rows = new Map<string, RunIndexRow>();
      for (const file of job.data?.results ?? []) {
        if (!file.result) continue;
        const stem = file.filename.replace(/\.[^.]+$/, "");
        results.set(stem, file.result);
        rows.set(stem, rowFromResult(stem, file.result));
      }
      const running = job.data ? job.data.status === "queued" || job.data.status === "running" : true;
      return {
        rows,
        resultFor: (stem: string) => results.get(stem),
        active: true,
        loading: running,
        error: job.isError || job.data?.status === "error",
        progress: job.data
          ? {
              done: job.data.progress.done,
              total: job.data.progress.total,
              current: job.data.progress.current_file,
            }
          : null,
      };
    }

    return {
      rows: new Map(),
      resultFor: () => undefined,
      active: false,
      loading: false,
      error: false,
      progress: null,
    };
  }, [overlay, runIndex.data, runIndex.isLoading, runIndex.isError, job.data, job.isError]);
}
