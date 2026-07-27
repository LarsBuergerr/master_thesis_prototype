// Datenzugriff der beiden Portalebenen.
//
// Ebene 1 (Katalog): beschreibende Metadaten eines Datenverzeichnisses — das
// ist der Portalinhalt und steht ohne jede Bewertung.
// Ebene 2 (Lauf): Scores eines abgeschlossenen Laufs, die sich darüberlegen.
//
// Beide Ebenen werden getrennt geladen und ausschließlich über den Dateistamm
// verknüpft (CatalogDataset.id === RunIndexRow.stem).

import { useMutation, useQuery } from "@tanstack/react-query";
import {
  analyzeCatalog,
  analyzeCatalogFile,
  fetchCatalogDatasets,
  fetchCatalogRdf,
  fetchCatalogs,
  fetchRunDeficits,
  fetchRunIndex,
  fetchRunResult,
  fetchRunTrend,
  fetchRuns,
} from "../api/client";
import type { AnalysisConfigInput } from "../api/types";

export function useCatalogs() {
  return useQuery({ queryKey: ["catalogs"], queryFn: fetchCatalogs, staleTime: Infinity });
}

export function useCatalogDatasets(catalog: string | null) {
  return useQuery({
    queryKey: ["catalog", catalog],
    queryFn: () => fetchCatalogDatasets(catalog as string),
    enabled: !!catalog,
    staleTime: Infinity,
  });
}

/**
 * RDF-Quelltext einer Datei. Nur für die Fundstellen-Anzeige; schlägt der
 * Abruf fehl, bleiben die Befunde vollständig — nur ohne Zeilenverweis.
 */
export function useCatalogRdf(catalog: string | null, file: string | null) {
  return useQuery({
    queryKey: ["catalog-rdf", catalog, file],
    queryFn: () => fetchCatalogRdf(catalog as string, file as string),
    enabled: !!catalog && !!file,
    staleTime: Infinity,
    retry: false,
  });
}

export function useRuns() {
  return useQuery({ queryKey: ["runs"], queryFn: fetchRuns, staleTime: Infinity });
}

export function useRunIndex(run: string | null) {
  return useQuery({
    queryKey: ["run-index", run],
    queryFn: () => fetchRunIndex(run as string),
    enabled: !!run,
    staleTime: Infinity,
  });
}

export function useRunResult(run: string | null, stem: string | null) {
  return useQuery({
    queryKey: ["run-result", run, stem],
    queryFn: () => fetchRunResult(run as string, stem as string),
    enabled: !!run && !!stem,
    staleTime: Infinity,
    retry: false,
  });
}

/** Häufigste Mängel eines abgeschlossenen Laufs. */
export function useRunDeficits(run: string | null) {
  return useQuery({
    queryKey: ["run-deficits", run],
    queryFn: () => fetchRunDeficits(run as string),
    enabled: !!run,
    staleTime: Infinity,
  });
}

/** Qualitätsverlauf über alle Läufe eines Datenbestands. */
export function useRunTrend(catalog: string | null) {
  return useQuery({
    queryKey: ["run-trend", catalog],
    queryFn: () => fetchRunTrend(catalog as string),
    enabled: !!catalog,
    staleTime: Infinity,
  });
}

export function useAnalyzeCatalog() {
  return useMutation({
    mutationFn: (vars: { catalog: string; config: AnalysisConfigInput }) =>
      analyzeCatalog(vars.catalog, vars.config),
  });
}

export function useAnalyzeCatalogFile() {
  return useMutation({
    mutationFn: (vars: { catalog: string; file: string; config: AnalysisConfigInput }) =>
      analyzeCatalogFile(vars.catalog, vars.file, vars.config),
  });
}
