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
}: {
  hidePassing: boolean;
  onChange: (next: boolean) => void;
  /** Anzahl nicht erfüllter Indikatoren über alle Dimensionen. */
  actionable: number;
  total: number;
}) {
  return (
    <div className="ind-toolbar">
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
