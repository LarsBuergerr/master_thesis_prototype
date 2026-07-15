import { useState } from "react";
import type { ChangePatch, FieldSuggestion, Recommendation, Remediation } from "../../api/types";
import { shortenUri } from "../../lib/status";

function ChangeLine({ sign, predicate, value, title }: {
  sign: "+" | "-";
  predicate: string;
  value: string;
  title?: string;
}) {
  const color = sign === "+" ? "var(--pass)" : "var(--fail)";
  return (
    <div className="diff-line" style={{ color }} title={title}>
      <span className="diff-sign">{sign}</span>
      <span className="muted">{shortenUri(predicate)}</span>{" "}
      <span>{value}</span>
    </div>
  );
}

function NeedsInputRow({ suggestion }: { suggestion: FieldSuggestion }) {
  const [chosen, setChosen] = useState("");
  return (
    <div className="diff-line diff-pending">
      <span className="diff-sign muted">?</span>
      <span className="muted">{shortenUri(suggestion.predicate)}</span>
      <select
        value={chosen}
        onChange={(e) => setChosen(e.target.value)}
        style={{ width: "auto", flex: 1 }}
      >
        <option value="">
          Wert wählen… ({suggestion.candidates.length} Kandidaten)
        </option>
        {suggestion.candidates.map((c) => (
          <option key={c} value={c} title={c}>
            {shortenUri(c)}
          </option>
        ))}
      </select>
      {chosen && (
        <ChangeLine
          sign="+"
          predicate={suggestion.predicate}
          value={shortenUri(chosen)}
          title={chosen}
        />
      )}
    </div>
  );
}

function ChangePatchView({ patch }: { patch: ChangePatch }) {
  return (
    <div>
      <div className="row" style={{ gap: 6 }}>
        <span className="chip patch">Patch</span>
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
      <div className="row" style={{ gap: 6 }}>
        <span className="chip recommendation">Empfehlung</span>
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
