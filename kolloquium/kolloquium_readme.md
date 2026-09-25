# Kolloquium – Stichpunkte & Zeitplan (v3-Foliensatz)

Ziel: ca. 30 Minuten **inklusive Live-Demo**. Basis: `kolloquium_buerger_v3.pptx/pdf` (22 sichtbare Hauptfolien + 2 Backup-Folien am Ende, die nicht mitgezählt werden).

Zeitrechnung: ~28 Min Vortragsinhalt + 5 Min Demo ≈ 33 Min brutto. An Folie 7, 15 und 20 lässt sich bei Zeitdruck am ehesten kürzen.

---

## Einstieg (≈3 Min)

**1 – Titel (20s)**
- Kurz vorstellen, Titel nennen, Betreuung danken

**2 – Ausgangslage (60s)**
- GovData = Aggregator, nicht Datenhalter — Qualität entsteht dezentral bei den Bereitstellenden
- 151.579 Datensätze → Größenordnung, die jede manuelle Prüfung ausschließt
- Kernsatz: SHACL sagt "ist das Feld da und valide", nicht "kann ich damit etwas anfangen"

**3 – Forschungsfragen (60s)**
- Zentrale Frage vorlesen, dann kurz: "formale Prüfung + ergänzende Dimensionen, ohne Nachvollziehbarkeit zu verlieren" als roten Faden benennen
- Die 5 Teilfragen nur kurz überfliegen, nicht einzeln erklären — kommen am Ende noch mal dran

---

## Grundlagen & Modellkonzeption (≈8 Min)

**4 – Bewertungslücke (75s)**
- Betonen: zwei Achsen (Anwendungsnähe × Operationalisierbarkeit), keine der drei Gruppen erfüllt beides
- Konkret an MQA aufhängen, da das später die Vergleichsbaseline ist — schon hier andeuten

**5 – Experteninterviews (60s)**
- Kurz: 3 leitfadengestützte Interviews
- "Fit for Purpose statt Formalerfüllung" als Leitsatz hervorheben, zieht sich durchs ganze Modell

**6 – Verdichtung zu 4 Dimensionen (75s)**
- Kurz erklären wie verdichtet wurde (Bewertungsfunktion statt Literaturherkunft als Kriterium)
- Die 4 Dimensionen einmal laut mit ihrer Leitfrage vorlesen — das ist der Rahmen für alles Folgende

**7 – Indikatoren & Messmodell (90s)**
- Tabelle nicht vorlesen, nur je 1 Beispiel pro Spalte nennen
- Die 4 Messprinzipien kurz anreißen, v.a. "Mittelung über Distributionen" und "Malus-Prinzip" — kommen in der Evaluation wieder vor

**8 – Scoring & Gewichtung (75s)**
- Formeln kurz erklären (zweistufig: Indikator → Dimension → Gesamt)
- Begründen warum Zugänglichkeit/Aussagekraft am höchsten gewichtet sind

---

## Prototyp (≈5 Min inkl. Demo-Übergang)

**10 – LLM-Bewertung Aussagekraft (90s)**
- Warum überhaupt LLM: einzige Dimension ohne regelbasierte Prüfbarkeit
- Ein-Aufruf-Architektur betonen (bewusst keine Agentenkette — Kosten & Nachvollziehbarkeit)
- Feste Reihenfolge findings → reasoning → applicable → score kurz erklären: Modell muss erst begründen, bevor es eine Zahl nennt

**11 – Verarbeitungspipeline (60s)**
- Grafik erklären: Extraktion → bedarfsgesteuerte Anreicherung → Indikatorausführung parallel über die 4 Dimensionen → Scoring
- "bedarfsgesteuert" betonen: Netzabruf und LLM-Call nur wenn ein aktiver Indikator es braucht — spart Zeit und Geld

**12 – Live-Demo (15s Übergang + 5 Min Demo)**
- Kurzer Satz zur Überleitung, dann Bildschirm wechseln
- Demo-Skript:
  1. Trefferliste mit Qualitätsfacette zeigen
  2. Einen schlecht bewerteten Datensatz anklicken
  3. Einen Befund aufklappen (Kernaussage → Ist-Angabe mit Fundstelle → Handlungsanweisung)
  4. Falls vorhanden: RDF-Vorlage zeigen
  5. Kurz die Aggregatsicht/Bestandsübersicht zeigen, falls Zeit bleibt
