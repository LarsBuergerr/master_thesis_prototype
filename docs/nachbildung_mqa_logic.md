### fetchen / generierung der originalen MQA Daten

Versucht hab ich bisher:

- Anpassung des schweizer Skripts. Absoluter quatsch weil der Prototyp von denen ein kompletten JSON-LD Katalog verwendet (Umschreibung wäre recht umständlich)
- Andere Version von https://github.com/mjanez/metadata-quality-react angeschaut (ist typescript und auch recht umständlich umzubauen für eigene Zwecke)
- Eigene Miniversion der Metrik implementiert (abseits von der dcat-ap konformität)
- Unter verschiedenen Endpunkten versucht die originalen MQA Berichte zu fetchen die unten aufgeführt sind:
  - [https://data.europa.eu/api/mqa/reporter/index.html](https://data.europa.eu/api/mqa/reporter/index.html) (hat nicht funktioniert hat nur ewig geladen)
  - [https://data.europa.eu/api/mqa/cache/index.html](https://data.europa.eu/api/mqa/cache/index.html) (hat auch nicht funktioniert)
  - https://data.europa.eu/datasets/{datasetId}/metrics (hat teilweise funktioniert. manchmal auch einfach garnicht)

Erkenntnisse aus dem ganzen Mist:

- Wenn ich ein RDF Metadatensatz in meine eigene Implementierung, in die Webpage von der Version von mjanez oben und die originalen Werte von dem 3 Link oben fetche bekomme ich 3 komplett unterschiedliche Ergebnisse.
- Ein Problem wird die DCAT-AP Konformität sein. Ein anderes könnte sein das manche Metriken einfach slightly anders implementiert sind und ein großes Problem ist das auf der originalen data.europa.de Version ein leicht abgespeckter oder veränderter Version des Metadatensatzes der Score generiert wird. Ein Beispiel folgt:
  - https://data.europa.eu/api/hub/repo/datasets/6951e0c5-4db3-4910-9fe3-f143d6062ceb.rdf Bei diesem Link fehlt gefühlt die Hälfte der Keys.
  - https://data.europa.eu/api/hub/repo/datasets/6951e0c5-4db3-4910-9fe3-f143d6062ceb~~1.rdf?useNormalizedId=true&locale=en Bei diesem Link stimmt alles. Nvm bin hier ein Tag später am schreiben selbst bei dem Link fehlt die hälfte. Es wird auf zwei Distributionen verwiesen die komplett leer sind und garkeine Attribute enthalten.
  - In der offiziellen API Doku wird aber auf den oberen Linjk verwiesen ohne noch die ganzen komischen Endattribute.
  - Der Bericht zu diesem Metadatensatz ist über diesen Link verfügbar: https://data.europa.eu/api/hub/repo/datasets/6951e0c5-4db3-4910-9fe3-f143d6062ceb~~1.rdf/metrics und weist eigentlich eher darauf hin das für die Berechnung des Scorings der abgeschwächte Metadatenversion genutzt wurde.
  - Like what??? was ist das für ein dummer dreck. wie dumm umständlich kann man es noch machen hell no.

- Weiterer Punkt der auffällt ist das die MQA Metrik bei einigen Indikatoren von der Beschreibung abweicht. Als Beispiel:
  - dcat:format muss laut Methodik aus dem kontrollierten Vokabular von data.europa.de kommen. Trotzdem wird für ein Plain Literal wie "TXT" der Indikator als erfüllt gesehen. Warum auch immer?

-> Also was machen wir jetzt? Ich würde jetzt lowkey die eigene Version einfach so weit verbessern das sie so nah rankommt an die offizielle Methodikbeschreibung des Modells.
-> Dann mappen wir i guess in irgendeiner weise die ergebnisse die aus meiner version des mqas kommen auf die Ergebnisse von meinem Prototypen.

### \*\*Ermittlung wie welche Implementation aufgebaut ist. Mit Fokus auf die originale Implementation von piveau.

`?ref=<commit>`\*\*

Also in der offiziellen Methodik von Piveau die die originale Version von MQA entwickelt haben werden Distributions-Scores nach dem single-best Prinzip gescored.
Dabei wird der Score von jeder Distribution und damit von sämtlichen Feldern in einer Distribution berechnet und dann aus allen Distributionen die beste genommen.
Wenn zum Beispiel in Distirbution A dct:format PASSED und dct:mediaType FAILED und in Distribution B ist es genau umgekehrt dann ist im score entweder nur format oder nur mediaType als PASSED je nach dem welche Distribution die höhere Gesamtpunktzahl hat.
Klingt verrückt dumm, ist es auch, macht absolut garkein sinn aber naja who am i to judge wa.

**`piveau-metrics-annotator` → `Annotation.kt`**

- Web: [https://gitlab.com/piveau/metrics/piveau-metrics-annotator/-/blob/master/src/main/kotlin/io/piveau/metrics/annotator/Annotation.kt](https://gitlab.com/piveau/metrics/piveau-metrics-annotator/-/blob/master/src/main/kotlin/io/piveau/metrics/annotator/Annotation.kt)
- https://gitlab.com/piveau/metrics/piveau-metrics-annotator/-/blob/c4c5f474efc46c4c05a48e613f65c3032196f36e/src/main/kotlin/io/piveau/metrics/annotator/Annotation.kt

Dort stehen wörtlich die zwei Listen `val datasetAnnotations = mutableListOf(...)` und `val distributionAnnotations = mutableListOf(...)`, und `calculateMetrics(...)` wendet erstere auf den Dataset-Knoten, letztere in einer Schleife auf jede `dcat:distribution` an. **Das ist die Tabelle 1:1.**

Metrik <-> RDF-Property (welche Property je Metrik geprüft wird)
Commit-SHA: f303045207c46bb0ecda2093d9687ad51a6aa4d9
https://gitlab.com/piveau/metrics/piveau-metrics-annotator/-/blob/master/src/main/kotlin/io/piveau/metrics/annotator/annotations/AvailabilityAnnotation.kt
https://gitlab.com/piveau/metrics/piveau-metrics-annotator/-/blob/c4c5f474efc46c4c05a48e613f65c3032196f36e/src/main/kotlin/io/piveau/metrics/annotator/annotations/AvailabilityAnnotation.kt

`object ByteSizeAvailableAnnotation : AvailabilityAnnotation(DCAT.byteSize, PV.byteSizeAvailability)` — die `object`-Definitionen mappen jede Metrik auf ihre Property.

Von best-Distribution betroffen (die Aggregation)
Commit-SHA: c2b30e8c515f66d325000ac56dd5c0e6f59cac7c
https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/master/src/main/kotlin/io/piveau/metrics/Scoring.kt
https://gitlab.com/piveau/metrics/piveau-metrics-score/-/blob/df994a1764462b48bf96dfe54f20e2ad2d26011e/src/main/kotlin/io/piveau/metrics/Scoring.kt

- `scoreMetrics(...)` → `reduce { … values.sum() >= … }` = Wahl der einen besten Distribution.
- `scoreDistribution(...)` = Summe der distribution-level-Metriken je Distribution.
- die `issued`/`modified`-Sonderbehandlung (Distribution + Dataset-Fallback) und die `accessUrlStatusCode`/`downloadUrlStatusCode`-Logik (HTTP 200–399).

accessURL und downloadURL StatusCode (Distribution, aber seperater Service )
Commit-SHA: 3e6b47ae9424d71fa11117085a914fd4624d1fb1
https://gitlab.com/piveau/metrics/piveau-metrics-accessibility

### Schweizer Ansatz

Der schweizer ansatz unterscheidet sich in diesem Punkt da hier prozentuale Werte vergeben werden je nachdem wie viele Distributionen die Eigenschaft erfüllen oder nicht.
Eigentlich der sinnvollere Ansatz aber naja whatever es wird sich jetzt halt lieber an der originalen Version orientiert da man das einfacher begründen kann.

Den anderen Ansatz implementiert mit TypeScript hatte ich mir noch nicht so genau angeschaut aber ist eigentlich auch irrelevant wenn man sich versucht so nah wie möglich am original zu orientieren.

Commit-Hash: 149a4eac3b7b5ac25bf9ddf0ac5e71eac67224b6
https://github.com/opendata-swiss/metadata-quality-dashboard/tree/main

Okay also der Ansatz von https://metadata-quality.mjanez.dev/ Github: https://github.com/mjanez/metadata-quality-react
Commit-Hash: 0188ba73b266a96712df3d25adcb6c4846f0e593 Branch: main
handelt das anscheinend ähnlich wie der schweizer Ansatz und verteilt teilweise Punkte je nach dem wie viele Dist. den Indikatoren erfüllen.

Ein weiterer Befund ist zudem das anscheinend bei dem Harvesting Prozess von data.europa.de die Metadaten die von govdata.de gefetched werden teils verändert werden. Deswegen entstehen auch so starke unterschiede grade im lokalen Ansatz von mir entwickelt und den offiziellen Ergebnissen des MQAs vom Triplestore von data.europa. MQA bei denen überprüft teilweise veränderte Version der Metadaten und dann is natürlich klar das da unterschiede entstehen.

### **24.06**

Aktueller Stand

Es wird aktuell die selbst implementierte Version genommen. In python implementiert und alle Indikatoren aus der Methodology der offiziellen data.europa.de Seite und aus Quellcode analyse so exakt wie möglich zu replizieren.

Die Distributionslogik Listen-Lookup single best Distribution wurde übernommen und nachvollzogen aus dem piveau source code (alle links sind oben aufgelistet)

Es wurden alle Indikatoren genau so übernommen wie sie aus der Dokumentation herauslesbar waren ausser die DCAT-AP Überprüfung die logischerweise auf eine DCAT-AP.de überprüfung überführt wurde sonst wäre der Vergleich in diesem Punkt nicht fair wenn wir DCAT-AP.de Metadaten betrachten.
