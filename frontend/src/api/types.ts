// Mirrors backend/schemas.py. Kept hand-written (small surface); could be
// generated from the backend's OpenAPI schema with openapi-typescript.

export type JobState = "queued" | "running" | "done" | "error";
export type IndicatorStatus =
  | "pass"
  | "partial"
  | "fail"
  | "not_applicable"
  | "error";

// Mirrors core/guidance.py — the plain-German layer over an indicator:
// what it checks, which field it touches and what to do about it.
export interface Vocabulary {
  label_de: string;
  url: string;
}

export interface IndicatorGuidance {
  label_de: string;
  what_de: string;
  field: string;
  fix_de: string;
  vocabulary?: Vocabulary | null;
}

export interface IndicatorInfo {
  indicator_id: string;
  name_de: string;
  name_en: string;
  dimension: string;
  description_de: string;
  description_en: string;
  default_weight: number;
  graded: boolean;
  guidance?: IndicatorGuidance | null;
}

export interface DimensionInfo {
  dimension: string;
  label_de: string;
  what_de: string;
}

export interface IndicatorsResponse {
  dimensions: string[];
  indicators: IndicatorInfo[];
  dimension_info: DimensionInfo[];
  score_glossary: Record<string, string>;
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

/**
 * Stelle im Graphen, an der ein Wert fehlt. Beschrieben wird die *Form* des
 * erwarteten Werts — nicht die Menge der zulässigen Werte: die steht im
 * verlinkten Vokabular (siehe core/remediation.py::FieldSuggestion).
 */
export interface FieldSuggestion {
  indicator_id: string;
  subject: string;
  predicate: string;
  reason: string;
  /** Erwartete Form in einem Satz. */
  expected_de: string;
  expected_en: string;
  /** Ein Wert, der die Schreibweise zeigt — Formbeispiel, keine Empfehlung. */
  example?: string | null;
  vocabulary_label?: string | null;
  vocabulary_url?: string | null;
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

// Mirrors core/finding.py. Attached to FAIL/PARTIAL/ERROR results: the
// indicator's `details` turned into an Ist/Soll comparison a data provider can
// act on. Built in the backend (scoring/findings.py), never in the UI.
export type FindingTone = "bad" | "warn" | "good" | "neutral";

export interface FactLine {
  label: string;
  value: string;
  tone: FindingTone;
  /** Fundstelle im Metadatensatz (Distributions-URI, SHACL-Pfad …). */
  where?: string | null;
}

export interface Finding {
  headline: string;
  current: FactLine[];
  target?: string | null;
  notes: string[];
}

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
  finding?: Finding | null;
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
  /** Fehlen bei `results=false` — dann trägt die Antwort nur den Fortschritt. */
  config?: AnalysisConfigInput | null;
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

// ---- Katalog: beschreibende Metadaten (spiegelt backend/catalog.py) --------

export interface CatalogInfo {
  name: string;
  dataset_count: number;
}

/** Ein Datensatz, wie ihn das Portal ohne jede Bewertung anzeigt. */
export interface CatalogDataset {
  /** Dateiname inkl. Endung — Adresse innerhalb des Katalogs. */
  file: string;
  /** Dateistamm — der Schlüssel, über den ein Lauf zugeordnet wird. */
  id: string;
  slug: string;
  uri?: string | null;
  title: string;
  description: string;
  keywords: string[];
  themes: string[];
  formats: string[];
  license?: string | null;
  license_uri?: string | null;
  modified: string;
  issued: string;
  publisher_name: string;
  category?: string | null;
  source?: string | null;
}

// ---- Läufe: Bewertung (spiegelt backend/runs.py) ---------------------------

export interface RunInfo {
  name: string;
  dataset_count: number;
  /** Datenverzeichnis des Laufs — zeigt, ob er zum geladenen Katalog passt. */
  directory?: string | null;
  /** Modell der Aussagekraft-Bewertung; `null` = ohne Sprachmodell gelaufen. */
  llm_model?: string | null;
  dimensions: string[];
}

export interface RunIndexRow {
  stem: string;
  overall?: number | null;
  grade?: string | null;
  dims: Record<string, number>;
  dim_weights: Record<string, number>;
  total_indicators: number;
  n_pass: number;
  n_partial: number;
  n_fail: number;
}

/** Wie oft ein Indikator über einen Lauf hinweg nicht erfüllt wurde. */
export interface RunDeficit {
  indicator_id: string;
  dimension?: string | null;
  fail: number;
  partial: number;
  total: number;
}

/** Ein Lauf im Qualitätsverlauf eines Datenbestands. */
export interface RunTrendPoint {
  run: string;
  timestamp?: string | null;
  dataset_count: number;
  mean_overall: number;
  min_overall: number;
  max_overall: number;
  llm_model?: string | null;
}

/** Antwort von `GET /config/default` — die Konfiguration der Evaluation. */
export interface DefaultConfigResponse {
  config: AnalysisConfigInput;
  /** Dateiname der Referenz-YAML; `null` heißt: Server nutzt nur Feld-Defaults. */
  source: string | null;
}
