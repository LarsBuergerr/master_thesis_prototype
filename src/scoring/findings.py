"""Bauen der Befunde: ``details`` → Ist-/Soll-Gegenüberstellung.

Aufbau analog zu :mod:`scoring.remediation`: eine Tabelle von Buildern, je
Indikator einer, angehängt post-hoc an das Ergebnis
(:func:`attach_finding`). Die Indikator-Klassen bleiben dadurch unberührt —
sie liefern weiterhin nur ``details``, die Deutung passiert hier.

Anders als die Remediation braucht ein Befund keinen ``DatasetContext``: er
liest ausschließlich das, was der Indikator ohnehin schon protokolliert hat.
Fehlt für eine ID ein Builder, entsteht ein generischer Befund aus Prüfmeldung
und Handlungsanweisung — kein Indikator bleibt ohne Erklärung.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional

from core.finding import FactLine, Finding
from core.guidance import guidance_for
from core.indicator import IndicatorResult, IndicatorStatus

__all__ = ["attach_finding", "build_finding"]

Details = Dict[str, Any]
Builder = Callable[[Details, str], Finding]


# --- Zugriffs-Helfer auf das lose typisierte ``details`` --------------------


def _num(details: Details, key: str, default: int = 0) -> int:
    value = details.get(key)
    return value if isinstance(value, (int, float)) else default


def _text(details: Details, key: str) -> Optional[str]:
    value = details.get(key)
    return value if isinstance(value, str) else None


def _strings(details: Details, key: str) -> List[str]:
    value = details.get(key)
    return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []


def _rows(details: Details, key: str) -> List[Details]:
    value = details.get(key)
    return [v for v in value if isinstance(v, dict)] if isinstance(value, list) else []


def _where(uri: Any) -> Optional[str]:
    """Distributions-URIs enden auf ``#distribution`` — für Menschen Rauschen."""
    if not isinstance(uri, str) or not uri:
        return None
    return uri[: -len("#distribution")] if uri.endswith("#distribution") else uri


def _plural(n: int, one: str, many: str) -> str:
    return one if n == 1 else many


def _quote(values: List[str], limit: int = 15) -> str:
    shown = [f"„{v}“" for v in values[:limit]]
    rest = len(values) - len(shown)
    return ", ".join(shown) + (f" … und {rest} weitere" if rest > 0 else "")


# --- Bausteine für Distributions-Indikatoren -------------------------------


def _per_distribution(details: Details, value_key: str, empty: str) -> List[FactLine]:
    """Ist-Block für alle Indikatoren mit ``per_distribution``: je Distribution
    der aktuelle Wert plus Fundstelle, damit klar ist, welche gemeint ist."""
    lines: List[FactLine] = []
    for idx, entry in enumerate(_rows(details, "per_distribution"), start=1):
        values = _strings(entry, value_key)
        lines.append(
            FactLine(
                label=f"Distribution {idx}",
                value=", ".join(values) if values else empty,
                tone="good" if entry.get("passes") is True else "bad",
                where=_where(entry.get("uri")),
            )
        )
    return lines


def _distribution_headline(details: Details, subject: str) -> str:
    total = _num(details, "total_distributions")
    passing = _num(details, "passing_count")
    if total == 0:
        return f"Es ist keine Distribution hinterlegt, {subject} kann daher nicht geprüft werden."
    word = _plural(total, "Distribution", "Distributionen")
    if passing == 0:
        return f"Keine der {total} {word} hat {subject}."
    return (
        f"{passing} von {total} {word} {_plural(passing, 'hat', 'haben')} {subject} "
        "— bei den übrigen fehlt sie."
    )


def _distribution_builder(value_key: str, subject: str, empty: str, target: str) -> Builder:
    def build(details: Details, message: str) -> Finding:
        return Finding(
            headline=_distribution_headline(details, subject),
            current=_per_distribution(details, value_key, empty),
            target=target,
        )

    return build


# --- Builder je Indikator --------------------------------------------------


