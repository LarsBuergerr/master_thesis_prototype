// Übersetzt ein Indikator-Ergebnis in einen Befund, den ein Datenbereitsteller
// ohne DCAT-Kenntnisse abarbeiten kann.
//
// Die Prüfmeldung des Backends („0/3 Distribution(en) mit gültigem Media Type")
// sagt *dass* etwas fehlt, aber nicht *wo* und *wie es aussehen müsste*. Die
// `details` jedes Indikators enthalten diese Belege bereits — hier werden sie
// je Indikator in drei Blöcke gegossen:
//
//   ist   – was im Metadatensatz aktuell steht (mit Fundstelle)
//   soll  – was der Indikator erwartet
//   hinweise – konkrete Einzelbefunde (tote Links, SHACL-Verstöße, LLM-Kritik)
//
// Der Vorschlag im Diff-Format (aktueller Wert → Platzhalter aus dem
// Vokabular) kommt aus der `remediation` des Backends und wird von
// RemediationView gerendert.

import type { IndicatorResult } from "../api/types";
import { indicatorMeta } from "./indicators";

export type Tone = "bad" | "warn" | "good" | "neutral";

export interface FactLine {
  label: string;
  value: string;
  tone?: Tone;
  /** Fundstelle im Metadatensatz (Distributions-URI o. ä.). */
  where?: string;
}

export interface Finding {
  /** Ein Satz, der das Problem benennt. */
  headline: string;
  /** Ist-Zustand mit Fundstellen. */
  current: FactLine[];
  /** Soll-Zustand in einem Satz. */
  target?: string;
  /** Einzelbefunde: tote Links, Schema-Verstöße, Kritikpunkte des Sprachmodells. */
  notes: string[];
}

// ---------------------------------------------------------------------------
// Zugriffs-Helfer auf das lose typisierte `details`-Objekt
// ---------------------------------------------------------------------------

type Details = Record<string, unknown>;

const num = (d: Details, key: string): number | undefined =>
  typeof d[key] === "number" ? (d[key] as number) : undefined;

const str = (d: Details, key: string): string | undefined =>
  typeof d[key] === "string" ? (d[key] as string) : undefined;

const list = (d: Details, key: string): unknown[] =>
  Array.isArray(d[key]) ? (d[key] as unknown[]) : [];

const strList = (d: Details, key: string): string[] =>
  list(d, key).filter((v): v is string => typeof v === "string");

const rows = (d: Details, key: string): Details[] =>
  list(d, key).filter((v): v is Details => typeof v === "object" && v !== null);

