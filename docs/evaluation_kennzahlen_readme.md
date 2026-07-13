# Evaluations-Kennzahlen — Spickzettel

Alle Zahlen auf einen Blick, mit Ein-Satz-Erklärung. Stand: **2026-07-13**,
Referenz-Run `run_2026-07-13_13-21-40_state-evaluation-final_EVAL` (Scoring-Stand:
Z7 ohne Malus, Gewicht 1.5), Ground Truth `ground_truth_template_slim_v2.csv`, n = 50.
Quellen: Notebook 10 (Ground Truth), Notebook 11 (MQA-Vergleich + Triangulation),
Vertiefung in `ground_truth_kennzahlen_kappa_analyse.md`.

> Achtung: Nach jeder Scoring- oder Config-Änderung Run + Notebooks neu laufen
> lassen — dann ändern sich alle Werte hier. MQA-Werte können durch die
> HTTP-Probes minimal schwanken.

---

## 1. Ground-Truth-Evaluation (Prototyp vs. Mensch, Notebook 10)

### Primärmetrik: Rangkorrelation

| Kennzahl | Wert | Sagt aus |
|---|---|---|
| Spearman ρ gesamt | **0.765** | Der Prototyp bringt die Datensätze in fast dieselbe Qualitäts-Reihenfolge wie der Mensch (1.0 = identisch, 0 = kein Zusammenhang). |
| Kendall τ gesamt | 0.638 | Dasselbe, anderes Rechenverfahren (konservativer) — Absicherung, dass ρ kein Artefakt ist. |

Wichtig: Basis ist das **ungewichtete** Mittel der vier Modell-Dimensionen vs. das
ungewichtete Mittel der vier Handbewertungen (symmetrisch, prüft die *Messung*,
nicht die Gewichtungsentscheidung).

### Pro Dimension (Spearman ρ)

| Dimension | ρ | Sagt aus |
|---|---|---|
| Reusability | **0.739** | Stärkste Übereinstimmung mit dem Menschen. |
| Accessibility | 0.712 | Gut — trotz der bekannten Login-Wall-Grenze (s.u.). |
| Expressiveness | 0.664 | Die LLM-Dimension misst valide — zentral, weil MQA das gar nicht kann. |
| Findability | 0.524 | Am schwächsten: präsenz-lastige Dimension, wenig Varianz im menschlichen Urteil. |

### Fehlergröße (0–5-Skala)

| Kennzahl | Wert | Sagt aus |
|---|---|---|
| MAE | **0.263** | Modell und Mensch liegen im Schnitt nur ~0.26 Skalenpunkte auseinander. |
| RMSE | 0.352 | Wie MAE, bestraft Ausreißer stärker — kein großer Abstand zu MAE = keine wilden Ausreißer. |
| Bias | **+0.013** | Praktisch null: Das Modell über- oder unterschätzt nicht systematisch. |

### Gesamturteil gut / mittel / schlecht (Sekundärmetrik)

| Kennzahl | Wert | Sagt aus |
|---|---|---|
| Accuracy | **0.860** | 43 von 50 Urteilen exakt getroffen. |
| Cohen's κ (gewichtet) | 0.405 | Zufallskorrigierte Übereinstimmung — niedrig, **aber irreführend** (siehe Kasten unten). |
| Bootstrap-CI für κ | [−0.06, 0.74] | Bei n=50 mit nur 6 Nicht-mittel-Fällen ist κ extrem unsicher — noch ein Grund, es nicht als Hauptmetrik zu nehmen. |
| PABAK | **0.790** | κ nach Korrektur des Prävalenzproblems — zeigt: Das Instrument ist gut, die Stichprobe ist nur homogen. |
| AUC (gut vs. Rest) | **0.876** | Schwellenfrei: Der kontinuierliche Score trennt "gute" Datensätze zuverlässig vom Rest — unabhängig davon, wo man die Urteilsgrenzen zieht. |

Konfusionsmatrix: schlecht 1/1 richtig, mittel 40/44 richtig, gut 2/5 richtig
(3 gut→mittel verpasst, 4 mittel→gut zu großzügig).

### ⚠️ Warum ist Cohen's κ so niedrig? (Das Kappa-Paradox)

Ganz einfach: **44 von 50 Datensätzen sind "mittel".** κ zieht die
Zufallsübereinstimmung ab — und wenn fast alles in einer Klasse liegt, ist
"zufällig richtig" schon bei ~80 %. Selbst ein sehr gutes Instrument kann dann
kaum noch κ-Punkte holen. Das ist ein bekanntes Problem der Kennzahl
(**Kappa-Paradox**, Feinstein & Cicchetti 1990), nicht des Prototyps:
86 % Accuracy und PABAK 0.79 zeigen die tatsächliche Güte. Deshalb ist
Spearman ρ die Primärmetrik und κ wird nur berichtet + erklärt.
Die Urteils-Schwellen wurden bewusst **nicht** nachträglich angepasst — Tuning an
der Evaluationsstichprobe (6 Nicht-mittel-Fälle!) wäre zirkulär; die AUC belegt
die Trennschärfe schwellenfrei.

