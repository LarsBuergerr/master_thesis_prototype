// Info-Icon mit Erläuterung. Sichtbar bei Hover *und* bei Tastaturfokus, mit
// aria-describedby verknüpft (WCAG SC 1.4.13 / 2.1.1) — ein reines
// title-Attribut wäre für Screenreader und Touch unzuverlässig.

import { useId, useState } from "react";

export function InfoTip({
  label,
  text,
  align = "start",
}: {
  /** Worauf sich die Erläuterung bezieht — für Screenreader. */
  label: string;
  text: string;
  align?: "start" | "end";
}) {
  const id = useId();
  const [open, setOpen] = useState(false);

  return (
    <span
      className="info-tip"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      <button
        type="button"
        className="info-tip-btn"
        aria-label={`Erläuterung: ${label}`}
        aria-describedby={open ? id : undefined}
        aria-expanded={open}
        onFocus={() => setOpen(true)}
        onBlur={() => setOpen(false)}
        onClick={(e) => {
          e.stopPropagation();
          setOpen((v) => !v);
        }}
      >
        <span aria-hidden="true">i</span>
      </button>
      {open && (
        <span className={`info-tip-bubble ${align}`} role="tooltip" id={id}>
          <strong>{label}</strong>
          {text}
        </span>
      )}
    </span>
  );
}
