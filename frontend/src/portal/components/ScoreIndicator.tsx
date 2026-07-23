// Kompakter Qualitäts-Indikator für die Trefferliste: ein Ring mit Prozentwert
// und Notenfarbe (GovData-Statusfarben via gradeColor). Bewusst leichtgewichtig
// als Inline-SVG gehalten (kein Recharts), da bis zu 50 Instanzen gleichzeitig
// in der Liste stehen. Die Farbe ist nie der einzige Träger: Note als Text und
// ein Textlabel stehen daneben (WCAG 1.4.1).

import { gradeColor } from "../../lib/status";
import { gradeLabel, scoreToGrade, scorePct } from "../lib/quality";

interface Props {
  score: number;
  size?: number;
  /** Klartext-Label (z. B. „Gut") unter dem Ring anzeigen. */
  showLabel?: boolean;
}

export function ScoreIndicator({ score, size = 56, showLabel = true }: Props) {
  const grade = scoreToGrade(score);
  const color = gradeColor(grade);
  const pct = scorePct(score);
  const stroke = size < 50 ? 5 : 6;
  const r = (size - stroke) / 2;
  const c = 2 * Math.PI * r;
  const clamped = Math.max(0, Math.min(1, score));
  const offset = c * (1 - clamped);

  return (
    <div
      className="score-indicator"
      title={`Metadaten-Qualität: ${pct} / 100 (Note ${grade} – ${gradeLabel(grade)})`}
    >
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} aria-hidden="true">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke="#e3e8ef"
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={c}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        <text
          x="50%"
          y="50%"
          dominantBaseline="central"
          textAnchor="middle"
          className="score-indicator-value"
          style={{ fill: "#192738" }}
        >
          {pct}
        </text>
      </svg>
      {showLabel && (
        <span className="score-indicator-label" style={{ color }}>
          {gradeLabel(grade)}
        </span>
      )}
      <span className="visually-hidden">
        Metadaten-Qualität {pct} von 100, Note {grade}
      </span>
    </div>
  );
}