def _keywords_count(details: Details, message: str) -> Finding:
    count = _num(details, "keyword_count")
    keywords = _strings(details, "keywords")
    if count == 0:
        headline = "Der Datensatz hat kein einziges Schlagwort — er ist über die Portalsuche kaum auffindbar."
    elif count < 3:
        headline = (
            f"Nur {count} {_plural(count, 'Schlagwort', 'Schlagwörter')} vergeben, "
            "empfohlen sind mindestens 3."
        )
    else:
        headline = f"{count} Schlagwörter sind zu viele — die Trefferqualität sinkt."
    label = (
        "Schlagwörter"
        if count == 0
        else f"Aktuell {count} {_plural(count, 'Schlagwort', 'Schlagwörter')}"
    )
    return Finding(
        headline=headline,
        current=[FactLine(label, _quote(keywords) if keywords else "keine", "bad")],
        target="3 bis 15 Schlagwörter, die Thema, Region und Datenart benennen.",
    )


def _theme_valid(details: Details, message: str) -> Finding:
    valid = _strings(details, "valid_themes")
    invalid = _strings(details, "invalid_themes")
    count = _num(details, "theme_count", len(valid) + len(invalid))
    if count == 0:
        return Finding(
            headline="Es ist keine Kategorie gesetzt — der Datensatz erscheint in keiner Themen-Facette.",
            current=[FactLine("dcat:theme", "nicht gesetzt", "bad")],
            target="Mindestens eine Kategorie als URI aus dem EU-Vokabular der 13 Datenkategorien.",
        )
    current: List[FactLine] = []
    if valid:
        current.append(FactLine("Anerkannt", ", ".join(valid), "good"))
    if invalid:
        current.append(FactLine("Nicht anerkannt", ", ".join(invalid), "bad"))
    return Finding(
        headline=(
            f"{len(invalid)} von {count} Kategorien stammen nicht aus dem "
            "EU-Vokabular und werden ignoriert."
        ),
        current=current,
        target="Mindestens eine Kategorie als URI aus dem EU-Vokabular der 13 Datenkategorien.",
    )


def _locn_geometry(details: Details, message: str) -> Finding:
    return Finding(
        headline="Es ist kein Gebiet hinterlegt — der Datensatz taucht in Kartensuchen nicht auf.",
        current=[FactLine("locn:geometry", "nicht gesetzt", "bad")],
        target=(
            "Eine Bounding Box oder ein Polygon als WKT oder GeoJSON, "
            "z. B. POLYGON ((9.25 52.16, …))."
        ),
    )


def _political_geocoding(details: Details, message: str) -> Finding:
    count = _num(details, "geocoding_count")
    uri = _text(details, "uri")
    return Finding(
        headline=(
            "Es ist kein Verwaltungsgebiet angegeben — eine Suche nach Ortsnamen "
            "findet den Datensatz nicht."
            if count == 0
            else "Das angegebene Verwaltungsgebiet stammt nicht aus dem DCAT-AP.de-Vokabular."
        ),
        current=[FactLine("dcatde:politicalGeocodingURI", uri or "nicht gesetzt", "bad")],
        target=(
            "Eine URI aus dem DCAT-AP.de-Geokodierungs-Vokabular, z. B. "
            "http://dcat-ap.de/def/politicalGeocoding/municipalityKey/07131038."
        ),
    )


def _geocoding_level(details: Details, message: str) -> Finding:
    count = _num(details, "level_count")
    invalid = _strings(details, "invalid")
    return Finding(
        headline=(
            "Die Ebene des Verwaltungsgebiets fehlt — Suchfilter können den "
            "Raumbezug nicht einordnen."
            if count == 0
            else "Nicht alle angegebenen Ebenen stammen aus dem kontrollierten Vokabular."
        ),
        current=[
            FactLine(
                "dcatde:politicalGeocodingLevelURI",
                ", ".join(invalid) if invalid else "nicht gesetzt",
                "bad",
            )
        ],
        target="Eine Ebenen-URI, z. B. http://dcat-ap.de/def/politicalGeocoding/Level/municipality.",
    )


def _temporal_coverage(details: Details, message: str) -> Finding:
    start_count = _num(details, "start_count")
    end_count = _num(details, "end_count")
    start_valid = details.get("start_valid") is True
    end_valid = details.get("end_valid") is True

    def line(label: str, count: int, valid: bool, fmt_key: str) -> FactLine:
        if count == 0:
            value = "nicht gesetzt"
        elif valid:
            value = "gesetzt und gültig"
        else:
            value = f"gesetzt, aber ungültiges Format ({_text(details, fmt_key) or 'unbekannt'})"
        return FactLine(label, value, "good" if valid else "bad")

    missing = start_count == 0 and end_count == 0
    return Finding(
        headline=(
            "Der Zeitraum der Daten ist nicht angegeben — Nutzende können die "
            "Aktualität nicht einschätzen."
            if missing
            else "Der angegebene Zeitraum ist unvollständig oder kein gültiges Datum."
        ),
        current=[
            line("dcat:startDate", start_count, start_valid, "start_format"),
            line("dcat:endDate", end_count, end_valid, "end_format"),
        ],
        target="Start- und Enddatum im Format JJJJ-MM-TT (oder als vollständiger Zeitstempel).",
    )


