# Die Evaluation, einfach erklärt

Diese Datei dröselt auf, was in Kapitel 5 der Thesis eigentlich passiert: welche Frage
gestellt wird, womit sie beantwortet wird, welche Zahl was bedeutet und wo die Zahlen
herkommen. Sie ist als Nachschlagewerk gedacht, nicht als Fließtext.

Stand: 05.08.2026. Alle Zahlen aus `outputs/thesis_kennzahlen_final.json`
(erzeugt von `playground/notebooks/18_evaluation_kapitel5_final.ipynb`).

---

## 1. Die Grundidee in drei Sätzen

Der Prototyp vergibt Punkte für Metadatenqualität. Damit stellt sich sofort die Frage:
**Sind diese Punkte irgendetwas wert?** Die Evaluation beantwortet das mit zwei
Vergleichen — einmal gegen einen Menschen, einmal gegen ein etabliertes Verfahren.

| Vergleich | Frage | Wogegen |
|---|---|---|
| **Strang 1: Ground Truth** | Bewertet der Prototyp *korrekt*? | Manuelle Bewertung durch einen Menschen |
| **Strang 2: MQA** | Sieht der Prototyp *mehr*? | Metadata Quality Assessment von data.europa.eu |

Warum beides nötig ist: Der MQA-Vergleich allein zeigt nur, dass die beiden Verfahren
sich unterscheiden. Er kann nicht sagen, *wer recht hat*. Dafür braucht es den
menschlichen Maßstab.

---

## 2. Die drei Hypothesen

Alles in Kapitel 5 zahlt auf genau drei Aussagen ein.

| | Behauptung | Wie belegt |
|---|---|---|
| **H1** | Wo Prototyp und MQA dasselbe prüfen, kommen sie zum selben Ergebnis. | Übereinstimmungsrate auf Klasse-A-Indikatoren |
| **H2** | Wo der Prototyp tiefer prüft, weichen die Ergebnisse ab. | Überschätzungsrate (Klasse B), Score-Streuung bei flacher MQA (Klasse C) |
| **H3** | Wo sie abweichen, liegt der Prototyp näher am Menschen. | Beide gegen die Ground Truth (Triangulation) |

**H3 trägt die eigentliche Aussage.** H2 allein würde nur zeigen, dass *anders* gemessen
wird — nicht, dass *besser* gemessen wird. Das ist der Punkt, an dem eine Verteidigung
hängen bleibt, deshalb steht H3 nicht ohne Grund am Ende.

---

## 3. Die Datengrundlage

```
GovData-CKAN-Katalog, 15.05.2026        151.579 Datensätze
  − NetCDF-Datensätze                     −1.793   (zu groß, hätte die Laufzeit dominiert)
  = Grundgesamtheit                      149.786
      ├─ Geo                              25.416
      └─ Nicht-Geo                       124.370
```

Daraus werden **zwei Stichproben** gezogen, die unterschiedliche Aufgaben haben:

### Kernstichprobe (n = 50)

Stratifizierte Zufallsziehung vom 25.06.2026, Seed 67, reproduzierbar über
Notebook 12. Zweistufig geschichtet:

1. Geo / Nicht-Geo
2. innerhalb beider Gruppen: die vier aufkommensstärksten Bereitsteller + Restkategorie

→ 10 Straten × 5 Datensätze = 50.

*Warum geschichtet?* Bei einer einfachen Zufallsziehung würden die paar riesigen Portale
den Großteil der Stichprobe stellen. Die Schichtung erzwingt Vielfalt.

**Alle quantitativen Aussagen der Arbeit stützen sich auf diese Stichprobe.**

### Extremfälle (n = 20)

Handverlesen: 10 erwartbar gute, 10 erwartbar schlechte Datensätze. Das ist ein
**Stresstest, keine Statistik** — weil die Auswahl konstruiert ist, lässt sich daraus
nichts auf die Grundgesamtheit verallgemeinern. Sie beantworten eine andere Frage:
*Trennt das Verfahren überhaupt, wenn der Unterschied offensichtlich ist?*

Deshalb werden beide Schichten **getrennt** ausgewertet und nie zusammengeworfen.

---

## 4. Die Ground Truth — der menschliche Maßstab

Ein Mensch bewertet alle 50 (bzw. 20) Datensätze entlang derselben vier Dimensionen wie
der Prototyp, auf einer Skala **0 bis 5**, mit **einer Ankerfrage je Dimension**.

