// Ableitungen rund um die Qualitätsbewertung: Notenstufe und deutsche
// Noten-/Dimensionslabels.
//
// Eine Übersetzung von Lauf-Ergebnissen in die `AnalysisResult`-Struktur
// braucht es nicht mehr: ein Lauf liefert genau diese Struktur, und die
// Ergebniskomponenten (OverallScoreCard, DimensionRadar, DimensionPanel)
// nehmen sie unverändert entgegen.

import { dimensionLabel } from "../../lib/indicators";

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
