"""Prototype-indicator → MQA-metric mapping with A/B/C classification.

This is the **editable heart** of the Modell-vs-MQA evaluation (see
``docs/evaluation_vs_mqa.md`` §3). Each prototype indicator is mapped to the MQA
metric(s) it corresponds to and classified by *how deeply* the two check the
same thing:

* ``A`` – äquivalent: MQA prüft im Kern dasselbe (Presence / Vokabular-Lookup /
  HTTP-Auflösbarkeit). Konvergenz erwartet (H1).
* ``B`` – Prototyp prüft strenger: MQA = PASS bei Vorhandensein/Listing, während
  der Prototyp Gültigkeit / Kongruenz / Tiefe verifiziert. MQA kann überschätzen.
* ``C`` – kein MQA-Pendant: MQA hat dafür keine Metrik (strukturell blind).

The ``mqa`` list names keys from :mod:`mqa.scorer` (``score_dataset`` →
``metrics``). ``mqa_agg`` says how multiple mapped metrics combine into a single
PASS for the contingency analysis (``any`` or ``all``). ``review=True`` flags a
borderline cell that must be argued against the MQA spec before publication —
these are exactly the A/B and B/C judgement calls.

Indicator IDs verified against ``scoring/indicators/`` (registry), MQA keys
against ``mqa/scorer.py``. Edit freely; the join harness reads this table and
flags any indicator it can't find here as ``unmapped`` (nothing is dropped
silently).
"""

from __future__ import annotations

import pandas as pd

# ---------------------------------------------------------------------------
# The mapping. One row per prototype indicator.
#   indicator, dimension, abc, mqa (list of mqa/scorer keys), mqa_agg, review,
#   rationale
# ---------------------------------------------------------------------------

