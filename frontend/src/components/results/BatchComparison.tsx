import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { FileResult } from "../../api/types";
import { gradeColor } from "../../lib/status";

/**
 * Grouped overall-score-per-file chart — the direct view of the thesis goal
 * (do good datasets score higher than bad ones?).
 */
export function BatchComparison({ results }: { results: FileResult[] }) {
  const data = results
    .filter((r) => r.result)
    .map((r) => ({
      file: r.filename,
      overall: Number(r.result!.summary.overall_score.toFixed(3)),
      grade: r.result!.summary.quality_grade,
    }));

  if (data.length < 2) return null;

  const min = Math.min(0, ...data.map((d) => d.overall));

  return (
    <div className="panel">
      <h2>Vergleich: Gesamtscore pro Datei</h2>
      <div style={{ width: "100%", height: Math.max(220, data.length * 36 + 40) }}>
        <ResponsiveContainer>
          <BarChart
            data={data}
            layout="vertical"
            margin={{ left: 8, right: 40, top: 4, bottom: 4 }}
          >
            <CartesianGrid strokeDasharray="3 3" stroke="#2c3142" />
            <XAxis
              type="number"
              domain={[min, 1]}
              tick={{ fill: "#6b7280", fontSize: 11 }}
            />
            <YAxis
              type="category"
              dataKey="file"
              width={180}
              tick={{ fill: "#98a0b3", fontSize: 11 }}
            />
            <Tooltip
              contentStyle={{
                background: "#1a1d27",
                border: "1px solid #2c3142",
                borderRadius: 6,
                fontSize: 12,
              }}
              formatter={(v, _n, item) => [`${v} (${item?.payload?.grade})`, "overall"]}
            />
            <Legend />
            <Bar dataKey="overall" name="Gesamtscore" radius={[0, 4, 4, 0]}>
              {data.map((d) => (
                <Cell key={d.file} fill={gradeColor(d.grade)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
