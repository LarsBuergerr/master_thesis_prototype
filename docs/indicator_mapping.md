# Indikator-Mapping: Prototyp ↔ MQA

Vollständige Zuordnung aller Prototyp-Indikatoren zu ihren MQA-Gegenstücken,
klassifiziert nach Prüftiefe (A/B/C). Implementiert in `src/evaluation/indicator_map.py`,
eingesetzt in `src/evaluation/indicator_join.py`.

## Klassifikationsschema

| Klasse | Bedeutung |
|--------|-----------|
| **A** | **Äquivalent** — MQA prüft im Kern dasselbe (Presence / Vokabular-Lookup / HTTP-Auflösbarkeit). Konvergenz erwartet (H1). |
| **B** | **Prototyp strenger** — MQA = PASS bei Vorhandensein/Listing, Prototyp verlangt Gültigkeit / Kongruenz / Tiefe. MQA kann Qualität überschätzen (H2). |
| **C** | **Kein MQA-Pendant** — MQA hat dafür keine Metrik, ist strukturell blind (H2). |

`review = ⚠` markiert Grenzfälle (A/B- oder B/C-Übergänge), die vor der Publikation
gegen die MQA-Spezifikation belegt werden müssen.

---

## Findability

| Indikator | A/B/C | MQA-Metrik(en) | Agg. | Review | Begründung |
|-----------|-------|----------------|------|--------|------------|
| `find_keywords_count` | **B** | `keyword_availability` | any | ⚠ | MQA: Presence `dcat:keyword`; Prototyp: Anzahl im Band 3 ≤ k ≤ 10 (Handreichung: min. 3). |
| `find_theme_valid` | **B** | `category_availability` | any | | MQA: Presence `dcat:theme`; Prototyp: Wert aus kontrolliertem Vokabular. |
| `find_temporal_coverage` | **A** | `temporal_availability` | any | ⚠ | Beide: zeitliche Abdeckung (start/end). Prototyp prüft zusätzlich `xs:date`/`dateTime`-Typ. |
| `find_locn_geometry` | **B** | `spatial_availability` | any | | MQA: `dct:spatial` Presence; Prototyp: tatsächliche `locn:geometry` (nicht leer). |
| `find_adminunitl2` | **B** | `spatial_availability` | any | | MQA: `dct:spatial` Presence; Prototyp: `locn:adminUnitL2` plausibel. |
| `find_accrual_periodicity` | **C** | — | — | | MQA: keine Metrik für Aktualisierungsfrequenz. |
| `find_issued_datetime` | **A** | `date_issued_availability` | any | ⚠ | Beide: Vorhandensein `dct:issued`. Prototyp prüft zusätzlich `xs:date`/`dateTime`-Typ. |
| `find_modified_datetime` | **A** | `date_modified_availability` | any | ⚠ | Beide: Vorhandensein `dct:modified`. Prototyp prüft zusätzlich `xs:date`/`dateTime`-Typ. |

---

## Accessibility

| Indikator | A/B/C | MQA-Metrik(en) | Agg. | Review | Begründung |
|-----------|-------|----------------|------|--------|------------|
| `acc_download_url` | **A** | `download_url_availability` | any | | Beide: Presence `dcat:downloadURL`. |
| `acc_download_url_response` | **A** | `download_url_status_code` | any | | Beide: HTTP-Auflösbarkeit der `downloadURL` (< 400). |
| `acc_access_url_response` | **A** | `access_url_status_code` | any | | Beide: HTTP-Auflösbarkeit der `accessURL` (< 400). |
| `acc_format` | **B** | `format_availability`, `format_media_type_vocabulary` | all | ⚠ | MQA: Format vorhanden + Vokabular (OR-Logik mit MediaType). Prototyp: Format vorhanden UND im EU-Vokabular — strenger, da MQA via MediaType-Treffer auch ohne Format-Vocab-Mitgliedschaft PASS gibt. |
| `acc_media_type` | **B** | `media_type_availability`, `format_media_type_vocabulary` | all | ⚠ | MQA: MediaType vorhanden + Vokabular (kombiniert). Prototyp: IANA-URI-Form + IANA-Vokabular-Mitgliedschaft — strenger, da MQA keine IANA-URI-Form prüft. |
| `acc_machine_readable_access` | **B** | `format_machine_readable` | any | | MQA: Listen-Lookup beste Distribution; Prototyp: Mittelwert aller Distributionen, 3 Stufen. |
| `acc_format_non_proprietary` | **A** | `format_non_proprietary` | any | | Beide: nicht-proprietäres Format-URI aus EU-Vokabular. Prototyp: Anteil aller Distributionen. |
| ~~`acc_format_congruence`~~ | **C** | — | — | 🚫 | **Aus dem Modell entfernt** (geblacklistet): schwer begründbar, hohe Fehleinschätzungsrate. Siehe `model_improvement_plan.md` §6.5. |
| ~~`acc_distribution_model`~~ | **C** | — | — | 🚫 | **Aus dem Modell entfernt** (geblacklistet): heuristische Modellierungs-Interpretation, hohe Fehleinschätzungsrate. Siehe `model_improvement_plan.md` §6.5. |

