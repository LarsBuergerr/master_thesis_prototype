# Änderungen zu den Kommentaren aus `thesis_2026-08-06_kommentiert_2.pdf`

Diese Datei mappt jeden der 22 Annotationen (Highlights/Notizen) aus `docs/thesis_2026-08-06_kommentiert_2.pdf`
auf die konkrete Änderung in `thesis/contents.tex`. Reihenfolge nach Zeitstempel der Annotation
(erste Runde 2026-08-07, zweite Runde 2026-08-10). Umgesetzt über die Commits `e7a69ab`, `a500f60`, `84311df`
sowie den aktuellen Arbeitsstand.

**Seitenzahlen** beziehen sich auf den aktuell kompilierten Stand (`thesis/build/report.pdf`, 12.08.2026,
Kapitelzählung nach dem in Punkt 12 beschriebenen Kapitel-Split). Bei den beiden strukturellen Verschiebungen
(Punkt 12, 22) ist zusätzlich die „Vorher“-Seite angegeben, wie sie als Annotation im Reviewer-PDF
`thesis_2026-08-06_kommentiert_2.pdf` verortet war — diese alten Seitenzahlen sind approximativ, da die
PDF-Annotationswerkzeuge Kommentare nachweislich gelegentlich der falschen Nachbarseite zuordnen.

Status: ✅ umgesetzt · ⚠️ offen

## Seitenübersicht

| # | Status | Seite aktuell | Seite vorher (Reviewer-PDF) |
|---|--------|----------------|------------------------------|
| 1 | ✅ | S. 34 | — |
| 2 | ✅ | S. 36 | — |
| 3 | ✅ | S. 38 | — |
| 4 | ✅ | S. 41 | — |
| 5 | ✅ | S. 45 (Übersicht) / S. 129 (Anhang C) | — |
| 6 | — | S. 44 | — |
| 7 | ✅ | S. 45 | — |
| 8 | ✅ | S. 47 | — |
| 9 | ✅ | S. 45 | — |
| 10 | ✅ | S. 49 | — |
| 11 | ✅ | S. 51 | — |
| 12 | ✅ | S. 31/32/44 | ca. S. 41 |
| 13 | ✅ | S. 57/59 | — |
| 14 | ✅ | S. 62 | — |
| 15 | ✅ | S. 63 | — |
| 16 | ⚠️ offen | S. 65–67 (thematisch, nicht umgesetzt) | ca. S. 61 |
| 17 | ⚠️ teilweise | S. 66 | ca. S. 62 |
| 18 | ✅ | S. 63, 65–66 | — |
| 19 | ✅ | S. 67 | — |
| 20 | ✅ | S. 67 | — |
| 21 | ✅ | S. 73 | — |
| 22 | ✅ | S. 42/78 | ca. S. 72 |
| 23 | ✅ | S. 88, 91 | ca. S. 81 |
| 24 | ✅ | S. 88 | ca. S. 81 |
| 25 | ✅ | S. 89 | ca. S. 82 |
| 26 | ✅ | S. 90 | ca. S. 83 |
| 27 | ✅ | S. 90 | ca. S. 83 |
| 28 | ✅ | S. 90–91 | ca. S. 83 |

Punkte 23–28 stammen aus einer weiteren Kommentarrunde (`thesis_2026-08-06_kommentiert_4.pdf`, 2026-08-11,
Evaluationskapitel) und sind unten unter „Runde 3“ dokumentiert. Seitenzahlen 1–22 beziehen sich weiterhin auf
den Stand vor Kapitel 6; durch das seither gewachsene Kapitel „Prototypische Operationalisierung“ hat sich deren
Seitenzählung nicht verschoben, da alle Ergänzungen ab Kapitel 6 liegen.

---

## Runde 1 (2026-08-07) — Experteninterviews-Kapitel

**1. ✅ „Schriftgröße zu klein im Vergleich zum Text der Arbeit. Und abweichende Schriftgröße zu anderen Tabellen.“** — **S. 34** (Tabelle 3.1)
Tabelle der Hauptkategorien (`tab:hauptkategorien`, K1–K10) lief vorher auf `\tiny`. Auf `longtable` mit
`\scriptsize` umgestellt (seitenübergreifend mit Fortsetzungskopf), passend zur Schriftgröße der übrigen Tabellen.

