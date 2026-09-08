# Quellenverzeichnis mit Fundstellen

Automatisch erzeugt aus `thesis/bib/report.bib` und den `.tex`-Quellen (`contents.tex`, `report.tex`, `appendix/*.tex`).

## Wie diese Datei zu lesen ist

Die Datei hat zwei Sichten auf dieselben Daten:

- **B. Durchgang in Textreihenfolge** — alle Zitatstellen so, wie sie im Text stehen. Für den linearen Prüfdurchgang.
- **C. Quellen im Detail** — nach Quelle gruppiert. Beantwortet die andere Frage: trägt eine Quelle wirklich alle Aussagen, die ihr zugeschrieben werden?

Zu jeder Stelle stehen:

- **Fundstelle** — Datei und Zeilennummer, dazu der Gliederungspfad bis zur Unterüberschrift
- **Aussage** — der Satz aus der Thesis, der die Zitation trägt. Das ist die Behauptung, die die Quelle belegen soll. In der Longlist der Kandidatendimensionen (Tabelle~C.1, `longlist_kandidatendimensionen.tex`) trägt jede Zeile mehrere Quellen, die jeweils für einen bestimmten Ausdruck stehen; dort steht deshalb pro Quelle nur der isolierte Ausdruck, der genau in dieser Quelle nachzuweisen ist, statt der ganzen Zeile.
- **`- [ ]`** — Obsidian-Task; beim Durchgehen direkt abhakbar
- **Link** — `DOI` und `Web` führen direkt zur Quelle. `Suche` heißt, dass in der `.bib` weder DOI noch URL steht; der Link ist dann nur eine Google-Scholar-Suche nach dem Titel und **kein Nachweis**.

In den Sätzen sind `\ref{…}` als `[label]` und Zitationen als `[@key]` dargestellt, sonstiges LaTeX-Markup ist entfernt.

> **Wichtige Einschränkung.** Diese Datei sagt, *was die Thesis an der jeweiligen Stelle behauptet* — nicht, ob die Quelle das tatsächlich hergibt. Genau das ist beim Prüfen die eigentliche Arbeit. Seitenangaben lassen sich nicht ausgeben, weil die Zitationen im Dokument bis auf eine Ausnahme keine Locator tragen (siehe Abschnitt „Auffälligkeiten“).

## Kennzahlen

| | |
|---|---|
| Einträge in `report.bib` | 61 |
| davon zitiert | 59 |
| davon nie zitiert | 2 |
| Zitatstellen (`\cite`-Befehle) | 201 |
| Quellenverweise gesamt | 280 |
| Quellen mit nur einer Fundstelle | 27 |

## A. Übersicht

Alphabetisch nach BibTeX-Key. „Kapitel“ nennt jedes Kapitel, in dem die Quelle vorkommt.

