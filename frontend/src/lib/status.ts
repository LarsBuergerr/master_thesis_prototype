import type { IndicatorStatus } from "../api/types";

export const STATUS_COLORS: Record<string, string> = {
  pass: "#3ecf8e",
  partial: "#f5b945",
  fail: "#ef5b6b",
  not_applicable: "#6b7280",
  error: "#6b7280",
};

export function statusColor(status: string): string {
  return STATUS_COLORS[status] ?? "#6b7280";
}

export function gradeColor(grade: string): string {
  if (grade === "A" || grade === "B") return "#3ecf8e";
  if (grade === "C") return "#f5b945";
  return "#ef5b6b";
}

export function statusLabel(status: IndicatorStatus): string {
  return status.replace("_", " ");
}

/** Round to 2 decimals for display, tolerating null/undefined. */
export function fmt(n: number | null | undefined, digits = 2): string {
  if (n === null || n === undefined || Number.isNaN(n)) return "–";
  return n.toFixed(digits);
}
