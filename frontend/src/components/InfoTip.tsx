// Info-Icon mit Erläuterung. Sichtbar bei Hover *und* bei Tastaturfokus, mit
// aria-describedby verknüpft (WCAG SC 1.4.13 / 2.1.1) — ein reines
// title-Attribut wäre für Screenreader und Touch unzuverlässig.
//
// Die Sprechblase wird bewusst nach `document.body` portiert und fest zum
// Viewport positioniert: Die Tabellenköpfe, in denen die Icons sitzen, stehen
// in einem Container mit `overflow-x: auto`. Ein absolut positioniertes Element
// darin vergrößert dessen Scrollbereich und wird am Rand abgeschnitten — die
// Tabelle würde beim Aufklappen breiter und die Erläuterung rechts abgeschnitten.

import { useCallback, useEffect, useId, useRef, useState } from "react";
import { createPortal } from "react-dom";

/** Muss zur max-width der Blase in _findings.scss passen. */
const BUBBLE_WIDTH = 280;
/** Grobe Höhe für die Entscheidung, ob nach oben geklappt wird. */
const BUBBLE_HEIGHT = 130;
const GAP = 6;
const MARGIN = 8;

interface Position {
  top: number;
  left: number;
  above: boolean;
}

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
  const [position, setPosition] = useState<Position | null>(null);
  const btnRef = useRef<HTMLButtonElement>(null);
  const open = position !== null;

  const show = useCallback(() => {
    const rect = btnRef.current?.getBoundingClientRect();
    if (!rect) return;

    // Am Knopf ausgerichtet, aber nie über den Fensterrand hinaus.
    const preferred = align === "end" ? rect.right - BUBBLE_WIDTH : rect.left - GAP;
    const left = Math.max(
      MARGIN,
      Math.min(preferred, window.innerWidth - BUBBLE_WIDTH - MARGIN),
    );
    // Nahe am unteren Rand nach oben klappen, statt aus dem Bild zu laufen.
    const above = rect.bottom + GAP + BUBBLE_HEIGHT > window.innerHeight;
    setPosition({
      top: above ? rect.top - GAP : rect.bottom + GAP,
      left,
      above,
    });
  }, [align]);

  const hide = useCallback(() => setPosition(null), []);

  // Beim Scrollen oder Größenändern wäre die gemessene Position veraltet.
  useEffect(() => {
    if (!open) return;
    window.addEventListener("scroll", hide, true);
    window.addEventListener("resize", hide);
    return () => {
      window.removeEventListener("scroll", hide, true);
      window.removeEventListener("resize", hide);
    };
  }, [open, hide]);

  return (
    <span className="info-tip" onMouseEnter={show} onMouseLeave={hide}>
      <button
        ref={btnRef}
        type="button"
        className="info-tip-btn"
        aria-label={`Erläuterung: ${label}`}
        aria-describedby={open ? id : undefined}
        aria-expanded={open}
        onFocus={show}
        onBlur={hide}
        onClick={(e) => {
          e.stopPropagation();
          if (open) hide();
          else show();
        }}
      >
        <span aria-hidden="true">i</span>
      </button>
      {position &&
        createPortal(
          <span
            className="info-tip-bubble"
            role="tooltip"
            id={id}
            style={{
              top: position.top,
              left: position.left,
              transform: position.above ? "translateY(-100%)" : undefined,
            }}
          >
            <strong>{label}</strong>
            {text}
          </span>,
          document.body,
        )}
    </span>
  );
}
