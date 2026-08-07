# Referenzdatensatz als roter Faden durch die Thesis

Vorhaben aus einer Anregung des Erstbetreuers: Ein Idealfall-Metadatensatz soll
die Thesis als wiederkehrendes Beispiel durchziehen, statt ungenutzt im
Repository zu liegen.

Stand: 06.08.2026. **Umgesetzt** — diese Datei dokumentiert das Artefakt, die
getroffenen Entscheidungen und die Stellen, an denen es in der Thesis auftaucht.

---

## 1. Das Artefakt

| | |
|---|---|
| Datei | `data/referenzdatensatz.rdf` (110 Zeilen) |
| Herkunft | `data/sample_2026-06-03_13-33/non_geo_land-schleswig-holstein_04.rdf` — realer Datensatz aus dem Open-Data-Portal Schleswig-Holstein, enthalten in der Stichprobe dieser Arbeit |
| Inhalt | „Feinstaub (PM2,5) Lübeck, Moislinger Allee Tagesmittel 2023“, Herausgeber Landesamt für Umwelt SH, ausgeliefert über die Messwertschnittstelle des Umweltbundesamtes |
| Distributionen | zwei — **derselbe Datenbestand** als CSV und als JSON |
| Eigene Config | `conf/state/state_perfect_example.yaml` |

### Warum dieser Satz und nicht die beiden Vorgänger

1. **Destatis 12411-0001** (erster Versuch): selbst zusammengesucht, Herkunft
   schlechter erklärbar; außerdem existiert im DCAT-AP.de-Schlüsselvokabular
   kein Schlüssel für das Bundesgebiet, sodass `find_political_geocoding` auf
   Bundesebene nicht kongruent erfüllbar ist.
2. **Bodenfeuchte Ingolstadt** (`data/extreme_cases_04/good_01.rdf`, aus dem
   Experteninterview): Herkunft ideal, Struktur nicht. Die beiden verbleibenden
   Distributionen waren **Messreihe + Abkürzungsverzeichnis**, also inhaltlich
   verschiedene Ressourcen — genau das Muster, das Abschnitt 3.x der Thesis als
   Fehlgebrauch der Distributionsebene beschreibt (`dcat:DatasetSeries` in
   DCAT~3). Ein Idealfall darf nicht ausgerechnet eine Schwäche des Prototyps
   ausnutzen. Andere Formate derselben Daten bietet das Portal nicht an:
   geprüft wurden `.json`, `.xlsx`, `.xls`, `.xml`, `.ods` — alle 404, es
   existieren nur `.csv` und `.jsonld`. Und `JSON_LD` fehlt in
   `NON_PROPRIETARY_FORMAT_URIS` (`src/extraction/distribution_probes.py:222`),
   weshalb die JSON-LD-Variante `acc_format_non_proprietary` auf 0,67 drückt.
   Die Liste zu ergänzen wäre sachlich richtig — JSON-LD ist so offen wie das
   dort gelistete RDF/Turtle —, würde aber die Scores aller Stichproben mit
   JSON-LD-Distributionen verschieben (u. a. 18 Dateien in
   `sample_small_portals_2026-07-21_10-20`) und damit berichtete Kennzahlen
   invalidieren. Bleibt als dokumentierte Lücke stehen.
3. **PM2,5 Lübeck 2023** (aktuell): zwei Distributionen mit identischem Inhalt
   in zwei offenen Formaten, abgeschlossener Bezugszeitraum, Gemeindeebene
   kongruent zum Gemeindeschlüssel, Herkunft aus der eigenen Stichprobe.

### Was gegenüber dem Portaloriginal geändert wurde

Beibehalten: Datensatz-URI, Distributions-URIs und -URLs, Herausgeber,
Lizenz (dl-by-de/2.0), `contributorID` (schleswigHolstein), Thema ENVI,
Geometrie der Messstation, Zeitraum 2023, `issued`/`modified`, `accessRights`.

Ergänzt (für den vollen Score nötig):

- `dcat:contactPoint` — fehlte; `reuse_contact`. Als Kontakt dient die
  Organisationsseite des LfU im Portal, **keine erfundene E-Mail-Adresse**
  (das Portal hinterlegt keine)
- `dcatap:availability` je Distribution — fehlte; `reuse_availability`
- `dcat:mediaType` je Distribution — fehlte; `acc_media_type`
- `dcatde:politicalGeocodingURI` (Gemeindeschlüssel 01003000, Lübeck) und
  `dcatde:politicalGeocodingLevelURI` (`municipality`) — fehlten;
  `find_political_geocoding`, `find_geocoding_level`
- `dct:language` je Datensatz und Distribution, `foaf:homepage`,
  `dcat:landingPage`, `dct:accrualPeriodicity` (`NEVER`, da abgeschlossen)

Entfernt: `dct:rights` (dubliert `dct:license`, ohne Wirkung).

Inhaltlich überarbeitet (Aussagekraft):

- **Titel** benennt Stoff, Ort, Station, Auswertungsart und Jahr
- **Beschreibung** neu geschrieben: Inhalt, Spalten, Einheit, Erhebungsmethode
  und Quelle, Formatunterschied der beiden Distributionen, Vorläufigkeit der
  Werte, abgeschlossener Bezugszeitraum, Nutzungszwecke. Das Original enthielt
  Markdown-Auszeichnung (`***vorläufig***`, Markdown-Link), die als
  Formatierungsrest abgewertet wird
- **Schlagwörter** atomar und singularisch statt der Slug-Reste des Portals
  (`5_`, `feinstaub-pm2`, `moislinger-allee`), ein englisches Äquivalent
- **Distributionstitel und -beschreibungen** neu, jeweils formatspezifisch

### Geprüfter Stand (06.08.2026)

