import {
  RadialBar,
  RadialBarChart,
  PolarAngleAxis,
  ResponsiveContainer,
} from "recharts";
import type { Summary } from "../../api/types";
import { fmt, gradeColor } from "../../lib/status";

export function OverallScoreCard({ summary }: { summary: Summary }) {
  // Clamp to [0,1] only for the gauge geometry; the printed value stays exact
  // so negative (penalised) scores remain visible as text.
  const gaugeValue = Math.max(0, Math.min(1, summary.overall_score));
  const color = gradeColor(summary.quality_grade);
  const data = [{ name: "score", value: gaugeValue * 100, fill: color }];

  return (
    <div className="gd-row" style={{ gap: 16, alignItems: "center" }}>
      <div style={{ width: 130, height: 130, position: "relative" }}>
        <ResponsiveContainer width="100%" height="100%">
          <RadialBarChart
            innerRadius="70%"
            outerRadius="100%"
            data={data}
            startAngle={90}
            endAngle={-270}
          >
            <PolarAngleAxis type="number" domain={[0, 100]} tick={false} />
            <RadialBar background dataKey="value" cornerRadius={8} />
          </RadialBarChart>
        </ResponsiveContainer>
        <div
          style={{
            position: "absolute",
            inset: 0,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <span className={`grade ${summary.quality_grade}`}>
            {summary.quality_grade}
          </span>
        </div>
      </div>
      <div>
        <div style={{ fontSize: 28, fontWeight: 700 }}>
          {fmt(summary.overall_score)}
        </div>
        <div className="muted">Gesamtscore</div>
        <div className="muted" style={{ marginTop: 6 }}>
          Pass-Rate: {fmt(summary.overall_pass_rate * 100, 0)}% · {summary.total_pass}/
          {summary.total_indicators} bestanden
        </div>
      </div>
    </div>
  );
}
