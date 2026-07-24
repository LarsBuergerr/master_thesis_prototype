// Zugriff auf das Klartext-Wissen zu den Indikatoren.
//
// Die Texte (sprechender Name, Erklärung, betroffenes Feld,
// Handlungsanweisung, Vokabular) stehen im Backend in `src/core/guidance.py`
// und kommen über `GET /indicators`. Hier liegt nur der Zugriff:
//
//   * `setGuidanceCatalog()` — füttert die Antwort des Backends ein
//     (aufgerufen von `useIndicators`, sobald die Registry geladen ist)
//   * `indicatorMeta()` / `dimensionLabel()` / `columnHelp()` — lesen
//
// Solange kein Backend erreichbar ist, greift der mitgelieferte Abzug
// (`portal/data/indicator_guidance.json`, erzeugt von
// `scripts/export_indicator_guidance.py`). Die Portalseite bleibt damit auch
// offline vollständig lesbar, ohne dass die Texte zweimal gepflegt werden.

import type { IndicatorGuidance, IndicatorsResponse } from "../api/types";
import snapshot from "../portal/data/indicator_guidance.json";

let guidanceById: Record<string, IndicatorGuidance> = {};
let nameById: Record<string, string> = {};
let dimensionInfo: Record<string, { label_de: string; what_de: string }> = {};
let glossary: Record<string, string> = {};

/** Übernimmt Katalogdaten (Backend-Antwort oder gebündelter Abzug). */
export function setGuidanceCatalog(data: {
  indicators: { indicator_id: string; name_de?: string; guidance?: IndicatorGuidance | null }[];
  dimension_info?: { dimension: string; label_de: string; what_de: string }[];
  score_glossary?: Record<string, string>;
}): void {
  const nextGuidance: Record<string, IndicatorGuidance> = {};
  const nextNames: Record<string, string> = {};
  for (const ind of data.indicators) {
    if (ind.guidance) nextGuidance[ind.indicator_id] = ind.guidance;
    if (ind.name_de) nextNames[ind.indicator_id] = ind.name_de;
  }
  guidanceById = nextGuidance;
  nameById = nextNames;

  const nextDims: Record<string, { label_de: string; what_de: string }> = {};
  for (const dim of data.dimension_info ?? []) {
    nextDims[dim.dimension] = { label_de: dim.label_de, what_de: dim.what_de };
  }
  dimensionInfo = nextDims;
  glossary = data.score_glossary ?? {};
}

// Abzug sofort laden: die Portalseite rendert hinterlegte Ergebnisse, bevor
// (oder ohne dass) das Backend antwortet.
setGuidanceCatalog(snapshot as Parameters<typeof setGuidanceCatalog>[0]);

/** Aktualisiert den Katalog aus einer `/indicators`-Antwort. */
export function applyIndicatorsResponse(data: IndicatorsResponse): void {
  setGuidanceCatalog(data);
}

export interface IndicatorMeta {
  /** Sprechender Name statt der technischen ID. */
  label: string;
  /** Was der Indikator prüft — Text des Info-Icons. */
  what: string;
  /** Betroffenes Metadatenfeld in DCAT-AP.de-Schreibweise. */
  field: string;
  /** Was zu tun ist, um den Indikator zu erfüllen. */
  fix: string;
  vocab?: { label: string; url: string };
}

/**
 * Klartext zu einer Indikator-ID. Fehlt der Eintrag (neuer Indikator, für den
 * noch kein Text hinterlegt ist), wird auf den Namen aus dem Ergebnis bzw. der
 * Registry zurückgefallen.
 */
export function indicatorMeta(id: string, fallbackName?: string): IndicatorMeta {
  const guidance = guidanceById[id];
  if (!guidance) {
    return {
      label: fallbackName || nameById[id] || id,
      what: "Für diesen Indikator liegt noch keine Kurzbeschreibung vor.",
      field: id,
      fix: "Siehe Prüfmeldung.",
    };
  }
  return {
    label: guidance.label_de,
    what: guidance.what_de,
    field: guidance.field,
    fix: guidance.fix_de,
    vocab: guidance.vocabulary
      ? { label: guidance.vocabulary.label_de, url: guidance.vocabulary.url }
      : undefined,
  };
}

export function dimensionLabel(dim: string): string {
  return dimensionInfo[dim]?.label_de ?? dim;
}

export function dimensionWhat(dim: string): string | undefined {
  return dimensionInfo[dim]?.what_de || undefined;
}

/** Erklärtext einer Tabellenspalte (status / score / raw / weight). */
export function columnHelp(key: "status" | "score" | "raw" | "weight"): string {
  return glossary[key] ?? "";
}
