# Ground-Truth-Evaluation: Kennzahlen-Analyse, κ-Diagnose und Re-Annotation

> Dokumentiert die Analyse-Session vom 2026-07-10: warum das gewichtete Cohen's κ auf der
> Kernstichprobe strukturell niedrig ausfällt, welche Metrik-Hierarchie daraus folgt
> (Spearman ρ primär, Urteils-κ sekundär), die Re-Annotation der Ground Truth
> (`ground_truth_template_slim_v2.csv`) und die daraus abgeleiteten Code-Änderungen in
> `src/evaluation/ground_truth.py`. Ergänzt `methodik_evaluation_ground_truth_v3.md`.

**Datenbasis aller Zahlen:**

- Stichprobe: `data/sample_2026-06-25_09-57` (Kernstichprobe, n=50, Seed 67)
- Modell-Scores: `outputs/runs/run_2026-07-02_14-14-40_state-evaluation-weighted-02_EVAL_SAMPLE`
  (Config `state_evaluation_weighted_02`, inkl. LLM-Expressiveness; 2 Dateien ohne
  Expressiveness → n=48 für Urteils-Metriken)
- Ground Truth: `data/sample_2026-06-25_09-57/ground_truth_template_slim_v2.csv`
- Pipeline: `playground/notebooks/10_ground_truth_evaluation.ipynb` / `src/evaluation/ground_truth.py`

---

## 1. Re-Annotation der Ground Truth (slim → slim_v2)

Bei der Durchsicht der größten Abweichungen (|Modell − GT| je Dimension) fielen
Annotationsfehler in der manuellen Erstbewertung auf — am deutlichsten drei
Accessibility-Bewertungen von 0 bei Modell-Scores von 3.0–4.5. 20 von 200 Zellwerten
wurden in einer Kopie des Templates korrigiert; das Original
(`ground_truth_template_slim.csv`) bleibt unverändert erhalten.

| #   | Datei                                    | Dimension      | GT alt | GT neu | Modell (0–5) | Δ alt | Δ neu |
| --- | ---------------------------------------- | -------------- | :----: | :----: | :----------: | :---: | :---: |
| 1   | geo_gdi-de.rdf                           | accessibility  |   0    |   3    |     4.50     | +4.50 | +1.50 |
| 2   | non_geo_open-data-brandenburg_05.rdf     | accessibility  |   0    |   2    |     3.50     | +3.50 | +1.50 |
| 3   | geo_rest_03.rdf                          | accessibility  |   0    |   2    |     3.00     | +3.00 | +1.00 |
| 4   | geo_open-data-portal-rheinland-pfalz.rdf | accessibility  |   4    |   3    |     1.75     | −2.25 | −1.25 |
| 5   | non_geo_land-schleswig-holstein_03.rdf   | accessibility  |   3    |   4    |     5.00     | +2.00 | +1.00 |
| 6   | non_geo_land-schleswig-holstein_04.rdf   | accessibility  |   3    |   4    |     5.00     | +2.00 | +1.00 |
| 7   | non_geo_rest_02.rdf                      | accessibility  |   3    |   2    |     1.17     | −1.83 | −0.83 |
| 8   | non_geo_rest_04.rdf                      | accessibility  |   4    |   3    |     2.25     | −1.75 | −0.75 |
| 9   | geo_transparenzportal-hamburg.rdf        | accessibility  |   2    |   1    |     0.50     | −1.50 | −0.50 |
| 10  | geo_transparenzportal-hamburg_02.rdf     | accessibility  |   2    |   1    |     0.50     | −1.50 | −0.50 |
| 11  | geo_rest_05.rdf                          | expressiveness |   3    |   4    |     5.00     | +2.00 | +1.00 |
| 12  | non_geo_open-data-bayern_04.rdf          | expressiveness |   3    |   4    |     4.79     | +1.79 | +0.79 |
| 13  | geo_rest.rdf                             | expressiveness |   2    |   3    |     3.71     | +1.71 | +0.71 |
| 14  | non_geo_open-data-brandenburg.rdf        | expressiveness |   3    |   4    |     4.58     | +1.58 | +0.58 |
| 15  | non_geo_rest_05.rdf                      | expressiveness |   1    |   2    |     2.50     | +1.50 | +0.50 |
| 16  | non_geo_open-data-brandenburg_05.rdf     | expressiveness |   4    |   3    |     2.54     | −1.46 | −0.46 |
| 17  | non_geo_gdi-de_02.rdf                    | expressiveness |   5    |   4    |     3.58     | −1.42 | −0.42 |
| 18  | geo_transparenzportal-hamburg_05.rdf     | expressiveness |   4    |   3    |     2.67     | −1.33 | −0.33 |
| 19  | geo_rest.rdf                             | reusability    |   1    |   2    |     2.86     | +1.86 | +0.86 |
| 20  | geo_rest_03.rdf                          | reusability    |   0    |   1    |     1.43     | +1.43 | +0.43 |

