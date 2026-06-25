# Methodik: Evaluation gegen Ground Truth (v3)

> Manuelle Bewertung einer Stichprobe als externer Maßstab, um zu prüfen ob der Prototyp
> dieselbe Rangordnung erzeugt wie ein Mensch — und ob er dabei besser abschneidet als die
> MQA (H3 aus `docs/evaluation_vs_mqa.md`).

---

## 1. Sampling-Strategie

**Stratifizierte purposive Stichprobe mit ergänzenden Extremfällen.**

Die Kernstichprobe (`sample_2026-06-25_09-57`, Seed 67, n=50) deckt zentrale Unterschiede
der GovData-Datenbasis ab:
- Themenbereiche
- Datenbereitsteller / Contributor
- Zugriffstypen (Datei, API, Data Service, Landing Page)
- Formatgruppen (CSV/JSON/XML, PDF/HTML, Geoformate, unklare Formate)
- Technische Vorqualität (erreichbare vs. nicht erreichbare Ressourcen)

Die ergänzenden Extremfälle (n=10) dienen als Stresstest:
- **Erwartbar gut:** klare Beschreibung, erreichbare Ressource, maschinenlesbares Format,
  Lizenz, Kontakt.
- **Erwartbar schlecht:** generischer Titel, nichtssagende Beschreibung, defekte Links,
  unklare Lizenz, falsche Formatangaben.

Kuratierte Extremfälle belegen den Mechanismus per Konstruktion → deshalb **zusätzlich**
die stratifizierte Kernstichprobe als Bias-Kontrolle. Beide Schichten getrennt auswerten.

---

## 2. Bewertungsraster

Bewertung entlang derselben vier Dimensionen wie der Prototyp, aber **nicht** mit exakt
denselben Einzelindikatoren. Die Ankerformulierungen beschreiben intentional die
**nutzerseitige Qualitätserfahrung**, nicht die technische Metadatenstruktur. Damit wird
sichergestellt, dass die Ground-Truth-Bewertung dasselbe Konstrukt mit einer methodisch
unabhängigen Perspektive misst und nicht die Indikatorlogik des Prototyps manuell
nachvollzieht [campbell1959convergent; jonsson2007rubrics].

### Skala je Dimension (0–5, Anchored Rubric)

**6-stufige Skala** ohne einzelnen Mittelpunkt (gerade Stufenanzahl → Forced Choice bleibt
erhalten). Preston & Colman (2000) zeigen empirisch, dass Reliabilität, Validität und
Diskriminierungsfähigkeit von Ratingskalen bis 5–7 Kategorien steigen und bei 4 Kategorien
(0–3) suboptimal sind [preston2000optimal]. Das Argument gegen Mittelpunkte
(Central Tendency Bias, [garland1991midpoint]) gilt für Einstellungsskalen ohne inhaltliche
Anker; bei einer faktischen Qualitätsbewertung mit definierten Ankerformulierungen je Stufe
entfällt das Ausweichverhalten strukturell, da der Bewerter gegen konkrete Kriterien prüft
statt eine vage Präferenz auszudrücken [jonsson2007rubrics].

### Dimensionen, Kernfragen und Anker

**Auffindbarkeit** — *Kann ein Nutzer diesen Datensatz über seine Metadaten finden und thematisch einordnen?*

| Stufe | Anker |
|-------|-------|
| **0** | Datensatz ist über seine Metadaten weder auffindbar noch inhaltlich einzuordnen |
| **1** | Grobe Domäne erkennbar; Kontext, Zeitraum und Ort vollständig unklar |
| **2** | Thema identifizierbar; inhaltlicher, zeitlicher oder räumlicher Kontext weitgehend fehlend |
| **3** | Thema und Grundkontext erkennbar; einzelne Kontextdimensionen fehlen oder sind unscharf |
| **4** | Gut auffindbar und einordenbar; kleinere Lücken bei Kontext oder Kategorisierung |
| **5** | Vollständig auffindbar; Thema, Zeitraum, Ort und Zweck sofort aus Metadaten ersichtlich |

**Zugänglichkeit** — *Ist die Ressource tatsächlich abrufbar und technisch korrekt beschrieben?*

| Stufe | Anker |
|-------|-------|
| **0** | Ressource nicht erreichbar oder technische Angaben vollständig fehlend oder falsch |
| **1** | Ressource erreichbar, technische Beschreibung aber stark fehlerhaft oder irreführend |
| **2** | Ressource erreichbar; Format oder Abrufbarkeit teilweise unklar oder inkonsistent beschrieben |
| **3** | Ressource erreichbar und grundlegend korrekt beschrieben; einzelne technische Angaben fehlen |
| **4** | Gut erreichbar, technisch korrekt und vollständig beschrieben; kleinere Inkonsistenzen |
| **5** | Einwandfrei erreichbar; alle technischen Angaben korrekt, konsistent und maschinenlesbar |

