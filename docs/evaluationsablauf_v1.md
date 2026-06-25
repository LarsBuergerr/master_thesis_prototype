# Evaluationsablauf — Gesamtstruktur

> Stand: 25.06.2026. Basiert auf `evaluations_aufbau.md` und
> `methodik_evaluation_ground_truth_v2.md`.
> Sample: `sample_2026-06-25_09-57`, Seed 67, n=50 + 10 Extremfälle.

---

## Übersicht der Evaluationsschritte

| # | Schritt | Zweck | Werkzeug / Methode |
|---|---------|-------|--------------------|
| 1 | Indikatorgewichte herleiten | Weighted Config begründen | B-Analyse (NB11) + DCAT-AP.de MUST-Felder |
| 2 | Dimensionsgewichte herleiten | Weighted Config begründen | MQA-Punktesystem + FAIR-Literatur |
| 3 | LLM-Selektion | Bestes Modell für Expressiveness finden | Expressiveness-Only-Runs, mehrere Modelle |
| 4 | Stabilitätsnachweis | Deterministik des gewählten LLM zeigen | n Wiederholungsläufe, Varianzanalyse |
| 5 | Ground Truth erstellen | Externer menschlicher Maßstab | Manuelles Labeling, blind, 0–3 pro Dimension |
| 6 | Prototyp vs. GT | H3 vorbereiten, Modell validieren | Spearman ρ, Cohen's κ je Dimension + Gesamt |
| 7 | MQA vs. GT | H3 direkt testen | Gleiche Metriken wie Schritt 6 |
| 8 | Prototyp vs. MQA (Indikator-Ebene) | H1 + H2 testen | NB11: Konvergenz (A), Überschätzung (B), Blindheit (C) |

Die Extremfall-Stichprobe (10 Datensätze) dient als Illustration für Schritte 1–2
und läuft **nicht** in die statistischen Tests ein.

---

## Schritt 1 — Indikatorgewichte: datengetriebene Herleitung

**Werkzeug:** B-Analyse aus Notebook 11 (`indicator_join.py`).

Die B-Indikatoren sind genau die Fälle, wo MQA mit Presence-Checks durchwinkt,
was der Prototyp ablehnt. Die Weighted Config bestraft diese Indikatoren gezielt
stärker — das ist keine Annahme, sondern aus den Disagreement-Daten abgeleitet:

| Indikator | MQA-Überschätzung | Gewichtungs-Rationale |
|-----------|-------------------|-----------------------|
| `find_adminunitl2` | 58 % | MQA akzeptiert beliebige `dct:spatial`-URIs → Gewicht erhöht |
| `find_keywords_count` | 40 % | MQA = 1 Keyword reicht → Gewicht erhöht |
| `reuse_contact` | 29 % | MQA = Presence genügt → Gewicht erhöht |
| `acc_machine_readable_access` | 4 % | Niedriger Disagreement → Gewicht bleibt moderat |

**Ergänzende Begründung:** DCAT-AP.de kennzeichnet bestimmte Felder als
Pflichtanforderung (MUST/SOLL gemäß Konventionenhandbuch). Indikatoren, die
auf Pflichtfelder mappen (`reuse_license`, `acc_download_url`, `reuse_contact`),
erhalten in der Weighted Config höhere Gewichte — das ist spec-konform und
unabhängig von den Evaluationsdaten begründbar.

---

## Schritt 2 — Dimensionsgewichte: literaturbasierte Herleitung

Dimensionsgewichte lassen sich **nicht** sinnvoll empirisch gegen eine GT validieren
(n=50 zu klein, Effekte zu gering). Stattdessen: Begründung über zwei externe
Referenzpunkte.

### 2a. MQA-Punktesystem als Referenz

MQA gewichtet Dimensionen implizit durch sein Punktesystem
[dataeuropa2024mqa]:

| MQA-Dimension | Punkte | Anteil |
|---------------|--------|--------|
| Findability | 100 | 24,7 % |
| Accessibility | 100 | 24,7 % |
| Interoperability | 110 | 27,2 % |
| Reusability | 75 | 18,5 % |
| Contextuality | 20 | 4,9 % |

Die eigene Weighted Config orientiert sich an dieser impliziten Priorisierung:
Accessibility und Reusability werden relativ stärker gewichtet, weil sie
die Nachnutzbarkeit direkt bestimmen.

