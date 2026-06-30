# Modellverbesserungsplan — Zusammenfassung aller offenen Punkte

Stand: 2026-06-30  
Grundlage: Analyse des DCAT-AP.de Konventionenhandbuches v2.0 und der
Handreichung zur Metadatenqualität (oc.bydata, 12/2025)

---

## 1. Code-Fixes

### 1.1 Bereits korrekt implementiert (keine Fixes nötig)

Nach Lektüre des tatsächlichen Codes sind zwei der ursprünglich als "kritisch"
markierten Fixes bereits vollständig implementiert:

**`reuse_contact`** (`reusability.py:506`) — bereits über Konvention 01 hinaus:
Prüft `vcard:hasEmail` (mailto: mit Regex-Validierung, 0.25 Punkte),
`vcard:hasURL` (http/https-Validierung, 0.25 Punkte), `vcard:Organization`-Typing
(0.25 Punkte) + Bonus-Felder (fn, hasTelephone, etc., bis 0.25 Punkte).
PASS ≥ 0.85, PARTIAL ≥ 0.5. Erfüllt und übertrifft Konvention 01.

**`reuse_license`** (`reusability.py:91`) — prüft bereits DCAT-AP.de-Vokabular:
Vergleicht gegen `OPEN_LICENSE_URIS` (PASS, score=1.0) und
`RESTRICTED_LICENSE_URIS` (PARTIAL, score=0.5) aus dem geladenen
licenses.rdf-Vokabular. URIs außerhalb des Vokabulars = FAIL score=0.0.
Erfüllt Konvention 32 korrekt.

---

### 1.2 `find_keywords_count` → Threshold-Logik-Bug beheben

**Problem:** Die aktuelle Logik hat einen Fehler der dazu führt dass
**3 Keywords = FAIL** obwohl die Handreichung "mindestens 3" verlangt.

Ursache: PASS-Bedingung ist `MIN_KEYWORDS < count` (also `3 < count`, d.h.
count > 3). Damit bekommt `count == 3` weder PASS noch PARTIAL (da PARTIAL
`count in [2, 8]` oder `11 <= count <= 15` prüft). Zusätzlich ergibt
`count == 8` fälschlicherweise PARTIAL obwohl 8 im optimalen Band liegt
(`MAX_KEYWORDS - 2 = 8` ist in der PARTIAL-Bedingung).

**Fix:**
- PASS = `count >= 3 AND count <= MAX_KEYWORDS` (d.h. 3–10)
- PARTIAL = `count in [1, 2]` ODER `count > MAX_KEYWORDS` (zu wenige oder zu viele)
- FAIL = 0 Keywords

**Quelle:** Handreichung zur Metadatenqualität, oc.bydata 12/2025, S. 14:
"Verwenden Sie mindestens drei relevante Schlagwörter"

---

## 2. Neue Indikatoren (Lücken schließen)

### 2.1 `acc_distribution_status` — `adms:status` auf Distributionen

**Begründung:** Konvention 22 (MUSS): Distributionen müssen `adms:status`
"Completed", "Deprecated" oder "Withdrawn" transportieren. Konvention 23
(MUSS): Diese müssen in DCAT-AP.de-konformen Portalen angezeigt werden.
Aktuell kein Indikator dafür — das ist eine klare Lücke bei MUSS-Anforderungen.

**Design:**
- PASS = alle Distributionen haben einen validen `adms:status` Wert
- PARTIAL = mindestens eine Distribution hat einen validen Status
- FAIL = kein `adms:status` auf Distributionen

**Klasse:** C (kein MQA-Pendant)  
**Quelle:** DCAT-AP.de Konventionenhandbuch v2.0, Konventionen 22–24 (MUSS)

---

### 2.2 `find_identifier` — `dct:identifier` Pflichtfeld

