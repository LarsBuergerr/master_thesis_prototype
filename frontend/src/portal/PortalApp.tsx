// Orchestriert die Portal-Ansichten innerhalb des GovData-Rahmens.
//
// Ohne geladenen Datenbestand zeigt das Portal nichts als die Quellenauswahl —
// es hängt an keinem eingebauten Datensatz. Erst ein Katalog füllt es; eine
// Bewertung legt sich optional darüber (siehe portal/source.tsx). Den
// Ansichtszustand (list / detail / quality / analyzer) hält diese Komponente,
// bewusst ohne Router-Bibliothek.

import { useEffect, useState } from "react";
import { GovDataShell } from "./components/GovDataShell";
import { DatasetSearch } from "./components/DatasetSearch";
import { DatasetDetail } from "./components/DatasetDetail";
import { QualityDashboard } from "./components/QualityDashboard";
import { SourcePicker } from "./components/SourcePicker";
import { AnalyzerApp } from "../components/AnalyzerApp";
import { useIndicators } from "../hooks/useAnalysis";
import { PortalSourceProvider, usePortalSource } from "./source";
import type { PortalRoute } from "./route";

export function PortalApp() {
  return (
    <PortalSourceProvider>
      <PortalRoutes />
    </PortalSourceProvider>
  );
}

function PortalRoutes() {
  const { catalog } = usePortalSource();
  const [route, setRoute] = useState<PortalRoute>({ view: "list" });

  // Holt die Indikator-Registry samt Klartext-Guidance und aktualisiert damit
  // den Katalog (siehe lib/indicators). Ohne Backend bleibt der gebündelte
  // Abzug in Kraft — Ergebnisse sind dann trotzdem beschriftet.
  useIndicators();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [route]);

  // Katalogwechsel führt zurück in die Liste: eine Detailseite des vorherigen
  // Bestands gibt es im neuen nicht.
  useEffect(() => {
    setRoute({ view: "list" });
  }, [catalog]);

  if (!catalog) {
    return (
      <GovDataShell view="list" onNavigate={setRoute} hasCatalog={false}>
        <SourcePicker />
      </GovDataShell>
    );
  }

  return (
    <GovDataShell view={route.view} onNavigate={setRoute} hasCatalog>
      {route.view === "list" && <DatasetSearch onNavigate={setRoute} />}
      {route.view === "detail" && <DatasetDetail id={route.id} onNavigate={setRoute} />}
      {route.view === "quality" && <QualityDashboard />}
      {route.view === "analyzer" && <AnalyzerApp />}
    </GovDataShell>
  );
}
