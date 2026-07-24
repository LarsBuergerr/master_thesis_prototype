// Sortiert Vokabular-Kandidaten nach Nähe zum aktuell eingetragenen Wert.
//
// Ein kontrolliertes Vokabular hat schnell mehrere hundert bis tausend
// Einträge (IANA-Media-Types). Eine alphabetische Auswahlliste hilft dem
// Datenbereitsteller nicht — steht im Metadatensatz „SHP", ist
// „…/file-type/SHP" gemeint. Deshalb wird der wahrscheinlichste Kandidat
// vorne einsortiert und als Vorschlag in den Diff gesetzt.

/** Lokaler Name einer URI, also das letzte Pfadsegment. */
export function localName(uri: string): string {
  return uri.replace(/[/#]$/, "").split(/[/#]/).pop() ?? uri;
}

function similarity(a: string, b: string): number {
  const x = a.toLowerCase();
  const y = b.toLowerCase();
  if (x === y) return 1;
  if (x.includes(y) || y.includes(x)) return 0.8;

  let common = 0;
  while (common < x.length && common < y.length && x[common] === y[common]) common++;
  return common / Math.max(x.length, y.length);
}

/**
 * Kandidaten nach Ähnlichkeit zu den vorhandenen Werten sortieren. Ohne
 * Anhaltspunkte bleibt die Reihenfolge des Backends erhalten.
 */
export function rankCandidates(candidates: string[], hints: string[]): string[] {
  if (hints.length === 0) return candidates;
  const tails = hints.map(localName);
  return [...candidates].sort(
    (a, b) =>
      Math.max(...tails.map((t) => similarity(localName(b), t))) -
      Math.max(...tails.map((t) => similarity(localName(a), t))),
  );
}

/** Werte, die im Metadatensatz stehen — Grundlage für die Sortierung. */
export function hintsFromDetails(details: Record<string, unknown>): string[] {
  const out: string[] = [];
  const push = (value: unknown) => {
    if (Array.isArray(value)) out.push(...value.filter((v): v is string => typeof v === "string"));
  };

  for (const key of ["formats", "media_types", "invalid", "values"]) push(details[key]);
  if (Array.isArray(details.per_distribution)) {
    for (const entry of details.per_distribution) {
      if (entry && typeof entry === "object") {
        const row = entry as Record<string, unknown>;
        for (const key of ["formats", "media_types", "licenses", "availability"]) push(row[key]);
      }
    }
  }
  return out.slice(0, 8);
}
