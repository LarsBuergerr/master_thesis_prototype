import type { ChangePatch, FieldSuggestion, Recommendation, Remediation } from "../../api/types";
import { shortenUri } from "../../lib/status";

function ChangeLine({ sign, predicate, value, title }: {
  sign: "+" | "-";
  predicate: string;
  value: string;
  title?: string;
}) {
  return (
    <div className={`diff-line ${sign === "+" ? "diff-add" : "diff-del"}`} title={title}>
      <span className="diff-sign">{sign}</span>
      <span className="muted">{shortenUri(predicate)}</span>{" "}
      <span>{value}</span>
    </div>
  );
}

/**
 * Fehlender Wert an einer bekannten Stelle. Gezeigt wird das betroffene Feld,
 * die erwartete Form und ein Beispiel für die Schreibweise — nicht das
 * Vokabular selbst: das hat je nach Feld bis zu ein paar tausend Einträge, und
 * eine Auswahlliste dieser Größe hilft niemandem beim Eintragen. Die
 * vollständige Liste steht verlinkt an der Quelle.
 */
function NeedsInputRow({ suggestion }: { suggestion: FieldSuggestion }) {
  return (
    <div className="diff-pending">
      <div className="diff-line">
        <span className="diff-sign muted">?</span>
        <span className="muted">{shortenUri(suggestion.predicate)}</span>
        <span>{suggestion.expected_de}</span>
      </div>
      {suggestion.example && (
        <p className="diff-hint muted">
          Schreibweise: <code title={suggestion.example}>{suggestion.example}</code>
        </p>
      )}
      {suggestion.vocabulary_url && (
        <p className="diff-hint muted">
          Zulässige Werte:{" "}
          <a href={suggestion.vocabulary_url} target="_blank" rel="noreferrer">
            {suggestion.vocabulary_label ?? shortenUri(suggestion.vocabulary_url)}
          </a>
        </p>
      )}
    </div>
  );
}

function ChangePatchView({ patch }: { patch: ChangePatch }) {
  return (
    <div>
      <div className="gd-row" style={{ gap: 6 }}>
        <span className="gd-tag patch">Patch</span>
        <span className="muted">{patch.summary_de}</span>
      </div>
      <div className="diff-box">
        {patch.ready.map((c, idx) => (
          <ChangeLine
            key={idx}
            sign={c.op === "add" ? "+" : "-"}
            predicate={c.predicate}
            value={c.object.type === "literal" ? `"${c.object.value}"` : shortenUri(c.object.value)}
            title={`${c.subject}\n${c.reason}`}
          />
        ))}
        {patch.needs_input.map((s, idx) => (
          <NeedsInputRow key={idx} suggestion={s} />
        ))}
      </div>
    </div>
  );
}

function RecommendationView({ rec }: { rec: Recommendation }) {
  return (
    <div>
      <div className="gd-row" style={{ gap: 6 }}>
        <span className="gd-tag recommendation">Empfehlung</span>
        <span>{rec.message_de}</span>
      </div>
      {rec.findings.length > 0 && (
        <ul className="findings">
          {rec.findings.map((f, idx) => (
            <li key={idx}>{f}</li>
          ))}
        </ul>
      )}
      {rec.see_also.length > 0 && (
        <div className="muted" style={{ marginTop: 4 }}>
          Siehe auch:{" "}
          {rec.see_also.map((uri, idx) => (
            <span key={uri}>
              {idx > 0 && ", "}
              <a href={uri} target="_blank" rel="noreferrer" title={uri}>
                {shortenUri(uri)}
              </a>
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

export function RemediationView({ remediation }: { remediation: Remediation }) {
  if (remediation.kind === "change_patch") {
    return <ChangePatchView patch={remediation} />;
  }
  return <RecommendationView rec={remediation} />;
}
