import axios from "axios";
import type {
  AnalysisConfigInput,
  IndicatorsResponse,
  JobCreated,
  JobDetail,
} from "./types";

const baseURL = import.meta.env.VITE_API_BASE ?? "http://localhost:8000";

export const api = axios.create({ baseURL });

export async function fetchIndicators(): Promise<IndicatorsResponse> {
  const { data } = await api.get<IndicatorsResponse>("/indicators");
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

export async function fetchJob(jobId: string): Promise<JobDetail> {
  const { data } = await api.get<JobDetail>(`/jobs/${jobId}`);
  return data;
}

// ---- Stichprobe (Portal) ---------------------------------------------------
// Die Portalseite zeigt Datensätze der Evaluationsstichprobe. Damit sie nicht
// nur hinterlegte Zahlen wiedergibt, kann sie dieselbe RDF-Datei über das
// Backend live bewerten lassen — gleiche Pipeline wie beim Upload.

/** RDF-Quelltext eines Stichproben-Datensatzes (für die Fundstellen-Anzeige). */
export async function fetchSampleRdf(name: string): Promise<string> {
  const { data } = await api.get<string>(`/samples/${encodeURIComponent(name)}/rdf`, {
    responseType: "text",
    transformResponse: (v) => v,
  });
  return data;
}

/** Startet eine echte Analyse der Stichproben-Datei und liefert die Job-ID. */
export async function analyzeSample(
  name: string,
  config: AnalysisConfigInput,
): Promise<JobCreated> {
  const { data } = await api.post<JobCreated>(
    `/samples/${encodeURIComponent(name)}/analyze`,
    null,
    { params: { config: JSON.stringify(config) } },
  );
  return data;
}
