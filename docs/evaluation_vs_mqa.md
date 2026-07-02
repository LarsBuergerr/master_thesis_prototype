# Evaluation gegen MQA

> Beide Scorer (Prototyp und MQA-Re-Implementierung) laufen auf **identischem Input**;
> der Unterschied liegt ausschließlich in der Prüftiefe. Das A/B/C-Mapping klassifiziert
> jeden Prototyp-Indikator danach, wie er sich zur entsprechenden MQA-Metrik verhält —
> das ist die Basis beider zentralen Hypothesen.

## 1. Kernidee

**Presence-based vs. verification-based:** Die MQA bewertet überwiegend, *ob* ein Feld
vorhanden ist (presence), in einem Vokabular *gelistet* ist (lookup), per SHACL
DCAT-AP-konform ist oder eine URL auflöst. Sie nimmt Qualität bei Vorhandensein weitgehend
an. Der Prototyp **verifiziert**: Gültigkeit, Kongruenz, Tiefe und semantischen Gehalt.

Der Mehrwert verteilt sich in zwei Richtungen:
- **(B) MQA prüft schwächer** — PASS bei Presence/Listing, während der Prototyp
  Korrektheit/Kongruenz/Auflösbarkeit prüft.
- **(C) MQA prüft gar nicht** — kein MQA-Pendant; u. a. die gesamte semantische
  *expressiveness*-Dimension.

Die MQA-Re-Implementierung (`src/mqa/scorer.py`) folgt der offiziellen Methodik
[dataeuropa2024mqa] und läuft auf demselben RDF-Input wie der Prototyp.

## 2. Hypothesen

- **H1 (Konvergenz):** Auf den äquivalenten Checks (A-Indikatoren) stimmen beide Scorer
  hoch überein → der Prototyp bildet die etablierte MQA-Logik korrekt ab
  (*convergent validity* [campbell1959convergent]).

- **H2 (Mehrwert):** Auf B- und C-Indikatoren divergieren die Scores systematisch:
  MQA = PASS, Prototyp = FAIL/PARTIAL (Überschätzung durch MQA) bzw. MQA reagiert gar
  nicht, der Prototyp variiert (strukturelle Blindheit der MQA).

- **H3 (optional, Korrektheit):** Wo divergiert wird, stimmt der Prototyp besser mit einem
  externen Qualitätsurteil (Ground Truth) überein als die MQA. Erfordert
  Experten-Annotation; ohne Ground Truth lässt sich nur Divergenz, nicht Überlegenheit
  belegen (→ §6.2).

## 3. A/B/C-Klassifikationsschema

### 3.1 Schema-Definition

| Klasse | Bedeutung | Erwartung |
|--------|-----------|-----------|
| **A** – äquivalent | Prototyp und MQA prüfen im Kern dasselbe (Presence / Lookup / HTTP) | hohe Übereinstimmung (H1) |
| **B** – Prototyp strenger | MQA = PASS bei Vorhandensein; Prototyp verifiziert Gültigkeit/Kongruenz/Tiefe | MQA-PASS & Prototyp-FAIL als Überschätzungsnachweis (H2) |
| **C** – kein MQA-Pendant | MQA hat keine entsprechende Metrik (strukturell blind) | Prototyp variiert, MQA bleibt flach (H2) |

Die vollständige Indikator-Zuordnung liegt in `src/evaluation/indicator_map.py`:
jede Zeile enthält die zugeordneten MQA-Metriken, die Aggregationsregel (`any`/`all`),
eine `rationale`-Begründung und einen `review`-Flag für Grenzfälle.

### 3.2 Methodische Grundlage

Die A/B/C-Partitionierung entspricht klassischen Validitätsbegriffen aus der Messtheorie
[cronbach1955construct]:

- **A → convergent validity:** Zwei Operationalisierungen desselben Konstrukts sollten
  übereinstimmen [campbell1959convergent]. Hohe A-Übereinstimmung zeigt, dass der
  Prototyp keine zufälligen Artefakte produziert.
