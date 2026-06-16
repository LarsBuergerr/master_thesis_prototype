# Evaluation gegen MQA

> Rohstichpunkte zur späteren Ausformulierung. Plan: eigenes Modell und die MQA
> auf derselben Stichprobe laufen lassen, Defizite der MQA definieren, die das
> eigene Modell adressiert, und prüfen, ob sich das im Score niederschlägt.
> Quellen am Ende als BibTeX.

## 0. Kernidee in einem Satz

- **Presence-based vs. verification-based**: Die MQA bewertet überwiegend, _ob_
  ein Feld vorhanden ist (presence), in einem Vokabular _gelistet_ ist (lookup),
  per SHACL DCAT-AP-konform ist oder eine URL auflöst. Sie nimmt Qualität bei
  Vorhandensein weitgehend an. Das eigene Modell **verifiziert** die Qualität:
  Gültigkeit, Kongruenz, Tiefe und semantischen Gehalt.
- Der Mehrwert ist **nicht** auf die Dimension _expressiveness_ beschränkt,
  sondern verteilt sich über die Indikatoren in zwei Richtungen:
  - **(B) MQA prüft schwächer** als das eigene Modell (PASS bei Presence/Listing,
    während der eigene Indikator Korrektheit/Kongruenz/Auflösbarkeit prüft).
  - **(C) MQA prüft gar nicht** (kein MQA-Pendant; u. a. die gesamte semantische
    _expressiveness_-Dimension).
- These der Evaluation: Es existieren Datensätze, die in der MQA hoch punkten
  (alle Felder vorhanden, Vokabular-konform), deren Metadaten aber tatsächlich
  ungültig/inkongruent/semantisch arm sind — diese soll das eigene Modell
  systematisch niedriger bewerten, die MQA nicht.
- Konzeptioneller Anschluss: der Gegensatz _completeness/presence_ vs.
  _accuracy/conformance_ entspricht den Metadaten-Qualitätsdimensionen von
  [bruce2004continuum]; die Kritik, dass portal-basierte Checks meist nur
  Vorhandensein messen, bei [neumaier2016automated].

## 1. Forschungsfrage & Hypothesen

- **RQ**: Erkennt das eigene Modell Qualitätsdefizite, die die MQA konstruktions-

bedingt nicht erfassen kann, und schlägt sich das im Score nieder?

- **H1 (Konvergenz)**: Auf den geteilten (strukturellen) Dimensionen korrelieren

beide Scores hoch → das Modell ist kein Zufallsprodukt, sondern bildet die

etablierte MQA-Logik ab (_convergent validity_).

- **H2 (Divergenz/Mehrwert)**: Auf der Teilmenge mit semantischen Defiziten

divergieren die Scores systematisch (MQA hoch, eigenes Modell niedrig)

(_discriminant validity_).

- **H3 (optional, Korrektheit)**: Wo divergiert wird, stimmt das eigene Modell

besser mit einem externen Qualitätsurteil (Ground Truth) überein als die MQA.

## 2. MQA als Vergleichsbaseline beschaffen (praktischer Knackpunkt)

- Es gibt **noch keine** lokale MQA-Implementierung im Prototyp; MQA wird bisher

nur als Gewichtungs-Referenz in Kommentaren genannt.

- Die offizielle MQA von data.europa.eu lässt sich nicht direkt auf lokale RDFs

anwenden (sie bewertet nur vom Portal geharvestete Metadaten).

- Optionen, MQA-Scores für dieselbe Stichprobe zu erzeugen:

- **(A) MQA-Algorithmus lokal nachbauen** nach der offiziellen Methodik

(Metriken + Punktetabelle je FAIR-Dimension) [dataeuropa2024mqa]. Saubere,

reproduzierbare Variante; Punktelogik ist dokumentiert.

- **(B) Vorhandene Implementierung nutzen** (z. B. die offenen MQA-Scoring-/

SHACL-Ressourcen) und an das eigene Input-Format anpassen.

- **(C) DCAT-AP-SHACL-Validierung + MQA-Punktetabelle** kombinieren.

- Empfehlung: **(A)** als schlanke, transparente Re-Implementierung — Methodik

und Punktevergabe im Anhang dokumentieren (Nachvollziehbarkeit/Reproduzier-

barkeit der Baseline).

