// Klartext-Katalog zu den Qualitätsindikatoren.
//
// Die Ergebnisse aus dem Backend tragen technische IDs (`find_keywords_count`)
// und knappe Prüfmeldungen. Datenbereitsteller sind aber keine DCAT-Experten:
// sie brauchen einen sprechenden Namen, eine Erklärung, das betroffene
// Metadatenfeld und einen konkreten nächsten Schritt. Genau das steht hier —
// bewusst im Frontend, damit die Formulierungen unabhängig von der
// Prüf-Implementierung gepflegt werden können.
//
// Fällt eine ID heraus (neuer Indikator im Backend), greift `indicatorMeta()`
// auf den vom Backend gelieferten `name_de` zurück.

export interface IndicatorMeta {
  /** Sprechender Name statt der technischen Indikator-ID. */
  label: string;
  /** Was der Indikator prüft — Text des Info-Icons in der Zeile. */
  what: string;
  /** Betroffenes Metadatenfeld in DCAT-AP.de-Schreibweise. */
  field: string;
  /** Was zu tun ist, um den Indikator zu erfüllen. */
  fix: string;
  /** Kontrolliertes Vokabular, aus dem der Wert stammen muss. */
  vocab?: { label: string; url: string };
}

const VOCAB = {
  dataTheme: {
    label: "EU-Datenkategorien",
    url: "http://publications.europa.eu/resource/authority/data-theme",
  },
  fileType: {
    label: "EU-Dateiformate",
    url: "http://publications.europa.eu/resource/authority/file-type",
  },
  mediaType: {
    label: "IANA Media Types",
    url: "https://www.iana.org/assignments/media-types/media-types.xhtml",
  },
  availability: {
    label: "Planned Availability",
    url: "http://publications.europa.eu/resource/authority/planned-availability",
  },
  license: {
    label: "DCAT-AP.de Lizenzen",
    url: "https://www.dcat-ap.de/def/licenses/",
  },
  geocoding: {
    label: "DCAT-AP.de Geokodierung",
    url: "http://dcat-ap.de/def/politicalGeocoding/",
  },
  geocodingLevel: {
    label: "DCAT-AP.de Geokodierungs-Ebenen",
    url: "http://dcat-ap.de/def/politicalGeocoding/Level/",
  },
  contributor: {
    label: "DCAT-AP.de Datenbereitsteller",
    url: "http://dcat-ap.de/def/contributors/",
  },
  frequency: {
    label: "EU-Aktualisierungsfrequenzen",
    url: "http://publications.europa.eu/resource/authority/frequency",
  },
  accessRights: {
    label: "EU-Zugriffsrechte",
    url: "http://publications.europa.eu/resource/authority/access-right",
  },
} as const;

