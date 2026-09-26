# Kolloquium – Stichpunkte & Zeitplan (v3-Foliensatz)

Ziel: ca. 30 Minuten **inklusive Live-Demo**. Basis: `kolloquium_buerger_v3.pptx/pdf`
(23 PDF-Seiten: 21 sichtbare Hauptfolien mit der Nummerierung 1–8 und 10–22, Folie 9 ist
ausgeblendet, dazu 2 Backup-Folien 23/24, die nicht mitgezählt werden).

**Zeitrechnung:** ~25 Min Vortragsinhalt + 5 Min Demo ≈ 30 Min.
Die Stichpunkte sind bewusst großzügig – gedacht zum Wegstreichen, nicht zum Vorlesen.
Wo es bei Zeitdruck am ehesten geht, steht jeweils am Folienende unter *Kürzen:*.

| Block | Folien | Budget |
|---|---|---|
| Einstieg | 1–3 | ~2,5 Min |
| Grundlagen & Modellkonzeption | 4–8 | ~7 Min |
| Prototyp + Demo | 10–12 | ~7,5 Min |
| Evaluation | 13–17 | ~7,5 Min |
| Schluss | 18–22 | ~5,5 Min |

---

## Einstieg (≈2,5 Min)

### 1 – Titel (20 s)
- Kurz vorstellen, Titel nennen, Betreuung danken (Stephanie Bornholdt, Prof. Dr. Eiglsperger)
- Ein Satz zur Einordnung: Bewertungsmodell + Prototyp + Evaluation für DCAT-AP.de-Metadaten im GovData-Kontext

### 2 – Ausgangslage (75 s)
- **GovData ist Aggregator, nicht Datenhalter**: bündelt Metadaten von Bund, Ländern und Kommunen; die
  Datensätze selbst bleiben dezentral bei den bereitstellenden Stellen. Produktmanagement bei der FITKO,
  föderal besetztes Produktboard → Qualität entsteht verteilt und in sehr unterschiedlicher Tiefe
- **Metadaten sind die Beschreibungsschicht**: über sie wird gefunden, eingeordnet und nachgenutzt.
  Unvollständige oder inkonsistente Metadaten senken den Nutzen der Open-Data-Initiative unmittelbar
- **151.579 Datensätze** (CKAN-Vollauszug vom 15.05.2026) → jede manuelle Prüfung ist ausgeschlossen,
  Bewertung muss automatisiert laufen
- **DCAT-AP.de** = deutsche Ableitung von DCAT-AP (EU), das wiederum auf dem W3C-Vokabular DCAT aufbaut –
  mehrstufige Interoperabilitätskette, deshalb ist Standardkonformität überhaupt relevant
- **Kernsatz:** Die SHACL-Validierung prüft Struktur, Syntax, Pflichtfelder, Datentypen und Vokabular-URIs –
  nicht, ob mit der Angabe etwas anzufangen ist. Ein Metadatensatz kann formal vollständig valide und für
  Nutzende trotzdem unbrauchbar sein
- Optional als Aufhänger: Eine Beschreibung, die aus dem einen Wort „Justizblatt“ besteht, ist SHACL-valide
  (greift Folie 17 vor)

*Kürzen:* DCAT-Ableitungskette und der Justizblatt-Vorgriff.

### 3 – Forschungsfragen (45 s)
- Leitfrage vorlesen, dann den Nebensatz betonen: **„…ohne die Nachvollziehbarkeit zu gefährden“** –
  Nachvollziehbarkeit ist das durchgängige Entwurfsziel, nicht nur ein Nebenkriterium
- Die 5 Teilfragen nur überfliegen, nicht einzeln erklären – Folie 18 gibt die Antworten
- Optional: Die Zielsetzung sah ursprünglich eine agentenbasierte Architektur vor; was daraus geworden ist,
  kommt auf Folie 10

---

## Grundlagen & Modellkonzeption (≈7 Min)

### 4 – Bewertungslücke bestehender Ansätze (90 s)
- Zwei Achsen aufspannen: **Anwendungsnähe × Operationalisierbarkeit**. Keine der drei Gruppen erfüllt beides
- **Abstrakte Konzepte** (Wang & Strong 1996, ISO/IEC 25012, FAIR): begründen Qualität als mehrdimensionales,
  *nutzungsabhängiges* Konzept – legen aber nicht fest, welche Metadatenelemente, Vokabulare oder Zugriffspfade
  konkret zu prüfen sind
- **Nicht operationalisierbare Metriken** (Zaveri et al.; Nogueras-Iso et al. / ISO 19157): machen Qualität
  jenseits formaler Validität sichtbar, setzen für viele Prüfungen aber Kontextwissen, externe Referenzdaten
  oder stichprobenbasierte manuelle Inspektion voraus → nicht skalierbar
- **Geringe Prüftiefe** (Neumaier et al. / Open Data Portal Watch, MQA/Piveau): dem Anwendungskontext am
  nächsten und automatisiert prüfbar, dafür verengt auf leicht messbare, überwiegend feldbezogene Kriterien
- MQA konkret benennen, weil sie später die Vergleichsbaseline ist: 405-Punkte-System, 5 Dimensionen
  (Findability, Accessibility, Interoperability, Reusability, Contextuality), **Best-Distribution-Prinzip**
- **Zweite, oft übersehene Lücke – die empirische Absicherung:** Für *keinen* der dargestellten Ansätze liegt
  eine Angabe darüber vor, wie stark seine Werte mit dem Qualitätsurteil von Nutzenden zusammenhängen.
  Als Erfolgskontrolle dient überwiegend „der Score steigt“ – das belegt nur eine zunehmende Passung der Daten
  an die Metrik, keine bessere Nutzbarkeit
- Unterrepräsentiert bleiben damit: semantische Aussagekraft von Titel und Beschreibung, Verständlichkeit,
  kontextabhängige Feldrelevanz, Plausibilität zwischen Angaben, Metadaten-Daten-Kongruenz

*Kürzen:* Die Einzelautoren pro Gruppe – die Gruppenlogik trägt allein.

### 5 – Experteninterviews (75 s)
- **3 leitfadengestützte Experteninterviews**, 16.–24.04.2026, jeweils 24–41 Minuten;
  Interviewpartner aus dem FITKO-Umfeld (GovData-Produktmanagement / DCAT-AP.de-Standardisierung) und dem
  Open Data Competence Center Bayern (Qualitätsberatung / praktische Datenbereitstellung)
- Auswertung: qualitative Inhaltsanalyse nach Mayring, inhaltlich strukturierend mit kombiniert
  deduktiv-induktiver Kategorienbildung → 10 Kategorien K1–K10, Belegstellen über Interview-ID + Absatznummer
- Zweck klar sagen: **keine statistische Generalisierung**, sondern praxisbezogene Präzisierung und
  Priorisierung der literaturbasierten Dimensionen
- Die 5 Anforderungen kurz mit Inhalt füllen:
  1. Formale Validierung als **Basisschicht** – notwendig, aber nicht mit Gesamtqualität gleichzusetzen
  2. **Kontextsensitive Vollständigkeit** – relevante statt aller Felder, Pflicht/empfohlen/kontextspezifisch trennen
  3. **Semantische Qualität** – Titel, Beschreibung, Keywords können vorhanden und trotzdem nichtssagend,
     redundant, fachsprachlich unverständlich oder widersprüchlich sein
  4. **Technische Nutzbarkeit** – defekte Links, nicht erreichbare Downloads, Linkrot als zentrale Praxisprobleme
  5. **Transparentes Reporting** – Teil-Scores plus konkrete, auf Verbesserung ausgerichtete Hinweise
- **Quer dazu K10 (Automatisierungsgrenze):** KI als unterstützendes Werkzeug ja, als autonome Bewertungsinstanz
  nein – Halluzination, stochastische Ausreißer, Datenhoheit, Ressourcenaufwand. Prägt direkt Folie 10
- „Fit for Purpose statt Formalerfüllung“: Die Frage nach *dem* perfekten Metadatensatz konnte in keinem
  Interview beantwortet werden – kommt auf Folie 19 als konzeptionelle Grenze zurück

*Kürzen:* Auswertungsmethodik (Mayring, Kategorienzahl).