| Key | Kurzbeleg | Jahr | Link | Stellen | Kapitel |
|---|---|---|---|---:|---|
| `Basili1994GQM` | Basili et al. | 1994 | [Suche](https://scholar.google.com/scholar?q=The+Goal+Question+Metric+Approach) | 1 | Kap. 4 |
| `BernersLee2006LinkedData` | Berners-Lee | 2006 | [Web](https://www.w3.org/DesignIssues/LinkedData.html) | 2 | Kap. 3, Anhang |
| `BleiholderNaumann2008` | Bleiholder & Naumann | 2008 | [DOI](https://doi.org/10.1145/1456650.1456651) | 2 | Kap. 4 |
| `BmdsOpenData` | Bundesministerium für Digitales und S… | 2026 | [Web](https://bmds.bund.de/themen/digitale-wirtschaft/daten/open-data) | 1 | Kap. 2 |
| `bydata2025handreichung` | oc.bydata -- open bydata competence c… | 2025 | [Web](https://open.bydata.de/) | 5 | Kap. 4, Kap. 5 |
| `byrt1993bias` | Byrt et al. | 1993 | [DOI](https://doi.org/10.1016/0895-4356(93)90018-V) | 1 | Kap. 6 |
| `campbell1959convergent` | Campbell & Fiske | 1959 | [DOI](https://doi.org/10.1037/h0046016) | 2 | Kap. 6 |
| `corteslasalle_shacl_dqa` | Lasalle et al. | 2025 | [DOI](https://doi.org/10.48550/arXiv.2507.22305) | 1 | Kap. 3 |
| `cronbach1955construct` | Cronbach & Meehl | 1955 | [DOI](https://doi.org/10.1037/h0040957) | 1 | Kap. 6 |
| `data_europa` | data.europa.eu | 2026 | [Web](https://data.europa.eu/mqa/methodology?locale=en) | 22 | Kap. 2, Kap. 3, Kap. 4, Kap. 5, Kap. 6, Anhang |
| `dataeuropa_dqguidelines` | data.europa.eu | 2024 | [Web](https://op.europa.eu/webpub/op/data-quality-guidelines/en/) | 1 | Kap. 5 |
| `DCATAPDEImplRules2` | DCAT-AP.de | 2022 | [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/) | 8 | Kap. 2, Kap. 3, Kap. 4, Kap. 5 |
| `DCATAPDESpec2` | DCAT-AP.de | 2022 | [Web](https://www.dcat-ap.de/def/dcatde/2.0/spec/) | 4 | Kap. 2, Kap. 3, Kap. 5 |
| `DCATAPDESpec3` | DCAT-AP.de | 2024 | [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/) | 7 | Kap. 2, Kap. 3, Kap. 4, Kap. 5 |
| `DCATAPDEStart` | DCAT-AP.de | — | [Web](https://www.dcat-ap.de/) | 2 | Kap. 2 |
| `DresingPehl2018` | Dresing & Pehl | 2018 | [Web](https://www.audiotranskription.de/wp-content/uploads/2020/11/Praxisbuch_08_01_web.pdf) | 1 | Kap. 3 |
| `einhorn1971` | Einhorn | 1971 | [DOI](https://doi.org/10.1016/0030-5073(71)90002-X) | 1 | Kap. 6 |
| `feinstein1990kappa` | Feinstein & Cicchetti | 1990 | [DOI](https://doi.org/10.1016/0895-4356(90)90158-L) | 1 | Kap. 6 |
| `few2006dashboard` | Few | 2006 | [Suche](https://scholar.google.com/scholar?q=Information+Dashboard+Design%3A+The+Effective+Visual+Communication+of+Data) | 1 | Kap. 5 |
| `FitkoGovdata` | FITKO | 2026 | [Web](https://www.fitko.de/produktmanagement/govdata) | 7 | Kap. 1, Kap. 2 |
| `FITKOGovDataDocs` | FITKO | — | [Web](https://docs.fitko.de/resources/govdata/) | 1 | Kap. 2 |
| `Gayo2015LinkedDataValidationQuality` | Jose Emilio Labra Gayo | 2015 | [Web](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) | 4 | Kap. 2, Kap. 3 |
| `glaser1963` | Glaser | 1963 | [DOI](https://doi.org/10.1037/h0049294) | 1 | Kap. 6 |
| `govdata_portal` | FITKO | 2024 | [Web](https://www.govdata.de/) | 2 | Kap. 1, Kap. 5 |
| `ISO19157` | International Organization for Standa… | 2023 | [Web](https://www.iso.org/standard/78900.html) | 2 | Kap. 3, Anhang |
| `iso25012` | International Organization for Standa… | 2008 | [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model) | 11 | Kap. 2, Kap. 3, Kap. 4, Anhang |
| `iso25024` | International Organization for Standa… | 2015 | [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25024%3A2015+Systems+and+Software+Engineering+--+Systems+and+Software+Quality+Requirements+and+Evaluation+%28SQuaRE%29+--+Measurement+of+Data+Quality) | 1 | Kap. 4 |
| `Ji2023HallucinationSurvey` | Ji et al. | 2023 | [DOI](https://doi.org/10.1145/3571730) | 1 | Kap. 3 |
| `kubler2018comparison` | Kubler et al. | 2018 | [DOI](https://doi.org/10.1016/j.giq.2017.11.003) | 5 | Kap. 2, Kap. 3, Kap. 5 |
| `lnenicka2023` | Lnenicka et al. | 2024 | [DOI](https://doi.org/10.1016/j.giq.2023.101898) | 1 | Kap. 1 |
| `machado2009cvd` | Machado et al. | 2009 | [DOI](https://doi.org/10.1109/TVCG.2009.113) | 1 | Kap. 5 |
| `Mayring2014` | Mayring | 2014 | [Web](https://www.ssoar.info/ssoar/handle/document/39517) | 1 | Kap. 3 |
| `Mayring2015` | Mayring | 2015 | [Suche](https://scholar.google.com/scholar?q=Qualitative+Inhaltsanalyse%3A+Grundlagen+und+Techniken) | 1 | Kap. 3 |
| `nardo2008handbook` | Nardo et al. | 2008 | [DOI](https://doi.org/10.1787/9789264043466-en) | 2 | Kap. 5, Kap. 7 |
| `Neumaier2016MetadataQuality` | Neumaier et al. | 2016 | [DOI](https://doi.org/10.1145/2964909) | 20 | Kap. 2, Kap. 3, Kap. 4, Anhang |
| `noguerasiso_quality_metadata` | Nogueras-Iso et al. | 2021 | [DOI](https://doi.org/10.1109/ACCESS.2021.3073455) | 13 | Kap. 2, Kap. 3, Anhang |
| `OECD2020OURdata` | OECD | 2020 | [DOI](https://doi.org/10.1787/45f6de2d-en) | 4 | Kap. 2, Kap. 3, Kap. 5 |
| `openrouter_rankings_classification` | OpenRouter | 2026 | [Web](https://openrouter.ai/rankings#task-spend) | 1 | Kap. 6 |
| `piveauMetricsScore` | Piveau | — | [Web](https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt) | 2 | Kap. 4, Kap. 6 |
| `piveauMetricsV2` | piveau | 2026 | [Web](https://doc.piveau.eu/metrics/v2/scoring/) | 3 | Kap. 2, Kap. 6, Kap. 7 |
| `preston2000optimal` | Preston & Colman | 2000 | [DOI](https://doi.org/10.1016/S0001-6918(99)00050-5) | 1 | Kap. 6 |
| `Riley2017MetadataPrimer` | Riley | 2017 | [Web](https://www.niso.org/publications/understanding-metadata-2017) | 3 | Kap. 2 |
| `shneiderman1996eyes` | Shneiderman | 1996 | [DOI](https://doi.org/10.1109/VL.1996.545307) | 1 | Kap. 5 |
| `StrongLeeWang1997` | Strong et al. | 1997 | [Suche](https://scholar.google.com/scholar?q=Data+quality+in+context) | 5 | Kap. 2, Kap. 3, Anhang |
| `Ubaldi2013OGD` | Ubaldi | 2013 | [DOI](https://doi.org/10.1787/5k46bj4f03s7-en) | 5 | Kap. 2, Kap. 3, Kap. 5 |
| `w3c_css_validator` | World Wide Web Consortium | 2026 | [Web](https://jigsaw.w3.org/css-validator/) | 1 | Kap. 5 |
| `w3c_nu_checker` | World Wide Web Consortium | 2026 | [Web](https://validator.w3.org/nu/) | 1 | Kap. 5 |
| `w3c_sparql11_query` | World Wide Web Consortium | 2013 | [Web](https://www.w3.org/TR/sparql11-query/) | 1 | Kap. 2 |
| `w3c_wcag22` | World Wide Web Consortium | 2023 | [Web](https://www.w3.org/TR/WCAG22/) | 1 | Kap. 5 |
| `W3CDCAT3` | World Wide Web Consortium | 2024 | [Web](https://www.w3.org/TR/vocab-dcat-3/) | 6 | Kap. 2, Kap. 3, Kap. 4, Anhang |
| `W3CDQV` | Albertoni & Isaac | 2016 | [Web](https://www.w3.org/TR/vocab-dqv/) | 1 | Kap. 3 |
| `W3CRDF11Concepts` | World Wide Web Consortium | 2014 | [Web](https://www.w3.org/TR/rdf11-concepts/) | 5 | Kap. 2, Kap. 3, Anhang |
| `W3CSHACL` | World Wide Web Consortium | 2017 | [Web](https://www.w3.org/TR/shacl/) | 4 | Kap. 2, Kap. 3, Anhang |
| `wand1996anchoring` | Wand & Wang | 1996 | [Suche](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations) | 6 | Kap. 2, Kap. 3, Anhang |
| `wang1996beyond` | Wang & Strong | 1996 | [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers) | 21 | Kap. 2, Kap. 3, Kap. 4, Kap. 5, Anhang |
| `wentzel2023extensive` | Wentzel et al. | 2023 | [DOI](https://doi.org/10.1007/978-3-031-41138-0_17) | 22 | Kap. 2, Kap. 3, Kap. 4, Anhang |
| `wilkinson2016fair` | Wilkinson & others | 2016 | [DOI](https://doi.org/10.1038/sdata.2016.18) | 21 | Kap. 2, Kap. 3, Kap. 4, Anhang |
| `Zaveri2016LinkedDataQuality` | Zaveri et al. | 2016 | [DOI](https://doi.org/10.3233/SW-150175) | 26 | Kap. 2, Kap. 3, Kap. 4, Anhang |
| `Zheng2023LLMJudge` | Zheng et al. | 2023 | [Suche](https://scholar.google.com/scholar?q=Judging+LLM-as-a-Judge+with+MT-Bench+and+Chatbot+Arena) | 1 | Kap. 3 |

## B. Durchgang in Textreihenfolge

Alle Zitatstellen in der Reihenfolge, in der sie im Text vorkommen, gruppiert nach Kapitel und Abschnitt. Für einen linearen Prüfdurchgang: Arbeit und Liste nebeneinander, von oben nach unten.

Ein `\cite` mit mehreren Quellen steht hier **einmal** mit allen beteiligten Quellen — an solchen Stellen ist zu prüfen, ob jede von ihnen die Aussage trägt.

### Kap. 1 — Einleitung

**Problemstellung und Motivation**

- [ ] `contents.tex:5` — [`lnenicka2023`](https://doi.org/10.1016/j.giq.2023.101898)  
  > Offene Daten können dabei neue wirtschaftliche und gesellschaftliche Mehrwerte schaffen, indem sie Forschung, datenbasierte Anwendungen und evidenzbasierte Entscheidungsprozesse unterstützen [@lnenicka2023].

- [ ] `contents.tex:7` — [`govdata_portal`](https://www.govdata.de/), [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata)  
  > GovData fungiert als übergreifender Metadatenkatalog, über den Bund, Länder und Kommunen ihre offenen Datensätze auffindbar machen und einen zentralen Zugang zu Verwaltungsdaten bereitstellen [@govdata_portal, FitkoGovdata].

### Kap. 2 — Theoretische und konzeptionelle Grundlagen

**Open Government Data und das GovData-Portal**

- [ ] `contents.tex:90` — [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en), [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en)  
  > OGD ist damit mehr als die bloße Veröffentlichung staatlicher Informationen im Internet; gemeint ist die proaktive Bereitstellung wiederverwendbarer Datenbestände des öffentlichen Sektors. [@Ubaldi2013OGD, OECD2020OURdata]

- [ ] `contents.tex:92` — [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en), [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en)  
  > Ihre Relevanz ergibt sich damit aus der Verbindung von politischer Offenheit, technischer Nachnutzbarkeit, und gesellschaftlicher Wertschöpfung. [@Ubaldi2013OGD, OECD2020OURdata]

- [ ] `contents.tex:94` — [`BmdsOpenData`](https://bmds.bund.de/themen/digitale-wirtschaft/daten/open-data)  
  > GovData übernimmt damit vor allem eine Aggregations- und Sichtbarkeitsfunktion, indem verteilte Datenbestände über einen gemeinsamen Metadatenzugang auffindbar gemacht werden. [@BmdsOpenData]

- [ ] `contents.tex:97` — [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata)  
  > Die FITKO ordnet das Portal ihrem einheitlichen Produktmanagement-Modell für Produkte des IT-Planungsrats zu und verweist für GovData auf ein eigenes föderal besetztes Produktboard [@FitkoGovdata].

**Metadaten im Open-Data-Kontext**

- [ ] `contents.tex:101` — [`Riley2017MetadataPrimer`](https://www.niso.org/publications/understanding-metadata-2017)  
  > Für Datensätze im Open-Data-Kontext bedeutet dies, dass Metadaten nicht bloß Begleitinformationen sind, sondern die Beschreibungsschicht, über die Datensätze gefunden, eingeordnet, und verwendet werden können. [@Riley2017MetadataPrimer]

- [ ] `contents.tex:120` · _Unterschrift_ — [`Riley2017MetadataPrimer`](https://www.niso.org/publications/understanding-metadata-2017)  
  > Markup-Metadaten & Kennzeichnen die logische oder semantische Struktur innerhalb eines digitalen Objekts. justification=centering Metadatentypen in Anlehnung an NISO, eigene Übersetzung und Paraphrase [@Riley2017MetadataPrimer]

- [ ] `contents.tex:125` — [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/)  
  > DCAT ist hierfür das zentrale W3C-Vokabular, das die interoperable Beschreibung von Datenkatalogen, Datensätzen, und Datendiensten im Web ermöglichen soll. [@W3CDCAT3]

- [ ] `contents.tex:127` — [`Riley2017MetadataPrimer`](https://www.niso.org/publications/understanding-metadata-2017), [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata)  
  > In funktionaler Hinsicht lassen sich die im GovData-Kontext verwendeten Metadaten vor allem als deskriptive und administrative Metadaten einordnen, da sie einerseits der Beschreibung und Auffindbarkeit von Verwaltungsdaten dienen und andererseits Informationen zur Bereitstellung, zu Formaten, zu offenen Lizenzen, und zur Nachnutzbarkeit enthalten [@Riley2017MetadataPrimer,FitkoGovdata].

- [ ] `contents.tex:128` — [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata)  
  > Da GovData selbst als nationales Metadatenportal fungiert, einen Metadatenkatalog bereitstellt, und die beschriebenen Verwaltungsdaten weiterhin dezentral bei den bereitstellenden Stellen verbleiben, kommt dieser Beschreibungsschicht eine zentrale infrastrukturelle Funktion zu [@FitkoGovdata].

**DCAT-AP.de als Metadatenstandard**

- [ ] `contents.tex:132` — [`DCATAPDEStart`](https://www.dcat-ap.de/)  
  > DCAT-AP.de ist das gemeinsame deutsche Metadatenmodell für den Austausch offener Verwaltungsdaten und dient dazu, Metadaten aus unterschiedlichen Portalen in einer einheitlichen Struktur bereitzustellen [@DCATAPDEStart].

- [ ] `contents.tex:132` — [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/)  
  > Sein Zweck liegt insbesondere darin, Metadaten offener Verwaltungsdaten zwischen deutschen Open-Data-Portalen interoperabel auszutauschen und diese Daten über GovData zentral auffindbar zu machen [@DCATAPDESpec3,DCATAPDESpec2].

- [ ] `contents.tex:134` — [`DCATAPDEStart`](https://www.dcat-ap.de/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > Damit steht der Standard in einem mehrstufigen Interoperabilitätszusammenhang: vom allgemeinen Modell für Datenkataloge im Web über das europäische Anwendungsprofil bis hin zur deutschen Spezifikation für offene Verwaltungsdaten [@DCATAPDEStart,DCATAPDESpec3].

- [ ] `contents.tex:134` — [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata)  
  > Diese Einbettung ist insbesondere deshalb relevant, weil Metadaten im GovData-Kontext nicht nur innerhalb Deutschlands ausgetauscht, sondern zugleich an europäische Entwicklungen anschlussfähig bleiben sollen [@FitkoGovdata].

- [ ] `contents.tex:136` — [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata), [`FITKOGovDataDocs`](https://docs.fitko.de/resources/govdata/)  
  > Die Qualität und Standardkonformität der Metadaten ist damit eine zentrale Voraussetzung dafür, dass Datensätze portalübergreifend auffindbar, maschinell verarbeitbar und interoperabel nachnutzbar werden [@FitkoGovdata, FITKOGovDataDocs].

- [ ] `contents.tex:138` — [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Der Standard legt fest, welche Informationen in welcher Form beschrieben werden sollen, und schafft so die Grundlage für einheitliche semantische Beschreibungen, föderierte Suche, und die Weiterverarbeitung von Metadaten über Schnittstellen und Portale hinweg [@DCATAPDESpec3,DCATAPDEImplRules2].

**RDF, Linked Data und SHACL**

- [ ] `contents.tex:214` — [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/)  
  > RDF ist damit nicht primär als konkretes Dateiformat zu verstehen, sondern als abstraktes Datenmodell, auf dem unterschiedliche RDF-basierte Sprachen und Serialisierungen aufbauen. [@W3CRDF11Concepts]

- [ ] `contents.tex:219` — [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`w3c_sparql11_query`](https://www.w3.org/TR/sparql11-query/)  
  > SPARQL ist die standardisierte Abfragesprache für RDF-Daten und ermöglicht es, RDF-Graphen beziehungsweise RDF-Datenbestände über Graphmuster zu durchsuchen und auszuwerten [@W3CRDF11Concepts,w3c_sparql11_query].

- [ ] `contents.tex:222` — [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/)  
  > Es soll die Interoperabilität zwischen im Web veröffentlichten Datenkatalogen erleichtern, die Aggregation von Metadaten aus mehreren Katalogen unterstützen, die Auffindbarkeit von Datensätzen erhöhen, und föderierte Suche über verschiedene Kataloge hinweg ermöglichen. [@W3CDCAT3]

- [ ] `contents.tex:227` — [`W3CSHACL`](https://www.w3.org/TR/shacl/)  
  > SHACL ermöglicht somit die formale Überprüfung, ob ein RDF-Datenbestand vorgegebene strukturelle und syntaktische Anforderungen erfüllt. [@W3CSHACL]

- [ ] `contents.tex:230` — [`W3CSHACL`](https://www.w3.org/TR/shacl/)  
  > SHACL dient der Prüfung von RDF-Graphen gegen formal definierte Constraints und erlaubt damit insbesondere Aussagen über strukturelle und syntaktische Konformität [@W3CSHACL].

- [ ] `contents.tex:231` — [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > In der Literatur zu Linked Data und Metadatenqualität wird Validierung zwar als zentraler Bestandteil der Qualitätsprüfung betrachtet, zugleich aber betont, dass darüber hinaus weitere Qualitätsdimensionen wie Vollständigkeit, Auffindbarkeit, Genauigkeit, oder Nachnutzbarkeit relevant sind [@Gayo2015LinkedDataValidationQuality,Neumaier2016MetadataQuality,Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:233` — [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata)  
  > Dies gilt insbesondere im GovData-Kontext, in dem Metadaten nicht nur formal korrekt, sondern auch für die zentrale Auffindbarkeit und Nachnutzung dezentral bereitgestellter Verwaltungsdaten geeignet sein müssen [@FitkoGovdata].

**Datenqualität › Definition nach Wang and Strong 1996**

- [ ] `contents.tex:243` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Einen zentralen Referenzpunkt bildet die Arbeit von Wang und Strong, die Datenqualität als fitness for use definieren und damit die Perspektive der Datennutzenden in den Mittelpunkt stellen [@wang1996beyond].

- [ ] `contents.tex:243` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Ausgehend von einer empirischen Untersuchung von Datenkonsumentinnen und -konsumenten entwickeln sie ein hierarchisches Rahmenmodell, in dem Datenqualitätsmerkmale nicht allein aus theoretischen Vorannahmen oder aus Sicht von Systementwickelnden abgeleitet werden, sondern aus den Anforderungen tatsächlicher Nutzungssituationen hervorgehen [@wang1996beyond].

- [ ] `contents.tex:245` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Wang und Strong unterscheiden vier übergeordnete Kategorien von Datenqualität: intrinsische, kontextuelle, repräsentationale, und zugangsbezogene Qualität [@wang1996beyond].

- [ ] `contents.tex:254` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Vielmehr hängt sie davon ab, ob Daten in einem bestimmten Arbeits- oder Entscheidungskontext brauchbar sind [@wang1996beyond].

- [ ] `contents.tex:254` — [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context)  
  > Diese Perspektive wurde von Strong, Lee, und Wang weiter ausgebaut, die betonen, dass Datenqualitätsprobleme nicht nur in gespeicherten Daten selbst entstehen, sondern im weiteren Kontext von Informationssystemen, also auch in Produktions-, Speicher-, und Nutzungskontexten [@StrongLeeWang1997].

- [ ] `contents.tex:256` — [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > Ergänzend zu diesem nutzungsbezogenen Rahmen schlagen Wand und Wang eine ontologische Fundierung von Datenqualität vor [@wand1996anchoring].

- [ ] `contents.tex:256` — [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > Datenqualitätsprobleme lassen sich dann als Repräsentationsdefizite zwischen der beobachtbaren realen Welt und ihrer Abbildung im Informationssystem beschreiben [@wand1996anchoring].

**Datenqualität › Qualitätsmodell der ISO-Norm 25012**

- [ ] `contents.tex:264` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Datenqualitätsmerkmale werden den Perspektiven inhärenter und systemabhänger Qualität zugeordnet. [@iso25012]

**Datenqualität › FAIR-Prinzipien**

- [ ] `contents.tex:286` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Eine weitere zentrale Referenz bilden die FAIR-Prinzipien von Wilkinson et al. [@wilkinson2016fair].

- [ ] `contents.tex:288` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Wilkinson et al. betonen, dass die Prinzipien nicht nur die Nachnutzung durch menschliche Forschende unterstützen sollen, sondern ausdrücklich auch die Fähigkeit von Maschinen verbessern, Daten automatisch zu finden und zu nutzen [@wilkinson2016fair].

- [ ] `contents.tex:299` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Ihre Umsetzung kann daher inkrementell erfolgen und hängt vom jeweiligen Datenbestand, Fachkontext, und technischen Ökosystem ab.[@wilkinson2016fair]

- [ ] `contents.tex:336` · _Unterschrift_ — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > R1.3 & (Meta-)Daten erfüllen domänenspezifische Community-Standards. justification=centering FAIR-Prinzipien nach Wilkinson et al. [@wilkinson2016fair]

**Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al.**

- [ ] `contents.tex:349` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Einen zentralen Referenzpunkt für die systematische Einordnung von Metadatenqualität im Semantic-Web- und Linked-Data-Kontext bildet die Arbeit von Zaveri et al. [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:349` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Grundlage ist eine systematische Literaturauswertung, in der 118 potenziell relevante Arbeiten identifiziert, 73 Arbeiten näher geprüft, und schließlich 30 Kernansätze sowie 12 Werkzeuge zur Linked-Data-Qualitätsbewertung vergleichend analysiert werden [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:351` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Linked Data kann formal korrekt publiziert sein und zugleich unvollständig, inkonsistent, veraltet, schwer interpretierbar, oder unzureichend mit anderen Datenquellen verknüpft sein [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:353` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Zaveri et al. strukturieren diese Anforderungen in einem umfassenden Qualitätsrahmen mit insgesamt 18 Dimensionen und 69 Metriken [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:356` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Dies betrifft insbesondere Metriken der Vertrauenswürdigkeit, etwa die Einschätzung eines Datenanbieters oder einer Datenquelle [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:379` · _Unterschrift_ — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > [h!] 1.3 1whitewhite |p3.5cm|p9.3cm| Kategorie & Unterdimensionen Zugänglichkeit & Verfügbarkeit, Lizenzierung, Interlinking, Sicherheit, Performanz Intrinsische Qualität & Syntaktische Validität, Semantische Genauigkeit, Konsistenz, Prägnanz, Vollständigkeit Kontextuelle Qualität & Relevanz, Vertrauenswürdigkeit, Verständlichkeit, Aktualität Repräsentationale Qualität & Repräsentationsprägnanz, Interoperabilität, Vielseitigkeit, Interpretierbarkeit justification=centering Qualitätskategorien und Unterdimensionen für Linked Data nach Zaveri et al.; die zugehörigen 69 Einzelmetriken werden hier nicht im Detail wiedergegeben [@Zaveri2016LinkedDataQuality]

- [ ] `contents.tex:383` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Bewertet werden können dabei unterschiedliche Ebenen von Linked Data, insbesondere einzelne RDF-Tripel, RDF-Graphen, Entitäten, oder ganze Datensätze [@Zaveri2016LinkedDataQuality].

**Metadatenqualität und Qualitätsbewertung von Linked Data › Automatisierte Metadatenbewertung in Open-Data-Portalen nach Neumaier et al.**

- [ ] `contents.tex:388` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > In ihrer Arbeit entwickeln sie einen automatisierten Ansatz zur Bewertung von Metadatenqualität über unterschiedliche Datenportale hinweg [@Neumaier2016MetadataQuality].

- [ ] `contents.tex:395` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Drittens definieren die Autoren konkrete Qualitätsmetriken auf Basis zentraler DCAT-Eigenschaften, die automatisiert, skalierbar, und effizient berechnet werden können [@Neumaier2016MetadataQuality].

- [ ] `contents.tex:494` · _Unterschrift_ — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > justification=centering Qualitätsdimensionen auf DCAT-Schlüsseln nach Neumaier et al. [@Neumaier2016MetadataQuality]

**Metadatenqualität und Qualitätsbewertung von Linked Data › Gewichtung und Ranking von Open-Data-Portalen nach Kubler et al.**

- [ ] `contents.tex:504` — [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003)  
  > Kubler et al. beschreiben die Bewertung von Open-Data-Portalen als Multi-Criteria Decision Making Problem und entwickeln mit dem Open Data Portal Quality Framework einen Ansatz, der automatisiert berechnete Qualitätsindikatoren mit nutzerspezifischen Präferenzen verbindet [@kubler2018comparison].

- [ ] `contents.tex:513` — [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003)  
  > Die Rangordnung der Portale ergibt sich anschließend aus der Kombination der verfügbaren Qualitätswerte mit den gesetzten Präferenzen. [@kubler2018comparison]

**Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau**

- [ ] `contents.tex:623` · _Unterschrift_ — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > MQA-Qualitätsmetriken und Gewichtungen nach Wentzel et al. [@data_europa, wentzel2023extensive]

- [ ] `contents.tex:631` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Dadurch operationalisiert MQA/Piveau Metadatenqualität primär über praktische Nutzbarkeit, technische Zugänglichkeit, strukturelle Interoperabilität und rechtliche Wiederverwendbarkeit. [@data_europa, wentzel2023extensive] Während der Bearbeitung dieser Arbeit wurde eine überarbeitete Fassung des Frameworks (Metrics v2) angekündigt und dokumentiert, jedoch noch nicht veröffentlicht [@piveauMetricsV2].

- [ ] `contents.tex:631` — [`piveauMetricsV2`](https://doc.piveau.eu/metrics/v2/scoring/)  
  > Dadurch operationalisiert MQA/Piveau Metadatenqualität primär über praktische Nutzbarkeit, technische Zugänglichkeit, strukturelle Interoperabilität und rechtliche Wiederverwendbarkeit. [@data_europa, wentzel2023extensive] Während der Bearbeitung dieser Arbeit wurde eine überarbeitete Fassung des Frameworks (Metrics v2) angekündigt und dokumentiert, jedoch noch nicht veröffentlicht [@piveauMetricsV2].

- [ ] `contents.tex:633` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Einzelne Messergebnisse werden als dqv:QualityMeasurement modelliert, während SHACL-basierte Validierungsergebnisse zur DCAT-AP-Konformität als Qualitätsannotation eingebunden werden können. [@wentzel2023extensive] Beide Modellierungsformen sind in Tabelle [tab:piveau_dqv_model] dargestellt. [h!] 1.2 1whitewhite

- [ ] `contents.tex:677` · _Unterschrift_ — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > [t]0.46 Quality Measurement ll DQV Quality Measurement rdf:type dqv:QualityMeasurement dqv:isMeasurementOf dqv:value dqv:computedOn prov:generatedAtTime [t]0.46 Quality Annotation ll DQV Quality Annotation rdf:type dqv:QualityAnnotation oa:hasBody dqv:inDimension oa:motivatedBy dc:isVersionOf oa:hasTarget prov:generatedAtTime Modellierung von Quality Measurements und Quality Annotations nach Wentzel et al. [@wentzel2023extensive]

**Metadatenqualität und Qualitätsbewertung von Linked Data › ISO 19157 als Qualitätsinstrument**

- [ ] `contents.tex:687` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Diese Struktur erlaubt es, verschiedene Fehlerarten präziser voneinander zu unterscheiden und Qualitätsmessungen nicht nur als einfache Punktwerte, sondern als methodisch nachvollziehbare Prüfergebnisse zu modellieren. [@noguerasiso_quality_metadata]

- [ ] `contents.tex:693` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Dadurch entsteht eine zweistufige Bewertungslogik, die Rohmessung, Prüfverfahren und Qualitätsurteil voneinander trennt. [@noguerasiso_quality_metadata]

**Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken**

- [ ] `contents.tex:704` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Die abstrakten Qualitätskonzepte von Wang und Strong, ISO/IEC 25012 und FAIR liefern die begriffliche Rahmung und begründen Qualität als mehrdimensionales, nutzungsabhängiges Konzept, legen aber nicht fest, welche Metadatenelemente, Vokabulare oder Zugriffspfade konkret zu prüfen sind [@wang1996beyond, iso25012, wilkinson2016fair].

- [ ] `contents.tex:708` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Die stärker auf RDF und Metadaten ausgerichteten Modelle von Zaveri et al. und Nogueras-Iso et al. machen Qualitätsaspekte jenseits der formalen Validität sichtbar, setzen für viele ihrer Prüfungen jedoch Kontextwissen, externe Referenzdaten oder manuelle Bewertungen voraus und sind damit nur begrenzt skalierbar [@Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata].

- [ ] `contents.tex:713` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Die portalnahen Ansätze von Neumaier et al. und die MQA sind dem Anwendungskontext am nächsten und automatisiert prüfbar, konzentrieren sich dafür aber auf leicht messbare, überwiegend formale und feldbezogene Kriterien und bilden weitergehende semantische Aspekte nur eingeschränkt ab [@Neumaier2016MetadataQuality, wentzel2023extensive].

**Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken › Bewertungslücke im DCAT-AP.de- und GovData-Kontext**

- [ ] `contents.tex:730` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Die portalnahen Ansätze sind zwar operationalisiert, begründen die Auswahl und Gewichtung ihrer Metriken jedoch nicht empirisch [@data_europa].

### Kap. 3 — Experteninterviews

**Experteninterviews: Ziel, Auswahl und Durchführung**

- [ ] `contents.tex:750` — [`DresingPehl2018`](https://www.audiotranskription.de/wp-content/uploads/2020/11/Praxisbuch_08_01_web.pdf)  
  > Die Transkription orientierte sich an einem inhaltlich-semantischen Transkriptionsverständnis nach Dresing und Pehl [@DresingPehl2018].

**Auswertungsverfahren der Interviews**

- [ ] `contents.tex:779` — [`Mayring2014`](https://www.ssoar.info/ssoar/handle/document/39517), [`Mayring2015`](https://scholar.google.com/scholar?q=Qualitative+Inhaltsanalyse%3A+Grundlagen+und+Techniken)  
  > Die Auswertung der Experteninterviews erfolgte mithilfe einer qualitativen Inhaltsanalyse in Anlehnung an Mayring [@Mayring2014, Mayring2015].

- [ ] `contents.tex:808` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > K1 & Qualitäts- verständnis und ideale Metadaten & Forschungsfrage zur Entwicklung eines praxisrelevanten Bewertungsmodells; Leitfadenblock „perfekte Metadaten“; Datenqualitätsverständnis nach [@wang1996beyond]. & Ableitung übergeordneter Anforderungen an ein gutes DCAT-AP.de-Metadatenmodell.

- [ ] `contents.tex:810` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > K2 & Vollständigkeit, Reichhaltigkeit und Feldrelevanz & Leitfadenfrage zu Qualitätsmerkmalen; Literatur zu Vollständigkeit nach [@wentzel2023extensive, wilkinson2016fair, DCATAPDESpec2, DCATAPDESpec3]. & Bestimmung, welche Metadatenfelder für einen Score geprüft und wie Pflicht-, empfohlene und optionale Angaben gewichtet werden.

- [ ] `contents.tex:812` — [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CSHACL`](https://www.w3.org/TR/shacl/), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf)  
  > K3 & Formale und syntaktische Qualität & Forschungsfrage zur Integration von RDF-/SHACL-Prüfungen; Literatur zu Conformance, syntaktischer Validität und DCAT-AP.de-Konformität nach [@W3CRDF11Concepts, W3CSHACL, DCATAPDESpec2, DCATAPDESpec3, DCATAPDEImplRules2, Gayo2015LinkedDataValidationQuality]. & Erfassung regelbasierter, automatisierbarer Fehler über SHACL, XML/RDF, URI-, Vokabular- und Datentypprüfungen.

- [ ] `contents.tex:814` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > K4 & Semantische und inhaltliche Qualität & Forschungsfrage zu KI-gestützten Analyseverfahren; Literatur zu Verständlichkeit, Accuracy, semantischer Konsistenz und Qualität von Freitextfeldern nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata]. & Ergänzung formaler Prüfungen um Aussagekraft, Verständlichkeit, Plausibilität und inhaltliche Passung.

- [ ] `contents.tex:816` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > K5 & Technische Zugänglichkeit, Aktualität und Nutzbarkeit & Literatur zu Accessibility, Retrievability, Open Data Fitness und MQA/Piveau nach [@wilkinson2016fair, data_europa, Neumaier2016MetadataQuality, kubler2018comparison, wentzel2023extensive]. & Bewertung, ob Ressourcen erreichbar, technisch nutzbar, aktuell genug und praktisch weiterverarbeitbar sind.

- [ ] `contents.tex:818` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf)  
  > K6 & Interoperabilität und Linked-Data-Qualität & Literatur zu FAIR, Linked Data, RDF-Grundlagen, DCAT und Linked-Data-Qualität nach [@wilkinson2016fair, W3CRDF11Concepts, W3CDCAT3, Zaveri2016LinkedDataQuality, Gayo2015LinkedDataValidationQuality]. & Bewertung, ob Metadaten über URIs, Normdaten, kontrollierte Vokabulare und Graphbezüge interoperabel und verknüpfbar sind.

- [ ] `contents.tex:820` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en)  
  > K7 & Kontextsensitivität und Fit for Purpose & Forschungsfrage zur praxisrelevanten Bewertung; Literatur zu Fit for Purpose, Kontextualität, FAIR-Nachnutzung und domänenspezifischer Datenqualität nach [@wang1996beyond, StrongLeeWang1997, wand1996anchoring, wilkinson2016fair, Ubaldi2013OGD]. & Anpassung von Bewertung, Gewichtung und Interpretation an Nutzungskontext, Domäne und Stakeholderperspektive.

- [ ] `contents.tex:822` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > K8 & Rohdatenbezug und Metadaten-Daten-Kongruenz & Forschungsfrage zur Kombination formaler Validierung mit kontextbezogenen Prüfverfahren; Leitfadenblock „Relevanz des eigentlichen Datensatzes“; Literatur zu Accuracy und Daten-Metadaten-Konsistenz nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, noguerasiso_quality_metadata]. & Prüfung, ob Metadaten mit der tatsächlichen Ressource übereinstimmen und ob Rohdaten zur Plausibilisierung herangezogen werden können.

- [ ] `contents.tex:824` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`W3CDQV`](https://www.w3.org/TR/vocab-dqv/), [`ISO19157`](https://www.iso.org/standard/78900.html)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

- [ ] `contents.tex:826` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`corteslasalle_shacl_dqa`](https://doi.org/10.48550/arXiv.2507.22305), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`BernersLee2006LinkedData`](https://www.w3.org/DesignIssues/LinkedData.html)  
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.

**Zentrale Ergebnisse der Interviews › Zusammenfassung der empirischen Modellanforderungen**

- [ ] `contents.tex:1030` — [`Ji2023HallucinationSurvey`](https://doi.org/10.1145/3571730)  
  > Generative KI kann halluzinieren [@Ji2023HallucinationSurvey] und neigt selbst bei identischer Eingabe zu schwer reproduzierbaren Urteilen [@Zheng2023LLMJudge], weshalb KI-gestützte Verfahren die Bewertung nur ergänzen und im Reporting gekennzeichnet sein sollen, während die Scoringlogik regelbasiert, dokumentiert und nachvollziehbar bleibt.

- [ ] `contents.tex:1030` — [`Zheng2023LLMJudge`](https://scholar.google.com/scholar?q=Judging+LLM-as-a-Judge+with+MT-Bench+and+Chatbot+Arena)  
  > Generative KI kann halluzinieren [@Ji2023HallucinationSurvey] und neigt selbst bei identischer Eingabe zu schwer reproduzierbaren Urteilen [@Zheng2023LLMJudge], weshalb KI-gestützte Verfahren die Bewertung nur ergänzen und im Reporting gekennzeichnet sein sollen, während die Scoringlogik regelbasiert, dokumentiert und nachvollziehbar bleibt.

**Zielgruppen des Bewertungsmodells**

- [ ] `contents.tex:1045` — [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en), [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en)  
  > Diese Dreiteilung folgt der in Kapitel 2 eingeführten Definition offener Daten, die Bereitstellung und Nachnutzung als zwei Seiten desselben Vorgangs begreift [@Ubaldi2013OGD, OECD2020OURdata], und deckt sich mit der Auswahl der Interviewpartner, die sowohl die Perspektive des GovData-Produktmanagements und der Standardisierung als auch die der praktischen Datenbereitstellung abdecken (Abschnitt [sec:interviews_ziel_auswahl]).

### Kap. 4 — Konzeption eines Metadatenqualitätsmodells

**Ableitung relevanter Qualitätsdimensionen**

- [ ] `contents.tex:1104` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Auch Wang und Strong (1996) ordneten ihre empirisch ermittelten Qualitätsdimensionen in der abschließenden Verdichtungsstufe ihrer Studie nicht nach deren Herkunft, sondern anhand eines zuvor entwickelten konzeptionellen Rahmens vier übergeordneten Kategorien zu [@wang1996beyond].

**Ableitung formaler, technischer und semantischer Einzelindikatoren**

- [ ] `contents.tex:1202` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Dieses Vorgehen ist anschlussfähig an die MQA, die die DCAT-AP-Konformität ebenfalls als eine Metrik innerhalb ihres Dimensionsmodells führt [@data_europa, wentzel2023extensive].

- [ ] `contents.tex:1206` — [`Basili1994GQM`](https://scholar.google.com/scholar?q=The+Goal+Question+Metric+Approach)  
  > Die Auswahl der Indikatoren orientiert sich, am Goal-Question-Metric-Prinzip, nachdem Metriken top-down aus übergeordneten Zielen abgeleitet werden [@Basili1994GQM].

**Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Ternäre und graduelle Indikatoren**

- [ ] `contents.tex:1240` — [`iso25024`](https://scholar.google.com/scholar?q=ISO%2FIEC+25024%3A2015+Systems+and+Software+Engineering+--+Systems+and+Software+Quality+Requirements+and+Evaluation+%28SQuaRE%29+--+Measurement+of+Data+Quality), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Die Norm ergänzt die Qualitätscharakteristiken aus ISO/IEC 25012 um konkrete Messfunktionen [@iso25024, iso25012].

- [ ] `contents.tex:1240` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Die zweite Klasse umfasst semantische Urteile, die naturgemäß keine scharfe Erfüllungsgrenze besitzen, beispielsweise die Aussagekraft einer Beschreibung; für solche originär subjektiven Qualitätsurteile ist eine kontinuierliche Skala methodisch etabliert, wie sie bereits Wang und Strong zur Erhebung von Wichtigkeitsurteilen mittels neunstufiger Skala einsetzten [@wang1996beyond].

**Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Bewertungsebene und Aggregation über Distributionen**

- [ ] `contents.tex:1246` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`piveauMetricsScore`](https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt)  
  > Bei mehreren Distributionen bestimmt die am besten bewertete Distribution das Ergebnis, unter der Annahme, dass alle Distributionen denselben Datensatz lediglich in unterschiedlichen Formaten repräsentieren [@data_europa, piveauMetricsScore].

- [ ] `contents.tex:1247` · Locator: `Abschnitt~12.3` — [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/)  
  > Erst mit DCAT 3 wurde für diesen Fall die eigene Klasse dcat:DatasetSeries eingeführt [@W3CDCAT3].

- [ ] `contents.tex:1247` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Empirische Untersuchungen von Open-Data-Portalen verorten zentrale Fehlerbilder wie nicht abrufbare Ressourcen entsprechend auf der Ebene der einzelnen Ressource, weshalb Neumaier et al. die Abrufbarkeit je Ressource und nicht je Datensatz prüfen [@Neumaier2016MetadataQuality].

- [ ] `contents.tex:1248` — [`BleiholderNaumann2008`](https://doi.org/10.1145/1456650.1456651)  
  > In der Terminologie der Datenintegration entspricht das Best-Distribution-Prinzip damit einer conflict-avoiding-Strategie, die einen bevorzugten Wert auswählt und übrige Werte unberücksichtigt lässt und dadurch Inkonsistenzen maskiert, statt sie sichtbar zu machen [@BleiholderNaumann2008].

- [ ] `contents.tex:1248` — [`BleiholderNaumann2008`](https://doi.org/10.1145/1456650.1456651)  
  > Da das Ziel dieser Arbeit gerade die Aufdeckung und Meldung fehlerhafter Distributionen ist (Abschnitt [subsec:befund]), wählt das Bewertungsmodell stattdessen bewusst eine conflict-resolving-Strategie in Form der Mittelwertbildung [@BleiholderNaumann2008].

**Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Malus-Prinzip**

- [ ] `contents.tex:1252` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Eine unklare Lizenz macht die Nachnutzung rechtlich unsicher, was die Nachnutzbarkeit stark verkompliziert [@Neumaier2016MetadataQuality].

**Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren**

- [ ] `contents.tex:1271` · _Tabelle_ — [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1273` · _Tabelle_ — [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1275` · _Tabelle_ — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1277` · _Tabelle_ — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1279` · _Tabelle_ — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1281` · _Tabelle_ — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1283` · _Tabelle_ — [`bydata2025handreichung`](https://open.bydata.de/)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

**Ableitung formaler, technischer und semantischer Einzelindikatoren › Aussagekraftsindikatoren**

- [ ] `contents.tex:1390` — [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/), [`bydata2025handreichung`](https://open.bydata.de/)  
  > Erstens werden die Bewertungskriterien nicht frei definiert, sondern aus den Qualitätsanforderungen des DCAT-AP.de-Konventionenhandbuchs sowie der Handreichung zur Verbesserung der Metadatenqualität von offenen Daten abgeleitet [@DCATAPDEImplRules2, bydata2025handreichung].

### Kap. 5 — Prototypische Operationalisierung

**Extraktion und Anreicherung der Metadaten**

- [ ] `contents.tex:1516` — [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Dazu gehören die Vokabulare des Publications Office der Europäischen Union für Themen, Dateitypen und Aktualisierungsfrequenzen https://op.europa.eu/en/web/eu-vocabularies/authority-tables, das Medientypregister der IANA https://www.iana.org/assignments/media-types/ sowie die Lizenzliste, die IDs der Datenbereitsteller und das Schlüsselverzeichnis der politischen Geokodierung aus DCAT-AP.de [@DCATAPDEImplRules2].

**Implementierung der Einzelindikatoren › Auffindbarkeitsindikatoren**

- [ ] `contents.tex:1680` — [`bydata2025handreichung`](https://open.bydata.de/)  
  > Die Schlagwortspanne von 3 bis 15 ist direkt aus der Handreichung zur Verbesserung der Metadatenqualität des open bydata competence center übernommen, die für einen Datensatz mindestens drei relevante Schlagwörter empfiehlt und je nach Dateninhalt maximal 15 Begriffe als ausreichend ansieht [@bydata2025handreichung].

- [ ] `contents.tex:1680` — [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Die dedizierte Eigenschaft dcatde:politicalGeocodingURI ist gemäß Konvention 08 des DCAT-AP.de-Konventionenhandbuchs der vorgesehene Weg, den verwaltungspolitischen Geobezug als URI aus dem zugehörigen kontrollierten Vokabular auszudrücken [@DCATAPDEImplRules2].

**Implementierung der Einzelindikatoren › Zugänglichkeitsindikatoren**

- [ ] `contents.tex:1739` — [`dataeuropa_dqguidelines`](https://op.europa.eu/webpub/op/data-quality-guidelines/en/)  
  > Die Stufenzuordnung von Z7 (maschinenlesbarer Zugriffsweg) orientiert sich an der Klassifikation maschinenlesbarer Dateitypen der Data Quality Guidelines von data.europa.eu [@dataeuropa_dqguidelines].

**Implementierung der Einzelindikatoren › Nachnutzbarkeitsindikatoren**

- [ ] `contents.tex:1773` — [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Diese Version bildet ein vollständig abgeschlossenes Profil, das neben der Spezifikation auch ein zugehöriges Konventionenhandbuch bereitstellt [@DCATAPDESpec2, DCATAPDEImplRules2] und damit die Grundlage des in Kapitel 4 abgeleiteten Bewertungsmodells bildet.

- [ ] `contents.tex:1773` — [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > Die im Dezember 2024 veröffentlichte Version 3.0 wird bewusst nicht verwendet, da für sie kein geschlossenes Konventionenhandbuch mehr vorgesehen ist; die Konventionen werden stattdessen in die Spezifikation überführt, in Guidelines umgewandelt oder gestrichen, wobei entsprechende Guidelines bislang nicht vorliegen [@DCATAPDESpec3].

**LLM-gestützte Bewertung der Aussagekraft › Eingabe und Prompt**

- [ ] `contents.tex:1843` — [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/), [`bydata2025handreichung`](https://open.bydata.de/)  
  > Sie enthält die schrittweise Vorgehensweise je Kriterium, die aus dem DCAT-AP.de-Konventionenhandbuch v2.0 (Kapitel 1.7 und 3.4) sowie der Handreichung zur Verbesserung der Metadatenqualität abgeleiteten Bewertungsregeln [@DCATAPDEImplRules2, bydata2025handreichung] und eine Ankerskala, die Wertebereiche verbal an Qualitätsniveaus bindet.

**Scoring-, Gewichtungs- und Aggregationslogik**

- [ ] `contents.tex:1871` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Wie in Sektion [sec:wang_strong_definition_quality] erläutert, ist Datenqualität kein eindimensionales Konstrukt, sondern setzt sich aus mehreren, getrennt zu messenden Dimensionen zusammen [@wang1996beyond].

**Scoring-, Gewichtungs- und Aggregationslogik › Punktevergabe je Indikator**

- [ ] `contents.tex:1877` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Tabelle [tab:mqa_metrics_weights]) [@data_europa].

- [ ] `contents.tex:1877` — [`nardo2008handbook`](https://doi.org/10.1787/9789264043466-en)  
  > Die Literatur zu zusammengesetzten Indikatoren behandelt die Gewichts- und Punktwahl entsprechend als transparent zu dokumentierende Entwurfsentscheidung, die sich auf Experten- und Konstrukteursurteile stützt [@nardo2008handbook].

- [ ] `contents.tex:1877` — [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003)  
  > Kubler et al. zeigen mit ihrem AHP-basierten Ansatz zudem, dass Qualitätsgewichte grundsätzlich präferenzabhängig sind und je nach Stakeholderperspektive unterschiedlich ausfallen [@kubler2018comparison].

**Scoring-, Gewichtungs- und Aggregationslogik › Gewichtung der Indikatoren und Dimensionen**

- [ ] `contents.tex:1932` — [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en), [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en)  
  > Bereitstellung ohne Zugangsbeschränkungen unter Bedingungen, die die Wiederverwendung erlauben [@Ubaldi2013OGD, OECD2020OURdata].

- [ ] `contents.tex:1932` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Tabelle [tab:mqa_metrics_weights]) [@data_europa].

- [ ] `contents.tex:1934` — [`bydata2025handreichung`](https://open.bydata.de/)  
  > Sind Titel, Beschreibung und Schlagwörter nichtssagend, bleibt der Datensatz für Nutzende unverständlich, auch wenn die Metadaten vollständig sind, worauf auch die Handreichung zur Verbesserung der Metadatenqualität ihren Schwerpunkt legt [@bydata2025handreichung].

**Menschenlesbares Qualitätsreporting › Einbettung in eine Portalumgebung**

- [ ] `contents.tex:2107` — [`govdata_portal`](https://www.govdata.de/)  
  > Um dies zeigen zu können, ohne Zugriff auf ein produktiv betriebenes Portal zu haben, bildet der Prototyp die Oberfläche des GovData-Portals nach [@govdata_portal] und übernimmt dessen Gestaltungssystem und Seitenaufbau.

**Menschenlesbares Qualitätsreporting › Vom Prüfergebnis zum Befund**

- [ ] `contents.tex:2140` — [`w3c_nu_checker`](https://validator.w3.org/nu/), [`w3c_css_validator`](https://jigsaw.w3.org/css-validator/)  
  > Die Auflistung der nicht bestandenen Prüfungen mit Fundstelle und, wo möglich, Quelltextbeleg orientiert sich damit an der Form, die die Konformitätsprüfdienste des W3C für Markup und Stylesheets etabliert haben [@w3c_nu_checker, w3c_css_validator]:

**Menschenlesbares Qualitätsreporting › Darstellung und Bedienung**

- [ ] `contents.tex:2206` — [`shneiderman1996eyes`](https://doi.org/10.1109/VL.1996.545307)  
  > Sie folgen dem Ordnungsprinzip Überblick zuerst, dann Filtern, dann Details auf Anforderung, das Shneiderman als Grundmuster informationsvisualisierender Oberflächen beschreibt [@shneiderman1996eyes]:

- [ ] `contents.tex:2218` — [`few2006dashboard`](https://scholar.google.com/scholar?q=Information+Dashboard+Design%3A+The+Effective+Visual+Communication+of+Data)  
  > Die Zusammenstellung folgt dem für Übersichtsdarstellungen formulierten Grundsatz, die zur Beurteilung erforderlichen Größen gemeinsam und nach ihrem Informationswert geordnet zu zeigen, statt sie auf mehrere Ansichten zu verteilen [@few2006dashboard].

- [ ] `contents.tex:2232` — [`w3c_wcag22`](https://www.w3.org/TR/WCAG22/)  
  > Für die Gestaltung gelten durchgängig zwei Regeln der Barrierefreiheit, die den Web Content Accessibility Guidelines entnommen sind [@w3c_wcag22].

- [ ] `contents.tex:2232` — [`machado2009cvd`](https://doi.org/10.1109/TVCG.2009.113)  
  > Ergänzend wurden die Diagrammfarben mit einem physiologisch begründeten Simulationsmodell für Farbfehlsichtigkeit [@machado2009cvd] auf ihre Unterscheidbarkeit geprüft.

### Kap. 6 — Evaluation

**Evaluationsdesign und Hypothesen**

- [ ] `contents.tex:2262` — [`campbell1959convergent`](https://doi.org/10.1037/h0046016)  
  > Methodisch entspricht dies dem Nachweis konvergenter Validität [@campbell1959convergent].

**Ground-Truth-Erhebung**

- [ ] `contents.tex:2319` — [`preston2000optimal`](https://doi.org/10.1016/S0001-6918(99)00050-5)  
  > Die Stufenzahl folgt dem Befund von Preston und Colman [@preston2000optimal], wonach Reliabilität, Validität und Diskriminierungsfähigkeit von Ratingskalen auf etwa fünf bis sieben Stufen zunehmen und vierstufige Skalen suboptimal sind.

- [ ] `contents.tex:2364` — [`campbell1959convergent`](https://doi.org/10.1037/h0046016)  
  > Damit misst die Ground Truth dasselbe Konstrukt aus methodisch unabhängiger Perspektive, statt die Prüflogik des Prototyps manuell nachzuvollziehen [@campbell1959convergent].

- [ ] `contents.tex:2393` — [`glaser1963`](https://doi.org/10.1037/h0049294)  
  > Die Schwellen in Tabelle [tab:gt_gesamturteil] legen inhaltlich fest, was ein gutes, mittleres oder schlechtes Ergebnis trennt, unabhängig davon, wie sich die konkrete Stichprobe zufällig verteilt und orientieren sich an der kriteriumsorientierten Messung nach Glaser [@glaser1963].

- [ ] `contents.tex:2404` — [`einhorn1971`](https://doi.org/10.1016/0030-5073(71)90002-X)  
  > Diese Kombination stellt sicher, dass ein gravierender Mangel in nur einer Dimension, etwa eine unklare Lizenz bei ansonsten guten Metadaten, nicht einfach im Durchschnitt der übrigen drei Dimensionen verschwindet [@einhorn1971].

**Vergleichsbaseline: MQA-Reimplementierung und A/B/C-Klassifikation**

- [ ] `contents.tex:2422` — [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Um beide Verfahren auf exakt derselben Datengrundlage vergleichen zu können, wurde die MQA-Bewertungslogik nach der offiziellen Methodik [@data_europa] reimplementiert und gegen die veröffentlichten Berichte von data.europa.eu validiert.

- [ ] `contents.tex:2426` — [`piveauMetricsScore`](https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt)  
  > Wo die Methodik die Berechnung nicht abschließend festlegt, insbesondere bei der Behandlung mehrerer Distributionen, wurde die Logik ergänzend aus dem öffentlichen Quellcode des MQA-Scoring-Dienstes nachvollzogen [@piveauMetricsScore].

- [ ] `contents.tex:2439` — [`piveauMetricsV2`](https://doc.piveau.eu/metrics/v2/scoring/)  
  > Bemerkenswert ist, dass Metrics v2 zwei Konstruktionsentscheidungen dieses Modells nachträglich teilt, die hier gegenüber der MQA v1 eigens begründet wurden: die Mittelung über die Distributionen eines Datensatzes anstelle des Best-Distribution-Prinzips (Abschnitt [sec:messmodell]) und die Entkopplung der SHACL-Konformität vom eigentlichen Score, die hier als einzelner aggregierter Indikator geführt wird [@piveauMetricsV2].

- [ ] `contents.tex:2462` — [`cronbach1955construct`](https://doi.org/10.1037/h0040957)  
  > Diese Partitionierung entspricht klassischen Validitätsbegriffen der Messtheorie [@cronbach1955construct]:

**Auswertungsverfahren und Kennzahlen**

- [ ] `contents.tex:2497` — [`feinstein1990kappa`](https://doi.org/10.1016/0895-4356(90)90158-L)  
  > Das ist ein bekanntes Phänomen, das als Kappa-Paradox beschrieben ist [@feinstein1990kappa].

- [ ] `contents.tex:2532` — [`byrt1993bias`](https://doi.org/10.1016/0895-4356(93)90018-V)  
  > PABAK (Prevalence-Adjusted Bias-Adjusted Kappa) korrigiert zusätzlich um die Verzerrung durch die ungleiche Urteilsverteilung selbst [@byrt1993bias] und macht dadurch sichtbar, dass die niedrige -Punktschätzung hier ein Verteilungs- und kein Qualitätsbefund ist.

**Modellauswahl für die LLM-gestützte Bewertung**

- [ ] `contents.tex:2662` — [`openrouter_rankings_classification`](https://openrouter.ai/rankings#task-spend)  
  > Die Plattform weist aus, welche Modelle je Aufgabentyp den größten Anteil der abgerechneten Nutzung auf sich vereinen, und die drei genannten Modelle führen dort die Kategorie der Klassifikationsaufgaben an [@openrouter_rankings_classification].

### Kap. 7 — Schlussbetrachtung

**Ergebnisdiskussion und Reflexion › Methodische Grenzen**

- [ ] `contents.tex:3643` — [`nardo2008handbook`](https://doi.org/10.1787/9789264043466-en)  
  > Dass auch etablierte Verfahren ihre Punktwerte per Konvention festlegen und die Literatur zu zusammengesetzten Indikatoren dies als dokumentationspflichtige Entwurfsentscheidung behandelt [@nardo2008handbook], entlastet die Setzung, hebt sie aber nicht auf.

**Ausblick › Weiterer Forschungs- und Entwicklungsbedarf**

- [ ] `contents.tex:3749` — [`piveauMetricsV2`](https://doc.piveau.eu/metrics/v2/scoring/)  
  > Schließlich legt die während der Bearbeitung angekündigte Fassung Metrics v2 einen erneuten Baseline-Vergleich nahe, sobald sie veröffentlicht und produktiv verfügbar ist [@piveauMetricsV2].

### Anhang — (ohne Kapitel)

**(Kapiteleinleitung)**

- [ ] `appendix/iso19157_qualitaetselemente.tex:187` · _Unterschrift_ — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Kombinierte Übersicht der ISO-19157-Qualitätselemente, Scopes, Measures und Evaluationsarten nach Nogueras-Iso et al. [@noguerasiso_quality_metadata]

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „Conformance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „DCAT-AP conformity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „syntactic validity, consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — [`W3CSHACL`](https://www.w3.org/TR/shacl/)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „SHACL-Constraints für Kardinalitäten, Datentypen, Klassen, Properties und Wertebereiche“

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „conformity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „Completeness, appropriate amount of data, value-added“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „completeness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „FAIR F2, R1“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „schema completeness, property completeness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „Existence“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „feldbezogene MQA-Metriken“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „completeness omission“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „FAIR F1--F4“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „Findability: keywords, categories, spatial search, temporal search“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „Discovery: dct:title, dct:description, dcat:keyword“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „DCAT-Identifikatoren und Katalogmodell“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „relevance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „FAIR A1, A1.1, A2“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „availability, dereferenceability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „Access, AccessURL, Retrievable“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „Accessibility: accessURL, downloadURL, URL availability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „Timeliness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „currentness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „timeliness, freshness, currency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „Date, Preservation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „dct:issued, dct:modified“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „temporal consistency, temporal validity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „FAIR I1--I3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „interoperability, interlinking, reuse of existing terms, reuse of vocabularies, dereferenceability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „Interoperability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/), [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „RDF-/DCAT-basierte Katalogbeschreibung“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — [`BernersLee2006LinkedData`](https://www.w3.org/DesignIssues/LinkedData.html)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „Linked-Data-Prinzipien“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „FAIR I2“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „MQA-Vokabularmetriken für Format, Lizenz, Zugriffsrechte und Kategorien“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „vocabulary reuse, semantic accuracy“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „thematic classification correctness, domain consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „FAIR R1, R1.1, R1.2, R1.3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „Reusability: license, access rights, contact point, publisher“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „Rights, OpenLicense, Contact“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „value-added, relevance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „FileFormat, FormatAccr, OpenFormat, MachineRead“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „format, media type, format vocabulary, non-proprietary format, machine readability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „FAIR R1.3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „versatility, interoperability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „interpretability, ease of understanding, concise representation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „understandability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „understandability, interpretability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „quality of free text“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „semantic accuracy, consistency, no contradictory values, correct annotations“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „conceptual consistency, domain consistency, nonquantitative attribute correctness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „accuracy, consistent representation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „accuracy, consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „ontologische Repräsentationsdefizite“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „FormatAccr, SizeAccr, Retrievable“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „nonquantitative attribute correctness, positional correctness, domain consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „accuracy, consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „FAIR R1: genaue und relevante Attribute“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „positional correctness, spatial domain consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „geographic search, dct:spatial“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „spatial information“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „FAIR R1.3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „fitness for use, relevance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — [`ISO19157`](https://www.iso.org/standard/78900.html)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „ISO 19157 als geodatenbezogener Qualitätsrahmen“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „believability, reputation, objectivity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „credibility, traceability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „trustworthiness, reputation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „FAIR R1.2“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „publisher, contact point“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „fitness for use, relevance, value-added, appropriate amount of data“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „Datenqualität im Nutzungskontext“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „kontextabhängige Relevanz von Qualitätsmerkmalen“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „FAIR R1/R1.3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „relevance“

## C. Quellen im Detail

Sortiert nach Anzahl der Fundstellen, absteigend — die tragendsten Quellen zuerst.

### `Zaveri2016LinkedDataQuality` — Zaveri et al. (2016)

**Quality Assessment for Linked Data: A Survey**  
in: Semantic Web · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.3233/SW-150175)**  

26 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:231` — RDF, Linked Data und SHACL · gemeinsam mit [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909) · [DOI](https://doi.org/10.3233/SW-150175)  
  > In der Literatur zu Linked Data und Metadatenqualität wird Validierung zwar als zentraler Bestandteil der Qualitätsprüfung betrachtet, zugleich aber betont, dass darüber hinaus weitere Qualitätsdimensionen wie Vollständigkeit, Auffindbarkeit, Genauigkeit, oder Nachnutzbarkeit relevant sind [@Gayo2015LinkedDataValidationQuality,Neumaier2016MetadataQuality,Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:349` — Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al. · [DOI](https://doi.org/10.3233/SW-150175)  
  > Einen zentralen Referenzpunkt für die systematische Einordnung von Metadatenqualität im Semantic-Web- und Linked-Data-Kontext bildet die Arbeit von Zaveri et al. [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:349` — Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al. · [DOI](https://doi.org/10.3233/SW-150175)  
  > Grundlage ist eine systematische Literaturauswertung, in der 118 potenziell relevante Arbeiten identifiziert, 73 Arbeiten näher geprüft, und schließlich 30 Kernansätze sowie 12 Werkzeuge zur Linked-Data-Qualitätsbewertung vergleichend analysiert werden [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:351` — Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al. · [DOI](https://doi.org/10.3233/SW-150175)  
  > Linked Data kann formal korrekt publiziert sein und zugleich unvollständig, inkonsistent, veraltet, schwer interpretierbar, oder unzureichend mit anderen Datenquellen verknüpft sein [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:353` — Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al. · [DOI](https://doi.org/10.3233/SW-150175)  
  > Zaveri et al. strukturieren diese Anforderungen in einem umfassenden Qualitätsrahmen mit insgesamt 18 Dimensionen und 69 Metriken [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:356` — Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al. · [DOI](https://doi.org/10.3233/SW-150175)  
  > Dies betrifft insbesondere Metriken der Vertrauenswürdigkeit, etwa die Einschätzung eines Datenanbieters oder einer Datenquelle [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:379` — Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al. · _Unterschrift_ · [DOI](https://doi.org/10.3233/SW-150175)  
  > [h!] 1.3 1whitewhite |p3.5cm|p9.3cm| Kategorie & Unterdimensionen Zugänglichkeit & Verfügbarkeit, Lizenzierung, Interlinking, Sicherheit, Performanz Intrinsische Qualität & Syntaktische Validität, Semantische Genauigkeit, Konsistenz, Prägnanz, Vollständigkeit Kontextuelle Qualität & Relevanz, Vertrauenswürdigkeit, Verständlichkeit, Aktualität Repräsentationale Qualität & Repräsentationsprägnanz, Interoperabilität, Vielseitigkeit, Interpretierbarkeit justification=centering Qualitätskategorien und Unterdimensionen für Linked Data nach Zaveri et al.; die zugehörigen 69 Einzelmetriken werden hier nicht im Detail wiedergegeben [@Zaveri2016LinkedDataQuality]

- [ ] `contents.tex:383` — Metadatenqualität und Qualitätsbewertung von Linked Data › Linked-Data-Qualität nach Zaveri et al. · [DOI](https://doi.org/10.3233/SW-150175)  
  > Bewertet werden können dabei unterschiedliche Ebenen von Linked Data, insbesondere einzelne RDF-Tripel, RDF-Graphen, Entitäten, oder ganze Datensätze [@Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:708` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken · gemeinsam mit [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Die stärker auf RDF und Metadaten ausgerichteten Modelle von Zaveri et al. und Nogueras-Iso et al. machen Qualitätsaspekte jenseits der formalen Validität sichtbar, setzen für viele ihrer Prüfungen jedoch Kontextwissen, externe Referenzdaten oder manuelle Bewertungen voraus und sind damit nur begrenzt skalierbar [@Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:814` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [DOI](https://doi.org/10.3233/SW-150175)  
  > K4 & Semantische und inhaltliche Qualität & Forschungsfrage zu KI-gestützten Analyseverfahren; Literatur zu Verständlichkeit, Accuracy, semantischer Konsistenz und Qualität von Freitextfeldern nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata]. & Ergänzung formaler Prüfungen um Aussagekraft, Verständlichkeit, Plausibilität und inhaltliche Passung.

- [ ] `contents.tex:818` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [DOI](https://doi.org/10.3233/SW-150175)  
  > K6 & Interoperabilität und Linked-Data-Qualität & Literatur zu FAIR, Linked Data, RDF-Grundlagen, DCAT und Linked-Data-Qualität nach [@wilkinson2016fair, W3CRDF11Concepts, W3CDCAT3, Zaveri2016LinkedDataQuality, Gayo2015LinkedDataValidationQuality]. & Bewertung, ob Metadaten über URIs, Normdaten, kontrollierte Vokabulare und Graphbezüge interoperabel und verknüpfbar sind.

- [ ] `contents.tex:826` — Auswertungsverfahren der Interviews · gemeinsam mit [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`corteslasalle_shacl_dqa`](https://doi.org/10.48550/arXiv.2507.22305), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`BernersLee2006LinkedData`](https://www.w3.org/DesignIssues/LinkedData.html) · [DOI](https://doi.org/10.3233/SW-150175)  
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1279` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · [DOI](https://doi.org/10.3233/SW-150175)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „syntactic validity, consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „schema completeness, property completeness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — (Kapiteleinleitung) · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „relevance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „availability, dereferenceability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „timeliness, freshness, currency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „interoperability, interlinking, reuse of existing terms, reuse of vocabularies, dereferenceability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „vocabulary reuse, semantic accuracy“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „versatility, interoperability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „understandability, interpretability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „semantic accuracy, consistency, no contradictory values, correct annotations“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „accuracy, consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „trustworthiness, reputation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — (Kapiteleinleitung) · [DOI](https://doi.org/10.3233/SW-150175)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „relevance“

---

### `data_europa` — data.europa.eu (2026)

**Metadata Quality Assessment Methodology: How data.europa.eu Measures the Quality of Harvested Metadata**  
Typ: `misc`  
→ **[Quelle öffnen](https://data.europa.eu/mqa/methodology?locale=en)**  
Zugriff: 2026-04-29  

22 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:623` — Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau · _Unterschrift_ · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > MQA-Qualitätsmetriken und Gewichtungen nach Wentzel et al. [@data_europa, wentzel2023extensive]

- [ ] `contents.tex:631` — Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Dadurch operationalisiert MQA/Piveau Metadatenqualität primär über praktische Nutzbarkeit, technische Zugänglichkeit, strukturelle Interoperabilität und rechtliche Wiederverwendbarkeit. [@data_europa, wentzel2023extensive] Während der Bearbeitung dieser Arbeit wurde eine überarbeitete Fassung des Frameworks (Metrics v2) angekündigt und dokumentiert, jedoch noch nicht veröffentlicht [@piveauMetricsV2].

- [ ] `contents.tex:730` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken › Bewertungslücke im DCAT-AP.de- und GovData-Kontext · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Die portalnahen Ansätze sind zwar operationalisiert, begründen die Auswahl und Gewichtung ihrer Metriken jedoch nicht empirisch [@data_europa].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:816` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > K5 & Technische Zugänglichkeit, Aktualität und Nutzbarkeit & Literatur zu Accessibility, Retrievability, Open Data Fitness und MQA/Piveau nach [@wilkinson2016fair, data_europa, Neumaier2016MetadataQuality, kubler2018comparison, wentzel2023extensive]. & Bewertung, ob Ressourcen erreichbar, technisch nutzbar, aktuell genug und praktisch weiterverarbeitbar sind.

- [ ] `contents.tex:824` — Auswertungsverfahren der Interviews · gemeinsam mit [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`W3CDQV`](https://www.w3.org/TR/vocab-dqv/), [`ISO19157`](https://www.iso.org/standard/78900.html) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1202` — Ableitung formaler, technischer und semantischer Einzelindikatoren · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Dieses Vorgehen ist anschlussfähig an die MQA, die die DCAT-AP-Konformität ebenfalls als eine Metrik innerhalb ihres Dimensionsmodells führt [@data_europa, wentzel2023extensive].

- [ ] `contents.tex:1246` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Bewertungsebene und Aggregation über Distributionen · gemeinsam mit [`piveauMetricsScore`](https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Bei mehreren Distributionen bestimmt die am besten bewertete Distribution das Ergebnis, unter der Annahme, dass alle Distributionen denselben Datensatz lediglich in unterschiedlichen Formaten repräsentieren [@data_europa, piveauMetricsScore].

- [ ] `contents.tex:1275` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1877` — Scoring-, Gewichtungs- und Aggregationslogik › Punktevergabe je Indikator · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Tabelle [tab:mqa_metrics_weights]) [@data_europa].

- [ ] `contents.tex:1932` — Scoring-, Gewichtungs- und Aggregationslogik › Gewichtung der Indikatoren und Dimensionen · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Tabelle [tab:mqa_metrics_weights]) [@data_europa].

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2422` — Vergleichsbaseline: MQA-Reimplementierung und A/B/C-Klassifikation · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Um beide Verfahren auf exakt derselben Datengrundlage vergleichen zu können, wurde die MQA-Bewertungslogik nach der offiziellen Methodik [@data_europa] reimplementiert und gegen die veröffentlichten Berichte von data.europa.eu validiert.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „DCAT-AP conformity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „feldbezogene MQA-Metriken“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „Findability: keywords, categories, spatial search, temporal search“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „Accessibility: accessURL, downloadURL, URL availability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „dct:issued, dct:modified“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „Interoperability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „MQA-Vokabularmetriken für Format, Lizenz, Zugriffsrechte und Kategorien“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „Reusability: license, access rights, contact point, publisher“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „format, media type, format vocabulary, non-proprietary format, machine readability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „geographic search, dct:spatial“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — (Kapiteleinleitung) · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [Web](https://data.europa.eu/mqa/methodology?locale=en)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „publisher, contact point“

---

### `wentzel2023extensive` — Wentzel et al. (2023)

**An Extensive Methodology and Framework for Quality Assessment of DCAT-AP Datasets**  
in: Electronic Government · Verlag: Springer · Typ: `inproceedings`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1007/978-3-031-41138-0_17)**  
Zusatz-URL: <https://doi.org/10.1007/978-3-031-41138-0_17>  

22 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:623` — Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau · _Unterschrift_ · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > MQA-Qualitätsmetriken und Gewichtungen nach Wentzel et al. [@data_europa, wentzel2023extensive]

- [ ] `contents.tex:631` — Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Dadurch operationalisiert MQA/Piveau Metadatenqualität primär über praktische Nutzbarkeit, technische Zugänglichkeit, strukturelle Interoperabilität und rechtliche Wiederverwendbarkeit. [@data_europa, wentzel2023extensive] Während der Bearbeitung dieser Arbeit wurde eine überarbeitete Fassung des Frameworks (Metrics v2) angekündigt und dokumentiert, jedoch noch nicht veröffentlicht [@piveauMetricsV2].

- [ ] `contents.tex:633` — Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Einzelne Messergebnisse werden als dqv:QualityMeasurement modelliert, während SHACL-basierte Validierungsergebnisse zur DCAT-AP-Konformität als Qualitätsannotation eingebunden werden können. [@wentzel2023extensive] Beide Modellierungsformen sind in Tabelle [tab:piveau_dqv_model] dargestellt. [h!] 1.2 1whitewhite

- [ ] `contents.tex:677` — Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau · _Unterschrift_ · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > [t]0.46 Quality Measurement ll DQV Quality Measurement rdf:type dqv:QualityMeasurement dqv:isMeasurementOf dqv:value dqv:computedOn prov:generatedAtTime [t]0.46 Quality Annotation ll DQV Quality Annotation rdf:type dqv:QualityAnnotation oa:hasBody dqv:inDimension oa:motivatedBy dc:isVersionOf oa:hasTarget prov:generatedAtTime Modellierung von Quality Measurements und Quality Annotations nach Wentzel et al. [@wentzel2023extensive]

- [ ] `contents.tex:713` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken · gemeinsam mit [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Die portalnahen Ansätze von Neumaier et al. und die MQA sind dem Anwendungskontext am nächsten und automatisiert prüfbar, konzentrieren sich dafür aber auf leicht messbare, überwiegend formale und feldbezogene Kriterien und bilden weitergehende semantische Aspekte nur eingeschränkt ab [@Neumaier2016MetadataQuality, wentzel2023extensive].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:810` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > K2 & Vollständigkeit, Reichhaltigkeit und Feldrelevanz & Leitfadenfrage zu Qualitätsmerkmalen; Literatur zu Vollständigkeit nach [@wentzel2023extensive, wilkinson2016fair, DCATAPDESpec2, DCATAPDESpec3]. & Bestimmung, welche Metadatenfelder für einen Score geprüft und wie Pflicht-, empfohlene und optionale Angaben gewichtet werden.

- [ ] `contents.tex:816` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > K5 & Technische Zugänglichkeit, Aktualität und Nutzbarkeit & Literatur zu Accessibility, Retrievability, Open Data Fitness und MQA/Piveau nach [@wilkinson2016fair, data_europa, Neumaier2016MetadataQuality, kubler2018comparison, wentzel2023extensive]. & Bewertung, ob Ressourcen erreichbar, technisch nutzbar, aktuell genug und praktisch weiterverarbeitbar sind.

- [ ] `contents.tex:824` — Auswertungsverfahren der Interviews · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`W3CDQV`](https://www.w3.org/TR/vocab-dqv/), [`ISO19157`](https://www.iso.org/standard/78900.html) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

- [ ] `contents.tex:826` — Auswertungsverfahren der Interviews · gemeinsam mit [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`corteslasalle_shacl_dqa`](https://doi.org/10.48550/arXiv.2507.22305), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`BernersLee2006LinkedData`](https://www.w3.org/DesignIssues/LinkedData.html) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1202` — Ableitung formaler, technischer und semantischer Einzelindikatoren · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Dieses Vorgehen ist anschlussfähig an die MQA, die die DCAT-AP-Konformität ebenfalls als eine Metrik innerhalb ihres Dimensionsmodells führt [@data_europa, wentzel2023extensive].

- [ ] `contents.tex:1275` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „DCAT-AP conformity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „feldbezogene MQA-Metriken“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „Findability: keywords, categories, spatial search, temporal search“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „Accessibility: accessURL, downloadURL, URL availability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „dct:issued, dct:modified“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „Interoperability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „MQA-Vokabularmetriken für Format, Lizenz, Zugriffsrechte und Kategorien“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „Reusability: license, access rights, contact point, publisher“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „format, media type, format vocabulary, non-proprietary format, machine readability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „geographic search, dct:spatial“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — (Kapiteleinleitung) · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [DOI](https://doi.org/10.1007/978-3-031-41138-0_17)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „publisher, contact point“

---

### `wang1996beyond` — Wang & Strong (1996)

**Beyond Accuracy: What Data Quality Means to Data Consumers**  
in: Journal of Management Information Systems · Typ: `article`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  

21 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:243` — Datenqualität › Definition nach Wang and Strong 1996 · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Einen zentralen Referenzpunkt bildet die Arbeit von Wang und Strong, die Datenqualität als fitness for use definieren und damit die Perspektive der Datennutzenden in den Mittelpunkt stellen [@wang1996beyond].

- [ ] `contents.tex:243` — Datenqualität › Definition nach Wang and Strong 1996 · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Ausgehend von einer empirischen Untersuchung von Datenkonsumentinnen und -konsumenten entwickeln sie ein hierarchisches Rahmenmodell, in dem Datenqualitätsmerkmale nicht allein aus theoretischen Vorannahmen oder aus Sicht von Systementwickelnden abgeleitet werden, sondern aus den Anforderungen tatsächlicher Nutzungssituationen hervorgehen [@wang1996beyond].

- [ ] `contents.tex:245` — Datenqualität › Definition nach Wang and Strong 1996 · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Wang und Strong unterscheiden vier übergeordnete Kategorien von Datenqualität: intrinsische, kontextuelle, repräsentationale, und zugangsbezogene Qualität [@wang1996beyond].

- [ ] `contents.tex:254` — Datenqualität › Definition nach Wang and Strong 1996 · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Vielmehr hängt sie davon ab, ob Daten in einem bestimmten Arbeits- oder Entscheidungskontext brauchbar sind [@wang1996beyond].

- [ ] `contents.tex:704` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken · gemeinsam mit [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Die abstrakten Qualitätskonzepte von Wang und Strong, ISO/IEC 25012 und FAIR liefern die begriffliche Rahmung und begründen Qualität als mehrdimensionales, nutzungsabhängiges Konzept, legen aber nicht fest, welche Metadatenelemente, Vokabulare oder Zugriffspfade konkret zu prüfen sind [@wang1996beyond, iso25012, wilkinson2016fair].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:808` — Auswertungsverfahren der Interviews · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > K1 & Qualitäts- verständnis und ideale Metadaten & Forschungsfrage zur Entwicklung eines praxisrelevanten Bewertungsmodells; Leitfadenblock „perfekte Metadaten“; Datenqualitätsverständnis nach [@wang1996beyond]. & Ableitung übergeordneter Anforderungen an ein gutes DCAT-AP.de-Metadatenmodell.

- [ ] `contents.tex:814` — Auswertungsverfahren der Interviews · gemeinsam mit [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > K4 & Semantische und inhaltliche Qualität & Forschungsfrage zu KI-gestützten Analyseverfahren; Literatur zu Verständlichkeit, Accuracy, semantischer Konsistenz und Qualität von Freitextfeldern nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata]. & Ergänzung formaler Prüfungen um Aussagekraft, Verständlichkeit, Plausibilität und inhaltliche Passung.

- [ ] `contents.tex:820` — Auswertungsverfahren der Interviews · gemeinsam mit [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > K7 & Kontextsensitivität und Fit for Purpose & Forschungsfrage zur praxisrelevanten Bewertung; Literatur zu Fit for Purpose, Kontextualität, FAIR-Nachnutzung und domänenspezifischer Datenqualität nach [@wang1996beyond, StrongLeeWang1997, wand1996anchoring, wilkinson2016fair, Ubaldi2013OGD]. & Anpassung von Bewertung, Gewichtung und Interpretation an Nutzungskontext, Domäne und Stakeholderperspektive.

- [ ] `contents.tex:822` — Auswertungsverfahren der Interviews · gemeinsam mit [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > K8 & Rohdatenbezug und Metadaten-Daten-Kongruenz & Forschungsfrage zur Kombination formaler Validierung mit kontextbezogenen Prüfverfahren; Leitfadenblock „Relevanz des eigentlichen Datensatzes“; Literatur zu Accuracy und Daten-Metadaten-Konsistenz nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, noguerasiso_quality_metadata]. & Prüfung, ob Metadaten mit der tatsächlichen Ressource übereinstimmen und ob Rohdaten zur Plausibilisierung herangezogen werden können.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1104` — Ableitung relevanter Qualitätsdimensionen · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Auch Wang und Strong (1996) ordneten ihre empirisch ermittelten Qualitätsdimensionen in der abschließenden Verdichtungsstufe ihrer Studie nicht nach deren Herkunft, sondern anhand eines zuvor entwickelten konzeptionellen Rahmens vier übergeordneten Kategorien zu [@wang1996beyond].

- [ ] `contents.tex:1240` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Ternäre und graduelle Indikatoren · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Die zweite Klasse umfasst semantische Urteile, die naturgemäß keine scharfe Erfüllungsgrenze besitzen, beispielsweise die Aussagekraft einer Beschreibung; für solche originär subjektiven Qualitätsurteile ist eine kontinuierliche Skala methodisch etabliert, wie sie bereits Wang und Strong zur Erhebung von Wichtigkeitsurteilen mittels neunstufiger Skala einsetzten [@wang1996beyond].

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1871` — Scoring-, Gewichtungs- und Aggregationslogik · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Wie in Sektion [sec:wang_strong_definition_quality] erläutert, ist Datenqualität kein eindimensionales Konstrukt, sondern setzt sich aus mehreren, getrennt zu messenden Dimensionen zusammen [@wang1996beyond].

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „Completeness, appropriate amount of data, value-added“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — (Kapiteleinleitung) · gemeinsam mit [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „relevance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „Timeliness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „value-added, relevance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „interpretability, ease of understanding, concise representation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „accuracy, consistent representation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „fitness for use, relevance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „believability, reputation, objectivity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „fitness for use, relevance, value-added, appropriate amount of data“

---

### `wilkinson2016fair` — Wilkinson & others (2016)

**The FAIR Guiding Principles for scientific data management and stewardship**  
in: Scientific Data · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1038/sdata.2016.18)**  

21 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:286` — Datenqualität › FAIR-Prinzipien · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Eine weitere zentrale Referenz bilden die FAIR-Prinzipien von Wilkinson et al. [@wilkinson2016fair].

- [ ] `contents.tex:288` — Datenqualität › FAIR-Prinzipien · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Wilkinson et al. betonen, dass die Prinzipien nicht nur die Nachnutzung durch menschliche Forschende unterstützen sollen, sondern ausdrücklich auch die Fähigkeit von Maschinen verbessern, Daten automatisch zu finden und zu nutzen [@wilkinson2016fair].

- [ ] `contents.tex:299` — Datenqualität › FAIR-Prinzipien · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Ihre Umsetzung kann daher inkrementell erfolgen und hängt vom jeweiligen Datenbestand, Fachkontext, und technischen Ökosystem ab.[@wilkinson2016fair]

- [ ] `contents.tex:336` — Datenqualität › FAIR-Prinzipien · _Unterschrift_ · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > R1.3 & (Meta-)Daten erfüllen domänenspezifische Community-Standards. justification=centering FAIR-Prinzipien nach Wilkinson et al. [@wilkinson2016fair]

- [ ] `contents.tex:704` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Die abstrakten Qualitätskonzepte von Wang und Strong, ISO/IEC 25012 und FAIR liefern die begriffliche Rahmung und begründen Qualität als mehrdimensionales, nutzungsabhängiges Konzept, legen aber nicht fest, welche Metadatenelemente, Vokabulare oder Zugriffspfade konkret zu prüfen sind [@wang1996beyond, iso25012, wilkinson2016fair].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:810` — Auswertungsverfahren der Interviews · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > K2 & Vollständigkeit, Reichhaltigkeit und Feldrelevanz & Leitfadenfrage zu Qualitätsmerkmalen; Literatur zu Vollständigkeit nach [@wentzel2023extensive, wilkinson2016fair, DCATAPDESpec2, DCATAPDESpec3]. & Bestimmung, welche Metadatenfelder für einen Score geprüft und wie Pflicht-, empfohlene und optionale Angaben gewichtet werden.

- [ ] `contents.tex:816` — Auswertungsverfahren der Interviews · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > K5 & Technische Zugänglichkeit, Aktualität und Nutzbarkeit & Literatur zu Accessibility, Retrievability, Open Data Fitness und MQA/Piveau nach [@wilkinson2016fair, data_europa, Neumaier2016MetadataQuality, kubler2018comparison, wentzel2023extensive]. & Bewertung, ob Ressourcen erreichbar, technisch nutzbar, aktuell genug und praktisch weiterverarbeitbar sind.

- [ ] `contents.tex:818` — Auswertungsverfahren der Interviews · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > K6 & Interoperabilität und Linked-Data-Qualität & Literatur zu FAIR, Linked Data, RDF-Grundlagen, DCAT und Linked-Data-Qualität nach [@wilkinson2016fair, W3CRDF11Concepts, W3CDCAT3, Zaveri2016LinkedDataQuality, Gayo2015LinkedDataValidationQuality]. & Bewertung, ob Metadaten über URIs, Normdaten, kontrollierte Vokabulare und Graphbezüge interoperabel und verknüpfbar sind.

- [ ] `contents.tex:820` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > K7 & Kontextsensitivität und Fit for Purpose & Forschungsfrage zur praxisrelevanten Bewertung; Literatur zu Fit for Purpose, Kontextualität, FAIR-Nachnutzung und domänenspezifischer Datenqualität nach [@wang1996beyond, StrongLeeWang1997, wand1996anchoring, wilkinson2016fair, Ubaldi2013OGD]. & Anpassung von Bewertung, Gewichtung und Interpretation an Nutzungskontext, Domäne und Stakeholderperspektive.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1281` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „FAIR F2, R1“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „FAIR F1--F4“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „FAIR A1, A1.1, A2“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „FAIR I1--I3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „FAIR I2“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „FAIR R1, R1.1, R1.2, R1.3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „FAIR R1.3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „FAIR R1: genaue und relevante Attribute“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „FAIR R1.3“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „FAIR R1.2“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1038/sdata.2016.18)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „FAIR R1/R1.3“

---

### `Neumaier2016MetadataQuality` — Neumaier et al. (2016)

**Automated Quality Assessment of Metadata Across Open Data Portals**  
in: Journal of Data and Information Quality · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1145/2964909)**  

20 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:231` — RDF, Linked Data und SHACL · gemeinsam mit [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175) · [DOI](https://doi.org/10.1145/2964909)  
  > In der Literatur zu Linked Data und Metadatenqualität wird Validierung zwar als zentraler Bestandteil der Qualitätsprüfung betrachtet, zugleich aber betont, dass darüber hinaus weitere Qualitätsdimensionen wie Vollständigkeit, Auffindbarkeit, Genauigkeit, oder Nachnutzbarkeit relevant sind [@Gayo2015LinkedDataValidationQuality,Neumaier2016MetadataQuality,Zaveri2016LinkedDataQuality].

- [ ] `contents.tex:388` — Metadatenqualität und Qualitätsbewertung von Linked Data › Automatisierte Metadatenbewertung in Open-Data-Portalen nach Neumaier et al. · [DOI](https://doi.org/10.1145/2964909)  
  > In ihrer Arbeit entwickeln sie einen automatisierten Ansatz zur Bewertung von Metadatenqualität über unterschiedliche Datenportale hinweg [@Neumaier2016MetadataQuality].

- [ ] `contents.tex:395` — Metadatenqualität und Qualitätsbewertung von Linked Data › Automatisierte Metadatenbewertung in Open-Data-Portalen nach Neumaier et al. · [DOI](https://doi.org/10.1145/2964909)  
  > Drittens definieren die Autoren konkrete Qualitätsmetriken auf Basis zentraler DCAT-Eigenschaften, die automatisiert, skalierbar, und effizient berechnet werden können [@Neumaier2016MetadataQuality].

- [ ] `contents.tex:494` — Metadatenqualität und Qualitätsbewertung von Linked Data › Automatisierte Metadatenbewertung in Open-Data-Portalen nach Neumaier et al. · _Unterschrift_ · [DOI](https://doi.org/10.1145/2964909)  
  > justification=centering Qualitätsdimensionen auf DCAT-Schlüsseln nach Neumaier et al. [@Neumaier2016MetadataQuality]

- [ ] `contents.tex:713` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [DOI](https://doi.org/10.1145/2964909)  
  > Die portalnahen Ansätze von Neumaier et al. und die MQA sind dem Anwendungskontext am nächsten und automatisiert prüfbar, konzentrieren sich dafür aber auf leicht messbare, überwiegend formale und feldbezogene Kriterien und bilden weitergehende semantische Aspekte nur eingeschränkt ab [@Neumaier2016MetadataQuality, wentzel2023extensive].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:816` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [DOI](https://doi.org/10.1145/2964909)  
  > K5 & Technische Zugänglichkeit, Aktualität und Nutzbarkeit & Literatur zu Accessibility, Retrievability, Open Data Fitness und MQA/Piveau nach [@wilkinson2016fair, data_europa, Neumaier2016MetadataQuality, kubler2018comparison, wentzel2023extensive]. & Bewertung, ob Ressourcen erreichbar, technisch nutzbar, aktuell genug und praktisch weiterverarbeitbar sind.

- [ ] `contents.tex:824` — Auswertungsverfahren der Interviews · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`W3CDQV`](https://www.w3.org/TR/vocab-dqv/), [`ISO19157`](https://www.iso.org/standard/78900.html) · [DOI](https://doi.org/10.1145/2964909)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

- [ ] `contents.tex:826` — Auswertungsverfahren der Interviews · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`corteslasalle_shacl_dqa`](https://doi.org/10.48550/arXiv.2507.22305), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`BernersLee2006LinkedData`](https://www.w3.org/DesignIssues/LinkedData.html) · [DOI](https://doi.org/10.1145/2964909)  
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1247` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Bewertungsebene und Aggregation über Distributionen · [DOI](https://doi.org/10.1145/2964909)  
  > Empirische Untersuchungen von Open-Data-Portalen verorten zentrale Fehlerbilder wie nicht abrufbare Ressourcen entsprechend auf der Ebene der einzelnen Ressource, weshalb Neumaier et al. die Abrufbarkeit je Ressource und nicht je Datensatz prüfen [@Neumaier2016MetadataQuality].

- [ ] `contents.tex:1252` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Malus-Prinzip · [DOI](https://doi.org/10.1145/2964909)  
  > Eine unklare Lizenz macht die Nachnutzung rechtlich unsicher, was die Nachnutzbarkeit stark verkompliziert [@Neumaier2016MetadataQuality].

- [ ] `contents.tex:1277` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · [DOI](https://doi.org/10.1145/2964909)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „Conformance“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „Existence“

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „Discovery: dct:title, dct:description, dcat:keyword“

- [ ] `appendix/longlist_kandidatendimensionen.tex:44` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 4 (Technische Zugänglichkeit und Abrufbarkeit) — belegter Ausdruck: „Access, AccessURL, Retrievable“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „Date, Preservation“

- [ ] `appendix/longlist_kandidatendimensionen.tex:64` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 8 (Wiederverwendbarkeit und organisatorische Nutzbarkeit) — belegter Ausdruck: „Rights, OpenLicense, Contact“

- [ ] `appendix/longlist_kandidatendimensionen.tex:69` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 9 (Format- und Maschinenlesbarkeitsqualität) — belegter Ausdruck: „FileFormat, FormatAccr, OpenFormat, MachineRead“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „FormatAccr, SizeAccr, Retrievable“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1145/2964909)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „spatial information“

---

### `noguerasiso_quality_metadata` — Nogueras-Iso et al. (2021)

**Quality of Metadata in Open Data Portals**  
in: IEEE Access · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1109/ACCESS.2021.3073455)**  

13 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:687` — Metadatenqualität und Qualitätsbewertung von Linked Data › ISO 19157 als Qualitätsinstrument · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Diese Struktur erlaubt es, verschiedene Fehlerarten präziser voneinander zu unterscheiden und Qualitätsmessungen nicht nur als einfache Punktwerte, sondern als methodisch nachvollziehbare Prüfergebnisse zu modellieren. [@noguerasiso_quality_metadata]

- [ ] `contents.tex:693` — Metadatenqualität und Qualitätsbewertung von Linked Data › ISO 19157 als Qualitätsinstrument · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Dadurch entsteht eine zweistufige Bewertungslogik, die Rohmessung, Prüfverfahren und Qualitätsurteil voneinander trennt. [@noguerasiso_quality_metadata]

- [ ] `contents.tex:708` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken · gemeinsam mit [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Die stärker auf RDF und Metadaten ausgerichteten Modelle von Zaveri et al. und Nogueras-Iso et al. machen Qualitätsaspekte jenseits der formalen Validität sichtbar, setzen für viele ihrer Prüfungen jedoch Kontextwissen, externe Referenzdaten oder manuelle Bewertungen voraus und sind damit nur begrenzt skalierbar [@Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:814` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > K4 & Semantische und inhaltliche Qualität & Forschungsfrage zu KI-gestützten Analyseverfahren; Literatur zu Verständlichkeit, Accuracy, semantischer Konsistenz und Qualität von Freitextfeldern nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata]. & Ergänzung formaler Prüfungen um Aussagekraft, Verständlichkeit, Plausibilität und inhaltliche Passung.

- [ ] `contents.tex:822` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > K8 & Rohdatenbezug und Metadaten-Daten-Kongruenz & Forschungsfrage zur Kombination formaler Validierung mit kontextbezogenen Prüfverfahren; Leitfadenblock „Relevanz des eigentlichen Datensatzes“; Literatur zu Accuracy und Daten-Metadaten-Konsistenz nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, noguerasiso_quality_metadata]. & Prüfung, ob Metadaten mit der tatsächlichen Ressource übereinstimmen und ob Rohdaten zur Plausibilisierung herangezogen werden können.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „completeness omission“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „temporal consistency, temporal validity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:59` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 7 (Vokabular-, Normdaten- und Klassifikationsqualität) — belegter Ausdruck: „thematic classification correctness, domain consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „quality of free text“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „conceptual consistency, domain consistency, nonquantitative attribute correctness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:84` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 12 (Metadaten-Daten-Kongruenz) — belegter Ausdruck: „nonquantitative attribute correctness, positional correctness, domain consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — (Kapiteleinleitung) · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „positional correctness, spatial domain consistency“

- [ ] `appendix/iso19157_qualitaetselemente.tex:187` — (Kapiteleinleitung) · _Unterschrift_ · [DOI](https://doi.org/10.1109/ACCESS.2021.3073455)  
  > Kombinierte Übersicht der ISO-19157-Qualitätselemente, Scopes, Measures und Evaluationsarten nach Nogueras-Iso et al. [@noguerasiso_quality_metadata]

---

### `iso25012` — International Organization for Standa… (2008)

**ISO/IEC 25012:2008 Data Quality Model**  
Organisation: International Organization for Standardization · Typ: `misc`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  

11 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:264` — Datenqualität › Qualitätsmodell der ISO-Norm 25012 · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Datenqualitätsmerkmale werden den Perspektiven inhärenter und systemabhänger Qualität zugeordnet. [@iso25012]

- [ ] `contents.tex:704` — Metadatenqualität und Qualitätsbewertung von Linked Data › Vergleich bestehender Ansätze und offene Bewertungslücken · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Die abstrakten Qualitätskonzepte von Wang und Strong, ISO/IEC 25012 und FAIR liefern die begriffliche Rahmung und begründen Qualität als mehrdimensionales, nutzungsabhängiges Konzept, legen aber nicht fest, welche Metadatenelemente, Vokabulare oder Zugriffspfade konkret zu prüfen sind [@wang1996beyond, iso25012, wilkinson2016fair].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:824` — Auswertungsverfahren der Interviews · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`W3CDQV`](https://www.w3.org/TR/vocab-dqv/), [`ISO19157`](https://www.iso.org/standard/78900.html) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1240` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Ternäre und graduelle Indikatoren · gemeinsam mit [`iso25024`](https://scholar.google.com/scholar?q=ISO%2FIEC+25024%3A2015+Systems+and+Software+Engineering+--+Systems+and+Software+Quality+Requirements+and+Evaluation+%28SQuaRE%29+--+Measurement+of+Data+Quality) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Die Norm ergänzt die Qualitätscharakteristiken aus ISO/IEC 25012 um konkrete Messfunktionen [@iso25024, iso25012].

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „conformity“

- [ ] `appendix/longlist_kandidatendimensionen.tex:34` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 2 (Vollständigkeit und feldbezogene Reichhaltigkeit) — belegter Ausdruck: „completeness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:49` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 5 (Aktualität und temporale Konsistenz) — belegter Ausdruck: „currentness“

- [ ] `appendix/longlist_kandidatendimensionen.tex:74` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 10 (Semantische Aussagekraft und Verständlichkeit) — belegter Ausdruck: „understandability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „accuracy, consistency“

- [ ] `appendix/longlist_kandidatendimensionen.tex:94` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 14 (Vertrauenswürdigkeit, Provenienz und Verantwortlichkeit) — belegter Ausdruck: „credibility, traceability“

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „kontextabhängige Relevanz von Qualitätsmerkmalen“

---

### `DCATAPDEImplRules2` — DCAT-AP.de (2022)

**DCAT-AP.de Konventionenhandbuch 2.0**  
Typ: `online`  
→ **[Quelle öffnen](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)**  
Zugriff: 2026-04-21  

8 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:138` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Der Standard legt fest, welche Informationen in welcher Form beschrieben werden sollen, und schafft so die Grundlage für einheitliche semantische Beschreibungen, föderierte Suche, und die Weiterverarbeitung von Metadaten über Schnittstellen und Portale hinweg [@DCATAPDESpec3,DCATAPDEImplRules2].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:812` — Auswertungsverfahren der Interviews · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CSHACL`](https://www.w3.org/TR/shacl/), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > K3 & Formale und syntaktische Qualität & Forschungsfrage zur Integration von RDF-/SHACL-Prüfungen; Literatur zu Conformance, syntaktischer Validität und DCAT-AP.de-Konformität nach [@W3CRDF11Concepts, W3CSHACL, DCATAPDESpec2, DCATAPDESpec3, DCATAPDEImplRules2, Gayo2015LinkedDataValidationQuality]. & Erfassung regelbasierter, automatisierbarer Fehler über SHACL, XML/RDF, URI-, Vokabular- und Datentypprüfungen.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1273` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1390` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Aussagekraftsindikatoren · gemeinsam mit [`bydata2025handreichung`](https://open.bydata.de/) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Erstens werden die Bewertungskriterien nicht frei definiert, sondern aus den Qualitätsanforderungen des DCAT-AP.de-Konventionenhandbuchs sowie der Handreichung zur Verbesserung der Metadatenqualität von offenen Daten abgeleitet [@DCATAPDEImplRules2, bydata2025handreichung].

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1516` — Extraktion und Anreicherung der Metadaten · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Dazu gehören die Vokabulare des Publications Office der Europäischen Union für Themen, Dateitypen und Aktualisierungsfrequenzen https://op.europa.eu/en/web/eu-vocabularies/authority-tables, das Medientypregister der IANA https://www.iana.org/assignments/media-types/ sowie die Lizenzliste, die IDs der Datenbereitsteller und das Schlüsselverzeichnis der politischen Geokodierung aus DCAT-AP.de [@DCATAPDEImplRules2].

- [ ] `contents.tex:1680` — Implementierung der Einzelindikatoren › Auffindbarkeitsindikatoren · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Die dedizierte Eigenschaft dcatde:politicalGeocodingURI ist gemäß Konvention 08 des DCAT-AP.de-Konventionenhandbuchs der vorgesehene Weg, den verwaltungspolitischen Geobezug als URI aus dem zugehörigen kontrollierten Vokabular auszudrücken [@DCATAPDEImplRules2].

- [ ] `contents.tex:1773` — Implementierung der Einzelindikatoren › Nachnutzbarkeitsindikatoren · gemeinsam mit [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Diese Version bildet ein vollständig abgeschlossenes Profil, das neben der Spezifikation auch ein zugehöriges Konventionenhandbuch bereitstellt [@DCATAPDESpec2, DCATAPDEImplRules2] und damit die Grundlage des in Kapitel 4 abgeleiteten Bewertungsmodells bildet.

- [ ] `contents.tex:1843` — LLM-gestützte Bewertung der Aussagekraft › Eingabe und Prompt · gemeinsam mit [`bydata2025handreichung`](https://open.bydata.de/) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/implRules/)  
  > Sie enthält die schrittweise Vorgehensweise je Kriterium, die aus dem DCAT-AP.de-Konventionenhandbuch v2.0 (Kapitel 1.7 und 3.4) sowie der Handreichung zur Verbesserung der Metadatenqualität abgeleiteten Bewertungsregeln [@DCATAPDEImplRules2, bydata2025handreichung] und eine Ankerskala, die Wertebereiche verbal an Qualitätsniveaus bindet.

---

### `DCATAPDESpec3` — DCAT-AP.de (2024)

**DCAT-AP.de Spezifikation 3.0**  
Typ: `online`  
→ **[Quelle öffnen](https://www.dcat-ap.de/def/dcatde/3.0/spec/)**  
Zugriff: 2026-04-21  

7 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:132` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/) · [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > Sein Zweck liegt insbesondere darin, Metadaten offener Verwaltungsdaten zwischen deutschen Open-Data-Portalen interoperabel auszutauschen und diese Daten über GovData zentral auffindbar zu machen [@DCATAPDESpec3,DCATAPDESpec2].

- [ ] `contents.tex:134` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`DCATAPDEStart`](https://www.dcat-ap.de/) · [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > Damit steht der Standard in einem mehrstufigen Interoperabilitätszusammenhang: vom allgemeinen Modell für Datenkataloge im Web über das europäische Anwendungsprofil bis hin zur deutschen Spezifikation für offene Verwaltungsdaten [@DCATAPDEStart,DCATAPDESpec3].

- [ ] `contents.tex:138` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/) · [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > Der Standard legt fest, welche Informationen in welcher Form beschrieben werden sollen, und schafft so die Grundlage für einheitliche semantische Beschreibungen, föderierte Suche, und die Weiterverarbeitung von Metadaten über Schnittstellen und Portale hinweg [@DCATAPDESpec3,DCATAPDEImplRules2].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:810` — Auswertungsverfahren der Interviews · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/) · [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > K2 & Vollständigkeit, Reichhaltigkeit und Feldrelevanz & Leitfadenfrage zu Qualitätsmerkmalen; Literatur zu Vollständigkeit nach [@wentzel2023extensive, wilkinson2016fair, DCATAPDESpec2, DCATAPDESpec3]. & Bestimmung, welche Metadatenfelder für einen Score geprüft und wie Pflicht-, empfohlene und optionale Angaben gewichtet werden.

- [ ] `contents.tex:812` — Auswertungsverfahren der Interviews · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CSHACL`](https://www.w3.org/TR/shacl/), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > K3 & Formale und syntaktische Qualität & Forschungsfrage zur Integration von RDF-/SHACL-Prüfungen; Literatur zu Conformance, syntaktischer Validität und DCAT-AP.de-Konformität nach [@W3CRDF11Concepts, W3CSHACL, DCATAPDESpec2, DCATAPDESpec3, DCATAPDEImplRules2, Gayo2015LinkedDataValidationQuality]. & Erfassung regelbasierter, automatisierbarer Fehler über SHACL, XML/RDF, URI-, Vokabular- und Datentypprüfungen.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1271` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1773` — Implementierung der Einzelindikatoren › Nachnutzbarkeitsindikatoren · [Web](https://www.dcat-ap.de/def/dcatde/3.0/spec/)  
  > Die im Dezember 2024 veröffentlichte Version 3.0 wird bewusst nicht verwendet, da für sie kein geschlossenes Konventionenhandbuch mehr vorgesehen ist; die Konventionen werden stattdessen in die Spezifikation überführt, in Guidelines umgewandelt oder gestrichen, wobei entsprechende Guidelines bislang nicht vorliegen [@DCATAPDESpec3].

---

### `FitkoGovdata` — FITKO (2026)

**GovData**  
Typ: `misc`  
→ **[Quelle öffnen](https://www.fitko.de/produktmanagement/govdata)**  
Zugriff: 2026-04-20  

7 Fundstellen.

**Kap. 1 — Einleitung**

- [ ] `contents.tex:7` — Problemstellung und Motivation · gemeinsam mit [`govdata_portal`](https://www.govdata.de/) · [Web](https://www.fitko.de/produktmanagement/govdata)  
  > GovData fungiert als übergreifender Metadatenkatalog, über den Bund, Länder und Kommunen ihre offenen Datensätze auffindbar machen und einen zentralen Zugang zu Verwaltungsdaten bereitstellen [@govdata_portal, FitkoGovdata].

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:97` — Open Government Data und das GovData-Portal · [Web](https://www.fitko.de/produktmanagement/govdata)  
  > Die FITKO ordnet das Portal ihrem einheitlichen Produktmanagement-Modell für Produkte des IT-Planungsrats zu und verweist für GovData auf ein eigenes föderal besetztes Produktboard [@FitkoGovdata].

- [ ] `contents.tex:127` — Metadaten im Open-Data-Kontext · gemeinsam mit [`Riley2017MetadataPrimer`](https://www.niso.org/publications/understanding-metadata-2017) · [Web](https://www.fitko.de/produktmanagement/govdata)  
  > In funktionaler Hinsicht lassen sich die im GovData-Kontext verwendeten Metadaten vor allem als deskriptive und administrative Metadaten einordnen, da sie einerseits der Beschreibung und Auffindbarkeit von Verwaltungsdaten dienen und andererseits Informationen zur Bereitstellung, zu Formaten, zu offenen Lizenzen, und zur Nachnutzbarkeit enthalten [@Riley2017MetadataPrimer,FitkoGovdata].

- [ ] `contents.tex:128` — Metadaten im Open-Data-Kontext · [Web](https://www.fitko.de/produktmanagement/govdata)  
  > Da GovData selbst als nationales Metadatenportal fungiert, einen Metadatenkatalog bereitstellt, und die beschriebenen Verwaltungsdaten weiterhin dezentral bei den bereitstellenden Stellen verbleiben, kommt dieser Beschreibungsschicht eine zentrale infrastrukturelle Funktion zu [@FitkoGovdata].

- [ ] `contents.tex:134` — DCAT-AP.de als Metadatenstandard · [Web](https://www.fitko.de/produktmanagement/govdata)  
  > Diese Einbettung ist insbesondere deshalb relevant, weil Metadaten im GovData-Kontext nicht nur innerhalb Deutschlands ausgetauscht, sondern zugleich an europäische Entwicklungen anschlussfähig bleiben sollen [@FitkoGovdata].

- [ ] `contents.tex:136` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`FITKOGovDataDocs`](https://docs.fitko.de/resources/govdata/) · [Web](https://www.fitko.de/produktmanagement/govdata)  
  > Die Qualität und Standardkonformität der Metadaten ist damit eine zentrale Voraussetzung dafür, dass Datensätze portalübergreifend auffindbar, maschinell verarbeitbar und interoperabel nachnutzbar werden [@FitkoGovdata, FITKOGovDataDocs].

- [ ] `contents.tex:233` — RDF, Linked Data und SHACL · [Web](https://www.fitko.de/produktmanagement/govdata)  
  > Dies gilt insbesondere im GovData-Kontext, in dem Metadaten nicht nur formal korrekt, sondern auch für die zentrale Auffindbarkeit und Nachnutzung dezentral bereitgestellter Verwaltungsdaten geeignet sein müssen [@FitkoGovdata].

---

### `W3CDCAT3` — World Wide Web Consortium (2024)

**Data Catalog Vocabulary (DCAT) -- Version 3**  
Institution: W3C · Typ: `techreport`  
→ **[Quelle öffnen](https://www.w3.org/TR/vocab-dcat-3/)**  

6 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:125` — Metadaten im Open-Data-Kontext · [Web](https://www.w3.org/TR/vocab-dcat-3/)  
  > DCAT ist hierfür das zentrale W3C-Vokabular, das die interoperable Beschreibung von Datenkatalogen, Datensätzen, und Datendiensten im Web ermöglichen soll. [@W3CDCAT3]

- [ ] `contents.tex:222` — RDF, Linked Data und SHACL · [Web](https://www.w3.org/TR/vocab-dcat-3/)  
  > Es soll die Interoperabilität zwischen im Web veröffentlichten Datenkatalogen erleichtern, die Aggregation von Metadaten aus mehreren Katalogen unterstützen, die Auffindbarkeit von Datensätzen erhöhen, und föderierte Suche über verschiedene Kataloge hinweg ermöglichen. [@W3CDCAT3]

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:818` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [Web](https://www.w3.org/TR/vocab-dcat-3/)  
  > K6 & Interoperabilität und Linked-Data-Qualität & Literatur zu FAIR, Linked Data, RDF-Grundlagen, DCAT und Linked-Data-Qualität nach [@wilkinson2016fair, W3CRDF11Concepts, W3CDCAT3, Zaveri2016LinkedDataQuality, Gayo2015LinkedDataValidationQuality]. & Bewertung, ob Metadaten über URIs, Normdaten, kontrollierte Vokabulare und Graphbezüge interoperabel und verknüpfbar sind.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1247` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Bewertungsebene und Aggregation über Distributionen · Locator: `Abschnitt~12.3` · [Web](https://www.w3.org/TR/vocab-dcat-3/)  
  > Erst mit DCAT 3 wurde für diesen Fall die eigene Klasse dcat:DatasetSeries eingeführt [@W3CDCAT3].

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:39` — (Kapiteleinleitung) · [Web](https://www.w3.org/TR/vocab-dcat-3/)  
  > Nr. 3 (Auffindbarkeit und Identifizierbarkeit) — belegter Ausdruck: „DCAT-Identifikatoren und Katalogmodell“

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — (Kapiteleinleitung) · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/) · [Web](https://www.w3.org/TR/vocab-dcat-3/)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „RDF-/DCAT-basierte Katalogbeschreibung“

---

### `wand1996anchoring` — Wand & Wang (1996)

**Anchoring Data Quality Dimensions in Ontological Foundations**  
in: Communications of the ACM · Typ: `article`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  

6 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:256` — Datenqualität › Definition nach Wang and Strong 1996 · [Suche](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > Ergänzend zu diesem nutzungsbezogenen Rahmen schlagen Wand und Wang eine ontologische Fundierung von Datenqualität vor [@wand1996anchoring].

- [ ] `contents.tex:256` — Datenqualität › Definition nach Wang and Strong 1996 · [Suche](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > Datenqualitätsprobleme lassen sich dann als Repräsentationsdefizite zwischen der beobachtbaren realen Welt und ihrer Abbildung im Informationssystem beschreiben [@wand1996anchoring].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:814` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [Suche](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > K4 & Semantische und inhaltliche Qualität & Forschungsfrage zu KI-gestützten Analyseverfahren; Literatur zu Verständlichkeit, Accuracy, semantischer Konsistenz und Qualität von Freitextfeldern nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata]. & Ergänzung formaler Prüfungen um Aussagekraft, Verständlichkeit, Plausibilität und inhaltliche Passung.

- [ ] `contents.tex:820` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [Suche](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > K7 & Kontextsensitivität und Fit for Purpose & Forschungsfrage zur praxisrelevanten Bewertung; Literatur zu Fit for Purpose, Kontextualität, FAIR-Nachnutzung und domänenspezifischer Datenqualität nach [@wang1996beyond, StrongLeeWang1997, wand1996anchoring, wilkinson2016fair, Ubaldi2013OGD]. & Anpassung von Bewertung, Gewichtung und Interpretation an Nutzungskontext, Domäne und Stakeholderperspektive.

- [ ] `contents.tex:822` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [Suche](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > K8 & Rohdatenbezug und Metadaten-Daten-Kongruenz & Forschungsfrage zur Kombination formaler Validierung mit kontextbezogenen Prüfverfahren; Leitfadenblock „Relevanz des eigentlichen Datensatzes“; Literatur zu Accuracy und Daten-Metadaten-Konsistenz nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, noguerasiso_quality_metadata]. & Prüfung, ob Metadaten mit der tatsächlichen Ressource übereinstimmen und ob Rohdaten zur Plausibilisierung herangezogen werden können.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:79` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)  
  > Nr. 11 (Inhaltliche Plausibilität und semantische Konsistenz) — belegter Ausdruck: „ontologische Repräsentationsdefizite“

---

### `bydata2025handreichung` — oc.bydata -- open bydata competence c… (2025)

**Handreichung zur Verbesserung der Metadatenqualität von offenen Daten**  
Anm.: Stand 12/2025, herausgegeben von der byte -- Bayerische Agentur für Digitales GmbH · Typ: `online`  
→ **[Quelle öffnen](https://open.bydata.de/)**  
Zugriff: 2026-07-06  

5 Fundstellen.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1283` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Herleitungsnachweis der Indikatoren · _Tabelle_ · [Web](https://open.bydata.de/)  
  > [H] 1.2 1whitewhite p0.12 p0.55 p0.10 Kurzzeichen & Quelle der Anforderung & Referenz SPEC & DCAT-AP.de-Spezifikation & [@DCATAPDESpec3] KONV xx & Konvention xx des DCAT-AP.de-Konventionenhandbuchs & [@DCATAPDEImplRules2] MQA & Metrik des Metadata Quality Assessment & [@data_europa, wentzel2023extensive] NEU & Metrik nach Neumaier et al. & [@Neumaier2016MetadataQuality] ZAV & Metrik nach Zaveri et al. & [@Zaveri2016LinkedDataQuality] FAIR & FAIR-Prinzipien & [@wilkinson2016fair] HMQ & Handreichung zur Verbesserung der Metadatenqualität von offenen Daten & [@bydata2025handreichung] INT-Kx & Interviewkategorie Kx & Tabelle [tab:zentrale_interviewergebnisse] Kurzzeichen der Herleitungssignale in den Indikatortabellen

- [ ] `contents.tex:1390` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Aussagekraftsindikatoren · gemeinsam mit [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/) · [Web](https://open.bydata.de/)  
  > Erstens werden die Bewertungskriterien nicht frei definiert, sondern aus den Qualitätsanforderungen des DCAT-AP.de-Konventionenhandbuchs sowie der Handreichung zur Verbesserung der Metadatenqualität von offenen Daten abgeleitet [@DCATAPDEImplRules2, bydata2025handreichung].

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1680` — Implementierung der Einzelindikatoren › Auffindbarkeitsindikatoren · [Web](https://open.bydata.de/)  
  > Die Schlagwortspanne von 3 bis 15 ist direkt aus der Handreichung zur Verbesserung der Metadatenqualität des open bydata competence center übernommen, die für einen Datensatz mindestens drei relevante Schlagwörter empfiehlt und je nach Dateninhalt maximal 15 Begriffe als ausreichend ansieht [@bydata2025handreichung].

- [ ] `contents.tex:1843` — LLM-gestützte Bewertung der Aussagekraft › Eingabe und Prompt · gemeinsam mit [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/) · [Web](https://open.bydata.de/)  
  > Sie enthält die schrittweise Vorgehensweise je Kriterium, die aus dem DCAT-AP.de-Konventionenhandbuch v2.0 (Kapitel 1.7 und 3.4) sowie der Handreichung zur Verbesserung der Metadatenqualität abgeleiteten Bewertungsregeln [@DCATAPDEImplRules2, bydata2025handreichung] und eine Ankerskala, die Wertebereiche verbal an Qualitätsniveaus bindet.

- [ ] `contents.tex:1934` — Scoring-, Gewichtungs- und Aggregationslogik › Gewichtung der Indikatoren und Dimensionen · [Web](https://open.bydata.de/)  
  > Sind Titel, Beschreibung und Schlagwörter nichtssagend, bleibt der Datensatz für Nutzende unverständlich, auch wenn die Metadaten vollständig sind, worauf auch die Handreichung zur Verbesserung der Metadatenqualität ihren Schwerpunkt legt [@bydata2025handreichung].

---

### `kubler2018comparison` — Kubler et al. (2018)

**Comparison of Metadata Quality in Open Data Portals Using the Analytic Hierarchy Process**  
in: Government Information Quarterly · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1016/j.giq.2017.11.003)**  

5 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:504` — Metadatenqualität und Qualitätsbewertung von Linked Data › Gewichtung und Ranking von Open-Data-Portalen nach Kubler et al. · [DOI](https://doi.org/10.1016/j.giq.2017.11.003)  
  > Kubler et al. beschreiben die Bewertung von Open-Data-Portalen als Multi-Criteria Decision Making Problem und entwickeln mit dem Open Data Portal Quality Framework einen Ansatz, der automatisiert berechnete Qualitätsindikatoren mit nutzerspezifischen Präferenzen verbindet [@kubler2018comparison].

- [ ] `contents.tex:513` — Metadatenqualität und Qualitätsbewertung von Linked Data › Gewichtung und Ranking von Open-Data-Portalen nach Kubler et al. · [DOI](https://doi.org/10.1016/j.giq.2017.11.003)  
  > Die Rangordnung der Portale ergibt sich anschließend aus der Kombination der verfügbaren Qualitätswerte mit den gesetzten Präferenzen. [@kubler2018comparison]

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:816` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17) · [DOI](https://doi.org/10.1016/j.giq.2017.11.003)  
  > K5 & Technische Zugänglichkeit, Aktualität und Nutzbarkeit & Literatur zu Accessibility, Retrievability, Open Data Fitness und MQA/Piveau nach [@wilkinson2016fair, data_europa, Neumaier2016MetadataQuality, kubler2018comparison, wentzel2023extensive]. & Bewertung, ob Ressourcen erreichbar, technisch nutzbar, aktuell genug und praktisch weiterverarbeitbar sind.

- [ ] `contents.tex:824` — Auswertungsverfahren der Interviews · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`W3CDQV`](https://www.w3.org/TR/vocab-dqv/), [`ISO19157`](https://www.iso.org/standard/78900.html) · [DOI](https://doi.org/10.1016/j.giq.2017.11.003)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1877` — Scoring-, Gewichtungs- und Aggregationslogik › Punktevergabe je Indikator · [DOI](https://doi.org/10.1016/j.giq.2017.11.003)  
  > Kubler et al. zeigen mit ihrem AHP-basierten Ansatz zudem, dass Qualitätsgewichte grundsätzlich präferenzabhängig sind und je nach Stakeholderperspektive unterschiedlich ausfallen [@kubler2018comparison].

---

### `StrongLeeWang1997` — Strong et al. (1997)

**Data quality in context**  
in: Communications of the ACM · Typ: `article`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=Data+quality+in+context)  

5 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:254` — Datenqualität › Definition nach Wang and Strong 1996 · [Suche](https://scholar.google.com/scholar?q=Data+quality+in+context)  
  > Diese Perspektive wurde von Strong, Lee, und Wang weiter ausgebaut, die betonen, dass Datenqualitätsprobleme nicht nur in gespeicherten Daten selbst entstehen, sondern im weiteren Kontext von Informationssystemen, also auch in Produktions-, Speicher-, und Nutzungskontexten [@StrongLeeWang1997].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:814` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [Suche](https://scholar.google.com/scholar?q=Data+quality+in+context)  
  > K4 & Semantische und inhaltliche Qualität & Forschungsfrage zu KI-gestützten Analyseverfahren; Literatur zu Verständlichkeit, Accuracy, semantischer Konsistenz und Qualität von Freitextfeldern nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, Zaveri2016LinkedDataQuality, noguerasiso_quality_metadata]. & Ergänzung formaler Prüfungen um Aussagekraft, Verständlichkeit, Plausibilität und inhaltliche Passung.

- [ ] `contents.tex:820` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [Suche](https://scholar.google.com/scholar?q=Data+quality+in+context)  
  > K7 & Kontextsensitivität und Fit for Purpose & Forschungsfrage zur praxisrelevanten Bewertung; Literatur zu Fit for Purpose, Kontextualität, FAIR-Nachnutzung und domänenspezifischer Datenqualität nach [@wang1996beyond, StrongLeeWang1997, wand1996anchoring, wilkinson2016fair, Ubaldi2013OGD]. & Anpassung von Bewertung, Gewichtung und Interpretation an Nutzungskontext, Domäne und Stakeholderperspektive.

- [ ] `contents.tex:822` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`noguerasiso_quality_metadata`](https://doi.org/10.1109/ACCESS.2021.3073455) · [Suche](https://scholar.google.com/scholar?q=Data+quality+in+context)  
  > K8 & Rohdatenbezug und Metadaten-Daten-Kongruenz & Forschungsfrage zur Kombination formaler Validierung mit kontextbezogenen Prüfverfahren; Leitfadenblock „Relevanz des eigentlichen Datensatzes“; Literatur zu Accuracy und Daten-Metadaten-Konsistenz nach [@wang1996beyond, wand1996anchoring, StrongLeeWang1997, noguerasiso_quality_metadata]. & Prüfung, ob Metadaten mit der tatsächlichen Ressource übereinstimmen und ob Rohdaten zur Plausibilisierung herangezogen werden können.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:99` — (Kapiteleinleitung) · [Suche](https://scholar.google.com/scholar?q=Data+quality+in+context)  
  > Nr. 15 (Nutzungsrelevanz und Fit for Purpose) — belegter Ausdruck: „Datenqualität im Nutzungskontext“

---

### `Ubaldi2013OGD` — Ubaldi (2013)

**Open Government Data: Towards Empirical Analysis of Open Government Data Initiatives**  
Institution: OECD Publishing · Typ: `techreport`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1787/5k46bj4f03s7-en)**  
Zusatz-URL: <https://dx.doi.org/10.1787/5k46bj4f03s7-en>  

5 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:90` — Open Government Data und das GovData-Portal · gemeinsam mit [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en) · [DOI](https://doi.org/10.1787/5k46bj4f03s7-en)  
  > OGD ist damit mehr als die bloße Veröffentlichung staatlicher Informationen im Internet; gemeint ist die proaktive Bereitstellung wiederverwendbarer Datenbestände des öffentlichen Sektors. [@Ubaldi2013OGD, OECD2020OURdata]

- [ ] `contents.tex:92` — Open Government Data und das GovData-Portal · gemeinsam mit [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en) · [DOI](https://doi.org/10.1787/5k46bj4f03s7-en)  
  > Ihre Relevanz ergibt sich damit aus der Verbindung von politischer Offenheit, technischer Nachnutzbarkeit, und gesellschaftlicher Wertschöpfung. [@Ubaldi2013OGD, OECD2020OURdata]

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:820` — Auswertungsverfahren der Interviews · gemeinsam mit [`wang1996beyond`](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers), [`StrongLeeWang1997`](https://scholar.google.com/scholar?q=Data+quality+in+context), [`wand1996anchoring`](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18) · [DOI](https://doi.org/10.1787/5k46bj4f03s7-en)  
  > K7 & Kontextsensitivität und Fit for Purpose & Forschungsfrage zur praxisrelevanten Bewertung; Literatur zu Fit for Purpose, Kontextualität, FAIR-Nachnutzung und domänenspezifischer Datenqualität nach [@wang1996beyond, StrongLeeWang1997, wand1996anchoring, wilkinson2016fair, Ubaldi2013OGD]. & Anpassung von Bewertung, Gewichtung und Interpretation an Nutzungskontext, Domäne und Stakeholderperspektive.

- [ ] `contents.tex:1045` — Zielgruppen des Bewertungsmodells · gemeinsam mit [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en) · [DOI](https://doi.org/10.1787/5k46bj4f03s7-en)  
  > Diese Dreiteilung folgt der in Kapitel 2 eingeführten Definition offener Daten, die Bereitstellung und Nachnutzung als zwei Seiten desselben Vorgangs begreift [@Ubaldi2013OGD, OECD2020OURdata], und deckt sich mit der Auswahl der Interviewpartner, die sowohl die Perspektive des GovData-Produktmanagements und der Standardisierung als auch die der praktischen Datenbereitstellung abdecken (Abschnitt [sec:interviews_ziel_auswahl]).

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1932` — Scoring-, Gewichtungs- und Aggregationslogik › Gewichtung der Indikatoren und Dimensionen · gemeinsam mit [`OECD2020OURdata`](https://doi.org/10.1787/45f6de2d-en) · [DOI](https://doi.org/10.1787/5k46bj4f03s7-en)  
  > Bereitstellung ohne Zugangsbeschränkungen unter Bedingungen, die die Wiederverwendung erlauben [@Ubaldi2013OGD, OECD2020OURdata].

---

### `W3CRDF11Concepts` — World Wide Web Consortium (2014)

**RDF 1.1 Concepts and Abstract Syntax**  
Institution: W3C · Typ: `techreport`  
→ **[Quelle öffnen](https://www.w3.org/TR/rdf11-concepts/)**  
Zugriff: 2026-04-21  

5 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:214` — RDF, Linked Data und SHACL · [Web](https://www.w3.org/TR/rdf11-concepts/)  
  > RDF ist damit nicht primär als konkretes Dateiformat zu verstehen, sondern als abstraktes Datenmodell, auf dem unterschiedliche RDF-basierte Sprachen und Serialisierungen aufbauen. [@W3CRDF11Concepts]

- [ ] `contents.tex:219` — RDF, Linked Data und SHACL · gemeinsam mit [`w3c_sparql11_query`](https://www.w3.org/TR/sparql11-query/) · [Web](https://www.w3.org/TR/rdf11-concepts/)  
  > SPARQL ist die standardisierte Abfragesprache für RDF-Daten und ermöglicht es, RDF-Graphen beziehungsweise RDF-Datenbestände über Graphmuster zu durchsuchen und auszuwerten [@W3CRDF11Concepts,w3c_sparql11_query].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:812` — Auswertungsverfahren der Interviews · gemeinsam mit [`W3CSHACL`](https://www.w3.org/TR/shacl/), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [Web](https://www.w3.org/TR/rdf11-concepts/)  
  > K3 & Formale und syntaktische Qualität & Forschungsfrage zur Integration von RDF-/SHACL-Prüfungen; Literatur zu Conformance, syntaktischer Validität und DCAT-AP.de-Konformität nach [@W3CRDF11Concepts, W3CSHACL, DCATAPDESpec2, DCATAPDESpec3, DCATAPDEImplRules2, Gayo2015LinkedDataValidationQuality]. & Erfassung regelbasierter, automatisierbarer Fehler über SHACL, XML/RDF, URI-, Vokabular- und Datentypprüfungen.

- [ ] `contents.tex:818` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [Web](https://www.w3.org/TR/rdf11-concepts/)  
  > K6 & Interoperabilität und Linked-Data-Qualität & Literatur zu FAIR, Linked Data, RDF-Grundlagen, DCAT und Linked-Data-Qualität nach [@wilkinson2016fair, W3CRDF11Concepts, W3CDCAT3, Zaveri2016LinkedDataQuality, Gayo2015LinkedDataValidationQuality]. & Bewertung, ob Metadaten über URIs, Normdaten, kontrollierte Vokabulare und Graphbezüge interoperabel und verknüpfbar sind.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — (Kapiteleinleitung) · gemeinsam mit [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/) · [Web](https://www.w3.org/TR/rdf11-concepts/)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „RDF-/DCAT-basierte Katalogbeschreibung“

---

### `DCATAPDESpec2` — DCAT-AP.de (2022)

**DCAT-AP.de Spezifikation 2.0**  
Typ: `online`  
→ **[Quelle öffnen](https://www.dcat-ap.de/def/dcatde/2.0/spec/)**  
Zugriff: 2026-04-21  

4 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:132` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/spec/)  
  > Sein Zweck liegt insbesondere darin, Metadaten offener Verwaltungsdaten zwischen deutschen Open-Data-Portalen interoperabel auszutauschen und diese Daten über GovData zentral auffindbar zu machen [@DCATAPDESpec3,DCATAPDESpec2].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:810` — Auswertungsverfahren der Interviews · gemeinsam mit [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/spec/)  
  > K2 & Vollständigkeit, Reichhaltigkeit und Feldrelevanz & Leitfadenfrage zu Qualitätsmerkmalen; Literatur zu Vollständigkeit nach [@wentzel2023extensive, wilkinson2016fair, DCATAPDESpec2, DCATAPDESpec3]. & Bestimmung, welche Metadatenfelder für einen Score geprüft und wie Pflicht-, empfohlene und optionale Angaben gewichtet werden.

- [ ] `contents.tex:812` — Auswertungsverfahren der Interviews · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CSHACL`](https://www.w3.org/TR/shacl/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/spec/)  
  > K3 & Formale und syntaktische Qualität & Forschungsfrage zur Integration von RDF-/SHACL-Prüfungen; Literatur zu Conformance, syntaktischer Validität und DCAT-AP.de-Konformität nach [@W3CRDF11Concepts, W3CSHACL, DCATAPDESpec2, DCATAPDESpec3, DCATAPDEImplRules2, Gayo2015LinkedDataValidationQuality]. & Erfassung regelbasierter, automatisierbarer Fehler über SHACL, XML/RDF, URI-, Vokabular- und Datentypprüfungen.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1773` — Implementierung der Einzelindikatoren › Nachnutzbarkeitsindikatoren · gemeinsam mit [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/) · [Web](https://www.dcat-ap.de/def/dcatde/2.0/spec/)  
  > Diese Version bildet ein vollständig abgeschlossenes Profil, das neben der Spezifikation auch ein zugehöriges Konventionenhandbuch bereitstellt [@DCATAPDESpec2, DCATAPDEImplRules2] und damit die Grundlage des in Kapitel 4 abgeleiteten Bewertungsmodells bildet.

---

### `Gayo2015LinkedDataValidationQuality` — Jose Emilio Labra Gayo (2015)

**Linked Data Validation and Quality**  
Institution: European Public Sector Information Platform · Typ: `techreport`  
→ **[Quelle öffnen](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf)**  

4 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:231` — RDF, Linked Data und SHACL · gemeinsam mit [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175) · [Web](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf)  
  > In der Literatur zu Linked Data und Metadatenqualität wird Validierung zwar als zentraler Bestandteil der Qualitätsprüfung betrachtet, zugleich aber betont, dass darüber hinaus weitere Qualitätsdimensionen wie Vollständigkeit, Auffindbarkeit, Genauigkeit, oder Nachnutzbarkeit relevant sind [@Gayo2015LinkedDataValidationQuality,Neumaier2016MetadataQuality,Zaveri2016LinkedDataQuality].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:812` — Auswertungsverfahren der Interviews · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CSHACL`](https://www.w3.org/TR/shacl/), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/) · [Web](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf)  
  > K3 & Formale und syntaktische Qualität & Forschungsfrage zur Integration von RDF-/SHACL-Prüfungen; Literatur zu Conformance, syntaktischer Validität und DCAT-AP.de-Konformität nach [@W3CRDF11Concepts, W3CSHACL, DCATAPDESpec2, DCATAPDESpec3, DCATAPDEImplRules2, Gayo2015LinkedDataValidationQuality]. & Erfassung regelbasierter, automatisierbarer Fehler über SHACL, XML/RDF, URI-, Vokabular- und Datentypprüfungen.

- [ ] `contents.tex:818` — Auswertungsverfahren der Interviews · gemeinsam mit [`wilkinson2016fair`](https://doi.org/10.1038/sdata.2016.18), [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`W3CDCAT3`](https://www.w3.org/TR/vocab-dcat-3/), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175) · [Web](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf)  
  > K6 & Interoperabilität und Linked-Data-Qualität & Literatur zu FAIR, Linked Data, RDF-Grundlagen, DCAT und Linked-Data-Qualität nach [@wilkinson2016fair, W3CRDF11Concepts, W3CDCAT3, Zaveri2016LinkedDataQuality, Gayo2015LinkedDataValidationQuality]. & Bewertung, ob Metadaten über URIs, Normdaten, kontrollierte Vokabulare und Graphbezüge interoperabel und verknüpfbar sind.

- [ ] `contents.tex:826` — Auswertungsverfahren der Interviews · gemeinsam mit [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`corteslasalle_shacl_dqa`](https://doi.org/10.48550/arXiv.2507.22305), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`BernersLee2006LinkedData`](https://www.w3.org/DesignIssues/LinkedData.html) · [Web](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf)  
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.

---

### `OECD2020OURdata` — OECD (2020)

**Open, Useful and Re-usable Data (OURdata) Index: 2019**  
Institution: OECD Publishing · Typ: `techreport`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1787/45f6de2d-en)**  
Zusatz-URL: <http://dx.doi.org/10.1787/45f6de2d-en>  

4 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:90` — Open Government Data und das GovData-Portal · gemeinsam mit [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [DOI](https://doi.org/10.1787/45f6de2d-en)  
  > OGD ist damit mehr als die bloße Veröffentlichung staatlicher Informationen im Internet; gemeint ist die proaktive Bereitstellung wiederverwendbarer Datenbestände des öffentlichen Sektors. [@Ubaldi2013OGD, OECD2020OURdata]

- [ ] `contents.tex:92` — Open Government Data und das GovData-Portal · gemeinsam mit [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [DOI](https://doi.org/10.1787/45f6de2d-en)  
  > Ihre Relevanz ergibt sich damit aus der Verbindung von politischer Offenheit, technischer Nachnutzbarkeit, und gesellschaftlicher Wertschöpfung. [@Ubaldi2013OGD, OECD2020OURdata]

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:1045` — Zielgruppen des Bewertungsmodells · gemeinsam mit [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [DOI](https://doi.org/10.1787/45f6de2d-en)  
  > Diese Dreiteilung folgt der in Kapitel 2 eingeführten Definition offener Daten, die Bereitstellung und Nachnutzung als zwei Seiten desselben Vorgangs begreift [@Ubaldi2013OGD, OECD2020OURdata], und deckt sich mit der Auswahl der Interviewpartner, die sowohl die Perspektive des GovData-Produktmanagements und der Standardisierung als auch die der praktischen Datenbereitstellung abdecken (Abschnitt [sec:interviews_ziel_auswahl]).

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1932` — Scoring-, Gewichtungs- und Aggregationslogik › Gewichtung der Indikatoren und Dimensionen · gemeinsam mit [`Ubaldi2013OGD`](https://doi.org/10.1787/5k46bj4f03s7-en) · [DOI](https://doi.org/10.1787/45f6de2d-en)  
  > Bereitstellung ohne Zugangsbeschränkungen unter Bedingungen, die die Wiederverwendung erlauben [@Ubaldi2013OGD, OECD2020OURdata].

---

### `W3CSHACL` — World Wide Web Consortium (2017)

**Shapes Constraint Language (SHACL)**  
Institution: W3C · Typ: `techreport`  
→ **[Quelle öffnen](https://www.w3.org/TR/shacl/)**  
Zugriff: 2026-04-21  

4 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:227` — RDF, Linked Data und SHACL · [Web](https://www.w3.org/TR/shacl/)  
  > SHACL ermöglicht somit die formale Überprüfung, ob ein RDF-Datenbestand vorgegebene strukturelle und syntaktische Anforderungen erfüllt. [@W3CSHACL]

- [ ] `contents.tex:230` — RDF, Linked Data und SHACL · [Web](https://www.w3.org/TR/shacl/)  
  > SHACL dient der Prüfung von RDF-Graphen gegen formal definierte Constraints und erlaubt damit insbesondere Aussagen über strukturelle und syntaktische Konformität [@W3CSHACL].

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:812` — Auswertungsverfahren der Interviews · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/), [`DCATAPDESpec2`](https://www.dcat-ap.de/def/dcatde/2.0/spec/), [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/), [`DCATAPDEImplRules2`](https://www.dcat-ap.de/def/dcatde/2.0/implRules/), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf) · [Web](https://www.w3.org/TR/shacl/)  
  > K3 & Formale und syntaktische Qualität & Forschungsfrage zur Integration von RDF-/SHACL-Prüfungen; Literatur zu Conformance, syntaktischer Validität und DCAT-AP.de-Konformität nach [@W3CRDF11Concepts, W3CSHACL, DCATAPDESpec2, DCATAPDESpec3, DCATAPDEImplRules2, Gayo2015LinkedDataValidationQuality]. & Erfassung regelbasierter, automatisierbarer Fehler über SHACL, XML/RDF, URI-, Vokabular- und Datentypprüfungen.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:29` — (Kapiteleinleitung) · [Web](https://www.w3.org/TR/shacl/)  
  > Nr. 1 (Formale und syntaktische Konformität) — belegter Ausdruck: „SHACL-Constraints für Kardinalitäten, Datentypen, Klassen, Properties und Wertebereiche“

---

### `piveauMetricsV2` — piveau (2026)

**Metrics v2: Scoring Methodology**  
Anm.: Vorabdokumentation einer noch nicht veröffentlichten Fassung · Typ: `online`  
→ **[Quelle öffnen](https://doc.piveau.eu/metrics/v2/scoring/)**  
Zugriff: 2026-09-07  

3 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:631` — Metadatenqualität und Qualitätsbewertung von Linked Data › Operationalisierung der Metadatenqualitätsbewertung durch MQA/Piveau · [Web](https://doc.piveau.eu/metrics/v2/scoring/)  
  > Dadurch operationalisiert MQA/Piveau Metadatenqualität primär über praktische Nutzbarkeit, technische Zugänglichkeit, strukturelle Interoperabilität und rechtliche Wiederverwendbarkeit. [@data_europa, wentzel2023extensive] Während der Bearbeitung dieser Arbeit wurde eine überarbeitete Fassung des Frameworks (Metrics v2) angekündigt und dokumentiert, jedoch noch nicht veröffentlicht [@piveauMetricsV2].

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2439` — Vergleichsbaseline: MQA-Reimplementierung und A/B/C-Klassifikation · [Web](https://doc.piveau.eu/metrics/v2/scoring/)  
  > Bemerkenswert ist, dass Metrics v2 zwei Konstruktionsentscheidungen dieses Modells nachträglich teilt, die hier gegenüber der MQA v1 eigens begründet wurden: die Mittelung über die Distributionen eines Datensatzes anstelle des Best-Distribution-Prinzips (Abschnitt [sec:messmodell]) und die Entkopplung der SHACL-Konformität vom eigentlichen Score, die hier als einzelner aggregierter Indikator geführt wird [@piveauMetricsV2].

**Kap. 7 — Schlussbetrachtung**

- [ ] `contents.tex:3749` — Ausblick › Weiterer Forschungs- und Entwicklungsbedarf · [Web](https://doc.piveau.eu/metrics/v2/scoring/)  
  > Schließlich legt die während der Bearbeitung angekündigte Fassung Metrics v2 einen erneuten Baseline-Vergleich nahe, sobald sie veröffentlicht und produktiv verfügbar ist [@piveauMetricsV2].

---

### `Riley2017MetadataPrimer` — Riley (2017)

**Understanding Metadata: What is Metadata, and What is it For? A Primer**  
Verlag: NISO · Typ: `book`  
→ **[Quelle öffnen](https://www.niso.org/publications/understanding-metadata-2017)**  

3 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:101` — Metadaten im Open-Data-Kontext · [Web](https://www.niso.org/publications/understanding-metadata-2017)  
  > Für Datensätze im Open-Data-Kontext bedeutet dies, dass Metadaten nicht bloß Begleitinformationen sind, sondern die Beschreibungsschicht, über die Datensätze gefunden, eingeordnet, und verwendet werden können. [@Riley2017MetadataPrimer]

- [ ] `contents.tex:120` — Metadaten im Open-Data-Kontext · _Unterschrift_ · [Web](https://www.niso.org/publications/understanding-metadata-2017)  
  > Markup-Metadaten & Kennzeichnen die logische oder semantische Struktur innerhalb eines digitalen Objekts. justification=centering Metadatentypen in Anlehnung an NISO, eigene Übersetzung und Paraphrase [@Riley2017MetadataPrimer]

- [ ] `contents.tex:127` — Metadaten im Open-Data-Kontext · gemeinsam mit [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata) · [Web](https://www.niso.org/publications/understanding-metadata-2017)  
  > In funktionaler Hinsicht lassen sich die im GovData-Kontext verwendeten Metadaten vor allem als deskriptive und administrative Metadaten einordnen, da sie einerseits der Beschreibung und Auffindbarkeit von Verwaltungsdaten dienen und andererseits Informationen zur Bereitstellung, zu Formaten, zu offenen Lizenzen, und zur Nachnutzbarkeit enthalten [@Riley2017MetadataPrimer,FitkoGovdata].

---

### `BernersLee2006LinkedData` — Berners-Lee (2006)

**Linked Data**  
Anm.: Design Issues · Typ: `misc`  
→ **[Quelle öffnen](https://www.w3.org/DesignIssues/LinkedData.html)**  
Zugriff: 2026-05-04  

2 Fundstellen.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:826` — Auswertungsverfahren der Interviews · gemeinsam mit [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`corteslasalle_shacl_dqa`](https://doi.org/10.48550/arXiv.2507.22305), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175) · [Web](https://www.w3.org/DesignIssues/LinkedData.html)  
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:54` — (Kapiteleinleitung) · [Web](https://www.w3.org/DesignIssues/LinkedData.html)  
  > Nr. 6 (Interoperabilität und Linked-Data-Reife) — belegter Ausdruck: „Linked-Data-Prinzipien“

---

### `BleiholderNaumann2008` — Bleiholder & Naumann (2008)

**Data Fusion**  
in: ACM Computing Surveys · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1145/1456650.1456651)**  

2 Fundstellen.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1248` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Bewertungsebene und Aggregation über Distributionen · [DOI](https://doi.org/10.1145/1456650.1456651)  
  > In der Terminologie der Datenintegration entspricht das Best-Distribution-Prinzip damit einer conflict-avoiding-Strategie, die einen bevorzugten Wert auswählt und übrige Werte unberücksichtigt lässt und dadurch Inkonsistenzen maskiert, statt sie sichtbar zu machen [@BleiholderNaumann2008].

- [ ] `contents.tex:1248` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Bewertungsebene und Aggregation über Distributionen · [DOI](https://doi.org/10.1145/1456650.1456651)  
  > Da das Ziel dieser Arbeit gerade die Aufdeckung und Meldung fehlerhafter Distributionen ist (Abschnitt [subsec:befund]), wählt das Bewertungsmodell stattdessen bewusst eine conflict-resolving-Strategie in Form der Mittelwertbildung [@BleiholderNaumann2008].

---

### `campbell1959convergent` — Campbell & Fiske (1959)

**Convergent and Discriminant Validation by the Multitrait-Multimethod Matrix**  
in: Psychological Bulletin · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1037/h0046016)**  

2 Fundstellen.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2262` — Evaluationsdesign und Hypothesen · [DOI](https://doi.org/10.1037/h0046016)  
  > Methodisch entspricht dies dem Nachweis konvergenter Validität [@campbell1959convergent].

- [ ] `contents.tex:2364` — Ground-Truth-Erhebung · [DOI](https://doi.org/10.1037/h0046016)  
  > Damit misst die Ground Truth dasselbe Konstrukt aus methodisch unabhängiger Perspektive, statt die Prüflogik des Prototyps manuell nachzuvollziehen [@campbell1959convergent].

---

### `DCATAPDEStart` — DCAT-AP.de (o. J.)

**DCAT-AP.de -- Start**  
Typ: `online`  
→ **[Quelle öffnen](https://www.dcat-ap.de/)**  
Zugriff: 2026-04-21  

2 Fundstellen.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:132` — DCAT-AP.de als Metadatenstandard · [Web](https://www.dcat-ap.de/)  
  > DCAT-AP.de ist das gemeinsame deutsche Metadatenmodell für den Austausch offener Verwaltungsdaten und dient dazu, Metadaten aus unterschiedlichen Portalen in einer einheitlichen Struktur bereitzustellen [@DCATAPDEStart].

- [ ] `contents.tex:134` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`DCATAPDESpec3`](https://www.dcat-ap.de/def/dcatde/3.0/spec/) · [Web](https://www.dcat-ap.de/)  
  > Damit steht der Standard in einem mehrstufigen Interoperabilitätszusammenhang: vom allgemeinen Modell für Datenkataloge im Web über das europäische Anwendungsprofil bis hin zur deutschen Spezifikation für offene Verwaltungsdaten [@DCATAPDEStart,DCATAPDESpec3].

---

### `govdata_portal` — FITKO (2024)

**GovData – Das Datenportal für Deutschland**  
Typ: `misc`  
→ **[Quelle öffnen](https://www.govdata.de/)**  
Zugriff: 2026-03-05  

2 Fundstellen.

**Kap. 1 — Einleitung**

- [ ] `contents.tex:7` — Problemstellung und Motivation · gemeinsam mit [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata) · [Web](https://www.govdata.de/)  
  > GovData fungiert als übergreifender Metadatenkatalog, über den Bund, Länder und Kommunen ihre offenen Datensätze auffindbar machen und einen zentralen Zugang zu Verwaltungsdaten bereitstellen [@govdata_portal, FitkoGovdata].

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:2107` — Menschenlesbares Qualitätsreporting › Einbettung in eine Portalumgebung · [Web](https://www.govdata.de/)  
  > Um dies zeigen zu können, ohne Zugriff auf ein produktiv betriebenes Portal zu haben, bildet der Prototyp die Oberfläche des GovData-Portals nach [@govdata_portal] und übernimmt dessen Gestaltungssystem und Seitenaufbau.

---

### `ISO19157` — International Organization for Standa… (2023)

**ISO 19157-1:2023 Geographic Information -- Data Quality -- Part 1: General Requirements**  
Organisation: International Organization for Standardization · Typ: `misc`  
→ **[Quelle öffnen](https://www.iso.org/standard/78900.html)**  
Zugriff: 2026-05-04  

2 Fundstellen.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:824` — Auswertungsverfahren der Interviews · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`W3CDQV`](https://www.w3.org/TR/vocab-dqv/) · [Web](https://www.iso.org/standard/78900.html)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

**Anhang — (ohne Kapitel)**

- [ ] `appendix/longlist_kandidatendimensionen.tex:89` — (Kapiteleinleitung) · [Web](https://www.iso.org/standard/78900.html)  
  > Nr. 13 (Räumliche und domänenspezifische Kontextqualität) — belegter Ausdruck: „ISO 19157 als geodatenbezogener Qualitätsrahmen“

---

### `nardo2008handbook` — Nardo et al. (2008)

**Handbook on Constructing Composite Indicators: Methodology and User Guide**  
Verlag: OECD Publishing · Typ: `book`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1787/9789264043466-en)**  

2 Fundstellen.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1877` — Scoring-, Gewichtungs- und Aggregationslogik › Punktevergabe je Indikator · [DOI](https://doi.org/10.1787/9789264043466-en)  
  > Die Literatur zu zusammengesetzten Indikatoren behandelt die Gewichts- und Punktwahl entsprechend als transparent zu dokumentierende Entwurfsentscheidung, die sich auf Experten- und Konstrukteursurteile stützt [@nardo2008handbook].

**Kap. 7 — Schlussbetrachtung**

- [ ] `contents.tex:3643` — Ergebnisdiskussion und Reflexion › Methodische Grenzen · [DOI](https://doi.org/10.1787/9789264043466-en)  
  > Dass auch etablierte Verfahren ihre Punktwerte per Konvention festlegen und die Literatur zu zusammengesetzten Indikatoren dies als dokumentationspflichtige Entwurfsentscheidung behandelt [@nardo2008handbook], entlastet die Setzung, hebt sie aber nicht auf.

---

### `piveauMetricsScore` — Piveau (o. J.)

**piveau-metrics-score: Scoring.kt**  
Anm.: Quellcode des MQA-Scoring-Dienstes, Commit df994a17 · Typ: `online`  
→ **[Quelle öffnen](https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt)**  
Zugriff: 2026-07-07  

2 Fundstellen.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1246` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Bewertungsebene und Aggregation über Distributionen · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en) · [Web](https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt)  
  > Bei mehreren Distributionen bestimmt die am besten bewertete Distribution das Ergebnis, unter der Annahme, dass alle Distributionen denselben Datensatz lediglich in unterschiedlichen Formaten repräsentieren [@data_europa, piveauMetricsScore].

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2426` — Vergleichsbaseline: MQA-Reimplementierung und A/B/C-Klassifikation · [Web](https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt)  
  > Wo die Methodik die Berechnung nicht abschließend festlegt, insbesondere bei der Behandlung mehrerer Distributionen, wurde die Logik ergänzend aus dem öffentlichen Quellcode des MQA-Scoring-Dienstes nachvollzogen [@piveauMetricsScore].

---

### `Basili1994GQM` — Basili et al. (1994)

**The Goal Question Metric Approach**  
in: Encyclopedia of Software Engineering · Verlag: John Wiley & Sons · Typ: `incollection`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=The+Goal+Question+Metric+Approach)  

1 Fundstelle.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1206` — Ableitung formaler, technischer und semantischer Einzelindikatoren · [Suche](https://scholar.google.com/scholar?q=The+Goal+Question+Metric+Approach)  
  > Die Auswahl der Indikatoren orientiert sich, am Goal-Question-Metric-Prinzip, nachdem Metriken top-down aus übergeordneten Zielen abgeleitet werden [@Basili1994GQM].

---

### `BmdsOpenData` — Bundesministerium für Digitales und S… (2026)

**Open Data**  
Typ: `misc`  
→ **[Quelle öffnen](https://bmds.bund.de/themen/digitale-wirtschaft/daten/open-data)**  
Zugriff: 2026-04-20  

1 Fundstelle.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:94` — Open Government Data und das GovData-Portal · [Web](https://bmds.bund.de/themen/digitale-wirtschaft/daten/open-data)  
  > GovData übernimmt damit vor allem eine Aggregations- und Sichtbarkeitsfunktion, indem verteilte Datenbestände über einen gemeinsamen Metadatenzugang auffindbar gemacht werden. [@BmdsOpenData]

---

### `byrt1993bias` — Byrt et al. (1993)

**Bias, Prevalence and Kappa**  
in: Journal of Clinical Epidemiology · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1016/0895-4356(93)90018-V)**  

1 Fundstelle.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2532` — Auswertungsverfahren und Kennzahlen · [DOI](https://doi.org/10.1016/0895-4356(93)90018-V)  
  > PABAK (Prevalence-Adjusted Bias-Adjusted Kappa) korrigiert zusätzlich um die Verzerrung durch die ungleiche Urteilsverteilung selbst [@byrt1993bias] und macht dadurch sichtbar, dass die niedrige -Punktschätzung hier ein Verteilungs- und kein Qualitätsbefund ist.

---

### `corteslasalle_shacl_dqa` — Lasalle et al. (2025)

**Is SHACL Suitable for Data Quality Assessment?**  
Typ: `inproceedings`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.48550/arXiv.2507.22305)**  

1 Fundstelle.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:826` — Auswertungsverfahren der Interviews · gemeinsam mit [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`Gayo2015LinkedDataValidationQuality`](https://data.europa.eu/sites/default/files/report/2015_linked_data_validation_and_quality.pdf), [`Zaveri2016LinkedDataQuality`](https://doi.org/10.3233/SW-150175), [`BernersLee2006LinkedData`](https://www.w3.org/DesignIssues/LinkedData.html) · [DOI](https://doi.org/10.48550/arXiv.2507.22305)  
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.

---

### `cronbach1955construct` — Cronbach & Meehl (1955)

**Construct Validity in Psychological Tests**  
in: Psychological Bulletin · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1037/h0040957)**  

1 Fundstelle.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2462` — Vergleichsbaseline: MQA-Reimplementierung und A/B/C-Klassifikation · [DOI](https://doi.org/10.1037/h0040957)  
  > Diese Partitionierung entspricht klassischen Validitätsbegriffen der Messtheorie [@cronbach1955construct]:

---

### `dataeuropa_dqguidelines` — data.europa.eu (2024)

**Data Quality Guidelines**  
Anm.: Publications Office of the European Union; Klassifikation maschinenlesbarer Dateitypen (Table~5) · Typ: `online`  
→ **[Quelle öffnen](https://op.europa.eu/webpub/op/data-quality-guidelines/en/)**  
Zugriff: 2026-07-08  

1 Fundstelle.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:1739` — Implementierung der Einzelindikatoren › Zugänglichkeitsindikatoren · [Web](https://op.europa.eu/webpub/op/data-quality-guidelines/en/)  
  > Die Stufenzuordnung von Z7 (maschinenlesbarer Zugriffsweg) orientiert sich an der Klassifikation maschinenlesbarer Dateitypen der Data Quality Guidelines von data.europa.eu [@dataeuropa_dqguidelines].

---

### `DresingPehl2018` — Dresing & Pehl (2018)

**Praxisbuch Interview, Transkription und Analyse: Anleitungen und Regelsysteme f{\"u}r qualitativ Forschende**  
Verlag: Eigenverlag · Typ: `book`  
→ **[Quelle öffnen](https://www.audiotranskription.de/wp-content/uploads/2020/11/Praxisbuch_08_01_web.pdf)**  

1 Fundstelle.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:750` — Experteninterviews: Ziel, Auswahl und Durchführung · [Web](https://www.audiotranskription.de/wp-content/uploads/2020/11/Praxisbuch_08_01_web.pdf)  
  > Die Transkription orientierte sich an einem inhaltlich-semantischen Transkriptionsverständnis nach Dresing und Pehl [@DresingPehl2018].

---

### `einhorn1971` — Einhorn (1971)

**Use of Nonlinear, Noncompensatory Models as a Function of Task and Amount of Information**  
in: Organizational Behavior and Human Performance · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1016/0030-5073(71)90002-X)**  

1 Fundstelle.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2404` — Ground-Truth-Erhebung · [DOI](https://doi.org/10.1016/0030-5073(71)90002-X)  
  > Diese Kombination stellt sicher, dass ein gravierender Mangel in nur einer Dimension, etwa eine unklare Lizenz bei ansonsten guten Metadaten, nicht einfach im Durchschnitt der übrigen drei Dimensionen verschwindet [@einhorn1971].

---

### `feinstein1990kappa` — Feinstein & Cicchetti (1990)

**High Agreement but Low Kappa: I. The Problems of Two Paradoxes**  
in: Journal of Clinical Epidemiology · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1016/0895-4356(90)90158-L)**  

1 Fundstelle.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2497` — Auswertungsverfahren und Kennzahlen · [DOI](https://doi.org/10.1016/0895-4356(90)90158-L)  
  > Das ist ein bekanntes Phänomen, das als Kappa-Paradox beschrieben ist [@feinstein1990kappa].

---

### `few2006dashboard` — Few (2006)

**Information Dashboard Design: The Effective Visual Communication of Data**  
Verlag: O'Reilly Media · Typ: `book`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=Information+Dashboard+Design%3A+The+Effective+Visual+Communication+of+Data)  

1 Fundstelle.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:2218` — Menschenlesbares Qualitätsreporting › Darstellung und Bedienung · [Suche](https://scholar.google.com/scholar?q=Information+Dashboard+Design%3A+The+Effective+Visual+Communication+of+Data)  
  > Die Zusammenstellung folgt dem für Übersichtsdarstellungen formulierten Grundsatz, die zur Beurteilung erforderlichen Größen gemeinsam und nach ihrem Informationswert geordnet zu zeigen, statt sie auf mehrere Ansichten zu verteilen [@few2006dashboard].

---

### `FITKOGovDataDocs` — FITKO (o. J.)

**GovData -- Föderales Entwicklungsportal**  
Typ: `online`  
→ **[Quelle öffnen](https://docs.fitko.de/resources/govdata/)**  
Zugriff: 2026-04-21  

1 Fundstelle.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:136` — DCAT-AP.de als Metadatenstandard · gemeinsam mit [`FitkoGovdata`](https://www.fitko.de/produktmanagement/govdata) · [Web](https://docs.fitko.de/resources/govdata/)  
  > Die Qualität und Standardkonformität der Metadaten ist damit eine zentrale Voraussetzung dafür, dass Datensätze portalübergreifend auffindbar, maschinell verarbeitbar und interoperabel nachnutzbar werden [@FitkoGovdata, FITKOGovDataDocs].

---

### `glaser1963` — Glaser (1963)

**Instructional Technology and the Measurement of Learning Outcomes: Some Questions**  
in: American Psychologist · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1037/h0049294)**  

1 Fundstelle.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2393` — Ground-Truth-Erhebung · [DOI](https://doi.org/10.1037/h0049294)  
  > Die Schwellen in Tabelle [tab:gt_gesamturteil] legen inhaltlich fest, was ein gutes, mittleres oder schlechtes Ergebnis trennt, unabhängig davon, wie sich die konkrete Stichprobe zufällig verteilt und orientieren sich an der kriteriumsorientierten Messung nach Glaser [@glaser1963].

---

### `iso25024` — International Organization for Standa… (2015)

**ISO/IEC 25024:2015 Systems and Software Engineering -- Systems and Software Quality Requirements and Evaluation (SQuaRE) -- Measurement of Data Quality**  
Organisation: International Organization for Standardization · Typ: `misc`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=ISO%2FIEC+25024%3A2015+Systems+and+Software+Engineering+--+Systems+and+Software+Quality+Requirements+and+Evaluation+%28SQuaRE%29+--+Measurement+of+Data+Quality)  

1 Fundstelle.

**Kap. 4 — Konzeption eines Metadatenqualitätsmodells**

- [ ] `contents.tex:1240` — Ableitung formaler, technischer und semantischer Einzelindikatoren › Konzeptionelles Messmodell › Ternäre und graduelle Indikatoren · gemeinsam mit [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model) · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25024%3A2015+Systems+and+Software+Engineering+--+Systems+and+Software+Quality+Requirements+and+Evaluation+%28SQuaRE%29+--+Measurement+of+Data+Quality)  
  > Die Norm ergänzt die Qualitätscharakteristiken aus ISO/IEC 25012 um konkrete Messfunktionen [@iso25024, iso25012].

---

### `Ji2023HallucinationSurvey` — Ji et al. (2023)

**Survey of Hallucination in Natural Language Generation**  
in: ACM Computing Surveys · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1145/3571730)**  

1 Fundstelle.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:1030` — Zentrale Ergebnisse der Interviews › Zusammenfassung der empirischen Modellanforderungen · [DOI](https://doi.org/10.1145/3571730)  
  > Generative KI kann halluzinieren [@Ji2023HallucinationSurvey] und neigt selbst bei identischer Eingabe zu schwer reproduzierbaren Urteilen [@Zheng2023LLMJudge], weshalb KI-gestützte Verfahren die Bewertung nur ergänzen und im Reporting gekennzeichnet sein sollen, während die Scoringlogik regelbasiert, dokumentiert und nachvollziehbar bleibt.

---

### `lnenicka2023` — Lnenicka et al. (2024)

**Identifying patterns and recommendations of and for sustainable open data initiatives: a benchmarking-driven analysis of open government data initiatives among European countries**  
in: Government Information Quarterly · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1016/j.giq.2023.101898)**  

1 Fundstelle.

**Kap. 1 — Einleitung**

- [ ] `contents.tex:5` — Problemstellung und Motivation · [DOI](https://doi.org/10.1016/j.giq.2023.101898)  
  > Offene Daten können dabei neue wirtschaftliche und gesellschaftliche Mehrwerte schaffen, indem sie Forschung, datenbasierte Anwendungen und evidenzbasierte Entscheidungsprozesse unterstützen [@lnenicka2023].

---

### `machado2009cvd` — Machado et al. (2009)

**A Physiologically-Based Model for Simulation of Color Vision Deficiency**  
in: IEEE Transactions on Visualization and Computer Graphics · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1109/TVCG.2009.113)**  

1 Fundstelle.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:2232` — Menschenlesbares Qualitätsreporting › Darstellung und Bedienung · [DOI](https://doi.org/10.1109/TVCG.2009.113)  
  > Ergänzend wurden die Diagrammfarben mit einem physiologisch begründeten Simulationsmodell für Farbfehlsichtigkeit [@machado2009cvd] auf ihre Unterscheidbarkeit geprüft.

---

### `Mayring2014` — Mayring (2014)

**Qualitative Content Analysis: Theoretical Foundation, Basic Procedures and Software Solution**  
Verlag: GESIS Leibniz Institute for the Social Sciences · Typ: `book`  
→ **[Quelle öffnen](https://www.ssoar.info/ssoar/handle/document/39517)**  

1 Fundstelle.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:779` — Auswertungsverfahren der Interviews · gemeinsam mit [`Mayring2015`](https://scholar.google.com/scholar?q=Qualitative+Inhaltsanalyse%3A+Grundlagen+und+Techniken) · [Web](https://www.ssoar.info/ssoar/handle/document/39517)  
  > Die Auswertung der Experteninterviews erfolgte mithilfe einer qualitativen Inhaltsanalyse in Anlehnung an Mayring [@Mayring2014, Mayring2015].

---

### `Mayring2015` — Mayring (2015)

**Qualitative Inhaltsanalyse: Grundlagen und Techniken**  
Verlag: Beltz · Typ: `book`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=Qualitative+Inhaltsanalyse%3A+Grundlagen+und+Techniken)  

1 Fundstelle.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:779` — Auswertungsverfahren der Interviews · gemeinsam mit [`Mayring2014`](https://www.ssoar.info/ssoar/handle/document/39517) · [Suche](https://scholar.google.com/scholar?q=Qualitative+Inhaltsanalyse%3A+Grundlagen+und+Techniken)  
  > Die Auswertung der Experteninterviews erfolgte mithilfe einer qualitativen Inhaltsanalyse in Anlehnung an Mayring [@Mayring2014, Mayring2015].

---

### `openrouter_rankings_classification` — OpenRouter (2026)

**AI Model Rankings -- Top models by task**  
Anm.: Rangliste der je Aufgabentyp meistgenutzten Modelle, gemessen am Anteil an den auf der Plattform abgerechneten Ausgaben. Die Seite wird fortlaufend aktualisiert; der angegebene Stand bezieht sich auf das Abrufdatum · Typ: `online`  
→ **[Quelle öffnen](https://openrouter.ai/rankings#task-spend)**  
Zugriff: 2026-07-16  

1 Fundstelle.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2662` — Modellauswahl für die LLM-gestützte Bewertung · [Web](https://openrouter.ai/rankings#task-spend)  
  > Die Plattform weist aus, welche Modelle je Aufgabentyp den größten Anteil der abgerechneten Nutzung auf sich vereinen, und die drei genannten Modelle führen dort die Kategorie der Klassifikationsaufgaben an [@openrouter_rankings_classification].

---

### `preston2000optimal` — Preston & Colman (2000)

**Optimal Number of Response Categories in Rating Scales: Reliability, Validity, Discriminating Power, and Respondent Preferences**  
in: Acta Psychologica · Typ: `article`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1016/S0001-6918(99)00050-5)**  

1 Fundstelle.

**Kap. 6 — Evaluation**

- [ ] `contents.tex:2319` — Ground-Truth-Erhebung · [DOI](https://doi.org/10.1016/S0001-6918(99)00050-5)  
  > Die Stufenzahl folgt dem Befund von Preston und Colman [@preston2000optimal], wonach Reliabilität, Validität und Diskriminierungsfähigkeit von Ratingskalen auf etwa fünf bis sieben Stufen zunehmen und vierstufige Skalen suboptimal sind.

---

### `shneiderman1996eyes` — Shneiderman (1996)

**The Eyes Have It: A Task by Data Type Taxonomy for Information Visualizations**  
in: Proceedings of the 1996 IEEE Symposium on Visual Languages · Verlag: IEEE Computer Society · Typ: `inproceedings`  
→ **[Quelle öffnen (DOI)](https://doi.org/10.1109/VL.1996.545307)**  

1 Fundstelle.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:2206` — Menschenlesbares Qualitätsreporting › Darstellung und Bedienung · [DOI](https://doi.org/10.1109/VL.1996.545307)  
  > Sie folgen dem Ordnungsprinzip Überblick zuerst, dann Filtern, dann Details auf Anforderung, das Shneiderman als Grundmuster informationsvisualisierender Oberflächen beschreibt [@shneiderman1996eyes]:

---

### `w3c_css_validator` — World Wide Web Consortium (2026)

**W3C CSS Validation Service**  
Typ: `online`  
→ **[Quelle öffnen](https://jigsaw.w3.org/css-validator/)**  
Zugriff: 2026-07-28  

1 Fundstelle.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:2140` — Menschenlesbares Qualitätsreporting › Vom Prüfergebnis zum Befund · gemeinsam mit [`w3c_nu_checker`](https://validator.w3.org/nu/) · [Web](https://jigsaw.w3.org/css-validator/)  
  > Die Auflistung der nicht bestandenen Prüfungen mit Fundstelle und, wo möglich, Quelltextbeleg orientiert sich damit an der Form, die die Konformitätsprüfdienste des W3C für Markup und Stylesheets etabliert haben [@w3c_nu_checker, w3c_css_validator]:

---

### `w3c_nu_checker` — World Wide Web Consortium (2026)

**The Nu Html Checker**  
Anm.: Konformitätsprüfdienst des W3C für HTML; Meldungsformat dokumentiert unter \url{https://github.com/validator/validator/wiki/Output-\%C2\%BB-JSON · Typ: `online`  
→ **[Quelle öffnen](https://validator.w3.org/nu/)**  
Zugriff: 2026-07-28  

1 Fundstelle.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:2140` — Menschenlesbares Qualitätsreporting › Vom Prüfergebnis zum Befund · gemeinsam mit [`w3c_css_validator`](https://jigsaw.w3.org/css-validator/) · [Web](https://validator.w3.org/nu/)  
  > Die Auflistung der nicht bestandenen Prüfungen mit Fundstelle und, wo möglich, Quelltextbeleg orientiert sich damit an der Form, die die Konformitätsprüfdienste des W3C für Markup und Stylesheets etabliert haben [@w3c_nu_checker, w3c_css_validator]:

---

### `w3c_sparql11_query` — World Wide Web Consortium (2013)

**SPARQL 1.1 Query Language**  
Institution: W3C · Typ: `techreport`  
→ **[Quelle öffnen](https://www.w3.org/TR/sparql11-query/)**  
Zugriff: 2026-05-06  

1 Fundstelle.

**Kap. 2 — Theoretische und konzeptionelle Grundlagen**

- [ ] `contents.tex:219` — RDF, Linked Data und SHACL · gemeinsam mit [`W3CRDF11Concepts`](https://www.w3.org/TR/rdf11-concepts/) · [Web](https://www.w3.org/TR/sparql11-query/)  
  > SPARQL ist die standardisierte Abfragesprache für RDF-Daten und ermöglicht es, RDF-Graphen beziehungsweise RDF-Datenbestände über Graphmuster zu durchsuchen und auszuwerten [@W3CRDF11Concepts,w3c_sparql11_query].

---

### `w3c_wcag22` — World Wide Web Consortium (2023)

**Web Content Accessibility Guidelines (WCAG) 2.2**  
Institution: W3C · Typ: `techreport`  
→ **[Quelle öffnen](https://www.w3.org/TR/WCAG22/)**  
Zugriff: 2026-07-28  

1 Fundstelle.

**Kap. 5 — Prototypische Operationalisierung**

- [ ] `contents.tex:2232` — Menschenlesbares Qualitätsreporting › Darstellung und Bedienung · [Web](https://www.w3.org/TR/WCAG22/)  
  > Für die Gestaltung gelten durchgängig zwei Regeln der Barrierefreiheit, die den Web Content Accessibility Guidelines entnommen sind [@w3c_wcag22].

---

### `W3CDQV` — Albertoni & Isaac (2016)

**Data on the Web Best Practices: Data Quality Vocabulary**  
Institution: World Wide Web Consortium · Typ: `techreport`  
→ **[Quelle öffnen](https://www.w3.org/TR/vocab-dqv/)**  
Zugriff: 2026-05-04  

1 Fundstelle.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:824` — Auswertungsverfahren der Interviews · gemeinsam mit [`data_europa`](https://data.europa.eu/mqa/methodology?locale=en), [`kubler2018comparison`](https://doi.org/10.1016/j.giq.2017.11.003), [`Neumaier2016MetadataQuality`](https://doi.org/10.1145/2964909), [`wentzel2023extensive`](https://doi.org/10.1007/978-3-031-41138-0_17), [`iso25012`](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model), [`ISO19157`](https://www.iso.org/standard/78900.html) · [Web](https://www.w3.org/TR/vocab-dqv/)  
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.

---

### `Zheng2023LLMJudge` — Zheng et al. (2023)

**Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena**  
in: Advances in Neural Information Processing Systems · Anm.: Datasets and Benchmarks Track · Typ: `inproceedings`  
→ kein Link hinterlegt — [auf Google Scholar suchen](https://scholar.google.com/scholar?q=Judging+LLM-as-a-Judge+with+MT-Bench+and+Chatbot+Arena)  

1 Fundstelle.

**Kap. 3 — Experteninterviews**

- [ ] `contents.tex:1030` — Zentrale Ergebnisse der Interviews › Zusammenfassung der empirischen Modellanforderungen · [Suche](https://scholar.google.com/scholar?q=Judging+LLM-as-a-Judge+with+MT-Bench+and+Chatbot+Arena)  
  > Generative KI kann halluzinieren [@Ji2023HallucinationSurvey] und neigt selbst bei identischer Eingabe zu schwer reproduzierbaren Urteilen [@Zheng2023LLMJudge], weshalb KI-gestützte Verfahren die Bewertung nur ergänzen und im Reporting gekennzeichnet sein sollen, während die Scoringlogik regelbasiert, dokumentiert und nachvollziehbar bleibt.

---

## D. Auffälligkeiten

### Nie zitiert

Diese Einträge stehen in der `.bib`, werden aber nirgends zitiert. Bei `biblatex` mit Standardeinstellung erscheinen sie nicht im Literaturverzeichnis — entweder verwenden oder entfernen.

- [ ] `jonsson2007rubrics` — Jonsson & Svingby (2007): The Use of Scoring Rubrics: Reliability, Validity and Educational Consequences — [DOI](https://doi.org/10.1016/j.edurev.2007.05.002)
- [ ] `openrouter_provider_routing` — OpenRouter (o. J.): Provider Routing -- OpenRouter Documentation — [Web](https://openrouter.ai/docs/features/provider-routing)

### Nur eine Fundstelle

Einmal zitierte Quellen tragen jeweils genau eine Aussage. Wenn diese Aussage nicht hält, fällt die Quelle ersatzlos weg — deshalb lohnt hier der genaueste Blick.

- [ ] `Basili1994GQM` — contents.tex:1206, Kap. 4 · [Suche](https://scholar.google.com/scholar?q=The+Goal+Question+Metric+Approach)
  > Die Auswahl der Indikatoren orientiert sich, am Goal-Question-Metric-Prinzip, nachdem Metriken top-down aus übergeordneten Zielen abgeleitet werden [@Basili1994GQM].
- [ ] `BmdsOpenData` — contents.tex:94, Kap. 2 · [Web](https://bmds.bund.de/themen/digitale-wirtschaft/daten/open-data)
  > GovData übernimmt damit vor allem eine Aggregations- und Sichtbarkeitsfunktion, indem verteilte Datenbestände über einen gemeinsamen Metadatenzugang auffindbar gemacht werden. [@BmdsOpenData]
- [ ] `byrt1993bias` — contents.tex:2532, Kap. 6 · [DOI](https://doi.org/10.1016/0895-4356(93)90018-V)
  > PABAK (Prevalence-Adjusted Bias-Adjusted Kappa) korrigiert zusätzlich um die Verzerrung durch die ungleiche Urteilsverteilung selbst [@byrt1993bias] und macht dadurch sichtbar, dass die niedrige -Punktschätzung hier ein Verteilungs- und kein Qualitätsbefund ist.
- [ ] `corteslasalle_shacl_dqa` — contents.tex:826, Kap. 3 · [DOI](https://doi.org/10.48550/arXiv.2507.22305)
  > K10 & KI-gestützte Analyseverfahren und Automatisierungsgrenzen & Forschungsfrage zu KI-basierter Unterstützung und agentenbasierten Ansätzen; Leitfadenblock „KI-gestützte Ansätze und AI Agents“; Literatur zu automatisierter Metadatenqualitätsbewertung, SHACL-gestützter Qualitätsprüfung und Grenzen regelbasierter beziehungsweise automatisierter Verfahren nach [@Neumaier2016MetadataQuality, wentzel2023extensive, corteslasalle_shacl_dqa, Gayo2015LinkedDataValidationQuality, Zaveri2016LinkedDataQuality, BernersLee2006LinkedData]. & Einordnung, welche Qualitätsaspekte durch KI unterstützt werden können und wo regelbasierte oder menschliche Bewertung notwendig bleibt.
- [ ] `cronbach1955construct` — contents.tex:2462, Kap. 6 · [DOI](https://doi.org/10.1037/h0040957)
  > Diese Partitionierung entspricht klassischen Validitätsbegriffen der Messtheorie [@cronbach1955construct]:
- [ ] `dataeuropa_dqguidelines` — contents.tex:1739, Kap. 5 · [Web](https://op.europa.eu/webpub/op/data-quality-guidelines/en/)
  > Die Stufenzuordnung von Z7 (maschinenlesbarer Zugriffsweg) orientiert sich an der Klassifikation maschinenlesbarer Dateitypen der Data Quality Guidelines von data.europa.eu [@dataeuropa_dqguidelines].
- [ ] `DresingPehl2018` — contents.tex:750, Kap. 3 · [Web](https://www.audiotranskription.de/wp-content/uploads/2020/11/Praxisbuch_08_01_web.pdf)
  > Die Transkription orientierte sich an einem inhaltlich-semantischen Transkriptionsverständnis nach Dresing und Pehl [@DresingPehl2018].
- [ ] `einhorn1971` — contents.tex:2404, Kap. 6 · [DOI](https://doi.org/10.1016/0030-5073(71)90002-X)
  > Diese Kombination stellt sicher, dass ein gravierender Mangel in nur einer Dimension, etwa eine unklare Lizenz bei ansonsten guten Metadaten, nicht einfach im Durchschnitt der übrigen drei Dimensionen verschwindet [@einhorn1971].
- [ ] `feinstein1990kappa` — contents.tex:2497, Kap. 6 · [DOI](https://doi.org/10.1016/0895-4356(90)90158-L)
  > Das ist ein bekanntes Phänomen, das als Kappa-Paradox beschrieben ist [@feinstein1990kappa].
- [ ] `few2006dashboard` — contents.tex:2218, Kap. 5 · [Suche](https://scholar.google.com/scholar?q=Information+Dashboard+Design%3A+The+Effective+Visual+Communication+of+Data)
  > Die Zusammenstellung folgt dem für Übersichtsdarstellungen formulierten Grundsatz, die zur Beurteilung erforderlichen Größen gemeinsam und nach ihrem Informationswert geordnet zu zeigen, statt sie auf mehrere Ansichten zu verteilen [@few2006dashboard].
- [ ] `FITKOGovDataDocs` — contents.tex:136, Kap. 2 · [Web](https://docs.fitko.de/resources/govdata/)
  > Die Qualität und Standardkonformität der Metadaten ist damit eine zentrale Voraussetzung dafür, dass Datensätze portalübergreifend auffindbar, maschinell verarbeitbar und interoperabel nachnutzbar werden [@FitkoGovdata, FITKOGovDataDocs].
- [ ] `glaser1963` — contents.tex:2393, Kap. 6 · [DOI](https://doi.org/10.1037/h0049294)
  > Die Schwellen in Tabelle [tab:gt_gesamturteil] legen inhaltlich fest, was ein gutes, mittleres oder schlechtes Ergebnis trennt, unabhängig davon, wie sich die konkrete Stichprobe zufällig verteilt und orientieren sich an der kriteriumsorientierten Messung nach Glaser [@glaser1963].
- [ ] `iso25024` — contents.tex:1240, Kap. 4 · [Suche](https://scholar.google.com/scholar?q=ISO%2FIEC+25024%3A2015+Systems+and+Software+Engineering+--+Systems+and+Software+Quality+Requirements+and+Evaluation+%28SQuaRE%29+--+Measurement+of+Data+Quality)
  > Die Norm ergänzt die Qualitätscharakteristiken aus ISO/IEC 25012 um konkrete Messfunktionen [@iso25024, iso25012].
- [ ] `Ji2023HallucinationSurvey` — contents.tex:1030, Kap. 3 · [DOI](https://doi.org/10.1145/3571730)
  > Generative KI kann halluzinieren [@Ji2023HallucinationSurvey] und neigt selbst bei identischer Eingabe zu schwer reproduzierbaren Urteilen [@Zheng2023LLMJudge], weshalb KI-gestützte Verfahren die Bewertung nur ergänzen und im Reporting gekennzeichnet sein sollen, während die Scoringlogik regelbasiert, dokumentiert und nachvollziehbar bleibt.
- [ ] `lnenicka2023` — contents.tex:5, Kap. 1 · [DOI](https://doi.org/10.1016/j.giq.2023.101898)
  > Offene Daten können dabei neue wirtschaftliche und gesellschaftliche Mehrwerte schaffen, indem sie Forschung, datenbasierte Anwendungen und evidenzbasierte Entscheidungsprozesse unterstützen [@lnenicka2023].
- [ ] `machado2009cvd` — contents.tex:2232, Kap. 5 · [DOI](https://doi.org/10.1109/TVCG.2009.113)
  > Ergänzend wurden die Diagrammfarben mit einem physiologisch begründeten Simulationsmodell für Farbfehlsichtigkeit [@machado2009cvd] auf ihre Unterscheidbarkeit geprüft.
- [ ] `Mayring2014` — contents.tex:779, Kap. 3 · [Web](https://www.ssoar.info/ssoar/handle/document/39517)
  > Die Auswertung der Experteninterviews erfolgte mithilfe einer qualitativen Inhaltsanalyse in Anlehnung an Mayring [@Mayring2014, Mayring2015].
- [ ] `Mayring2015` — contents.tex:779, Kap. 3 · [Suche](https://scholar.google.com/scholar?q=Qualitative+Inhaltsanalyse%3A+Grundlagen+und+Techniken)
  > Die Auswertung der Experteninterviews erfolgte mithilfe einer qualitativen Inhaltsanalyse in Anlehnung an Mayring [@Mayring2014, Mayring2015].
- [ ] `openrouter_rankings_classification` — contents.tex:2662, Kap. 6 · [Web](https://openrouter.ai/rankings#task-spend)
  > Die Plattform weist aus, welche Modelle je Aufgabentyp den größten Anteil der abgerechneten Nutzung auf sich vereinen, und die drei genannten Modelle führen dort die Kategorie der Klassifikationsaufgaben an [@openrouter_rankings_classification].
- [ ] `preston2000optimal` — contents.tex:2319, Kap. 6 · [DOI](https://doi.org/10.1016/S0001-6918(99)00050-5)
  > Die Stufenzahl folgt dem Befund von Preston und Colman [@preston2000optimal], wonach Reliabilität, Validität und Diskriminierungsfähigkeit von Ratingskalen auf etwa fünf bis sieben Stufen zunehmen und vierstufige Skalen suboptimal sind.
- [ ] `shneiderman1996eyes` — contents.tex:2206, Kap. 5 · [DOI](https://doi.org/10.1109/VL.1996.545307)
  > Sie folgen dem Ordnungsprinzip Überblick zuerst, dann Filtern, dann Details auf Anforderung, das Shneiderman als Grundmuster informationsvisualisierender Oberflächen beschreibt [@shneiderman1996eyes]:
- [ ] `w3c_css_validator` — contents.tex:2140, Kap. 5 · [Web](https://jigsaw.w3.org/css-validator/)
  > Die Auflistung der nicht bestandenen Prüfungen mit Fundstelle und, wo möglich, Quelltextbeleg orientiert sich damit an der Form, die die Konformitätsprüfdienste des W3C für Markup und Stylesheets etabliert haben [@w3c_nu_checker, w3c_css_validator]:
- [ ] `w3c_nu_checker` — contents.tex:2140, Kap. 5 · [Web](https://validator.w3.org/nu/)
  > Die Auflistung der nicht bestandenen Prüfungen mit Fundstelle und, wo möglich, Quelltextbeleg orientiert sich damit an der Form, die die Konformitätsprüfdienste des W3C für Markup und Stylesheets etabliert haben [@w3c_nu_checker, w3c_css_validator]:
- [ ] `w3c_sparql11_query` — contents.tex:219, Kap. 2 · [Web](https://www.w3.org/TR/sparql11-query/)
  > SPARQL ist die standardisierte Abfragesprache für RDF-Daten und ermöglicht es, RDF-Graphen beziehungsweise RDF-Datenbestände über Graphmuster zu durchsuchen und auszuwerten [@W3CRDF11Concepts,w3c_sparql11_query].
- [ ] `w3c_wcag22` — contents.tex:2232, Kap. 5 · [Web](https://www.w3.org/TR/WCAG22/)
  > Für die Gestaltung gelten durchgängig zwei Regeln der Barrierefreiheit, die den Web Content Accessibility Guidelines entnommen sind [@w3c_wcag22].
- [ ] `W3CDQV` — contents.tex:824, Kap. 3 · [Web](https://www.w3.org/TR/vocab-dqv/)
  > K9 & Scoring, Gewichtung, Reporting und Verbesserungshinweise & Forschungsfrage zu aggregiertem Qualitätsindikator; Literatur zu MQA/Piveau, AHP-basierter Gewichtung, DQV-nahen Qualitätsdimensionen und ISO-orientierten Qualitätsmodellen nach [@data_europa, kubler2018comparison, Neumaier2016MetadataQuality, wentzel2023extensive, iso25012, W3CDQV, ISO19157]. & Überführung von Einzelindikatoren in Teilscores, Gesamtscore und handlungsorientiertes Qualitätsreporting.
- [ ] `Zheng2023LLMJudge` — contents.tex:1030, Kap. 3 · [Suche](https://scholar.google.com/scholar?q=Judging+LLM-as-a-Judge+with+MT-Bench+and+Chatbot+Arena)
  > Generative KI kann halluzinieren [@Ji2023HallucinationSurvey] und neigt selbst bei identischer Eingabe zu schwer reproduzierbaren Urteilen [@Zheng2023LLMJudge], weshalb KI-gestützte Verfahren die Bewertung nur ergänzen und im Reporting gekennzeichnet sein sollen, während die Scoringlogik regelbasiert, dokumentiert und nachvollziehbar bleibt.

### Auskommentierte Zitationen

Diese Zitationen stehen in auskommentiertem Text und sind deshalb oben nicht aufgeführt. Relevant nur, falls der Text wieder aktiviert wird — Schlüssel, die nicht in der `.bib` stehen, würden dann ins Leere laufen.

- [ ] `contents.tex:717` — `kubler_2018` — **nicht in der `.bib`**
- [ ] `contents.tex:717` — `albertoni_isaac_2016` — **nicht in der `.bib`**

### Ohne hinterlegten Link

Bei diesen Einträgen enthält die `.bib` weder `doi` noch `url`. Für die Prüfung und für Leserinnen und Leser wäre je ein Nachweis sinnvoll.

- [ ] `Basili1994GQM` — Basili et al. (1994): The Goal Question Metric Approach — [suchen](https://scholar.google.com/scholar?q=The+Goal+Question+Metric+Approach)
- [ ] `few2006dashboard` — Few (2006): Information Dashboard Design: The Effective Visual Communication of Data — [suchen](https://scholar.google.com/scholar?q=Information+Dashboard+Design%3A+The+Effective+Visual+Communication+of+Data)
- [ ] `iso25012` — International Organization for Standa… (2008): ISO/IEC 25012:2008 Data Quality Model — [suchen](https://scholar.google.com/scholar?q=ISO%2FIEC+25012%3A2008+Data+Quality+Model)
- [ ] `iso25024` — International Organization for Standa… (2015): ISO/IEC 25024:2015 Systems and Software Engineering -- Systems and Software Quality Requirements and Evaluation (SQuaRE) -- Measurement of Data Quality — [suchen](https://scholar.google.com/scholar?q=ISO%2FIEC+25024%3A2015+Systems+and+Software+Engineering+--+Systems+and+Software+Quality+Requirements+and+Evaluation+%28SQuaRE%29+--+Measurement+of+Data+Quality)
- [ ] `Mayring2015` — Mayring (2015): Qualitative Inhaltsanalyse: Grundlagen und Techniken — [suchen](https://scholar.google.com/scholar?q=Qualitative+Inhaltsanalyse%3A+Grundlagen+und+Techniken)
- [ ] `StrongLeeWang1997` — Strong et al. (1997): Data quality in context — [suchen](https://scholar.google.com/scholar?q=Data+quality+in+context)
- [ ] `wand1996anchoring` — Wand & Wang (1996): Anchoring Data Quality Dimensions in Ontological Foundations — [suchen](https://scholar.google.com/scholar?q=Anchoring+Data+Quality+Dimensions+in+Ontological+Foundations)
- [ ] `wang1996beyond` — Wang & Strong (1996): Beyond Accuracy: What Data Quality Means to Data Consumers — [suchen](https://scholar.google.com/scholar?q=Beyond+Accuracy%3A+What+Data+Quality+Means+to+Data+Consumers)
- [ ] `Zheng2023LLMJudge` — Zheng et al. (2023): Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena — [suchen](https://scholar.google.com/scholar?q=Judging+LLM-as-a-Judge+with+MT-Bench+and+Chatbot+Arena)

### Zitationen mit Locator

Nur diese Stellen nennen eine konkrete Position in der Quelle. Bei allen übrigen 279 Stellen muss die Fundstelle in der Quelle beim Prüfen selbst gesucht werden.

- [ ] `W3CDCAT3` · Locator `Abschnitt~12.3` — contents.tex:1247
  > Erst mit DCAT 3 wurde für diesen Fall die eigene Klasse dcat:DatasetSeries eingeführt [@W3CDCAT3].

### Mehrfachzitationen

Stellen, an denen mehrere Quellen gemeinsam einen Satz belegen. Hier ist zu prüfen, ob wirklich jede der Quellen die Aussage trägt.

| Quellen | Stellen |
|---|---:|
| `data_europa`, `wentzel2023extensive` | 15 |
| `OECD2020OURdata`, `Ubaldi2013OGD` | 4 |
| `DCATAPDEImplRules2`, `bydata2025handreichung` | 2 |
| `BernersLee2006LinkedData`, `Gayo2015LinkedDataValidationQuality`, `Neumaier2016MetadataQuality`, `Zaveri2016LinkedDataQuality`, `corteslasalle_shacl_dqa`, `wentzel2023extensive` | 1 |
| `DCATAPDEImplRules2`, `DCATAPDESpec2` | 1 |
| `DCATAPDEImplRules2`, `DCATAPDESpec2`, `DCATAPDESpec3`, `Gayo2015LinkedDataValidationQuality`, `W3CRDF11Concepts`, `W3CSHACL` | 1 |
| `DCATAPDEImplRules2`, `DCATAPDESpec3` | 1 |
| `DCATAPDESpec2`, `DCATAPDESpec3` | 1 |
| `DCATAPDESpec2`, `DCATAPDESpec3`, `wentzel2023extensive`, `wilkinson2016fair` | 1 |
| `DCATAPDESpec3`, `DCATAPDEStart` | 1 |
| `FITKOGovDataDocs`, `FitkoGovdata` | 1 |
| `FitkoGovdata`, `Riley2017MetadataPrimer` | 1 |
| `FitkoGovdata`, `govdata_portal` | 1 |
| `Gayo2015LinkedDataValidationQuality`, `Neumaier2016MetadataQuality`, `Zaveri2016LinkedDataQuality` | 1 |
| `Gayo2015LinkedDataValidationQuality`, `W3CDCAT3`, `W3CRDF11Concepts`, `Zaveri2016LinkedDataQuality`, `wilkinson2016fair` | 1 |
| `ISO19157`, `Neumaier2016MetadataQuality`, `W3CDQV`, `data_europa`, `iso25012`, `kubler2018comparison`, `wentzel2023extensive` | 1 |
| `Mayring2014`, `Mayring2015` | 1 |
| `Neumaier2016MetadataQuality`, `data_europa`, `kubler2018comparison`, `wentzel2023extensive`, `wilkinson2016fair` | 1 |
| `Neumaier2016MetadataQuality`, `wentzel2023extensive` | 1 |
| `StrongLeeWang1997`, `Ubaldi2013OGD`, `wand1996anchoring`, `wang1996beyond`, `wilkinson2016fair` | 1 |
| `StrongLeeWang1997`, `Zaveri2016LinkedDataQuality`, `noguerasiso_quality_metadata`, `wand1996anchoring`, `wang1996beyond` | 1 |
| `StrongLeeWang1997`, `noguerasiso_quality_metadata`, `wand1996anchoring`, `wang1996beyond` | 1 |
| `W3CDCAT3`, `W3CRDF11Concepts` | 1 |
| `W3CRDF11Concepts`, `w3c_sparql11_query` | 1 |
| `Zaveri2016LinkedDataQuality`, `noguerasiso_quality_metadata` | 1 |
| `Zaveri2016LinkedDataQuality`, `wang1996beyond` | 1 |
| `data_europa`, `piveauMetricsScore` | 1 |
| `iso25012`, `iso25024` | 1 |
| `iso25012`, `wang1996beyond`, `wilkinson2016fair` | 1 |
| `w3c_css_validator`, `w3c_nu_checker` | 1 |

---

Neu erzeugen: `python3 scripts/quellen_report.py` (Skript liegt im Repo, schreibt diese Datei nach `thesis/README_quellen.md`).
