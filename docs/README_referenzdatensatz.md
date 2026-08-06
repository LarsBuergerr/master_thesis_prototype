# Referenzdatensatz als roter Faden durch die Thesis — Arbeitsplan

Vorhaben aus einer Anregung des Erstbetreuers: Der handgebaute „perfect example"-
Metadatensatz soll die Thesis als wiederkehrendes Beispiel durchziehen, statt
ungenutzt im Repository zu liegen.

Stand: 06.08.2026. **Noch nichts davon ist umgesetzt** — diese Datei hält den
abgestimmten Plan fest.

---

## 1. Das Artefakt

| | |
|---|---|
| Datei | `data/perfect_example_01.rdf` (109 Zeilen) |
| Variante | `data/perfect_example_01.rebuilt.rdf` (Zweck ungeklärt, vor Verwendung prüfen) |
| Inhalt | Destatis-Tabelle 12411-0001 „Bevölkerung: Deutschland, Stichtag", zwei Distributionen (CSV, JSON) |
| Alte Läufe | `outputs/runs_archive/run_2026-06-02_*_state-perfect-example_*` |
| Eigene Config | `conf/state/state_perfect_example.yaml` |

### Geprüfter Stand (06.08.2026)

Bewertet mit `state_evaluation_final`, Sprachmodell aus:

```
findability    score 1.000   8/8
accessibility  score 1.000   7/7
reusability    score 1.000   6/6
```

**Alle 21 deterministischen Indikatoren bestanden.** Der Datensatz ist also
entgegen der ursprünglichen Annahme *nicht* veraltet und kann ohne Sanierung
verwendet werden. Ungeprüft ist allein die Aussagekraft (LLM).

Reproduktion:

```bash
.venv/bin/python src/main.py --config-name state/state_evaluation_final \
  state.directory_path=data state.files='[perfect_example_01.rdf]' \
  state.llm.enabled=false state.run_output_dir_suffix=PERFECT_CHECK
```

Lauf vom 06.08.: `outputs/runs/run_2026-08-06_10-13-21_state-evaluation-final_PERFECT_CHECK`
(kann gelöscht werden, war nur Verifikation).

---

## 2. Leitidee

Derselbe Datensatz, in jedem Kapitel eine andere Frage an ihn — nicht viermal
dieselbe Darstellung:

| Kapitel | Frage |
|---|---|
| 2 Grundlagen | Wie sieht ein vollständiger DCAT-AP.de-Datensatz aus? |
| 3 Konzeption | Welche der abgeleiteten Anforderungen erfüllt er? |
| 4 Operationalisierung | Was macht der Prototyp mit ihm? |
| 5 Evaluation | Erreicht das Messinstrument seinen eigenen Höchstwert? |

**Benennung:** nicht „Perfect Example" — das behauptet mehr, als das Konstrukt
einlöst, und provoziert die Rückfrage „perfekt wonach?". Stattdessen
**Referenzdatensatz** oder *konstruierter Idealfall*. Der Begriff muss
mittragen, dass der Satz konstruiert ist und keine Aussage über reale
Portaldaten erlaubt.

---

## 3. Die vier Ankerpunkte (nach Nutzen sortiert)

### 3.1 Kapitel 5 — Deckenprüfung des Instruments (höchster Nutzen)

Das eigentliche Argument, kein Beiwerk. Die Kernstichprobe liegt im Mittel bei
65/100; der naheliegende Prüfereinwand lautet: *Ist die Skala oben überhaupt
erreichbar, oder misst das Verfahren systematisch zu streng?* Ein konstruierter
Datensatz, der 1,0 erreicht, beantwortet das — analog zur Ceiling-Analyse, aber
auf der Instrumentenseite statt der Verteilungsseite. Damit wird aus
„mittelmäßige Metadaten" ein Befund über die Datenlage statt über das Verfahren.

- Umfang: ca. eine halbe Seite, ggf. eine kleine Tabelle (Score je Dimension)
- Platzierung: eigener Unterabschnitt, entweder am Ende von 5.5
  (Auswertungsverfahren, als Instrumentenprüfung vor der ersten Zahl) oder als
  erster Unterabschnitt von 5.7
- **Voraussetzung: ein Lauf mit aktiviertem Sprachmodell**, sonst fehlt die
  Aussagekraft-Dimension und der Gesamtscore ist nicht belastbar