### 6 – Verdichtung 15 → 4 Dimensionen (75 s)
- **Longlist von 15 Kandidatendimensionen**, Aufnahme über 5 Kriterien: in mindestens einem Literaturansatz
  verankert, durch Interviews gestützt oder für GovData plausibel, fachlich relevant, mindestens durch einen
  Indikator operationalisierbar, nicht vollständig durch eine andere Dimension abgedeckt
- **Verdichtungsprinzip:** Zusammengeführt wird nach **Bewertungsfunktion**, nicht nach Literaturherkunft.
  Methodisches Vorbild: Wang & Strong haben ihre empirisch ermittelten Dimensionen in der letzten
  Verdichtungsstufe genauso zugeordnet
- Warum 4 und nicht 15: eine kleine, möglichst orthogonale Dimensionsmenge ist Voraussetzung für die in
  Teilfrage 4 geforderte Operationalisierbarkeit und für ein im Reporting nachvollziehbares Scoring
- Die 4 Dimensionen einmal mit ihrer Leitfrage laut vorlesen – das ist der Rahmen für alles Folgende
- **Wichtig:** Die formale DCAT-AP.de-Konformität ist *keine* eigene Dimension. Pflichtfeldprüfungen macht
  SHACL bereits; sie wird deshalb nicht feldweise dupliziert, sondern geht als ein einzelner aggregierter
  Indikator (N6) in die Nachnutzbarkeit ein. Anschlussfähig an die MQA, die es genauso hält
- Ehrliche Einschränkung gleich mitliefern: Anforderung 2 (nutzungsabhängige Vollständigkeit) bleibt nur
  teilweise abgedeckt – umgesetzt ist davon allein die Ergebnisstufe „nicht anwendbar“

*Kürzen:* die 5 Longlist-Aufnahmekriterien.

### 7 – Indikatoren & Messmodell (105 s) — *inhaltlich dichteste Folie*
- **27 aktive Einzelindikatoren** in drei Typen: **FI** formal (empfohlene/optionale Felder, kontrollierte
  Vokabulare, URI-Strukturen), **TI** technisch (Erreichbarkeit, HTTP-Status, Format, Maschinenlesbarkeit),
  **SI** semantisch (Aussagekraft, Kohärenz, Plausibilität)
- Ableitung nach dem **Goal-Question-Metric-Prinzip** (Basili): Metriken top-down aus den Dimensionszielen.
  Auswahl über 6 Kriterien: Standardbezug, Konventionsbezug, Literaturbezug, Interviewbezug,
  Operationalisierbarkeit, Reportingfähigkeit
- **Jeder Indikator trägt eine Herleitungsspalte** (SPEC, KONV xx, MQA, NEU, ZAV, FAIR, HMQ, INT-Kx) →
  lückenlos auf Standard, Konventionenhandbuch, Literatur oder Interviewkategorie rückführbar.
  Das ist ein eigener Teil des wissenschaftlichen Beitrags (Folie 21) – ruhig betonen
- Tabelle nicht vorlesen, nur je 1 Beispiel pro Spalte: A1 Schlagwortumfang · Z5 Erreichbarkeit Download-URL ·
  S2 Aussagekraft der Beschreibung
- Bewusst **nicht** aufgenommen: reine Pflichtfeld-Existenzprüfungen (macht SHACL)
- **Die 4 Messprinzipien – hier lohnt Zeit, sie kommen in der Evaluation wieder:**
  - **Ergebnisstufen** erfüllt / teilweise erfüllt / nicht erfüllt. Die Zwischenstufe ist nötig, z. B. bei einer
    gesetzten Themenkategorie, die nicht aus dem kontrollierten Vokabular stammt: höherwertig als keine Angabe,
    aber nicht standardkonform. Eine binäre Prüfung müsste zu streng oder zu nachsichtig sein
  - **Ternär vs. graduell** (angelehnt an die Skalentypen der ISO/IEC 25024): ternär = ordinal 1 / 0,5 / 0;
    graduell = kontinuierlicher Erfüllungsgrad 0–1, der *unverfälscht* in die Aggregation eingeht – die
    Ergebnisstufe dient dort nur der Darstellung im Reporting
  - **Mittelung über Distributionen statt Best-Distribution.** Die MQA lässt bei mehreren Distributionen die
    beste das Ergebnis bestimmen. Deren Annahme („alle Distributionen sind derselbe Inhalt in anderen Formaten“)
    trägt in der Praxis nicht – DCAT 3 führt für inhaltlich eigenständige Teildatensätze erst
    `dcat:DatasetSeries` ein. Unter Best-Distribution bleibt eine tote Download-URL folgenlos, solange eine
    Distribution funktioniert → systematische Überbewertung aus Nutzendensicht.
    Begrifflich: *conflict-avoiding* (maskiert Inkonsistenzen) vs. bewusst gewähltes *conflict-resolving*
  - **Malus-Prinzip.** Eine angegebene, aber nicht erreichbare URL und eine eingeschränkte/unklare/fehlende
    Lizenz gehen mit **−0,5** statt 0 ein: Sie sind schlechter als das Fehlen der Angabe, weil sie Verfügbarkeit
    vortäuschen bzw. die Nachnutzung rechtlich unsicher machen. Konkret: **zwei defekte Distributionen heben
    den Beitrag einer funktionierenden vollständig auf.** Dimensionswert wird bei 0 nach unten gekappt
  - **Nicht anwendbar.** Neutral überspringen – geht weder in Zähler noch Nenner ein. Die Entscheidung ist Teil
    der Prüflogik des Indikators selbst, im Prototyp betrifft das nur S6 (kontextuelle Qualifizierer)
- Gute Anekdote für Rückfragen: **2 Kongruenzindikatoren wurden implementiert und wieder deaktiviert**
  (Format/Medientyp vs. tatsächlich ausgelieferter Inhaltstyp; repräsentieren die Distributionen denselben
  Inhalt?). Grund: Heterogenität der Modellierungspraxis, Zahl der Sonderfälle nicht beherrschbar.
  Kriterium dahinter: **Die Unsicherheit einer Messung muss kleiner bleiben als ihr Informationsbeitrag** –
  sonst verschlechtert der Indikator das Gesamturteil, statt es zu präzisieren

*Kürzen:* GQM/Auswahlkriterien und die Kongruenz-Anekdote (Letztere für den Fragenteil aufheben).

### 8 – Scoring & Gewichtung (75 s)
- **Zweistufige Aggregation**, beide Stufen gewichtete Mittelwerte, alle Gewichte konfigurierbar (nicht im Code):
  Indikator → Dimension (über die aktiven *und anwendbaren* Indikatoren, bei 0 gekappt) → Gesamtscore
- Punktevergabe: erfüllt 1,0 / teilweise 0,5 / nicht erfüllt 0,0; graduelle Indikatoren tragen ihren
  Erfüllungsgrad direkt bei. Notenstufen A ≥ 0,9 · B ≥ 0,75 · C ≥ 0,6 · D ≥ 0,4 · sonst F – rein konventionell,
  ohne Einfluss auf die Rechnung
- **Indikatorgewichte bleiben nah an 1,0**, angehoben werden nur vier: Z5, Z6, N1 auf **2,0**, Z7 auf **1,5**
- Begründung für die 2,0er: Ein Defekt macht den Datensatz *faktisch unbrauchbar*, egal wie gut der Rest ist.
  Das sind genau die definierenden Merkmale offener Daten aus Kapitel 2 (Zugang ohne Beschränkung, Bedingungen,
  die Wiederverwendung erlauben) und dieselben Defekte, die die Interviews als Hauptpraxisprobleme nennen (K5).
  Z7 (Maschinenlesbarkeit) bewusst dazwischen: ebenfalls definierendes Merkmal, aber eine einzelne nicht
  maschinenlesbare Distribution ist nicht zwingend datenbrechend
- **Dimensionsgewichte:** Zugänglichkeit 2,0 · Aussagekraft 2,0 · Nachnutzbarkeit 1,5 · Auffindbarkeit 1,0.
  Ein Versagen in Zugänglichkeit oder Aussagekraft entwertet den Datensatz am stärksten; Auffindbarkeit sind
  überwiegend Präsenz- und Strukturprüfungen, und ihr Nutzen hängt von der Erfüllung der anderen ab –
  ein auffindbarer Datensatz ohne Lizenz bleibt nutzlos
