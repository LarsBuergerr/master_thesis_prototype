// Kompakte Werkzeugleiste über den Ergebnistabellen.
//
// Rechtsbündig und klein gehalten — es ist ein Anzeigeschalter, kein Inhalt.
// Der Zähler bleibt sichtbar, damit eine gefilterte Tabelle nie unbemerkt
// unvollständig ist; in einem Werkzeug, dessen Zweck Nachvollziehbarkeit ist,
// wäre stilles Ausblenden das falsche Signal.

export function ResultToolbar({
  hidePassing,
  onChange,
  actionable,
  total,
  allExpanded,
  onToggleAll,
}: {
  hidePassing: boolean;
  onChange: (next: boolean) => void;
  /** Anzahl nicht erfüllter Indikatoren über alle Dimensionen. */
  actionable: number;
  total: number;
  /** Richtung der letzten Betätigung — bestimmt nur die Beschriftung. */
  allExpanded: boolean;
  /** Klappt Dimensionen und die Befunde darin gemeinsam auf bzw. zu. */
  onToggleAll: () => void;
}) {
  return (
    <div className="ind-toolbar">
      {/* Ein Knopf für beide Ebenen: Wer alles sehen will, will nicht erst jede
          Dimension und darin nochmals jeden Befund einzeln aufklappen. */}
      <button
        type="button"
        className="ind-toolbar-btn"
        onClick={onToggleAll}
        title={
          allExpanded
            ? "Alle Dimensionen und Befunde zuklappen"
            : "Alle Dimensionen und alle Befunde darin aufklappen"
        }
      >
        {allExpanded ? "Alles einklappen" : "Alles ausklappen"}
      </button>

      <label className="ind-toolbar-check">
        <input
          type="checkbox"
          checked={hidePassing}
          onChange={(e) => onChange(e.target.checked)}
        />
        Nur Handlungsbedarf
        <span className="ind-toolbar-count">
          ({actionable}/{total})
        </span>
      </label>
    </div>
  );
}
