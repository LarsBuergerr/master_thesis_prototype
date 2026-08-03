// Indikator-Tabelle einer Dimension.
//
// Adressat ist der Datenbereitsteller, nicht der Entwickler: die Zeile zeigt
// den Klarnamen des Indikators (nicht die technische ID), ein Info-Icon mit
// der Erklärung, was geprüft wird, und die Prüfmeldung im Klartext. Jede
// Spalte trägt ihre eigene Erläuterung, und nicht erfüllte Indikatoren lassen
// sich zu einem vollständigen Befund aufklappen (Ist-Zustand, Soll-Zustand,
// Änderungsvorschlag).

import { Fragment, useEffect, useRef, useState } from "react";
import type { DimensionResult, IndicatorResult } from "../../api/types";
import { fmt, statusIcon, statusLabel } from "../../lib/status";
import { columnHelp, dimensionLabel, dimensionWhat, indicatorMeta } from "../../lib/indicators";
import { InfoTip } from "../InfoTip";
import { IndicatorBarChart } from "./IndicatorBarChart";
import { IndicatorFinding } from "./IndicatorFinding";

const STATUS_LABELS: Record<string, string> = {
  pass: "erfüllt",
  partial: "teilweise",
  fail: "nicht erfüllt",
  not_applicable: "nicht anwendbar",
  error: "Fehler",
};

function statusText(status: string): string {
  return STATUS_LABELS[status] ?? statusLabel(status as never);
}

/**
 * Auftrag von außen, alles auf- oder zuzuklappen (Werkzeugleiste).
 *
 * `nonce` zählt die Betätigungen mit und ist der eigentliche Auslöser: Wer nach
 * „Alles ausklappen" einzelne Panels von Hand zuklappt und dann erneut auf
 * denselben Knopf drückt, erwartet, dass wieder alles offen ist. An `open`
 * allein wäre das nicht zu erkennen — der Wert hat sich ja nicht geändert.
 */
export interface ExpandSignal {
  open: boolean;
  nonce: number;
}

/** Folgt dem Signal, lässt zwischendurch aber jedes Auf- und Zuklappen von Hand zu. */
function useExpandSignal(initial: boolean, signal?: ExpandSignal) {
  const [open, setOpen] = useState(initial);
  // Der beim Einhängen anliegende Stand zählt nicht als Auftrag — sonst würde
  // das Signal beim ersten Rendern `initial` überschreiben.
  const applied = useRef(signal?.nonce);

  useEffect(() => {
    if (!signal || signal.nonce === applied.current) return;
    applied.current = signal.nonce;
    setOpen(signal.open);
  }, [signal]);

  return [open, setOpen] as const;
}

function IndicatorRow({
  indicator,
  rdfSource,
  expand,
}: {
  indicator: IndicatorResult;
  rdfSource?: string;
  expand?: ExpandSignal;
}) {
  const [open, setOpen] = useExpandSignal(false, expand);
  const meta = indicatorMeta(indicator.indicator_id, indicator.name_de);
  // Aufklappbar ist eine Zeile genau dann, wenn das Backend einen Befund
  // mitgeliefert hat — bei PASS gibt es nichts zu tun.
  const actionable = indicator.finding != null;

  return (
    <Fragment>
      <tr
        className={`ind-row${actionable ? " actionable" : ""}${open ? " open" : ""}`}
      >
        <th scope="row" className="ind-cell">
          <div className="ind-head">
            <InfoTip label={meta.label} text={meta.what} />
            <span className="ind-name">{meta.label}</span>
            <code className="ind-field" title={`Metadatenfeld · ${indicator.indicator_id}`}>
              {meta.field}
            </code>
          </div>
          <p className="ind-message">{indicator.message_de || indicator.error || "—"}</p>
          {actionable && (
            <button
              type="button"
              className="ind-toggle"
              aria-expanded={open}
              onClick={() => setOpen((v) => !v)}
            >
              {open ? "Hinweise ausblenden" : "Was ist zu tun?"}
            </button>
          )}
        </th>
        <td>
          <span className={`gd-tag gd-tag-status ${indicator.status}`}>
            <span aria-hidden="true">{statusIcon(indicator.status)}</span>
            {statusText(indicator.status)}
          </span>
        </td>
        <td className="tnum">{fmt(indicator.score)}</td>
        <td className="tnum">{fmt(indicator.effective_weight, 2)}</td>
      </tr>
      {actionable && open && (
        <tr className="ind-finding-row">
          <td colSpan={4}>
            <IndicatorFinding indicator={indicator} rdfSource={rdfSource} />
          </td>
        </tr>
      )}
    </Fragment>
  );
}