**2. ✅ „Im nächsten Satz schreibst du Codierung mit K. Entweder oder ;)“** — **S. 36** (zwischen Tabelle 3.2 und 3.3)
Durchgängige Vereinheitlichung der Terminologie: `Kodierung`/`Kodiereinheit`/`Kodierleitfaden`/`Kodierregel`
→ `Codierung`/`Codiereinheit`/`Codierleitfaden`/`Codierregel` im gesamten Abschnitt (mehrere Stellen, u. a.
Tabellenüberschriften und Fließtext).

**3. ✅ „Wieder zu kleiner Text“** — **S. 38** (Tabelle 3.4)
Tabelle „Zentrale Ergebnisse der Interviewauswertung“ (`tab:zentrale_interviewergebnisse`) lief ebenfalls auf
`\tiny` und wurde analog zu Punkt 1 auf `longtable` mit `\scriptsize` umgestellt.

**4. ✅ „Bitte die Aussagen belegen. Deine Experten könnten AI-Bias erzählen und du gibst es ohne Einordnung in Belege wieder.“** — **S. 41**
Absatz zu den Grenzen generativer KI (K10-Auswertung) mit Literatur unterlegt: Halluzinationsrisiko jetzt mit
`\cite{Ji2023HallucinationSurvey}` belegt und explizit an den Interviewbefund rückgebunden (`INT-K10.8`);
Reproduzierbarkeitsproblem von LLM-Bewertungen zusätzlich mit `\cite{Zheng2023LLMJudge}` (Positions-,
Verbositäts-, Selbstbevorzugungseffekte) begründet.

**5. ✅ „Ist der Text hier nochmal kleiner geworden? Zum Glück gibts ne Zoom-Funktion…“** — **strukturell verschoben**
Vorher: eine einzige `\tiny`-Tabelle mit 15 Zeilen und vollem Quellenapparat, mehrseitig direkt im Kapitel.
Nachher: kompakte Übersichtstabelle (`tab:longlist-uebersicht`, nur Nr. + Dimension, normale Tabellenschrift) an
**S. 45** im Kapitel, vollständige Tabelle mit Quellenapparat (`tab:longlist-kandidatendimensionen`) in den
Anhang verschoben (`app:longlist_kandidatendimensionen`, **S. 129**).

**6. — „Sehr gute Begründung!“** — **S. 44**
Highlight bezieht sich auf die fünf Aufnahmekriterien der Longlist („Eine Dimension wird in die Longlist
aufgenommen, wenn sie die folgenden Kriterien erfüllt: 1. Sie ist in mindestens einem relevanten
Literaturansatz verankert. […]“, direkt am Kapitelanfang von Kapitel 4). Positives Feedback, keine Änderung
erforderlich; per Bildvergleich der Annotation gegen den PDF-Ausschnitt verifiziert.

**7. ✅ „Nur weil etwas komplex ist, kannst du's nicht ausschließen. Auch Vergleichbarkeit und Evaluierbarkeit ist so lala als Begründung. Geh nochmal zurück zu deinen Forschungsfragen…“** — **S. 45**
Die Begründung für die Verdichtung der Longlist auf vier Hauptdimensionen benannte vorher „schwer zu
implementieren“ und „in der Evaluation schlecht vergleichbar“ als eigenständige Gründe. Umformuliert: Die
Verdichtung wird jetzt direkt an Kriterium 5 der Longlist-Aufnahme (Redundanz zwischen Kandidatendimensionen)
und an Teilfrage 4 der Forschungsfragen (geforderte prototypische Operationalisierbarkeit) rückgebunden, statt an
vage Komplexitäts-/Vergleichbarkeitsargumente.

**8. ✅ „Woher ziehst du diese Kriterien jetzt? Verweise auf Forschungsfragen und Textpassagen“** — **S. 47**
Die sechs Auswahlkriterien für Indikatoren sind jetzt explizit hergeleitet: Anlehnung an das
Goal-Question-Metric-Prinzip `\cite{Basili1994GQM}`, mit Zuordnung der sechs Kriterien zu Standard-/
Konventionsbezug (Abschnitt 2.3), Literatur-/Interviewbezug (Kapitel 2, Abschnitt 3.3) und
Operationalisierbarkeit/Reportingfähigkeit (Teilfrage 4 und 5 der Forschungsfragen).