**Begründung:** Die Handreichung zur Metadatenqualität listet `dct:identifier`
als Pflichtfeld für Datensätze. Das Konventionenhandbuch (Konventionen 25/26)
beschreibt es als zentrales Merkmal für Duplikaterkennung im GovData-Verbund.
Aktuell kein dedizierter Indikator.

**Design:**
- PASS = `dct:identifier` vorhanden, URI-Form
- PARTIAL = `dct:identifier` vorhanden als Literal (nicht URI)
- FAIL = nicht vorhanden

**Klasse:** C (MQA prüft identifier implizit via Dublettenlogik, nicht als
eigenständige Qualitätsmetrik)  
**Quelle:** Handreichung zur Metadatenqualität S. 4; Konventionenhandbuch
Konventionen 25/26

---

### 2.3 `reuse_language` — `dct:language` auf Distribution

**Begründung:** Die Handreichung listet `dct:language` als empfohlenes Feld
für Distributionen. Wichtig für EU-weite Auffindbarkeit über data.europa.eu
und für die Nachnutzung durch nicht-deutschsprachige Nutzer. Aktuell nicht
abgedeckt.

**Design:**
- PASS = mindestens eine Distribution hat `dct:language`
- FAIL = kein `dct:language` auf Distributionen

**Klasse:** C  
**Quelle:** Handreichung zur Metadatenqualität S. 7 (empfohlenes Feld)

---

## 3. Expressiveness-Dimension: Prompt-Verbesserungen

Der LLM-Prompt ist aktuell zu generisch. Beide Dokumente liefern sehr
konkrete, normativ belegte Qualitätskriterien die in den Prompt eingearbeitet
werden müssen. Das macht den innovativen Teil der Thesis normativ begründbar.

### 3.1 `expr_title_quality` — Prompt konkretisieren

Ergänze in System-Prompt / Criterion-Description:

```
Title quality criteria (DCAT-AP.de Handreichung / Konventionenhandbuch 1.7):
GOOD:
- Specific, concise, includes temporal context (year/period) and/or geographic
  scope where relevant ("Einwohnerzahlen Stadt XY 2025")
- Distinguishable from similar datasets of other publishers

BAD — mark down for:
- Overly generic without place/year context ("Einwohnerzahlen")
- Methodology or explanations in title (belongs in description)
- Unexplained technical abbreviations or codes as primary identifier
- Redundant with publisher name (publisher is shown separately)

Convention 1.7: "Keine Metadaten, insbesondere keinen Zeit- und Ortsbezug
[im Titel], wenn diese in den dafür vorgesehenen Metadatenfeldern gemacht
werden KÖNNEN — AUSNAHME: Wenn es dem übergreifenden Verständnis dient."
→ Time/place IN the title is acceptable and often helpful for data series.
```

**Quelle:** DCAT-AP.de Konventionenhandbuch v2.0 Kap. 1.7;
Handreichung zur Metadatenqualität S. 9–10

---

### 3.2 `expr_description_quality` — Vollständigkeitskriterien ergänzen

Ergänze konkrete Prüffragen aus der Handreichung (S. 11):

```
A complete description should answer these questions (Handreichung oc.bydata):
1. Was ist enthalten? — What data fields and content does the dataset contain?
2. Wie ist es strukturiert? — Format, table structure, categories, encoding
3. Wie und wieso wurden die Daten erhoben? — Method, source, sample size
4. Weshalb / wozu? — Purpose, what use case does it serve
5. Besonderheiten? — Cutoff date (Stichtag), provisional/estimated data,
   quality disclaimers, KI-Unterstützung, links to documentation

For distributions specifically:
- Delimiter and character encoding for CSV files
- Field descriptions if non-obvious column names

Mark DOWN:
- Descriptions that merely restate the title
- Descriptions with HTML/Markdown formatting (renders as raw text in GovData)
- Very short descriptions without structural information
```

**Quelle:** Handreichung zur Metadatenqualität S. 11–13;
DCAT-AP.de Konventionenhandbuch v2.0 Kap. 3.4 (Formatierung)