- **Bewusste Abweichung von der MQA**, die Auffindbarkeit zu den höchstgewichteten Dimensionen zählt –
  auf Basis reiner Präsenzmetriken. (Wird auf Folie 15 als Erklärung der einzigen Ausnahme wieder gebraucht!)
- Ehrlich dazusagen: Gewichte und Punktwerte sind **normative Setzungen**. Auch die MQA legt ihre 405 Punkte
  per Konvention fest, und die Literatur zu zusammengesetzten Indikatoren (Nardo et al.) behandelt das als
  dokumentationspflichtige Entwurfsentscheidung. Maßgeblich sind die **Relationen**, nicht die Absolutwerte:
  Teilerfüllung zählt halb, ein irreführender Defekt wiegt schwerer als eine fehlende Angabe

*Kürzen:* die Formeln nur zeigen, nicht durchsprechen – die Gewichtsbegründung ist der Mehrwert.

---

## Prototyp (≈2,5 Min + 5 Min Demo)

### 10 – Sprachmodellgestützte Bewertung der Aussagekraft (90 s)
- **Warum überhaupt ein Sprachmodell:** Aussagekraft ist die einzige Dimension ohne regelbasierte Prüfbarkeit.
  Ob ein Titel für sich verständlich ist oder eine Beschreibung inhaltlichen Mehrwert liefert, lässt sich weder
  über Feldexistenz noch über syntaktische Muster entscheiden
- **Bewusste Abweichung von der Interview-Skepsis (K10)** – offen ansprechen. Drei Vorkehrungen begrenzen den
  Schritt: (1) Beschränkung auf 1 von 4 Dimensionen und einen einzigen Aufruf ohne Agentenkette,
  (2) strukturierte, begründungspflichtige Ausgabe, (3) Temperatur 0
- Der **Aufgabenschnitt selbst** begrenzt das Halluzinationsrisiko: Bewertet wird nicht, ob eine Angabe sachlich
  zutrifft, sondern ob die Freitextfelder untereinander und zum übrigen Datensatz passen → kein Weltwissen nötig
  (ausgeräumt ist das Risiko damit nicht, das auch sagen)
- **Ein-Aufruf-Architektur:** statt 6 Einzelabfragen 1 Aufruf je Datensatz. Weniger Kosten, und vor allem
  konsistentere Urteile – alle sechs Kriterien gehen aus derselben ganzheitlichen Betrachtung hervor,
  Widersprüche zwischen Einzelurteilen werden unwahrscheinlich. Schlägt der Aufruf fehl, melden die Indikatoren
  „nicht anwendbar“, statt den Lauf abzubrechen
- **Explizit machen:** An die Stelle der in der Zielsetzung skizzierten Agentenarchitektur tritt eine einzelne
  strukturierte Abfrage – Entscheidung zugunsten der Nachvollziehbarkeit. Eine mehrstufige Kette hätte
  Fehlerfortpflanzung, und das Zustandekommen des Urteils wäre nicht mehr an einer Stelle nachlesbar
- **Strukturierte Ausgabe** (Pydantic-Schema, als verbindliche Ausgabestruktur erzwungen, keine Nachverarbeitung):
  je Kriterium `findings` (1–3 beobachtbare Befunde) → `reasoning` → `applicable` → `score` (0–1).
  **Die Reihenfolge erzwingt Evidenz vor Zahl** – das Modell muss erst benennen, was es sieht
- Die diskrete Ergebnisstufe wird **deterministisch aus dem Score abgeleitet**, nicht vom Modell erfragt →
  Stufe und Wert können sich nicht widersprechen. `applicable` setzt die Nicht-Anwendbarkeit aus dem Messmodell um
- **Die Rubrik ist nicht frei erfunden:** abgeleitet aus dem DCAT-AP.de-Konventionenhandbuch v2.0 (Kap. 1.7, 3.4)
  und der Handreichung zur Verbesserung der Metadatenqualität, plus einer Ankerskala, die Wertebereiche verbal
  an Qualitätsniveaus bindet
- Zwei Robustheitsvorkehrungen: Feldpräsenz darf nicht als Qualität gewertet werden (generische, kryptische oder
  widersprüchliche Angaben werden trotz Vorhandensein abgewertet); der Metadateninhalt ist durch Trennmarken
  abgegrenzt und ausdrücklich als reiner Bewertungsgegenstand deklariert → **Prompt-Injection-Schutz**
- Datenschutz in einem Satz erledigen: bewertet werden ausschließlich ohnehin öffentlich publizierte Metadaten

*Kürzen:* Prompt-Injection und Datenschutz – nur auf Nachfrage.

### 11 – Verarbeitungspipeline (60 s) — *nur Grafik, frei erzählen*
- **Drei Entwurfsentscheidungen** vorweg: (1) alle bewertungsrelevanten Fakten genau einmal erheben und in einer
  typisierten **Faktenbasis** ablegen, auf der alle Indikatoren arbeiten; (2) beide teuren Anreicherungsschritte
  **bedarfsgesteuert**; (3) Indikatorenkatalog über Selbstregistrierung erweiterbar – ein neuer Indikator ist eine
  Klasse mit einer Prüfmethode, die Verarbeitungskette bleibt unverändert
- **Ablauf entlang der Grafik:** RDF/XML einlesen → Graph *einmal* traversieren → Faktenbasis, dabei schon
  vorberechnet, ob Themen, Formate, Medientypen und Lizenzen den kontrollierten Vokabularen angehören →
  technische Anreicherung (Erreichbarkeit) → semantische Anreicherung (1 LLM-Aufruf) → Indikatoren der
  4 Dimensionen → Scoring → JSON-Report + Protokolle. Nach dem letzten Datensatz laufweite Kennzahlen,
  Diagramme und Kostenübersicht
- **„bedarfsgesteuert“ betonen:** Netzabruf und Sprachmodellaufruf entfallen komplett, wenn nach der aktiven
  Konfiguration kein Indikator ihre Ergebnisse konsumiert
- Erreichbarkeitsprüfung: jede eindeutige URL höchstens **einmal je Lauf**, HEAD plus ergänzend GET mit
  abgebrochenem Inhaltsbezug (Verbindung nach den Antwort-Headern geschlossen, Body wird nie gelesen)
- Vokabularprüfungen gegen **lokal mitgelieferte Kopien** (EU-Vokabulare für Themen/Dateitypen/Frequenzen,
  IANA-Medientypregister, DCAT-AP.de-Lizenzliste, Contributor-IDs, politische Geokodierung) → deterministisch
  und unabhängig von der Verfügbarkeit externer Dienste
- 3 externe Abhängigkeiten: Distributions-Endpunkte, Sprachmodell, SHACL-Validierungsdienst (kommt auf Folie 20 wieder)
- Stack in einem Halbsatz: Python 3.12, rdflib, requests, Pydantic, LangChain, **Hydra** (Gewichte und
  Indikatormenge konfigurierbar ohne Code-Änderung), matplotlib
- **Abgrenzung:** kein Harvesting, kein Dauerbetrieb, kein Monitoring – Analysewerkzeug für Einzel- und
  Stichprobenläufe. Bewertet werden die Metadaten und ihre technische Einlösbarkeit, **nicht** die fachliche
  Qualität der beschriebenen Daten

*Kürzen:* Stack und HEAD/GET-Detail.

### 12 – Live-Demo (15 s Übergang + 5 Min)
**Übergangssatz:** Ein Qualitätsbefund wirkt dort, wo die Metadaten ohnehin gepflegt werden. Deshalb liegt die
Bewertung als zusätzliche Ebene in den gewohnten Portalansichten und nicht in einem separaten Upload-Tool.

**Vor dem Bildschirmwechsel in zwei Sätzen einordnen:**
- Die Nachbildung der GovData-Oberfläche ist **Mittel zum Zweck und nicht Gegenstand der Arbeit** – sie zeigt,
  dass sich die Ergebnisse einbetten lassen. Die Bewertung liegt als eigene Ebene neben dem Bestand, verknüpft
  allein über die Identität des Datensatzes: Ein produktives Portal müsste sein Datenmodell nicht erweitern