**9. ✅ „Gibts für dieses Vorgehen Quellen?“** — **S. 45** (unmittelbar im Anschluss an Punkt 7, gleicher Absatz)
Für das Vorgehen, Kandidatendimensionen nach Bewertungsfunktion statt nach Herkunftsmodell zu gruppieren, wird
jetzt Wang & Strong (1996) als methodisches Vorbild zitiert (`\cite{wang1996beyond}`), die in ihrer Studie analog
vorgingen.

**10. ✅ „Steile These. Beleg?“** — **S. 49**
Die Unterscheidung zwischen ternären und graduellen Indikatoren ist jetzt mit den Skalentypen aus
ISO/IEC 25024 begründet (`\cite{iso25024, iso25012}`); die Verwendung einer kontinuierlichen Skala für subjektive
Qualitätsurteile zusätzlich mit Wang & Strongs neunstufiger Wichtigkeitsskala belegt (`\cite{wang1996beyond}`).

**11. ✅ „Und wer erzählt dem Modell, welches Kriterium fachlich nicht zutrifft?“** — **S. 51**
Absatz zur Ergebnisstufe „nicht anwendbar“ ergänzt: Die Anwendbarkeitsentscheidung ist kein separater
Regelmechanismus, sondern Teil der Prüflogik des jeweiligen Indikators selbst — im Prototyp gibt das
LLM-gestützte Verfahren zu kontextuellen Qualifizierern (Abschnitt „LLM-gestützte Bewertung der Aussagekraft“)
die Anwendbarkeit als eigenes Feld seiner strukturierten Ausgabe aus.

**12. ✅ „Du fügst hier Kapitel 2 und die Auswertung der Experteninterviews zusammen … Vorschlag: Ab hier eigenes Kapitel.“** — **strukturell, ca. S. 41 (vorher) → S. 32/44 (nachher)**
Vorher: Theoretische Grundlagen, Bewertungslücke, Experteninterviews und Modellkonzeption liefen als ein
einziges, durchlaufendes Kapitel 2 „Theoretische und konzeptionelle Grundlagen“; die Annotation markierte die
Stelle ungefähr auf S. 41 der damaligen Fassung (Reviewer-PDF).
Nachher: Umgesetzt wie vorgeschlagen (Hauptvorschlag, nicht die Alternative „2.7 anhängen“). Kapitel 2 endet
jetzt bei der Bewertungslücke (**S. 31**), Kapitel 3 „Experteninterviews“ beginnt bei **S. 32**, Kapitel 4
„Konzeption eines Metadatenqualitätsmodells“ bei **S. 44**. Alle nachfolgenden Kapitel- und Abschnittsverweise
(`Kapitel~4/5/6`, `Abschnitt~5.x → 6.x` usw.) im gesamten Dokument entsprechend nachgezogen.

---

## Runde 2 (2026-08-10) — Prototyp-Kapitel

**13. ✅ „Die Vermischung ist mir zu unsauber. Das Diagramm ist auch bei weitem mehr Flussdiagramm als alles andere. Können die drei Schritte auch unabhängig voneinander laufen? Teilen sie sich Datenmodelle? Wenn ja, wieso?“** — **S. 57 (Abschnittsanfang) / S. 59 (Antwort im Fließtext)**
Abschnitt von „Systemarchitektur und Verarbeitungspipeline“ (Schichten-Framing) zu „Verarbeitungspipeline“
umbenannt und neu strukturiert; Diagramm entsprechend als `pipeline_prototype.png` statt
`architecture_prototype.png` referenziert. Neuer Absatz beantwortet die Frage explizit: Die Schritte sind
über die Faktenbasis sequenziell gekoppelt und nicht unabhängig lauffähig; dass sie sich ein gemeinsames
Datenmodell teilen, wird als bewusste Entwurfsentscheidung benannt und auf die Begründung der Faktenbasis
verwiesen.

