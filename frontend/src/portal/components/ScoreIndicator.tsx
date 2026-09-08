// Kompakter Qualitäts-Indikator für die Trefferliste: Beschriftung, Punktwert
// mit Bezugsgröße („80 / 100"), ein Balken in der Notenfarbe und das
// Klartext-Urteil. Bewusst leichtgewichtig als DOM/CSS gehalten (kein
// Recharts), da bis zu 50 Instanzen gleichzeitig in der Liste stehen.
//
// Der Balken hat den früheren Ring abgelöst: Er trägt dieselbe Aussage auf
// weniger Höhe und lässt neben der Beschriftung Platz für den Infotag, über
// den die Kurzfassung der Bewertung erreichbar ist (Dimensionen, Note,
// Erfüllungsquote).
//
// Farbe ist nie der einzige Träger: Der Punktwert, das Notenkürzel und ein
// Textlabel stehen daneben (WCAG 1.4.1). Die Beschriftung nimmt die
// Text-Notenfarbe (>= 4,5:1 gegen Weiß, WCAG 1.4.3) — die satte Flächenfarbe
// bleibt dem Balken vorbehalten (WCAG 1.4.11).

import type { RunIndexRow } from "../../api/types";
import { gradeColor, gradeTextColor } from "../../lib/status";
import { InfoTip } from "../../components/InfoTip";
import { DIMENSION_ORDER, dimensionLabel, gradeLabel, scoreToGrade, scorePct } from "../lib/quality";

interface Props {
  score: number;
  /** Kurzbewertung für den Infotag; fehlt sie, entfällt der Tag. */
  detail?: RunIndexRow | null;
  /** Klick auf den Wert — führt zur Detailseite. */
  onOpen?: () => void;
  /** Beschriftung des Klickziels für Screenreader. */
  openLabel?: string;
}

export function ScoreIndicator({ score, detail, onOpen, openLabel }: Props) {
  const grade = scoreToGrade(score);
  const color = gradeColor(grade);
  const textColor = gradeTextColor(grade);
  const pct = scorePct(score);
  const filled = Math.max(0, Math.min(100, pct));

  const figure = (
    <>
      <span className="score-indicator-figure">
        <span className="score-indicator-value tnum" style={{ color: textColor }}>
          {pct}
        </span>
        <span className="score-indicator-max"> / 100</span>
      </span>
      <span className="score-indicator-bar" aria-hidden="true">
        <span className="score-indicator-fill" style={{ width: `${filled}%`, background: color }} />
      </span>
      <span className="score-indicator-label" style={{ color: textColor }}>
        {gradeLabel(grade)} ({grade})
      </span>
      <span className="visually-hidden">
        Metadaten-Qualität {pct} von 100 Punkten, Note {grade}
      </span>
    </>
  );

  return (
    <div className="score-indicator">
      <div className="score-indicator-head">
        <span className="score-indicator-caption">Metadaten-Qualität</span>
        <InfoTip
          size="rich"
          align="end"
          label="Metadaten-Qualität"
          text={<QualitySummary score={score} detail={detail} />}
        />
      </div>
      {onOpen ? (
        <button
          type="button"
          className="score-indicator-body button-reset"
          onClick={onOpen}
          aria-label={openLabel}
        >
          {figure}
        </button>
      ) : (
        <div className="score-indicator-body">{figure}</div>
      )}
    </div>
  );
}

/**
 * Inhalt des Infotags: erst, was die Zahl überhaupt ist, dann woraus sie sich
 * zusammensetzt. Die Dimensionszeilen sind der eigentliche Zugewinn — sie
 * beantworten „woran liegt es?" schon in der Trefferliste, ohne die
 * Detailseite zu öffnen.
 */
function QualitySummary({ score, detail }: { score: number; detail?: RunIndexRow | null }) {
  const grade = scoreToGrade(score);
  const dims = detail?.dims ?? {};
  const known = DIMENSION_ORDER.filter((d) => dims[d] != null) as string[];
  const extra = Object.keys(dims).filter((d) => !known.includes(d));
  const order = [...known, ...extra];

  return (
    <>
      <span className="score-tip-lead">
        Automatisch geprüfte Qualität der <em>Metadaten</em> — nicht der Daten selbst: wie
        vollständig, konform und aussagekräftig dieser Eintrag beschrieben ist.
      </span>
      <span className="score-tip-total">
        <b className="tnum">{scorePct(score)} / 100</b> · Note {grade} ({gradeLabel(grade)})
      </span>
      {order.length > 0 && (
        <span className="score-tip-dims">
          {order.map((dim) => {
            const value = scorePct(dims[dim]);
            return (
              <span key={dim} className="score-tip-dim">
                <span className="score-tip-dim-name">{dimensionLabel(dim)}</span>
                <span className="score-tip-dim-bar" aria-hidden="true">
                  <span
                    className="score-tip-dim-fill"
                    style={{
                      width: `${Math.max(0, Math.min(100, value))}%`,
                      background: gradeColor(scoreToGrade(dims[dim])),
                    }}
                  />
                </span>
                <span className="score-tip-dim-value tnum">{value}</span>
              </span>
            );
          })}
        </span>
      )}
      {detail && (
        <span className="score-tip-foot">
          {detail.n_pass} von {detail.total_indicators} Indikatoren erfüllt
          {detail.n_partial > 0 && `, ${detail.n_partial} teilweise`}
        </span>
      )}
    </>
  );
}