---

## 2. Prototyp vs. MQA (Notebook 11)

### Indikator-Ebene (A/B/C-Mapping, 27 aktive Indikatoren)

| Kennzahl | Wert | Sagt aus |
|---|---|---|
| [A] Konvergenz | **96.0 %** | Auf den 9 äquivalenten Checks stimmen beide fast immer überein → der Prototyp bildet die etablierte Baseline korrekt ab (Validitätsnachweis). |
| [B] Überschätzung | **15.8 %** (71/450) | In jedem 6. B-Fall sagt MQA PASS, wo der Prototyp (der Gültigkeit statt Präsenz prüft) FAIL sagt → MQA nimmt Qualität an, die nicht da ist. |
| [B] Spitzenreiter | political_geocoding **56 %** | MQA akzeptiert jedes `dct:spatial`; der Prototyp verlangt das DCAT-AP.de-Vokabular. |
| [C] Blindheit | 9 Indikatoren, 169/450 Fälle < 0.5 | Für 9 Prototyp-Indikatoren hat MQA **gar keine Metrik** — und dort findet der Prototyp massenhaft echte Mängel (z.B. Beschreibungsqualität: Ø 0.40). |

### Gesamtscore-Vergleich

| Kennzahl | Wert | Sagt aus |
|---|---|---|
| Pearson r | ~0.85 | Beide Gesamtscores hängen stark zusammen. |
| Spearman ρ | ~0.84 | Beide ranken die Datensätze sehr ähnlich. |
| Ø Δ (Prototyp − MQA) | ~−0.02 | Im Niveau fast gleich — der Prototyp ist global *nicht* pauschal strenger. |

**Warum so hoch, obwohl der Prototyp strenger prüft?** (1) Korrelation misst
Reihenfolge, nicht Niveau — gleichmäßige Strenge ändert ρ nicht. (2) Defekte
clustern: Wer Felder schlampig füllt, schreibt auch schlechte Beschreibungen —
beide Systeme messen denselben "Sorgfalts-Faktor". (3) Bei ~23 Indikatoren
verschiebt eine einzelne strengere Prüfung den Gesamtscore nur um ~0.02–0.04.
Die Unterschiede sieht man daher nicht im Mittelwert, sondern auf Indikator-
([B], [C]) und Fallebene — genau das ist die These.

---

## 3. Triangulation: Wer liegt näher am Menschen? (Notebook 11, §9)

Beide System-**Gesamtscores** gegen die manuelle Ground Truth (Spearman ρ):

| Ziel (menschliches Urteil) | Prototyp | MQA | Δ |
|---|---|---|---|
| GT gesamt (4 Dim.) | **0.793** | 0.740 | +0.05 |
| GT ohne Expressiveness (3 Dim.) | **0.711** | 0.671 | +0.04 |
| GT Expressiveness | **0.713** | 0.611 | **+0.10** |
| GT Accessibility | **0.596** | 0.569 | +0.03 |
| GT Reusability | **0.467** | 0.426 | +0.04 |
| GT Findability | 0.169 | **0.252** | −0.08 |

**Lesart:** Der Prototyp rankt näher am Menschen — insgesamt, sogar ohne seinen
Expressiveness-Vorteil (d.h. die strengeren Validitätsprüfungen allein zahlen sich
aus), und mit dem größten Abstand genau bei der Inhaltsqualität, die MQA
strukturell nicht misst (MQAs 0.611 dort ist nur geerbt: Inhaltsqualität
korreliert mit struktureller Pflege). Ehrlicher Kontrapunkt: Bei Findability
(präsenz-lastig, MQAs Heimspiel) liegt MQA vorn — beide aber schwach.

**Warum hier 0.793 statt 0.765 aus Abschnitt 1?** Anderes Modell-Aggregat:
0.765 = ungewichtetes Dimensionsmittel (prüft die Messung), 0.793 = produktiver
gewichteter `overall_score` (prüft das Endprodukt, fair gegen MQAs Endscore).
Nebenbefund: Die a priori festgelegte Gewichtung rückt den Score näher ans
menschliche Urteil (0.765 → 0.793) — ein Validierungsargument für die
Gewichtungsentscheidung.

---

## 4. Bekannte Grenzen (ehrlich bleiben)

- **n = 50, Einzelannotator:** ρ-Differenzen von ~0.05 sind nicht
  inferenzstatistisch abgesichert → als konsistente Richtung verkaufen, nicht als
  Signifikanz.
- **Login-Wall (`geo_gdi-de`):** Download-URL liefert HTTP 200 mit Login-Seite
  statt der Daten — Mensch erkennt es, weder Prototyp noch MQA können es →
  dokumentierte Messgrenze + Future Work (Auth-Erkennung).
- **Findability:** schwächste Dimension auf beiden Seiten; im Modell bewusst
  niedrig gewichtet.
- **κ-Kalibrierung:** Eine belastbare Verdict-Kalibrierung bräuchte eine separate,
  qualitätsheterogene Stichprobe (mehr gut/schlecht-Fälle) → Future Work.