**14. ✅ „Was ist die Abbruchbedingung?“** — **S. 62**
Beschreibung der technischen Erreichbarkeitsprüfung präzisiert: „…über eine GET-Anfrage mit abgebrochenem
Inhaltsbezug: Die Verbindung wird unmittelbar nach Eintreffen der Antwort-Header geschlossen, ohne den
Antwortkörper zu lesen.“

**15. ✅ „Wo finde ich jetzt Modellkonfiguration 27? In den Tabellen ist alles alphanumerisch“** — **S. 63** (Tabelle 5.1)
Formulierung von „27 aktiviert“ zu „Insgesamt sind 27 Indikatoren umgesetzt“ geändert, um die missverständliche
Nummerierung zu vermeiden; die Zuordnungstabelle (`tab:impl_mapping`) wurde um eine Spalte mit ausgeschriebenem
Indikatornamen erweitert (vorher nur Kürzel + Bezeichner). Dabei wurde auch die inkonsistente N-Nummerierung
(N2–N6 vs. N3–N7) korrigiert.

**16. ⚠️ offen — „Hier besteht eine Optimierungsmöglichkeit: DCAT-AP.de definiert weiter, dass Dokumentationen zusätzlich über `foaf:page` eingebunden werden sollten.“** — **S. 65–67** (thematisch: Zugänglichkeits-/Nachnutzbarkeitsindikatoren, dort wäre die Ergänzung einzuordnen)
Noch nicht umgesetzt. Im Text findet sich kein Verweis auf `foaf:page`.

**17. ⚠️ teilweise — „[SHACL-Validator] ist gerade nicht erreichbar. Hast du ein Gefühl, wie oft das der Fall ist? Regelmäßige HealthChecks?“** — **S. 66** (Haupttext + Fußnote)
Die SHACL-Fußnote wurde ergänzt, erklärt darin aber nur, warum ein direkter Browser-Aufruf der API mit
`405 Method Not Allowed` antwortet (Weboberfläche vs. REST-Endpunkt) — nicht die eigentliche Frage nach
Ausfallhäufigkeit bzw. Health-Checks des externen Dienstes. Diese Frage ist inhaltlich noch offen.

**18. ✅ „Das Arbeiten mit Kürzeln ist üblich … könntest du den Indikator in Klammern danach nennen?“** — **S. 63** (Tabelle) + **S. 65–66** (Inline-Glossen im Fließtext)
Neben der Tabellenspalte aus Punkt 15 wurden Kürzel im Fließtext dort, wo sie erstmals im Detail diskutiert
werden, um den Klartextnamen ergänzt, z. B. „Z7 (maschinenlesbarer Zugriffsweg)“ (S. 65), „N1 (freie Lizenz)“,
„N4 (geplante Verfügbarkeit)“ (beide S. 66).

**19. ✅ „Wenigstens Verlinken und ggf. hier auch vollständig nennen.“** — **S. 67**
Betraf entgegen erster Vermutung nicht die Konventionenhandbuch-Zitation, sondern die Erwähnung von
„Forschungsfrage 3“ im Abschnitt zur LLM-gestützten Aussagekraftsbewertung. Ersetzt durch eine ausgeschriebene
Beschreibung der Teilfrage plus Querverweis: „…den zentralen Baustein für die dritte Teilfrage dieser Arbeit,
welche ergänzenden kontext- und semantikbezogenen Prüfungen … (vgl. Abschnitt~\ref{sec:forschungsfragen})“.

**20. ✅ „Erinnere den Leser hier daran, dass es sich um OpenData handelt … eh schon online frei verfügbare Daten.“** — **S. 67** (gleicher Absatz wie Punkt 19)
Ergänzt im selben LLM-Abschnitt: „Bewertet werden dabei ausschließlich Metadaten offener Verwaltungsdaten, die
ohnehin frei im Netz veröffentlicht sind; ihre Übergabe an ein externes Sprachmodell wirft daher keine Fragen
des Datenschutzes oder der Vertraulichkeit auf.“

**21. ✅ „imho zu ugs. ‚nicht erreichbare‘ oder offline usw.“** — **S. 73** (Abschnitt 5.6.3, Gewichtung)
Umgangssprachliches „tote URL“ im Absatz zur Indikatorgewichtung durch „nicht erreichbare URL“ ersetzt.

