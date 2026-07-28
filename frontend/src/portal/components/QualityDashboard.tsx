// Aggregierte Auswertung der überlagerten Bewertung („Metadatenqualität"-Seite):
// Kennzahlen plus vier Diagramme (Verteilung der Gesamtbewertung,
// Dimensions-Mittel, häufigste Mängel, Verlauf über die Läufe).
//
// Alle Zahlen stammen aus der Bewertung, die gerade über dem Datenbestand
// liegt — aus einem abgeschlossenen Lauf oder aus einer Berechnung dieser
// Sitzung. Ohne Bewertung zeigt die Seite, was zu tun ist, statt leerer Achsen.
//
// Ausnahme ist der Verlauf: er blickt über alle Läufe dieses Datenbestands
// hinweg und beantwortet die Frage, die einen Portalbetreiber mehr interessiert
// als jeder Einzelstand — bewegt sich die Qualität nach oben oder nach unten.
//
// Diagramme mit Recharts und den GovData-Chartfarben (CHART_COLORS /
// STATUS_COLORS), konsistent zu den übrigen Charts der Anwendung.

import { useMemo } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  ReferenceArea,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { dimensionLabel, DIMENSION_ORDER, scorePct } from "../lib/quality";
import { CHART_COLORS } from "../../lib/theme";
import { gradeColor, statusColor } from "../../lib/status";
import { scoreToGrade } from "../lib/quality";
import { indicatorMeta } from "../../lib/indicators";
import { useCatalog, useOverlay, usePortalSource } from "../source";
import { useRunDeficits, useRunResult, useRunTrend } from "../../hooks/usePortal";

const C = CHART_COLORS;

const SCORE_BINS: { label: string; lo: number; hi: number }[] = [
  { label: "0–40", lo: 0, hi: 0.4 },
  { label: "40–55", lo: 0.4, hi: 0.55 },
  { label: "55–65", lo: 0.55, hi: 0.65 },
  { label: "65–75", lo: 0.65, hi: 0.75 },
  { label: "75–100", lo: 0.75, hi: 1.001 },
];

/** Wie viele Indikatoren die Mängel-Rangliste zeigt. */
const TOP_DEFICITS = 10;

const tooltipStyle = {
  background: C.panel,
  border: `1px solid ${C.gridline}`,
  borderRadius: 5,
  fontSize: 12,
  color: C.text,
};

/** Kürzt lange Indikator-Namen für die Achsenbeschriftung. */
function shorten(label: string, max = 30): string {
  return label.length <= max ? label : `${label.slice(0, max - 1)}…`;
}

