// Ableitungen rund um die Qualitätsbewertung: Notenstufe und deutsche
// Noten-/Dimensionslabels.
//
// Eine Übersetzung von Lauf-Ergebnissen in die `AnalysisResult`-Struktur
// braucht es nicht mehr: ein Lauf liefert genau diese Struktur, und die
// Ergebniskomponenten (OverallScoreCard, DimensionRadar, DimensionPanel)
// nehmen sie unverändert entgegen.

import { dimensionLabel } from "../../lib/indicators";
import { scorePoints } from "../../lib/status";

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

/** Score als Punkte von 100 — dieselbe Rechnung wie im Analyzer (lib/status). */
export const scorePct = scorePoints;

/**
 * Deutsche Bezeichnungen der EU-Datenthemen (MDR-Vokabular `data-theme`), auf
 * die DCAT-AP.de `dcat:theme` verweist. Der Katalog liefert nur den Code
 * („GOVE"); als Chip in der Trefferliste sagt der niemandem etwas, der ihn
 * nicht auswendig kennt.
 */
const THEME_LABELS: Record<string, string> = {
  AGRI: "Landwirtschaft und Ernährung",
  ECON: "Wirtschaft und Finanzen",
  EDUC: "Bildung, Kultur und Sport",
  ENER: "Energie",
  ENVI: "Umwelt",
  GOVE: "Regierung und öffentlicher Sektor",
  HEAL: "Gesundheit",
  INTR: "Internationale Themen",
  JUST: "Justiz und öffentliche Sicherheit",
  OP_DATPRO: "Vorläufige Daten",
  REGI: "Regionen und Städte",
  SOCI: "Bevölkerung und Gesellschaft",
  TECH: "Wissenschaft und Technologie",
  TRAN: "Verkehr",
};

/** Klartext zu einem Datenthema; unbekannte Codes bleiben, wie sie sind. */
export function themeLabel(theme: string): string {
  const code = theme.split(/[/#]/).pop() ?? theme;
  return THEME_LABELS[code.toUpperCase()] ?? theme;
}