MAPPING: list[dict] = [
    # ---- Findability ----
    dict(
        indicator="find_keywords_count",
        dimension="findability",
        abc="B",
        mqa=["keyword_availability"],
        mqa_agg="any",
        review=True,
        rationale="MQA: Presence dcat:keyword; Prototyp: Anzahl im Band 2<k<6.",
    ),
    dict(
        indicator="find_theme_valid",
        dimension="findability",
        abc="B",
        mqa=["category_availability"],
        mqa_agg="any",
        review=False,
        rationale="MQA: Presence dcat:theme; Prototyp: Wert aus kontrolliertem Vokabular.",
    ),
    dict(
        indicator="find_temporal_coverage",
        dimension="findability",
        abc="A",
        mqa=["temporal_availability"],
        mqa_agg="any",
        review=True,
        rationale="Beide: zeitliche Abdeckung (start/end). Prototyp prüft zusätzlich Datentyp.",
    ),
    dict(
        indicator="find_locn_geometry",
        dimension="findability",
        abc="B",
        mqa=["spatial_availability"],
        mqa_agg="any",
        review=False,
        rationale="MQA: dct:spatial Presence; Prototyp: tatsächliche locn:geometry (nicht leer).",
    ),
    dict(
        indicator="find_political_geocoding",
        dimension="findability",
        abc="B",
        mqa=["spatial_availability"],
        mqa_agg="any",
        review=False,
        rationale="MQA: dct:spatial Presence; Prototyp: dcatde:politicalGeocodingURI aus Vokabular (Fallback locn:adminUnitL2).",
    ),
    dict(
        indicator="find_accrual_periodicity",
        dimension="findability",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: keine Metrik für Aktualisierungsfrequenz.",
    ),
    # dct:issued / dct:modified — MQA zählt sie in Contextuality (auf der besten
    # Distribution mit Dataset-Fallback), der Prototyp als Findability-Indikator.
    dict(
        indicator="find_issued_datetime",
        dimension="findability",
        abc="A",
        mqa=["date_issued_availability"],
        mqa_agg="any",
        review=True,
        rationale="Beide: Vorhandensein dct:issued. Prototyp prüft zusätzlich xs:date/dateTime-Typ.",
    ),
    dict(
        indicator="find_modified_datetime",
        dimension="findability",
        abc="A",
        mqa=["date_modified_availability"],
        mqa_agg="any",
        review=True,
        rationale="Beide: Vorhandensein dct:modified. Prototyp prüft zusätzlich xs:date/dateTime-Typ.",
    ),
    # ---- Accessibility ----
    dict(
        indicator="acc_download_url",
        dimension="accessibility",
        abc="A",
        mqa=["download_url_availability"],
        mqa_agg="any",
        review=False,
        rationale="Beide: Presence dcat:downloadURL.",
    ),
    dict(
        indicator="acc_download_url_response",
        dimension="accessibility",
        abc="A",
        mqa=["download_url_status_code"],
        mqa_agg="any",
        review=False,
        rationale="Beide: HTTP-Auflösbarkeit der downloadURL (<400).",
    ),
    dict(
        indicator="acc_access_url_response",
        dimension="accessibility",
        abc="A",
        mqa=["access_url_status_code"],
        mqa_agg="any",
        review=False,
        rationale="Beide: HTTP-Auflösbarkeit der accessURL (<400).",
    ),
    dict(
        indicator="acc_format",
        dimension="accessibility",
        abc="B",
        mqa=["format_availability", "format_media_type_vocabulary"],
        mqa_agg="all",
        review=True,
        rationale=(
            "MQA: Format vorhanden + format_media_type_vocabulary (Format OR MediaType im Vokabular, OR-Logik). "
            "Prototyp: Format vorhanden UND spezifisch im EU-Vokabular — strenger, da MQA via MediaType-Treffer "
            "auch ohne Format-Vocab-Mitgliedschaft PASS gibt."
        ),
    ),
    dict(
        indicator="acc_media_type",
        dimension="accessibility",
        abc="B",
        mqa=["media_type_availability", "format_media_type_vocabulary"],
        mqa_agg="all",
        review=True,
        rationale=(
            "MQA: MediaType vorhanden + format_media_type_vocabulary (Format OR MediaType im Vokabular, kombiniert). "
            "Prototyp: IANA-URI-Form + IANA-Vokabular-Mitgliedschaft — strenger, da MQA keine IANA-URI-Form prüft "
            "und der Vocab-Check via Format-Treffer auch ohne MediaType-Eintrag PASS gibt."
        ),
    ),
    dict(
        indicator="acc_machine_readable_access",
        dimension="accessibility",
        abc="B",
        mqa=["format_machine_readable"],
        mqa_agg="any",
        review=False,
        rationale="MQA: Listen-Lookup beste Distribution; Prototyp: Mittelwert aller Distributionen, 3 Stufen.",
    ),
    dict(
        indicator="acc_format_non_proprietary",
        dimension="accessibility",
        abc="A",
        mqa=["format_non_proprietary"],
        mqa_agg="any",
        review=False,
        rationale="Beide: nicht-proprietäres Format-URI aus EU-Vokabular. Prototyp: Anteil aller Distributionen.",
    ),
    dict(
        indicator="acc_format_congruence",
        dimension="accessibility",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=True,
        rationale="MQA: keine Format↔MIME-Kongruenzmetrik (B/C-Grenzfall).",
    ),
    dict(
        indicator="acc_distribution_model",
        dimension="accessibility",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=True,
        rationale="MQA: keine Metrik für Distributions-Modellierung (dcat_ap_compliance ist SHACL).",
    ),
    # ---- Reusability ----
    dict(
        indicator="reuse_dcat_ap_de_compliance",
        dimension="reusability",
        abc="A",
        mqa=["dcat_ap_compliance"],
        mqa_agg="any",
        review=False,
        rationale=(
            "Beide: DCAT-AP SHACL-Konformität via ITB-API (wenn MQA shacl_validation=True). "
            "FAIL bei mindestens einer Verletzung."
        ),
    ),
    dict(
        indicator="reuse_license",
        dimension="reusability",
        abc="B",
        mqa=["license_availability", "known_license"],
        mqa_agg="any",
        review=True,
        rationale=(
            "MQA: Lizenz vorhanden (license_availability) + EU-Autoritäts-URI (known_license). "
            "Prototyp: DCAT-AP-DE-Vokabular (andere Autorität) → B, da Prototyp strenger in "
            "Vokabularwahl, MQA strenger bei EU-Autoritäts-URI."
        ),
    ),
    dict(
        indicator="reuse_access_rights",
        dimension="reusability",
        abc="A",
        mqa=["access_rights_availability", "access_rights_vocabulary"],
        mqa_agg="all",
        review=True,
        rationale="Beide: accessRights vorhanden + Vokabular.",
    ),
    dict(
        indicator="reuse_publisher",
        dimension="reusability",
        abc="B",
        mqa=["publisher_availability"],
        mqa_agg="any",
        review=False,
        rationale="MQA: Presence dct:publisher; Prototyp: strukturierter foaf:Agent.",
    ),
    dict(
        indicator="reuse_contact",
        dimension="reusability",
        abc="B",
        mqa=["contact_point_availability"],
        mqa_agg="any",
        review=False,
        rationale="MQA: Presence dcat:contactPoint; Prototyp: strukturierte vcard:Organization.",
    ),
    dict(
        indicator="reuse_contributor_id",
        dimension="reusability",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: keine Metrik (DCAT-AP-DE dcatde:contributorID).",
    ),
    # ---- Expressiveness (all C — MQA has no semantic content check) ----
    dict(
        indicator="expr_title_quality",
        dimension="expressiveness",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: keine Titel-Inhaltsprüfung.",
    ),
    dict(
        indicator="expr_description_quality",
        dimension="expressiveness",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: keine Beschreibungs-Inhaltsprüfung.",
    ),
    dict(
        indicator="expr_keyword_quality",
        dimension="expressiveness",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: zählt Keywords, prüft keine Bedeutung.",
    ),
    dict(
        indicator="expr_title_description_coherence",
        dimension="expressiveness",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: keine Kohärenzprüfung Titel↔Beschreibung.",
    ),
    dict(
        indicator="expr_thematic_consistency",
        dimension="expressiveness",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: keine thematische Konsistenzprüfung.",
    ),
    dict(
        indicator="expr_contextual_qualifiers",
        dimension="expressiveness",
        abc="C",
        mqa=[],
        mqa_agg="any",
        review=False,
        rationale="MQA: keine Prüfung kontextueller Qualifizierer.",
    ),
]

