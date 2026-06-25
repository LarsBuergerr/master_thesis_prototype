# Evaluationsaufbau Stand 25.06

Sample reproduzierbar aus notebook `12_fetch_stratified_sample.ipynb`

Sample: `sample_2026-06-25_09-57`
Randomseed: 67
Size: 50/50

Alle Tests und alle Konfigurationen die in der Thesis gezeigt werden werden auf einer Sample stattfinden. Um die Reproduzierbarkeit zu verbessern.
Zusätzlich wurde eine manuelle Extremfall Stichprobe von 10 (@TODO maybe auf 20 erhöhen) erstellt die Edgecases repräsentiert.

1. Unterschiedliche Konfigurationen / Gewichtung der Indikatoren und Dimensionen
   1. Bestenfalls einmal Default und einmal die erstellte Konfiguration `state_evaluation_weighted`. @TODO Diskussionsgrundlage schaffen warum genau diese Konfiguration Sinn ergibt.
   2. Das kann man recht gut an der Extremfallsample zeigen wie sich der Output verändert.

2. Unterschiedliche LLM Modelle und das welches am besten performed noch Differenzen von multiplen Runs mit dem selben LLM aufzeigen. Zeigen dass der Output stabil ist. Aufzeigen warum sonnet4.5 hier am besten ist. (Diese Runs am besten mit der großen Stichprobe machen)

3. Zur Evaluation an sich zuerst eine Ground Truth erstellen und das Modell mit der `weigted` Konfiguration und dem besten LLM gegen diese GroundTruth laufen lassen. ODER man erstellt eine Ground Truth dann mit dieser lässt man das Modell mit Standartwerten und der Weighted Config laufen und kann daran zeigen dass die `weighted_config` näher an die ground truth hinkommt als der Default. Damit kann man aber nur die Indikatorgewichtung beweisen. Die Dimensionsgewichtung muss man sich anders herleiten. Vllt einfach abgeleitet aus Literatur und MQA?

4. Im folgenden Schritt lässt man NUR die Expressiveness Dimension mit unterschiedlichen Modellen laufen und kann dadurch zeigen das ein bestimmtes Modell am nächsten an die Ground Truth hinkommt. Dieses Modell validiert man im Anschluss durch multiple Läufe und zeigt damit das die Ergebnisse konsistent über mehrere Durchläufe sind.

5. Dieses fertige Modell lässt man dann gegen MQA laufen zeigt H1 - H3 auf. Tweaked noch etwas den Output das es gut aussieht und im besten Fall vergleicht man dann noch die Ground Truth gegen MQA und den Prototyp und kann zeigen dass der Prototyp eine höhere Korrelation bzw kleine Standartabweichung als MQA gegen die GT hat.

### TODO bis man die ganzen Tokens für Testruns verbrennt

1. Extremfall Stichprobe erhöhen (low Prio)
2. Sich überlegen ob diese Groundtruth Methodik aktuell wirklich so klappt. (Das Problem an der aktuellen Methodik (also von 0-3 pro Dimension bewerten kann eventuell dazu führen dass man die Unterschiede zwischen unterschiedlichen Konfigurationen und dem Vergleich zu MQA garnicht erkennt weil die Abstufungen zu grob sind. Ein anderes Problem generell ist überhaupt zu erklären wieso man genau die Methodik die man dann letztendlich nimmt halt nimmt lul))
3. GroundTruth erstellen / Manuell labeln und hoffen das man Pro-Prototyp labelt :sob:
4. die Indikatoren nochmal überarbeiten und eventuell nochmal über die DCAT-AP.de Konventionen gehen und noch einen Parameter adden oder so.
5. Expressiveness Dimension nochmal komplett überarbeiten und etwas Prompt Engineering betreiben sodass die Bewertung eher der Beschreibung der Felder in dem Konventionshandbuch entsprechen.
6. Indikatormap nochmal überarbeiten und eventuell die Evaluation so flexibel gestalten dass man nicht jedes mal den Testrun machen muss sondern Eventuell im nachgang noch das Mapping verändern kann welches dann dynamisch die generierten CSV Files updated
7. Alle Visualisierung auf Deutsch darstellen
8.