def _datetime_field(field: str) -> Builder:
    def build(details: Details, message: str) -> Finding:
        total = _num(details, "total")
        invalid = _rows(details, "invalid")
        if total == 0:
            return Finding(
                headline=f"{field} ist nicht gesetzt — es ist nicht erkennbar, wie aktuell der Datensatz ist.",
                current=[FactLine(field, "nicht gesetzt", "bad")],
                target="Datum als JJJJ-MM-TT oder Zeitstempel JJJJ-MM-TTThh:mm:ss.",
            )
        return Finding(
            headline=(
                f"{len(invalid)} {_plural(len(invalid), 'Wert entspricht', 'Werte entsprechen')} "
                "nicht dem erwarteten Datumsformat."
            ),
            current=[
                FactLine(
                    field,
                    str(entry.get("value") or entry.get("raw") or "ungültiger Wert"),
                    "bad",
                    _where(entry.get("subject")),
                )
                for entry in invalid
            ],
            target="Datum als JJJJ-MM-TT oder Zeitstempel JJJJ-MM-TTThh:mm:ss.",
        )

    return build


def _accrual_periodicity(details: Details, message: str) -> Finding:
    value = _text(details, "value")
    return Finding(
        headline=(
            "Die Aktualisierungsfrequenz steht nicht als URI aus dem kontrollierten Vokabular."
            if value
            else "Die Aktualisierungsfrequenz fehlt — Nutzende wissen nicht, ob sich ein erneuter Abruf lohnt."
        ),
        current=[FactLine("dct:accrualPeriodicity", value or "nicht gesetzt", "bad")],
        target="Eine Frequenz-URI aus dem EU-Vokabular, z. B. …/authority/frequency/ANNUAL.",
    )


def _download_url(details: Details, message: str) -> Finding:
    total = _num(details, "total_distributions")
    with_url = _num(details, "distributions_with_download_url")
    missing = total - with_url
    return Finding(
        headline=(
            f"Keine der {total} {_plural(total, 'Distribution', 'Distributionen')} "
            "hat einen direkten Download-Link."
            if with_url == 0
            else f"{missing} von {total} Distributionen {_plural(missing, 'hat', 'haben')} "
            "keinen direkten Download-Link."
        ),
        current=[
            FactLine("Distributionen gesamt", str(total), "neutral"),
            FactLine("davon mit dcat:downloadURL", str(with_url), "bad"),
        ],
        target=(
            "Je Distribution eine dcat:downloadURL, die direkt auf die Datei zeigt "
            "(nicht auf eine Webseite)."
        ),
    )


_TIER_TEXT = {
    "high": "gut maschinenlesbar",
    "mid": "eingeschränkt maschinenlesbar",
    "none": "nicht maschinenlesbar",
}


def _machine_readable(details: Details, message: str) -> Finding:
    total = _num(details, "total_distributions")
    high = _num(details, "high_count")
    none = _num(details, "none_count")
    if high == 0:
        headline = (
            f"Keine der {total} {_plural(total, 'Distribution', 'Distributionen')} "
            "liegt in einem gut maschinenlesbaren Format vor."
        )
    else:
        tail = (
            f", {none} {_plural(none, 'ist', 'sind')} gar nicht automatisiert verarbeitbar"
            if none > 0
            else ""
        )
        headline = (
            f"Nur {high} von {total} Distributionen {_plural(high, 'ist', 'sind')} "
            f"gut maschinenlesbar{tail}."
        )
    current = []
    for idx, entry in enumerate(_rows(details, "per_distribution"), start=1):
        tier = str(entry.get("tier_label", ""))
        current.append(
            FactLine(
                f"Distribution {idx}",
                f"{entry.get('effective_mime') or 'unbekanntes Format'} — {_TIER_TEXT.get(tier, tier)}",
                "good" if tier == "high" else "warn" if tier == "mid" else "bad",
                _where(entry.get("uri")),
            )
        )
    return Finding(
        headline=headline,
        current=current,
        target=(
            "Den Inhalt zusätzlich strukturiert anbieten (CSV, JSON, GeoJSON) "
            "statt nur als PDF, HTML oder Bilddienst."
        ),
    )


