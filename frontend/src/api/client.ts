import axios from "axios";
import type {
  AnalysisConfigInput,
  AnalysisResult,
  CatalogDataset,
  CatalogInfo,
  DefaultConfigResponse,
  IndicatorsResponse,
  JobCreated,
  JobDetail,
  RunIndexRow,
  RunInfo,
} from "./types";

const baseURL = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export const api = axios.create({ baseURL });

export async function fetchIndicators(): Promise<IndicatorsResponse> {
  const { data } = await api.get<IndicatorsResponse>("/indicators");
  return data;
}

/**
 * Konfiguration der Evaluation, wie sie auf dem Server liegt. Ausgangspunkt
 * jedes Laufs im Frontend, damit Upload-Werkzeug und Portal-Livelauf dieselben
 * Gewichte und dieselbe Indikator-Menge fahren wie die Arbeit.
 */
export async function fetchDefaultConfig(): Promise<DefaultConfigResponse> {
  const { data } = await api.get<DefaultConfigResponse>("/config/default");
  return data;
}

export async function submitAnalysis(
  files: File[],
  config: AnalysisConfigInput,
): Promise<JobCreated> {
  const form = new FormData();
  for (const f of files) form.append("files", f, f.name);
  form.append("config", JSON.stringify(config));
  const { data } = await api.post<JobCreated>("/analyze", form);
  return data;
}

/**
 * Job-Zustand. `includeResults: false` liefert nur Status und Fortschritt —
 * die richtige Form fürs Pollen eines Laufs über viele Dateien, dessen
 * Ergebnisse sich auf etliche Megabyte summieren.
 */
export async function fetchJob(jobId: string, includeResults = true): Promise<JobDetail> {
  const { data } = await api.get<JobDetail>(`/jobs/${jobId}`, {
    params: includeResults ? undefined : { results: false },
  });
  return data;
}

// ---- Ebene 1: Katalog (beschreibende Metadaten) ----------------------------
// Ein Datenverzeichnis voller RDF-Dateien ergibt die Portalinhalte. Diese
// Ebene weiß nichts von Bewertung — sie ist für sich vollständig.

const enc = encodeURIComponent;

export async function fetchCatalogs(): Promise<CatalogInfo[]> {
  const { data } = await api.get<CatalogInfo[]>("/catalogs");
  return data;
}

export async function fetchCatalogDatasets(name: string): Promise<CatalogDataset[]> {
  const { data } = await api.get<CatalogDataset[]>(`/catalogs/${enc(name)}/datasets`);
  return data;
}

/** RDF-Quelltext einer Datei (für die Fundstellen-Anzeige im Befund). */
export async function fetchCatalogRdf(name: string, file: string): Promise<string> {
  const { data } = await api.get<string>(`/catalogs/${enc(name)}/files/${enc(file)}/rdf`, {
    responseType: "text",
    transformResponse: (v) => v,
  });
  return data;
}

/** Bewertet alle Dateien des Verzeichnisses; liefert die Job-ID. */
export async function analyzeCatalog(
  name: string,
  config: AnalysisConfigInput,
): Promise<JobCreated> {
  const { data } = await api.post<JobCreated>(`/catalogs/${enc(name)}/analyze`, null, {
    params: { config: JSON.stringify(config) },
  });
  return data;
}

/** Bewertet eine einzelne Datei des Verzeichnisses. */
export async function analyzeCatalogFile(
  name: string,
  file: string,
  config: AnalysisConfigInput,
): Promise<JobCreated> {
  const { data } = await api.post<JobCreated>(
    `/catalogs/${enc(name)}/files/${enc(file)}/analyze`,
    null,
    { params: { config: JSON.stringify(config) } },
  );
  return data;
}

// ---- Ebene 2: Läufe (Bewertung) --------------------------------------------
// Ein abgeschlossener Lauf legt sich über den Katalog. Verknüpft wird allein
// über den Dateinamen; ein Lauf trägt keine Titel oder Schlagwörter.

export async function fetchRuns(): Promise<RunInfo[]> {
  const { data } = await api.get<RunInfo[]>("/runs");
  return data;
}

/** Kurzbewertung je Datei — klein genug für Liste und Übersichtsseite. */
export async function fetchRunIndex(name: string): Promise<RunIndexRow[]> {
  const { data } = await api.get<RunIndexRow[]>(`/runs/${enc(name)}`);
  return data;
}

/** Vollständiges Ergebnis einer Datei — für die Detailseite. */
export async function fetchRunResult(name: string, stem: string): Promise<AnalysisResult> {
  const { data } = await api.get<AnalysisResult>(`/runs/${enc(name)}/${enc(stem)}`);
  return data;
}