- **Drei Auflösungsstufen für drei Zielgruppen**, nach Shneiderman „Overview first, zoom and filter,
  details on demand“: Datennutzende = Auswahlkriterium (Gesamtscore) · Datenbereitstellende = Arbeitsauftrag
  (Befund je Indikator) · Portalbetreibende = Steuerungsinstrument (Aggregation über den Bestand)

**Demo-Skript:**
1. **Trefferliste**: Qualitätsfacette links neben den bestehenden Filtern, Score je Treffer rechts neben den
   beschreibenden Angaben
2. **Infotag** am Treffer aufklappen: 4 Dimensionswerte + Anteil erfüllter Indikatoren, ohne die Seite zu verlassen
   („dasselbe Ordnungsprinzip wiederholt sich innerhalb eines einzelnen Treffers“)
3. **Detailsicht** eines schlecht bewerteten Datensatzes: Note, Gesamtscore, Netzdiagramm über die vier Dimensionen,
   darunter je Dimension Score, Gewicht und Anzahl der Indikatoren mit Handlungsbedarf.
   Schalter „nur Handlungsbedarf“ zeigen
4. **Einen Befund aufklappen** – das ist der Kern: Kernaussage → Ist-Angaben mit **Fundstelle** → Hinweis als
   **Handlungsanweisung** („was zu tun ist“, nicht „wie es richtig aussähe“). Über alle 27 Indikatoren dieselbe
   Form – gelernt wird sie einmal. Vorbild sind die Konformitätsprüfdienste des W3C: Schweregrad, Kernaussage,
   Position in der Quelle, Quelltextauszug. Der Befund entsteht im **Bewertungskern**, nicht in der Oberfläche
5. **Vorlage** zeigen (z. B. politische Geokodierung): kurzes RDF/XML-Fragment in korrekter Schreibweise mit
   Beispielwert, dazu Vokabularname und Link. Pointe: Die Vorlage ist **unabhängig vom vorgefundenen Zustand** –
   sie wird gerade dann gebraucht, wenn das Feld ganz fehlt und es nichts gibt, worauf man zeigen könnte.
   Bei inhaltsabhängigen Indikatoren tritt stattdessen die **Fundstelle** mit Zeilennummer an ihre Stelle
6. **Aggregatsicht**: Zahl der Datensätze, mittlerer Score mit Spannweite, Verteilung, Mittelwerte je Dimension,
   häufigste Mängel, Verlauf über die Läufe. Dazusagen: Die Verlaufspunkte sind Bewertungsläufe, keine
   Erhebungszeitpunkte – erst bei wiederholtem Harvesting wird daraus eine Qualitätsentwicklung

**Satz zur Belastbarkeit (gut am Ende der Demo):** Die Oberfläche führt keine eigenen Voreinstellungen, sondern
lädt zur Laufzeit dieselbe Konfigurationsdatei, die auch der Evaluation zugrunde liegt – Gewichte, Punktevergabe
und Indikatormenge sind nicht nur ähnlich, sondern identisch.

*Kürzen:* zuerst Schritt 6, dann Schritt 2.

---

## Evaluation (≈7,5 Min) — Herzstück, hier nicht hetzen

### 13 – Evaluationsdesign (90 s)
- **Zwei komplementäre Stränge auf identischem RDF-Input.** Ground Truth beantwortet „bewertet er *korrekt*“,
  MQA-Baseline beantwortet „was sieht er *zusätzlich*“. Die Reihenfolge ist zwingend: Der Baseline-Vergleich
  allein zeigt nur, dass sich die Bewertungen unterscheiden – nicht, welche näher an der tatsächlichen Qualität liegt
- **Datengrundlage:** CKAN-Vollauszug 15.05.2026, 151.579 Datensätze; 1.793 Datensätze mit NetCDF-Distributionen
  entfernt (dominieren Laufzeit und Datenvolumen der Erreichbarkeitsprüfung ohne Erkenntnisgewinn) → 149.786;
  Aufteilung in 25.416 Geo- und 124.370 Nicht-Geo-Datensätze
- **Kernstichprobe n = 50:** stratifizierte Zufallsstichprobe, gezogen am 25.06.2026, Seed 67, über ein Notebook
  reproduzierbar. 10 Straten (Geo/Nicht-Geo × 4 aufkommensstärkste Bereitsteller + Restkategorie), je 5 Datensätze.
  Ohne Schichtung würden die wenigen großen Portale die Stichprobe dominieren
- **Extremfälle n = 20:** je 10 konstruiert gut / konstruiert schlecht. Sie belegen den Wirkmechanismus *per
  Konstruktion*, tragen aber **keine quantitativen Aussagen** – sie sind nicht randomisiert. Alle Kennzahlen der
  Arbeit stützen sich auf die Kernstichprobe (das wird auf Folie 16 noch wichtig)
- **Ground Truth:** alle 70 Datensätze, sechsstufige Skala 0–5 je Dimension, je eine ausformulierte Ankerfrage.
  6 Stufen nach Preston & Colman (Reliabilität, Validität und Diskriminierungsfähigkeit steigen bis ~5–7 Stufen,
  4 Stufen sind suboptimal); gerade Stufenzahl → kein Mittelpunkt → kein Ausweichen bei Unsicherheit
- **Methodisch entscheidend:** Die Anker beschreiben die **nutzerseitige Qualitätserfahrung**, nicht die
  Indikatorlogik des Prototyps – sonst würde man die eigene Prüflogik nur manuell nachvollziehen statt dasselbe
  Konstrukt unabhängig zu messen
- **Gesamturteil gut/mittel/schlecht:** Durchschnitt der vier Dimensionen **plus konjunktive Sperrbedingung**
  („gut“ nur, wenn keine Dimension unter 3) – ein gravierender Einzelmangel soll nicht im Durchschnitt der
  übrigen drei verschwinden. Schwellen kriteriumsorientiert **vorab** gesetzt, nicht an die Stichprobenverteilung
  angepasst
- **Blind gegenüber den Prototyp-Scores** (Anchoring-Bias). Aber: dieselbe Person hat Modell und Referenz erstellt
  → keine Inter-Rater-Reliabilität bestimmbar (kommt auf Folie 20 wieder)
- **MQA-Baseline:** nach offizieller Methodik reimplementiert, gegen die veröffentlichten data.europa.eu-Berichte
  validiert; wo die Methodik offenlässt, wie mehrere Distributionen behandelt werden, aus dem öffentlichen
  Quellcode des Scoring-Dienstes nachvollzogen. Skalen vor dem Vergleich normalisiert.
  Metrics v2 bewusst *nicht* als Baseline: weder stabile Spezifikation noch betriebene Instanz
- **A/B/C-Klassifikation jedes Prototyp-Indikators:** A = prüft im Kern dasselbe wie eine MQA-Metrik (H1) ·
  B = MQA honoriert Vorhandensein, Prototyp verifiziert Gültigkeit/Kongruenz, MQA-PASS + Prototyp-FAIL =
  nachgewiesene Überschätzung (H2) · C = kein MQA-Pendant, u. a. die gesamte Aussagekraft (H2).
  Entspricht konvergenter vs. inkrementeller Validität
- **Fairness explizit:** Auch die Gegenrichtung ist ausgewiesen – 4 MQA-Metriken ohne Prototyp-Pendant
  (`dct:rights`, `dcat:byteSize`, zweimal `dct:accessRights`) = 25 von 405 MQA-Punkten
- **Warum ρ und nicht κ als Primärmetrik:** (a) die Frage ist ordinal – geprüft wird, ob dieselbe Rangordnung
  entsteht; (b) 88 % der GT-Urteile liegen in der Kategorie *mittel*, die zufällig zu erwartende Übereinstimmung
  liegt dadurch schon bei ~0,79 → **Kappa-Paradox**; (c) das Bootstrap-Konfidenzintervall für κ reicht von
  0,18 bis 0,92 und überspannt damit den gesamten Bereich. Ergänzt um Kendall τ, Ceiling-Analyse, MAE/Bias,
  Accuracy, PABAK, AUC und Konfusionsmatrix