- Wichtig: **MQA-Version + Stand dokumentieren** (Methodik ändert sich; Punkte-

maxima haben sich über die Versionen geändert).

## 3. Indikator-Mapping & Relation zur MQA (Kern der Auswertung)

> Die zentrale Vergleichseinheit ist der **Indikator**, nicht die Dimension. Der
> Mehrwert liegt verteilt über Indikatoren (stärkere Prüfung + nicht abgedeckte
> Aspekte), daher ist eine Pro-Indikator-Klassifikation aussagekräftiger als eine
> Dimensions-Gegenüberstellung.

### 3.1 Klassifikationsschema (A/B/C)

- **A – äquivalent**: MQA prüft im Kern dasselbe (Presence / Vokabular-Lookup /
  HTTP-Auflösbarkeit). Hier wird Konvergenz erwartet (H1).
- **B – eigenes Modell prüft strenger**: MQA = PASS bei Vorhandensein/Listing,
  während der eigene Indikator Gültigkeit, Kongruenz, Auflösbarkeit oder Tiefe
  verifiziert. → MQA kann **überschätzen**.
- **C – kein MQA-Pendant**: MQA hat dafür keine Metrik (strukturell blind).

### 3.2 Klassifikationstabelle (Erstentwurf — gegen MQA-Spec prüfen)

| Relation | Indikatoren                                                                                                                                                                                                                                                                                           | MQA vs. eigenes Modell                                        |
| -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| **A**    | `find_keywords_count`, `find_temporal_coverage`, `acc_download_url`, `acc_download_url_response`, `acc_access_url_response`, `acc_format`, `reuse_license`, `reuse_access_rights`, `reuse_publisher`, `find_issued_datetime`, `find_modified_datetime`                                                | beide prüfen Presence / Vokabular / HTTP                      |
| **B**    | `find_theme_valid` (Vokabular-Gültigkeit statt nur Presence), `find_locn_geometry`, `find_adminunitl2` (echte Geometrie/Admin-Einheit statt nur `dct:spatial`), `acc_media_type`, `acc_machine_readable_access` (echte, abgestufte Maschinenlesbarkeit statt Listen-Lookup), `reuse_contact` (graded) | MQA passt bei Vorhandensein durch; eigenes Modell verifiziert |
| **C**    | `acc_format_congruence` (Format↔MIME-Kongruenz), `acc_distribution_model`, `find_accrual_periodicity`, `reuse_contributor_id` (DCAT-AP-DE), **alle `expr_*`**                                                                                                                                         | MQA hat keine entsprechende Metrik                            |

- `acc_format_congruence` ist je nach Lesart B oder C (MQA hat keine
  Kongruenz-Metrik) — als „verschärft + nicht abgedeckt" führen.

### 3.3 Wie man die Klassifikation erstellt

1. **MQA-Metrikliste** aus der offiziellen Methodik extrahieren (Metrik, geprüfte
   RDF-Property, Prüfart: presence / vocabulary / SHACL / HTTP, Punkte)
   [dataeuropa2024mqa].
2. Für **jeden** eigenen Indikator den MQA-Gegenpart suchen (gleiche/ähnliche
   Property).
3. Prüf-_Tiefe_ vergleichen, nicht nur die Property: prüft MQA nur Vorhandensein,
   du aber Gültigkeit/Kongruenz/Auflösbarkeit/Semantik? → **B**. Kein Gegenpart?
   → **C**. Gleiche Tiefe? → **A**.
4. Jede Zeile mit der konkreten MQA-Prüflogik **belegen** (Zitat/Verweis auf die
   Spec), damit B/C nicht behauptet, sondern gezeigt ist.
5. Ergebnis ist gleichzeitig der **Defizit-Katalog** (Abschnitt 4) und die
   Vorhersage, _wo_ Score-Divergenz auftreten muss.

### 3.4 Score-Normalisierung

- Beide Modelle auf gemeinsame Skala bringen (z. B. 0–1 oder 0–100), sonst sind
  Scores nicht vergleichbar.
- Drei Vergleichsebenen sauber trennen:
  - **Gesamtscore** (inkl. expressiveness) — Netto-Effekt.
  - **Reduziertes Modell** (nur A-Indikatoren) vs. MQA — Kontrolle für H1
    (bilden die geteilten Checks dasselbe ab?).
  - **B/C-Indikatoren isoliert** — der eigentliche Mehrwert (H2).

