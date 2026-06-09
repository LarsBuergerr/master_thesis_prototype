import type { DimensionResult } from "../../api/types";
import { fmt, statusLabel } from "../../lib/status";
import { IndicatorBarChart } from "./IndicatorBarChart";

export function DimensionPanel({ dim }: { dim: DimensionResult }) {
  return (
    <details>
      <summary>
        <span style={{ textTransform: "capitalize" }}>{dim.dimension}</span>{" "}
        <span className="muted">
          — Score {fmt(dim.score)} · {dim.pass_count}/{dim.indicator_count} pass
        </span>
      </summary>

      <div style={{ marginTop: 10 }}>
        <IndicatorBarChart dim={dim} />
      </div>

      <table style={{ marginTop: 10 }}>
        <thead>
          <tr>
            <th>Indikator</th>
            <th>Status</th>
            <th>Score</th>
            <th>Roh</th>
            <th>Gewicht</th>
            <th>Meldung</th>
          </tr>
        </thead>
        <tbody>
          {dim.indicators.map((i) => (
            <tr key={i.indicator_id}>
              <td>{i.indicator_id}</td>
              <td>
                <span className={`chip ${i.status}`}>{statusLabel(i.status)}</span>
              </td>
              <td>{fmt(i.score)}</td>
              <td className="muted">
                {i.raw_status && i.raw_status !== i.status
                  ? `${i.raw_status} / ${fmt(i.raw_score)}`
                  : fmt(i.raw_score)}
              </td>
              <td>{fmt(i.effective_weight, 2)}</td>
              <td className="muted">{i.message_de || i.error || ""}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </details>
  );
}