### 2b. FAIR-Prinzipien

Das FAIR-Prinzip *Accessible* (A) ist besonders kritisch: ein nicht-abrufbarer
Datensatz ist unabhängig von allen anderen Qualitätsmerkmalen wertlos
[wilkinson2016fair]. Das rechtfertigt ein höheres Dimensionsgewicht für
Accessibility.

### Fazit für die Thesis

Die Dimensionsgewichte werden als *begründete Designentscheidung* ausgewiesen,
nicht als empirisch validierte Größe. Zwei unabhängige Quellen (MQA-Punktesystem
+ FAIR) stützen die Richtung. Der Extremfall-Sample zeigt qualitativ, dass die
Weighted Config gute/schlechte Datensätze stärker auseinanderzieht als die
Default Config — das ist Illustration, kein statistischer Beweis.

---

## Schritt 3 — LLM-Selektion (Expressiveness)

**Vorgehen:**
- Nur die Expressiveness-Dimension mit verschiedenen Modellen laufen lassen
  (kein Token-Verbrauch für strukturelle Indikatoren)
- Kandidaten: mindestens zwei Modelle unterschiedlicher Größenklasse
  (z. B. `qwen3.5` lokal vs. `claude-sonnet-4.5` über OpenRouter)
- Vergleich gegen GT-Expressiveness-Scores (Spearman ρ)
- Das Modell mit der höchsten Korrelation zur GT wird als Produktivmodell gewählt

**Begründung der Methodik:** Selektion via Korrelation mit menschlichem Urteil
ist Standard für LLM-as-Judge-Evaluationen [zheng2023judging].

---

## Schritt 4 — Stabilitätsnachweis

**Problem:** LLM-Outputs sind stochastisch. Wenn `temperature=0` gesetzt ist,
sollten Runs auf identischem Input identische Ergebnisse liefern — das muss
aber empirisch gezeigt werden, weil manche Provider trotzdem leichte
Variationen produzieren.

**Vorgehen:**
- Gewähltes Modell mit `temperature=0` auf der großen Stichprobe (n=50)
  mindestens 3× laufen lassen
- Varianz der Expressiveness-Scores je Datensatz berechnen
- Akzeptanzkriterium: σ < 0.05 im Mittel → Ergebnisse gelten als stabil

**Ausgabe:** Boxplot der Score-Varianz über Wiederholungsläufe.

---

## Schritt 5 — Ground Truth erstellen

Methodikdetails in `methodik_evaluation_ground_truth_v2.md`. Kurzfassung:

- **Sample:** n=50 (stratifiziert) + 10 Extremfälle separat
- **Skala:** 0–3 pro Dimension (4 Stufen, Forced Choice, Anchored Rubric)
- **Dimensionen:** Auffindbarkeit, Zugänglichkeit, Nachnutzbarkeit, Aussagekraft
- **Blind:** Bewertung ohne Kenntnis der Modell-Scores
- **Gesamturteil:** gut / mittel / schlecht per Regelwerk (siehe v2-Methodik)

### Warum 0–3 ausreicht (und nicht feiner sein muss)

Die GT wird **nicht** für den Config-Vergleich (Default vs. Weighted) eingesetzt.
Für ihren tatsächlichen Zweck — Ranking-Übereinstimmung auf Gesamt- und
Dimensionsebene — sind 4 Stufen ausreichend. Vier Stufen entsprechen dem
MQA-Bändermodell (Bad/Sufficient/Good/Excellent) und sind bei Expert-Rubrics
reliabilitätsoptimal [dawes2008fivepoint, jonsson2007rubrics].

Der Config-Vergleich würde selbst mit einer feineren GT-Skala bei n=50 keine
statistisch belastbaren Unterschiede in Spearman ρ liefern (zu geringe Power).
Das ist kein Fehler der GT-Methodik, sondern ein Stichprobenproblem — und der
Grund, warum Config-Justifikation in Schritt 1–2 über andere Wege läuft.

### Begründung der Dimensionswahl

Die vier Dimensionen sind direkt aus dem Prototyp übernommen (keine eigene
Konstruktion). Die Ankerpunkte je Dimension unterscheiden sich bewusst von
den exakten Indikator-Formeln des Prototyps — damit die GT nicht nur die eigene
Modelllogik nachrechnet, sondern echte konvergente Validität misst
[campbell1959convergent].

---