- Bei Zeitdruck: Schritt 5 zuerst streichen

---

## Evaluation (≈8 Min) — Herzstück, hier nicht hetzen

**13 – Evaluationsdesign (75s)**
- Zwei Vergleichsstränge klar trennen: Ground Truth beantwortet "bewertet er korrekt", MQA-Baseline beantwortet "was sieht er zusätzlich"
- Kurz erwähnen: Referenzbewertung blind gegenüber Prototyp-Scores (Anchoring-Bias vermeiden)

**14 – Hauptergebnisse (90s)**
- Jede Zahl kurz einordnen, nicht nur vorlesen:
  - ρ = 0,765 / 92% → Übereinstimmung mit Mensch
  - ρ = 0,834 → auch mit der etablierten Baseline stark korreliert
  - 15,8% → aber auf Indikatorebene überschätzt die Baseline systematisch
  - 5/6 · 6/6 → und wo beide auseinanderlaufen, liegt der Prototyp näher am Menschen
- Kernaussage der ganzen Arbeit — ruhig etwas Zeit lassen

**15 – Triangulation Kernstichprobe (90s)**
- Auffindbarkeit als einzige Ausnahme erklären (niedrigstes Dimensionsgewicht → Gesamtscore ist dafür strukturell schwächerer Prädiktor, nicht dass die Indikatoren schlecht wären)
- Kurz erwähnen: auf den Extremfällen liegt der Prototyp bei allen 6 Zielgrößen vorne, mit größeren Abständen

**16 – Grenzfall Aussagekraft (90s)**
- Selbstkritische Folie — bewusst offen damit umgehen, wirkt souverän
- Zwei Ursachen trennen: (1) relationale Kriterien bleiben bei durchgängig schwachem Inhalt fälschlich hoch, (2) flache Mittelung verschluckt einzelne harte Defizite
- Betonen: Kernstichprobe unauffällig (0,569) — Problem zeigt sich nur bei den konstruierten Extremfällen

**17 – Beispiel Justizblatt (60s)**
- Konkretes Beispiel macht Folie 16 greifbar — kurz vorlesen, dann Pointe: ein hartes Defizit wird von fünf unauffälligen Werten überstimmt

---

## Schluss (

**18 – Antworten auf die Teilfragen (75s)**
- Falls Klick-Animation eingebaut: pro Zeile kurz pausieren, nicht alle 5 am Stück vorlesen
- Als Rückbezug zu Folie 3 framen: "Damit zurück zu den eingangs gestellten Fragen…"

**19 – Konzeptionelle Grenze (60s)**
- Lübeck-Beispiel ist die wichtigste Pointe der Schlussbetrachtung: gleicher Datensatz, gegensätzliches Urteil je nach Nutzungsszenario
- Kernaussage: ρ = 0,765 heißt "ordnet wie der gewählte Maßstab", nicht "objektiv richtig"

**20 – Methodische & technische Grenzen (60s)**
- Wichtigster Punkt: fehlende Inter-Rater-Reliabilität (eine Person hat sowohl Modell als auch Referenz erstellt)
- Rest kann schneller durch

**21 – Beitrag, Ausblick, Praxis (75s)**
- Beitrag-Spalte als eigentliche Antwort auf "was ist neu": Verbindung aus rückführbarer Indikatormenge + vollständiger Operationalisierung + Prüfung gegen menschliches Urteil
- Bei Praxis den Punkt "formale Validierung als Vorstufe" hervorheben — konkrete Handlungsempfehlung fürs Portal

**22 – Vielen Dank (10s)**
- Kurz, dann Fragen

---

## Hinweise

- Die beiden Backup-Folien (Quellen & Grundlagen, Scoring-Logik) sind bewusst nicht eingerechnet — nur zeigen, wenn gezielt danach gefragt wird.
- Aktuelle Kennzahlen (Stand nach Fix "wrong numbers in triangulation evaluation"): ρ = 0,834 (Kernstichprobe vs. MQA), ρ = 0,818 (Extremfälle vs. MQA), Dimension heißt jetzt durchgängig **Nachnutzbarkeit** (nicht mehr Wiederverwendbarkeit), Modell **GPT-5.5**.
