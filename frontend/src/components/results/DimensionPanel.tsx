// Indikator-Tabelle einer Dimension.
//
// Adressat ist der Datenbereitsteller, nicht der Entwickler: die Zeile zeigt
// den Klarnamen des Indikators (nicht die technische ID), ein Info-Icon mit
// der Erklärung, was geprüft wird, und die Prüfmeldung im Klartext. Jede
// Spalte trägt ihre eigene Erläuterung, und nicht erfüllte Indikatoren lassen
// sich zu einem vollständigen Befund aufklappen (Ist-Zustand, Soll-Zustand,
// Änderungsvorschlag).

import { Fragment, useState } from "react";
import type { DimensionResult, IndicatorResult } from "../../api/types";
import { fmt, statusIcon, statusLabel } from "../../lib/status";
import { COLUMN_HELP, DIMENSION_META, indicatorMeta } from "../../lib/indicators";
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

function IndicatorRow({
  indicator,
  rdfSource,
}: {
  indicator: IndicatorResult;
  rdfSource?: string;
}) {
  const [open, setOpen] = useState(false);
  const meta = indicatorMeta(indicator.indicator_id, indicator.name_de);
  const actionable =
    indicator.status === "fail" ||
    indicator.status === "partial" ||
    indicator.status === "error";

  return (
    <Fragment>
      <tr className={actionable ? "ind-row actionable" : "ind-row"}>
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
          <span className={`gd-tag ${indicator.status}`}>
            <span aria-hidden="true">{statusIcon(indicator.status)}</span>
            {statusText(indicator.status)}
          </span>
        </td>
        <td className="tnum">{fmt(indicator.score)}</td>
        <td className="tnum muted">
          {indicator.raw_status && indicator.raw_status !== indicator.status
            ? `${statusText(indicator.raw_status)} / ${fmt(indicator.raw_score)}`
            : fmt(indicator.raw_score)}
        </td>
        <td className="tnum">{fmt(indicator.effective_weight, 2)}</td>
      </tr>
      {actionable && open && (
        <tr className="ind-finding-row">
          <td colSpan={5}>
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
}: {
  dim: DimensionResult;
  /** RDF-Quelltext, um die betroffene Stelle zu zeigen (optional). */
  rdfSource?: string;
  defaultOpen?: boolean;
}) {
  const meta = DIMENSION_META[dim.dimension];
  const label = meta?.label ?? dim.dimension;
  const open = dim.indicators.filter((i) => i.status !== "pass").length;

  return (
    <details className="dim-panel" open={defaultOpen}>
      <summary>
        <span className="dim-name">{label}</span>{" "}
        <span className="muted">
          Score {fmt(dim.score)} · {dim.pass_count} von {dim.indicator_count} Indikatoren erfüllt
          {open > 0 && ` · ${open} mit Handlungsbedarf`}
        </span>
      </summary>

      {meta && <p className="dim-what muted">{meta.what}</p>}

      <div style={{ marginTop: 10 }}>
        <IndicatorBarChart dim={dim} />
      </div>

      <div className="gd-table-wrapper">
        <table className="gd-table ind-table" style={{ marginTop: 10 }}>
          <caption>Indikatoren der Dimension {label}</caption>
          <thead className="gd-table-head">
            <tr>
              <th scope="col">Indikator und Prüfergebnis</th>
              <th scope="col">
                Status <InfoTip label="Status" text={COLUMN_HELP.status} />
              </th>
              <th scope="col">
                Score <InfoTip label="Score" text={COLUMN_HELP.score} />
              </th>
              <th scope="col">
                Roh <InfoTip label="Rohwert" text={COLUMN_HELP.raw} />
              </th>
              <th scope="col">
                Gewicht <InfoTip label="Gewicht" text={COLUMN_HELP.weight} align="end" />
              </th>
            </tr>
          </thead>
          <tbody>
            {dim.indicators.map((i) => (
              <IndicatorRow key={i.indicator_id} indicator={i} rdfSource={rdfSource} />
            ))}
          </tbody>
        </table>
      </div>
    </details>
  );
}
