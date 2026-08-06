// Aufgeklappter Befund zu einem Indikator.
//
// Der Inhalt kommt fertig aus dem Backend (`IndicatorResult.finding`, gebaut in
// scoring/findings.py) — hier wird er nur dargestellt: Ist-Zustand mit
// Fundstelle, die Hinweise dazu, Einzelbefunde und darunter genau EIN
// Detailblock.
//
// Welcher das ist, entscheidet `guidance.detail` (core/guidance.py):
//
//   template  Vorlage mit Beispielwert. Sie hängt nicht am Ist-Zustand und ist
//             deshalb dieselbe, ob das Feld falsch gesetzt ist oder ganz fehlt
//             — gerade dann ist sie die eigentliche Hilfe.
//   location  Die betroffenen Zeilen der geprüften Datei. Für Felder, deren
//             richtige Form vom Inhalt abhängt (Schlagwörter, LLM-Kriterien)
//             oder deren Problem außerhalb der Datei liegt (tote Links). Fehlt
//             das Feld ganz, gibt es keine Zeilen — dann entfällt der Block.
//   none      Nichts. Befund und Hinweis oben tragen bereits alles.

import type { IndicatorResult } from "../../api/types";
import { indicatorMeta } from "../../lib/indicators";
import { fieldTerms, rdfExcerpt } from "../../lib/rdf";

/** Ab so vielen Ist-Zeilen bekommt der Block eine eigene Bildlaufleiste,
 *  damit ein Datensatz mit 30 SHACL-Verstößen die Seite nicht sprengt. */
const SCROLL_AFTER_FACTS = 8;

export function IndicatorFinding({
  indicator,
  rdfSource,
}: {
  indicator: IndicatorResult;
  /** RDF-Quelltext des Datensatzes, falls geladen. */
  rdfSource?: string;
}) {
  const finding = indicator.finding;
  if (!finding) return null;

  const meta = indicatorMeta(indicator.indicator_id, indicator.name_de);
  const excerpt =
    meta.detail === "location" && rdfSource
      ? rdfExcerpt(rdfSource, fieldTerms(meta.field))
      : [];

  return (
    <div className="finding">
      <div className={`finding-grid ${finding.current.length === 0 ? "single" : ""}`}>
        {finding.current.length > 0 && (
          <section className="finding-block">
            <h4 className="finding-h">So steht es im Metadatensatz</h4>
            <dl
              className={`finding-facts ${
                finding.current.length > SCROLL_AFTER_FACTS ? "scroll" : ""
              }`}
            >
              {finding.current.map((fact, idx) => (
                <div key={idx} className={`finding-fact ${fact.tone ?? "neutral"}`}>
                  <dt>{fact.label}</dt>
                  <dd>
                    {fact.value}
                    {fact.where && (
                      <span className="finding-where" title={fact.where}>
                        {fact.where}
                      </span>
                    )}
                  </dd>
                </div>
              ))}
            </dl>
          </section>
        )}

        <section className="finding-block">
          <h4 className="finding-h">Hinweise</h4>
          <p className="finding-target">{finding.target ?? meta.fix}</p>
          {meta.vocab && (
            <p className="finding-vocab">
              Zugelassene Werte:{" "}
              <a href={meta.vocab.url} target="_blank" rel="noreferrer">
                {meta.vocab.label}
              </a>
            </p>
          )}
        </section>
      </div>

      {finding.notes.length > 0 && (
        <section className="finding-block">
          <h4 className="finding-h">Im Einzelnen</h4>
          <ul className="findings">
            {finding.notes.map((note, idx) => (
              <li key={idx}>{note}</li>
            ))}
          </ul>
        </section>
      )}

      {meta.detail === "template" && meta.template && (
        <section className="finding-block">
          <h4 className="finding-h">So sollte es aussehen</h4>
          <pre className="finding-template">
            <code>{meta.template}</code>
          </pre>
        </section>
      )}

      {excerpt.length > 0 && (
        <section className="finding-block finding-block-source">
          <h4 className="finding-h">Betroffene Stelle in der Metadatendatei</h4>
          <div className="rdf-excerpt">
            {excerpt.map((line) => (
              <div key={line.no} className="rdf-line">
                <span className="rdf-line-no">{line.no}</span>
                <code>{line.text}</code>
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
