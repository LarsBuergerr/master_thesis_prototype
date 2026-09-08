// Dimensionsprofil als Netz.
//
// Die Achsenbeschriftung trägt den Teilscore mit: Das Netz zeigte bisher nur
// die *Form* des Profils, die Zahlen dazu standen erst in den Panels darunter.
// Wer wissen wollte, wie weit „Zugänglichkeit" nun tatsächlich kommt, musste
// die Fläche gegen die Achsenteilung schätzen. Die Tabellenwerte bleiben
// trotzdem stehen — das Netz vergleicht, die Tabelle belegt.
//
// Skala in Punkten von 100, wie überall sonst in der Oberfläche.

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
import { scorePoints } from "../../lib/status";
import { dimensionLabel } from "../../lib/indicators";

interface AngleTickProps {
  x?: number;
  y?: number;
  textAnchor?: string;
  payload?: { value: string };
  /** Teilscore je Dimensionsname, in Punkten von 100. */
  scores: Record<string, number>;
}

/** Dimensionsname mit dem Teilscore darunter. */
function AngleTick({ x, y, textAnchor, payload, scores }: AngleTickProps) {
  if (x == null || y == null || payload == null) return null;
  const name = payload.value;
  const anchor = (textAnchor ?? "middle") as "start" | "middle" | "end";
  return (
    <g>
      <text x={x} y={y} dy={4} textAnchor={anchor} fill={CHART_COLORS.textSecondary} fontSize={12}>
        {name}
      </text>
      <text
        x={x}
        y={y + 15}
        dy={4}
        textAnchor={anchor}
        fill={CHART_COLORS.text}
        fontSize={12}
        fontWeight={700}
      >
        {scores[name]} / 100
      </text>
    </g>
  );
}

export function DimensionRadar({ summary }: { summary: Summary }) {
  const colors = CHART_COLORS;
  const data = Object.entries(summary.dimension_scores).map(([dim, score]) => ({
    dimension: dimensionLabel(dim),
    score: scorePoints(score),
  }));

  if (data.length === 0) return null;

  const scores = Object.fromEntries(data.map((d) => [d.dimension, d.score]));

  return (
    <div style={{ width: "100%", height: 280 }}>
      <ResponsiveContainer>
        {/* Etwas kleineres Polygon als zuvor: Die Beschriftung trägt jetzt
            zwei Zeilen und braucht den Rand. */}
        <RadarChart data={data} outerRadius="66%">
          <PolarGrid stroke={colors.gridline} />
          <PolarAngleAxis
            dataKey="dimension"
            tick={(props) => <AngleTick {...props} scores={scores} />}
          />
          {/* Die Radiusachse bemisst nur noch das Netz. Ihre Skalenzahlen sind
              entfallen: Seit jede Achse ihren Wert selbst nennt, doppelten sie
              die Auskunft — und die oberste stieß mit der Beschriftung der
              senkrechten Achse zusammen. */}
          <PolarRadiusAxis domain={[0, 100]} angle={90} axisLine={false} tick={false} />
          {/* Neutrale Profilfläche in der UI-Primärfarbe: Das Netz zeigt eine
              Verteilung, kein Urteil — eine Warnfarbe würde jeden Datensatz
              schlecht aussehen lassen, auch einen gut bewerteten. */}
          <Radar dataKey="score" stroke={colors.primary} fill={colors.primary} fillOpacity={0.28} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
