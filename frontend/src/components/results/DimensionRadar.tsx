import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";
import type { Summary } from "../../api/types";
import { useTheme } from "../../hooks/useTheme";

export function DimensionRadar({ summary }: { summary: Summary }) {
  const { colors } = useTheme();
  const data = Object.entries(summary.dimension_scores).map(([dim, score]) => ({
    dimension: dim,
    score: Number(score.toFixed(3)),
  }));

  if (data.length === 0) return null;

  return (
    <div style={{ width: "100%", height: 260 }}>
      <ResponsiveContainer>
        <RadarChart data={data} outerRadius="70%">
          <PolarGrid stroke={colors.gridline} />
          <PolarAngleAxis
            dataKey="dimension"
            tick={{ fill: colors.textSecondary, fontSize: 12 }}
          />
          <PolarRadiusAxis domain={[0, 1]} tick={{ fill: colors.textSubtle, fontSize: 10 }} />
          <Radar dataKey="score" stroke={colors.accent} fill={colors.accent} fillOpacity={0.4} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