- **B → Operationalisierungstiefe:** Dieselbe Property, aber Presence vs. Validity.
  Die Hierarchie *Presence → Syntax → Semantics* ist in der Metadaten-Qualitätsliteratur
  etabliert [zaveri2016quality, neumaier2016automated]. Der Sprung von Presence auf
  Validity ist damit theoretisch fundiert, nicht willkürlich.
- **C → inkrementelle Validität:** Der Prototyp misst Aspekte, die strukturell außerhalb
  des MQA-Scope liegen.

Konzeptionell analog zum Multitrait-Multimethod-Ansatz [campbell1959convergent]: Hohe
A-Korrelation sichert das Fundament; B/C-Divergenz zeigt den eigenständigen Beitrag.

### 3.3 Implementierung

```
src/evaluation/indicator_map.py         ← A/B/C-Mapping-Tabelle (editierbar)
src/evaluation/indicator_join.py        ← Join-Harness: beide Scorer → Long-Table
                                           (file × indicator) mit A/B/C-Tags
playground/notebooks/
  11_mqa_indicator_comparison.ipynb     ← reproduzierbarer Vergleich
                                           (Konvergenz, Überschätzung, Blindheit)
data/sample_*/
  mqa_metrics.csv       ← MQA-Scores je (file, metric), gecacht
  model_indicators.csv  ← Prototyp-Scores je (file, indicator), gecacht
  indicator_join.csv    ← Join-Ergebnis als Long-Table
```

Die zentrale Vergleichseinheit ist der **Indikator**, nicht die Dimension: Der Mehrwert
ist über Indikatoren verteilt; eine Pro-Indikator-Klassifikation ist daher
aussagekräftiger als eine Dimensions-Gegenüberstellung.

### 3.4 Score-Normalisierung

- **MQA:** `mqa_points / mqa_max` je Datensatz.
- **Prototyp:** Pass-Rate (binärisiert: pass = 1, fail/partial = 0;
  not_applicable/error = NaN, ausgeschlossen).

Drei Vergleichsebenen getrennt halten:
1. **Gesamt** (inkl. C) — Netto-Effekt.
2. **Nur A** — Kontrolle für H1.
3. **B/C isoliert** — der eigentliche Mehrwert (H2).

## 4. Defizit-Katalog

### 4.1 B-Defizite (MQA überschätzt)

Nachweis-Muster: **MQA = PASS, Prototyp = FAIL/PARTIAL** → belegt, dass Presence ≠ Qualität.

| Indikator | MQA-Prüfung | Prototyp-Prüfung |
|-----------|-------------|------------------|
| `find_theme_valid` | `dcat:theme` vorhanden | Wert aus kontrolliertem Vokabular |
| `find_locn_geometry`, `find_political_geocoding` | `dct:spatial` vorhanden | echte `locn:geometry`/Admin-Einheit |
| `acc_media_type` | `dcat:mediaType` vorhanden | IANA-Vokabular-Mitgliedschaft |
| `acc_machine_readable_access` | Format im MR-Lookup | abgestufte echte Maschinenlesbarkeit |
| `reuse_publisher`, `reuse_contact` | Property vorhanden | strukturierter `foaf:Agent`/`vcard:Organization` |

### 4.2 C-Defizite (MQA strukturell blind)

Nachweis-Muster: **Prototyp-Score variiert, MQA = konstant** (keine Metrik vorhanden).

- **Semantisch leere Pflichtfelder:** Titel/Beschreibung vorhanden, aber inhaltsleer
  → `expr_title_quality`, `expr_description_quality`.
- **Platzhalter/Boilerplate:** generische/Copy-Paste-Texte → alle `expr_*`.
- **Inkohärenz Titel ↔ Beschreibung** → `expr_title_description_coherence`.
- **Bedeutungslose Keywords:** zählbar vorhanden (MQA: PASS), aber redundant/nichtssagend
  → `expr_keyword_quality`.