### 3.5 Dimensions-Mapping (optional, nur für Pro-Dimension-Darstellung)

> Für die Argumentation **nicht** nötig (Mehrwert liegt auf Indikator-Ebene).
> Nur sinnvoll, falls eine saubere Dimensions-Grafik gewünscht ist. Achtung: die
> eigenen Dimensionen mappen **nicht** 1:1 (MQA hat 5 Dimensionen, 405 Punkte):
> die eigene `accessibility` mischt MQA-_Accessibility_ (download/access URL) und
> MQA-_Interoperability_ (Format, MediaType, Maschinenlesbarkeit, DCAT-Konformität,
> 110 P.); `find_issued/modified_datetime` zählen in MQA zu _Contextuality_, nicht
> _Findability_. Für eine Pro-Dimension-Grafik die Indikator-Scores entsprechend
> in MQA-Buckets re-aggregieren (kein Prototyp-Umbau nötig).

## 4. Defizit-Katalog & Nachweis je Klasse

> Leitet sich direkt aus der A/B/C-Tabelle (Abschnitt 3) ab. Pro Defizit: was MQA
> tut, was das eigene Modell zusätzlich tut, erwartete Score-Wirkung, und wie man
> es am Datensatz **nachweist**.

### 4.1 B-Defizite (MQA überschätzt — prüft schwächer)

> Nachweis-Muster: Datensatz finden, bei dem **MQA = PASS**, der eigene Indikator
> aber **FAIL/PARTIAL**. Genau diese Fälle belegen, dass Presence ≠ Qualität.

- **Ungültiges Theme/Vokabular**: `dcat:theme` vorhanden (MQA: PASS), aber Wert
  nicht aus dem kontrollierten Vokabular → `find_theme_valid` FAIL.
- **Format ohne echte Geometrie/Admin-Einheit**: `dct:spatial` vorhanden
  (MQA: PASS), aber keine auswertbare Geometrie / kein Vokabular-Bezug
  → `find_locn_geometry`, `find_adminunitl2`.
- **Inkongruentes Format**: deklariertes Format ≠ tatsächlicher MIME/Inhalt
  (MQA prüft Kongruenz nicht) → `acc_format_congruence`.
- **Schein-Maschinenlesbarkeit**: Format im MR-Lookup, aber faktisch nicht/teils
  maschinenlesbar → `acc_machine_readable_access` (graded niedriger).
- **Tote/abweichende URLs an der Grenze**: MQA-Auflösbarkeit grob (HTTP<400),
  eigene Prüfung feiner → ggf. Divergenz bei `acc_*_url_response`.

### 4.2 C-Defizite (MQA strukturell blind — keine Metrik)

> Nachweis-Muster: Score des eigenen Modells reagiert auf das Defizit, der
> MQA-Score **gar nicht** (flach), weil keine Metrik existiert.

- **Semantisch leere Pflichtfelder**: Titel/Beschreibung vorhanden, aber inhalts-
  leer („Datensatz", „data", Dateiname) → `expr_title_quality`,
  `expr_description_quality`.
- **Platzhalter / Boilerplate**: generische/Copy-Paste-Texte über viele Datensätze
  → `expr_*`.
- **Inkohärenz Titel ↔ Beschreibung**: widersprüchlich/themenfremd
  → `expr_title_description_coherence`.
- **Schlechte Keywords**: vorhanden & zählbar (MQA: PASS), aber bedeutungslos/
  redundant → `expr_keyword_quality` (vs. reines Zählen).
- **Thematische Inkonsistenz**: Theme/Keywords/Inhalt passen nicht zusammen
  → `expr_thematic_consistency`.
- **Fehlende Zusatz-Metadaten ohne MQA-Metrik**: Update-Frequenz
  (`find_accrual_periodicity`), contributorID (`reuse_contributor_id`),
  Modellierungs-Kohärenz (`acc_distribution_model`).

### 4.3 Balance (ehrlich)

- **A-Indikatoren** und **MQA-only-Metriken** (Aspekte, die MQA prüft, das eigene
  Modell aber nicht — z. B. `dcat:byteSize`/Größe, ggf. Landing Page) ebenfalls
  auflisten → zeigt, dass die Bewertung nicht einseitig zugunsten des eigenen
  Modells gebaut ist.