/** Distributions-URIs enden auf „#distribution"; das ist für Menschen Rauschen. */
function whereLabel(uri: unknown): string | undefined {
  if (typeof uri !== "string" || !uri) return undefined;
  return uri.replace(/#distribution$/, "");
}

function quoteAll(values: string[], max = 6): string {
  const shown = values.slice(0, max).map((v) => `„${v}"`);
  const rest = values.length - shown.length;
  return shown.join(", ") + (rest > 0 ? ` … und ${rest} weitere` : "");
}

const plural = (n: number, one: string, many: string) => (n === 1 ? one : many);

// ---------------------------------------------------------------------------
// Distributions-Indikatoren: gleiche Struktur, unterschiedliches Wertfeld
// ---------------------------------------------------------------------------

/**
 * Baut den Ist-Block für alle Indikatoren mit `per_distribution`: je
 * Distribution der aktuelle Wert plus Fundstelle, damit klar ist, welche der
 * fünf Distributionen gemeint ist.
 */
function perDistribution(
  d: Details,
  valueKey: string,
  emptyText: string,
): FactLine[] {
  return rows(d, "per_distribution").map((entry, idx) => {
    const values = strList(entry, valueKey);
    const passes = entry.passes;
    return {
      label: `Distribution ${idx + 1}`,
      value: values.length ? values.join(", ") : emptyText,
      tone: passes === true ? "good" : ("bad" as Tone),
      where: whereLabel(entry.uri),
    };
  });
}

function distributionHeadline(d: Details, subject: string): string {
  const total = num(d, "total_distributions") ?? 0;
  const passing = num(d, "passing_count") ?? 0;
  if (total === 0) return `Es ist keine Distribution hinterlegt, ${subject} kann daher nicht geprüft werden.`;
  if (passing === 0) return `Keine der ${total} ${plural(total, "Distribution", "Distributionen")} hat ${subject}.`;
  return `${passing} von ${total} ${plural(total, "Distribution", "Distributionen")} ${plural(passing, "hat", "haben")} ${subject} — bei den übrigen fehlt sie.`;
}

// ---------------------------------------------------------------------------
// Befund je Indikator
// ---------------------------------------------------------------------------

function buildForIndicator(id: string, d: Details, message: string): Finding | null {
  switch (id) {
    // ---- Auffindbarkeit --------------------------------------------------
    case "find_keywords_count": {
      const count = num(d, "keyword_count") ?? 0;
      const keywords = strList(d, "keywords");
      return {
        headline:
          count === 0
            ? "Der Datensatz hat kein einziges Schlagwort — er ist über die Portalsuche kaum auffindbar."
            : count < 3
              ? `Nur ${count} ${plural(count, "Schlagwort", "Schlagwörter")} vergeben, empfohlen sind mindestens 3.`
              : `${count} Schlagwörter sind zu viele — die Trefferqualität sinkt.`,
        current: [
          {
            label: count === 0 ? "Schlagwörter" : `Aktuell ${count} ${plural(count, "Schlagwort", "Schlagwörter")}`,
            value: keywords.length ? quoteAll(keywords, 15) : "keine",
            tone: "bad",
          },
        ],
        target: "3 bis 15 Schlagwörter, die Thema, Region und Datenart benennen.",
        notes: [],
      };
    }

    case "find_theme_valid": {
      const invalid = strList(d, "invalid_themes");
      const valid = strList(d, "valid_themes");
      const count = num(d, "theme_count") ?? valid.length + invalid.length;
      return {
        headline:
          count === 0
            ? "Es ist keine Kategorie gesetzt — der Datensatz erscheint in keiner Themen-Facette."
            : `${invalid.length} von ${count} Kategorien stammen nicht aus dem EU-Vokabular und werden ignoriert.`,
        current: count === 0
          ? [{ label: "dcat:theme", value: "nicht gesetzt", tone: "bad" }]
          : [
              ...(valid.length ? [{ label: "Anerkannt", value: valid.join(", "), tone: "good" as Tone }] : []),
              ...(invalid.length ? [{ label: "Nicht anerkannt", value: invalid.join(", "), tone: "bad" as Tone }] : []),
            ],
        target: "Mindestens eine Kategorie als URI aus dem EU-Vokabular der 13 Datenkategorien.",
        notes: [],
      };
    }

    case "find_locn_geometry":
      return {
        headline: "Es ist kein Gebiet hinterlegt — der Datensatz taucht in Kartensuchen nicht auf.",
        current: [{ label: "locn:geometry", value: "nicht gesetzt", tone: "bad" }],
        target: "Eine Bounding Box oder ein Polygon als WKT oder GeoJSON, z. B. POLYGON ((9.25 52.16, …)).",
        notes: [],
      };

    case "find_political_geocoding": {
      const count = num(d, "geocoding_count") ?? 0;
      const uri = str(d, "uri");
      return {
        headline: count === 0
          ? "Es ist kein Verwaltungsgebiet angegeben — eine Suche nach Ortsnamen findet den Datensatz nicht."
          : "Das angegebene Verwaltungsgebiet stammt nicht aus dem DCAT-AP.de-Vokabular.",
        current: [
          {
            label: "dcatde:politicalGeocodingURI",
            value: uri ?? "nicht gesetzt",
            tone: "bad",
          },
        ],
        target:
          "Eine URI aus dem DCAT-AP.de-Geokodierungs-Vokabular, z. B. http://dcat-ap.de/def/politicalGeocoding/municipalityKey/07131038.",
        notes: [],
      };
    }

    case "find_geocoding_level": {
      const count = num(d, "level_count") ?? 0;
      const invalid = strList(d, "invalid");
      return {
        headline: count === 0
          ? "Die Ebene des Verwaltungsgebiets fehlt — Suchfilter können den Raumbezug nicht einordnen."
          : "Nicht alle angegebenen Ebenen stammen aus dem kontrollierten Vokabular.",
        current: [
          {
            label: "dcatde:politicalGeocodingLevelURI",
            value: invalid.length ? invalid.join(", ") : "nicht gesetzt",
            tone: "bad",
          },
        ],
        target:
          "Eine Ebenen-URI, z. B. http://dcat-ap.de/def/politicalGeocoding/Level/municipality.",
        notes: [],
      };
    }

    case "find_temporal_coverage": {
      const startCount = num(d, "start_count") ?? 0;
      const endCount = num(d, "end_count") ?? 0;
      const startValid = d.start_valid === true;
      const endValid = d.end_valid === true;
      const missing = startCount === 0 && endCount === 0;
      return {
        headline: missing
          ? "Der Zeitraum der Daten ist nicht angegeben — Nutzende können die Aktualität nicht einschätzen."
          : "Der angegebene Zeitraum ist unvollständig oder kein gültiges Datum.",
        current: [
          {
            label: "dcat:startDate",
            value: startCount === 0 ? "nicht gesetzt" : startValid ? "gesetzt und gültig" : `gesetzt, aber ungültiges Format (${str(d, "start_format") ?? "unbekannt"})`,
            tone: startValid ? "good" : "bad",
          },
          {
            label: "dcat:endDate",
            value: endCount === 0 ? "nicht gesetzt" : endValid ? "gesetzt und gültig" : `gesetzt, aber ungültiges Format (${str(d, "end_format") ?? "unbekannt"})`,
            tone: endValid ? "good" : "bad",
          },
        ],
        target: "Start- und Enddatum im Format JJJJ-MM-TT (oder als vollständiger Zeitstempel).",
        notes: [],
      };
    }

    case "find_issued_datetime":
    case "find_modified_datetime": {
      const total = num(d, "total") ?? 0;
      const invalid = rows(d, "invalid");
      const field = id === "find_issued_datetime" ? "dct:issued" : "dct:modified";
      return {
        headline: total === 0
          ? `${field} ist nicht gesetzt — es ist nicht erkennbar, wie aktuell der Datensatz ist.`
          : `${invalid.length} ${plural(invalid.length, "Wert entspricht", "Werte entsprechen")} nicht dem erwarteten Datumsformat.`,
        current: total === 0
          ? [{ label: field, value: "nicht gesetzt", tone: "bad" }]
          : invalid.map((entry) => ({
              label: field,
              value: String(entry.value ?? entry.raw ?? "ungültiger Wert"),
              tone: "bad" as Tone,
              where: whereLabel(entry.subject),
            })),
        target: "Datum als JJJJ-MM-TT oder Zeitstempel JJJJ-MM-TTThh:mm:ss.",
        notes: [],
      };
    }

    case "find_accrual_periodicity":
      return {
        headline: str(d, "value")
          ? "Die Aktualisierungsfrequenz steht nicht als URI aus dem kontrollierten Vokabular."
          : "Die Aktualisierungsfrequenz fehlt — Nutzende wissen nicht, ob sich ein erneuter Abruf lohnt.",
        current: [
          { label: "dct:accrualPeriodicity", value: str(d, "value") ?? "nicht gesetzt", tone: "bad" },
        ],
        target: "Eine Frequenz-URI aus dem EU-Vokabular, z. B. …/authority/frequency/ANNUAL.",
        notes: [],
      };

    // ---- Zugänglichkeit --------------------------------------------------
    case "acc_download_url": {
      const total = num(d, "total_distributions") ?? 0;
      const withUrl = num(d, "distributions_with_download_url") ?? 0;
      return {
        headline: withUrl === 0
          ? `Keine der ${total} ${plural(total, "Distribution", "Distributionen")} hat einen direkten Download-Link.`
          : `${total - withUrl} von ${total} Distributionen ${plural(total - withUrl, "hat", "haben")} keinen direkten Download-Link.`,
        current: [
          { label: "Distributionen gesamt", value: String(total), tone: "neutral" },
          { label: "davon mit dcat:downloadURL", value: String(withUrl), tone: "bad" },
        ],
        target: "Je Distribution eine dcat:downloadURL, die direkt auf die Datei zeigt (nicht auf eine Webseite).",
        notes: [],
      };
    }

    case "acc_format":
      return {
        headline: distributionHeadline(d, "ein Format aus dem EU-Vokabular"),
        current: perDistribution(d, "formats", "kein Format angegeben"),
        target: "Je Distribution eine Format-URI, z. B. http://publications.europa.eu/resource/authority/file-type/CSV.",
        notes: [],
      };

    case "acc_media_type":
      return {
        headline: distributionHeadline(d, "einen gültigen Media Type"),
        current: perDistribution(d, "media_types", "kein Media Type angegeben"),
        target: "Je Distribution eine IANA-URI, z. B. https://www.iana.org/assignments/media-types/text/csv.",
        notes: [],
      };

    case "acc_format_non_proprietary":
      return {
        headline: distributionHeadline(d, "ein offenes, herstellerunabhängiges Format"),
        current: perDistribution(d, "formats", "kein Format angegeben"),
        target: "Mindestens eine Distribution in einem offenen Format (z. B. CSV, JSON, GeoJSON, XML).",
        notes: [],
      };

    case "reuse_availability":
      return {
        headline: distributionHeadline(d, "eine Verfügbarkeitsangabe"),
        current: perDistribution(d, "availability", "keine Angabe"),
        target: "Je Distribution eine Verfügbarkeits-URI, z. B. …/planned-availability/STABLE.",
        notes: [],
      };

    case "acc_machine_readable_access": {
      const total = num(d, "total_distributions") ?? 0;
      const high = num(d, "high_count") ?? 0;
      const none = num(d, "none_count") ?? 0;
      const tierText: Record<string, string> = {
        high: "gut maschinenlesbar",
        mid: "eingeschränkt maschinenlesbar",
        none: "nicht maschinenlesbar",
      };
      return {
        headline: high === 0
          ? `Keine der ${total} ${plural(total, "Distribution", "Distributionen")} liegt in einem gut maschinenlesbaren Format vor.`
          : `Nur ${high} von ${total} Distributionen ${plural(high, "ist", "sind")} gut maschinenlesbar${none > 0 ? `, ${none} ${plural(none, "ist", "sind")} gar nicht automatisiert verarbeitbar` : ""}.`,
        current: rows(d, "per_distribution").map((entry, idx) => ({
          label: `Distribution ${idx + 1}`,
          value: `${String(entry.effective_mime ?? "unbekanntes Format")} — ${tierText[String(entry.tier_label)] ?? String(entry.tier_label ?? "")}`,
          tone: entry.tier_label === "high" ? "good" : entry.tier_label === "mid" ? "warn" : "bad",
          where: whereLabel(entry.uri),
        })),
        target: "Den Inhalt zusätzlich strukturiert anbieten (CSV, JSON, GeoJSON) statt nur als PDF, HTML oder Bilddienst.",
        notes: [],
      };
    }

    case "acc_download_url_response":
    case "acc_access_url_response": {
      const invalid = rows(d, "invalid");
      const validCount = num(d, "valid_count") ?? 0;
      const relevant = num(d, "relevant_distributions") ?? 0;
      const field = id === "acc_download_url_response" ? "dcat:downloadURL" : "dcat:accessURL";
      if (relevant === 0) {
        return {
          headline: `Es gibt keine ${field}, die geprüft werden könnte.`,
          current: [{ label: field, value: "bei keiner Distribution gesetzt", tone: "bad" }],
          target: `Je Distribution eine erreichbare ${field}.`,
          notes: [],
        };
      }
      return {
        headline: `${invalid.length} von ${relevant} ${plural(relevant, "Link antwortet", "Links antworten")} nicht korrekt — ${validCount} ${plural(validCount, "ist", "sind")} erreichbar.`,
        current: invalid.map((entry) => ({
          label: `HTTP ${entry.status_code ?? "keine Antwort"}`,
          value: String(entry.url ?? ""),
          tone: "bad" as Tone,
          where: whereLabel(entry.uri),
        })),
        target: "Alle Links antworten mit einem Statuscode im Bereich 200–299.",
        notes: invalid
          .map((entry) => (entry.fetch_error ? `${entry.url}: ${entry.fetch_error}` : ""))
          .filter(Boolean) as string[],
      };
    }

    // ---- Nachnutzbarkeit -------------------------------------------------
    case "reuse_license": {
      const total = num(d, "total_distributions") ?? 0;
      const free = num(d, "free_count") ?? 0;
      const malus = num(d, "no_free_license_malus");
      return {
        headline: free === 0
          ? `Keine der ${total} ${plural(total, "Distribution", "Distributionen")} hat eine freie Lizenz — eine Weiterverwendung ist rechtlich nicht gedeckt.`
          : `${total - free} von ${total} Distributionen ${plural(total - free, "hat", "haben")} keine freie Lizenz.`,
        current: rows(d, "per_distribution").map((entry, idx) => ({
          label: `Distribution ${idx + 1}`,
          value: strList(entry, "licenses").join(", ") || "keine Lizenz angegeben",
          tone: entry.tier === "free" ? "good" : "bad",
          where: whereLabel(entry.uri),
        })),
        target: "Je Distribution eine freie Lizenz als URI, z. B. http://dcat-ap.de/def/licenses/dl-zero-de/2.0.",
        notes: malus
          ? [`Wegen fehlender freier Lizenz wurde ein Malus von ${malus} auf den Score verrechnet.`]
          : [],
      };
    }

    case "reuse_publisher":
      return {
        headline: (num(d, "publisher_count") ?? 0) === 0
          ? "Es ist kein Herausgeber angegeben — die Verantwortlichkeit für den Datensatz ist unklar."
          : "Der Herausgeber ist nicht als strukturiertes Objekt mit Namen hinterlegt.",
        current: [
          {
            label: "dct:publisher",
            value: (num(d, "publisher_count") ?? 0) === 0 ? "nicht gesetzt" : "gesetzt, aber ohne foaf:Agent bzw. foaf:name",
            tone: "bad",
          },
        ],
        target: "Ein foaf:Agent mit foaf:name, verlinkt über dct:publisher.",
        notes: [],
      };

    case "reuse_contact": {
      const count = num(d, "contact_count") ?? 0;
      const withChannel = num(d, "contacts_with_channel") ?? 0;
      return {
        headline: count === 0
          ? "Es ist kein Kontaktpunkt hinterlegt — Nutzende können Fehler nicht melden."
          : "Der Kontaktpunkt enthält weder eine E-Mail-Adresse noch eine Kontakt-URL.",
        current: [
          { label: "dcat:contactPoint", value: count === 0 ? "nicht gesetzt" : `${count} ${plural(count, "Eintrag", "Einträge")}`, tone: count === 0 ? "bad" : "warn" },
          { label: "davon mit E-Mail oder URL", value: String(withChannel), tone: "bad" },
        ],
        target: "Ein vcard:Kind mit vcard:hasEmail (mailto:…) oder vcard:hasURL.",
        notes: [],
      };
    }

    case "reuse_contributor_id": {
      const values = strList(d, "values");
      const invalid = strList(d, "invalid");
      const count = num(d, "contributor_id_count") ?? values.length;
      return {
        headline: count === 0
          ? "Die Kennung des Datenbereitstellers fehlt."
          : count > 1
            ? `Es sind ${count} Kennungen gesetzt — erlaubt ist genau eine.`
            : "Die Kennung stammt nicht aus dem DCAT-AP.de-Vokabular.",
        current: values.length
          ? values.map((v) => ({
              label: "dcatde:contributorID",
              value: v,
              tone: invalid.includes(v) ? ("bad" as Tone) : ("good" as Tone),
            }))
          : [{ label: "dcatde:contributorID", value: "nicht gesetzt", tone: "bad" as Tone }],
        target: "Genau eine URI aus http://dcat-ap.de/def/contributors/.",
        notes: [],
      };
    }

    case "reuse_dcat_ap_de_compliance": {
      const violations = rows(d, "violations");
      const count = num(d, "violation_count") ?? violations.length;
      return {
        headline: `Der Metadatensatz verstößt an ${count} ${plural(count, "Stelle", "Stellen")} gegen das DCAT-AP.de-Schema.`,
        current: violations.map((v) => ({
          label: String(v.severity ?? "Violation") === "Warning" ? "Warnung" : "Verstoß",
          value: String(v.message ?? "").trim(),
          tone: String(v.severity) === "Warning" ? ("warn" as Tone) : ("bad" as Tone),
          where: typeof v.path === "string" ? v.path : whereLabel(v.focus),
        })),
        target: "Keine Verstöße gegen DCAT-AP.de v2.0 — jede Meldung nennt das betroffene Feld.",
        notes: [],
      };
    }

    // ---- Aussagekraft (LLM) ----------------------------------------------
    case "expr_title_quality":
    case "expr_description_quality":
    case "expr_title_description_coherence":
    case "expr_keyword_quality":
    case "expr_thematic_consistency":
    case "expr_contextual_qualifiers": {
      const findings = strList(d, "findings");
      const meta = indicatorMeta(id);
      return {
        headline: message || meta.what,
        current: [],
        target: meta.fix,
        notes: findings,
      };
    }

    default:
      return null;
  }
}

/**
 * Befund zu einem Indikator-Ergebnis. Für bestandene Indikatoren gibt es
 * nichts zu tun — dort liefert die Funktion `null`, damit die Tabelle
 * schlank bleibt.
 */
export function buildFinding(indicator: IndicatorResult): Finding | null {
  if (indicator.status === "pass" || indicator.status === "not_applicable") return null;

  if (indicator.status === "error" || indicator.error) {
    return {
      headline: "Dieser Indikator konnte nicht geprüft werden.",
      current: [{ label: "Fehler", value: indicator.error ?? "unbekannt", tone: "warn" }],
      notes: [],
    };
  }

  const details = (indicator.details ?? {}) as Details;
  const finding = buildForIndicator(indicator.indicator_id, details, indicator.message_de);
  if (finding) return finding;

  // Unbekannter Indikator: wenigstens Meldung und Handlungsanweisung zeigen.
  const meta = indicatorMeta(indicator.indicator_id, indicator.name_de);
  return {
    headline: indicator.message_de || meta.what,
    current: [],
    target: meta.fix,
    notes: [],
  };
}
