// Aggregierte Auswertung der Stichprobe („Metadatenqualität"-Seite): Kennzahlen
// plus vier Diagramme (Verteilung, Dimensions-Mittel, Prototyp vs. MQA je
// Datensatz, Übereinstimmung mit der Ground Truth). Diagramme mit Recharts und
// den GovData-Chartfarben (CHART_COLORS), konsistent zu den übrigen Charts der
// Anwendung.

import { useMemo } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ReferenceLine,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { AGGREGATE, DATASETS, GROUND_TRUTH } from "../data/evaluation";
import { dimensionLabel, DIMENSION_ORDER, scorePct } from "../lib/quality";
import { CHART_COLORS } from "../../lib/theme";
import { gradeColor } from "../../lib/status";
import { scoreToGrade } from "../lib/quality";

const C = CHART_COLORS;

const SCORE_BINS: { label: string; lo: number; hi: number }[] = [
  { label: "40–45", lo: 0.4, hi: 0.45 },
  { label: "45–55", lo: 0.45, hi: 0.55 },
  { label: "55–65", lo: 0.55, hi: 0.65 },
  { label: "65–75", lo: 0.65, hi: 0.75 },
  { label: "75–85", lo: 0.75, hi: 0.851 },
];

const GT_LABELS: Record<string, string> = {
  "gesamt (4 Dim.)": "Gesamt (4 Dim.)",
  "ohne Expressiveness (3 Dim.)": "Ohne Aussagekraft",
  findability: "Auffindbarkeit",
  accessibility: "Zugänglichkeit",
  reusability: "Nachnutzbarkeit",
  expressiveness: "Aussagekraft",
};

const tooltipStyle = {
  background: C.panel,
  border: `1px solid ${C.gridline}`,
  borderRadius: 5,
  fontSize: 12,
  color: C.text,
};

