/**
 * Theme tokens and the fixed status palette.
 *
 * Values here MUST stay in sync with the CSS custom properties in
 * `styles.css` (`:root` / `[data-theme]`) — duplicated rather than read via
 * `getComputedStyle` because Recharts (SVG) needs plain hex strings at
 * render time. See docs/frontend_design_literatur.md for how these hexes
 * were derived and validated (WCAG contrast, CVD-safe status palette).
 */

export type Theme = "light" | "dark";

const STORAGE_KEY = "theme";

export interface ThemeColors {
  page: string;
  panel: string;
  panel2: string;
  border: string;
  text: string;
  textSecondary: string;
  textSubtle: string;
  accent: string;
  accentSolid: string;
  gridline: string;
  baseline: string;
}

export const THEME_COLORS: Record<Theme, ThemeColors> = {
  light: {
    page: "#f9f9f7",
    panel: "#fcfcfb",
    panel2: "#f1f0ec",
    border: "rgba(11,11,11,0.10)",
    text: "#0b0b0b",
    textSecondary: "#52514e",
    textSubtle: "#898781",
    accent: "#2a78d6",
    accentSolid: "#256abf",
    gridline: "#e1e0d9",
    baseline: "#c3c2b7",
  },
  dark: {
    page: "#0d0d0d",
    panel: "#1a1a19",
    panel2: "#222221",
    border: "rgba(255,255,255,0.10)",
    text: "#ffffff",
    textSecondary: "#c3c2b7",
    textSubtle: "#898781",
    accent: "#3987e5",
    accentSolid: "#256abf",
    gridline: "#2c2c2a",
    baseline: "#383835",
  },
};

/** Fixed status palette — same hex in both themes (never themed, see doc). */
export const STATUS_COLORS: Record<string, { bg: string; on: string }> = {
  pass: { bg: "#0ca30c", on: "#0b0b0b" },
  partial: { bg: "#fab219", on: "#0b0b0b" },
  fail: { bg: "#d03b3b", on: "#ffffff" },
  error: { bg: "#ec835a", on: "#0b0b0b" },
  not_applicable: { bg: "#898781", on: "#0b0b0b" },
};

export const GRADE_STATUS: Record<string, keyof typeof STATUS_COLORS> = {
  A: "pass",
  B: "pass",
  C: "partial",
  D: "fail",
  F: "fail",
};

export function statusColor(status: string): string {
  return (STATUS_COLORS[status] ?? STATUS_COLORS.not_applicable).bg;
}

export function statusTextColor(status: string): string {
  return (STATUS_COLORS[status] ?? STATUS_COLORS.not_applicable).on;
}

export function gradeColor(grade: string): string {
  return statusColor(GRADE_STATUS[grade] ?? "fail");
}

export function getStoredTheme(): Theme | null {
  const v = localStorage.getItem(STORAGE_KEY);
  return v === "light" || v === "dark" ? v : null;
}

export function setStoredTheme(theme: Theme | null): void {
  if (theme) localStorage.setItem(STORAGE_KEY, theme);
  else localStorage.removeItem(STORAGE_KEY);
}

export function prefersDarkScheme(): boolean {
  return (
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
  );
}
