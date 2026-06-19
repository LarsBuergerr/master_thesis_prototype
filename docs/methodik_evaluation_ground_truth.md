# Methodik: Evaluation gegen Ground Truth

> Manuelle Bewertung einer Stichprobe als externer Maßstab, um zu prüfen ob der Prototyp
> dieselbe Rangordnung erzeugt wie ein Mensch — und ob er dabei besser abschneidet als die
> MQA (H3 aus `docs/evaluation_vs_mqa.md`).

## 1. Sampling-Strategie

**Stratifizierte purposive Stichprobe mit ergänzenden Extremfällen.**

Die Kernstichprobe deckt zentrale Unterschiede der GovData-Datenbasis ab:
- Themenbereiche (`dcat:theme`)
- Datenbereitsteller / Contributor
- Zugriffstypen (Datei, API, Data Service, Landing Page)
- Formatgruppen (CSV/JSON/XML, PDF/HTML, Geoformate, unklare Formate)
- Technische Vorqualität (erreichbare vs. nicht erreichbare Ressourcen)

Die ergänzenden Extremfälle dienen als Stresstest:
- **Erwartbar gut:** klare Beschreibung, erreichbare Ressource, maschinenlesbares Format,
  Lizenz, Kontakt, kontrollierte Vokabulare.
- **Erwartbar schlecht:** generischer Titel, nichtssagende Beschreibung, defekte Links,
  unklare Lizenz, falsche Formatangaben.

Kuratierte Extremfälle belegen den Mechanismus per Konstruktion → deshalb **zusätzlich**
die stratifizierte Kernstichprobe als Bias-Kontrolle. Beide Schichten getrennt auswerten.

## 2. Bewertungsraster

Bewertung entlang derselben vier Dimensionen wie der Prototyp, aber **nicht** mit exakt
denselben Einzelindikatoren — damit die Evaluation nicht nur die eigene Modelllogik
nachrechnet.

**Skala je Dimension (0–3, anchored Rubric [jonsson2007rubrics]):**

| Wert | Bedeutung |
|------|-----------|
| 0 | nicht erfüllt |
| 1 | schwach erfüllt |
| 2 | teilweise erfüllt |
| 3 | gut erfüllt |

**Dimensionen und Bewertungsfrage:**

| Dimension | Bewertungsfrage |
|-----------|----------------|
| Auffindbarkeit | Ist der Datensatz über Titel, Beschreibung, Keywords, Kategorien, Raum/Zeit gut auffindbar und einordenbar? |
| Zugänglichkeit | Ist die beschriebene Ressource erreichbar, abrufbar, maschinenlesbar und technisch plausibel beschrieben? |
| Nachnutzbarkeit | Sind Lizenz, Rechte, Kontakt, Herausgeber, Vokabulare für eine Weiterverwendung ausreichend klar? |
| Aussagekraft | Sind Titel, Beschreibung, Keywords und Kontextangaben verständlich, plausibel und informationshaltig? |

**Gesamturteil:**

| Urteil | Regel |
|--------|-------|
| gut | Durchschnitt ≥ 2.25 und keine Dimension < 2 |
| schlecht | Durchschnitt ≤ 1.25 oder ≥ 2 Dimensionen < 1.5 |
| mittel | alle übrigen Fälle |

Die 0–3-Skala ist bewusst grob/forced-choice (kein Mittelpunkt → erzwingt Richtung,
vermeidet zentrale Tendenz). Domänen-Vorbild: MQA selbst gradiert in vier Bändern
(Bad/Sufficient/Good/Excellent) [dataeuropa2024mqa]. Psychometrisch wäre 0–4 etwas
robuster [preston2000optimal], aber 0–3 ist bei Experten-Rubric-Bewertung verteidigbar.

## 3. Blinde Bewertung (gegen Anchoring-Bias)

Die manuelle Bewertung erfolgt **blind gegenüber den Modell-Scores**: Die Bewertungs-Vorlage
(`scripts/build_ground_truth_template.py`) enthält nur die zur Beurteilung nötigen Fakten
(Titel, Beschreibung, Keywords, Themes, Lizenz, Formate, URLs/Erreichbarkeit) — **nicht**
die Modell-Ausgabe. So misst der Vergleich echte Übereinstimmung.

