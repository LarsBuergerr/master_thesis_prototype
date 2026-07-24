// Orchestriert die Portal-Ansichten innerhalb des GovData-Rahmens. Hält den
// Ansichtszustand (list / detail / quality / analyzer) und scrollt bei jedem
// Wechsel nach oben. Bewusst ohne Router-Bibliothek.

import { useEffect, useState } from "react";
import { GovDataShell } from "./components/GovDataShell";
import { DatasetSearch } from "./components/DatasetSearch";
import { DatasetDetail } from "./components/DatasetDetail";
import { QualityDashboard } from "./components/QualityDashboard";
import { AnalyzerApp } from "../components/AnalyzerApp";
import { useIndicators } from "../hooks/useAnalysis";
import type { PortalRoute } from "./route";

export function PortalApp() {
  const [route, setRoute] = useState<PortalRoute>({ view: "list" });

  // Holt die Indikator-Registry samt Klartext-Guidance und aktualisiert damit
  // den Katalog (siehe lib/indicators). Ohne Backend bleibt der gebündelte
  // Abzug in Kraft — die Seite funktioniert dann unverändert.
  useIndicators();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [route]);

  return (
    <GovDataShell view={route.view} onNavigate={setRoute}>
      {route.view === "list" && <DatasetSearch onNavigate={setRoute} />}
      {route.view === "detail" && <DatasetDetail id={route.id} onNavigate={setRoute} />}
      {route.view === "quality" && <QualityDashboard />}
      {route.view === "analyzer" && <AnalyzerApp />}
    </GovDataShell>
  );
}
