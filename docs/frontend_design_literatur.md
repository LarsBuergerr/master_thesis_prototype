# Frontend-Redesign: Literaturgrundlage und Umsetzung

Dieses Dokument begründet das Redesign des Analyzer-Frontends
(`frontend/`) mit publizierter Literatur zu Dashboard-/UI-Design,
Wahrnehmung, Farbtheorie und Barrierefreiheit, sowie mit den vom Betreuer
genannten W3C-Validatoren als technischer Qualitätsreferenz. Ziel war ein
Design, das sich in der Verteidigung mit konkreten Quellen und (wo möglich)
berechneten/gemessenen Nachweisen statt mit Geschmacksurteilen begründen
lässt ("defendable").

Methodisch folgt der Farb-Teil einem im Rahmen dieser Arbeit verwendeten,
literatur-abgeleiteten Verfahren für Dashboard-Farbgebung (Kategorie 1
unten), das die Prinzipien von Brewer, Okabe/Ito, Ware und WCAG in ein
prüfbares Sechs-Kriterien-Schema überführt (u. a. OKLCH-Helligkeitsband,
Chroma-Untergrenze, CVD-Separation nach Machado–Oliveira–Fernandes 2009,
Kontrast). Alle konkreten Farbwerte wurden gegen dieses Schema **berechnet**,
nicht nach Augenmaß gewählt (siehe Abschnitt "Berechnete
Kontrast-Nachweise").

---

## 1. Literatur

### 1.1 Dashboard-Design

- **Few, S. (2006).** *Information Dashboard Design: The Effective Visual
  Communication of Data.* O'Reilly. — Kernprinzipien: Einfachheit vor
  Dekoration ("display data as clearly and simply as possible"),
  Ein-Bildschirm-Prinzip ("simultaneity of vision" — alles Wichtige auf
  einen Blick, ohne Scrollen zwischen Kontexten), Priorisierung nach
  Informationswert, und dass gute Dashboard-Gestaltung erlernte
  Wahrnehmungsprinzipien nutzt statt Dekoration.
  [Übersichtsfolien](https://blogs.ischool.berkeley.edu/i247s12/files/2012/01/Dashboard-Design-Overview-Presentation.pdf) ·
  [Rezension](https://www.uxmatters.com/mt/archives/2007/04/book-review-information-dashboard-design.php)

- **Shneiderman, B. (1996).** *The Eyes Have It: A Task by Data Type
  Taxonomy for Information Visualizations.* Proc. IEEE Symposium on Visual
  Languages. — Das "Visual Information-Seeking Mantra": *Overview first,
  zoom and filter, then details-on-demand.* Strukturiert, wie eine
  Oberfläche vom Gesamtbild zur Detailinformation führt.
  [PDF](https://www.cs.umd.edu/~ben/papers/Shneiderman1996eyes.pdf)

- **Nielsen Norman Group — "Dashboards: Making Charts and Graphs Easier to
  Understand".** Preattentive-Verarbeitung (Farbe/Form vor bewusster
  Aufmerksamkeit), Gestalt-Prinzip der Ähnlichkeit für Gruppierung, sowie
  eigenes Eyetracking zum F-förmigen Scan-Muster (horizontaler Sweep oben,
  kürzerer Sweep darunter, vertikaler Scan links).
  [Artikel](https://www.nngroup.com/articles/dashboards-preattentive/)

- **Nielsen, J. & Molich, R. (1990); Nielsen, J. (1994).** *10 Usability
  Heuristics for User Interface Design.* — insbes. "Recognition rather than
  recall", "Consistency and standards", "Visibility of system status",
  "Aesthetic and minimalist design", "Error prevention".
  [NN/G-Artikel](https://www.nngroup.com/articles/ten-usability-heuristics/)

### 1.2 Wahrnehmung und Gestaltgesetze

- **Ware, C. (2012/2021).** *Information Visualization: Perception for
  Design* (3./4. Aufl.). Morgan Kaufmann. — Präattentive Merkmale (Farbe,
  Form, Position werden < 10 ms erfasst, vor bewusster Aufmerksamkeit) und
  die Gestaltgesetze (Nähe, Ähnlichkeit, Kontinuität, Geschlossenheit,
  relative Größe) als zwei komplementäre Erklärungsmodelle dafür, wie
  visuelle Gruppierung gelesen wird.

### 1.3 Farbe

- **Tufte, E. (1983/2001).** *The Visual Display of Quantitative
  Information.* Graphics Press. — Daten-Tinten-Verhältnis (data-ink ratio)
  und der Begriff *Chartjunk* (Tinte, die dem Betrachter nichts Neues
  mitteilt): Grafiken sollen auf das Nötige reduziert werden.

- **Brewer, C. A.** *ColorBrewer* (mit M. Harrower, Penn State, seit 2002).
  — Systematik für Farbskalen nach Datentyp: **sequenziell** (geordnete
  Werte, ein Farbton hell→dunkel), **divergierend** (zwei Farbtöne mit
  neutralem Mittelpunkt für Werte mit Vorzeichen/Referenzpunkt),
  **qualitativ** (nominale Kategorien, Unterscheidung primär über
  Farbton). Inklusive farbenblind-sicherer Voreinstellungen.
  [colorbrewer2.org](https://colorbrewer2.org/)

- **Okabe, M. & Ito, K. (2008).** *Color Universal Design (CUD): How to
  make figures and presentations that are friendly to Colorblind people.*
  — 8-Farben-Palette, die für die häufigsten Formen von
  Farbsinnstörungen (Protanopie/Deuteranopie) unterscheidbar bleibt; De-facto-
  Standard für farbenblind-sichere kategoriale Paletten in wissenschaftlichen
  Abbildungen.

### 1.4 Barrierefreiheit (W3C WCAG)

- **W3C WAI — WCAG 2.2, Success Criterion 1.4.3 "Contrast (Minimum)".**
  Kontrastverhältnis Text/Hintergrund ≥ 4.5∶1 (normaler Text), ≥ 3∶1 für
  großen/fetten Text (≥ 18pt bzw. ≥ 14pt fett).
  [Understanding SC 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum)

- **W3C WAI — WCAG 2.2, Success Criterion 1.4.1 "Use of Color".**
  Farbe darf keine alleinige Informationsquelle sein — es braucht ein
  zusätzliches, nicht-farbliches Unterscheidungsmerkmal (Symbol, Text,
  Muster).
  [Understanding SC 1.4.1](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)

- **WCAG 2.4.1 "Bypass Blocks".** Tastatur-Nutzer benötigen einen Weg, sich
  wiederholende Navigationsblöcke zu überspringen (Skip-Link).

### 1.5 Technische Konformitäts-Referenz (vom Betreuer genannt)

- **W3C Markup Validation Service / Nu Html Checker**
  (`validator.w3.org/nu/`) — der aktuelle, WHATWG-Living-Standard-basierte
  HTML5-Konformitätsprüfer des W3C (Nachfolger des klassischen
  DTD-basierten Markup-Validators).
  [About the Nu Html Checker](https://validator.github.io/validator/site/nu-about.html)

- **W3C CSS Validation Service** (`jigsaw.w3.org/css-validator/`) — prüft
  Stylesheets gegen die CSS-Spezifikationen.
  [Jigsaw CSS Validator](https://jigsaw.w3.org/css-validator/)

---

## 2. Abgeleitete Design-Entscheidungen

| Literatur | Entscheidung im Frontend |
|---|---|
| Few (Ein-Bildschirm-Prinzip, Priorisierung) | Kopfzeile mit Titel + Theme-Umschalter global sichtbar; Gesamtscore/Grade/Radar ("Overview") stehen vor den Dimensions-Tabellen; keine dekorativen Elemente ohne Dateninhalt hinzugefügt. |
| Shneiderman (Overview → Zoom/Filter → Details-on-Demand) | Bestehende `<details>`-Struktur pro Dimension (Zoom/Filter) bleibt erhalten und wurde nicht durch etwas Komplexeres ersetzt; neu: Remediation-Zeilen unter jedem Indikator sind das nächste Detail-Level (Details-on-Demand) statt alles permanent einzublenden. |
| NN/G (Preattentive Processing, Gestalt-Ähnlichkeit, F-Muster) | Status wird konsequent über **Farbe + Form/Icon + Text** kodiert (s. u.), nie über Farbe allein; Kopfzeile oben, wichtigste Kennzahl (Gesamtscore) links oben im Hauptbereich — folgt dem F-Scan-Muster. |
| Nielsen-Heuristiken | "Visibility of system status": Fortschrittsbalken/Job-Status unverändert prominent. "Consistency": ein einziges Token-System (`--pass`/`--partial`/... ) ersetzt die bisher an mehreren Stellen verstreuten Hex-Werte. "Aesthetic and minimalist design": keine neuen Dekorationselemente, nur Korrektur bestehender Kontrast-/Konsistenzprobleme. |
| Ware / Gestalt (Nähe, Ähnlichkeit) | Zusammengehörige Kennzahlen bleiben in `.panel`-Gruppen mit konsistentem Abstand (neues 4-px-Spacing-Raster `--space-1`…`--space-6`) statt frei platzierter Inline-Styles. |
| Tufte (Data-Ink, Chartjunk) | Keine zusätzlichen Rahmen/Schatten/Farbverläufe eingeführt; Grafiken (Recharts) behalten reduzierte Achsen/Gitterlinien in gedämpfter Tinte (`--gridline`, `--text-subtle`). |
| Brewer / Okabe-Ito / WCAG 1.4.1 | **Statusfarben sind eine fixe, nie themenabhängige 5er-Palette** (pass/partial/fail/error/not_applicable), analog zu Brewers "qualitativ, primär über Farbton unterscheidbar"; jeder Status-Chip trägt zusätzlich ein Icon-Glyph (✓ / ◐ / ✕ / ! / –) **und** Text — nie Farbe allein (WCAG 1.4.1). |
| WCAG 1.4.3 (Kontrast) | Alte Chip-Gestaltung (farbiger Text auf 15 % transparentem Farbton) wurde **gemessen** (s. u.), nicht neu erfunden nach Augenmaß — sie unterschritt in praktisch jedem Fall 4.5∶1. Neue Chips: satte Füllfarbe + pro Status berechnete Textfarbe (Schwarz oder Weiß), die 4.5∶1 einhält. |
| WCAG 2.4.1 (Bypass Blocks) | Skip-Link "Zum Hauptinhalt springen" vor der Kopfzeile ergänzt; `<main id="main-content">` als Sprungziel. |
| W3C Nu Checker / CSS Validator | Gebautes `index.html` und die kompilierte CSS-Datei wurden real gegen die W3C-Dienste geprüft (Ergebnisse unten), nicht nur informell "sollte gültig sein" behauptet. |
| Semantik allgemein (W3C HTML5) | `<table>` bekommt `<caption>` + `<th scope="col">`/`<th scope="row">` statt reiner `<td>`-Zellen; Landmark-Elemente `<header>`/`<main>`/`<aside aria-label>` statt generischer `<div>`s. |

---

## 3. Farbpalette (berechnet, nicht geschätzt)

Alle Werte stammen aus einer im Projekt bereits vorhandenen, gegen die
Brewer/Okabe-Ito/WCAG-Kriterien validierten Referenzpalette (Statusfarben,
Chart-Grundfarben, Kontrast-Stufen) und wurden für dieses Frontend
zusätzlich **numerisch gegen die konkreten Hintergründe dieser App**
nachgerechnet (Node-Skript mit dem WCAG-Kontrastformel-Export der
Palette-Validierung).

### 3.1 Warum die alte Chip-Gestaltung ersetzt wurde

Alte Regel: farbiger Text auf 15 %-transparentem Hintergrund derselben
Farbe (`background: rgba(62,207,142,.15); color: var(--pass)`). Gemessene
Text/Hintergrund-Kontraste (WCAG-Formel, gerundet):

| Status | Hell, 15 % Deckkraft | Dunkel, 15 % Deckkraft | WCAG-AA-Ziel |
|---|---|---|---|
| pass | 2.76∶1 | 4.29∶1 | 4.5∶1 |
| partial | 1.64∶1 | 6.96∶1 | 4.5∶1 |
| fail | 3.77∶1 | 3.20∶1 | 4.5∶1 |
| error | 2.25∶1 | 5.18∶1 | 4.5∶1 |
| not_applicable | 2.99∶1 | 3.99∶1 | 4.5∶1 |

Im Hellmodus unterschreitet **jeder** Status das AA-Minimum, im Dunkelmodus
zwei von fünf. Das bestätigt messtechnisch, dass das alte (nur dunkel
gestaltete) Farbschema für einen Hellmodus so nicht tragfähig war.

### 3.2 Neue Chip-Gestaltung: satte Füllfarbe + berechnete Textfarbe

| Status | Füllfarbe | Textfarbe | Kontrast |
|---|---|---|---|
| pass | `#0ca30c` | Schwarz `#0b0b0b` | 5.87∶1 |
| partial | `#fab219` | Schwarz `#0b0b0b` | 10.73∶1 |
| fail | `#d03b3b` | Weiß `#ffffff` | 4.80∶1 |
| error | `#ec835a` | Schwarz `#0b0b0b` | 7.46∶1 |
| not_applicable | `#898781` | Schwarz `#0b0b0b` | 5.48∶1 |

Alle fünf liegen über der 4.5∶1-Schwelle aus WCAG 1.4.3. Zusätzlich trägt
jeder Chip ein Icon-Glyph (WCAG 1.4.1). Diese Statusfarben sind bewusst
**identisch in Hell- und Dunkelmodus** — Statusbedeutung soll sich nicht mit
dem Theme verschieben.

### 3.3 UI-Akzentfarbe (Buttons/Fokus)

Der reine Akzentton (`#2a78d6` hell / `#3987e5` dunkel) liegt mit weißer
Schrift bei 4.42∶1 bzw. 3.64∶1 — im Dunkelmodus unter dem AA-Ziel für
normalen Fließtext. Für ausfüllte Buttons wird deshalb ein einzelner,
themenunabhängiger, dunklerer Blauton aus derselben Farbfamilie verwendet
(`--accent-solid: #256abf`, 5.39∶1 mit Weiß) — funktional dieselbe Farbe,
nur so weit abgestuft, dass der Kontrast in **beiden** Modi sicher hält,
statt zwei separate, ungeprüfte Buttonfarben zu pflegen.

### 3.4 Chart-/Oberflächenfarben

| Rolle | Hell | Dunkel |
|---|---|---|
| Seite | `#f9f9f7` | `#0d0d0d` |
| Panel/Karte | `#fcfcfb` | `#1a1a19` |
| Panel (Eingabefelder) | `#f1f0ec` | `#222221` |
| Primärer Text | `#0b0b0b` (18.67∶1 auf Seite) | `#ffffff` (19.44∶1 auf Seite) |
| Sekundärer Text | `#52514e` (7.53∶1) | `#c3c2b7` (10.85∶1) |
| Gitterlinie (nur Charts) | `#e1e0d9` | `#2c2c2a` |

---

## 4. Reale W3C-Validierungsergebnisse

Ausgeführt gegen den produktiven Build (`npm run build`) am 15.07.2026.

### 4.1 Nu Html Checker (`validator.w3.org/nu/?out=json`)

Geprüft: `dist/index.html` (statisches Grundgerüst, das React zur Laufzeit
befüllt).

**Ergebnis: 0 Fehler, 0 Warnungen.** Es wurden lediglich 4
Info-Hinweise ausgegeben ("Trailing slash on void elements has no effect")
zu den selbstschließenden `<meta ... />`-Tags — das ist gültiges HTML5, der
Hinweis ist rein stilistisch (XHTML-Gewohnheit) und keine Konformitäts-
verletzung.

### 4.2 CSS Validator (`jigsaw.w3.org/css-validator/validator`)

Geprüft: die kompilierte, gebündelte CSS-Datei aus `dist/assets/`.

```
"validity": true,
"result": { "errorcount": 0, "warningcount": 1 }
```

Die einzige Warnung bemängelt `system-ui, -apple-system` in der
Font-Stack-Deklaration als "vendor extension" (kein Fehler) — dieser
System-Font-Stack ist Industriestandard (auch von der genutzten
Chart-Design-Referenz empfohlen) und bewusst beibehalten.

### 4.3 Bekannte Grenze dieser Prüfung

Der Nu Checker validiert das **statische** HTML-Grundgerüst; die von React
zur Laufzeit erzeugte Dashboard-Markup (Tabellen, ARIA-Attribute,
Remediation-Ansicht) ist im Server-Response nicht enthalten, da diese
Anwendung als Single-Page-App rein clientseitig rendert und in dieser
Umgebung kein Headless-Browser zur Verfügung stand, um den tatsächlich
gerenderten DOM abzugreifen. Diese Teile wurden stattdessen manuell gegen
dieselben Regeln geprüft (`<caption>` als erstes Kind von `<table>`,
`scope="col"`/`scope="row"` auf `<th>`, gültige ARIA-Attribute wie
`aria-pressed`, `aria-hidden`, `role="alert"`). Eine vollständige
Browser-DOM-Validierung wäre ein sinnvoller nächster Schritt (z. B. mit
Playwright: Seite rendern, `document.documentElement.outerHTML` abgreifen,
gegen den Nu Checker schicken).

---

## 5. Änderungsliste

**Backend/Schema:** keine Änderungen in diesem Schritt.

**Neu:**
- `frontend/src/lib/theme.ts` — Theme-Tokens (hell/dunkel) und die fixe
  Status-Palette als einzige Quelle für Recharts (SVG braucht echte Hex-
  Werte, keine CSS-Variablen).
- `frontend/src/hooks/useTheme.tsx` — `ThemeProvider`/`useTheme()`; folgt
  System-Voreinstellung (`prefers-color-scheme`) bis der Nutzer explizit
  umschaltet, danach persistiert in `localStorage`.
- `frontend/src/components/ThemeToggle.tsx` — Umschalt-Button mit
  `aria-pressed`/`aria-label`.

**Geändert:**
- `frontend/src/styles.css` — vollständig neu aufgebautes Token-System
  (hell als Standard, dunkel per Media-Query **und** `data-theme`-Override,
  siehe § 2); Chips auf satte Füllfarbe + Icon umgestellt; 4-px-Spacing-
  Raster (`--space-1`…`--space-6`); Skip-Link- und Fokus-Stile ergänzt;
  `<caption>`-Stil ergänzt; `.error-box` auf Rand-Akzent statt
  kontrastschwachem Farbton umgestellt (§ 3.1).
- `frontend/index.html` — `<meta name="color-scheme" content="light dark">`
  und `<meta name="description">` ergänzt.
- `frontend/src/main.tsx` — App in `<ThemeProvider>` gewrappt.
- `frontend/src/App.tsx` — Skip-Link, `<header>`-Landmark mit
  `ThemeToggle`, `<aside aria-label="Konfiguration">`, `<main
  id="main-content">`, `role="alert"` auf Fehlermeldungen.
- `frontend/src/lib/status.ts` — Farblogik nach `lib/theme.ts` ausgelagert;
  neue `statusIcon()`-Funktion für die Icon+Text-Kodierung.
- `frontend/src/components/results/DimensionPanel.tsx` — `<caption>`,
  `scope="col"`/`scope="row"`, Status-Chip mit Icon.
- `frontend/src/components/results/DimensionRadar.tsx`,
  `IndicatorBarChart.tsx`, `BatchComparison.tsx` — hartkodierte Hex-Farben
  durch `useTheme().colors` ersetzt (Charts folgen jetzt dem aktiven
  Theme).
- `frontend/src/components/results/OverallScoreCard.tsx` — unverändert in
  der Logik, profitiert automatisch von der neuen `gradeColor()`.

**Nicht geändert (bewusst):** die grundsätzliche Informationsarchitektur
(Sidebar = Konfiguration/Filter, Hauptbereich = Overview + aufklappbare
Details) blieb erhalten, da sie bereits dem Shneiderman-Muster entspricht —
Few's "keine unnötige Dekoration" spricht ausdrücklich gegen ein Redesign
um des Redesigns willen.