def _url_response(field: str) -> Builder:
    def build(details: Details, message: str) -> Finding:
        invalid = _rows(details, "invalid")
        valid_count = _num(details, "valid_count")
        relevant = _num(details, "relevant_distributions")
        if relevant == 0:
            return Finding(
                headline=f"Es gibt keine {field}, die geprüft werden könnte.",
                current=[FactLine(field, "bei keiner Distribution gesetzt", "bad")],
                target=f"Je Distribution eine erreichbare {field}.",
            )
        return Finding(
            headline=(
                f"{len(invalid)} von {relevant} {_plural(relevant, 'Link antwortet', 'Links antworten')} "
                f"nicht korrekt — {valid_count} {_plural(valid_count, 'ist', 'sind')} erreichbar."
            ),
            current=[
                FactLine(
                    f"HTTP {entry.get('status_code') or 'keine Antwort'}",
                    str(entry.get("url") or ""),
                    "bad",
                    _where(entry.get("uri")),
                )
                for entry in invalid
            ],
            target="Alle Links antworten mit einem Statuscode im Bereich 200–299.",
            notes=[
                f"{entry.get('url')}: {entry.get('fetch_error')}"
                for entry in invalid
                if entry.get("fetch_error")
            ],
        )

    return build


def _format_congruence(details: Details, message: str) -> Finding:
    inconsistent = _rows(details, "inconsistent")
    sampled = _num(details, "sampled_distributions")
    return Finding(
        headline=(
            f"Bei {len(inconsistent)} von {sampled} geprüften Distributionen widersprechen "
            "sich Formatangabe, Media Type und ausgelieferte Datei."
        ),
        current=[
            FactLine(
                f"Distribution {idx}",
                "; ".join(_strings(entry, "issues"))
                or f"gemeldet: {entry.get('coalesced') or 'unbekannt'}",
                "bad",
                _where(entry.get("download_url") or entry.get("access_url") or entry.get("uri")),
            )
            for idx, entry in enumerate(inconsistent, start=1)
        ],
        target=(
            "dct:format, dcat:mediaType, Dateiendung und der vom Server gemeldete "
            "Content-Type beschreiben dasselbe Format."
        ),
        notes=[
            w
            for entry in _rows(details, "warning_only")
            for w in _strings(entry, "warnings")
        ],
    )


def _distribution_model(details: Details, message: str) -> Finding:
    roles = details.get("role_counts") if isinstance(details.get("role_counts"), dict) else {}
    label = {
        "data_file": "Datendateien",
        "service_endpoint": "Dienste-Endpunkte",
        "landing_page": "Landing Pages",
        "archive": "Archive",
        "unknown": "nicht einzuordnen",
    }
    return Finding(
        headline=message or "Das Distributionsmodell des Datensatzes ist unvollständig.",
        current=[
            FactLine(label.get(key, key), str(count), "good" if count else "warn")
            for key, count in (roles or {}).items()
            if isinstance(count, int)
        ],
        target=(
            "Neben dem Dienst-Endpunkt mindestens eine herunterladbare Datendatei "
            "anbieten, damit Nutzende die Daten auch ohne Dienst verarbeiten können."
        ),
    )


def _access_rights(details: Details, message: str) -> Finding:
    count = _num(details, "access_rights_count")
    entries = _rows(details, "access_rights")
    return Finding(
        headline=(
            "Es ist nicht angegeben, ob der Datensatz öffentlich zugänglich ist."
            if count == 0
            else "Die Angabe zu den Zugriffsrechten stammt nicht aus dem EU-Vokabular."
        ),
        current=(
            [
                FactLine(
                    "dct:accessRights",
                    str(entry.get("uri") or entry.get("value") or entry.get("tier") or ""),
                    "bad",
                )
                for entry in entries
            ]
            if entries
            else [FactLine("dct:accessRights", "nicht gesetzt", "bad")]
        ),
        target="Eine URI aus dem EU-Vokabular, in der Regel …/authority/access-right/PUBLIC.",
    )


