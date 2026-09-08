// Indikator-Tabelle einer Dimension.
//
// Adressat ist der Datenbereitsteller, nicht der Entwickler: die Zeile zeigt
// den Klarnamen des Indikators (nicht die technische ID), ein Info-Icon mit
// der Erklärung, was geprüft wird, und die Prüfmeldung im Klartext. Jede
// Spalte trägt ihre eigene Erläuterung, und nicht erfüllte Indikatoren lassen
// sich zu einem vollständigen Befund aufklappen (Ist-Zustand, Soll-Zustand,
// Änderungsvorschlag).
//
// Score und Gewicht stehen in zwei eigenen Spalten. Zusammengelegt („0,50 /
// 2,00") lasen sie sich wie ein Bruch — als sei 0,50 ein Anteil von 2,00.

import { Fragment, useEffect, useRef, useState } from "react";
import type { DimensionResult, IndicatorResult } from "../../api/types";
import { fmt, scorePoints, statusIcon, statusLabel } from "../../lib/status";
import { columnHelp, dimensionLabel, dimensionWhat, indicatorMeta } from "../../lib/indicators";
import { InfoTip } from "../InfoTip";
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
        className={`ind-row ${indicator.status}${actionable ? " actionable" : ""}${open ? " open" : ""}`}
      >
        <th scope="row" className="ind-cell">
          <div className="ind-head">
            {/* Das Icon steht hinter dem Namen: Erst die Sache, dann das
                Angebot, sie erklärt zu bekommen. Davor gelesen unterbrach es
                den Namen, noch bevor er begonnen hatte. */}
            <span className="ind-name">{meta.label}</span>
            <InfoTip label={meta.label} text={meta.what} />
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
              {/* Richtungspfeil: nach unten heißt „hier geht es weiter", nach
                  oben „das schließt wieder". Ohne ihn war dem Text nicht
                  anzusehen, dass er etwas aufklappt. */}
              <span aria-hidden="true" className="ind-toggle-chevron">
                {open ? "▴" : "▾"}
              </span>
            </button>
          )}
        </th>
        {/* Der Status trägt keine eigene Spalte, sondern färbt die Score-Zelle.
            Farbe allein genügt dafür nicht (WCAG SC 1.4.1), deshalb bleiben das
            Icon-Glyph und ein Textlabel für Screenreader erhalten. */}
        <td
          className={`ind-metrics ind-metrics-score ${indicator.status}`}
          title={statusText(indicator.status)}
        >
          <span aria-hidden="true" className="ind-metrics-icon">
            {statusIcon(indicator.status)}
          </span>
          <span className="visually-hidden">{statusText(indicator.status)}</span>
          <span className="tnum ind-metrics-value">{fmt(indicator.score)}</span>
        </td>
        <td className={`ind-metrics ind-metrics-weight ${indicator.status}`}>
          <span className="tnum ind-metrics-value">{fmt(indicator.effective_weight, 2)}</span>
        </td>
      </tr>
      {actionable && open && (
        <tr className={`ind-finding-row ${indicator.status}`}>
          <td colSpan={3}>
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

  const rows = hidePassing
    ? dim.indicators.filter((i) => i.status !== "pass")
    : dim.indicators;
  const hidden = dim.indicators.length - rows.length;

  return (
    <details
      className="dim-panel"
      open={open}
      onToggle={(e) => setOpen(e.currentTarget.open)}
    >
      {/* Die Kennzahlen der Dimension als Chips: In der früheren Fließzeile
          („Score 0.80 · Gewicht 1.0 · …") verschwammen Bezeichnung und Wert zu
          einer Kette von Wörtern. Jeder Chip trennt beides — Bezeichnung
          normal, Wert fett — und ist als eigene Angabe erkennbar. */}
      <summary>
        <span className="dim-name">{label}</span>{" "}
        <span className="dim-chips">
          <span className="dim-chip dim-chip-score">
            Score <b className="tnum">{scorePoints(dim.score)} / 100</b>
          </span>
          <span className="dim-chip dim-chip-weight">
            Gewicht <b className="tnum">{fmt(dim.dimension_weight, 1)}</b>
          </span>
          <span className="dim-chip dim-chip-count">
            <b className="tnum">
              {dim.pass_count} / {dim.indicator_count}
            </b>{" "}
            Indikatoren erfüllt
          </span>
          {actionable > 0 && (
            <span className="dim-chip actionable">
              <b className="tnum">{actionable}</b> mit Handlungsbedarf
            </span>
          )}
        </span>
      </summary>

      {what && <p className="dim-what muted">{what}</p>}

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
                <th scope="col" className="ind-col-metric">
                  Score{" "}
                  <InfoTip
                    label="Score"
                    text={`${columnHelp("score")} ${columnHelp("status")}`}
                    align="end"
                  />
                </th>
                <th scope="col" className="ind-col-metric">
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