- **Deckenprüfung vorab** (wichtig, falls gefragt wird, ob das Verfahren einfach zu streng misst):
  Der Referenzdatensatz – der Lübeck-Feinstaubdatensatz als konstruierter Idealfall – erreicht **27 von 27
  Indikatoren** und einen Gesamtscore von **0,991**. Die drei deterministischen Dimensionen liegen exakt bei 1,000,
  **kein einziger Malus greift**. Damit ist der Einwand für sie ausgeräumt: Wo die Stichproben niedriger liegen,
  ist das ein Befund über die Metadaten, nicht über das Verfahren. Nur die Aussagekraft bleibt mit 0,972 knapp
  darunter → faktische Obergrenze bei ~0,97, Abstände in diesem Bereich nicht überinterpretieren

*Kürzen:* NetCDF-Ausschluss, Fairness-Absatz, Deckenprüfung (Letztere für den Fragenteil aufheben).

### 14 – Hauptergebnisse im Überblick (105 s) — *Kernaussage der Arbeit, Zeit lassen*
Jede Zahl kurz einordnen, nicht nur vorlesen:
- **ρ = 0,765** (Kernstichprobe, gesamt): Der Prototyp ordnet die Datensätze weitgehend so wie der menschliche
  Maßstab
- **92 % korrekte Gesamteinordnung** – und, wichtiger als die Quote: Beide Fehlklassifikationen liegen an der
  Schwelle *gut/mittel*, keine an *mittel/schlecht*. Der Prototyp verwechselt ausschließlich benachbarte Stufen
- Ergänzend, falls jemand nach Robustheit fragt: gewichtetes κ = 0,635 · PABAK = 0,88 · AUC = 0,907 ·
  MAE = 0,289 auf der 0–5-Skala · Bias = +0,018, also praktisch keine Niveauverschiebung
- Ceiling-Ausschöpfung je Dimension: Auffindbarkeit 0,524 (68,3 %) · Zugänglichkeit 0,712 (74,8 %) ·
  Nachnutzbarkeit 0,739 (79,6 %) · Aussagekraft 0,569 (66,8 %)
- **ρ = 0,834** gegenüber der MQA-Baseline, mittlere Differenz nur −0,022 Skalenpunkte
- **H1 belegt:** Auf den 9 Klasse-A-Indikatoren stimmen beide Verfahren in **96,0 %** von 450
  Datei-Indikator-Paaren überein (298× beide PASS, 134× beide FAIL). Die 18 Abweichungen sind **17 : 1**
  asymmetrisch – die MQA vergibt deutlich häufiger einen Pass, den der Prototyp verweigert
- **H2 belegt:** **15,8 % Überschätzungsrate** auf den 9 Klasse-B-Indikatoren (71 von 450).
  Stärkster Einzelbefund: **politische Geokodierung – bei 28 von 50 Datensätzen (56 %)** vergibt die MQA einen
  PASS für bloße Existenz, während der Prototyp die tatsächliche Gültigkeit prüft und verweigert
- **Klasse C:** Dort, wo die MQA per Design flach bleibt, differenziert der Prototyp sichtbar – die
  Beschreibungsqualität streut von 0 bis 0,9 (Mittelwert 0,46, σ 0,22)
- **H3 belegt:** **5 von 6** Zielgrößen auf der Kernstichprobe, **6 von 6** auf den Extremfällen näher am
  menschlichen Urteil
- **Den überraschenden Befund ruhig als solchen benennen:** Trotz 15,8 % nachgewiesener Überschätzung korrelieren
  die Gesamtscores mit 0,834 und unterscheiden sich im Mittel um 0,022 Punkte. Erklärung: Der Prototyp bewertet
  überwiegend **dieselben** Datensätze strenger, statt **andere** Datensätze anders – Rangvertauschungen, die ρ
  senken würden, treten kaum auf. **Der Gesamtscore verdeckt reale Messunterschiede.** Genau deshalb wurde der
  Vergleich über die A/B/C-Klassifikation geführt und nicht auf Scoreebene – und derselbe methodische Kurzschluss
  liegt den Erfolgskontrollen bestehender Verfahren zugrunde („der Score steigt also wird’s besser“)

*Kürzen:* die Zusatzkennzahlen (κ/PABAK/AUC/MAE) und die Ceiling-Liste.

### 15 – Triangulation auf der Kernstichprobe (75 s)
- **Präzisierung vorweg** (sonst missverständlich): Auf der Prototyp-Seite steht hier durchgehend der **globale
  Gesamtscore**, nicht die jeweilige Teilbewertung. Notwendig, weil die MQA keine vergleichbaren Teilscores hat.
  Die Zeile „Auffindbarkeit“ misst also, wie gut der *Gesamtscore* die menschliche Auffindbarkeits-Einschätzung
  vorhersagt
- **Kernstichprobe, Prototyp vs. MQA:** gesamt 0,750 / 0,704 · ohne Aussagekraft 0,688 / 0,655 ·
  Zugänglichkeit 0,588 / 0,569 · Nachnutzbarkeit 0,441 / 0,377 · Aussagekraft 0,651 / 0,571 ·
  **Ausnahme Auffindbarkeit 0,225 / 0,288**
- **Erklärung der Ausnahme** (Rückbezug auf Folie 8): Auffindbarkeit trägt das **niedrigste Dimensionsgewicht**
  (1,0 gegen 1,5–2,0) und prägt den Gesamtscore folglich am wenigsten. Der Gesamtscore ist damit *strukturell*
  ein schwächerer Prädiktor gerade für diese GT-Dimension – unabhängig von der Prüfgüte der
  Auffindbarkeitsindikatoren selbst, die mit ρ = 0,524 im Mittelfeld liegt
- Die Abstände auf der Kernstichprobe sind klein (0,02–0,08) – nicht überzeichnen, das Muster ist aber konsistent
- **Extremfälle:** alle 6 Zielgrößen vorn, Abstände +0,06 bis +0,14, auch bei der Auffindbarkeit (0,783 / 0,706).
  Plausibel, weil dort Feldpräsenz und tatsächliche Validität gezielt auseinanderlaufen
- **Starke Zusatzpointe, wenn Zeit ist:** Auf den Extremfällen ist die MQA in der reinen **Score-Spannweite**
  sogar leicht trennschärfer (0,44 vs. 0,38 Spreizung zwischen den Konstruktionsgruppen) – und korreliert
  trotzdem schlechter mit der Ground Truth. **Hohe Streuung allein garantiert keine korrekte Rangordnung**
- MQA-Vergleich auf den Extremfällen, falls gefragt: Konvergenz 95,6 %, Asymmetrie dort **vollständig einseitig
  (8 : 0)**, Überschätzung steigt auf 20,0 %, dominiert von der Lizenz (10 von 20 Datensätzen)

*Kürzen:* die vollständige Zahlenliste – Ausnahme + Erklärung reicht.

### 16 – Grenzfall: Aussagekraft auf den Extremfällen (90 s)
Selbstkritische Folie – bewusst offen damit umgehen, das wirkt souverän.
- **ρ = 0,321, nur 34,1 %** des Ceilings von 0,942 – der mit Abstand am wenigsten ausgeschöpfte Wert der
  gesamten Auswertung. Die Ceiling-Analyse schließt Skalen- und Stichprobenartefakte **explizit aus**:
  ein perfekt monotones Modell hätte hier 0,942 erreichen können
- **Symptom:** Die Modellwerte liegen in praktisch allen Fällen in einem schmalen Band zwischen **3,3 und 4,3**
  auf der 0–5-Skala – unabhängig davon, ob die Referenz bei 1 oder bei 4 liegt
- **Drei Ursachen auf drei verschiedenen Ebenen – nicht eine:**
  1. **Kriterienschnitt.** 2 der 6 Teilkriterien messen keine Inhaltsqualität, sondern eine *Beziehung zwischen
     Feldern*: Kohärenz Titel/Beschreibung und thematische Konsistenz. Sind alle Felder nichtssagend, sind sie
     untereinander vollkommen widerspruchsfrei – beide Kriterien vergeben **zu Recht** Punkte, aber das Gemessene
     ist kein Qualitätssignal mehr. Dahinter steckt eine implizite, nirgends kodierte Voraussetzung: dass die
     verglichenen Felder je einzeln informationshaltig sind
  2. **Aggregation.** Die 6 Teilkriterien gehen **ungewichtet** in den Dimensionswert ein → ein einzelnes hartes
     Defizit wird von fünf unauffälligen Werten praktisch neutralisiert (Beispiel auf Folie 17)
  3. **Der Maßstab selbst.** Die Extremfälle wurden nach fehlenden Feldern, ungültigen Vokabularangaben, toten
     Distributionslinks und unklaren Lizenzen ausgewählt – **Aussagekraft war ausdrücklich kein
     Selektionskriterium.** Bei der Referenzbewertung war die Konstruktionsabsicht aber bekannt, und die Annahme,
     dass die Textqualität mitläuft, liegt nahe, obwohl die Auswahl sie nicht stützt →
     **Erwartungsverzerrung nicht auszuschließen**