export const INDICATOR_META: Record<string, IndicatorMeta> = {
  // ---- Auffindbarkeit ----------------------------------------------------
  find_keywords_count: {
    label: "Anzahl Schlagwörter",
    what: "Schlagwörter sind der wichtigste Treffer-Kanal in der Portalsuche. Ideal sind 3 bis 15 Stück; zu wenige machen den Datensatz unauffindbar, zu viele verwässern die Treffer.",
    field: "dcat:keyword",
    fix: "Ergänzen Sie Schlagwörter, bis mindestens 3 vorhanden sind — z. B. Thema, Region und Datenart. Über 15 Schlagwörter sollten Sie ausdünnen.",
  },
  find_theme_valid: {
    label: "Kategorie aus EU-Vokabular",
    what: "Die Kategorie ordnet den Datensatz einem der 13 EU-Themenfelder zu und steuert die Facettensuche in GovData und data.europa.eu.",
    field: "dcat:theme",
    fix: "Vergeben Sie mindestens eine Kategorie als URI aus dem EU-Vokabular; freie Textwerte zählen nicht.",
    vocab: VOCAB.dataTheme,
  },
  find_locn_geometry: {
    label: "Räumliche Abdeckung (Geometrie)",
    what: "Die Geometrie beschreibt, welches Gebiet die Daten abdecken. Ohne sie erscheint der Datensatz nicht in Kartensuchen oder Umkreisfiltern.",
    field: "dct:spatial / locn:geometry",
    fix: "Hinterlegen Sie eine Bounding Box oder ein Polygon (WKT oder GeoJSON) als locn:geometry im dct:spatial-Objekt.",
  },
  find_political_geocoding: {
    label: "Verwaltungsgebiet (Geokodierung)",
    what: "Die politische Geokodierung nennt Land, Kreis oder Gemeinde als URI und macht den Datensatz über Ortsnamen auffindbar.",
    field: "dcatde:politicalGeocodingURI",
    fix: "Setzen Sie die URI des zuständigen Verwaltungsgebiets aus dem DCAT-AP.de-Vokabular ein.",
    vocab: VOCAB.geocoding,
  },
  find_geocoding_level: {
    label: "Ebene des Verwaltungsgebiets",
    what: "Die Ebene sagt, ob sich die Angabe auf Bund, Land, Kreis oder Gemeinde bezieht — nötig, damit Suchfilter richtig gruppieren.",
    field: "dcatde:politicalGeocodingLevelURI",
    fix: "Ergänzen Sie die passende Ebenen-URI (z. B. municipality) aus dem DCAT-AP.de-Vokabular.",
    vocab: VOCAB.geocodingLevel,
  },
  find_temporal_coverage: {
    label: "Zeitliche Abdeckung",
    what: "Anfang und Ende des Zeitraums, den die Daten beschreiben. Nutzende filtern damit nach Aktualität und Vergleichbarkeit.",
    field: "dct:temporal (dcat:startDate / dcat:endDate)",
    fix: "Geben Sie Start- und Enddatum als gültiges Datum (JJJJ-MM-TT) oder Zeitstempel an.",
  },
  find_accrual_periodicity: {
    label: "Aktualisierungsfrequenz",
    what: "Wie oft die Daten fortgeschrieben werden. Nutzende erkennen daran, ob sich ein erneuter Abruf lohnt.",
    field: "dct:accrualPeriodicity",
    fix: "Setzen Sie die Frequenz als URI aus dem EU-Vokabular (z. B. ANNUAL, MONTHLY) statt als Freitext.",
    vocab: VOCAB.frequency,
  },
  find_issued_datetime: {
    label: "Veröffentlichungsdatum",
    what: "Datum der Erstveröffentlichung, maschinenlesbar formatiert. Portale sortieren neue Datensätze danach.",
    field: "dct:issued",
    fix: "Tragen Sie das Datum im Format JJJJ-MM-TT oder als Zeitstempel (xs:dateTime) ein.",
  },
  find_modified_datetime: {
    label: "Datum der letzten Änderung",
    what: "Zeigt, wie aktuell der Datensatz ist. Fehlt oder veraltet die Angabe, wirkt der Datensatz gepflegt-los.",
    field: "dct:modified",
    fix: "Pflegen Sie das Änderungsdatum bei jeder Aktualisierung im Format JJJJ-MM-TT oder als Zeitstempel.",
  },

  // ---- Zugänglichkeit ----------------------------------------------------
  acc_download_url: {
    label: "Direkter Download-Link",
    what: "Die Download-URL zeigt direkt auf die Datei. Ohne sie müssen Nutzende erst durch eine Webseite navigieren — automatische Weiterverarbeitung ist dann nicht möglich.",
    field: "dcat:downloadURL",
    fix: "Ergänzen Sie je Distribution die direkte Datei-URL zusätzlich zur dcat:accessURL.",
  },
  acc_format: {
    label: "Format aus EU-Vokabular",
    what: "Das Format muss als URI aus dem EU-Vokabular angegeben sein, damit Portale nach Dateiformat filtern können. Freitext wie „SHP“ wird nicht erkannt.",
    field: "dct:format",
    fix: "Ersetzen Sie den Freitext durch die passende Format-URI aus dem EU-Vokabular.",
    vocab: VOCAB.fileType,
  },
  acc_media_type: {
    label: "Media Type (MIME)",
    what: "Der Media Type sagt Programmen, wie sie die Datei lesen müssen — Voraussetzung für automatische Verarbeitung.",
    field: "dcat:mediaType",
    fix: "Hinterlegen Sie je Distribution den IANA-Media-Type als URI, passend zum tatsächlichen Dateiformat.",
    vocab: VOCAB.mediaType,
  },
  acc_format_congruence: {
    label: "Format-Angaben stimmen überein",
    what: "Format, Media Type, Dateiendung und der vom Server gemeldete Content-Type müssen dasselbe Format beschreiben. Widersprüche führen zu Fehlern beim Abruf.",
    field: "dct:format / dcat:mediaType",
    fix: "Gleichen Sie die Angaben an die tatsächlich ausgelieferte Datei an.",
  },
  acc_download_url_response: {
    label: "Download-Link erreichbar",
    what: "Der Download-Link wurde aufgerufen. Antwortet der Server mit einem Fehler, ist der Datensatz praktisch nicht nutzbar.",
    field: "dcat:downloadURL",
    fix: "Prüfen Sie die gemeldeten URLs und korrigieren oder entfernen Sie tote Links.",
  },
  acc_access_url_response: {
    label: "Zugangs-Link erreichbar",
    what: "Die Zugangs-URL (Landing Page oder Dienst) wurde aufgerufen. Fehlerhafte Antworten führen Nutzende ins Leere.",
    field: "dcat:accessURL",
    fix: "Prüfen Sie die gemeldeten URLs und korrigieren oder entfernen Sie tote Links.",
  },
  acc_machine_readable_access: {
    label: "Maschinenlesbarer Zugang",
    what: "Bewertet, wie gut sich die Daten automatisiert weiterverarbeiten lassen: strukturierte Formate wie CSV, JSON oder GeoJSON zählen hoch, PDF oder HTML niedrig.",
    field: "dcat:mediaType / dct:format",
    fix: "Bieten Sie den Inhalt zusätzlich in einem strukturierten Format an (z. B. CSV, JSON, GeoJSON).",
  },
  acc_distribution_model: {
    label: "Vollständigkeit der Distributionen",
    what: "Prüft, ob jede Distribution die Pflichtangaben (Zugang, Format, Titel) mitbringt.",
    field: "dcat:distribution",
    fix: "Vervollständigen Sie die fehlenden Pflichtangaben je Distribution.",
  },
  acc_format_non_proprietary: {
    label: "Offenes Dateiformat",
    what: "Offene, herstellerunabhängige Formate lassen sich ohne kostenpflichtige Software öffnen — Kernanforderung an offene Daten.",
    field: "dct:format",
    fix: "Stellen Sie zusätzlich zu proprietären Formaten (z. B. XLSX, SHP) eine offene Variante bereit (z. B. CSV, GeoJSON).",
  },

  // ---- Nachnutzbarkeit ---------------------------------------------------
  reuse_license: {
    label: "Freie Lizenz",
    what: "Ohne klare, freie Lizenz dürfen Dritte die Daten rechtlich nicht weiterverwenden — unabhängig davon, wie gut sie technisch verfügbar sind.",
    field: "dct:license",
    fix: "Weisen Sie je Distribution eine freie Lizenz als URI zu (z. B. dl-zero-de/2.0 oder CC-BY 4.0).",
    vocab: VOCAB.license,
  },
  reuse_access_rights: {
    label: "Zugriffsrechte",
    what: "Gibt an, ob der Datensatz öffentlich, eingeschränkt oder nicht öffentlich ist.",
    field: "dct:accessRights",
    fix: "Setzen Sie die Zugriffsrechte als URI aus dem EU-Vokabular (in der Regel PUBLIC).",
    vocab: VOCAB.accessRights,
  },
  reuse_publisher: {
    label: "Herausgeber strukturiert angegeben",
    what: "Der Herausgeber muss als eigenständiges Objekt mit Namen hinterlegt sein, nicht nur als Textzeile — sonst lässt sich nicht eindeutig zuordnen, wer verantwortlich ist.",
    field: "dct:publisher (foaf:Agent / foaf:name)",
    fix: "Legen Sie den Herausgeber als foaf:Agent mit foaf:name an und verlinken Sie ihn über dct:publisher.",
  },
  reuse_contact: {
    label: "Kontaktmöglichkeit",
    what: "Eine erreichbare Kontaktadresse ist die einzige Möglichkeit für Nutzende, Fehler zu melden oder Rückfragen zu stellen.",
    field: "dcat:contactPoint (vcard:hasEmail / vcard:hasURL)",
    fix: "Hinterlegen Sie im Kontaktpunkt eine E-Mail-Adresse (mailto:) oder eine Kontakt-URL.",
  },
  reuse_contributor_id: {
    label: "Kennung des Datenbereitstellers",
    what: "Die contributorID ordnet den Datensatz dem liefernden Portal zu. Sie muss genau einmal und aus dem DCAT-AP.de-Vokabular gesetzt sein.",
    field: "dcatde:contributorID",
    fix: "Verwenden Sie genau eine contributorID-URI aus dem DCAT-AP.de-Vokabular.",
    vocab: VOCAB.contributor,
  },
  reuse_dcat_ap_de_compliance: {
    label: "DCAT-AP.de-Konformität",
    what: "Formale Prüfung der Metadaten gegen das DCAT-AP.de-Schema (SHACL). Verstöße können dazu führen, dass der Datensatz beim Harvesting abgelehnt wird.",
    field: "gesamter Metadatensatz",
    fix: "Arbeiten Sie die gemeldeten Verstöße ab — jede Meldung nennt das betroffene Feld.",
  },
  reuse_availability: {
    label: "Verfügbarkeitsgarantie",
    what: "Sagt zu, wie langfristig die Distribution abrufbar bleibt (z. B. STABLE oder TEMPORARY). Nutzende planen darüber ihre Weiterverwendung.",
    field: "dcatap:availability",
    fix: "Setzen Sie je Distribution eine Verfügbarkeits-URI aus dem EU-Vokabular.",
    vocab: VOCAB.availability,
  },

  // ---- Aussagekraft (LLM-gestützt) ---------------------------------------
  expr_title_quality: {
    label: "Aussagekraft des Titels",
    what: "Der Titel ist das Erste, was Nutzende sehen. Er sollte den Inhalt konkret benennen — ohne unerklärte Kürzel und ohne reine Nummerierung.",
    field: "dct:title",
    fix: "Nennen Sie im Titel Datenart, Gegenstand und ggf. Ort oder Zeitraum; schreiben Sie Abkürzungen aus.",
  },
  expr_description_quality: {
    label: "Aussagekraft der Beschreibung",
    what: "Die Beschreibung soll erklären, was die Daten enthalten, wie sie entstanden sind und wofür sie taugen — nicht nur den Titel wiederholen.",
    field: "dct:description",
    fix: "Beschreiben Sie Inhalt, Erhebungsmethode, Struktur und Nutzungszweck in einigen vollständigen Sätzen.",
  },
  expr_title_description_coherence: {
    label: "Titel und Beschreibung passen zusammen",
    what: "Titel und Beschreibung müssen denselben Gegenstand meinen. Widersprüche lassen Nutzende am falschen Datensatz arbeiten.",
    field: "dct:title / dct:description",
    fix: "Gleichen Sie beide Felder ab: Die Beschreibung sollte den Titel aufgreifen und konkretisieren.",
  },
  expr_keyword_quality: {
    label: "Qualität der Schlagwörter",
    what: "Bewertet nicht die Anzahl, sondern den Inhalt: Schlagwörter sollten fachlich, verständlich und einzeln sinnvoll sein — keine Systemkürzel wie „inspireidentifiziert“.",
    field: "dcat:keyword",
    fix: "Ersetzen Sie technische und formale Tags durch verständliche Fachbegriffe; ein Begriff je Schlagwort.",
  },
  expr_thematic_consistency: {
    label: "Thematische Stimmigkeit",
    what: "Kategorien, Schlagwörter, Titel und Beschreibung sollen dasselbe Thema zeichnen. Ausreißer verschlechtern die Trefferqualität der Suche.",
    field: "dcat:theme / dcat:keyword / dct:title",
    fix: "Entfernen Sie thematisch unpassende Kategorien und Schlagwörter.",
  },
  expr_contextual_qualifiers: {
    label: "Einordnende Kontextangaben",
    what: "Angaben wie Bezugszeitraum, Gebietsstand, Version oder „vorläufig/geschätzt“ entscheiden darüber, ob die Daten korrekt interpretiert werden.",
    field: "dct:description / dct:temporal",
    fix: "Ergänzen Sie Stichtag bzw. Bezugszeitraum, Gebiets- oder Verfahrensstand und Hinweise auf vorläufige Werte.",
  },
};