## 4. Mapping Modell → Grundbewertung

Der Prototyp liefert je Dimension einen Score (0–1), der auf die 0–3-Skala reskaliert wird
(`score × 3`). Auf die reskalierten Werte wird **dieselbe Gesamturteil-Regel** angewendet
wie auf die manuelle Bewertung — keine frei gewählten Schwellen.

Dimensions-Zuordnung:
`findability ↔ Auffindbarkeit`, `accessibility ↔ Zugänglichkeit`,
`reusability ↔ Nachnutzbarkeit`, `expressiveness ↔ Aussagekraft`.

## 5. Kennzahlen

Implementiert in `src/evaluation/ground_truth.py` und
`playground/notebooks/10_ground_truth_evaluation.ipynb`.

- **Pro Dimension:** Spearman ρ, Kendall τ (Modell-Score ↔ manuelle 0–3-Bewertung)
  — zeigt, ob das Modell je Dimension dieselbe Rangordnung erzeugt.
- **Gesamturteil:** Accuracy, Cohen's κ (gewichtet, gut > mittel > schlecht) [cohen1960kappa],
  Konfusionsmatrix.
- **Trennschärfe:** Modell-Score-Verteilung je GT-Grade (trennt das Modell „gut" von
  „schlecht"?); optional ROC/AUC für gut vs. nicht-gut.
- **Getrennt berichten:** Kernstichprobe vs. Extremfälle.

**Falls ≥ 2 Bewerter:innen:** Inter-Rater-Reliabilität (Cohen's κ / Krippendorff's α
[krippendorff2004content]) berichten, bevor gegen das Modell verglichen wird — sonst ist
unklar, ob eine niedrige Modell↔GT-Übereinstimmung am Modell oder an unscharfer Bewertung
liegt.

## 6. Visualisierungen (für die Thesis)

- Scatter Modell-Gesamtscore ↔ GT (Punkte nach GT-Grade gefärbt).
- 4er-Panel: je Dimension Modell-Score ↔ manuelle Bewertung.
- Boxplots der Modell-Scores je GT-Grade (Trennschärfe).
- Konfusionsmatrix-Heatmap (Modell-Grade × GT-Grade).
- Balken der Spearman-ρ je Dimension.

---

## BibTeX

```bibtex
@article{jonsson2007rubrics,
  title   = {The Use of Scoring Rubrics: Reliability, Validity and Educational Consequences},
  author  = {Jonsson, Anders and Svingby, Gunilla},
  journal = {Educational Research Review},
  volume  = {2},
  number  = {2},
  pages   = {130--144},
  year    = {2007},
  doi     = {10.1016/j.edurev.2007.05.002}
}

@article{preston2000optimal,
  title   = {Optimal Number of Response Categories in Rating Scales: Reliability, Validity,
             Discriminating Power, and Respondent Preferences},
  author  = {Preston, Carolyn C. and Colman, Andrew M.},
  journal = {Acta Psychologica},
  volume  = {104},
  number  = {1},
  pages   = {1--15},
  year    = {2000},
  doi     = {10.1016/S0001-6918(99)00050-5}
}

@article{garland1991midpoint,
  title   = {The Mid-Point on a Rating Scale: Is it Desirable?},
  author  = {Garland, Ron},
  journal = {Marketing Bulletin},
  volume  = {2},
  pages   = {66--70},
  year    = {1991}
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

@misc{dataeuropa2024mqa,
  title        = {Metadata Quality Assessment (MQA) — Data Quality Guidelines},
  author       = {{data.europa.eu}},
  howpublished = {\url{https://op.europa.eu/webpub/op/data-quality-guidelines/en/}},
  year         = {2024},
  note         = {Publications Office of the European Union, accessed 2026-06-16}
}

@article{likert1932technique,
  title   = {A Technique for the Measurement of Attitudes},
  author  = {Likert, Rensis},
  journal = {Archives of Psychology},
  volume  = {22},
  number  = {140},
  pages   = {1--55},
  year    = {1932}
}
```
