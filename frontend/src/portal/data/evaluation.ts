// Datenzugriff auf die Evaluationsstichprobe (n = 50), mit der die Bewertung
// in der Masterarbeit durchgeführt wurde. Quelle: outputs/mqa_comparison/
// comparison_sample_2026-06-25_09-57_gpt5-5_final (+ RDF-Metadaten der
// Stichprobe). Die JSON wird zur Bauzeit gebündelt (resolveJsonModule) und
// hier einmalig in domänennahe, camelCase-Objekte übersetzt.

import type { Finding, Remediation } from "../../api/types";
import raw from "./evaluation.json";

export type Stratum = "geo" | "non_geo";
export type ModelStatus = "pass" | "partial" | "fail";

/**
 * Ein Indikator-Ergebnis der Stichprobe. `message` und `remediation` stammen
 * 1:1 aus dem Referenz-Run, `finding` erzeugt derselbe Backend-Code, den auch
 * ein Live-Lauf benutzt (siehe scripts/enrich_portal_evaluation.py). Die
 * Felder entsprechen damit exakt dem, was das Backend liefert — die
 * Detailseite stellt beide Quellen identisch dar.
 */
export interface RawIndicator {
  id: string;
  dim: string;
  status: ModelStatus;
  score: number;
  message?: string;
  finding?: Finding | null;
  remediation?: Remediation | null;
  weight?: number;
  rawScore?: number;
  rawStatus?: string;
}

export interface Dataset {
  id: string;
  slug: string;
  /** RDF-Datei der Stichprobe — Schlüssel für den Live-Lauf über /samples. */
  file: string;
  title: string;
  description: string;
  publisher: string;
  publisherName: string;
  stratum: Stratum;
  modified: string;
  keywords: string[];
  themes: string[];
  formats: string[];
  license: string | null;
  /** Gesamtscore des Prototyps, 0..1. */
  overall: number;
  /** Score je Dimension (findability/accessibility/reusability/expressiveness). */
  dims: Record<string, number>;
  indicators: RawIndicator[];
  nPass: number;
  nPartial: number;
  nFail: number;
  /** Normierter MQA-Referenzscore (data.europa.eu), 0..1. */
  mqaNorm: number | null;
  /** Normierter Prototyp-Score im Vergleich (0..1). */
  protoNorm: number | null;
  /** Normierter MQA-Score im Vergleich (0..1). */
  mqaScoreNorm: number | null;
}

export interface GtRow {
  ziel: string;
  protRho: number;
  mqaRho: number;
  delta: number;
}

export interface Aggregate {
  n: number;
  overallMean: number;
  overallMin: number;
  overallMax: number;
  dimAvg: Record<string, number>;
  strata: Record<string, number>;
  publishers: Record<string, number>;
}

interface RawDataset {
  id: string;
  slug: string;
  file: string;
  publisher: string;
  stratum: string;
  title: string;
  description: string;
  modified: string;
  keywords: string[];
  themes: string[];
  formats: string[];
  license: string | null;
  publisher_name: string;
  overall: number;
  dims: Record<string, number>;
  indicators: RawIndicator[];
  n_pass: number;
  n_partial: number;
  n_fail: number;
  mqa_norm: number | null;
  model_norm: number | null;
  mqa_score_norm: number | null;
}

interface RawFile {
  datasets: RawDataset[];
  agg: {
    n: number;
    overall_mean: number;
    overall_min: number;
    overall_max: number;
    dim_avg: Record<string, number>;
    strata: Record<string, number>;
    publishers: Record<string, number>;
  };
  gt: { ziel: string; prot_rho: number; mqa_rho: number; delta: number }[];
}

const file = raw as unknown as RawFile;

export const DATASETS: Dataset[] = file.datasets.map((d) => ({
  id: d.id,
  slug: d.slug,
  file: d.file,
  title: d.title,
  description: d.description,
  publisher: d.publisher,
  publisherName: d.publisher_name,
  stratum: (d.stratum === "geo" ? "geo" : "non_geo") as Stratum,
  modified: d.modified,
  keywords: d.keywords,
  themes: d.themes,
  formats: d.formats,
  license: d.license,
  overall: d.overall,
  dims: d.dims,
  indicators: d.indicators,
  nPass: d.n_pass,
  nPartial: d.n_partial,
  nFail: d.n_fail,
  mqaNorm: d.mqa_norm,
  protoNorm: d.model_norm,
  mqaScoreNorm: d.mqa_score_norm,
}));

export const AGGREGATE: Aggregate = {
  n: file.agg.n,
  overallMean: file.agg.overall_mean,
  overallMin: file.agg.overall_min,
  overallMax: file.agg.overall_max,
  dimAvg: file.agg.dim_avg,
  strata: file.agg.strata,
  publishers: file.agg.publishers,
};

export const GROUND_TRUTH: GtRow[] = file.gt.map((r) => ({
  ziel: r.ziel,
  protRho: r.prot_rho,
  mqaRho: r.mqa_rho,
  delta: r.delta,
}));

export function datasetById(id: string): Dataset | undefined {
  return DATASETS.find((d) => d.id === id);
}
