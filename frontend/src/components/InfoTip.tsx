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
import type { ReactNode } from "react";
import { createPortal } from "react-dom";

/**
 * Maße der Blase je Variante. Sie müssen zu den `max-width`-Werten in
 * _findings.scss passen: Die Position wird hier gerechnet, nicht vom Browser.
 * Die Höhe ist nur eine Schätzung — sie entscheidet allein darüber, ob die
 * Blase nach oben klappt, statt aus dem Bild zu laufen.
 */
const SIZES = {
  regular: { width: 280, height: 130 },
  // Die Kurzfassung der Bewertung trägt eine Zeile je Dimension und braucht
  // deshalb mehr Platz in beide Richtungen.
  rich: { width: 300, height: 230 },
} as const;

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
  size = "regular",
}: {
  /** Worauf sich die Erläuterung bezieht — für Screenreader. */
  label: string;
  /** Erläuterung; auch strukturierter Inhalt (z. B. eine Kurzbewertung). */
  text: ReactNode;
  align?: "start" | "end";
  /** `rich` für mehrzeilige Inhalte — breitere Blase, siehe SIZES. */
  size?: keyof typeof SIZES;
}) {
  const id = useId();
  const [position, setPosition] = useState<Position | null>(null);
  const btnRef = useRef<HTMLButtonElement>(null);
  const open = position !== null;

  const show = useCallback(() => {
    const rect = btnRef.current?.getBoundingClientRect();
    if (!rect) return;

    const { width, height } = SIZES[size];
    // Am Knopf ausgerichtet, aber nie über den Fensterrand hinaus.
    const preferred = align === "end" ? rect.right - width : rect.left - GAP;
    const left = Math.max(MARGIN, Math.min(preferred, window.innerWidth - width - MARGIN));
    // Nahe am unteren Rand nach oben klappen, statt aus dem Bild zu laufen.
    const above = rect.bottom + GAP + height > window.innerHeight;
    setPosition({
      top: above ? rect.top - GAP : rect.bottom + GAP,
      left,
      above,
    });
  }, [align, size]);

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
            className={`info-tip-bubble${size === "rich" ? " rich" : ""}`}
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
