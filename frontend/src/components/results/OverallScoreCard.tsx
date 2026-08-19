// Gesamturteil als Ring mit Notenbuchstaben.
//
// Der Ring steht für sich, die Zahlen darunter — nebeneinander würde die
// Textspalte den Ring aus der Mitte drücken, sobald er neben dem Dimensionsnetz
// steht. Die Note ist nie der einzige Träger: Score und Pass-Rate stehen als
// Text daneben (WCAG 1.4.1).
//
// Der Score wird in Punkten von 100 genannt — dieselbe Schreibweise wie in der
// Trefferliste und im Dashboard. Der Anteilswert („0.80") stand nur hier und
// zwang den Leser, zwei Skalen für dieselbe Größe im Kopf zu behalten.

import {
  RadialBar,
  RadialBarChart,
  PolarAngleAxis,
  ResponsiveContainer,
} from "recharts";
import type { Summary } from "../../api/types";
import { fmt, gradeColor, scorePoints } from "../../lib/status";

export function OverallScoreCard({ summary }: { summary: Summary }) {
  // Clamp to [0,1] only for the gauge geometry; the printed value stays exact
  // so negative (penalised) scores remain visible as text.
  const gaugeValue = Math.max(0, Math.min(1, summary.overall_score));
  const color = gradeColor(summary.quality_grade);
  const data = [{ name: "score", value: gaugeValue * 100, fill: color }];

  return (
    <div className="score-card">
      <div className="score-card-gauge">
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
        <div className="score-card-grade">
          <span className={`grade ${summary.quality_grade}`}>{summary.quality_grade}</span>
        </div>
      </div>

      <div className="score-card-figures">
        <div className="score-card-value tnum">
          {scorePoints(summary.overall_score)}
          <span className="score-card-max"> / 100</span>
        </div>
        <div className="muted">Gesamtscore</div>
        <div className="muted score-card-note">
          Pass-Rate: {fmt(summary.overall_pass_rate * 100, 0)}% · {summary.total_pass}/
          {summary.total_indicators} bestanden
        </div>
      </div>
    </div>
  );
}