## 5. Stichprobe / Sampling

- **Zwei-Schichten-Design**:

- **(a) Kuratierte Kontrast-/Adversarial-Fälle** (vgl. `data/extreme_cases*`):

gezielt „strukturell perfekt, semantisch schlecht" konstruieren → maximiert

die erwartete Divergenz, demonstriert den Mechanismus.

- **(b) Repräsentatives Zufalls-Sample** echter Datensätze (vgl.

`data/sample_*`) → zeigt, wie oft/relevant der Effekt in der Praxis ist.

- Stichprobengröße begründen; bei kleiner Stichprobe → Fallstudien-/qualitativer

Charakter explizit machen.

- Sampling-Verfahren & Quelle (Portal, Datum, DCAT-AP-Version) dokumentieren.

- Daten + Scores als Replikationspaket ablegen.

## 6. Auswertung & Metriken

### Übereinstimmung & Divergenz (ohne Ground Truth)

- **Rangkorrelation** beider Scores: Spearman ρ / Kendall τ (gesamt und je

Schicht). Erwartung: hoch im strukturellen Teil (H1), niedriger/abweichend bei

Defizitfällen (H2).

- **Method-Comparison-Plot (Bland–Altman)**: Differenz (eigenes − MQA) gegen

Mittelwert → zeigt systematischen Bias & wo die Modelle auseinanderlaufen

[blandaltman1986].

- **Streudiagramm** MQA vs. eigenes Modell, Defizitfälle farblich markiert →

„MQA hoch / eigenes niedrig"-Quadrant ist die Kern-Evidenz.

- **Disagreement-Analyse**: Datensätze nach |Score-Differenz| ranken; Top-Fälle

qualitativ inspizieren (zeigt _warum_ divergiert wird).

- **Klassen-aufgelöste Divergenz (A/B/C)**: Score-Beitrag bzw. PASS/FAIL je

Indikator-Klasse getrennt auswerten. Erwartung: A ≈ deckungsgleich (H1),

Divergenz konzentriert sich auf B (MQA PASS / eigenes FAIL-PARTIAL) und C

(MQA reagiert nicht). Zähltabelle „MQA PASS & eigenes FAIL" je B-Indikator ist

direkter Beleg für die Überschätzung.

- **Klassifikations-Sicht**: beide Scores in Qualitätsklassen (z. B. MQA

Excellent/Good/Sufficient/Bad) binnen → Konfusionsmatrix, Cohen's κ

[cohen1960kappa].

### Korrektheit (mit Ground Truth — für H3)

- Externes Qualitätsurteil nötig, um „besser" statt nur „anders" zu zeigen:

- **Experten-Rating** der Stichprobe (1–2 unabhängige Annotator:innen) auf

einer Qualitätsskala, idealerweise blind ggü. beiden Modell-Scores.

- **Inter-Rater-Reliabilität** berichten (Cohen's κ / Krippendorff's α)

[cohen1960kappa, krippendorff2004content].

- Dann: Korrelation Modell↔GroundTruth vs. MQA↔GroundTruth vergleichen

→ höhere Korrelation = besseres Modell.

- Theoretischer Rahmen für „verschiedene Methoden messen dasselbe Konstrukt":

**Multitrait-Multimethod / Konvergenz- & Diskriminanzvalidität**

[campbell1959convergent]; Composite-Vergleich via Korrelationsanalyse

[nardo2008handbook].

## 7. Validitäts-Hinweis (ehrlich)

- **Ohne Ground Truth** lässt sich nur _Divergenz_ belegen, nicht _Überlegenheit_.

Die Aussage „mein Modell ist besser" braucht ein externes Kriterium (Abschnitt

6, H3). Sonst bleibt es bei „mein Modell erfasst zusätzliche, konzeptionell

begründete Aspekte, die MQA per Design nicht sieht" — auch valide, aber

schwächer formulieren.

- Eigene `expr_*`-Indikatoren sind **LLM-gestützt** → vor der Modell-vs-MQA-

Evaluation deren **Reliabilität** absichern (Determinismus bei temperature=0,

ggf. Übereinstimmung LLM↔Mensch), sonst ist der Mehrwert nicht von LLM-Rauschen

trennbar. (Vgl. bestehendes `docs/finetuning_expressiveness_judge.md`.)

