// Mirrors backend/schemas.py. Kept hand-written (small surface); could be
// generated from the backend's OpenAPI schema with openapi-typescript.

export type JobState = "queued" | "running" | "done" | "error";
export type IndicatorStatus =
  | "pass"
  | "partial"
  | "fail"
  | "not_applicable"
  | "error";

export interface IndicatorInfo {
  indicator_id: string;
  name_de: string;
  name_en: string;
  dimension: string;
  description_de: string;
  description_en: string;
  default_weight: number;
  graded: boolean;
}

export interface IndicatorsResponse {
  dimensions: string[];
  indicators: IndicatorInfo[];
}

// Mirrors core/remediation.py. Attached to FAIL/PARTIAL results only.
export type RdfTermKind = "uri" | "literal" | "bnode";

export interface RdfTerm {
  type: RdfTermKind;
  value: string;
}

export interface ChangeOp {
  op: "add" | "remove";
  subject: string;
  predicate: string;
  object: RdfTerm;
  reason: string;
}

export interface FieldSuggestion {
  indicator_id: string;
  subject: string;
  predicate: string;
  candidates: string[];
  reason: string;
}

export interface ChangePatch {
  kind: "change_patch";
  ready: ChangeOp[];
  needs_input: FieldSuggestion[];
  summary_de: string;
  summary_en: string;
}

export interface Recommendation {
  kind: "recommendation";
  message_de: string;
  message_en: string;
  findings: string[];
  see_also: string[];
}

export type Remediation = ChangePatch | Recommendation;

export interface IndicatorResult {
  indicator_id: string;
  name_de: string;
  name_en: string;
  dimension?: string | null;
  status: IndicatorStatus;
  score?: number | null;
  raw_status?: string | null;
  raw_score?: number | null;
  effective_score?: number | null;
  default_weight?: number | null;
  effective_weight?: number | null;
  message_de: string;
  message_en: string;
  details: Record<string, unknown>;
  error?: string | null;
  remediation?: Remediation | null;
}

export interface DimensionResult {
  dimension: string;
  score: number;
  dimension_weight: number;
  total_indicator_weight: number;
  indicator_count: number;
  pass_count: number;
  pass_rate: number;
  indicators: IndicatorResult[];
}

export interface Summary {
  overall_score: number;
  quality_grade: string;
  overall_pass_rate: number;
  dimension_scores: Record<string, number>;
  dimension_weights: Record<string, number>;
  total_indicators: number;
  total_pass: number;
  total_fail: number;
}

export interface AnalysisResult {
  by_dimension: Record<string, DimensionResult>;
  summary: Summary;
  weights: Record<string, unknown>;
  llm_usage: Array<Record<string, unknown>>;
  errors: string[];
}

export interface JobProgress {
  done: number;
  total: number;
  current_file?: string | null;
}

export interface FileResult {
  filename: string;
  result?: AnalysisResult | null;
  error?: string | null;
}

export interface JobDetail {
  job_id: string;
  status: JobState;
  created_at: string;
  updated_at: string;
  progress: JobProgress;
  files: string[];
  error?: string | null;
  config: AnalysisConfigInput;
  results: FileResult[];
}

export interface JobCreated {
  job_id: string;
  status: JobState;
}

// ---- request config ----

export interface ScoringOverride {
  pass_score?: number | null;
  partial_score?: number | null;
  fail_score?: number | null;
  allow_partial?: boolean | null;
}

export interface ScoringConfig {
  pass_score: number;
  partial_score: number;
  fail_score: number;
  allow_partial: boolean;
  overrides: Record<string, ScoringOverride>;
}

export interface LLMConfig {
  enabled: boolean;
  provider: string;
  model?: string | null;
  base_url?: string | null;
  temperature: number;
  max_tokens: number;
}

export interface AnalysisConfigInput {
  dimension_whitelist?: string[] | null;
  indicator_blacklist?: string[] | null;
  indicator_whitelist?: string[] | null;
  dimension_weights: Record<string, number>;
  indicator_weights: Record<string, number>;
  scoring?: ScoringConfig | null;
  llm: LLMConfig;
  language: string;
  max_workers: number;
}