def _license(details: Details, message: str) -> Finding:
    total = _num(details, "total_distributions")
    free = _num(details, "free_count")
    malus = details.get("no_free_license_malus")
    missing = total - free
    current = [
        FactLine(
            f"Distribution {idx}",
            ", ".join(_strings(entry, "licenses")) or "keine Lizenz angegeben",
            "good" if entry.get("tier") == "free" else "bad",
            _where(entry.get("uri")),
        )
        for idx, entry in enumerate(_rows(details, "per_distribution"), start=1)
    ]
    return Finding(
        headline=(
            f"Keine der {total} {_plural(total, 'Distribution', 'Distributionen')} hat eine "
            "freie Lizenz — eine Weiterverwendung ist rechtlich nicht gedeckt."
            if free == 0
            else f"{missing} von {total} Distributionen {_plural(missing, 'hat', 'haben')} keine freie Lizenz."
        ),
        current=current,
        target=(
            "Je Distribution eine freie Lizenz als URI, z. B. "
            "http://dcat-ap.de/def/licenses/dl-zero-de/2.0."
        ),
        notes=(
            [f"Wegen fehlender freier Lizenz wurde ein Malus von {malus} auf den Score verrechnet."]
            if malus
            else []
        ),
    )


def _publisher(details: Details, message: str) -> Finding:
    count = _num(details, "publisher_count")
    return Finding(
        headline=(
            "Es ist kein Herausgeber angegeben — die Verantwortlichkeit für den Datensatz ist unklar."
            if count == 0
            else "Der Herausgeber ist nicht als strukturiertes Objekt mit Namen hinterlegt."
        ),
        current=[
            FactLine(
                "dct:publisher",
                "nicht gesetzt" if count == 0 else "gesetzt, aber ohne foaf:Agent bzw. foaf:name",
                "bad",
            )
        ],
        target="Ein foaf:Agent mit foaf:name, verlinkt über dct:publisher.",
    )


def _contact(details: Details, message: str) -> Finding:
    count = _num(details, "contact_count")
    with_channel = _num(details, "contacts_with_channel")
    return Finding(
        headline=(
            "Es ist kein Kontaktpunkt hinterlegt — Nutzende können Fehler nicht melden."
            if count == 0
            else "Der Kontaktpunkt enthält weder eine E-Mail-Adresse noch eine Kontakt-URL."
        ),
        current=[
            FactLine(
                "dcat:contactPoint",
                "nicht gesetzt" if count == 0 else f"{count} {_plural(count, 'Eintrag', 'Einträge')}",
                "bad" if count == 0 else "warn",
            ),
            FactLine("davon mit E-Mail oder URL", str(with_channel), "bad"),
        ],
        target="Ein vcard:Kind mit vcard:hasEmail (mailto:…) oder vcard:hasURL.",
    )


def _contributor_id(details: Details, message: str) -> Finding:
    values = _strings(details, "values")
    invalid = _strings(details, "invalid")
    count = _num(details, "contributor_id_count", len(values))
    if count == 0:
        headline = "Die Kennung des Datenbereitstellers fehlt."
    elif count > 1:
        headline = f"Es sind {count} Kennungen gesetzt — erlaubt ist genau eine."
    else:
        headline = "Die Kennung stammt nicht aus dem DCAT-AP.de-Vokabular."
    current = (
        [
            FactLine("dcatde:contributorID", v, "bad" if v in invalid else "good")
            for v in values
        ]
        if values
        else [FactLine("dcatde:contributorID", "nicht gesetzt", "bad")]
    )
    return Finding(
        headline=headline,
        current=current,
        target="Genau eine URI aus http://dcat-ap.de/def/contributors/.",
    )


def _shacl(details: Details, message: str) -> Finding:
    violations = _rows(details, "violations")
    count = _num(details, "violation_count", len(violations))
    return Finding(
        headline=(
            f"Der Metadatensatz verstößt an {count} {_plural(count, 'Stelle', 'Stellen')} "
            "gegen das DCAT-AP.de-Schema."
        ),
        current=[
            FactLine(
                "Warnung" if v.get("severity") == "Warning" else "Verstoß",
                str(v.get("message", "")).strip(),
                "warn" if v.get("severity") == "Warning" else "bad",
                v.get("path") if isinstance(v.get("path"), str) else _where(v.get("focus")),
            )
            for v in violations
        ],
        target="Keine Verstöße gegen DCAT-AP.de v2.0 — jede Meldung nennt das betroffene Feld.",
    )


