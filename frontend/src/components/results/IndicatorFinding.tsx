// Aufgeklappter Befund zu einem Indikator: Ist-Zustand mit Fundstelle,
// Soll-Zustand, Einzelhinweise, der Änderungsvorschlag des Backends (Diff) und
// — sofern der RDF-Quelltext vorliegt — die betroffenen Zeilen der Datei.

import type { IndicatorResult } from "../../api/types";
import { buildFinding } from "../../lib/findings";
import { indicatorMeta } from "../../lib/indicators";
import { fieldTerms, rdfExcerpt } from "../../lib/rdf";
import { hintsFromDetails } from "../../lib/remediation";
import { RemediationView } from "./RemediationView";

export function IndicatorFinding({
  indicator,
  rdfSource,
}: {
  indicator: IndicatorResult;
  /** RDF-Quelltext des Datensatzes, falls geladen. */
  rdfSource?: string;
}) {
  const finding = buildFinding(indicator);
  if (!finding) return null;

  const meta = indicatorMeta(indicator.indicator_id, indicator.name_de);
  const excerpt = rdfSource ? rdfExcerpt(rdfSource, fieldTerms(meta.field)) : [];

  // Eine Empfehlung besteht aus Meldung und Einzelbefunden — beides steht
  // bereits oben in der Zeile bzw. unter „Im Einzelnen". Nur ein Patch bringt
  // hier zusätzliche Information (die konkreten Änderungen).
  const remediation = indicator.remediation;
  const patch = remediation?.kind === "change_patch" ? remediation : null;
  const seeAlso = remediation?.kind === "recommendation" ? remediation.see_also : [];

  // „Nächster Schritt" nur, wenn er nicht wortgleich der Soll-Beschreibung ist.
  const target = finding.target ?? meta.fix;
  const showFix = meta.fix !== target;

  return (
    <div className="finding">
      <div className={`finding-grid ${finding.current.length === 0 ? "single" : ""}`}>
        {finding.current.length > 0 && (
          <section className="finding-block">
            <h4 className="finding-h">So steht es im Metadatensatz</h4>
            <dl className="finding-facts">
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
          <h4 className="finding-h">So sollte es aussehen</h4>
          <p className="finding-target">{target}</p>
          {showFix && (
            <p className="finding-fix">
              <strong>Nächster Schritt:</strong> {meta.fix}
            </p>
          )}
          {meta.vocab && (
            <p className="finding-vocab">
              Zugelassene Werte:{" "}
              <a href={meta.vocab.url} target="_blank" rel="noreferrer">
                {meta.vocab.label}
              </a>
            </p>
          )}
          {seeAlso.length > 0 && (
            <p className="finding-vocab">
              Siehe auch:{" "}
              {seeAlso.map((uri, idx) => (
                <span key={uri}>
                  {idx > 0 && ", "}
                  <a href={uri} target="_blank" rel="noreferrer">
                    {uri}
                  </a>
                </span>
              ))}
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

      {patch && (
        <section className="finding-block">
          <h4 className="finding-h">Änderungsvorschlag</h4>
          <RemediationView
            remediation={patch}
            hints={hintsFromDetails(indicator.details ?? {})}
          />
        </section>
      )}

      {excerpt.length > 0 && (
        <section className="finding-block">
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