- **Thematische Inkonsistenz:** Theme/Keywords/Inhalt passen nicht → `expr_thematic_consistency`.
- **Keine MQA-Metrik (strukturell):** Update-Frequenz (`find_accrual_periodicity`),
  contributorID (`reuse_contributor_id`), Distributions-Modellierung (`acc_distribution_model`).

### 4.3 Balance (MQA prüft, Prototyp nicht)

Aspekte, die MQA prüft, der Prototyp aber nicht (`known_license`, `byte_size_availability`,
`rights_availability`, `dcat_ap_compliance` u. a.) — als `mqa_only_metrics()` in
`src/evaluation/indicator_map.py` ausgewiesen. Belegt, dass die Evaluation nicht einseitig
zugunsten des Prototyps konstruiert ist.

## 5. Stichprobe

Zwei-Schichten-Design:
- **(a) Zufalls-Sample** echter Datensätze (`data/sample_*/`) → zeigt, wie oft und relevant
  der Effekt in der Praxis ist.
- **(b) Kuratierte Kontrast-/Adversarial-Fälle** (`data/extreme_cases*`) → „strukturell
  perfekt, semantisch schlecht" → maximiert die erwartete B/C-Divergenz.

Kuratierte Fälle belegen den Mechanismus per Konstruktion — deshalb **zusätzlich** das
Zufalls-Sample als Bias-Kontrolle. Portal-Quelle, Datum und DCAT-AP-Version dokumentieren;
Daten + Scores als Replikationspaket ablegen.

## 6. Auswertung & Metriken

Implementiert in `playground/notebooks/11_mqa_indicator_comparison.ipynb`.

### 6.1 Ohne Ground Truth

- **[A] Konvergenz:** Agreement-Rate und Kontingenztabelle (beide PASS / beide FAIL /
  MQA-PASS+Prototyp-FAIL / Prototyp-PASS+MQA-FAIL) je A-Indikator.
- **[B] Überschätzung:** Anteil `MQA=PASS & Prototyp=FAIL` je B-Indikator
  (`overestimation_rate`).
- **[C] Blindheit:** Score-Verteilung (mean, std, min, max, n<0.5) je C-Indikator bei
  konstantem MQA-Score.
- **Gesamt-Scatter:** MQA-Score vs. Prototyp-Pass-Rate je Datensatz; Disagreement-Ranking
  nach `|Prototyp − MQA|`.
- **Method-Comparison (Bland–Altman):** Differenz gegen Mittelwert → systematischer Bias
  [blandaltman1986].
- **Klassifikations-Sicht:** Scores in Qualitätsbänder → Konfusionsmatrix, Cohen's κ
  [cohen1960kappa].

### 6.2 Mit Ground Truth (H3, optional)

- Experten-Rating blind gegenüber Modell-Scores (1–2 Annotator:innen).
- Inter-Rater-Reliabilität (Cohen's κ / Krippendorff's α) [krippendorff2004content] vor
  dem Modell-Vergleich berichten.
- Korrelation Prototyp↔GT vs. MQA↔GT vergleichen → höhere Korrelation = Evidenz für H3.
- Theoretischer Rahmen: Multitrait-Multimethod [campbell1959convergent],
  Composite-Vergleich [nardo2008handbook].

## 7. Validitäts-Hinweise

**Ohne Ground Truth** lässt sich nur *Divergenz*, nicht *Überlegenheit* belegen. Vertretbare
Formulierung: „Der Prototyp erfasst konzeptionell begründete Aspekte, die die MQA per
Design nicht sieht" — valide, aber schwächer als H3.

- **LLM-Stabilität:** `expr_*`-Indikatoren sind LLM-gestützt → Reproduzierbarkeit
  sicherstellen (temperature = 0, Run-zu-Run-MAE berichten), damit Mehrwert nicht von
  LLM-Rauschen trennbar ist.
- **A/B/C-Einstufung ist Interpretation:** jede Zeile gegen die MQA-Spec belegen;
  Grenzfälle (`review = True`, z. B. `acc_format_congruence` B vs. C) transparent machen.
