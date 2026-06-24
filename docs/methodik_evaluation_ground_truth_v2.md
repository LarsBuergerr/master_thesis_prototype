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

Die Skala hat keinen Mittelpunkt (forced-choice) und erzwingt damit eine Richtungsentscheidung; zentrale Tendenz wird so vermieden. Domänen-Vorbild: MQA selbst gradiert in vier Bändern (Bad/Sufficient/Good/Excellent) [dataeuropa2024mqa]. Psychometrisch wäre 0–4 etwas robuster [preston2000optimal], aber 0–3 ist bei Experten-Rubric-Bewertung verteidigbar.

Die vollständige Rubric mit Beispielen je Stufe liegt in der Bewertungs-Vorlage (`scripts/build_ground_truth_template.py`). Kernanker je Dimension:

| Wert | Auffindbarkeit | Zugänglichkeit | Nachnutzbarkeit | Aussagekraft |
|------|----------------|----------------|-----------------|--------------|
| **0** | Kein Titel oder vollständig generisch; keine Keywords; kein Raum-/Zeitbezug | Ressource nicht erreichbar; kein Format oder offensichtlich falsch | Keine Lizenz; kein Kontakt; kein Herausgeber | Beschreibung fehlt oder ist identisch mit dem Titel; keine Keywords |
| **1** | Titel vorhanden, aber nichtssagend; Keywords fehlen oder trivial; keine Kategorisierung | Ressource erreichbar, aber Format falsch beschrieben oder nicht maschinenlesbar | Lizenz vorhanden, aber unklar; Kontakt oder Herausgeber fehlt | Beschreibung vorhanden, aber Boilerplate oder inhaltsleer ohne Mehrwert |
| **2** | Titel verständlich; Keywords oder Kategorie vorhanden; Raum- oder Zeitbezug fehlt | Ressource erreichbar, Format korrekt; Medientyp fehlt oder Distribution unvollständig | Lizenz klar; Herausgeber angegeben; Kontakt fehlt oder nur unstrukturiert | Beschreibung inhaltlich, aber vage oder ohne Kontext (Zeitraum, Quelle, Methode) |
| **3** | Aussagekräftiger Titel; präzise Keywords; Kategorie, Raum- und Zeitbezug klar angegeben | Ressource erreichbar, maschinenlesbar; Format und Medientyp korrekt und kongruent | Lizenz klar und maschinenlesbar; strukturierter Kontakt und Herausgeber; kontrollierte Vokabulare | Beschreibung spezifisch und kontextuell; Keywords präzise; Titel und Beschreibung kohärent |

**Dimensionen und Kernfrage:**

| Dimension | Kernfrage |
|-----------|-----------|
| Auffindbarkeit | Kann ein Nutzer diesen Datensatz über seine Metadaten finden und thematisch einordnen? |
| Zugänglichkeit | Ist die Ressource tatsächlich abrufbar und technisch korrekt beschrieben? |
| Nachnutzbarkeit | Sind die rechtlichen und organisatorischen Rahmenbedingungen für eine Weiterverwendung klar? |
| Aussagekraft | Vermitteln Titel und Beschreibung inhaltlich relevante, nicht-redundante Informationen über den Datensatz? |

**Gesamturteil:**

| Urteil | Regel |
|--------|-------|
| gut | Durchschnitt ≥ 2.25 und keine Dimension < 2 |
| schlecht | Durchschnitt ≤ 1.25 oder (Durchschnitt < 2.0 und ≥ 2 Dimensionen < 1.5) |
| mittel | alle übrigen Fälle |

Die zweite "schlecht"-Bedingung (≥ 2 Dimensionen < 1.5) ist durch `Durchschnitt < 2.0` abgesichert, damit ein Datensatz mit hohem Gesamtschnitt nicht allein durch zwei schwache Einzeldimensionen als "schlecht" klassifiziert werden kann.

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

**Einschränkung der linearen Reskalierung:** Modell-Scores je Dimension sind durch die
zugrundeliegenden Binär-Indikatoren oft bimodal verteilt und nicht gleichmäßig über [0, 1]
gestreut. Die lineare Reskalierung (`score × 3`) überführt diese Verteilung unverzerrт auf
die Rubric-Skala, kann aber dazu führen, dass Modell-Klassen stärker auf die Extremwerte
(0 und 3) konzentriert sind als die manuelle Bewertung. Dieser Effekt wird in §5 durch
Boxplots der Modell-Scores je GT-Grade sichtbar gemacht und sollte bei der Interpretation
der Konfusionsmatrix berücksichtigt werden.

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
