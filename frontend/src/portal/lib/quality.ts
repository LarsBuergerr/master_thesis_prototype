// Ableitungen rund um die Qualitätsbewertung eines Datensatzes: Notenstufe,
// deutsche Dimensions-/Notenlabels und die Übersetzung eines Stichproben-
// Datensatzes in die bestehende `AnalysisResult`-Struktur. Dadurch lassen sich
// die vorhandenen Dashboard-Komponenten (OverallScoreCard, DimensionRadar,
// DimensionPanel) unverändert für die Portal-Detailseite wiederverwenden.

import type {
  AnalysisResult,
  DimensionResult,
  IndicatorResult,
  Summary,
} from "../../api/types";
import { dimensionLabel, indicatorMeta } from "../../lib/indicators";
import type { Dataset } from "../data/evaluation";

export { dimensionLabel };

/** Score -> Note, identisch zu src/scoring/service.py::_score_to_grade. */
export function scoreToGrade(score: number): string {
  if (score >= 0.9) return "A";
  if (score >= 0.75) return "B";
  if (score >= 0.6) return "C";
  if (score >= 0.4) return "D";
  return "F";
}

/** Kompaktes, für Laien lesbares Qualitätsurteil (Balken/Indikator). */
export function gradeLabel(grade: string): string {
  switch (grade) {
    case "A":
      return "Ausgezeichnet";
    case "B":
      return "Gut";
    case "C":
      return "Befriedigend";
    case "D":
      return "Ausreichend";
    default:
      return "Mangelhaft";
  }
}

export const DIMENSION_ORDER = [
  "findability",
  "accessibility",
  "reusability",
  "expressiveness",
] as const;

export const scorePct = (score: number): number => Math.round(score * 100);

function toIndicatorResult(
  raw: Dataset["indicators"][number],
): IndicatorResult {
  return {
    indicator_id: raw.id,
    name_de: indicatorMeta(raw.id).label,
    name_en: raw.id,
    dimension: raw.dim,
    status: raw.status,
    score: raw.score,
    raw_status: raw.rawStatus ?? raw.status,
    raw_score: raw.rawScore ?? raw.score,
    effective_score: raw.score,
    default_weight: raw.weight ?? 1,
    effective_weight: raw.weight ?? 1,
    message_de: raw.message ?? "",
    message_en: raw.message ?? "",
    details: {},
    error: null,
    remediation: raw.remediation ?? null,
    finding: raw.finding ?? null,
  };
}

/**
 * Baut aus einem Stichproben-Datensatz eine `AnalysisResult`-Struktur, wie sie
 * das Backend liefern würde — damit die bestehenden Dashboard-Komponenten sie
 * direkt darstellen können.
 */
export function buildAnalysisResult(ds: Dataset): AnalysisResult {
  const byDimension: Record<string, DimensionResult> = {};

  for (const dim of DIMENSION_ORDER) {
    const inds = ds.indicators
      .filter((i) => i.dim === dim)
      .map(toIndicatorResult);
    if (inds.length === 0) continue;
    const passCount = inds.filter((i) => i.status === "pass").length;
    byDimension[dim] = {
      dimension: dim,
      score: ds.dims[dim] ?? 0,
      dimension_weight: 1,
      total_indicator_weight: inds.length,
      indicator_count: inds.length,
      pass_count: passCount,
      pass_rate: inds.length ? passCount / inds.length : 0,
      indicators: inds,
    };
  }

  const totalIndicators = ds.indicators.length;
  const dimensionScores: Record<string, number> = {};
  const dimensionWeights: Record<string, number> = {};
  for (const dim of DIMENSION_ORDER) {
    if (ds.dims[dim] !== undefined) {
      dimensionScores[dim] = ds.dims[dim];
      dimensionWeights[dim] = 1;
    }
  }

  const summary: Summary = {
    overall_score: ds.overall,
    quality_grade: scoreToGrade(ds.overall),
    overall_pass_rate: totalIndicators ? ds.nPass / totalIndicators : 0,
    dimension_scores: dimensionScores,
    dimension_weights: dimensionWeights,
    total_indicators: totalIndicators,
    total_pass: ds.nPass,
    total_fail: ds.nFail,
  };

  return {
    by_dimension: byDimension,
    summary,
    weights: {},
    llm_usage: [],
    errors: [],
  };
}