---

### 3.3 `expr_keyword_quality` — Negativmuster konkretisieren

Ergänze konkrete Qualitätsregeln aus der Handreichung (S. 14–15):

```
Keyword quality criteria (Handreichung oc.bydata):

GOOD:
- Minimum 3 relevant keywords (FAIL if fewer)
- Short, singular, layperson-understandable terms
  ("Museum", "Kultur" not "Museumskulturangebot")
- Specific to content, not just describing the metadata type
- Multilingual variants improve EU-wide discoverability (bonus)

BAD — mark down for:
- Compounds that should be split into atomic terms
- Plural forms ("Veranstaltungen" → "Veranstaltung")
- Pure jargon/abbreviations ("BauGB" instead of "Baugesetzbuch")
- Redundancy with title — keywords complement, not repeat
- Formal/obvious tags: "Gemeinde", year number, publisher name
  (these are already in dedicated metadata fields)
- Too many keywords (>15): likely padding, check if all are meaningful
- Missing keywords entirely: automatic FAIL
```

**Quelle:** Handreichung zur Metadatenqualität S. 14–15

---

### 3.4 `expr_contextual_qualifiers` — Konkrete Checkliste ergänzen

```
Specific contextual qualifiers to check for (Handreichung + Konventionenhandbuch):
- Time series / statistics: year or reference period in title or description?
- Geographic datasets: geographic scope stated where not obvious?
- Survey / administrative data: cutoff date (Stichtag) mentioned?
- Estimated / provisional data: "vorläufig", "geschätzt", "hochgerechnet"?
- Draft data: "Entwurf", "preliminary" flagged?
- Regularly updated data: update cycle mentioned?
- Derived / aggregated data: aggregation method noted?

Note: these qualifiers are only required when the content CALLS for them —
a one-time static dataset does not need a "cutoff date" qualifier.
Penalize absence only when the data type clearly demands the qualifier.
```

**Quelle:** Handreichung zur Metadatenqualität S. 11 ("Gibt es Besonderheiten?")

---

### 3.5 `expr_thematic_consistency` — Theme-Keyword-Verbindung ergänzen

```
Also check: do keywords relate to the dcat:theme category?
A dataset tagged as ECON (Economy/Finance) but whose keywords are purely
geographic with no economic terms shows thematic inconsistency.
The theme, keywords, title, and description should form a coherent
subject picture — off-topic signals in any of these fields reduce score.
```

---

## 4. Begründungsstruktur für die Thesis

### 4.1 Die drei Begründungsebenen

Das Modell verwendet eine Drei-Ebenen-Begründung. Für jeden Indikator gilt
genau eine davon:

| Ebene | Indikatorklasse | Begründungsquelle | Beispiel |
|-------|----------------|-------------------|---------|
| **Normativ-europäisch** | A | MQA / DCAT-AP | `acc_download_url`, `reuse_license` |
| **Normativ-national** | B/C | DCAT-AP.de Konventionenhandbuch | `reuse_contributor_id`, `acc_distribution_status` |
| **Praxisbasiert** | B/C | Handreichung oc.bydata, first-principles | `find_keywords_count` ≥ 3, `expr_*` |

Für alle Expressiveness-Indikatoren gilt Ebene 3: Die Kriterien sind
operationalisierte Qualitätsmerkmale aus dem Konventionenhandbuch (Kap. 1.7,
3.4) und der Handreichung (S. 9–15) die durch LLM-Assessment ausgewertet
werden, weil sie semantischer Natur sind und sich nicht deterministisch
prüfen lassen.

---

### 4.2 Gewichtung: funktionale Abhängigkeitshierarchie

Die Indikatorgewichte sind nicht empirisch optimiert (keine Quelle hat das
je getan, inklusive MQA), sondern folgen einer funktionalen
Abhängigkeitslogik:

**Harte Blocker** (hohe Gewichtung): Ein Defizit hier macht den Datensatz
de facto unnutzbar, unabhängig von allen anderen Qualitätsdimensionen.
- `acc_download_url_response` — kaputte URL = kein Datenzugriff
- `reuse_license` — fehlende Lizenz = rechtlich nicht nachnutzbar
- `acc_machine_readable_access` — unlesbares Format = nicht maschinell verarbeitbar

**Mittlere Einschränkungen** (normale Gewichtung): Datensatz nutzbar, aber
Kontext oder Vertrauenswürdigkeit eingeschränkt.
- `reuse_publisher`, `reuse_contact` — Provenienz unklar
- `find_theme_valid`, `find_keywords_count` — Auffindbarkeit reduziert
- `expr_description_quality` — Nutzbarkeit ohne Kontext eingeschränkt

**Weiche Signale** (niedrige Gewichtung): Nice-to-have, kein direkter
Nutzbarkeitsimpakt.
- `find_accrual_periodicity` — fehlt oft auch bei guten Datensätzen
- `find_issued_datetime` — weniger kritisch als `dct:modified`
- `expr_contextual_qualifiers` — situationsabhängig

Diese Logik korrespondiert mit den FAIR-Prinzipien: ein Datensatz muss erst
*Findable* sein bevor *Accessible* relevant ist, und erst *Accessible* bevor
*Reusable* zutrifft. Indikatoren die frühere FAIR-Stufen sicherstellen
bekommen entsprechend höhere Gewichte.

---

### 4.3 Empirische Begründung durch Ground-Truth-Evaluation

Das Modell unterscheidet sich von MQA und allen anderen bekannten
DCAT-AP.de-Qualitätswerkzeugen durch eine empirische Validation:

- Stratifizierte Stichprobe n=50 + Extremfälle n=10
- Manuelle Bewertung auf 0–5-Skala (Blind-Evaluation)
- Primärmetrik: Cohen's κ (gewichtet, linear) — misst Übereinstimmung
  zwischen Modell und menschlichem Expertenurteil
- Sekundärmetriken: Spearman ρ, Kendall τ, MAE, RMSE, Bias, AUC

Das macht keine Aussage darüber ob die Indikatoren *die richtigen* sind —
aber es zeigt ob das Modell in seiner Gesamtheit mit menschlichem
Qualitätsurteil übereinstimmt. MQA hat das nie gemessen.

---

## 5. Gewichtung: Code vs. argumentierte Differenzierung

**Befund (verifiziert im Code):** Jeder Indikator hat im Code `weight=1.0`. In
`state_default.yaml` sind alle `dimension_weights` = 1 und der gesamte
`indicator_weights`-Block ist **auskommentiert**. Das laufende Modell behandelt
also alle aktiven Indikatoren und alle Dimensionen exakt gleich.

**Problem:** Section 4.2 argumentiert für eine *funktionale
Abhängigkeitshierarchie* (kaputter Download-Link wiegt schwerer als fehlende
accrualPeriodicity). Diese Hierarchie wird aktuell **nicht angewendet** — die
Argumentation verspricht etwas, das die Implementierung nicht einlöst. In der
Verteidigung ist das angreifbar.

**Zwei saubere Optionen (Entscheidung nötig):**

- **(a) Differenzieren:** `indicator_weights` aktivieren und gemäß der
  Hierarchie setzen (die Rationale-Kommentare stehen bereits im YAML,
  Z. 92–123). Vorteil: Modell und Argumentation stimmen überein.
- **(b) Uniform begründen:** Gleichgewichtung bewusst als Baseline deklarieren
  ("keine empirische Basis für spezifische Gewichte, daher gleichgewichtet").
  Dann muss Section 4.2 entschärft werden, damit sie keine differenzierte
  Gewichtung *behauptet*, die nicht stattfindet.