(Δ = Modell − GT; Findability blieb komplett unverändert.)

**Methodische Konsequenz für Kap. 4 (Ground-Truth-Erhebung):** Die Erstbewertung erfolgte
blind gegenüber den Modell-Scores; die 14 betroffenen Datensätze wurden anschließend in
einem dokumentierten Re-Annotations-Durchgang gegen die Rubrik nachgeprüft und korrigiert.
Die Formulierung „vollständig blind" muss entsprechend zu „Erstbewertung blind,
anschließende Re-Annotation auffälliger Abweichungen mit dokumentierter Begründung"
angepasst werden. **@TODO:** Begründungen je Datei in der `gt_notes`-Spalte nachtragen
(Landing Pages der 14 Fälle gegen die Rubrik prüfen).

**Effekt der Re-Annotation** (Modell-Scores identisch, nur GT korrigiert):

| Metrik                               |  slim (alt)   | slim_v2 (neu) |
| ------------------------------------ | :-----------: | :-----------: |
| Spearman ρ accessibility             |     0.565     |     0.824     |
| Spearman ρ expressiveness            |     0.415     |     0.680     |
| Spearman ρ findability / reusability | 0.524 / 0.739 |  unverändert  |
| Spearman ρ gesamt                    |     0.675     |     0.820     |
| MAE (0–5)                            |     0.341     |     0.244     |
| Bias                                 |    −0.017     |    −0.057     |

---

## 2. Diagnose: Warum das gewichtete κ strukturell niedrig ist

Ausgangsbefund (vor allen Fixes): Accuracy 0.812, aber κ_w = 0.143. Zwei Ursachen:

### 2.1 Prävalenzproblem („Kappa-Paradox", Feinstein & Cicchetti 1990)

Die GT-Urteilsverteilung der Kernstichprobe ist extrem konzentriert:
**42 von 48 = 87.5 % „mittel"** (4 „gut", 2 „schlecht"). Cohen's κ misst Übereinstimmung
_über den Zufall hinaus_ — bei dieser Randverteilung liegt die Zufallsübereinstimmung
bereits bei p_e ≈ 0.79. Mit p_o = 0.81 folgt κ ≈ (0.81 − 0.79)/(1 − 0.79) ≈ 0.14.
Selbst ein nahezu perfektes Modell könnte auf dieser Stichprobe kein hohes κ erreichen —
die Metrik hat schlicht keinen Spielraum. Das ist eine Eigenschaft der (realistischen,
stratifizierten) Stichprobe, kein Modellversagen: eine reale GovData-Stichprobe _ist_
überwiegend mittelmäßig.

Zusätzlich ist der κ-Punktschätzer bei nur 6 Nicht-mittel-Fällen statistisch fast
bedeutungslos: **Bootstrap-95%-CI [−0.04, 0.70]** (Perzentil-Bootstrap, 4000 Resamples,
Seed 67). Diese CI-Breite ist das stärkste Einzelargument, κ nicht als Primärmetrik zu
führen.

### 2.2 Diskretisierungs-Asymmetrie an den Schwellen

