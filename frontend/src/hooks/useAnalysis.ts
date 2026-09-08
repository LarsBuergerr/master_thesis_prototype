import { useMutation, useQuery } from "@tanstack/react-query";
import {
  fetchDefaultConfig,
  fetchIndicators,
  fetchJob,
  submitAnalysis,
} from "../api/client";
import { applyIndicatorsResponse } from "../lib/indicators";
import type { AnalysisConfigInput } from "../api/types";

/**
 * Indikator-Registry inklusive Klartext-Guidance. Die Antwort füttert
 * zusätzlich den Katalog in `lib/indicators`, damit Ergebnisse überall mit den
 * Texten des Backends beschriftet werden — bis dahin gilt der gebündelte
 * Abzug.
 */
export function useIndicators() {
  return useQuery({
    queryKey: ["indicators"],
    queryFn: async () => {
      const data = await fetchIndicators();
      applyIndicatorsResponse(data);
      return data;
    },
    staleTime: Infinity,
  });
}

/**
 * Referenz-Konfiguration der Evaluation vom Server. Sie ist die einzige Quelle
 * für Gewichte, Score-Policy und Indikator-Menge — ohne sie startet die
 * Oberfläche keinen Lauf, weil ein Lauf mit anderen Einstellungen andere Zahlen
 * liefern würde als die Arbeit ausweist.
 */
export function useDefaultConfig() {
  return useQuery({
    queryKey: ["default-config"],
    queryFn: fetchDefaultConfig,
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
 *
 * ``deferResults`` pollt nur Status und Fortschritt und holt die Ergebnisse
 * erst am Ende. Für einen Lauf über einen ganzen Datenbestand ist das der
 * Unterschied zwischen ein paar hundert Byte und zweistelligen Megabyte pro
 * Sekunde; bei ein bis zwei Dateien lohnt es nicht.
 */
export function useJob(jobId: string | null, deferResults = false) {
  const status = useQuery({
    queryKey: ["job", jobId, deferResults ? "status" : "full"],
    queryFn: () => fetchJob(jobId as string, !deferResults),
    enabled: !!jobId,
    refetchInterval: (query) => {
      const state = query.state.data?.status;
      return state === "done" || state === "error" ? false : 1000;
    },
  });

  const finished = status.data?.status === "done" || status.data?.status === "error";
  const results = useQuery({
    queryKey: ["job-results", jobId],
    queryFn: () => fetchJob(jobId as string, true),
    enabled: !!jobId && deferResults && finished,
    staleTime: Infinity,
  });

  if (!deferResults) return status;
  return {
    ...status,
    data: results.data ?? status.data,
    isError: status.isError || results.isError,
  };
}
