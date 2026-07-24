// Ausschnitte aus dem RDF-Quelltext des Metadatensatzes.
//
// Ein Befund ist erst dann umsetzbar, wenn klar ist, an welcher Stelle der
// Datei nachgebessert werden muss. Steht der Quelltext zur Verfügung (Live-Lauf
// über /samples/{name}/rdf), zeigt die Detailseite die betroffenen Zeilen mit
// Zeilennummer — analog zu einem Diff-Hunk.

export interface RdfLine {
  no: number;
  text: string;
}

/** Feld-Kurzschreibweisen („dcat:keyword“) → lokale Namen („keyword“). */
export function fieldTerms(field: string): string[] {
  const terms = new Set<string>();
  for (const match of field.matchAll(/[A-Za-z]+:([A-Za-z][A-Za-z0-9_]*)/g)) {
    terms.add(match[1]);
  }
  return [...terms];
}

/**
 * Zeilen des RDF-Quelltexts, die eines der Felder erwähnen. `maxLines` deckelt
 * die Ausgabe, damit ein Datensatz mit 40 Distributionen die Tabelle nicht
 * sprengt.
 */
export function rdfExcerpt(rdf: string, terms: string[], maxLines = 8): RdfLine[] {
  if (!rdf || terms.length === 0) return [];
  const pattern = new RegExp(`:(${terms.join("|")})\\b`, "i");
  const out: RdfLine[] = [];

  const lines = rdf.split(/\r?\n/);
  for (let i = 0; i < lines.length && out.length < maxLines; i++) {
    if (pattern.test(lines[i])) {
      out.push({ no: i + 1, text: lines[i].trim().slice(0, 300) });
    }
  }
  return out;
}
