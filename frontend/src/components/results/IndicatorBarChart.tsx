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
import { statusColor } from "../../lib/status";

export function IndicatorBarChart({ dim }: { dim: DimensionResult }) {
  const data = dim.indicators.map((i) => ({
    id: i.indicator_id,
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
            tick={{ fill: "#6b7280", fontSize: 10 }}
          />
          <YAxis
            type="category"
            dataKey="id"
            width={190}
            tick={{ fill: "#98a0b3", fontSize: 11 }}
          />
          <Tooltip
            contentStyle={{
              background: "#1a1d27",
              border: "1px solid #2c3142",
              borderRadius: 6,
              fontSize: 12,
            }}
            formatter={(value, _name, item) => [
              `${value} (${item?.payload?.status}, w=${item?.payload?.weight})`,
              "score",
            ]}
          />
          <Bar dataKey="score" radius={[0, 4, 4, 0]}>
            {data.map((d) => (
              <Cell key={d.id} fill={statusColor(d.status)} />
            ))}
            <LabelList
              dataKey="score"
              position="right"
              fill="#e6e8ee"
              fontSize={11}
              formatter={(v: unknown) => Number(v).toFixed(2)}
            />
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