/** Katalogeintrag mit Rückfall auf den Namen aus dem Backend-Ergebnis. */
export function indicatorMeta(id: string, fallbackName?: string): IndicatorMeta {
  return (
    INDICATOR_META[id] ?? {
      label: fallbackName || id,
      what: "Für diesen Indikator liegt noch keine Kurzbeschreibung vor.",
      field: id,
      fix: "Siehe Prüfmeldung.",
    }
  );
}

export const DIMENSION_META: Record<string, { label: string; what: string }> = {
  findability: {
    label: "Auffindbarkeit",
    what: "Wird der Datensatz über Suche, Filter und Karte gefunden? Bewertet Schlagwörter, Kategorien, Raum- und Zeitbezug.",
  },
  accessibility: {
    label: "Zugänglichkeit",
    what: "Kommen Nutzende technisch an die Daten heran? Bewertet Links, Formate, Erreichbarkeit und Maschinenlesbarkeit.",
  },
  reusability: {
    label: "Nachnutzbarkeit",
    what: "Dürfen und können Dritte die Daten weiterverwenden? Bewertet Lizenz, Herausgeber, Kontakt und Schema-Konformität.",
  },
  expressiveness: {
    label: "Aussagekraft",
    what: "Erklären die Metadaten den Inhalt verständlich? Bewertet Titel, Beschreibung, Schlagwörter und Kontextangaben — durch ein Sprachmodell.",
  },
};

export function dimensionLabel(dim: string): string {
  return DIMENSION_META[dim]?.label ?? dim;
}

/** Erklärtexte der Tabellenspalten (Info-Icons in der Kopfzeile). */
export const COLUMN_HELP = {
  status: "Ergebnis der Prüfung: erfüllt, teilweise erfüllt oder nicht erfüllt. „Nicht anwendbar“ heißt, dass der Indikator für diesen Datensatz nicht greift.",
  score:
    "Punktwert des Indikators von 0 bis 1 nach der Bewertungsregel — 1,00 bedeutet vollständig erfüllt. Dieser Wert geht gewichtet in den Dimensionsscore ein.",
  raw: "Der ungerundete Messwert vor Anwendung der Bewertungsregel, z. B. der Anteil der Distributionen, die die Prüfung bestehen. Weicht er vom Score ab, hat die Bewertungsregel gerundet oder einen Malus verrechnet.",
  weight:
    "Gewicht des Indikators innerhalb seiner Dimension. Höheres Gewicht heißt: Dieser Punkt schlägt stärker auf das Gesamtergebnis durch — dort lohnt sich Nachbessern am meisten.",
} as const;
