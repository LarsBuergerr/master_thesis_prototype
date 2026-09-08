// Leichtgewichtiges Ansichts-Modell für das Portal — bewusst ohne Router-
// Bibliothek (keine zusätzliche Abhängigkeit). Der Zustand liegt in PortalApp.

export type PortalView = "list" | "detail" | "quality" | "analyzer";

export type PortalRoute =
  | { view: "list" }
  | { view: "detail"; id: string }
  | { view: "quality" }
  | { view: "analyzer" };

export type Navigate = (route: PortalRoute) => void;