**22. ✅ „Deine Zielgruppen solltest du vor dem Prototyp gesammelt beleuchten … gehören für mich in ein Kapitel mit den Experteninterviews.“** — **strukturell, ca. S. 72 (vorher) → S. 42/78 (nachher)**
Vorher: Die Zielgruppen wurden erstmals im Reporting-Kapitel eingeführt; die Annotation markierte diese Stelle
ungefähr auf S. 72 der damaligen Fassung (Reviewer-PDF).
Nachher: Neuer Abschnitt 3.4 „Zielgruppen des Bewertungsmodells“ (**S. 42**) am Ende von Kapitel 3
(Experteninterviews), vor Kapitel 4, führt Datennutzende/Datenbereitstellende/Portalbetreibende allgemein ein.
Die bisherige Zielgruppen-Unterteilung im Reporting-Kapitel wurde zu „Auflösungsbedarf und Gestaltungsziele“
umbenannt (jetzt **S. 78**) und verweist auf die neue Einführung zurück, statt die Gruppen erneut vorzustellen.
Zwei bislang unverankerte „Nutzendensicht“-Stellen in Kapitel 4 (Mittelwertbildung, Malus-Prinzip, beide auf
**S. 50**) verweisen jetzt explizit auf den neuen Abschnitt.

---

## Runde 3 (2026-08-11) — Evaluationskapitel

Aus `thesis_2026-08-06_kommentiert_4.pdf`, sechs neue Annotationen auf S. 81–83 der damaligen Fassung
(Kapitel 6, Evaluation). Wie zuvor per Bildvergleich der Annotation-Koordinaten gegen den gerenderten
PDF-Ausschnitt verifiziert.

**23. ✅ „Das klingt ominös nach einer reinen Selbsteinschätzung.“** — **S. 88** (Abschnitt 6.1) + **S. 91** (Limitation)
Highlight lag auf „Prototyp mit einem **externen** menschlichen Qualitätsurteil“. Der Punkt ist berechtigt: Die
Ground-Truth-Bewertung wurde im Rahmen dieser Arbeit selbst vorgenommen, nicht durch eine unbeteiligte dritte
Person. Lösung: „extern“ durchgängig durch „unabhängig“ ersetzt (4 Stellen in Abschnitt 6.1 und bei der
H3-Hypothese) — methodisch korrekt, da die Unabhängigkeit sich auf andere Anker und Blindheit gegenüber den
Prototyp-Scores stützt, nicht auf eine externe Person. Die bestehende Limitationspassage in Abschnitt 6.3
(„Ground-Truth-Erhebung“, S. 91) wurde erweitert: Sie benennt jetzt explizit, dass die Bewertung nicht durch
Dritte erfolgte, dass ein Bestätigungsfehler durch Vorwissen über das Modell nicht auszuschließen ist, und dass
sich „unabhängig“ ausschließlich auf die methodische, nicht die personelle Trennung bezieht.

**24. ✅ „Hier ist viel Wiederholung der Stichpunkte drinnen. Kürzungspotential.“** — **S. 88** (Abschnitt 6.1)
Der Fließtext-Absatz direkt nach der H1/H2/H3-Itemize-Liste wiederholte deren Inhalt fast wörtlich noch einmal
in Prosa. Absatz entfernt, die darin enthaltenen Zusatzinformationen (Zitat zu konvergenter Validität bei H1,
Klarstellung „Divergenz ist kein Fehler“ bei H2, Synthese-Rolle von H3) direkt in die drei Listenpunkte
eingearbeitet.

**25. ✅ „Link?“ (bei „Notebook 12“)** — **S. 89** (Abschnitt 6.2)
Fußnote mit GitHub-Link auf `playground/notebooks/12_fetch_stratified_sample.ipynb` ergänzt.

**26. ✅ „Link und umformulieren“ (bei „derselben vier Qualitätsdimensionen, die auch der Prototyp verwendet“)** — **S. 90** (Abschnitt 6.3)
Umformuliert zu: „…entlang derselben vier Qualitätsdimensionen, die in Kapitel~4 hergeleitet wurden
(Tabelle~\ref{tab:finale-qualitaetsdimensionen}) und die der Prototyp gemäß Kapitel~5 operationalisiert.“ — wie
vorgeschlagen mit expliziten Kapitel-Querverweisen statt der vagen Formulierung.