export function DimensionPanel({
  dim,
  rdfSource,
  defaultOpen = false,
  hidePassing = false,
  expand,
}: {
  dim: DimensionResult;
  /** RDF-Quelltext, um die betroffene Stelle zu zeigen (optional). */
  rdfSource?: string;
  defaultOpen?: boolean;
  /** Erfüllte Indikatoren ausblenden, um nur den Handlungsbedarf zu zeigen. */
  hidePassing?: boolean;
  /** Auf-/Zuklappen von außen — gilt für das Panel und seine Befunde. */
  expand?: ExpandSignal;
}) {
  const label = dimensionLabel(dim.dimension);
  const what = dimensionWhat(dim.dimension);
  const [open, setOpen] = useExpandSignal(defaultOpen, expand);
  const actionable = dim.indicators.filter((i) => i.status !== "pass").length;

  // Gefiltert wird nur die Tabelle. Das Balkendiagramm behält alle Indikatoren:
  // es ist die Übersicht der Dimension, und ohne die erfüllten Balken sähe eine
  // gut bewertete Dimension aus wie eine schlechte.
  const rows = hidePassing
    ? dim.indicators.filter((i) => i.status !== "pass")
    : dim.indicators;
  const hidden = dim.indicators.length - rows.length;

  // Die Aufgabe des Diagramms ist der *Vergleich* von Erfüllungsgraden. Wo alle
  // Indikatoren 0 oder 1 erreichen, zeigt es nichts, was nicht schon in der
  // Statusspalte steht; bei einem einzigen Zwischenwert steht die Zahl bereits
  // in der Score-Spalte. Erst ab zwei gestuften Ergebnissen gibt es etwas zu
  // vergleichen. Über die Stichprobe (n = 50) heißt das: bei Aussagekraft immer
  // sichtbar, bei Zugänglichkeit in 38 % der Fälle, bei Auffindbarkeit und
  // Nachnutzbarkeit praktisch nie.
  const graded =
    dim.indicators.filter((i) => {
      const score = i.score ?? 0;
      return score > 0 && score < 1;
    }).length >= 2;

  return (
    <details
      className="dim-panel"
      open={open}
      onToggle={(e) => setOpen(e.currentTarget.open)}
    >
      <summary>
        <span className="dim-name">{label}</span>{" "}
        <span className="muted">
          Score {fmt(dim.score)} · Gewicht {fmt(dim.dimension_weight, 1)} ·{" "}
          {dim.pass_count} von {dim.indicator_count} Indikatoren erfüllt
          {actionable > 0 && ` · ${actionable} mit Handlungsbedarf`}
        </span>
      </summary>

      {what && <p className="dim-what muted">{what}</p>}

      {graded && (
        <div style={{ marginTop: 10 }}>
          <IndicatorBarChart dim={dim} />
        </div>
      )}

      {rows.length === 0 ? (
        <p className="dim-all-passed muted" style={{ marginTop: 10 }}>
          Alle {dim.indicator_count} Indikatoren dieser Dimension sind erfüllt.
        </p>
      ) : (
        <div className="gd-table-wrapper">
          <table className="gd-table ind-table" style={{ marginTop: 10 }}>
            <caption>
              Indikatoren der Dimension {label}
              {hidden > 0 && ` — ${hidden} erfüllte ausgeblendet`}
            </caption>
            <thead className="gd-table-head">
              <tr>
                <th scope="col">Indikator und Prüfergebnis</th>
                <th scope="col">
                  Status <InfoTip label="Status" text={columnHelp("status")} />
                </th>
                <th scope="col">
                  Score <InfoTip label="Score" text={columnHelp("score")} />
                </th>
                <th scope="col">
                  Gewicht <InfoTip label="Gewicht" text={columnHelp("weight")} align="end" />
                </th>
              </tr>
            </thead>
            <tbody>
              {rows.map((i) => (
                <IndicatorRow
                  key={i.indicator_id}
                  indicator={i}
                  rdfSource={rdfSource}
                  expand={expand}
                />
              ))}
            </tbody>
          </table>
        </div>
      )}
    </details>
  );
}
