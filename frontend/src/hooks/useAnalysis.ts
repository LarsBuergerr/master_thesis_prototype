import { useMutation, useQuery } from "@tanstack/react-query";
import { fetchIndicators, fetchJob, submitAnalysis } from "../api/client";
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
