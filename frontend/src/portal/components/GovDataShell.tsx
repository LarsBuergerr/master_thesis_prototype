// GovData-Rahmen (Chrome) um alle Portal-Ansichten: Bund-Leiste mit
// Flaggen-Signet, Kopfzeile mit Logo + Hauptnavigation, Fußzeile. Aufbau,
// Beschriftungen und Farbwelt orientieren sich am offiziellen GovData-Portal
// (govdata.de). Kein Dark-Mode/keine Umschalter — GovData ist ein reines
// Hell-Design.

import type { ReactNode } from "react";
import type { Navigate, PortalView } from "../route";

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
  children: ReactNode;
}

export function GovDataShell({ view, onNavigate, children }: Props) {
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
            <span className="gd-logo-mark">
              <span className="gd-logo-gov">Gov</span>
              <span className="gd-logo-data">Data</span>
            </span>
            <span className="gd-logo-sub">Das Datenportal für Deutschland</span>
          </button>

          <nav className="gd-nav" aria-label="Hauptnavigation">
            {NAV.map((item, idx) => {
              const active = !item.inert && item.view === view;
              return (
                <button
                  key={`${item.label}-${idx}`}
                  type="button"
                  className={`gd-nav-link button-reset${active ? " active" : ""}`}
                  aria-current={active ? "page" : undefined}
                  onClick={() =>
                    !item.inert &&
                    onNavigate(item.view === "quality" ? { view: "quality" } : { view: "list" })
                  }
                >
                  {item.label}
                </button>
              );
            })}
          </nav>

          <div className="gd-header-actions">
            <button
              type="button"
              className={`gd-button${view === "analyzer" ? " gd-button-secondary" : " gd-button-primary"}`}
              onClick={() => onNavigate({ view: "analyzer" })}
            >
              Analyse-Werkzeug
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
            Prototyp-Demonstrator auf Basis der GovData-Gestaltung. Datengrundlage:
            Evaluationsstichprobe <code>sample_2026-06-25</code> (n&nbsp;=&nbsp;50).
            Kein offizielles Angebot von GovData bzw. der Bundesrepublik Deutschland.
          </p>
        </div>
      </footer>
    </div>
  );
}