## 8. Threats to Validity (Diskussion)

- **Construct**: Die A/B/C-Einstufung je Indikator ist eine Interpretation der

MQA-Prüftiefe → jede Zeile gegen die MQA-Spec belegen; Grenzfälle (z. B.

`acc_format_congruence` B vs. C) transparent machen. Dimensionen mappen nicht

1:1 (MQA-Interoperability/Contextuality) — nur relevant für Pro-Dimension-Sicht.

- **Internal**: korrekte/aktuelle MQA-Re-Implementierung (gegen Referenz prüfen).

- **External**: Generalisierbarkeit bei kleinem/extreme-lastigem Sample.

- **Bias**: kuratierte Defizitfälle „beweisen" den Effekt fast per Konstruktion →

deshalb zusätzlich das Zufalls-Sample (Abschnitt 5b).

- **LLM-Stabilität**: Nicht-Determinismus / Modell-Drift der expressiveness-Bewertung.

## 9. Konkrete Schritte (Pipeline)

1. MQA lokal re-implementieren (Variante A) + gegen mind. einen bekannten

data.europa.eu-Report gegenprüfen.

2. Indikator→MQA-Mapping + A/B/C-Klassifikation (Abschnitt 3) erstellen und gegen
   die MQA-Spec belegen; Score-Normalisierung festlegen.

3. Stichprobe finalisieren (Kontrastfälle + Zufalls-Sample).

4. Beide Modelle batch-weise auf identischem Input laufen lassen; Scores +

Dimensions-Subscores je Datensatz exportieren.

5. (für H3) Experten-Rating einholen, IRR berechnen.

6. Auswertung: Korrelationen, Bland–Altman, Scatter, Disagreement-Tabelle,

Konfusionsmatrix.

7. Defizit-Katalog (Abschnitt 4) an konkreten Disagreement-Fällen belegen.

---

## BibTeX-Quellen

```bibtex

@article{neumaier2016automated,

title = {Automated Quality Assessment of Metadata across Open Data Portals},

author = {Neumaier, Sebastian and Umbrich, J{\"u}rgen and Polleres, Axel},

journal = {Journal of Data and Information Quality (JDIQ)},

volume = {8},

number = {1},

pages = {1--29},

year = {2016},

publisher = {ACM},

doi = {10.1145/2964909}

}



@article{campbell1959convergent,

title = {Convergent and Discriminant Validation by the Multitrait-Multimethod Matrix},

author = {Campbell, Donald T. and Fiske, Donald W.},

journal = {Psychological Bulletin},

volume = {56},

number = {2},

pages = {81--105},

year = {1959},

doi = {10.1037/h0046016}

}



@article{blandaltman1986,

title = {Statistical Methods for Assessing Agreement between Two Methods of Clinical Measurement},

author = {Bland, J. Martin and Altman, Douglas G.},

journal = {The Lancet},

volume = {327},

number = {8476},

pages = {307--310},

year = {1986},

doi = {10.1016/S0140-6736(86)90837-8}

}



@article{cohen1960kappa,

title = {A Coefficient of Agreement for Nominal Scales},

author = {Cohen, Jacob},

journal = {Educational and Psychological Measurement},

volume = {20},

number = {1},

pages = {37--46},

year = {1960},

doi = {10.1177/001316446002000104}

}



@book{krippendorff2004content,

title = {Content Analysis: An Introduction to Its Methodology},

author = {Krippendorff, Klaus},

year = {2004},

edition = {2nd},

publisher = {Sage},

address = {Thousand Oaks, CA}

}



@book{nardo2008handbook,

title = {Handbook on Constructing Composite Indicators: Methodology and User Guide},

author = {Nardo, Michela and Saisana, Michaela and Saltelli, Andrea and Tarantola, Stefano and Hoffman, Anders and Giovannini, Enrico},

year = {2008},

publisher = {OECD Publishing},

address = {Paris},

doi = {10.1787/9789264043466-en}

}



@misc{dataeuropa2024mqa,

title = {Metadata Quality Assessment (MQA) -- Data Quality Guidelines},

author = {{data.europa.eu}},

howpublished = {\url{https://op.europa.eu/webpub/op/data-quality-guidelines/en/}},

year = {2024},

note = {Publications Office of the European Union, accessed 2026-06-16}

}

```