- **MQA-Re-Implementierung:** gegen mindestens einen bekannten data.europa.eu-Report
  gegenprüfen; Methodikversion dokumentieren (Punkte-Maxima haben sich über die Versionen
  geändert).
- **Dimensionen-Mismatch:** MQA-*Contextuality* (`dct:issued`, `dct:modified`) und
  MQA-*Interoperability* (Format, MediaType) mappen nicht 1:1 auf die eigenen Dimensionen.
  Relevant nur für Pro-Dimension-Grafiken; die Indikator-Ebene ist davon unabhängig.

---

## BibTeX

```bibtex
@article{cronbach1955construct,
  title   = {Construct Validity in Psychological Tests},
  author  = {Cronbach, Lee J. and Meehl, Paul E.},
  journal = {Psychological Bulletin},
  volume  = {52},
  number  = {4},
  pages   = {281--302},
  year    = {1955},
  doi     = {10.1037/h0040957}
}

@article{zaveri2016quality,
  title   = {Quality Assessment for Linked Data: A Survey},
  author  = {Zaveri, Amrapali and Rula, Anisa and Maurino, Andrea and Pietrobon, Ricardo
             and Lehmann, Jens and Auer, S{\"o}ren},
  journal = {Semantic Web},
  volume  = {7},
  number  = {1},
  pages   = {63--93},
  year    = {2016},
  doi     = {10.3233/SW-150175}
}

@article{neumaier2016automated,
  title   = {Automated Quality Assessment of Metadata across Open Data Portals},
  author  = {Neumaier, Sebastian and Umbrich, J{\"u}rgen and Polleres, Axel},
  journal = {Journal of Data and Information Quality (JDIQ)},
  volume  = {8},
  number  = {1},
  pages   = {1--29},
  year    = {2016},
  doi     = {10.1145/2964909}
}

@article{campbell1959convergent,
  title   = {Convergent and Discriminant Validation by the Multitrait-Multimethod Matrix},
  author  = {Campbell, Donald T. and Fiske, Donald W.},
  journal = {Psychological Bulletin},
  volume  = {56},
  number  = {2},
  pages   = {81--105},
  year    = {1959},
  doi     = {10.1037/h0046016}
}

@article{blandaltman1986,
  title   = {Statistical Methods for Assessing Agreement between Two Methods of Clinical Measurement},
  author  = {Bland, J. Martin and Altman, Douglas G.},
  journal = {The Lancet},
  volume  = {327},
  number  = {8476},
  pages   = {307--310},
  year    = {1986},
  doi     = {10.1016/S0140-6736(86)90837-8}
}

@article{cohen1960kappa,
  title   = {A Coefficient of Agreement for Nominal Scales},
  author  = {Cohen, Jacob},
  journal = {Educational and Psychological Measurement},
  volume  = {20},
  number  = {1},
  pages   = {37--46},
  year    = {1960},
  doi     = {10.1177/001316446002000104}
}

@book{krippendorff2004content,
  title     = {Content Analysis: An Introduction to Its Methodology},
  author    = {Krippendorff, Klaus},
  year      = {2004},
  edition   = {2nd},
  publisher = {Sage},
  address   = {Thousand Oaks, CA}
}

@book{nardo2008handbook,
  title     = {Handbook on Constructing Composite Indicators: Methodology and User Guide},
  author    = {Nardo, Michela and Saisana, Michaela and Saltelli, Andrea and Tarantola,
               Stefano and Hoffman, Anders and Giovannini, Enrico},
  year      = {2008},
  publisher = {OECD Publishing},
  address   = {Paris},
  doi       = {10.1787/9789264043466-en}
}

@misc{dataeuropa2024mqa,
  title        = {Metadata Quality Assessment (MQA) — Data Quality Guidelines},
  author       = {{data.europa.eu}},
  howpublished = {\url{https://op.europa.eu/webpub/op/data-quality-guidelines/en/}},
  year         = {2024},
  note         = {Publications Office of the European Union, accessed 2026-06-16}
}
```