def _llm_criterion(details: Details, message: str) -> Finding:
    """Aussagekraft-Indikatoren: das Urteil steht als Meldung, die Begründung
    Punkt für Punkt in ``details['findings']``."""
    return Finding(headline=message, notes=_strings(details, "findings"))


BUILDERS: Dict[str, Builder] = {
    "find_keywords_count": _keywords_count,
    "find_theme_valid": _theme_valid,
    "find_locn_geometry": _locn_geometry,
    "find_political_geocoding": _political_geocoding,
    "find_geocoding_level": _geocoding_level,
    "find_temporal_coverage": _temporal_coverage,
    "find_accrual_periodicity": _accrual_periodicity,
    "find_issued_datetime": _datetime_field("dct:issued"),
    "find_modified_datetime": _datetime_field("dct:modified"),
    "acc_download_url": _download_url,
    "acc_format": _distribution_builder(
        "formats",
        "ein Format aus dem EU-Vokabular",
        "kein Format angegeben",
        "Je Distribution eine Format-URI, z. B. "
        "http://publications.europa.eu/resource/authority/file-type/CSV.",
    ),
    "acc_media_type": _distribution_builder(
        "media_types",
        "einen gültigen Media Type",
        "kein Media Type angegeben",
        "Je Distribution eine IANA-URI, z. B. "
        "https://www.iana.org/assignments/media-types/text/csv.",
    ),
    "acc_format_non_proprietary": _distribution_builder(
        "formats",
        "ein offenes, herstellerunabhängiges Format",
        "kein Format angegeben",
        "Mindestens eine Distribution in einem offenen Format (z. B. CSV, JSON, GeoJSON, XML).",
    ),
    "reuse_availability": _distribution_builder(
        "availability",
        "eine Verfügbarkeitsangabe",
        "keine Angabe",
        "Je Distribution eine Verfügbarkeits-URI, z. B. …/planned-availability/STABLE.",
    ),
    "acc_machine_readable_access": _machine_readable,
    "acc_format_congruence": _format_congruence,
    "acc_distribution_model": _distribution_model,
    "reuse_access_rights": _access_rights,
    "acc_download_url_response": _url_response("dcat:downloadURL"),
    "acc_access_url_response": _url_response("dcat:accessURL"),
    "reuse_license": _license,
    "reuse_publisher": _publisher,
    "reuse_contact": _contact,
    "reuse_contributor_id": _contributor_id,
    "reuse_dcat_ap_de_compliance": _shacl,
    "expr_title_quality": _llm_criterion,
    "expr_description_quality": _llm_criterion,
    "expr_title_description_coherence": _llm_criterion,
    "expr_keyword_quality": _llm_criterion,
    "expr_thematic_consistency": _llm_criterion,
    "expr_contextual_qualifiers": _llm_criterion,
}


def build_finding(result: IndicatorResult) -> Optional[Finding]:
    """Befund zu einem Ergebnis, oder ``None`` wenn es nichts zu tun gibt.

    PASS und NOT_APPLICABLE liefern ``None`` — dort ist die Prüfmeldung die
    ganze Geschichte.
    """
    status = result.status
    if status in (IndicatorStatus.PASS, IndicatorStatus.NOT_APPLICABLE):
        return None

    if status is IndicatorStatus.ERROR or result.error:
        return Finding(
            headline="Dieser Indikator konnte nicht geprüft werden.",
            current=[FactLine("Fehler", result.error or "unbekannt", "warn")],
        )

    details = result.details or {}
    builder = BUILDERS.get(result.indicator_id)
    if builder is not None:
        finding = builder(details, result.message_de)
        if finding.target is None:
            guidance = guidance_for(result.indicator_id)
            finding.target = guidance.fix_de if guidance else None
        return finding

    # Unbekannter Indikator: Meldung und Handlungsanweisung reichen aus.
    guidance = guidance_for(result.indicator_id)
    return Finding(
        headline=result.message_de or (guidance.what_de if guidance else result.indicator_id),
        target=guidance.fix_de if guidance else None,
    )


def attach_finding(result: IndicatorResult) -> None:
    """Setzt ``result.finding`` in place. No-op für PASS / NOT_APPLICABLE."""
    result.finding = build_finding(result)
