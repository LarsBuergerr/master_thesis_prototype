# Frontend: Übernahme des GovData-Designs

Dieses Dokument beschreibt, wie das Analyzer-Frontend (`frontend/`) auf das
Corporate Design des offiziellen GovData-Portals umgestellt wurde, damit es
sich bei Bedarf mit minimalem Aufwand in GovData einbetten lässt. Es ergänzt
`docs/frontend_design_literatur.md`: Die dort hergeleiteten Prinzipien
(WCAG-Kontraste, Farbe nie als alleiniger Informationsträger,
Overview-first-Struktur) bleiben in Kraft — nur die **konkrete Farb- und
Typografie-Implementierung** folgt jetzt dem GovData-Styleguide statt der
projekteigenen Referenzpalette.

## 1. Quelle

- **Repo:** [GovDataOfficial/GovData-Frontend](https://github.com/GovDataOfficial/GovData-Frontend)
  (AGPL-3.0), das offizielle "GovData Template-Engine"-Frontend
  (Next.js-basiert), analysiert am 16.07.2026 (aktueller `main`-Stand).
- Maßgebliche Dateien: `webapp/src/css/_color-tokens.scss` (Figma-Styleguide-
  Tokens), `_variables.scss`, `_fonts.scss`, `_mixins.scss`, `_global.scss`,
  `components/_gd-button.scss`, `_gd-tag.scss`, `_gd-table.scss`,
  `_gd-alert.scss`, `_gd-design-box.scss`, `_gd-input.scss` sowie die
  Metadatenqualitäts-Seite
  `webapp/src/app/metadatenqualitaet/_components/Charts/common.ts`.

## 2. Libraries und Styles im GovData-Frontend

| Bereich | GovData verwendet | Übernahme hier |
|---|---|---|
| Framework | Next.js 16, React 19, TypeScript | Nicht übernommen — der Analyzer bleibt Vite + React (SPA gegen FastAPI). Für die Einbettung zählt das gerenderte Markup/CSS, nicht der Renderer. |
| CSS | **SCSS** (`sass` 1.77.6), `@import`-Kaskade `main.scss` | **Übernommen**: `frontend/src/css/main.scss` spiegelt Struktur und Importreihenfolge; `sass` 1.77.6 als Dev-Dependency (gleiche Version wie GovData, vermeidet die `@import`-Deprecation neuerer sass-Versionen). |
| Grid/Breakpoints | Bootstrap 5.3 (nur `bootstrap-grid` + Breakpoint-Mixins), Breakpoints 767/1024/1440 px | **Übernommen** (`bootstrap` ^5.3.6, Import von `bootstrap-grid` mit GovData-Breakpoint-Map). |
| Reset | `normalize.css` 8 | **Übernommen.** |
| Schrift | **Noto Sans** 300/400/700 via `@fontsource/noto-sans` | **Übernommen** (gleiche Fontsource-Pakete, gleiche Schnitte). |
| Farb-Tokens | `$clr-…`-SCSS-Variablen aus dem GOVDATA-Figma-Styleguide | **Wörtlich übernommen** in `frontend/src/css/_color-tokens.scss` (Namen + Hex unverändert). |
| Icons | Font Awesome 6 Free (+ eigene SVGs mit CSS-Filtern) | Nicht übernommen — die Status-Glyphen (✓ ◐ ✕ ! –) bleiben Unicode-Text (WCAG-1.4.1-Begründung in der Literatur-Doku); spart die Webfont-Abhängigkeit. |
| Charts | Chart.js **2.9.4** auf der Metadatenqualitäts-Seite | Nicht übernommen (Chart.js 2 ist EOL); Recharts bleibt, aber mit den **Chart-Farben der GovData-Metadatenqualitäts-Seite** (Magenta `rgb(128,0,75)` / `rgb(230,203,218)` = `$clr-metadaten-magenta-400/200`). |
| Sonstiges | i18next, OpenLayers, tippy.js, YASGUI, iron-session … | Portalfunktionen ohne Entsprechung im Analyzer — nicht relevant. |

Kein Dark Mode: GovData ist ein reines Hell-Design. Der bisherige
Dark-Mode samt Theme-Toggle wurde deshalb entfernt (`useTheme.tsx`,
`ThemeToggle.tsx`, `data-theme`-Mechanik); `color-scheme` steht auf `light`.

## 3. Übernommene Komponentenklassen (Einbettungs-Schnittstelle)

Das Markup verwendet jetzt GovDatas eigene Klassennamen. Beim Einbetten in
das Portal greifen dessen Stylesheets also direkt; standalone liefert die
lokale SCSS-Kaskade pixelgleiche Regeln.

| GovData-Klasse | Verwendung im Analyzer |
|---|---|
| `design-box design-box-padding` | alle Karten/Panels (vorher `.panel`) |
| `gd-button gd-button-primary` / `-secondary` | "Analyse starten" / "Dateien wählen" |
| `gd-tag` + Statusmodifikator | Status-Chips; `green`/`yellow`-Muster des Portals um `pass/partial/fail/error/not_applicable/patch/recommendation` erweitert |
| `gd-table`, `gd-table-head`, `gd-table-wrapper` | Indikator-Tabellen |
| `alert alert-info` / `alert gd-alert-danger` | Leerzustand / Fehlermeldungen |
| `gd-input` | Konfigurations-Formular (Labels fett, 40-px-Felder, Grey-500-Rahmen) |
| Fokus-Stil | 3 px Outline `#0073a8`, Offset 2 px (GovData `outline-base()`-Mixin) |

Nur die Layout-Hülle (`.app`-Grid, Fortschrittsbalken, Diff-Ansicht,
Score-Grade) ist anwendungsspezifisch und liegt gesammelt in
`frontend/src/css/components/_analyzer.scss` — ebenfalls ausschließlich auf
GovData-Tokens aufgebaut.

## 4. Status-Palette auf GovData-Tokens (berechnet, nicht geschätzt)

GovData kennzeichnet Tags nach dem Muster *helle 200er-Füllung + 500er-Text
+ 1-px-Rahmen* (`.gd-tag.green`/`.yellow`). Die fünf Analyzer-Status folgen
diesem Muster; die WCAG-Kontraste (Formel wie in der Literatur-Doku,
Node-Skript) wurden nachgerechnet:

### 4.1 Tags (Text auf Füllung, Ziel ≥ 4.5∶1, WCAG 1.4.3)

| Status | Füllung | Text | Kontrast |
|---|---|---|---|
| pass | `#d9f7f1` (success-200) | `#206d5c` (success-500) | 5.44∶1 |
| partial | `#fdfacc` (warning-200) | `#7b7301` (warning-500) | 4.59∶1 |
| fail | `#ffdada` (error-200) | `#b33030` (error-500) | 4.82∶1 |
| error | `#3d3d3d` (media-grey-500, Muster `.gd-tag.black`) | `#ffffff` | 10.86∶1 |
| not_applicable | `#e3e8ef` (grey-200) | `#3d4f66` (grey-600) | 6.80∶1 |
| Patch | `#e6cbda` (metadaten-magenta-200) | `#80004b` (metadaten-magenta-400) | 6.89∶1 |
| Empfehlung | `#f3f6fb` (grey-100) | `#3d4f66` (grey-600) | 7.73∶1 |

Jeder Status trägt weiterhin zusätzlich ein Icon-Glyph (WCAG 1.4.1).

### 4.2 Chart-Flächen (satte Töne, Ziel ≥ 3∶1 gegen Weiß, WCAG 1.4.11)

| Rolle | Farbe | Kontrast vs. `#fff` |
|---|---|---|
| pass | `#2d9880` (success-400) | 3.55∶1 |
| partial | `#938a01` (warning-400) | 3.57∶1 |
| fail | `#e63e3e` (error-400) | 4.10∶1 |
| error | `#3d3d3d` | 10.86∶1 |
| not_applicable | `#5d728b` (grey-500; grey-400 fiele mit 2.52∶1 durch) | 4.95∶1 |
| Radar-Akzent | `#80004b` (MQA-Magenta, wie GovData-Metadatenqualitäts-Charts) | 10.40∶1 |
| Score-Grade-Text (A/B, C, D/F) | `#206d5c` / `#7b7301` / `#b33030` | 6.17 / 4.89 / 6.21∶1 |

### 4.3 Grundflächen und Text

| Rolle | Wert | Kontrast |
|---|---|---|
| Seite | `#f5f5f5` (`$clr-body-background`) | — |
| Karte | `#ffffff` (design-box) | — |
| Fließtext | `#192738` (grey-800) | 15.12∶1 auf Weiß |
| Sekundärtext (`.muted`) | `#3d4f66` (grey-600) | 8.37∶1 |
| Subtiltext (`.subtle`) | `#5d728b` (grey-500) | 4.95∶1 |
| Primär-Button | Weiß auf `#0073a8` (primary-400) | 5.23∶1 |
| Info-Alert | `#0073a8` auf `#e6f1f6` | 4.55∶1 |
| Danger-Alert | `#b50303` auf `#fee5e2` (GovData-Werte) | 5.88∶1 |

Damit erfüllen alle übernommenen Paarungen die AA-Ziele — die
GovData-Palette ersetzt die bisherige Referenzpalette ohne
Kontrast-Regression.

## 5. Geänderte Dateien

**Neu:** `frontend/src/css/` (main.scss, _function/_color-tokens/_mixins/
_variables/_fonts/_global.scss, components/_gd-design-box/_gd-button/
_gd-tag/_gd-table/_gd-alert/_gd-input/_analyzer.scss).

**Entfernt:** `frontend/src/styles.css`, `frontend/src/hooks/useTheme.tsx`,
`frontend/src/components/ThemeToggle.tsx` (Dark-Mode/Theming — GovData ist
hell-only).

**Geändert:** `package.json` (+`bootstrap`, `@fontsource/noto-sans`,
`normalize.css`, `sass`), `index.html` (`color-scheme: light`), `main.tsx`
(SCSS-Import statt ThemeProvider), `lib/theme.ts` (statische
GovData-Chart-Palette), `App.tsx`, `UploadPanel.tsx`, `ConfigPanel.tsx`,
`JobProgress.tsx`, `results/*` (GovData-Klassennamen, statische
Chart-Farben).

**Verifikation:** `npm run build` (inkl. `tsc -b`) fehlerfrei; gerenderte
Seite per Headless-Chromium gegen den Produktiv-Build geprüft
(GovData-Typografie, -Buttons, -Alerts, -Boxen sichtbar korrekt).