**27. ✅ „bis … bis“ (Tippfehler/Formulierung)** — **S. 90** (Abschnitt 6.3)
„…bis etwa fünf bis sieben Kategorien zunehmen…“ → „…**auf** etwa fünf bis sieben Kategorien zunehmen…“.

**28. ✅ „Bitte was?! … ich bin keine Statistikerin. Vielleicht geht das irgendwie verständlicher?“** — **S. 90–91** (Abschnitt 6.3, Central-Tendency-Bias)
Der Absatz zum Verzicht auf einen Skalenmittelpunkt in einen klaren Dreischritt aufgelöst: erst was ein
Skalenmittelpunkt ist, dann was Central-Tendency-Bias bedeutet, dann warum er bei einer ankerbasierten
Bewertung abgeschwächt ist.

*Korrektur (2026-08-12):* Die erste Fassung dieser Vereinfachung behauptete fälschlich, jede der sechs Stufen
sei durch eine eigene Ankerformulierung beschrieben (unter Verweis auf Tabelle~\ref{tab:gt_anker} und
`\cite{jonsson2007rubrics}`). Tatsächlich existiert im Thesis-Text nur eine Ankerfrage pro Dimension, keine
Beschreibung je Stufe — beim Labeln wurde ausschließlich anhand dieser einen Frage pro Dimension bewertet.
Formulierung entsprechend abgeschwächt: „jede Dimension … durch eine … Ankerfrage konkretisiert“ statt „jede
Stufe … durch eine Ankerformulierung beschrieben“, das Ausweichverhalten wird nur noch als „abgeschwächt“
statt als „nicht zu erwarten“ beschrieben, und die zu starke Zitation von `\cite{jonsson2007rubrics}` (die sich
auf Rubriken mit Ankern je Stufe bezieht) wurde entfernt.

## Allgemeine Verbesserungen (nicht kommentargebunden)

Auf Wunsch umgesetzt, unabhängig von einzelnen PDF-Kommentaren:

**A. Unerklärte Statistik-Begriffe vor Erstverwendung kurz erläutert** — **S. 88–93** (Abschnitt 6.5,
„Auswertungsverfahren und Kennzahlen“, sowie Kernstichprobe-Auswertung)
Kurze, unaufdringliche Klammer- bzw. Einschub-Erläuterungen bei Erstnennung ergänzt für: Cohens $\kappa$
(Übereinstimmungsmaß, das Zufallsübereinstimmung herausrechnet), Bootstrap-Konfidenzintervall (durch
wiederholtes Ziehen von Teilstichproben geschätzte Unsicherheitsspanne), Kendalls $\tau$ (weitere,
robustere Rangkorrelation), PABAK (ausgeschrieben: Prevalence-Adjusted Bias-Adjusted Kappa), AUC (Fläche unter
der ROC-Kurve; 0,5 = Zufall, 1,0 = perfekte Trennung), Bland-Altman-Darstellung (Score-Differenz gegen
Score-Mittelwert je Datensatz), Disattenuationskorrektur (Korrektur einer Korrelation um die Messungenauigkeit
beider Seiten) und Cronbachs $\alpha$ (Maß interner Konsistenz zwischen den vier Dimensionswerten).

**B. Fest verdrahtete Kapitel-/Abschnittsverweise auf `\label`/`\ref` umgestellt** — **S. 88–109** (gesamtes
Kapitel 6, rund 20 Stellen)
Alle literalen „Abschnitt~6.X“-Verweise im Evaluationskapitel durch `\ref{}` auf neu gesetzte Labels ersetzt
(u. a. `sec:eval_design`, `sec:eval_stichprobe`, `sec:eval_mqa_abc`, `sec:eval_auswertungsverfahren`,
`sec:eval_modellauswahl`, `subsec:eval_modellauswahl_auswahl`, `subsec:eval_reproduzierbarkeit`,
`sec:eval_ergebnisse_gt`, `subsec:eval_gt_extremfaelle`). Dabei einen bereits bestehenden Fehler gefunden und
mitkorrigiert: „Abschnitt~6.3“ bei der A/B/C-Klassifikation (S. 91) verwies fälschlich auf „Ground-Truth-Erhebung“
statt auf „Vergleichsbaseline: MQA-Reimplementierung und A/B/C-Klassifikation“ (Abschnitt 6.4), wo diese
Klassifikation tatsächlich definiert ist — vermutlich ein Rest aus einer früheren Kapitelnummerierung.

