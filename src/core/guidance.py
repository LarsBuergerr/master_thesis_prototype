"""Handlungswissen je Indikator — die Klartext-Ebene über der Prüflogik.

Ein Indikator-Ergebnis nennt eine ID (``find_keywords_count``) und eine knappe
Prüfmeldung („Suboptimale Anzahl Keywords: 1"). Für einen Datenbereitsteller
ohne DCAT-Kenntnisse ist das zu wenig: er braucht einen sprechenden Namen, die
Begründung, das betroffene Metadatenfeld und den nächsten Schritt.

Die Texte stehen bewusst als **Beiwagen-Registry** hier und nicht in den 27
Indikator-Konstruktoren: die Prüflogik bleibt unangetastet, die Formulierungen
lassen sich an einer Stelle pflegen, und redaktionelle Änderungen erzeugen
keine Diffs in ``scoring/indicators/``. Über :attr:`core.indicator.Indicator.
guidance` hängt der Eintrag trotzdem am Indikator-Objekt, so als wäre er dort
deklariert — ein Indikator kann ihn also mitliefern, ohne ihn zu tragen.

Ausgeliefert wird das Ganze über ``GET /indicators``; das Frontend joint über
die ``indicator_id``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class Vocabulary:
    """Kontrolliertes Vokabular, aus dem ein Wert stammen muss."""

    label_de: str
    url: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


#: Was ein Befund unterhalb der Ist/Soll-Gegenüberstellung zeigt.
#:
#: ``template`` — eine Vorlage aus :attr:`IndicatorGuidance.template`: das Feld
#:   in korrekter Schreibweise mit einem Beispielwert. Sie steht unabhängig vom
#:   Ist-Zustand, ist also bei „falsch angegeben" und „fehlt ganz" dieselbe.
#: ``location`` — die betroffenen Zeilen der geprüften Datei. Für Felder, deren
#:   richtige Form sich nicht als Vorlage vorgeben lässt, weil sie vom Inhalt
#:   abhängt (Schlagwörter, LLM-Kriterien) oder weil das Problem außerhalb der
#:   Datei liegt (tote Links).
#: ``none`` — nichts; Befund und Hinweis oben tragen bereits alles.
DetailMode = str  # "template" | "location" | "none"


@dataclass(frozen=True)
class IndicatorGuidance:
    """Klartext-Beschreibung eines Indikators für Endnutzer."""

    #: Sprechender Name anstelle der technischen ID.
    label_de: str
    #: Was geprüft wird und warum es zählt (Info-Text in der Oberfläche).
    what_de: str
    #: Betroffenes Metadatenfeld in DCAT-AP.de-Schreibweise.
    field: str
    #: Was zu tun ist, um den Indikator zu erfüllen.
    fix_de: str
    vocabulary: Optional[Vocabulary] = None
    #: Siehe :data:`DetailMode`.
    detail: DetailMode = "location"
    #: RDF/XML-Vorlage, nur bei ``detail == "template"``. Alle Beispielwerte
    #: sind gegen das jeweilige Vokabular geprüft (siehe
    #: ``extraction.vocabularies``) — eine Vorlage darf keinen Wert zeigen, der
    #: seinerseits durchfallen würde.
    template: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "label_de": self.label_de,
            "what_de": self.what_de,
            "field": self.field,
            "fix_de": self.fix_de,
            "vocabulary": self.vocabulary.to_dict() if self.vocabulary else None,
            "detail": self.detail,
            "template": self.template,
        }


# Verlinkt wird jeweils die *Übersichtsseite* eines Vokabulars, nicht die
# Namensraum-URI der Werte. Letztere liefert zwar HTTP 200, aber rohes RDF/XML
# (``text/xml``) — im Browser eine Wand aus Markup statt einer Werteliste.
#
# Für die EU-Vokabulare ist das die Concept-Scheme-Ansicht auf op.europa.eu;
# sie nimmt genau die Authority-URI entgegen, gegen die auch validiert wird.
# Die Werte lädt die Seite per JavaScript nach — im Browser sichtbar, in einem
# reinen HTTP-Abruf nicht.
_EU_SCHEME = (
    "https://op.europa.eu/en/web/eu-vocabularies/concept-scheme/-/resource"
    "?uri=http://publications.europa.eu/resource/authority/"
)

_DATA_THEME = Vocabulary("EU-Datenkategorien", _EU_SCHEME + "data-theme")
_FILE_TYPE = Vocabulary("EU-Dateiformate", _EU_SCHEME + "file-type")
_MEDIA_TYPE = Vocabulary(
    "IANA Media Types",
    "https://www.iana.org/assignments/media-types/media-types.xhtml",
)
_AVAILABILITY = Vocabulary("Planned Availability", _EU_SCHEME + "planned-availability")
_LICENSE = Vocabulary("DCAT-AP.de Lizenzen", "https://www.dcat-ap.de/def/licenses/")
# ``/def/politicalGeocoding/`` selbst gibt es nicht (404) — die fünf
# Schlüssel-Vokabulare (Gemeinde-, Regional-, Kreis-, Landes-,
# Regierungsbezirksschlüssel) hängen einzeln darunter. Der Indikator akzeptiert
# jedes davon, also verweist der Link auf die Übersicht, die sie alle listet.
_GEOCODING = Vocabulary("DCAT-AP.de Geokodierung", "https://www.dcat-ap.de/def/")
_GEOCODING_LEVEL = Vocabulary(
    "DCAT-AP.de Geokodierungs-Ebenen",
    "https://www.dcat-ap.de/def/politicalGeocoding/Level/",
)
_CONTRIBUTOR = Vocabulary(
    "DCAT-AP.de Datenbereitsteller", "https://www.dcat-ap.de/def/contributors/"
)
_FREQUENCY = Vocabulary("EU-Aktualisierungsfrequenzen", _EU_SCHEME + "frequency")
_ACCESS_RIGHTS = Vocabulary("EU-Zugriffsrechte", _EU_SCHEME + "access-right")


GUIDANCE: Dict[str, IndicatorGuidance] = {
    # --- Findability ------------------------------------------------------
    "find_keywords_count": IndicatorGuidance(
        label_de="Anzahl Schlagwörter",
        what_de=(
            "Schlagwörter sind der wichtigste Treffer-Kanal in der Portalsuche. "
            "Ideal sind 3 bis 15 Stück; zu wenige machen den Datensatz "
            "unauffindbar, zu viele verwässern die Treffer."
        ),
        field="dcat:keyword",
        fix_de=(
            "Ergänzen Sie Schlagwörter, bis mindestens 3 vorhanden sind — z. B. "
            "Thema, Region und Datenart. Über 15 Schlagwörter sollten Sie ausdünnen."
        ),
        # Welche Schlagwörter richtig sind, hängt am Inhalt — eine Vorlage
        # könnte nur die Syntax zeigen, die hier nie das Problem ist.
        detail="location",
    ),
    "find_theme_valid": IndicatorGuidance(
        label_de="Kategorie aus EU-Vokabular",
        what_de=(
            "Die Kategorie ordnet den Datensatz einem der 13 EU-Themenfelder zu "
            "und steuert die Facettensuche in GovData und data.europa.eu."
        ),
        field="dcat:theme",
        fix_de=(
            "Vergeben Sie mindestens eine Kategorie als URI aus dem EU-Vokabular; "
            "freie Textwerte zählen nicht."
        ),
        vocabulary=_DATA_THEME,
        detail="template",
        template=(
            '<dcat:theme rdf:resource="http://publications.europa.eu/resource/'
            'authority/data-theme/ENVI"/>'
        ),
    ),
    "find_locn_geometry": IndicatorGuidance(
        label_de="Räumliche Abdeckung (Geometrie)",
        what_de=(
            "Die Geometrie beschreibt, welches Gebiet die Daten abdecken. Ohne sie "
            "erscheint der Datensatz nicht in Kartensuchen oder Umkreisfiltern."
        ),
        field="dct:spatial / locn:geometry",
        fix_de=(
            "Hinterlegen Sie eine Bounding Box oder ein Polygon (WKT oder GeoJSON) "
            "als locn:geometry im dct:spatial-Objekt."
        ),
        detail="template",
        template=(
            "<dct:spatial>\n"
            "  <dct:Location>\n"
            '    <locn:geometry rdf:datatype="http://www.opengis.net/ont/geosparql#wktLiteral"\n'
            "      >POLYGON ((9.25 52.16, 9.95 52.16, 9.95 52.52, 9.25 52.52, 9.25 52.16))</locn:geometry>\n"
            "  </dct:Location>\n"
            "</dct:spatial>"
        ),
    ),
    "find_political_geocoding": IndicatorGuidance(
        label_de="Verwaltungsgebiet (Geokodierung)",
        what_de=(
            "Die politische Geokodierung nennt Land, Kreis oder Gemeinde als URI "
            "und macht den Datensatz über Ortsnamen auffindbar."
        ),
        field="dcatde:politicalGeocodingURI",
        fix_de=(
            "Setzen Sie die URI des zuständigen Verwaltungsgebiets aus dem "
            "DCAT-AP.de-Vokabular ein."
        ),
        vocabulary=_GEOCODING,
        detail="template",
        # districtKey/01001 ist ein realer Eintrag des Vokabulars. Die früher
        # hier genannte municipalityKey/07131038 steht NICHT darin und wäre als
        # Vorlage eine Falschauskunft gewesen.
        template=(
            '<dcatde:politicalGeocodingURI rdf:resource="http://dcat-ap.de/def/'
            'politicalGeocoding/districtKey/01001"/>'
        ),
    ),
    "find_geocoding_level": IndicatorGuidance(
        label_de="Ebene des Verwaltungsgebiets",
        what_de=(
            "Die Ebene sagt, ob sich die Angabe auf Bund, Land, Kreis oder "
            "Gemeinde bezieht — nötig, damit Suchfilter richtig gruppieren."
        ),
        field="dcatde:politicalGeocodingLevelURI",
        fix_de=(
            "Ergänzen Sie die passende Ebenen-URI (z. B. municipality) aus dem "
            "DCAT-AP.de-Vokabular."
        ),
        vocabulary=_GEOCODING_LEVEL,
        detail="template",
        template=(
            '<dcatde:politicalGeocodingLevelURI rdf:resource="http://dcat-ap.de/def/'
            'politicalGeocoding/Level/municipality"/>'
        ),
    ),
    "find_temporal_coverage": IndicatorGuidance(
        label_de="Zeitliche Abdeckung",
        what_de=(
            "Anfang und Ende des Zeitraums, den die Daten beschreiben. Nutzende "
            "filtern damit nach Aktualität und Vergleichbarkeit."
        ),
        field="dct:temporal (dcat:startDate / dcat:endDate)",
        fix_de=(
            "Geben Sie Start- und Enddatum als gültiges Datum (JJJJ-MM-TT) oder "
            "Zeitstempel an."
        ),
        detail="template",
        template=(
            "<dct:temporal>\n"
            "  <dct:PeriodOfTime>\n"
            '    <dcat:startDate rdf:datatype="http://www.w3.org/2001/XMLSchema#date"\n'
            "      >2024-01-01</dcat:startDate>\n"
            '    <dcat:endDate rdf:datatype="http://www.w3.org/2001/XMLSchema#date"\n'
            "      >2024-12-31</dcat:endDate>\n"
            "  </dct:PeriodOfTime>\n"
            "</dct:temporal>"
        ),
    ),
    "find_accrual_periodicity": IndicatorGuidance(
        label_de="Aktualisierungsfrequenz",
        what_de=(
            "Wie oft die Daten fortgeschrieben werden. Nutzende erkennen daran, "
            "ob sich ein erneuter Abruf lohnt."
        ),
        field="dct:accrualPeriodicity",
        fix_de=(
            "Setzen Sie die Frequenz als URI aus dem EU-Vokabular (z. B. ANNUAL, "
            "MONTHLY) statt als Freitext."
        ),
        vocabulary=_FREQUENCY,
        detail="template",
        template=(
            '<dct:accrualPeriodicity rdf:resource="http://publications.europa.eu/'
            'resource/authority/frequency/ANNUAL"/>'
        ),
    ),
    "find_issued_datetime": IndicatorGuidance(
        label_de="Veröffentlichungsdatum",
        what_de=(
            "Datum der Erstveröffentlichung, maschinenlesbar formatiert. Portale "
            "sortieren neue Datensätze danach."
        ),
        field="dct:issued",
        fix_de="Tragen Sie das Datum im Format JJJJ-MM-TT oder als Zeitstempel (xs:dateTime) ein.",
        detail="template",
        template=(
            '<dct:issued rdf:datatype="http://www.w3.org/2001/XMLSchema#date"\n'
            "  >2024-01-15</dct:issued>"
        ),
    ),
    "find_modified_datetime": IndicatorGuidance(
        label_de="Datum der letzten Änderung",
        what_de=(
            "Zeigt, wie aktuell der Datensatz ist. Fehlt oder veraltet die "
            "Angabe, wirkt der Datensatz ungepflegt."
        ),
        field="dct:modified",
        fix_de=(
            "Pflegen Sie das Änderungsdatum bei jeder Aktualisierung im Format "
            "JJJJ-MM-TT oder als Zeitstempel."
        ),
        detail="template",
        template=(
            '<dct:modified rdf:datatype="http://www.w3.org/2001/XMLSchema#date"\n'
            "  >2024-06-30</dct:modified>"
        ),
    ),
    # --- Accessibility ----------------------------------------------------
    "acc_download_url": IndicatorGuidance(
        label_de="Direkter Download-Link",
        what_de=(
            "Die Download-URL zeigt direkt auf die Datei. Ohne sie müssen Nutzende "
            "erst durch eine Webseite navigieren — automatische Weiterverarbeitung "
            "ist dann nicht möglich."
        ),
        field="dcat:downloadURL",
        fix_de="Ergänzen Sie je Distribution die direkte Datei-URL zusätzlich zur dcat:accessURL.",
        # Der Befund oben nennt bereits, welche Distribution keine URL hat; die
        # URL selbst kann keine Vorlage vorgeben.
        detail="none",
    ),
    "acc_format": IndicatorGuidance(
        label_de="Format aus EU-Vokabular",
        what_de=(
            "Das Format muss als URI aus dem EU-Vokabular angegeben sein, damit "
            "Portale nach Dateiformat filtern können. Freitext wie „SHP“ wird "
            "nicht erkannt."
        ),
        field="dct:format",
        fix_de="Ersetzen Sie den Freitext durch die passende Format-URI aus dem EU-Vokabular.",
        vocabulary=_FILE_TYPE,
        detail="template",
        template=(
            '<dcat:Distribution rdf:about="…">\n'
            '  <dct:format rdf:resource="http://publications.europa.eu/resource/'
            'authority/file-type/CSV"/>\n'
            "</dcat:Distribution>"
        ),
    ),
    "acc_media_type": IndicatorGuidance(
        label_de="Media Type (MIME)",
        what_de=(
            "Der Media Type sagt Programmen, wie sie die Datei lesen müssen — "
            "Voraussetzung für automatische Verarbeitung."
        ),
        field="dcat:mediaType",
        fix_de=(
            "Hinterlegen Sie je Distribution den IANA-Media-Type als URI, passend "
            "zum tatsächlichen Dateiformat."
        ),
        vocabulary=_MEDIA_TYPE,
        detail="template",
        template=(
            '<dcat:Distribution rdf:about="…">\n'
            '  <dcat:mediaType rdf:resource="https://www.iana.org/assignments/'
            'media-types/text/csv"/>\n'
            "</dcat:Distribution>"
        ),
    ),
    "acc_format_congruence": IndicatorGuidance(
        label_de="Format-Angaben stimmen überein",
        what_de=(
            "Format, Media Type, Dateiendung und der vom Server gemeldete "
            "Content-Type müssen dasselbe Format beschreiben. Widersprüche führen "
            "zu Fehlern beim Abruf."
        ),
        field="dct:format / dcat:mediaType",
        fix_de="Gleichen Sie die Angaben an die tatsächlich ausgelieferte Datei an.",
        # Welcher der widersprüchlichen Werte der richtige ist, entscheidet die
        # ausgelieferte Datei — eine Vorlage kann das nicht vorwegnehmen.
        detail="location",
    ),
    "acc_download_url_response": IndicatorGuidance(
        label_de="Download-Link erreichbar",
        what_de=(
            "Der Download-Link wurde aufgerufen. Antwortet der Server mit einem "
            "Fehler, ist der Datensatz praktisch nicht nutzbar."
        ),
        field="dcat:downloadURL",
        fix_de="Prüfen Sie die gemeldeten URLs und korrigieren oder entfernen Sie tote Links.",
        # Das Problem liegt am anderen Ende der Leitung, nicht in der Syntax —
        # die Fundstelle zeigt, welche Zeile die tote URL trägt.
        detail="location",
    ),
    "acc_access_url_response": IndicatorGuidance(
        label_de="Zugangs-Link erreichbar",
        what_de=(
            "Die Zugangs-URL (Landing Page oder Dienst) wurde aufgerufen. "
            "Fehlerhafte Antworten führen Nutzende ins Leere."
        ),
        field="dcat:accessURL",
        fix_de="Prüfen Sie die gemeldeten URLs und korrigieren oder entfernen Sie tote Links.",
        detail="location",
    ),
    "acc_machine_readable_access": IndicatorGuidance(
        label_de="Maschinenlesbarer Zugang",
        what_de=(
            "Bewertet, wie gut sich die Daten automatisiert weiterverarbeiten "
            "lassen: strukturierte Formate wie CSV, JSON oder GeoJSON zählen hoch, "
            "PDF oder HTML niedrig."
        ),
        field="dcat:mediaType / dct:format",
        fix_de=(
            "Bieten Sie den Inhalt in einem strukturierten, maschinenlesbaren "
            "Format an — etwa CSV, JSON oder GeoJSON."
        ),
        # Das Format ist eine Frage des bereitgestellten Inhalts, nicht der
        # Schreibweise; die Zeile im Quelltext hilft dabei nicht weiter.
        detail="none",
    ),
    "acc_distribution_model": IndicatorGuidance(
        label_de="Vollständigkeit der Distributionen",
        what_de="Prüft, ob jede Distribution die Pflichtangaben (Zugang, Format, Titel) mitbringt.",
        field="dcat:distribution",
        fix_de="Vervollständigen Sie die fehlenden Pflichtangaben je Distribution.",
        detail="location",
    ),
    "acc_format_non_proprietary": IndicatorGuidance(
        label_de="Offenes Dateiformat",
        what_de=(
            "Offene, herstellerunabhängige Formate lassen sich ohne "
            "kostenpflichtige Software öffnen — Kernanforderung an offene Daten."
        ),
        field="dct:format",
        fix_de=(
            "Stellen Sie die Daten in einem offenen, nicht proprietären Format "
            "bereit — etwa CSV, JSON, GeoJSON oder XML."
        ),
        detail="none",
    ),
    # --- Reusability ------------------------------------------------------
    "reuse_license": IndicatorGuidance(
        label_de="Freie Lizenz",
        what_de=(
            "Ohne klare, freie Lizenz dürfen Dritte die Daten rechtlich nicht "
            "weiterverwenden — unabhängig davon, wie gut sie technisch verfügbar sind."
        ),
        field="dct:license",
        fix_de=(
            "Weisen Sie je Distribution eine freie Lizenz als URI zu (z. B. "
            "dl-zero-de/2.0 oder CC-BY 4.0)."
        ),
        vocabulary=_LICENSE,
        # Vorlage statt Fundstelle: welche Lizenz falsch dasteht, sagt schon der
        # Ist-Block; was fehlt, ist die zulässige Schreibweise einer freien.
        detail="template",
        template=(
            '<dcat:Distribution rdf:about="…">\n'
            '  <dct:license rdf:resource="http://dcat-ap.de/def/licenses/'
            'dl-zero-de/2.0"/>\n'
            "</dcat:Distribution>"
        ),
    ),
    "reuse_access_rights": IndicatorGuidance(
        label_de="Zugriffsrechte",
        what_de="Gibt an, ob der Datensatz öffentlich, eingeschränkt oder nicht öffentlich ist.",
        field="dct:accessRights",
        fix_de="Setzen Sie die Zugriffsrechte als URI aus dem EU-Vokabular (in der Regel PUBLIC).",
        vocabulary=_ACCESS_RIGHTS,
        detail="template",
        template=(
            '<dct:accessRights rdf:resource="http://publications.europa.eu/'
            'resource/authority/access-right/PUBLIC"/>'
        ),
    ),
    "reuse_publisher": IndicatorGuidance(
        label_de="Herausgeber strukturiert angegeben",
        what_de=(
            "Der Herausgeber muss als eigenständiges Objekt mit Namen hinterlegt "
            "sein, nicht nur als Textzeile — sonst lässt sich nicht eindeutig "
            "zuordnen, wer verantwortlich ist."
        ),
        field="dct:publisher (foaf:Agent / foaf:name)",
        fix_de=(
            "Legen Sie den Herausgeber als foaf:Agent mit foaf:name an und "
            "verlinken Sie ihn über dct:publisher."
        ),
        detail="template",
        template=(
            "<dct:publisher>\n"
            '  <foaf:Agent rdf:about="https://example.org/organisation/musterbehoerde">\n'
            "    <foaf:name>Musterbehörde der Beispielstadt</foaf:name>\n"
            "  </foaf:Agent>\n"
            "</dct:publisher>"
        ),
    ),
    "reuse_contact": IndicatorGuidance(
        label_de="Kontaktmöglichkeit",
        what_de=(
            "Eine erreichbare Kontaktadresse ist die einzige Möglichkeit für "
            "Nutzende, Fehler zu melden oder Rückfragen zu stellen."
        ),
        field="dcat:contactPoint (vcard:hasEmail / vcard:hasURL)",
        fix_de=(
            "Hinterlegen Sie im Kontaktpunkt eine E-Mail-Adresse (mailto:) oder "
            "eine Kontakt-URL."
        ),
        detail="template",
        # Beide Kanäle in der Vorlage: Der Indikator lässt E-Mail *oder* URL
        # genügen, die Vorlage zeigt aber, wie jeder von beiden zu schreiben
        # ist — die E-Mail mit mailto:-Präfix, die URL als absolute http(s)-URL.
        template=(
            "<dcat:contactPoint>\n"
            '  <vcard:Organization rdf:about="https://example.org/organisation/musterbehoerde">\n'
            "    <vcard:fn>Poststelle der Musterbehörde</vcard:fn>\n"
            '    <vcard:hasEmail rdf:resource="mailto:open.data@musterbehoerde.de"/>\n'
            '    <vcard:hasURL rdf:resource="https://www.musterbehoerde.de/kontakt"/>\n'
            "  </vcard:Organization>\n"
            "</dcat:contactPoint>"
        ),
    ),
    "reuse_contributor_id": IndicatorGuidance(
        label_de="Kennung des Datenbereitstellers",
        what_de=(
            "Die contributorID ordnet den Datensatz dem liefernden Portal zu. Sie "
            "muss genau einmal und aus dem DCAT-AP.de-Vokabular gesetzt sein."
        ),
        field="dcatde:contributorID",
        fix_de="Verwenden Sie genau eine contributorID-URI aus dem DCAT-AP.de-Vokabular.",
        vocabulary=_CONTRIBUTOR,
        detail="template",
        # Der Beispielwert ist ein realer Eintrag des Vokabulars und steht nur
        # für die Schreibweise — einzutragen ist das eigene liefernde Portal.
        template=(
            '<dcatde:contributorID rdf:resource="http://dcat-ap.de/def/'
            'contributors/berlinOpenData"/>'
        ),
    ),
    "reuse_dcat_ap_de_compliance": IndicatorGuidance(
        label_de="DCAT-AP.de-Konformität",
        what_de=(
            "Formale Prüfung der Metadaten gegen das DCAT-AP.de-Schema (SHACL). "
            "Verstöße können dazu führen, dass der Datensatz beim Harvesting "
            "abgelehnt wird."
        ),
        field="gesamter Metadatensatz",
        fix_de="Arbeiten Sie die gemeldeten Verstöße ab — jede Meldung nennt das betroffene Feld.",
        # Der Ist-Block listet jeden Verstoß samt betroffenem Feld; ein
        # gemeinsamer Ausschnitt oder eine Vorlage für „den ganzen Datensatz"
        # gäbe es ohnehin nicht.
        detail="none",
    ),
    "reuse_availability": IndicatorGuidance(
        label_de="Verfügbarkeitsgarantie",
        what_de=(
            "Sagt zu, wie langfristig die Distribution abrufbar bleibt (z. B. "
            "STABLE oder TEMPORARY). Nutzende planen darüber ihre Weiterverwendung."
        ),
        field="dcatap:availability",
        fix_de="Setzen Sie je Distribution eine Verfügbarkeits-URI aus dem EU-Vokabular.",
        vocabulary=_AVAILABILITY,
        detail="template",
        template=(
            '<dcat:Distribution rdf:about="…">\n'
            '  <dcatap:availability rdf:resource="http://publications.europa.eu/'
            'resource/authority/planned-availability/AVAILABLE"/>\n'
            "</dcat:Distribution>"
        ),
    ),
    # --- Expressiveness (LLM) ---------------------------------------------
    "expr_title_quality": IndicatorGuidance(
        label_de="Aussagekraft des Titels",
        what_de=(
            "Der Titel ist das Erste, was Nutzende sehen. Er sollte den Inhalt "
            "konkret benennen — ohne unerklärte Kürzel und ohne reine Nummerierung."
        ),
        field="dct:title",
        fix_de=(
            "Nennen Sie im Titel Datenart, Gegenstand und ggf. Ort oder Zeitraum; "
            "schreiben Sie Abkürzungen aus."
        ),
    ),
    "expr_description_quality": IndicatorGuidance(
        label_de="Aussagekraft der Beschreibung",
        what_de=(
            "Die Beschreibung soll erklären, was die Daten enthalten, wie sie "
            "entstanden sind und wofür sie taugen — nicht nur den Titel wiederholen."
        ),
        field="dct:description",
        fix_de=(
            "Beschreiben Sie Inhalt, Erhebungsmethode, Struktur und Nutzungszweck "
            "in einigen vollständigen Sätzen."
        ),
    ),
    "expr_title_description_coherence": IndicatorGuidance(
        label_de="Titel und Beschreibung passen zusammen",
        what_de=(
            "Titel und Beschreibung müssen denselben Gegenstand meinen. "
            "Widersprüche lassen Nutzende am falschen Datensatz arbeiten."
        ),
        field="dct:title / dct:description",
        fix_de=(
            "Gleichen Sie beide Felder ab: Die Beschreibung sollte den Titel "
            "aufgreifen und konkretisieren."
        ),
    ),
    "expr_keyword_quality": IndicatorGuidance(
        label_de="Qualität der Schlagwörter",
        what_de=(
            "Bewertet nicht die Anzahl, sondern den Inhalt: Schlagwörter sollten "
            "fachlich, verständlich und einzeln sinnvoll sein — keine Systemkürzel "
            "wie „inspireidentifiziert“."
        ),
        field="dcat:keyword",
        fix_de=(
            "Ersetzen Sie technische und formale Tags durch verständliche "
            "Fachbegriffe; ein Begriff je Schlagwort."
        ),
    ),
    "expr_thematic_consistency": IndicatorGuidance(
        label_de="Thematische Stimmigkeit",
        what_de=(
            "Kategorien, Schlagwörter, Titel und Beschreibung sollen dasselbe "
            "Thema zeichnen. Ausreißer verschlechtern die Trefferqualität der Suche."
        ),
        field="dcat:theme / dcat:keyword / dct:title",
        fix_de="Entfernen Sie thematisch unpassende Kategorien und Schlagwörter.",
    ),
    "expr_contextual_qualifiers": IndicatorGuidance(
        label_de="Einordnende Kontextangaben",
        what_de=(
            "Angaben wie Bezugszeitraum, Gebietsstand, Version oder "
            "„vorläufig/geschätzt“ entscheiden darüber, ob die Daten korrekt "
            "interpretiert werden."
        ),
        field="dct:description / dct:temporal",
        fix_de=(
            "Ergänzen Sie Stichtag bzw. Bezugszeitraum, Gebiets- oder "
            "Verfahrensstand und Hinweise auf vorläufige Werte."
        ),
    ),
}


#: Was eine Dimension zusammenfasst — für Überschriften und Info-Icons.
DIMENSION_GUIDANCE: Dict[str, Dict[str, str]] = {
    "findability": {
        "label_de": "Auffindbarkeit",
        "what_de": (
            "Wird der Datensatz über Suche, Filter und Karte gefunden? Bewertet "
            "Schlagwörter, Kategorien, Raum- und Zeitbezug."
        ),
    },
    "accessibility": {
        "label_de": "Zugänglichkeit",
        "what_de": (
            "Kommen Nutzende technisch an die Daten heran? Bewertet Links, "
            "Formate, Erreichbarkeit und Maschinenlesbarkeit."
        ),
    },
    "reusability": {
        "label_de": "Nachnutzbarkeit",
        "what_de": (
            "Dürfen und können Dritte die Daten weiterverwenden? Bewertet Lizenz, "
            "Herausgeber, Kontakt und Schema-Konformität."
        ),
    },
    "expressiveness": {
        "label_de": "Aussagekraft",
        "what_de": (
            "Erklären die Metadaten den Inhalt verständlich? Bewertet Titel, "
            "Beschreibung, Schlagwörter und Kontextangaben — durch ein Sprachmodell."
        ),
    },
}


#: Erklärung der Kennzahlen, die neben jedem Indikator stehen.
SCORE_GLOSSARY: Dict[str, str] = {
    "status": (
        "Ergebnis der Prüfung: erfüllt, teilweise erfüllt oder nicht erfüllt. "
        "„Nicht anwendbar“ heißt, dass der Indikator für diesen Datensatz nicht greift."
    ),
    "score": (
        "Punktwert des Indikators von 0 bis 1 nach der Bewertungsregel — 1,00 "
        "bedeutet vollständig erfüllt. Dieser Wert geht gewichtet in den "
        "Dimensionsscore ein."
    ),
    "raw": (
        "Der ungerundete Messwert vor Anwendung der Bewertungsregel, z. B. der "
        "Anteil der Distributionen, die die Prüfung bestehen. Weicht er vom Score "
        "ab, hat die Bewertungsregel gerundet oder einen Malus verrechnet."
    ),
    "weight": (
        "Gewicht des Indikators innerhalb seiner Dimension. Höheres Gewicht heißt: "
        "Dieser Punkt schlägt stärker auf das Gesamtergebnis durch — dort lohnt "
        "sich Nachbessern am meisten."
    ),
}


def guidance_for(indicator_id: str) -> Optional[IndicatorGuidance]:
    """Klartext-Eintrag zu einer Indikator-ID, oder ``None``.

    ``None`` ist kein Fehler: ein neu registrierter Indikator läuft, bevor die
    Redaktion nachgezogen ist — die Oberfläche fällt dann auf ``name_de`` und
    ``description_de`` des Indikators zurück.
    """
    return GUIDANCE.get(indicator_id)
