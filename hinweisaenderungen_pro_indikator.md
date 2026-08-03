Overall änderungen:

- Dieses Patch Ding komplett entfernen. Es soll insgesamt im unteren Teil der Meldungen sich auf zwei Arten beschränken. Bei Indikatoren bei denen es nicht möglich ist ein form template zu zeigen die betroffene Stelle der aktuellen metadatendatei zeigen wie beispielsweise bei Keywords oder maschinenlesbares Format. Bei den anderen ein template vorschlag geben beispielsweise bei Kategorie aus EU-Vokabular ein Beispiel geben wie es aussehen könnte mit einem Beispielthema in dem fall. Oder bei Räumliche abdeckung (Geometrie) auch ein Template geben wie es aussehen könnte wieder mit einem Beispielwert natürlich, oder bei contactPoint auch ein template anzeigen wie es aussehen könnte.
  Expressiveness Dimension ist gut so wie sie ist bei dieser wird unten immer wie oben auch einfach die betroffene Stelle in der Metadatendatei gezeigt

Im Falle das das Feld komplett fehlt und nicht nur komplett falsch angegeben wurde dann sollte bei den Indikatoren bei denen kein form template angegeben werden kann der block einfach komplett verschwinden wie es aktuell ja auch schon der fall ist zb bei Anzahl Schlagwörter. bei den anderen sollte das template trotzdem angezeigt werden und sich nicht verändern zwischen den Fällen angegeben aber falsch und fehlt komplett.

Von der Namensgebung sollten sich die Felder auch etwas ändern. ich finde der rechte text titel "so sollte es aussehen" passt nicht ganz vor allem wenn man jetzt immer noch unten ein template angezeigt bekommt. ändere das ab zu iwas im sinne von "Hinweise" oder irgendwas was es besser trifft. der untere Block sollte entweder "Betroffene Stellen in der Metadatendatei" heissen oder so etwas wie "So sollte es aussehen" oder ähnlich.

Jetzt die konkreten änderungen an den einzelnen Indikatoren

### Anzahl Schlagwörter:

- gut so wies ist

### Kategorie aus EU-Vokabular

- zu viel clutter
- anstatt "Nicht anerkannt" wie bei den anderen Indikatoren auch den Tag angeben also dcat:theme in dem Fall
- Wie oben erwähnt patch ding entfernen und reduzieren auf ein template wie es angegeben werden sollte mit korrektem Vokabular.

### Räumliche abdeckung (geometrie)

- Auf template änderung von oben updaten

### Ebene des verwaltungsgebiet

- patch raus updaten wie "kategorie aus EU-Vokabular"

### Zeitliche Abdeckung

- auf template änderung von oben updaten

### Veröffentlichungsdatum und Datum der letzten änderung

- gleich wie "zeitliche Abdeckung" auf template änderung von oben updaten

### Direkter Download-Link

- gut so wie es ist bei diesem indikator braucht man nicht umbedingt einen block unten

### Format aus EU-Vokabular

- Patch raus und eine template änderung wie oben beschrieben anzeigen.

### Media Type (MIME)

- Gleich wie "Format aus EU-Vokabular

### Download-Link erreichbar

- Dieses "im einzelnen" Feld raus, der Block betroffene Stelle kann bleiben

### Access-Url erreichbar

- Gleich wie beim download Link abändern

### Maschinenlesbarer Zugang

- Nicht ganz sicher hier, ich glaube der block betroffene Stelle ist hier etwas unnötig und der hinweistext muss angepasst werden. lasse das wort "zusätzlich" weg und sage nur sowas wie der inhalt soll in strukturierten maschinenlesbaren Formaten wie CSV JSON etc angeboten werden.

Ich weis auch nicht ganz ob es diesen Nächster Schritt block gibt. den finde ich eigentlich bei fast allen indikatoren etwas überflüssig.

### offenes Dateiformat

- Ähnlicher Fall wie oben auf jeden Fall den text anpassen sag einfach sowas wie die Daten sollen in einem nicht proprietärem offenen Format bereit gestellt werden zb (blabla)

### Freie Lizenz

- Auch nicht ganz sicher ob es vllt besser wäre anstatt die betroffene Stelle zu zeigen ein template zeigt. überleg dir was du besser findest, aonsnsten ist der indikator fine.

### Herausgeber strukturiert angegeben

anstatt betroffene stelle, template angabe wie oben zeigen wie es aussehen soll

### Kontaktmöglichkeit

auch anstatt betroffener stelle template anzeigen

### Kennung des Datenbereitstellers

- Patch raus und template vorschlag anzeigen anstatt betroffene Stelle

### DCAT-Konformität

- Den ersten Block mit den ganzen verstößen vllt ab ner gewissen länge scrollable lassen, ein unteren block braucht es da nicht ist also gut so wie es ist

### Verfügbarkeitsgarantie

- Patch raus und betroffene stelle zu template vorschau ändern

Die Expressiveness Indikatoren sind gut so wie sie sind falls ich da änderungen haben will gebe ich sie dir später.