## Weitere Nacharbeiten auf Rückmeldung (nicht kommentargebunden, 2026-08-12)

Nach Rückmeldung, dass Teile von Abschnitt 6.3/6.5 trotz Punkt 28 und Verbesserung A weiterhin schwer
verständlich waren, drei weitere Überarbeitungsrunden:

**C. Bootstrap-Konfidenzintervall und Sekundärmetriken nochmal grundlegend überarbeitet** — **S. 93**
(Abschnitt 6.5)
Verbesserung A hatte Fachbegriffe nur durch andere Fachbegriffe umschrieben, das reichte nicht. Jetzt:
das Bootstrap-Verfahren als eigener, klar formulierter Gedankengang (wiederholtes Ziehen von Teilstichproben
mit Zurücklegen, $\kappa$ jeweils neu berechnen, Bandbreite der Ergebnisse zeigt die Unsicherheit) statt als
eingeschobene Nebenbemerkung; die fünf Sekundärmetriken (Accuracy, gewichtetes $\kappa$, PABAK, AUC,
Konfusionsmatrix) aus einem Bandwurmsatz in eine Liste überführt, die vorab erklärt, *warum* es überhaupt
fünf verschiedene Maße braucht (jedes gleicht eine Schwäche der anderen aus), und bei jedem Punkt sowohl die
Bedeutung als auch die konkrete Schwäche nennt.

**D. „Die Schwellen sind kriteriumsorientiert gesetzt…“ vereinfacht** — **S. 90** (Abschnitt 6.3, Ableitung
des Gesamturteils)
Fachbegriffe „kriteriumsorientiert“, „kompensatorisch“ und „konjunktiv“ aus dem Fließtext entfernt, ohne den
Inhalt zu verlieren: ein Absatz erklärt jetzt, dass die Schwellen inhaltlich und nicht nachträglich an die
Stichprobenverteilung angepasst festgelegt sind, ein zweiter erklärt die Ableitungsregel konkret (Durchschnitt
zählt, aber eine Sperrbedingung verhindert, dass ein einzelner schwerer Mangel im Durchschnitt verschwindet)
mit einem Beispiel (unklare Lizenz bei sonst guten Metadaten).

**E. Dopplung in der Limitation-Passage entfernt** — **S. 91** (Abschnitt 6.3)
Der Absatz zur Selbstbewertung (siehe Punkt 23) sagte zweimal hintereinander in leicht anderen Worten, dass
keine unbeteiligte dritte Person bewertet hat: einmal direkt, einmal über die Erklärung, worauf sich
„unabhängig“ bezieht. Zu einem Satz zusammengezogen, Rest der Passage unverändert.

**F. Gedankenstriche (`--`) und Semikolons (`;`) in den selbst verfassten Passagen reduziert** — **S. 88–93**
(Abschnitt 6.1–6.5)
In allen Textstellen, die im Rahmen dieser Überarbeitung neu formuliert wurden (Punkte 23–28, A, C, D),
`--` und `;` durch Punkte, Kommas, Doppelpunkte oder Klammern ersetzt und dabei ein durch eine frühere
Bearbeitung entstandenes Satzfragment ohne Verb korrigiert. Ursprünglicher, unveränderter Text des Autors
(z. B. an Stellen, wo nur eine Kapitelnummer durch `\ref` ersetzt wurde) wurde dabei bewusst nicht angetastet.

---

## Offene Punkte

- **Punkt 16** (`foaf:page`-Verlinkung von Dokumentations-Distributionen) — nicht umgesetzt.
- **Punkt 17** (Health-Checks / Ausfallhäufigkeit des SHACL-Validierungsdienstes) — Fußnote beantwortet nur den
  Nebenaspekt (405-Antwort bei Browser-Aufruf), nicht die eigentliche Frage nach Monitoring/Downtime.