- **Zwei Beobachtungen stützen Ursache 3:** Der Wert bricht *nur* auf den konstruierten Extremfällen ein
  (Kernstichprobe: 0,569) und *nur* in der Dimension, die kein Selektionskriterium war – Auffindbarkeit und
  Nachnutzbarkeit erreichen auf derselben Stichprobe 90,3 % bzw. 91,0 % ihres Ceilings.
  Damit ist der Befund zugleich ein **Argument für das Stichprobendesign**
- Darüber hinaus eine Eigenschaft des Gegenstands: Aussagekraft ist von den vier Dimensionen die am schwersten
  zu bewertende. Bei Erreichbarkeit oder Lizenz liegt ein nachprüfbarer Sachverhalt vor, hier ein Urteil.
  **0,321 sagt deshalb auch etwas über die Reproduzierbarkeit des Maßstabs** – eine Inter-Rater-Reliabilität
  wäre an dieser Stelle die aussagekräftigste fehlende Kennzahl der ganzen Evaluation
- **Wichtig zur Einordnung:** Das ist eine Limitation der **Aggregationslogik**, nicht des Sprachmodellurteils –
  die einzelnen Teilkriterien differenzieren sichtbar (Klasse-C-Boxplot)
- Trotzdem trennt der Gesamtscore die Konstruktionsgruppen deutlich: **4,06 vs. 2,10** auf der 0–5-Skala –
  aber nicht *durch* die Aussagekraft, sondern *trotz* ihrer, weil die drei übrigen Dimensionen abfedern
- Beide Gegenmittel sind im Messmodell **schon angelegt** (→ Ausblick Folie 21): „nicht anwendbar“ für
  relationale Kriterien unterhalb einer Mindestinformationsschwelle, und eine nicht-kompensatorische Aggregation
  statt der flachen Mittelung

*Kürzen:* Ursache 3 und die Reproduzierbarkeits-Reflexion.

### 17 – Ein Beispiel: Justizblatt-Datensatz (60 s)
- Macht Folie 16 greifbar – `bad_09.rdf` aus den Extremfällen
- Die Beschreibung besteht aus dem einzigen Wort **„Justizblatt“**. Das Modell bewertet die
  Beschreibungsqualität mit **FAIL (0,15)** und begründet: erklärt weder Inhalt noch Struktur der Ressource
- Die übrigen **5 Teilkriterien liegen bei 0,65–0,95** → gemittelter Dimensionswert **0,72**
- Auf der 0–5-Skala: **GT = 1, Modell = 3,6**. Bei `good_02.rdf`: GT = 2, Modell = 3,8
- Bei **10 von 20** Extremfällen weicht das dreistufige Urteil deshalb ab (Genauigkeit 50 %) – immer derselbe Effekt
- **Pointe:** Ein hartes Defizit wird von fünf unauffälligen Werten überstimmt. Genau diesen Kompensationseffekt
  verhindert das Malus-Prinzip auf Indikatorebene – **innerhalb** der Aussagekraft gibt es ihn noch nicht
- Rückbezug auf Folie 2, wenn er passt: Dieser Datensatz ist SHACL-valide

---

## Schluss (≈5,5 Min)

### 18 – Antworten auf die Teilfragen (90 s)
- Als Rückbezug zu Folie 3 framen: „Damit zurück zu den eingangs gestellten Fragen…“
- Bei der Klick-Animation pro Zeile kurz pausieren, nicht alle fünf am Stück
- **TF1 – Übertragbarkeit:** schichtweise. Abstrakte Modelle liefern die begriffliche Rahmung, die
  Linked-Data-Perspektive einen operationalisierbaren Teil, die portalnahe MQA die unmittelbar anschlussfähige
  Prüflogik. **Entscheidend war nicht der Implementierungsaufwand, sondern die Prüfbarkeit aus dem Metadatensatz heraus**
- **TF2 – Dimensionen und Indikatoren:** vier Dimensionen aus 15 Kandidaten, 27 aktive Indikatoren (29 konzipiert,
  2 Kongruenzindikatoren nach Erprobung deaktiviert). 4 von 5 Interview-Anforderungen umgesetzt. Offen bleibt
  allein die nutzungsabhängige Vollständigkeit – **nicht aus Aufwandsgründen, sondern weil sie als absolute
  Eigenschaft eines Datensatzes nicht bestimmbar ist**
- **TF3 – semantische Erweiterung:** eine eigene sprachmodellgestützte Dimension. Nachvollziehbar, weil jedes
  Teilurteil begründet ausgegeben wird, und die Verlässlichkeit **gemessen statt vorausgesetzt** ist.
  Ehrlich dazu: Es ist zugleich die schwächste Dimension, und das überträgt sich auf die Messgüte insgesamt
- **TF4 – Konzeption und Operationalisierung:** vier Messmodell-Festlegungen tragen die Umsetzung – Trennung von
  Messung und präsentationaler Ergebnisstufe, Distributionsmittelung, Malus-Prinzip, „nicht anwendbar“.
  Prototypisch als durchgehende Kette von der Extraktion bis zur menschenlesbaren Ausgabe.
  **Die Evaluation weist nach, dass diese Festlegungen nicht nur begründet, sondern wirksam sind**
- **TF5 – Reporting:** einheitlicher Befund mit Handlungsanweisung über alle 27 Indikatoren, jedes negative
  Teilergebnis auf die betroffene Stelle im Metadatensatz zurückgeführt. **Die einzige Teilfrage ohne empirische
  Prüfung** – an Beispielen gezeigt, aber nicht mit Datenbereitstellenden erprobt

### 19 – Konzeptionelle Grenze (75 s)
- Die wichtigste Pointe der Schlussbetrachtung – dafür Zeit nehmen
- **Lübeck/Feinstaub:** derselbe Metadatensatz, in beiden Fällen standardkonform.
  Für eine einmalige Auswertung („an wie vielen Tagen 2023 wurde der Grenzwert überschritten?“) ist er
  **vollständig**. Für einen Dienst, der die Messreihe fortlaufend einbindet, fehlt mit
  `dct:accrualPeriodicity` genau die Angabe, die über das Abfrageintervall entscheidet →
  **gegensätzliches Vollständigkeitsurteil bei identischem Datensatz**
- Deshalb konnte auch in keinem Interview die Frage nach dem perfekten Metadatensatz beantwortet werden
- **Für Metadatenqualität existiert aus prinzipiellen Gründen keine belastbare externe Referenz** – nicht
  aus Aufwandsgründen. Ein Maßstab, der nutzungsunabhängig festlegt, was gute Qualität ist, widerspricht der
  Qualitätsdefinition, gegen die er prüfen soll
- **Konsequenz für die Interpretation:** ρ = 0,765 besagt, dass der Prototyp die Datensätze **so ordnet wie der
  erhobene Maßstab** – nicht, dass er sie richtig ordnet. Eine Referenzbewertung erhebt notwendigerweise *ein
  mögliches* Qualitätsurteil, nicht *das maßgebliche*
- Deshalb beschreiben die Ankerfragen die nutzerseitige Qualitätserfahrung: Sie **approximieren** einen typischen
  Nutzenden, ohne ihn zu ersetzen. Am stärksten trifft das die Aussagekraft, die doppelt belastet ist
- **Kein Sonderproblem dieser Arbeit:** Diese Grenze erklärt zugleich, warum bestehende Ansätze ihre Validität
  überwiegend gar nicht prüfen und warum es die perfekte Metrik für Metadatenqualität nicht geben kann
