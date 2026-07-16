/**
 * GovData-Farbpalette für die Recharts-Diagramme.
 *
 * Die Hex-Werte MÜSSEN mit den SCSS-Tokens in `src/css/_color-tokens.scss`
 * übereinstimmen (dupliziert statt via `getComputedStyle`, weil Recharts/SVG
 * zur Renderzeit echte Hex-Strings braucht). Quelle der Tokens ist das
 * offizielle GovData-Frontend (webapp/src/css/_color-tokens.scss); die
 * Chart-Akzentfarben (Magenta) entsprechen der GovData-Metadatenqualitäts-
 * Seite (app/metadatenqualitaet/_components/Charts/common.ts: COLOR_DARK /
 * COLOR_LIGHT). Kontrast-Nachweise: docs/frontend_govdata_adoption.md.
 *
 * GovData ist ein reines Hell-Design — es gibt daher keinen Dark-Mode mehr.
 */

export interface ChartColors {
  page: string;
  panel: string;
  panel2: string;
  border: string;
  text: string;
  textSecondary: string;
  textSubtle: string;
  /** Chart-Akzent: Magenta der GovData-Metadatenqualitäts-Seite. */
  accent: string;
  accentLight: string;
  /** UI-Primärfarbe (Buttons/Links/Fortschritt): GovData Primary-400. */
  primary: string;
  gridline: string;
  baseline: string;
}

export const CHART_COLORS: ChartColors = {
  page: "#f5f5f5", // $clr-body-background
  panel: "#ffffff", // design-box
  panel2: "#f3f6fb", // $clr-neutral-grey-100
  border: "#cdd8e1", // $clr-neutral-grey-300
  text: "#192738", // $clr-neutral-grey-800
  textSecondary: "#3d4f66", // $clr-neutral-grey-600
  textSubtle: "#5d728b", // $clr-neutral-grey-500
  accent: "#80004b", // $clr-metadaten-magenta-400 (MQA COLOR_DARK)
  accentLight: "#e6cbda", // $clr-metadaten-magenta-200 (MQA COLOR_LIGHT)
  primary: "#0073a8", // $clr-primary-400
  gridline: "#cdd8e1", // $clr-neutral-grey-300
  baseline: "#93a5bb", // $clr-neutral-grey-400
};

/**
 * Status-Palette für Chart-Flächen (satte 400/500er-Töne, alle >= 3:1 gegen
 * Weiß, WCAG 1.4.11) und für Tags (`on` = Textfarbe auf heller 200er-Füllung,
 * alle >= 4.5:1, WCAG 1.4.3). Die Tag-Optik selbst kommt aus
 * `css/components/_gd-tag.scss` (GovData-Muster .gd-tag.green/.yellow).
 */
export const STATUS_COLORS: Record<string, { solid: string; bg: string; on: string }> = {
  pass: { solid: "#2d9880", bg: "#d9f7f1", on: "#206d5c" },
  partial: { solid: "#938a01", bg: "#fdfacc", on: "#7b7301" },
  fail: { solid: "#e63e3e", bg: "#ffdada", on: "#b33030" },
  error: { solid: "#3d3d3d", bg: "#3d3d3d", on: "#ffffff" },
  not_applicable: { solid: "#5d728b", bg: "#e3e8ef", on: "#3d4f66" },
};

export const GRADE_STATUS: Record<string, keyof typeof STATUS_COLORS> = {
  A: "pass",
  B: "pass",
  C: "partial",
  D: "fail",
  F: "fail",
};

/** Satte Statusfarbe für Chart-Flächen (Balken, Gauge). */
export function statusColor(status: string): string {
  return (STATUS_COLORS[status] ?? STATUS_COLORS.not_applicable).solid;
}

export function statusTextColor(status: string): string {
  return (STATUS_COLORS[status] ?? STATUS_COLORS.not_applicable).on;
}

export function gradeColor(grade: string): string {
  return statusColor(GRADE_STATUS[grade] ?? "fail");
}