---

## Reusability

| Indikator | A/B/C | MQA-Metrik(en) | Agg. | Review | Begründung |
|-----------|-------|----------------|------|--------|------------|
| `reuse_dcat_ap_de_compliance` | **A** | `dcat_ap_compliance` | any | | Beide: DCAT-AP SHACL-Konformität via ITB-API. FAIL bei mindestens einer Verletzung. |
| `reuse_license` | **B** | `license_availability`, `known_license` | any | ⚠ | MQA: Lizenz vorhanden + EU-Autoritäts-URI. Prototyp: DCAT-AP-DE-Vokabular (andere Autorität) — gegenseitig strenger in unterschiedlichen Aspekten. |
| `reuse_access_rights` | **A** | `access_rights_availability`, `access_rights_vocabulary` | all | ⚠ | Beide: `accessRights` vorhanden + Vokabular. |
| `reuse_publisher` | **B** | `publisher_availability` | any | | MQA: Presence `dct:publisher`; Prototyp: strukturierter `foaf:Agent`. |
| `reuse_contact` | **B** | `contact_point_availability` | any | | MQA: Presence `dcat:contactPoint`; Prototyp: valide `vcard:hasEmail` oder `vcard:hasURL` (Konvention 01). PARTIAL wenn Kontakt ohne Kanal. |
| `reuse_contributor_id` | **C** | — | — | | MQA: keine Metrik (DCAT-AP-DE `dcatde:contributorID`). |

---

## Expressiveness

Alle Expressiveness-Indikatoren sind **C** — MQA hat keine semantischen Inhaltsprüfungen.

| Indikator | A/B/C | MQA-Metrik(en) | Begründung |
|-----------|-------|----------------|------------|
| `expr_title_quality` | **C** | — | MQA: keine Titel-Inhaltsprüfung. |
| `expr_description_quality` | **C** | — | MQA: keine Beschreibungs-Inhaltsprüfung. |
| `expr_keyword_quality` | **C** | — | MQA: zählt Keywords, prüft keine Bedeutung. |
| `expr_title_description_coherence` | **C** | — | MQA: keine Kohärenzprüfung Titel↔Beschreibung. |
| `expr_thematic_consistency` | **C** | — | MQA: keine thematische Konsistenzprüfung. |
| `expr_contextual_qualifiers` | **C** | — | MQA: keine Prüfung kontextueller Qualifizierer. |

---

## MQA prüft, Prototyp nicht

Diese MQA-Metriken haben kein Prototyp-Gegenstück (balance §4.3 aus `docs/evaluation_vs_mqa.md`):

| MQA-Metrik | Anmerkung |
|------------|-----------|
| `rights_availability` | `dct:rights` Presence — überschneidet sich mit `reuse_access_rights`, deckt aber einen anderen Pfad ab. |
| `byte_size_availability` | `dcat:byteSize` Presence — im Prototyp kein dedizierter Indikator. |

---

## Übersicht nach Klasse

| Klasse | Anzahl | Indikatoren |
|--------|--------|-------------|
| **A** | 9 | `acc_download_url`, `acc_download_url_response`, `acc_access_url_response`, `acc_format_non_proprietary`, `find_temporal_coverage`, `find_issued_datetime`, `find_modified_datetime`, `reuse_dcat_ap_de_compliance`, `reuse_access_rights` |
| **B** | 10 | `find_keywords_count`, `find_theme_valid`, `find_locn_geometry`, `find_adminunitl2`, `acc_format`, `acc_media_type`, `acc_machine_readable_access`, `reuse_license`, `reuse_publisher`, `reuse_contact` |
| **C** | 8 | `find_accrual_periodicity`, `reuse_contributor_id`, `expr_title_quality`, `expr_description_quality`, `expr_keyword_quality`, `expr_title_description_coherence`, `expr_thematic_consistency`, `expr_contextual_qualifiers` |
| **Aktiv gesamt** | **27** | |
| 🚫 Entfernt | 2 | `acc_format_congruence`, `acc_distribution_model` (geblacklistet, Code bleibt) |
