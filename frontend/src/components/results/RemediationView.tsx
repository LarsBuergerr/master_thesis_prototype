import { useState } from "react";
import type { ChangePatch, FieldSuggestion, Recommendation, Remediation } from "../../api/types";
import { shortenUri } from "../../lib/status";

/** Wie viele Vokabular-Einträge die Auswahlliste anbietet. */
const MAX_OPTIONS = 40;

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
 * Fehlender Wert aus einem kontrollierten Vokabular. Konnte das Backend die
 * Kandidaten nach Nähe zum vorhandenen Wert sortieren (`ranked`, siehe
 * scoring/remediation/vocab_fields.py), steht der wahrscheinlich gemeinte
 * vorbelegt als Vorschlagszeile im Diff; sonst bleibt die Auswahl leer, statt
 * den alphabetisch ersten Eintrag wie eine Empfehlung aussehen zu lassen.
 */
function NeedsInputRow({ suggestion }: { suggestion: FieldSuggestion }) {
  const [chosen, setChosen] = useState(() =>
    suggestion.ranked ? (suggestion.candidates[0] ?? "") : "",
  );
  const total = suggestion.candidate_total ?? suggestion.candidates.length;

  return (
    <div className="diff-pending">
      <div className="diff-line">
        <span className="diff-sign muted">?</span>
        <span className="muted">{shortenUri(suggestion.predicate)}</span>
        <select
          value={chosen}
          onChange={(e) => setChosen(e.target.value)}
          style={{ width: "auto", flex: 1 }}
          aria-label={`Wert für ${shortenUri(suggestion.predicate)} wählen`}
        >
          <option value="">Wert wählen… ({total} zugelassene Werte)</option>
          {suggestion.candidates.slice(0, MAX_OPTIONS).map((c) => (
            <option key={c} value={c} title={c}>
              {shortenUri(c)}
            </option>
          ))}
        </select>
      </div>
      {chosen && (
        // Volle URI statt Kurzform: der Vorschlag soll zeigen, was wörtlich in
        // die Datei gehört — die Kurzform „SHP“ wäre vom bisherigen Freitext
        // nicht zu unterscheiden.
        <ChangeLine sign="+" predicate={suggestion.predicate} value={chosen} title={chosen} />
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