export function QualityDashboard() {
  const gesamt = GROUND_TRUTH.find((g) => g.ziel.startsWith("gesamt"))!;
  const betterThanMqa = GROUND_TRUTH.filter((g) => g.delta > 0).length;

  const histData = useMemo(
    () =>
      SCORE_BINS.map((b) => ({
        label: b.label,
        count: DATASETS.filter((d) => d.overall >= b.lo && d.overall < b.hi).length,
        mid: (b.lo + b.hi) / 2,
      })),
    [],
  );

  const dimData = useMemo(
    () =>
      DIMENSION_ORDER.map((dim) => ({
        dim: dimensionLabel(dim),
        value: Number(((AGGREGATE.dimAvg[dim] ?? 0) * 100).toFixed(1)),
      })),
    [],
  );

  const scatterData = useMemo(
    () =>
      DATASETS.filter((d) => d.protoNorm != null && d.mqaScoreNorm != null).map((d) => ({
        x: Math.round(d.mqaScoreNorm! * 100),
        y: Math.round(d.protoNorm! * 100),
        title: d.title,
        grade: scoreToGrade(d.overall),
      })),
    [],
  );

  const triData = useMemo(
    () =>
      GROUND_TRUTH.map((g) => ({
        ziel: GT_LABELS[g.ziel] ?? g.ziel,
        Prototyp: Number(g.protRho.toFixed(3)),
        MQA: Number(g.mqaRho.toFixed(3)),
      })),
    [],
  );

  return (
    <div className="gd-portal-container gd-dashboard stack">
      <header className="gd-dash-head">
        <p className="gd-dash-eyebrow">Prototyp · LLM-gestützte Metadatenbewertung</p>
        <h1>Metadatenqualität der Stichprobe</h1>
        <p className="gd-dash-lead">
          Ergebnisse des Bewertungsprototyps über die Evaluationsstichprobe (n&nbsp;=&nbsp;
          {AGGREGATE.n}, geschichtet nach Geo-/Fachdaten). Bewertet werden vier Dimensionen mit 27
          Indikatoren; trianguliert gegen das offizielle MQA-Verfahren von data.europa.eu sowie eine
          manuelle Ground&nbsp;Truth.
        </p>
      </header>

      <div className="gd-kpis">
        <Kpi k="Datensätze" v={`${AGGREGATE.n}`} n="25 Geo / 25 Fachdaten" />
        <Kpi
          k="Ø Gesamtscore"
          v={`${scorePct(AGGREGATE.overallMean)}`}
          unit="/ 100"
          n={`Spanne ${scorePct(AGGREGATE.overallMin)}–${scorePct(AGGREGATE.overallMax)}`}
        />
        <Kpi
          k="ρ zur Ground Truth"
          v={gesamt.protRho.toFixed(2)}
          n={`MQA-Referenz ${gesamt.mqaRho.toFixed(2)} · Δ +${gesamt.delta.toFixed(2)}`}
        />
        <Kpi
          k="Prototyp ≥ MQA"
          v={`${betterThanMqa}`}
          unit="/ 6"
          n="Ziele mit höherer GT-Korrelation"
        />
      </div>

      <div className="gd-panels">
        <Panel title="Verteilung der Gesamtbewertung" hint="Anzahl Datensätze je Score-Bereich (0–100).">
          <div style={{ width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <BarChart data={histData} margin={{ left: 4, right: 12, top: 8, bottom: 4 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={C.gridline} vertical={false} />
                <XAxis dataKey="label" tick={{ fill: C.textSubtle, fontSize: 11 }} />
                <YAxis allowDecimals={false} tick={{ fill: C.textSubtle, fontSize: 11 }} />
                <Tooltip
                  contentStyle={tooltipStyle}
                  cursor={{ fill: C.panel2 }}
                  formatter={(v) => [`${v} Datensätze`, "Anzahl"]}
                />
                <Bar dataKey="count" name="Datensätze" radius={[4, 4, 0, 0]}>
                  {histData.map((d) => (
                    <Cell key={d.label} fill={gradeColor(scoreToGrade(d.mid))} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel title="Durchschnitt je Dimension" hint="Mittlerer Indikator-Score der vier Dimensionen.">
          <div style={{ width: "100%", height: 240 }}>
            <ResponsiveContainer>
              <BarChart
                data={dimData}
                layout="vertical"
                margin={{ left: 24, right: 40, top: 8, bottom: 4 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke={C.gridline} horizontal={false} />
                <XAxis type="number" domain={[0, 100]} tick={{ fill: C.textSubtle, fontSize: 11 }} />
                <YAxis
                  type="category"
                  dataKey="dim"
                  width={110}
                  tick={{ fill: C.textSecondary, fontSize: 12 }}
                />
                <Tooltip
                  contentStyle={tooltipStyle}
                  cursor={{ fill: C.panel2 }}
                  formatter={(v) => [`${v} / 100`, "Ø Score"]}
                />
                <Bar dataKey="value" name="Ø Score" radius={[0, 4, 4, 0]}>
                  {dimData.map((d) => (
                    <Cell key={d.dim} fill={gradeColor(scoreToGrade(d.value / 100))} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel
          title="Prototyp vs. MQA je Datensatz"
          hint="Normierter Score je Datensatz. Punkte nahe der Diagonalen bedeuten Übereinstimmung mit dem offiziellen Verfahren."
        >
          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <ScatterChart margin={{ left: 8, right: 16, top: 8, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={C.gridline} />
                <XAxis
                  type="number"
                  dataKey="x"
                  domain={[0, 100]}
                  name="MQA-Score"
                  tick={{ fill: C.textSubtle, fontSize: 11 }}
                  label={{ value: "MQA-Score", position: "insideBottom", offset: -10, fill: C.textSubtle, fontSize: 11 }}
                />
                <YAxis
                  type="number"
                  dataKey="y"
                  domain={[0, 100]}
                  name="Prototyp-Score"
                  tick={{ fill: C.textSubtle, fontSize: 11 }}
                  label={{ value: "Prototyp", angle: -90, position: "insideLeft", fill: C.textSubtle, fontSize: 11 }}
                />
                <ReferenceLine
                  segment={[{ x: 0, y: 0 }, { x: 100, y: 100 }]}
                  stroke={C.baseline}
                  strokeDasharray="4 4"
                />
                <Tooltip
                  contentStyle={tooltipStyle}
                  cursor={{ strokeDasharray: "3 3" }}
                  formatter={(v, n) => [`${v}`, n === "y" ? "Prototyp" : "MQA"]}
                  labelFormatter={() => ""}
                />
                <Scatter data={scatterData} name="Datensätze">
                  {scatterData.map((d, i) => (
                    <Cell key={i} fill={gradeColor(d.grade)} fillOpacity={0.82} />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          </div>
        </Panel>

        <Panel
          title="Übereinstimmung mit der Ground Truth"
          hint="Rangkorrelation (Spearman ρ) zur manuellen Ground Truth — Prototyp neben MQA. Höher ist besser."
        >
          <div style={{ width: "100%", height: 300 }}>
            <ResponsiveContainer>
              <BarChart
                data={triData}
                layout="vertical"
                margin={{ left: 24, right: 16, top: 8, bottom: 4 }}
                barGap={2}
              >
                <CartesianGrid strokeDasharray="3 3" stroke={C.gridline} horizontal={false} />
                <XAxis type="number" domain={[0, 1]} tick={{ fill: C.textSubtle, fontSize: 11 }} />
                <YAxis
                  type="category"
                  dataKey="ziel"
                  width={130}
                  tick={{ fill: C.textSecondary, fontSize: 11 }}
                />
                <Tooltip
                  contentStyle={tooltipStyle}
                  cursor={{ fill: C.panel2 }}
                  formatter={(v, n) => [`ρ = ${v}`, n]}
                />
                <Legend />
                <Bar dataKey="Prototyp" fill={C.primary} radius={[0, 3, 3, 0]} />
                <Bar dataKey="MQA" fill={C.accent} radius={[0, 3, 3, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Panel>
      </div>
    </div>
  );
}

function Kpi({ k, v, unit, n }: { k: string; v: string; unit?: string; n: string }) {
  return (
    <div className="gd-kpi design-box">
      <p className="gd-kpi-k">{k}</p>
      <p className="gd-kpi-v">
        {v}
        {unit && <span className="gd-kpi-unit"> {unit}</span>}
      </p>
      <p className="gd-kpi-n">{n}</p>
    </div>
  );
}

function Panel({
  title,
  hint,
  children,
}: {
  title: string;
  hint: string;
  children: React.ReactNode;
}) {
  return (
    <section className="gd-panel design-box design-box-padding">
      <h2 className="gd-panel-title">{title}</h2>
      <p className="gd-panel-hint muted">{hint}</p>
      {children}
    </section>
  );
}