**Nachnutzbarkeit** — *Sind die rechtlichen und organisatorischen Rahmenbedingungen für eine Weiterverwendung klar?*

| Stufe | Anker |
|-------|-------|
| **0** | Keine Lizenz, kein Kontakt, kein Herausgeber — Nachnutzung faktisch unmöglich |
| **1** | Einzelne Angaben vorhanden, aber unklar oder widersprüchlich; Nachnutzung rechtlich unsicher |
| **2** | Lizenz oder Kontakt vorhanden, aber unvollständig; Weiterverwendung mit erheblichem Aufwand möglich |
| **3** | Wesentliche Angaben vorhanden; einzelne organisatorische Details fehlen |
| **4** | Lizenz, Kontakt und Herausgeber vollständig und klar; kleinere Lücken bei Zusatzinformationen |
| **5** | Vollständige, klare und strukturierte Angaben; Nachnutzung ohne Rückfragen möglich |

**Aussagekraft** — *Vermitteln Titel und Beschreibung inhaltlich relevante, nicht-redundante Informationen über den Datensatz?*

| Stufe | Anker |
|-------|-------|
| **0** | Beschreibung fehlt oder ist identisch mit Titel; kein inhaltlicher Mehrwert |
| **1** | Beschreibung vorhanden, aber inhaltsleere Floskeln oder reiner Boilerplate-Text |
| **2** | Beschreibung inhaltlich, aber vage; kein zeitlicher, räumlicher oder methodischer Kontext |
| **3** | Beschreibung informativ; einzelne Kontextdimensionen fehlen oder sind unscharf |
| **4** | Beschreibung klar und kontextuell; Titel und Beschreibung kohärent; kleinere Lücken |
| **5** | Beschreibung spezifisch und kontextuell vollständig; Titel prägnant; keine Redundanz |

### Gesamturteil

| Urteil | Regel |
|--------|-------|
| **gut** | Durchschnitt ≥ 4.0 und keine Dimension < 3 |
| **schlecht** | Durchschnitt ≤ 2.0 oder (Durchschnitt < 3.5 und ≥ 2 Dimensionen < 2) |
| **mittel** | alle übrigen Fälle |

Die zweite „schlecht"-Bedingung ist durch `Durchschnitt < 3.5` abgesichert, damit ein
Datensatz mit hohem Gesamtschnitt nicht allein durch zwei schwache Einzeldimensionen als
„schlecht" klassifiziert werden kann.

**Methodische Begründung der Klassifikationslogik:**

Die Schwellenwerte folgen einem **kriteriumsorientierten Ansatz** [glaser1963; popham1969]:
Die Grenzen repräsentieren inhaltlich definierte Qualitätsniveaus — ein Datensatz mit
Durchschnitt ≥ 4.0 erfüllt alle wesentlichen Qualitätsanforderungen, unabhängig davon
wo er relativ zur Stichprobenverteilung liegt. Das Maximum (5.0) ist aspirational, nicht
Schwelle — konsistent mit der Rubric-Design-Praxis [brookhart2013] und dem MQA-Bändermodell,
das ebenfalls keinen Perfektscore für "Excellent" verlangt [dataeuropa2024mqa].

Das Kollabieren der 0–5-Ordinalskala in drei inhaltlich bedeutsame Kategorien
(gut / mittel / schlecht) ist methodisch valide, wenn — wie hier — die Kategorien
an substantiellen Unterschieden im Konstrukt orientiert sind und nicht willkürlich
gezogen werden [agresti2010].

Die Aggregationslogik ist **hybrid**: primär kompensatorisch (Durchschnitt über alle
Dimensionen), abgesichert durch einen konjunktiven Floor (keine Dimension < 3 für "gut",
≥ 2 Dimensionen < 2 können zu "schlecht" führen). Dieser Hybridansatz verhindert, dass
ein Extremwert in einer Dimension katastrophale Lücken in anderen wegkompensiert
[einhorn1971] — ein bekanntes Problem rein kompensatorischer Aggregationsmodelle.

---

## 3. Blinde Bewertung (gegen Anchoring-Bias)

Die manuelle Bewertung erfolgt **blind gegenüber den Modell-Scores**: Die Bewertungsvorlage
(`scripts/build_ground_truth_template.py`) enthält nur die zur Beurteilung nötigen Fakten
(Titel, Beschreibung, Keywords, Themes, Lizenz, Formate, URLs/Erreichbarkeit) — **nicht**
die Modell-Ausgabe. So misst der Vergleich echte Übereinstimmung.