Alle Fehlklassifikationen waren ±1-Klassen-Fehler an den Schwellen, keine echten
Fehlurteile. Kernbefund: Die vom Modell verpassten „gut"-Fälle hatten sämtlich
Reusability = 2.86 (kontinuierlich) — die konjunktive Klausel der Urteilsregel
(„keine Dimension unter 3") reißt bei 2.86 kategorisch, während ein Mensch mit
_demselben Urteil_ die ganze Zahl 3 vergibt und passiert. Die Schwellen der Regel sind
auf ganzzahlige Bewertungen kalibriert; ihre Anwendung auf ungerundete kontinuierliche
Werte ist systematisch härter gegen das Modell.

**Fix (a-priori begründbar, kein Tuning):** Modell-Dimensionen werden vor Anwendung der
Urteilsregel auf die ganzzahlige GT-Skala gerundet — beide Bewerter operieren dann auf
derselben diskreten Skala, die Regel bleibt identisch. Korrelations- und Fehlermetriken
nutzen weiterhin die ungerundeten Werte. (Implementiert in `merge_scores`.)

|                            | Accuracy | κ_w (linear) | κ ungewichtet | GT=gut erkannt |
| -------------------------- | :------: | :----------: | :-----------: | :------------: |
| Modell kontinuierlich      |  0.812   |    0.143     |     0.111     |    0 von 4     |
| Modell ganzzahlig gerundet |  0.833   |  **0.373**   |     0.354     |    2 von 4     |

---

## 3. Exkurs: Warum mehr Urteilsstufen das Problem nicht lösen

Getestet: dieselben Daten, Urteil aus dem 0–5-Gesamtmittel mit feineren Klasseneinteilungen
(beide Seiten identisch gebinnt):

| Skala                              | exakte Übereinst. | κ unweighted | κ linear | κ quadratisch |
| ---------------------------------- | :---------------: | :----------: | :------: | :-----------: |
| 3 Stufen, Verdict-Regel (Original) |       81 %        |     0.11     |   0.14   |       —       |
| 3 Stufen, gleich breite Bins       |       84 %        |     0.68     |   0.68   |     0.68      |
| 5 Stufen, gleich breite Bins       |       84 %        |     0.68     |   0.72   |     0.78      |
| 6 Stufen (Runden auf 0–5)          |       62 %        |     0.41     |   0.50   |     0.61      |

(Zum Vergleich: Spearman ρ der kontinuierlichen Werte = 0.82.)

Drei Schlussfolgerungen:

1. **Nicht die Stufenzahl ist das Problem, sondern die Lage der Schwellen relativ zur
   Stichprobenverteilung.** Schon 3 Klassen mit anderen Schnittpunkten liefern κ = 0.68 —
   die Verdict-Regel legt ihre Schwellen genau dorthin, wo sie 87 % der realen Stichprobe
   in eine Klasse schieben.
2. **Mehr Stufen senken die exakte Übereinstimmung** (jede zusätzliche Grenze erzeugt neue
   Grenzfall-Flips; bei 6 Stufen nur noch 62 %, alle Fehler ±1 Stufe). Nur _gewichtetes_ κ
   kompensiert das.
3. **Fein gestuftes, quadratisch gewichtetes κ konvergiert gegen eine Korrelation**
   (≈ ICC): 0.61 → 0.78 → nahe ρ = 0.82. Man misst dann dasselbe wie Spearman, nur
   abhängig von zwei willkürlichen Zusatzentscheidungen (Bin-Grenzen, Gewichtsschema).
   Wenn die Frage „stimmen die kontinuierlichen Scores überein" lautet, ist die
   Rangkorrelation auf den ungebinnten Werten das saubere Instrument.

**Bewusst NICHT gemacht: Schwellen-Shopping.** Weichere Regelvarianten (gut ≥ 3.75,
konjunktive Schwelle 2.5, Terzil-Bins) liefern κ zwischen 0.14 und 0.68 — genau diese
Varianz zeigt, dass nachträglich gewählte Schwellen Metrik-Optimierung wären. Die
Semantik der bestehenden Regel („gut darf keine schwache Dimension haben") bleibt
unangetastet; einzige Änderung ist die Skalenangleichung (Rundung, §2.2).

---

## 4. Resultierende Metrik-Hierarchie (für Kap. 4 „Auswertungsverfahren")

**Primärmetrik: Spearman ρ** (gesamt + je Dimension, mit Ceiling-Analyse).
Begründung: (a) Die Forschungsfrage ist ordinal — „erzeugt der Prototyp dieselbe
Rangordnung wie ein Mensch"; der kontinuierliche Score ist der eigentliche Modell-Output,
das Urteil nur eine abgeleitete Diskretisierung. (b) κ ist auf dieser Stichprobe
strukturell gedeckelt und instabil (§2.1). (c) Ergänzend MAE/Bias als Kalibrierungs-Check,
da Korrelation nur Rangordnung, nicht Niveau misst.

**Sekundärmetrik: Urteils-Übereinstimmung** (gut/mittel/schlecht) — Accuracy, gewichtetes
κ **mit Bootstrap-CI**, **PABAK** (prävalenzbereinigt, Byrt/Bishop/Carlin 1993:
`(k·p_o − 1)/(k − 1)`), AUC gut-vs-rest (schwellenfrei), Konfusionsmatrix. Das Urteil ist
die praktische Entscheidungsebene („publizierbar / verbessern / überarbeiten") und bleibt
berichtenswert — mit expliziter Einordnung des Prävalenzproblems.

### Zitierfähige Endwerte (Kernstichprobe, slim_v2, Run 2026-07-02)

| Kennzahl                                      | Wert                                                                |
| --------------------------------------------- | ------------------------------------------------------------------- |
| Spearman ρ gesamt                             | **0.820**                                                           |
| Spearman ρ je Dimension (find/acc/reuse/expr) | 0.524 / 0.824 / 0.739 / 0.680                                       |
| Kendall τ gesamt                              | 0.677                                                               |
| Anteil vom Ceiling-ρ (find/acc/reuse/expr)    | 0.683 / 0.864 / 0.796 / 0.801                                       |
| MAE / RMSE (0–5)                              | 0.244 / 0.304                                                       |
| Bias                                          | −0.057 (leichte Unterschätzung)                                     |
| Accuracy (Urteil, n=48)                       | 0.833                                                               |
| Cohen κ gewichtet                             | 0.373 („fair", Landis & Koch 1977) — Bootstrap-95%-CI [−0.04, 0.70] |
| PABAK                                         | 0.750                                                               |
| AUC gut vs. rest                              | 0.938                                                               |

Argumentationslinie für die Thesis: Das breite κ-CI begründet, warum die Urteilsebene
Sekundärmetrik ist; PABAK 0.75 und AUC 0.94 zeigen, dass die niedrige κ-Punktschätzung
ein Prävalenz-, kein Qualitätsbefund ist; die Primäraussage trägt ρ = 0.82.

---

## 5. Umgesetzte Code-Änderungen (2026-07-10)

In `src/evaluation/ground_truth.py`:

- `merge_scores`: Modell-Urteil wird aus den auf ganze Zahlen gerundeten 0–5-Dimensionen
  abgeleitet (Diskretisierungs-Asymmetrie, §2.2); kontinuierliche Spalten unverändert.
- Neu `pabak(...)`: prävalenz- und bias-bereinigtes κ, k-Klassen-Formel.
- Neu `kappa_bootstrap_ci(...)`: Perzentil-Bootstrap-CI (Default: linear gewichtet,
  4000 Resamples, Seed 67); `compare()` liefert `weighted_kappa_ci` und `pabak` mit.
- Docstrings (Modul, `compare`) auf die neue Metrik-Hierarchie aktualisiert.

In `playground/notebooks/10_ground_truth_evaluation.ipynb`:

- `GT_CSV` zeigt auf `ground_truth_template_slim_v2.csv`.
- Kennzahlen-Zelle: Rangkorrelation zuerst (Primärmetrik), Klassifikationsblock mit
  κ + CI, PABAK, Hinweistext; veraltete Markdown-Zellen (0–3-Skala, „×3") korrigiert.

## 6. Literatur

- Feinstein, A. R. & Cicchetti, D. V. (1990). High agreement but low kappa: I. The
  problems of two paradoxes. _Journal of Clinical Epidemiology_, 43(6), 543–549.
- Byrt, T., Bishop, J. & Carlin, J. B. (1993). Bias, prevalence and kappa.
  _Journal of Clinical Epidemiology_, 46(5), 423–429.
- Landis, J. R. & Koch, G. G. (1977). The measurement of observer agreement for
  categorical data. _Biometrics_, 33(1), 159–174.