| Dimension | Ankerfrage (verkürzt) |
|---|---|
| Auffindbarkeit | Ist der Datensatz über Titel, Beschreibung, Schlagwörter, Kategorien, Raum/Zeit findbar und einordenbar? |
| Zugänglichkeit | Ist die Ressource erreichbar, abrufbar, maschinenlesbar, technisch plausibel beschrieben? |
| Nachnutzbarkeit | Sind Lizenz, Rechte, Kontakt, Herausgeber, Vokabulare klar genug für eine Weiterverwendung? |
| Aussagekraft | Sind Titel, Beschreibung, Schlagwörter, Kontextangaben verständlich, plausibel, informationshaltig? |

**Drei Entwurfsentscheidungen, die man kennen muss:**

- **Die Anker beschreiben die Nutzererfahrung, nicht die Indikatorlogik.** Es steht dort
  „kann ein Nutzer den Datensatz finden?", nicht „ist `dct:title` belegt?". Sonst würde
  die Ground Truth nur den Prototyp nachrechnen und der Vergleich wäre wertlos
  (Campbell & Fiske: methodische Unabhängigkeit).
- **Nur eine Frage je Dimension, keine Beschreibung je Stufe.** Stufenbeschreibungen
  müssten benennen, woran sich 3 von 4 unterscheidet — und würden dafür genau die
  Merkmale heranziehen, die der Prototyp prüft. Der Preis: die Einzelwerte sind weniger
  gut reproduzierbar.
- **Blind bewertet.** Die Bewertungsvorlage enthält nur den Metadateninhalt, keine
  Prototyp-Scores. Sonst hätte man sich unbewusst an den Maschinenwerten orientiert
  (Anchoring-Bias) und die Übereinstimmung künstlich hochgetrieben.

Aus den vier Dimensionswerten wird ein Gesamturteil abgeleitet:

| Urteil | Durchschnitt | Zusatzbedingung |
|---|---|---|
| gut | ≥ 4,0 | keine Dimension < 3 |
| schlecht | ≤ 2,0 | — |
| | oder < 3,5 | mindestens zwei Dimensionen < 2 |
| mittel | alle übrigen Fälle | |

Die Zusatzbedingung ist der Kern: ohne sie könnte ein Spitzenwert in einer Dimension
eine gravierende Lücke in einer anderen wegmitteln.

**Bekannte Schwäche:** ein einziger Bewerter, also keine Inter-Rater-Reliabilität
bestimmbar. Gegengesteuert mit Kalibrierung an fünf Beispielen, kurzen Sitzungen und
markierten Zweifelsfällen.

---

## 5. Die MQA-Baseline — das etablierte Verfahren

Die MQA von data.europa.eu wurde **nachgebaut** (nicht angefragt), damit beide Verfahren
exakt dieselben RDF-Dateien bewerten. Die Reimplementierung ist reines
Evaluationswerkzeug und gehört nicht zum Prototyp.

**Der inhaltliche Unterschied, um den sich alles dreht:**

| | MQA | Prototyp |
|---|---|---|
| prüft | *ob* ein Feld da ist | *ob es stimmt* |
| Beispiel | „`dct:format` ist gesetzt" → Punkt | „…und der Wert steht im EU-Vokabular" |

Um das messbar zu machen, bekommt **jeder Prototyp-Indikator eine Klasse**:

| Klasse | Bedeutung | Anzahl | Erwartung |
|---|---|---|---|
| **A** | prüft im Kern dasselbe wie eine MQA-Metrik | 9 | hohe Übereinstimmung → H1 |
| **B** | MQA honoriert Vorhandensein, Prototyp verifiziert Gültigkeit | 9 | MQA-PASS + Prototyp-FAIL = Überschätzung → H2 |
| **C** | kein MQA-Pendant (u. a. die ganze Aussagekraft) | 9 | MQA blind, Prototyp differenziert → H2 |

Vollständige Zuordnung: Anhang der Thesis, generiert aus `src/evaluation/indicator_map.py`.

**Fairness:** Umgekehrt gibt es zwei MQA-Metriken ohne Prototyp-Pendant
(`rights_availability`, `byte_size_availability`). Beide Felder sind nach DCAT-AP.de
weder Pflicht noch Empfehlung. Das steht bewusst in der Thesis, damit der Vergleich
nicht einseitig wirkt.

---

## 6. Die Kennzahlen — was misst was?

Das ist die Stelle, an der man am ehesten den Überblick verliert. Sortiert nach Zweck:

### Rangkorrelation — „stimmt die Reihenfolge?"

| Kennzahl | Was sie sagt | Bereich |
|---|---|---|
| **Spearman ρ** | **Primärmetrik.** Ordnet der Prototyp die Datensätze genauso wie der Mensch? | −1 … +1 |
| Kendall τ | dasselbe, robustere Variante | −1 … +1 |