- Muss ausdrücklich als Instrumentenprüfung deklariert werden, nicht als
  Qualitätsbefund — der Satz ist konstruiert und nicht randomisiert gezogen

### 3.2 Kapitel 2, §2.3 „DCAT-AP.de als Metadatenstandard" — Einführung

In `contents.tex:118` steht ein `@TODO` des Autors: „ggf. noch etwas expliziter
erläutern wie DCAT-AP.de aufgebaut ist". Der Referenzdatensatz beantwortet genau
das.

- gekürztes Listing: Dataset-Kopf, eine Distribution, Kontaktblock
- zwei Absätze: Aufbau Dataset ↔ Distribution, Rolle der kontrollierten Vokabulare
- vollständiges RDF in den Anhang
- hier wird der Datensatz eingeführt und benannt, alle späteren Stellen verweisen zurück

### 3.3 §4.8.5 „Von der Meldung zur Handlungsanweisung" — Auflösung der Vorlagen

Label: `subsec:handlungsanweisung`. Billigster Einbau mit sichtbarster Wirkung.

Zwei Sätze genügen: Die „So sollte es aussehen"-Vorlagen aus
`src/core/guidance.py` sind feldweise Ausschnitte genau dieses Datensatzes. Was
die Oberfläche einem Bereitsteller stückweise zeigt, steht in Kapitel 2 einmal
als Ganzes. Schließt den Kreis, ohne neue Argumentation.

### 3.4 Ende von Kapitel 3 — Scharnier zur Operationalisierung

Ein Absatz: Die abgeleiteten Indikatoren beschreiben zusammengenommen den
Zustand, den der Referenzdatensatz verkörpert; er ist der operationalisierte
Sollzustand des Modells. Begründet nebenbei die Vollständigkeit der
Indikatormenge.

### 3.5 Optional — Frontend-Screenshot

Detailansicht mit Note A und durchgehend erfüllten Indikatoren, als Gegenstück
zu den Befund-Screenshots in 4.8. Billig, da das Frontend ohnehin läuft.

---

## 4. Vor der Umsetzung zu klären

Sobald der Datensatz Schaustück wird, liest ihn jemand genau. Drei Stellen, die
die Indikatoren *nicht* prüfen, einem Leser aber auffallen:

1. **Distributions-URLs passen nicht zum Inhalt.** `dcat:accessURL` und
   `dcat:downloadURL` zeigen auf
   `opendata.schleswig-holstein.de/.../kreis-hzgt.-lauenburg.csv`, während der
   Datensatz Bevölkerungszahlen des Bundes von Destatis beschreibt. Erreichbar
   ja, inhaltlich passend nein.
2. **Zweite Distribution widersprüchlich benannt.** Titel und Beschreibung sagen
   „XLSX", `dct:format` ist JSON und `dcat:mediaType` ist `application/json`.
3. **Geokodierung inkonsistent.** `politicalGeocodingLevelURI` steht auf
   `federal`, der Schlüssel darunter
   (`politicalGeocoding/municipalityKey/08435005`) ist eine Gemeinde in
   Baden-Württemberg.

Zwei Wege: korrigieren, oder im Text als bewusste Platzhalter benennen. Die
zweite Variante hat Charme, weil sie zeigt, wo die Grenze des Indikatorensatzes
liegt (Kongruenzprüfungen fehlen bzw. sind blacklisted).

---

## 5. Reihenfolge der Umsetzung

1. Lauf mit Sprachmodell über die eine Datei → Gesamtscore und
   Aussagekraft-Werte für 3.1 (Kosten: wenige Cent)
2. Entscheidung zu Abschnitt 4 (korrigieren vs. deklarieren)
3. Kapitel 5 (3.1) — trägt das Argument
4. Kapitel 2 (3.2) + Anhang — führt ein
5. Die beiden Kurzverweise (3.3, 3.4)
6. optional Screenshot (3.5)

---

## 6. Randbedingungen

- **Thesis nicht selbst kompilieren** (siehe Memory `no-latex-build`): Der
  Editor des Autors läuft mit eigenem latexmk auf dasselbe `thesis/build`.
- Keine Commits, Pushes oder PRs.
- `@TODO`-Kommentare des Autors nie entfernen, auch nicht bei Erledigung — das
  gilt insbesondere für das TODO in §2.3, das durch 3.2 beantwortet wird.
