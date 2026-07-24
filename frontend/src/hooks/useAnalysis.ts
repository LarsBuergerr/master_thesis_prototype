import { useMutation, useQuery } from "@tanstack/react-query";
import {
  analyzeSample,
  fetchIndicators,
  fetchJob,
  fetchSampleRdf,
  submitAnalysis,
} from "../api/client";
import type { AnalysisConfigInput } from "../api/types";

export function useIndicators() {
  return useQuery({
    queryKey: ["indicators"],
    queryFn: fetchIndicators,
    staleTime: Infinity,
  });
}

export function useSubmitAnalysis() {
  return useMutation({
    mutationFn: (vars: { files: File[]; config: AnalysisConfigInput }) =>
      submitAnalysis(vars.files, vars.config),
  });
}

/**
 * Polls a job until it reaches a terminal state. ``refetchInterval`` returns
 * ``false`` once done/error so polling stops automatically.
 */
/** Startet einen echten Analyselauf über eine Datei der Stichprobe. */
export function useAnalyzeSample() {
  return useMutation({
    mutationFn: (vars: { name: string; config: AnalysisConfigInput }) =>
      analyzeSample(vars.name, vars.config),
  });
}

/**
 * RDF-Quelltext eines Stichproben-Datensatzes. Wird nur geladen, wenn ein
 * Backend erreichbar ist; schlägt der Abruf fehl, zeigt die Detailseite die
 * Befunde weiterhin — nur ohne Fundstellen im Quelltext.
 */
export function useSampleRdf(name: string | null) {
  return useQuery({
    queryKey: ["sample-rdf", name],
    queryFn: () => fetchSampleRdf(name as string),
    enabled: !!name,
    staleTime: Infinity,
    retry: false,
  });
}

export function useJob(jobId: string | null) {
  return useQuery({
    queryKey: ["job", jobId],
    queryFn: () => fetchJob(jobId as string),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      return status === "done" || status === "error" ? false : 1000;
    },
  });
}