*Warum ρ und nicht Genauigkeit?* Weil die Forschungsfrage ordinal ist. Der Score ist das
eigentliche Ergebnis; das Urteil gut/mittel/schlecht ist nur eine daraus abgeleitete
Vergröberung.

### Kalibrierung — „stimmt auch das Niveau?"

Rangkorrelationen sind blind für systematische Verschiebungen: Ein Verfahren, das alles
konstant um 2 Punkte zu niedrig bewertet, hat trotzdem ρ = 1,0.

| Kennzahl | Was sie sagt |
|---|---|
| **MAE** | mittlerer absoluter Abstand zum Menschen |
| **Bias** | Richtung des Fehlers: positiv = zu großzügig, negativ = zu streng |

### Urteilsebene — „liegt die Ampel richtig?"

| Kennzahl | Was sie sagt |
|---|---|
| Accuracy | Anteil exakt getroffener Urteile |
| gewichtetes κ | Übereinstimmung, zufallsbereinigt |
| **PABAK** | dasselbe, aber um die schiefe Verteilung bereinigt |
| AUC gut-vs-Rest | Trennschärfe ohne feste Schwelle |
| Konfusionsmatrix | wer wurde wohin verwechselt |

### Das Kappa-Problem (wichtig!)

87 % der Ground-Truth-Datensätze liegen in der Kategorie *mittel*. Dadurch liegt die
**zufällig erwartbare Übereinstimmung schon bei ~0,79**. Selbst ein perfektes Verfahren
könnte hier kein hohes κ erreichen — das ist das **Kappa-Paradox** (Feinstein &
Cicchetti 1990).

> Eine niedrige κ-Zahl ist hier ein **Befund über die Datenlage**, kein Qualitätsmangel
> des Prototyps. Genau deshalb ist ρ die Primärmetrik und κ nur Sekundärmetrik, und
> genau deshalb wird PABAK mitberichtet.

Bewusst *nicht* gemacht: die Urteilsschwellen nachträglich so verschieben, dass κ besser
aussieht. Das wäre Metrik-Optimierung statt Messung.

### Ceiling-Analyse — „wie viel war überhaupt drin?"

Berechnet, welches ρ bei der vorliegenden Ground-Truth-Verteilung *maximal* erreichbar
wäre, und setzt den beobachteten Wert ins Verhältnis. Fängt den Einwand ab, ein Wert von
0,52 sei „schlecht" — wenn das Maximum bei 0,77 liegt, sind das 68 % des Möglichen.

### MQA-spezifisch

| Kennzahl | Für | Was sie sagt |
|---|---|---|
| Übereinstimmungsrate | Klasse A | wie oft beide gleich urteilen |
| Überschätzungsrate | Klasse B | wie oft MQA PASS gibt, wo der Prototyp FAIL sieht |
| Score-Streuung | Klasse C | ob der Prototyp differenziert, wo die MQA flach bleibt |
| Bland-Altman | gesamt | ob die Abweichung über den Wertebereich stabil ist |

---

## 7. Die Modellauswahl — warum GPT-5.5?

**Der entscheidende Rahmen zuerst:** Von vier Dimensionen ist nur die **Aussagekraft**
LLM-gestützt. Die anderen drei werden deterministisch aus dem RDF berechnet und sind
über alle Modelle hinweg **bitgenau identisch** (ρ = 0,524 / 0,712 / 0,739).

→ Die Modellwahl berührt genau ein Viertel des Verfahrens. Gesamtkennzahlen mischen den
identischen Teil bei und verwässern den Vergleich, deshalb wird auf der Aussagekraft
entschieden.

| | GPT-5.5 | Opus 4.8 | Sonnet 4.6 |
|---|---|---|---|
| **ρ Aussagekraft** (Primär) | 0,569 | 0,608 | 0,598 |
| ρ gesamt | 0,765 | 0,770 | 0,745 |
| Accuracy | 0,92 | 0,90 | 0,88 |
| κ gewichtet | 0,635 | 0,508 | 0,359 |
| AUC | 0,907 | 0,902 | 0,876 |
| MAE | 0,289 | 0,275 | 0,308 |
| Bias | +0,018 | −0,018 | −0,144 |
| **Kosten / 50 Dateien** | **1,79 $** | 4,10 $ | 2,02 $ |

**Wichtig: GPT-5.5 gewinnt die Primärmetrik nicht.** Opus liegt vorn, Sonnet ebenfalls.
Die Argumentation folgt trotzdem sauber der in 5.5 vorab festgelegten Hierarchie und
nicht dem Muster „Modell X gewinnt bei A, B und C" — das wäre nachträgliches
Zusammensuchen passender Argumente. Sie läuft in drei Schritten:

1. **Opus 4.8 scheidet am Aufwand aus.** Doppelte Kosten (4,10 $ gegenüber ~2 $) ohne
   belastbaren Vorsprung: 0,010 vor Sonnet, 0,040 vor GPT — Abstände, die **kleiner sind
   als die Schwankung eines einzelnen Modells zwischen Wiederholungsläufen**.
2. **Die Primärmetrik trennt GPT-5.5 und Sonnet 4.6 nicht.** Der Abstand beträgt 0,029
   (bzw. 0,028 auf der Wiederholungsstichprobe) bei einer Streuung von σ = 0,023 — das
   1,2-fache des Rauschens, mit überlappenden Wertebereichen. Nicht von Zufall zu
   unterscheiden.
3. **Also entscheiden die nachgeordneten Kriterien**, und die zeigen geschlossen auf
   GPT-5.5. Am deutlichsten die **Kalibrierung**: Sonnet unterschätzt die Aussagekraft
   systematisch um 0,723 Skalenpunkte (~15 % der Skalenbreite), GPT nur um 0,077. Dazu
   Accuracy, κ, PABAK, AUC und die Zahl korrekt erkannter guter Datensätze (3 von 5
   gegenüber 1 von 5) — und die niedrigsten Kosten.

### Reproduzierbarkeit (Wiederholungsläufe, n = 30)

Dieselben Dateien mehrfach durch dasselbe Modell:

| | GPT-5.5 | Sonnet 4.6 |
|---|---|---|
| Spanne der Lauf-Mittelwerte | 0,0004 | 0,0063 |
| Standardabweichung je Datensatz | 0,0046 | 0,0082 |
| MAE zwischen Läufen | 0,0059 | 0,0107 |
| ρ zwischen Läufen | 0,993 | 0,991 |
| höchster Statuswechsel-Anteil | 16,7 % | 46,7 % |

Der letzte Wert ist der aufschlussreichste: Bei Sonnet kippt ein einzelnes Kriterium
(`expr_contextual_qualifiers`) in fast der Hälfte der Wiederholungen die Ergebnisstufe.

> **Achtung bei der Interpretation:** Die Score-Streuung ist winzig, aber genau deshalb
> nicht harmlos. Wenn benachbarte Datensätze im Mittel 0,0083 auseinanderliegen und das
> Rauschen bei 0,0150 liegt, ist die *Rangordnung* in diesem Bereich nicht stabil — auch
> wenn die *Werte* es sind. Das ist der Grund, warum Abbildungen mit Spannweiten und
> Tabellen mit Standardabweichungen auf den ersten Blick zu widersprechen scheinen.

---

## 8. Die Ergebnisse

### Ground Truth, Kernstichprobe (n = 50)

| Kennzahl | Wert |
|---|---|
| **ρ gesamt** | **0,765** |
| ρ Auffindbarkeit | 0,524 (68 % vom Ceiling) |
| ρ Zugänglichkeit | 0,712 (75 % vom Ceiling) |
| ρ Nachnutzbarkeit | 0,739 (80 % vom Ceiling) |
| ρ Aussagekraft | 0,569 (67 % vom Ceiling) |
| Accuracy | 0,92 |
| κ gewichtet | 0,635 (KI 0,18 – 0,92) |
| PABAK | 0,88 |
| AUC | 0,907 |
| MAE / Bias | 0,289 / +0,018 |

Der Bias von +0,018 ist praktisch null — der Prototyp ist weder systematisch zu
großzügig noch zu streng. Das breite κ-Konfidenzintervall ist das eigentliche Argument
gegen κ als Entscheidungsgrundlage.

### Ground Truth, Extremfälle (n = 20)

| Kennzahl | Wert |
|---|---|
| ρ gesamt | 0,827 |
| ρ Auffindbarkeit / Nachnutzbarkeit | 0,874 / 0,872 |
| ρ Aussagekraft | 0,321 |
| Accuracy | 0,50 |
| mittlerer Score „konstruiert schlecht" | 2,10 |
| mittlerer Score „konstruiert gut" | 4,06 |

Die Trennung funktioniert (2,10 vs. 4,06), aber die Urteils-Accuracy bricht auf 0,50 ein
— bei extremen Fällen liegen die Werte nah an den Urteilsschwellen, und die Aussagekraft
korreliert hier deutlich schlechter. Beides gehört ehrlich berichtet.

### MQA-Vergleich, Kernstichprobe

**Klasse A (H1 — Konvergenz):**

