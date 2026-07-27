import {
  PolarAngleAxis,
  PolarGrid,
  PolarRadiusAxis,
  Radar,
  RadarChart,
  ResponsiveContainer,
} from "recharts";
import type { Summary } from "../../api/types";
import { CHART_COLORS } from "../../lib/theme";
import { dimensionLabel } from "../../lib/indicators";

/**
 * Skalenbeschriftung der Radiusachse.
 *
 * Recharts dreht die Beschriftung der Radiusachse in deren Winkel — bei der
 * Vorgabe stehen die Zahlen dadurch quer. Eine eigene Beschriftung umgeht die
 * Rotation und setzt die Werte aufrecht an die senkrechte Achse.
 */
function RadiusTick({ x, y, payload }: { x?: number; y?: number; payload?: { value: number } }) {
  if (x == null || y == null || payload == null) return null;
  return (
    <text
      x={x}
      y={y}
      dy={3}
      textAnchor="end"
      fill={CHART_COLORS.textSubtle}
      fontSize={10}
    >
      {payload.value}
    </text>
  );
}

export function DimensionRadar({ summary }: { summary: Summary }) {
  const colors = CHART_COLORS;
  const data = Object.entries(summary.dimension_scores).map(([dim, score]) => ({
    dimension: dimensionLabel(dim),
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
          {/* Senkrechte Achse nach oben, Beschriftung aufrecht (siehe RadiusTick). */}
          <PolarRadiusAxis
            domain={[0, 1]}
            angle={90}
            tickCount={3}
            axisLine={false}
            tick={<RadiusTick />}
          />
          {/* Neutrale Profilfläche in der UI-Primärfarbe: Das Netz zeigt eine
              Verteilung, kein Urteil — eine Warnfarbe würde jeden Datensatz
              schlecht aussehen lassen, auch einen gut bewerteten. */}
          <Radar dataKey="score" stroke={colors.primary} fill={colors.primary} fillOpacity={0.28} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