export function QualityDashboard() {
  const { catalog, overlay, presenting } = usePortalSource();
  const { datasets } = useCatalog();
  const state = useOverlay();

  const rows = useMemo(() => [...state.rows.values()], [state.rows]);
  const scored = useMemo(() => rows.filter((r) => r.overall != null), [rows]);

  // Die Mängel-Rangliste braucht Indikator-Ebene, die der Index nicht trägt.
  // Für einen Lauf holt sie sich das erste Ergebnis, um wenigstens die
  // Indikator-Menge zu kennen; die Zählung selbst kommt aus den Statuszahlen
  // je Datei, sofern Einzelergebnisse vorliegen (Berechnung dieser Sitzung).
  const sampleStem = scored[0]?.stem ?? null;
  const sampleResult = useRunResult(overlay?.kind === "run" ? overlay.run : null, sampleStem);

  // Die Rangliste braucht die Indikator-Ebene, die der Lauf-Index nicht trägt.
  // Für einen abgeschlossenen Lauf aggregiert sie das Backend (ein Aufruf statt
  // 50 Einzelergebnissen); eine Berechnung dieser Sitzung hat die Ergebnisse
  // ohnehin schon im Speicher.
  const runDeficits = useRunDeficits(overlay?.kind === "run" ? overlay.run : null);

  const deficitData = useMemo(() => {
    const counts = new Map<string, { fail: number; partial: number; total: number }>();

    for (const row of runDeficits.data ?? []) {
      counts.set(row.indicator_id, { fail: row.fail, partial: row.partial, total: row.total });
    }
    if (counts.size === 0) {
      for (const row of scored) {
        const result = state.resultFor(row.stem);
        if (!result) continue;
        for (const dim of Object.values(result.by_dimension)) {
          for (const indicator of dim.indicators) {
            const entry = counts.get(indicator.indicator_id) ?? { fail: 0, partial: 0, total: 0 };
            entry.total += 1;
            if (indicator.status === "fail") entry.fail += 1;
            else if (indicator.status === "partial") entry.partial += 1;
            counts.set(indicator.indicator_id, entry);
          }
        }
      }
    }

    return [...counts.entries()]
      .map(([id, c]) => ({
        id,
        label: shorten(indicatorMeta(id).label),
        fullLabel: indicatorMeta(id).label,
        fail: c.fail,
        partial: c.partial,
        total: c.total,
        share: Number((((c.fail + c.partial) / c.total) * 100).toFixed(1)),
      }))
      .sort((a, b) => b.share - a.share)
      .slice(0, TOP_DEFICITS);
  }, [scored, state, runDeficits.data]);

  const stats = useMemo(() => {
    if (scored.length === 0) return null;
    const values = scored.map((r) => r.overall as number);
    const dims: Record<string, number[]> = {};
    for (const row of scored) {
      for (const [dim, score] of Object.entries(row.dims)) {
        (dims[dim] ??= []).push(score);
      }
    }
    const totalIndicators = scored.reduce((acc, r) => acc + r.total_indicators, 0);
    const totalPass = scored.reduce((acc, r) => acc + r.n_pass, 0);
    return {
      n: scored.length,
      mean: values.reduce((a, b) => a + b, 0) / values.length,
      min: Math.min(...values),
      max: Math.max(...values),
      dimAvg: Object.fromEntries(
        Object.entries(dims).map(([dim, list]) => [dim, list.reduce((a, b) => a + b, 0) / list.length]),
      ),
      passShare: totalIndicators ? Math.round((totalPass / totalIndicators) * 100) : 0,
    };
  }, [scored]);

  const histData = useMemo(
    () =>
      SCORE_BINS.map((b) => ({
        label: b.label,
        count: scored.filter((r) => (r.overall as number) >= b.lo && (r.overall as number) < b.hi)
          .length,
        mid: (b.lo + b.hi) / 2,
      })),
    [scored],
  );

  const dimData = useMemo(
    () =>
      DIMENSION_ORDER.filter((dim) => stats?.dimAvg[dim] != null).map((dim) => ({
        dim: dimensionLabel(dim),
        value: Number(((stats?.dimAvg[dim] ?? 0) * 100).toFixed(1)),
      })),
    [stats],
  );

  const trend = useRunTrend(catalog);
  const trendData = useMemo(
    () =>
      (trend.data ?? []).map((point) => ({
        label: point.timestamp ?? point.run,
        score: Math.round(point.mean_overall * 1000) / 10,
        n: point.dataset_count,
        model: point.llm_model,
        run: point.run,
      })),
    [trend.data],
  );

  const worst = deficitData[0];

  if (!state.active || !stats) {
    return (
      <div className="gd-portal-container gd-dashboard stack">
        <header className="gd-dash-head">
          <p className="gd-dash-eyebrow">Prototyp · LLM-gestützte Metadatenbewertung</p>
          <h1>Metadatenqualität</h1>
          <p className="gd-dash-lead">
            Für den Datenbestand <code>{catalog}</code> liegt keine Bewertung vor. Legen Sie in der
            Datenansicht einen abgeschlossenen Lauf darüber oder starten Sie eine Berechnung —
            danach werten die Diagramme hier genau diese Ergebnisse aus.
          </p>
        </header>
        {state.loading && <p className="muted">Bewertung wird geladen…</p>}
      </div>
    );
  }

  const indicatorLevelAvailable = deficitData.length > 0;

  return (
    <div className="gd-portal-container gd-dashboard stack">
      <header className="gd-dash-head">
        <p className="gd-dash-eyebrow">Prototyp · LLM-gestützte Metadatenbewertung</p>
        <h1>Metadatenqualität des Datenbestands</h1>
        <p className="gd-dash-lead">
          Auswertung über <strong>{stats.n}</strong> bewertete Datensätze aus{" "}
          <code>{catalog}</code>
          {/* Die Herkunft der Bewertung ist eine Eigenschaft des Prototyps,
              nicht des Portals — im Vorführmodus entfällt sie. */}
          {!presenting && overlay?.kind === "run" && (
            <>
              {" "}
              · Lauf <code>{overlay.run}</code>
            </>
          )}
          {!presenting && overlay?.kind === "job" && <> · {overlay.label}</>}. Bewertet werden{" "}
          {Object.keys(stats.dimAvg).length} Dimensionen mit{" "}
          {sampleResult.data?.summary.total_indicators ?? scored[0]?.total_indicators} Indikatoren.
        </p>
      </header>

      <div className="gd-kpis">
        <Kpi k="Bewertete Datensätze" v={`${stats.n}`} n={`von ${datasets.length} im Bestand`} />
        <Kpi
          k="Ø Gesamtscore"
          v={`${scorePct(stats.mean)}`}
          unit="/ 100"
          n={`Spanne ${scorePct(stats.min)}–${scorePct(stats.max)}`}
        />
        <Kpi
          k="Erfüllte Indikatoren"
          v={`${stats.passShare}`}
          unit="%"
          n="über alle Prüfungen hinweg"
        />
        {worst ? (
          <Kpi
            k="Häufigster Mangel"
            v={`${Math.round(worst.share)}`}
            unit="%"
            n={worst.fullLabel}
          />
        ) : (
          <Kpi k="Häufigster Mangel" v="—" n="wird ermittelt…" />
        )}
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

        <Panel title="Durchschnitt je Dimension" hint="Mittlerer Dimensionsscore über alle bewerteten Datensätze.">
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

        {indicatorLevelAvailable && (
          <Panel
            title="Häufigste Mängel"
            hint={`Anteil der Datensätze, die den Indikator nicht oder nur teilweise erfüllen — die ${TOP_DEFICITS} auffälligsten. Der Tooltip trennt beides auf.`}
          >
            <div style={{ width: "100%", height: 320 }}>
              <ResponsiveContainer>
                <BarChart
                  data={deficitData}
                  layout="vertical"
                  margin={{ left: 24, right: 44, top: 8, bottom: 4 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke={C.gridline} horizontal={false} />
                  <XAxis
                    type="number"
                    domain={[0, 100]}
                    unit="%"
                    tick={{ fill: C.textSubtle, fontSize: 11 }}
                  />
                  <YAxis
                    type="category"
                    dataKey="label"
                    width={180}
                    tick={{ fill: C.textSecondary, fontSize: 11 }}
                  />
                  <Tooltip
                    contentStyle={tooltipStyle}
                    cursor={{ fill: C.panel2 }}
                    formatter={(_v, _n, item) => {
                      const d = item.payload as (typeof deficitData)[number];
                      return [
                        `${d.share} % — ${d.fail} nicht erfüllt, ${d.partial} teilweise (von ${d.total})`,
                        d.fullLabel,
                      ];
                    }}
                    labelFormatter={() => ""}
                  />
                  <Bar
                    dataKey="share"
                    name="nicht erfüllt"
                    fill={statusColor("fail")}
                    radius={[0, 4, 4, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Panel>
        )}

        {trendData.length > 1 && (
          <Panel
            title="Verlauf über die Bewertungsläufe"
            hint="Mittlerer Gesamtscore je Lauf über diesen Datenbestand, chronologisch."
          >
            <div style={{ width: "100%", height: 260 }}>
              <ResponsiveContainer>
                <LineChart data={trendData} margin={{ left: 4, right: 16, top: 8, bottom: 4 }}>
                  {/* Notenbänder als ruhiger Hintergrund: zeigt, in welchem
                      Qualitätsbereich sich der Bestand bewegt. */}
                  <ReferenceArea y1={0} y2={40} fill={gradeColor("F")} fillOpacity={0.06} />
                  <ReferenceArea y1={40} y2={60} fill={gradeColor("D")} fillOpacity={0.05} />
                  <ReferenceArea y1={60} y2={75} fill={gradeColor("C")} fillOpacity={0.06} />
                  <ReferenceArea y1={75} y2={100} fill={gradeColor("A")} fillOpacity={0.06} />
                  <CartesianGrid strokeDasharray="3 3" stroke={C.gridline} vertical={false} />
                  <XAxis dataKey="label" tick={{ fill: C.textSubtle, fontSize: 10 }} />
                  <YAxis domain={[0, 100]} tick={{ fill: C.textSubtle, fontSize: 11 }} />
                  <Tooltip
                    contentStyle={tooltipStyle}
                    formatter={(_v, _n, item) => {
                      const d = item.payload as (typeof trendData)[number];
                      return [
                        `${d.score} / 100 · ${d.n} Datensätze · ${d.model ?? "ohne Sprachmodell"}`,
                        "Ø Gesamtscore",
                      ];
                    }}
                  />
                  <Line
                    type="monotone"
                    dataKey="score"
                    name="Ø Gesamtscore"
                    stroke={C.primary}
                    strokeWidth={2}
                    dot={{ r: 4, fill: C.primary }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
            <p className="gd-panel-note muted">
              Die Punkte sind Bewertungsläufe, keine Erhebungszeitpunkte. Solange derselbe
              Datenstand mehrfach bewertet wird, zeigt die Linie die Streuung des Verfahrens;
              zum Qualitätsverlauf wird sie erst, wenn der Bestand wiederholt geerntet und
              danach bewertet wird.
            </p>
          </Panel>
        )}
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