#: All MQA metric keys, in dimension/point order (from ``mqa.scorer``). Used to
#: derive which MQA metrics have NO prototype counterpart (the honest balance,
#: ``docs/evaluation_vs_mqa.md`` §4.3).
ALL_MQA_METRICS: list[str] = [
    "keyword_availability",
    "category_availability",
    "spatial_availability",
    "temporal_availability",
    "access_url_status_code",
    "download_url_availability",
    "download_url_status_code",
    "dcat_ap_compliance",
    "format_availability",
    "media_type_availability",
    "format_media_type_vocabulary",
    "format_non_proprietary",
    "format_machine_readable",
    "license_availability",
    "known_license",
    "access_rights_availability",
    "access_rights_vocabulary",
    "contact_point_availability",
    "publisher_availability",
    "rights_availability",
    "byte_size_availability",
    "date_issued_availability",
    "date_modified_availability",
]


def mapping_df() -> pd.DataFrame:
    """The mapping as a DataFrame, ``mqa`` joined to a ';'-string for display."""
    df = pd.DataFrame(MAPPING)
    df["mqa_str"] = df["mqa"].apply(lambda xs: ";".join(xs))
    return df


def mqa_only_metrics() -> list[str]:
    """MQA metrics that no prototype indicator maps to (MQA prüft, Prototyp nicht)."""
    mapped = {m for row in MAPPING for m in row["mqa"]}
    return [m for m in ALL_MQA_METRICS if m not in mapped]