Lauf `outputs/runs/run_2026-08-06_15-42-18_state-evaluation-final_REF_UBA`,
Config `state_evaluation_final`, Modell GPT-5.5:

```
Auffindbarkeit        1,000   8/8
Zugänglichkeit        1,000   7/7
Wiederverwendbarkeit  1,000   6/6
Aussagekraft          0,972   6/6   (Titel 0,95 · Beschreibung 0,98 ·
                                     Kohärenz 1,00 · Schlagwörter 0,90 ·
                                     Thematik 1,00 · Kontext 1,00)
Gesamtscore           0,991   Note A   27/27 Indikatoren bestanden
```

Reproduktion (die Eval-Config hat aktuell die Aussagekraft nicht im
Dimensions-Whitelist, deshalb der Override):

```bash
.venv/bin/python src/main.py --config-name state/state_evaluation_final \
  state.directory_path=data state.files='[referenzdatensatz.rdf]' \
  'state.quality.dimension_whitelist=[accessibility,reusability,findability,expressiveness]' \
  state.run_output_dir_suffix=REF_UBA
```

Kosten je Lauf: rund 0,04 USD.

**Die deterministischen 21 Indikatoren sind vollständig erreichbar.** Die
Aussagekraft nicht: Das Sprachmodell vergibt auch bei einer Rubrik ohne
benennbaren Mangel nicht durchgängig 1,0; oberhalb von etwa 0,97 ist die
Dimension faktisch gedeckelt. Wiederholungsläufe auf identischer Eingabe ergaben
0,991 und 0,993 (LLM-Streuung, deckt sich mit Abschnitt 5.6 der Thesis).

Erreichbarkeit beider Distributions-URLs am 06.08.2026 geprüft: HTTP 200,
55,9 kB (CSV) bzw. 23,3 kB (JSON).

---

## 2. Leitidee

Derselbe Datensatz, in jedem Kapitel eine andere Frage an ihn:

| Kapitel | Frage |
|---|---|
| 2 Grundlagen | Wie sieht ein vollständiger DCAT-AP.de-Datensatz aus? |
| 3 Konzeption | Welchen Sollzustand beschreiben die abgeleiteten Indikatoren? |
| 4 Operationalisierung | Was zeigt der Prototyp einem Bereitsteller davon? |
| 5 Evaluation | Erreicht das Messinstrument seinen eigenen Höchstwert? |

**Benennung:** durchgängig **Referenzdatensatz**, in der Einführung einmal als
*konstruierter Idealfall* präzisiert. Nicht „Perfect Example“ — das behauptet
mehr, als das Konstrukt einlöst. Der Dateiname im Repository wurde am
07.08.2026 entsprechend von `perfect_example_01.rdf` auf `referenzdatensatz.rdf`
umbenannt (`conf/state/state_perfect_example.yaml` folgt der Umbenennung).

---

## 3. Umgesetzte Ankerpunkte in der Thesis

| Stelle | Label | Inhalt |
|---|---|---|
| §2.3, neuer Unterabschnitt „Aufbau eines DCAT-AP.de-Datensatzes am Referenzdatensatz“ | `sec:referenzdatensatz` | Einführung, gekürztes Listing (`lst:referenzdatensatz`), zwei Absätze zu Dataset↔Distribution (inkl. „derselbe Inhalt in zwei Formaten“) und kontrollierten Vokabularen |
| Ende Kapitel 3, nach der Aussagekrafts-Tabelle | — | Scharnier-Absatz: Der Referenzdatensatz ist die konkrete Form des Modells; plausibilisiert die Vollständigkeit der Indikatormenge |
| §4.8.5 „Von der Meldung zur Handlungsanweisung“ | `subsec:handlungsanweisung` | Absatz: Feldweise Vorlage vs. vollständiger Beispieldatensatz als zwei Auflösungsstufen |
| §5.5, neuer Unterabschnitt „Deckenprüfung des Messinstruments am Referenzdatensatz“ | `subsec:deckenpruefung` | Trägt das Argument: Tabelle `tab:deckenpruefung`, Befund zur Skalendecke, Deckelung der Aussagekraft bei ~0,97, zwei Einschränkungen |
| Anhang | `app:referenzdatensatz` | Vollständiges RDF/XML, `thesis/appendix/referenzdatensatz.tex`, eingebunden in `report.tex` |

Zur Formulierung in §4.8.5: Die Vorlagen in `src/core/guidance.py` sind
**keine** wörtlichen Ausschnitte dieses Datensatzes (sie führen eigene
Beispielwerte). Der Text behauptet das entsprechend auch nicht, sondern stellt
die beiden Darstellungsformen nebeneinander.

Nicht umgesetzt: der optionale Frontend-Screenshot der Detailansicht mit Note A.

### LaTeX-Fallstrick

Die Listings brauchen `breaklines`, aber **nicht** `breakanywhere`: Unter
pdflatex bricht fvextra sonst mitten in ein UTF-8-Mehrbyte-Zeichen und der Lauf
stirbt mit `Invalid UTF-8 byte sequence`. Stattdessen `breakafter=/` — bricht
lange Vokabular-URIs, ohne je in einen Umlaut zu schneiden.

---

## 4. Randbedingungen

- **Thesis nicht selbst kompilieren** (Memory `no-latex-build`): Der Editor des
  Autors läuft mit eigenem latexmk auf dasselbe `thesis/build`. Wenn doch
  nötig, mit `-outdir` in ein separates Verzeichnis bauen.
- Keine Commits, Pushes oder PRs.
- `@TODO`-Kommentare des Autors nie entfernen, auch nicht bei Erledigung — das
  gilt insbesondere für das TODO in §2.3, das durch den neuen Unterabschnitt
  beantwortet wird.