Empfehlung: **(a)**, weil die funktionale Hierarchie ein gutes,
nachvollziehbares Argument ist — aber nur wenn sie tatsächlich im Code wirkt.

---

## 6. Scoring-Nachvollziehbarkeit (Partial-Scores & GRADED-Schwellen)

Dies ist der substanziell wichtigste Punkt für die Aussagekraft des Modells.
Grundlage: Lektüre von `score_policy.py` und allen GRADED-Indikatoren.

> **Status: umgesetzt.** Die Ebenen 1–3 unten sind im Code implementiert
> (`score_policy.py`, `reusability.py`, alle drei State-Configs). Die
> Sensitivitätsanalyse (6.4) bleibt offen. Zusätzlich wurden
> `acc_format_congruence` und `acc_distribution_model` aus dem Modell entfernt
> (siehe 6.5).

### 6.1 Mechanik (verifiziert in `score_policy.py:105-114`)

Für GRADED-Indikatoren (`Indicator.GRADED = True`) gilt:

| Status | resultierender Score |
|--------|----------------------|
| PASS | roher Score |
| PARTIAL | roher Score *(identisch zu PASS!)* |
| FAIL | `fail_score` (default 0.0) |

**Konsequenz 1:** Die PASS/PARTIAL-Grenze (Cutoffs 0.9 / 0.85 / 0.8) ist
numerisch **bedeutungslos** — beide Pfade behalten den rohen Score. Diese
Cutoffs sind reine Anzeige-Labels und müssen *nicht* zahlenmäßig verteidigt
werden.

**Konsequenz 2 (das eigentliche Problem):** Die FAIL-Grenze ist die einzige,
die numerisch wirkt — und sie erzeugt eine **Diskontinuität**:

> `acc_format_non_proprietary`: roh 0.49 → FAIL → **0.0**.
> Roh 0.50 → PARTIAL → **0.50**.

Ein Messunterschied von 0.01 erzeugt 0.50 Output-Unterschied. Das ist der
Kern des Nachvollziehbarkeitsproblems — nicht dass es Schwellen gibt, sondern
dass eine davon eine Klippe in einen sonst stetigen Wert reißt.

### 6.2 Leitprinzip: Messung ≠ Label

Die kontinuierliche Messung (Anteil bzw. quellen-gebundener Mittelwert) ist das
verteidigbare Konstrukt. Das Status-Label (PASS/PARTIAL/FAIL) ist eine
sekundäre Diskretisierung, die arbiträre Cutoffs einführt. Ziel: die Messung
zur kanonischen Größe machen, das Label nur fürs Reporting.

### 6.3 Drei-Ebenen-Empfehlung

**Ebene 1 — Bruch-Logik (`pass_count / dist_count`) unverändert lassen.**
Das ist das stärkste Konstrukt: "Anteil der Distributionen, die X erfüllen"
ist eine direkte, interpretierbare Messung ohne Threshold-Bedarf. Der
Nutzer-Wunsch, diese Per-Distribution-Logik zu erhalten, ist genau richtig.

**Ebene 2 — FAIL-Klippe für GRADED entfernt (umgesetzt).** In
`score_policy.py:evaluate()` liefern GRADED-Indikatoren ihren `raw_score` jetzt
bei **jedem** Status (PASS/PARTIAL/FAIL). Effekt:

- Dataset-Score ist eine **stetige, monotone** Funktion der Messung.
- PASS/PARTIAL/FAIL sind **vollständig präsentational** — keine Cutoffs mehr
  zu verteidigen.
- Der `fail_score`-Penalty-Pfad bleibt erhalten als **expliziter
  Per-Indikator-Override** (z. B. `acc_machine_readable_access: {fail_score:
  -0.5}` in `state_presentation_tuned.yaml`) — nur dann wird ein graded FAIL
  bestraft, sonst zählt der rohe Score. Für ternäre Indikatoren gilt der
  `fail_score`-Pfad uneingeschränkt.

