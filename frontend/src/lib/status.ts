import type { IndicatorStatus } from "../api/types";

export { statusColor, statusTextColor, gradeColor } from "./theme";

export function statusLabel(status: IndicatorStatus): string {
  return status.replace("_", " ");
}

/** Icon glyph per status — status is never carried by color alone (WCAG SC
 * 1.4.1 "Use of Color"; see thesis section 5.8). */
const STATUS_ICONS: Record<string, string> = {
  pass: "✓",
  partial: "◐",
  fail: "✕",
  error: "!",
  not_applicable: "–",
};

export function statusIcon(status: string): string {
  return STATUS_ICONS[status] ?? "?";
}

/** Round to 2 decimals for display, tolerating null/undefined. */
export function fmt(n: number | null | undefined, digits = 2): string {
  if (n === null || n === undefined || Number.isNaN(n)) return "–";
  return n.toFixed(digits);
}

/** Last path/fragment segment of a URI, for compact display (full URI stays
 * available via the caller's `title` tooltip). Falls back to the input
 * unchanged for non-URI strings (e.g. plain literals). */
export function shortenUri(uri: string): string {
  const match = uri.match(/[/#]([^/#]+)\/?$/);
  return match ? decodeURIComponent(match[1]) : uri;
}