- Zweite konzeptuelle Grenze in einem Satz: Geprüft wird **Konsistenz, nicht fachliche Richtigkeit** – ein
  plausibel formulierter, sachlich falscher Bezugszeitraum besteht jede Prüfung
- Abschluss: Der Beitrag liegt daher nicht in der Absolutheit des Urteils, sondern in seiner Nachvollziehbarkeit
  und in einer **geprüften relativen Güte** gegenüber dem etablierten Verfahren

*Kürzen:* die zweite Grenze (fachliche Richtigkeit).

### 20 – Methodische & technische Grenzen (60 s)
- **Wichtigster Punkt zuerst:** Die Referenzbewertung stammt von einer einzigen Person, die zugleich das Modell
  entwickelt hat → **Inter-Rater-Reliabilität nicht bestimmbar**, Bestätigungsfehler nicht vollständig
  auszuschließen. „Unabhängig“ meint in dieser Arbeit ausschließlich die **methodische** Trennung – abweichende
  Anker und Blindheit gegenüber den Prototyp-Scores –, nicht personelle Unabhängigkeit
- Gewichte begründet, aber **nicht validiert**; Sensitivitätsanalyse fehlt
- Lineare additive Aggregation erlaubt **Kompensation zwischen Dimensionen**; der Malus schränkt sie gezielt ein,
  hebt sie aber nicht auf. Geometrische oder nicht-kompensatorische Alternativen wurden nicht geprüft.
  Die Kappung bei 0 kostet Auflösung im unteren Wertebereich
- Domänen- und Portalabhängigkeit: Indikatorauswahl ist auf DCAT-AP.de und GovData kalibriert; Bewertungsebene
  ist der Einzeldatensatz zu einem Zeitpunkt, eine Betrachtung über die Zeit ist ausgeschlossen
- **Technisch – Modellabhängigkeit:** Ein Modellwechsel oder eine unangekündigte Anbieter-Aktualisierung kann
  die Aussagekraftswerte verändern. Die Ergebnisse gelten für die **Kombination aus Modell und Promptfassung**,
  nicht für das Modell allein
- Nicht bitgenau reproduzierbar – die Streuung ist klein (σ 0,0046 je Datensatz, MAE 0,0059 zwischen zwei Läufen,
  ρ 0,993 zwischen Läufen), kann in dicht besetzten Wertebereichen aber die Rangfolge benachbarter Datensätze
  vertauschen. **Die drei deterministischen Dimensionen sind über alle Läufe bitgenau identisch** – das ist
  zugleich ein Validitätsnachweis für die Pipeline als Ganzes
- **Kosten:** ca. **1,79 USD je 50 Datensätze** → für den gesamten Katalog Größenordnung mehrerer Tausend USD.
  Die Laufzeit skaliert zudem nicht gleichmäßig, deshalb wurden sehr große Ressourcen vorab ausgeschlossen
- SHACL-Konformitätsprüfung hängt an einem externen Dienst ohne Überwachung; die Erreichbarkeitsprüfung ist
  netz- und zeitpunktabhängig – ein heute erhobener Wert muss morgen nicht mehr gelten
- **Abschlusssatz, der die Folie dreht:** Diese Grenzen betreffen die **Reichweite** der Aussagen, nicht die
  Tragfähigkeit des Verfahrens. Hervorzuheben ist, dass sie sich überhaupt benennen und in weiten Teilen
  beziffern lassen – **für keinen der untersuchten Ansätze liegt eine vergleichbare Angabe vor**

*Kürzen:* Domänenabhängigkeit und die externen Dienste.

### 21 – Beitrag, Ausblick, Praxis (90 s)
- **Beitrag = die Verbindung dreier Elemente, die in allen untersuchten Ansätzen getrennt auftreten:**
  (1) eine aus Literatur *und* Empirie hergeleitete, lückenlos rückführbare Indikatormenge,
  (2) ihre vollständige prototypische Operationalisierung,
  (3) eine Prüfung dieser Operationalisierung gegen ein menschliches Referenzurteil.
  Ergebnis: eine Metrik, **deren Übereinstimmung mit der wahrgenommenen Qualität beziffert und deren
  Messunsicherheit gemessen ist**
- **Drei über den Gegenstand hinaus verallgemeinerbare methodische Befunde** (gute Antwort auf „was ist hier
  eigentlich neu?“):
  1. Die Auswahl eines Sprachmodells setzt eine **Reproduzierbarkeitsprüfung** voraus – erst sie liefert die
     Auflösungsgrenze, unterhalb derer Unterschiede zwischen Kandidaten nicht mehr interpretierbar sind.
     Hier war der Abstand der beiden besten Modelle kleiner als die Streuung eines Modells zwischen zwei Läufen
  2. Die **Unsicherheit einer Messung muss kleiner bleiben als ihr Informationsbeitrag** – sonst verschlechtert
     der Indikator das Gesamturteil, statt es zu präzisieren (Beleg: die deaktivierten Kongruenzindikatoren)
  3. Ein Vergleich zweier Bewertungsverfahren **allein auf Gesamtscore-Ebene ist nicht aussagekräftig** –
     0,834 Korrelation bei gleichzeitig 15,8 % nachweisbarer Überschätzung
- **Ausblick, nach Dringlichkeit:**
  - Mehrfachbewertung durch unabhängige Personen – die aussagekräftigste Ergänzung der gesamten Evaluation,
    insbesondere für die Aussagekraft, deren schwache Messgüte ohne diese Kennzahl nicht eindeutig dem Modell
    oder dem Maßstab zugerechnet werden kann
  - „Nicht anwendbar“ für relationale Kriterien, solange die verglichenen Felder eine Mindestinformationsschwelle
    nicht überschreiten; flache Mittelung durch eine Aggregation ersetzen, die ein hartes Defizit nicht
    neutralisieren lässt
  - Unsicherheits- und Sensitivitätsanalyse der Gewichte
  - Nutzerstudie zu TF5: Verständlichkeit der Handlungsanweisungen und anschließende Korrekturquote
  - Erneuter Baseline-Vergleich gegen **MQA Metrics v2**, sobald veröffentlicht – v2 übernimmt mit der
    Distributionsmittelung und der vom Score entkoppelten SHACL-Konformität **zwei hier eigens begründete
    Entscheidungen**; eine semantische Dimension sieht auch v2 nicht vor, **die adressierte Bewertungslücke
    besteht also fort**
- **Praxis:**
  - **Formale Validierung als Vorstufe statt gleichrangiger Indikator:** Wer die Mindestanforderungen verfehlt,
    müsste erst korrigieren, bevor eine differenzierte Qualitätsaussage überhaupt sinnvoll ist.
    Ausdrücklich als Überlegung kennzeichnen – diese Anordnung wurde in der Arbeit nicht geprüft
  - Die Wirkung entsteht nicht über den Score, sondern über den **Weg zurück zur konkreten Stelle im
    Metadatensatz**. Eine Qualitätsmessung, deren Zustandekommen nicht rekonstruierbar ist, kann auf den
    Datenbestand nicht wirken – egal wie gut sie misst
  - Sprachmodelle nur dort, wo **kein deterministisch prüfbarer Sachverhalt** vorliegt, und nie dominierend in
    Dimensionen, in denen es ihn gibt. Wer sie produktiv einsetzt, muss laufende Kosten und Modellstabilität
    einplanen

*Kürzen:* die drei methodischen Befunde auf einen (Nr. 3) reduzieren.

### 22 – Vielen Dank (10 s)
- Kurz halten, dann Fragen

---

## Zahlen-Spickzettel