Damit reduziert sich die gesamte Verteidigungslast auf zwei Sätze: (1) wie der
kontinuierliche Score konstruiert wird und (2) dass die Statuslabels rein
präsentational sind.

**Ebene 3 — Interne Per-Item-Gewichte (umgesetzt, soweit nötig).** Stand nach
Entfernung der zwei nicht-vertretbaren Indikatoren (6.5):

| Indikator | interner Wert | Status |
|-----------|---------------|--------|
| `acc_machine_readable_access` | Tiers 1.0/0.5/0.0 | **Behalten** — an data.europa.eu-Format-Rating-Tabelle (1–3) gebunden; in der Thesis als Quelle nennen |
| `acc_format_non_proprietary`, `acc_*_url_response` | binär pro Item | **Behalten** — sauberer Anteil, kein Magic |
| `reuse_contact` | ~~0.25×3 + 0.05-Bonus~~ | **Umgebaut auf ternär** — PASS (E-Mail oder URL vorhanden) / PARTIAL (Kontakt ohne valide E-Mail/URL) / FAIL (kein Kontakt), gemäß Konvention 01; kein GRADED mehr |
| `acc_format_congruence`, `acc_distribution_model` | 0.7 bzw. 0.6/0.4 | **Aus dem Modell entfernt** (6.5) |

**Ternäre Indikatoren:** ein einziger globaler `partial_score = 0.5` mit einer
Semantik ("Eigenschaft vorhanden, aber nicht vollständig valide"). Die
hartcodierten Per-Indikator-Scores werden durch die Policy ohnehin überschrieben
— sie sind konsistent als Vielfache von 0.5 gehalten.

### 6.4 Optional: Sensitivitätsanalyse als stärkstes Argument

Statt Cutoffs *quellenbasiert* zu belegen (unmöglich), zeigen dass das
End-Ranking robust gegen ±0.1-Verschiebung der Schwellen ist. Passt direkt zu
Notebook 10 und ist methodisch das überzeugendste Argument für die Wahl der
verbleibenden Schwellen. **Offen.**

### 6.5 Entfernte Indikatoren: `acc_format_congruence` & `acc_distribution_model`

Beide wurden per `indicator_blacklist` in allen drei State-Configs aus dem
Modell genommen. Begründung:

- **Schwer zu begründen:** Für beide gibt es kein MQA-Pendant und keine
  normative Quelle (beide sind Klasse C). `acc_format_congruence` mischt vier
  heterogene Signale (dct:format, dcat:mediaType, URL-Endung, HTTP
  Content-Type); `acc_distribution_model` interpretiert die Modellierungsabsicht
  des Publishers heuristisch.
- **Hohe Fehleinschätzungsrate:** Beide erzeugen viele False Positives/Negatives
  (z. B. legitime Format-Varianten als "split-data" fehlklassifiziert,
  HTTP-Content-Type-Abweichungen bei korrekten Daten). Die Unsicherheit der
  Messung übersteigt ihren Informationswert und schadet der Gesamtaussage des
  Modells.

Das aktive Modell umfasst damit **27 Indikatoren** (29 registriert, 2
geblacklistet). Der Code beider Indikatoren bleibt erhalten (reversibel über die
Config), läuft aber nicht.

---

## 7. Doc/Code-Inkonsistenzen (Glaubwürdigkeit)

Zwei verifizierte Widersprüche zwischen Dokumentation und Implementierung, die
ein Gutachter findet:

- **`reuse_contributor_id`** (`reusability.py:670`): Der Docstring beschreibt ein
  4-stufiges Scoring (1.0 / 0.5 / 0.25 / 0.0). Der **Code produziert nur 1.0
  oder 0.0** — die 0.5- und 0.25-Stufen existieren nicht (single-not-vocab →
  FAIL 0.0, multiple → FAIL 0.0). Docstring an Code angleichen.