**Konsistenz bei Einzelbewerter:** Da Inter-Rater-Reliabilität entfällt, wird interne
Konsistenz durch kompakte Bewertungssessions (alle 50 Datensätze in wenigen Sessions),
vorherige Kalibrierung an 5 Beispieldatensätzen und explizite Markierung von Zweifelsfällen
zur abschließenden Überprüfung sichergestellt.

---

## 4. Mapping Modell → GT-Skala

Der Prototyp liefert je Dimension einen Score (0–1), der auf die 0–5-Skala reskaliert wird
(`score × 5`). Auf die reskalierten Werte wird **dieselbe Gesamturteil-Regel** angewendet
wie auf die manuelle Bewertung — keine frei gewählten Schwellen.

Dimensions-Zuordnung:
`findability ↔ Auffindbarkeit`, `accessibility ↔ Zugänglichkeit`,
`reusability ↔ Nachnutzbarkeit`, `expressiveness ↔ Aussagekraft`.

**Einschränkung der linearen Reskalierung:** Modell-Scores je Dimension sind durch die
zugrundeliegenden Binär-Indikatoren oft bimodal verteilt und nicht gleichmäßig über [0, 1]
gestreut. Die lineare Reskalierung überführt diese Verteilung unverzerrт auf die GT-Skala,
kann aber dazu führen, dass Modell-Klassen stärker auf die Extremwerte konzentriert sind
als die manuelle Bewertung. Dieser Effekt wird in §5 durch Boxplots der Modell-Scores je
GT-Grade sichtbar gemacht.

---

## 5. Kennzahlen

Implementiert in `src/evaluation/ground_truth.py` und
`playground/notebooks/10_ground_truth_evaluation.ipynb`.

**Primärmetrik:**
- **Gesamturteil:** Cohen's κ (gewichtet, gut > mittel > schlecht) [cohen1960kappa],
  Accuracy, Konfusionsmatrix — robust gegenüber gebundenen Rängen auf Dimensionsebene.

**Sekundärmetriken:**
- **Pro Dimension:** Spearman ρ, Kendall τ (Modell-Score ↔ manuelle 0–5-Bewertung).
  Durch die 6-stufige Skala entstehen weniger gebundene Ränge als bei 0–3, was die
  Diskriminierungsfähigkeit des Rangkorrelationskoeffizienten verbessert [preston2000optimal].
  Dennoch als ergänzende Metrik zu interpretieren, nicht als primären Hypothesentest.
- **Trennschärfe:** Modell-Score-Verteilung je GT-Grade (Boxplots); optional ROC/AUC
  für gut vs. nicht-gut.

**Getrennt berichten:** Kernstichprobe (n=50) vs. Extremfälle (n=10).

**Falls ≥ 2 Bewerter:innen:** Inter-Rater-Reliabilität (Cohen's κ / Krippendorff's α
[krippendorff2004content]) berichten, bevor gegen das Modell verglichen wird.

---

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

@article{glaser1963,
  title   = {Instructional Technology and the Measurement of Learning Outcomes:
             Some Questions},
  author  = {Glaser, Robert},
  journal = {American Psychologist},
  volume  = {18},
  number  = {8},
  pages   = {519--521},
  year    = {1963},
  doi     = {10.1037/h0049294}
}

@article{popham1969,
  title   = {Implications of Criterion-Referenced Measurement},
  author  = {Popham, W. James and Husek, T. R.},
  journal = {Journal of Educational Measurement},
  volume  = {6},
  number  = {1},
  pages   = {1--9},
  year    = {1969},
  doi     = {10.1111/j.1745-3984.1969.tb00654.x}
}

@book{brookhart2013,
  title     = {How to Create and Use Rubrics for Formative Assessment and Grading},
  author    = {Brookhart, Susan M.},
  year      = {2013},
  publisher = {ASCD},
  address   = {Alexandria, VA}
}

@book{agresti2010,
  title     = {Analysis of Ordinal Categorical Data},
  author    = {Agresti, Alan},
  year      = {2010},
  edition   = {2nd},
  publisher = {Wiley},
  address   = {Hoboken, NJ},
  doi       = {10.1002/9780470594001}
}

@article{einhorn1971,
  title   = {Use of Nonlinear, Noncompensatory Models as a Function of Task and
             Amount of Information},
  author  = {Einhorn, Hillel J.},
  journal = {Organizational Behavior and Human Performance},
  volume  = {6},
  number  = {1},
  pages   = {1--27},
  year    = {1971},
  doi     = {10.1016/0030-5073(71)90031-6}
}
```