| | |
|---|---|
| Prüfungen | 450 |
| **Übereinstimmung** | **96 %** |
| beide PASS / beide FAIL | 298 / 134 |
| MQA PASS, Prototyp FAIL | 17 |
| Prototyp PASS, MQA FAIL | 1 |

→ H1 bestätigt: Der Prototyp bildet die etablierte Logik korrekt ab.

**Klasse B (H2 — Überschätzung):** z. B. `find_political_geocoding` mit einer
Überschätzungsrate von **56 %** — in 28 von 50 Fällen gibt die MQA einen Punkt, wo der
Prototyp den Wert als ungültig erkennt. Die Asymmetrie ist durchgängig: 0-mal urteilt
der Prototyp großzügiger.

**Klasse C (H2 — blinder Fleck):** z. B. `reuse_availability`, wo die MQA gar nicht
hinschaut und alle 50 Datensätze durchfallen.

**Gesamtvergleich:** ρ = 0,829 zwischen beiden Verfahren, mittlere Differenz −0,022 —
sie messen erkennbar dasselbe Konstrukt, aber nicht identisch.

**Triangulation (H3 — die entscheidende Tabelle):** beide gegen die Ground Truth:

| Ziel | Prototyp | MQA | Δ |
|---|---|---|---|
| **gesamt (4 Dim.)** | **0,779** | **0,740** | **+0,038** |
| ohne Aussagekraft (3 Dim.) | 0,695 | 0,671 | +0,024 |
| Auffindbarkeit | 0,134 | 0,252 | **−0,119** |
| Zugänglichkeit | 0,591 | 0,569 | +0,022 |
| Nachnutzbarkeit | 0,457 | 0,426 | +0,031 |
| Aussagekraft | 0,682 | 0,611 | +0,071 |

→ H3 in der Tendenz bestätigt, aber **nicht überall**: Bei der Auffindbarkeit liegt die
MQA näher am Menschen. Der Gesamtvorsprung von +0,038 ist zudem klein. Das gehört so
berichtet — ein durchgängiger Vorsprung wäre verdächtig.

Bei den Extremfällen ist der Abstand deutlicher (0,845 vs. 0,699, Δ = +0,146), was
plausibel ist: Dort liegen genau die Fälle, bei denen tiefere Prüfung den Unterschied
macht.

---

## 9. Wo liegt was?

| Was | Wo |
|---|---|
| Alle Kennzahlen, konsolidiert | `outputs/thesis_kennzahlen_final.json` |
| Erzeugendes Notebook | `playground/notebooks/18_evaluation_kapitel5_final.ipynb` |
| Stichprobenziehung | `playground/notebooks/12_fetch_stratified_sample.ipynb` |
| Ground-Truth-Auswertung | `playground/notebooks/10_ground_truth_evaluation.ipynb` |
| MQA-Indikatorvergleich | `playground/notebooks/11_mqa_indicator_comparison.ipynb` |
| Wiederholungsläufe | `playground/notebooks/14_run_konsistenz_vergleich.ipynb` |
| Abbildungen Modellauswahl | `playground/notebooks/15_modellauswahl_abbildungen.ipynb` |
| Abbildungen GT / MQA | `playground/notebooks/16_…` / `17_…` |
| Bewertete Stichprobe (RDF) | `data/sample_2026-06-25_09-57/` |
| Ground-Truth-Template | `data/sample_2026-06-25_09-57/ground_truth_template_slim_v2.csv` |
| A/B/C-Zuordnung | `src/evaluation/indicator_map.py` |
| Bewertungskonfiguration | `conf/state/state_evaluation_final.yaml` |
| Bewertungsläufe | `outputs/runs/` |

---

## 10. Die ehrlichen Schwachstellen

Damit sie nicht in der Verteidigung als Überraschung kommen:

1. **Ein einziger Ground-Truth-Bewerter.** Keine Inter-Rater-Reliabilität bestimmbar.
2. **n = 50.** Klein. Trägt Rangkorrelationen, aber die κ-Konfidenzintervalle sind breit.
3. **Extremfälle sind konstruiert.** Keine Verallgemeinerung möglich, deshalb strikt
   getrennt ausgewertet.
4. **Der H3-Vorsprung ist klein** (+0,038) und bei der Auffindbarkeit negativ.
5. **Die MQA ist nachgebaut**, nicht die Originalimplementierung — validiert gegen die
   veröffentlichten Berichte, aber eben nachgebaut.
6. **Die LLM-Bewertung ist nicht bitgenau reproduzierbar.** Die Streuung ist klein, aber
   in dichten Score-Bereichen kann sie die Rangordnung drehen.