- **`reuse_access_rights`**: `indicator_mapping.md` listet Aggregation als
  **"all"**, der Code nimmt aber `max()` (`reusability.py:324`) = **"any"** (eine
  in-vocab-URI genügt für PASS). Label im Mapping korrigieren.

---

## 9. Offene Punkte die NICHT implementiert werden müssen

Diese Punkte wurden identifiziert aber bewusst ausgeklammert:

| Punkt | Begründung für Ausschluss |
|-------|--------------------------|
| `acc_conforms_to` (`dct:conformsTo`) | MQA-Äquivalent fehlt auch; das SHACL-Compliance-Indikator deckt Konformität bereits ab |
| `find_political_geocoding_level` (`dcatde:politicalGeocodingLevelURI`) | Bereits teilweise durch `find_adminunitl2` abgedeckt; Aufwand vs. Nutzen niedrig |
| `reuse_license_attribution` (`dcatde:licenseAttributionByText`) | Nur bei BY-Lizenzen relevant; Lizenz-parsing komplex, limitierter Mehrwert im Gesamtkontext |
| `acc_distribution_availability` (`dcatap:availability`) | Prüft Stabilitätsversprechen der URL, nicht aktuelle Qualität; schwer operationalisierbar |
| `expr_description_completeness` als separates LLM-Kriterium | Wird in `expr_description_quality` subsumiert durch Prompt-Update |
| Indicator-Mapping-Tabelle erweitern für neue Indikatoren | Kann nach Implementierung ergänzt werden |

---

## 10. Umsetzungsreihenfolge

| Priorität | Aufgabe | Aufwand | Wirkung |
|-----------|---------|---------|---------|
| **1** | FAIL-Klippe für GRADED entfernen (`score_policy.py`) | klein | beseitigt Scoring-Diskontinuität — größter Aussagekraft-Gewinn |
| **1** | `find_keywords_count` Threshold-Logik-Bug fixen | minimal | 3 Keywords = FAIL ist falsch |
| **1** | Gewichtung entscheiden (differenzieren vs. uniform begründen) | klein | Modell und Argumentation in Einklang |
| **1** | Doc/Code-Inkonsistenzen fixen (contributor_id, access_rights) | minimal | Glaubwürdigkeit |
| **1** | Expressiveness-Prompt-Update (alle 4 Kriterien) | mittel | größter Qualitätsgewinn |
| **2** | `acc_format_congruence` binarisieren (0.7-Tier raus) | klein | entfernt unbelegte Magic Number |
| **2** | `acc_distribution_status` neu (MUSS-Lücke) | mittel | Vollständigkeit |
| **2** | `find_identifier` neu (Pflichtfeld) | klein | Vollständigkeit |
| **3** | Sensitivitätsanalyse Schwellen (Notebook 10) | mittel | stärkstes Argument für Cutoff-Wahl |
| **3** | `reuse_language` neu | klein | optional |
| **3** | `indicator_mapping.md` für neue Indikatoren aktualisieren | minimal | Dokumentation |

---

## 11. Was nicht geändert werden muss (explizite Bestätigung)

- Alle 29 existierenden Indikatoren bleiben valide
- Die 4-Dimensionen-Struktur bleibt (kein Interoperability-Dimension nötig —
  acc_format und acc_media_type decken das MQA-Interoperability-Äquivalent ab)
- Die ScorePolicy-**Architektur** bleibt — nur die FAIL-Behandlung für GRADED
  wird angepasst (Section 6.3, Ebene 2); die YAML-Konfiguration bleibt kompatibel
- Die Bruch-Logik `pass_count / dist_count` der Per-Distribution-Indikatoren
  bleibt unverändert (Section 6.3, Ebene 1)
- Der SHACL-Indikator (`reuse_dcat_ap_de_compliance`) bleibt
- Die Ground-Truth-Evaluation-Methodik (Notebook 10) bleibt
