import {
  Bar,
  BarChart,
  Cell,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { DimensionResult } from "../../api/types";
import { CHART_COLORS } from "../../lib/theme";
import { statusColor } from "../../lib/status";
import { indicatorMeta } from "../../lib/indicators";

const STATUS_TEXT: Record<string, string> = {
  pass: "erfüllt",
  partial: "teilweise erfüllt",
  fail: "nicht erfüllt",
  not_applicable: "nicht anwendbar",
  error: "Fehler",
};

export function IndicatorBarChart({ dim }: { dim: DimensionResult }) {
  const colors = CHART_COLORS;
  // Achsenbeschriftung mit dem Klarnamen: die technische ID sagt einem
  // Datenbereitsteller nichts.
  const data = dim.indicators.map((i) => ({
    id: indicatorMeta(i.indicator_id, i.name_de).label,
    score: i.score ?? 0,
    status: i.status,
    weight: i.effective_weight ?? 1,
  }));

  // Include negative scores (penalised fails) in the domain so they're visible.
  const min = Math.min(0, ...data.map((d) => d.score));
  const height = Math.max(120, data.length * 30 + 20);

  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ left: 8, right: 40, top: 4, bottom: 4 }}
        >
          <XAxis
            type="number"
            domain={[min, 1]}
            tick={{ fill: colors.textSubtle, fontSize: 10 }}
          />
          <YAxis
            type="category"
            dataKey="id"
            width={190}
            tick={{ fill: colors.textSecondary, fontSize: 11 }}
          />
          <Tooltip
            contentStyle={{
              background: colors.panel,
              border: `1px solid ${colors.gridline}`,
              borderRadius: 5,
              fontSize: 12,
              color: colors.text,
            }}
            formatter={(value, _name, item) => [
              `${value} — ${STATUS_TEXT[item?.payload?.status] ?? item?.payload?.status}, Gewicht ${item?.payload?.weight}`,
              "Score",
            ]}
          />
          <Bar dataKey="score" radius={[0, 4, 4, 0]}>
            {data.map((d) => (
              <Cell key={d.id} fill={statusColor(d.status)} />
            ))}
            <LabelList
              dataKey="score"
              position="right"
              fill={colors.text}
              fontSize={11}
              formatter={(v: unknown) => Number(v).toFixed(2)}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