## Schritt 6 — Prototyp vs. Ground Truth

**Konfiguration:** Bestes LLM (aus Schritt 3) + Weighted Config.

**Metriken:**
- **Pro Dimension:** Spearman ρ (Modell-Score 0–1 ↔ GT-Grade 0–3)
- **Gesamturteil:** Accuracy + Cohen's κ (gewichtet, gut > mittel > schlecht)
- **Trennschärfe:** Modell-Score-Verteilung je GT-Grade (Boxplots)
- **Konfusionsmatrix:** Modell-Klasse × GT-Klasse

**Erwartung:** Spearman ρ > 0.5 pro Dimension, Cohen's κ > 0.4 gesamt.

**Getrennte Auswertung:** Kernstichprobe (n=50) und Extremfälle (n=10) separat
berichten — die Extremfälle belegen den Mechanismus per Konstruktion, die
Kernstichprobe ist die unverzerrte Schätzung.

---

## Schritt 7 — MQA vs. Ground Truth (H3)

**Vorgehen:** MQA-Scores auf denselben 50 Datensätzen mit denselben GT-Labels
vergleichen. Gleiche Metriken wie Schritt 6.

**Hypothese H3:** Der Prototyp korreliert stärker mit der GT als die MQA
(Spearman ρ\_Prototyp > Spearman ρ\_MQA).

**Warum das zu erwarten ist:** MQA ist auf Presence-Checks optimiert und
unterschätzt Qualitätsprobleme systematisch (belegt durch Schritt 8 / B-Analyse).
Ein Modell, das tiefer prüft, sollte dem menschlichen Urteil näher kommen.

**Fallback:** Falls H3 nicht gezeigt werden kann — das Ergebnis ist trotzdem
interpretierbar. MQA deckt einen anderen Qualitätsbegriff ab (formal-strukturell)
als das menschliche Urteil (inhaltlich-funktional). Eine fehlende Überlegenheit
wäre dann kein Fehler des Prototyps, sondern ein Befund über die Grenzen von
Presence-basierten Metriken.

---

## Schritt 8 — Prototyp vs. MQA auf Indikator-Ebene (H1 + H2)

Bereits implementiert in Notebook 11. Läuft auf der großen Stichprobe (n=50).

**H1 (Konvergenz auf A-Indikatoren):** Übereinstimmungsrate > 90 % belegt,
dass der Prototyp die MQA-Basislogik korrekt abbildet → die Erweiterungen
bauen auf einer validierten Grundlage auf.

**H2 (Überschätzung durch MQA):** B-Indikatoren zeigen wo MQA systematisch
PASS gibt, der Prototyp ablehnt. C-Indikatoren zeigen, wo MQA strukturell
blind ist und der Prototyp differenziert.

---

## Was absichtlich nicht gemacht wird

| Was | Warum nicht |
|-----|-------------|
| Config-Vergleich via GT | n=50 zu gering für belastbare ρ-Unterschiede; falsches Werkzeug |
| GT mit > 3 Stufen | Mehr Stufen = schlechtere Reliabilität bei Einzelbewerter; kein Gewinn für H3 |
| Dimensionsgewichte empirisch validieren | Dimensionsgewichte verändern nur Aggregation, nicht Dimension-Scores; GT kann das bei dieser n nicht auflösen |
| Extremfall-Sample in statistische Tests | Construct-by-design → kein repräsentativer Test; nur Illustration |

---

## Literatur (ergänzend zu v2-Methodik)

```bibtex
@article{wilkinson2016fair,
  title   = {The FAIR Guiding Principles for Scientific Data Management and Stewardship},
  author  = {Wilkinson, Mark D. and others},
  journal = {Scientific Data},
  volume  = {3},
  pages   = {160018},
  year    = {2016},
  doi     = {10.1038/sdata.2016.18}
}

@article{dawes2008fivepoint,
  title   = {Do Data Characteristics Change According to the Number of Scale Points Used?},
  author  = {Dawes, John},
  journal = {International Journal of Market Research},
  volume  = {50},
  number  = {1},
  pages   = {61--77},
  year    = {2008},
  doi     = {10.1177/147078530805000106}
}

@inproceedings{zheng2023judging,
  title     = {Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena},
  author    = {Zheng, Lianmin and others},
  booktitle = {Advances in Neural Information Processing Systems},
  volume    = {36},
  year      = {2023}
}
```