| Kennzahl | Wert |
|---|---|
| Katalogauszug GovData (15.05.2026) | 151.579 Datensätze |
| Nach NetCDF-Ausschluss | 149.786 (25.416 Geo / 124.370 Nicht-Geo) |
| Kernstichprobe / Extremfälle | n = 50 (stratifiziert, Seed 67) / n = 20 |
| Dimensionen / aktive Indikatoren | 4 / 27 (aus 15 Kandidatendimensionen, 29 konzipiert) |
| ρ Prototyp ↔ Ground Truth (Kern) | **0,765** |
| ρ je Dimension (Kern) | Auffindbark. 0,524 · Zugängl. 0,712 · Nachnutzb. 0,739 · Aussagekr. 0,569 |
| Ceiling-Ausschöpfung (Kern) | 68,3 % · 74,8 % · 79,6 % · 66,8 % |
| Accuracy / κ_gew. / PABAK / AUC | 92 % · 0,635 · 0,88 · 0,907 |
| MAE / Bias (0–5-Skala) | 0,289 / +0,018 |
| ρ Prototyp ↔ MQA (Kern / Extrem) | 0,834 / 0,818 |
| Klasse-A-Konvergenz (Kern / Extrem) | 96,0 % (17:1 asymmetrisch) / 95,6 % (8:0) |
| Klasse-B-Überschätzung (Kern / Extrem) | 15,8 % (71/450) / 20,0 % (36/180) |
| Stärkster B-Einzelbefund | Politische Geokodierung: 28 von 50 (56 %) |
| Triangulation H3 | 5/6 (Kern) · 6/6 (Extrem) |
| Aussagekraft Extremfälle | ρ = 0,321 = 34,1 % des Ceilings (0,942) |
| Justizblatt (`bad_09.rdf`) | Beschreibung 0,15 · übrige 5 bei 0,65–0,95 · Dimension 0,72 · GT 1 vs. Modell 3,6 |
| Trennschärfe Extremfälle (0–5) | gut 4,06 vs. schlecht 2,10 |
| Deckenprüfung Referenzdatensatz | 27/27 Indikatoren, Gesamtscore 0,991 (Aussagekraft 0,972) |
| Reproduzierbarkeit GPT-5.5 | σ 0,0046 je Datensatz · MAE 0,0059 · ρ 0,993 zwischen Läufen |
| Kosten | 1,79 USD je 50 Datensätze |
| Dimensionsgewichte | Zugängl. 2,0 · Aussagekr. 2,0 · Nachnutzb. 1,5 · Auffindbark. 1,0 |
| Angehobene Indikatoren | Z5/Z6/N1 = 2,0 · Z7 = 1,5 · Malus = −0,5 |

---

## Erwartbare Fragen – Kurzantworten

**„Warum GPT-5.5 und nicht Opus 4.8 oder Sonnet 4.6?“**
Kandidaten nach dem OpenRouter-Ranking für Klassifikationsaufgaben. Erster Befund: Die drei deterministischen
Dimensionen sind über alle drei Modelle **bitgenau identisch** (0,524 / 0,712 / 0,739) – die Modellwahl berührt
ausschließlich die Aussagekraft. Opus 4.8 scheidet am Aufwand aus (4,10 vs. 1,79 USD, ohne belastbaren Vorsprung).
GPT-5.5 und Sonnet 4.6 trennt die Primärmetrik nicht (Abstand 0,028–0,029 bei σ = 0,023, Wertebereiche überlappen).
Entschieden haben die nachgeordneten Kriterien: **Sonnet unterschätzt die Aussagekraft systematisch um 0,723
Skalenpunkte** (~15 % der Skalenbreite), GPT-5.5 nur um 0,077. Dadurch drückt Sonnet 19 von 50 Datensätzen unter
die Sperrklausel „keine Dimension unter 3“ (GT: 7) und erkennt nur **1 von 5** wirklich guten Datensätzen als gut,
GPT-5.5 dagegen 3. Dazu stabiler (max. 17 % Statuswechsel je Kriterium vs. 47 %) und das günstigste Modell.

**„Warum ρ und nicht Cohens κ?“**
Die Frage ist ordinal; der kontinuierliche Score ist das eigentliche Ergebnis, das dreistufige Urteil nur eine
Diskretisierung. Dazu liegen 88 % der GT-Urteile in *mittel*, die Zufallsübereinstimmung also schon bei ~0,79
(Kappa-Paradox), und das Bootstrap-KI für κ reicht von 0,18 bis 0,92. κ wird deshalb nur ergänzend berichtet.
Eine feinere Skala hilft nicht: Je feiner, desto mehr nähert sich quadratisch gewichtetes κ einer Korrelation an –
es misst am Ende dasselbe wie ρ, nur zusätzlich abhängig von Stufenzahl und Schwellenlage.

**„Warum keine Agentenkette, wie in der Zielsetzung skizziert?“**
Bewusste Entscheidung zugunsten der Nachvollziehbarkeit (Teilfrage 3 verlangt sie ausdrücklich): mehrstufige
Verarbeitung bedeutet Fehlerfortpflanzung zwischen den Schritten, und das Zustandekommen des Urteils wäre nicht
mehr an einer Stelle nachlesbar. Dazu Kosten und höhere Konsistenz aus einer ganzheitlichen Betrachtung.

**„Ist die MQA-Reimplementierung fair?“**
Nach offizieller Methodik implementiert, gegen die veröffentlichten data.europa.eu-Berichte validiert,
unterspezifizierte Stellen (Mehrfachdistributionen) aus dem öffentlichen Quellcode nachvollzogen, Skalen
normalisiert. Die Gegenrichtung ist explizit ausgewiesen: 4 MQA-Metriken ohne Prototyp-Pendant = 25 von 405 Punkten,
alle vier nach DCAT-AP.de weder verpflichtend noch empfohlen.

**„Warum nicht gegen Metrics v2?“**
Zum Bearbeitungszeitpunkt weder stabile Spezifikation noch betriebene Instanz, gegen die sich auf identischer
Datengrundlage vergleichen ließe. Bemerkenswert: v2 übernimmt zwei hier eigens begründete Entscheidungen
(Distributionsmittelung, vom Score entkoppelte SHACL-Konformität) – eine semantische Dimension sieht auch v2 nicht vor.

**„n = 50 ist wenig.“**
Die Ground Truth wurde manuell je Dimension und Datensatz erhoben; die Schichtung sichert Abdeckung statt Masse
(10 Straten, sonst dominieren die wenigen aufkommensstärksten Portale). Die Extremfälle ergänzen den
Wirkmechanismus per Konstruktion, tragen aber bewusst keine quantitativen Aussagen. Die Unsicherheit ist
ausgewiesen (Bootstrap-KI, Ceiling-Analyse) statt weggelassen.

**„Misst das Verfahren nicht einfach zu streng?“**
Die Deckenprüfung am Referenzdatensatz beantwortet genau das: 27/27 Indikatoren, 0,991 Gesamtscore, die drei
deterministischen Dimensionen exakt 1,000, kein Malus greift. Wo die Stichproben niedriger liegen, ist das ein
Befund über die Metadaten.

**„Halluzinationen / Prompt Injection?“**
Aufgabenschnitt erfordert kein Weltwissen (nur Passung der Felder untereinander), strukturierte Ausgabe mit
Befund-vor-Zahl-Reihenfolge, deterministisch abgeleitete Ergebnisstufe, Temperatur 0. Metadateninhalt ist durch
Trennmarken abgegrenzt und ausdrücklich als reiner Bewertungsgegenstand deklariert, den das Modell nie als
Anweisung behandeln darf. Vollständig ausgeräumt ist das Risiko damit nicht – das sage ich auch so in der Arbeit.

---

## Hinweise

- Folie 9 ist im Foliensatz ausgeblendet – die Nummerierung springt von 8 auf 10, das ist kein Fehler.
- Die beiden Backup-Folien (23 Quellen & Grundlagen, 24 Scoring-Logik) sind nicht eingerechnet – nur zeigen,
  wenn gezielt danach gefragt wird. Backup 24 ist die schnellste Antwort auf jede Gewichtungs- oder
  Aggregationsfrage.
- Durchgängige Benennungen: Dimension heißt **Nachnutzbarkeit** (nicht Wiederverwendbarkeit), Modell **GPT-5.5**,
  Baseline **MQA v1** (nicht Metrics v2).
- Drei Sätze, die sich lohnen, wörtlich zu können:
  1. „SHACL sagt, ob das Feld da ist – nicht, ob ich damit etwas anfangen kann.“
  2. „ρ = 0,765 heißt: Der Prototyp ordnet so wie der gewählte Maßstab – nicht, dass er richtig ordnet.“
  3. „Ein Vergleich zweier Bewertungsverfahren allein auf Gesamtscore-Ebene ist nicht aussagekräftig:
     0,834 Korrelation bei 15,8 % nachweisbarer Überschätzung.“
