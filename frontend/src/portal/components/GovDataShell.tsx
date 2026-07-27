// GovData-Rahmen (Chrome) um alle Portal-Ansichten: Bund-Leiste mit
// Flaggen-Signet, Kopfzeile mit Logo + Hauptnavigation, Fußzeile. Aufbau,
// Beschriftungen und Farbwelt orientieren sich am offiziellen GovData-Portal
// (govdata.de). Kein Dark-Mode/keine Umschalter — GovData ist ein reines
// Hell-Design.

import type { ReactNode } from "react";
import type { Navigate, PortalView } from "../route";
import { usePortalSource } from "../source";

// GovData liefert kein Icon-Set aus, das hier eingebunden wäre (der übernommene
// Button-Auszug lässt die Icon-Variante bewusst weg). Die beiden Glyphen sind
// deshalb selbst gezeichnet — im selben Stil wie der Qualitätsring: schlankes
// Inline-SVG mit `currentColor`, damit sie die Zustandsfarben des Buttons
// mitnehmen.
function ToolIcon() {
  return (
    <svg
      className="gd-button-icon"
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {/* Schraubenschlüssel */}
      <path d="M15.5 4.2a4.5 4.5 0 0 0-5.9 5.6L3.6 15.8a1.6 1.6 0 0 0 0 2.3l2.3 2.3a1.6 1.6 0 0 0 2.3 0l6-6a4.5 4.5 0 0 0 5.6-5.9l-2.6 2.6-2.6-.7-.7-2.6z" />
    </svg>
  );
}

function SwapIcon() {
  return (
    <svg
      className="gd-button-icon"
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      {/* Datenbestand (Zylinder) mit Wechselpfeil */}
      <ellipse cx="12" cy="5.5" rx="7" ry="2.8" />
      <path d="M5 5.5v6c0 1.5 3.1 2.8 7 2.8s7-1.3 7-2.8v-6" />
      <path d="M8 19h8m0 0-2.5-2.5M16 19l-2.5 2.5" />
    </svg>
  );
}

interface NavItem {
  label: string;
  // Nur parameterlose Ansichten sind über die Hauptnavigation erreichbar.
  view: "list" | "quality";
  inert?: boolean;
}

const NAV: NavItem[] = [
  { label: "Daten", view: "list" },
  { label: "Metadatenqualität", view: "quality" },
  { label: "SPARQL", view: "list", inert: true },
  { label: "Informationen", view: "list", inert: true },
];

interface Props {
  view: PortalView;
  onNavigate: Navigate;
  /** Ohne geladenen Datenbestand führt die Navigation ins Leere — dann bleibt
   *  nur die Quellenauswahl, und die Menüpunkte sind abgeschaltet. */
  hasCatalog: boolean;
  children: ReactNode;
}

export function GovDataShell({ view, onNavigate, hasCatalog, children }: Props) {
  const { reset } = usePortalSource();

  return (
    <div className="gd-portal">
      <a className="skip-link" href="#portal-main">
        Zum Hauptinhalt springen
      </a>

      <div className="gd-federal">
        <div className="gd-federal-inner">
          <span className="gd-flag" aria-hidden="true">
            <i />
            <i />
            <i />
          </span>
          <span>Offizielle Website der Bundesrepublik Deutschland</span>
        </div>
      </div>

      <header className="gd-header">
        <div className="gd-header-inner">
          <button
            type="button"
            className="gd-logo button-reset"
            onClick={() => onNavigate({ view: "list" })}
            aria-label="GovData – zur Startseite"
          >
            <span className="gd-logo-dots" aria-hidden="true">
              {Array.from({ length: 20 }, (_, i) => (
                <i key={i} />
              ))}
            </span>
            <span className="gd-logo-text">
              <span className="gd-logo-mark">
                <span className="gd-logo-gov">Gov</span>
                <span className="gd-logo-data">Data</span>
              </span>
              <span className="gd-logo-sub">Das Datenportal für Deutschland</span>
            </span>
          </button>

          <nav className="gd-nav" aria-label="Hauptnavigation">
            {NAV.map((item, idx) => {
              const active = hasCatalog && !item.inert && item.view === view;
              const disabled = !hasCatalog || item.inert;
              return (
                <button
                  key={`${item.label}-${idx}`}
                  type="button"
                  className={`gd-nav-link button-reset${active ? " active" : ""}`}
                  aria-current={active ? "page" : undefined}
                  disabled={disabled}
                  onClick={() =>
                    !disabled &&
                    onNavigate(item.view === "quality" ? { view: "quality" } : { view: "list" })
                  }
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          <div className="gd-header-actions">
            {hasCatalog && (
              <button
                type="button"
                className="gd-button gd-button-ghost gd-button-icon-only"
                onClick={reset}
                title="Portal leeren und einen anderen Datenbestand laden"
                aria-label="Datenbestand wechseln"
              >
                <SwapIcon />
                <span className="gd-button-label">Datenbestand wechseln</span>
              </button>
            )}
            <button
              type="button"
              className={`gd-button gd-button-collapsing${view === "analyzer" ? " gd-button-secondary" : " gd-button-primary"}`}
              onClick={() => onNavigate({ view: "analyzer" })}
              title="Analyse-Werkzeug"
              aria-label="Analyse-Werkzeug"
            >
              <ToolIcon />
              <span className="gd-button-label">Analyse-Werkzeug</span>
            </button>
          </div>
        </div>
      </header>

      <main id="portal-main" className="gd-portal-main">
        {children}
      </main>

      <footer className="gd-footer">
        <div className="gd-footer-inner">
          <nav className="gd-footer-nav" aria-label="Servicenavigation">
            <a href="#" onClick={(e) => e.preventDefault()}>
              Kontakt
            </a>
            <a href="#" onClick={(e) => e.preventDefault()}>
              Datenschutzerklärung
            </a>
            <a href="#" onClick={(e) => e.preventDefault()}>
              Nutzungshinweise
            </a>
            <a href="#" onClick={(e) => e.preventDefault()}>
              Barrierefreiheit
            </a>
            <a href="#" onClick={(e) => e.preventDefault()}>
              Impressum
            </a>
          </nav>
          <p className="gd-footer-note">
            Prototyp-Demonstrator auf Basis der GovData-Gestaltung. Inhalte und
            Qualitätsbewertung werden zur Laufzeit geladen und sind getrennte Ebenen.
            Kein offizielles Angebot von GovData bzw. der Bundesrepublik Deutschland.
          </p>
        </div>
      </footer>
    </div>
  );
}
