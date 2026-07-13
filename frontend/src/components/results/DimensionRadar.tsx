import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";
import type { Summary } from "../../api/types";

export function DimensionRadar({ summary }: { summary: Summary }) {
  const data = Object.entries(summary.dimension_scores).map(([dim, score]) => ({
    dimension: dim,
    score: Number(score.toFixed(3)),
  }));

  if (data.length === 0) return null;

  return (
    <div style={{ width: "100%", height: 260 }}>
      <ResponsiveContainer>
        <RadarChart data={data} outerRadius="70%">
          <PolarGrid stroke="#2c3142" />
          <PolarAngleAxis dataKey="dimension" tick={{ fill: "#98a0b3", fontSize: 12 }} />
          <PolarRadiusAxis domain={[0, 1]} tick={{ fill: "#6b7280", fontSize: 10 }} />
          <Radar
            dataKey="score"
            stroke="#5b8def"
            fill="#5b8def"
            fillOpacity={0.4}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
