# DCAT-AP-DE Metadata Quality Prototype

A research prototype (master's thesis) that automatically assesses the **quality
of open-data metadata** described in [DCAT-AP-DE](https://www.dcat-ap.de/).
It parses RDF/XML metadata records, scores them against a catalogue of quality
indicators grouped into four dimensions, and turns every failed check into a
plain-language finding with a concrete instruction on how to fix it.

Most indicators are **deterministic** (structural checks, controlled-vocabulary
lookups, HTTP reachability probes). The _expressiveness_ dimension is scored by a
single **LLM call** per dataset, because judging whether a title or description is
_meaningful_ cannot be done with rules alone.

The repository holds three parts that build on each other:

| Part            | Where       | What it is                                                                                                |
| --------------- | ----------- | --------------------------------------------------------------------------------------------------------- |
| **Analyzer**    | `src/`      | The scoring engine. Runs from the command line over a directory of RDF files and writes JSON reports.     |
| **Backend API** | `backend/`  | A FastAPI wrapper around the analyzer. Serves metadata catalogues, completed runs and on-demand analyses. |
| **Frontend**    | `frontend/` | A GovData-style portal mock that shows the metadata and lays a quality assessment over it.                |

---

## Table of contents

- [Quality model](#quality-model)
- [Indicator catalogue](#indicator-catalogue)
- [Findings](#findings)
- [Project structure](#project-structure)
- [How a run works](#how-a-run-works)
- [Web application](#web-application)
- [Setup](#setup)
- [Running](#running)
- [Configuration reference](#configuration-reference)
- [Output](#output)
- [Extending the prototype](#extending-the-prototype)
- [Troubleshooting](#troubleshooting)

---

## Quality model

Quality is decomposed into four dimensions (German term in parentheses — the
dimension keys used in config are the English values):

| Key              | Dimension       | Question it answers                                                                                            |
| ---------------- | --------------- | -------------------------------------------------------------------------------------------------------------- |
| `findability`    | Auffindbarkeit  | Can the dataset be found through relevant metadata (keywords, themes, spatial/temporal coverage, dates)?       |
| `accessibility`  | Zugänglichkeit  | Are the data accessible in usable formats and technically reachable (URLs, formats, media types, HTTP probes)? |
| `reusability`    | Nachnutzbarkeit | Can the data be reused under clear terms (license, access rights, structured publisher & contact)?             |
| `expressiveness` | Aussagekraft    | Are the metadata meaningful and self-consistent (title/description quality, coherence)? — **LLM-scored**       |

### Scoring

Each indicator returns a **status** and a **score in `[0.0, 1.0]`**:

| Status           | Meaning                                                                                                           |
| ---------------- | ----------------------------------------------------------------------------------------------------------------- |
| `pass`           | All requirements met                                                                                              |
| `partial`        | Some requirements met / mixed results                                                                             |
| `fail`           | Requirements not met or field missing                                                                             |
| `not_applicable` | Cannot / need not be evaluated (no LLM configured, or a criterion the model marks not applicable to this dataset) |
| `error`          | Exception during validation                                                                                       |

**How the status maps to the numeric score** (under a `ScorePolicy`, the default):

- **Ternary indicators** (most): `pass` → `pass_score` (default `1.0`),
  `partial` → `partial_score` (`0.5`), `fail` → `fail_score` (`0.0`). All three
  are tunable globally and per indicator.
- **Graded indicators** contribute their **raw continuous score regardless of
  status** — the `pass`/`partial`/`fail` label is presentational, so the
  aggregate stays a smooth function of the measurement. Two groups:
  - `expr_*` — a continuous LLM criterion score in `[0, 1]` per dataset (the
    label is derived from that score; see the Expressiveness section).
  - **Per-distribution** indicators — score each distribution (+1 / 0 or a tier)
    and average over all distributions: `acc_download_url`, `acc_format`,
    `acc_media_type`, `acc_format_non_proprietary`, `acc_download_url_response`,
    `acc_access_url_response`, `acc_machine_readable_access`, `reuse_license`,
    `reuse_availability`, `find_issued_datetime`, `find_modified_datetime`.
- **Per-distribution malus:** some graded indicators score a _negative_ value
  for a failing distribution (dead URL, restricted/missing license), so a bad
  distribution actively drags the mean down instead of just scoring low:
  `acc_download_url_response`, `acc_access_url_response` (−0.5 per dead URL),
  `reuse_license` (−0.5 per non-free distribution). A dimension score is floored
  at 0, so the overall score never goes negative. `acc_machine_readable_access`
  deliberately carries **no** malus — non-machine-readable distributions often
  supplement a machine-readable one (docs, map views), so a _none_ tier scores 0
  instead of pulling the mean below it.

The **Scoring** column in each catalogue table below states the per-indicator
rule.

> Under the default score policy (`pass 1.0 / partial 0.5 / fail 0.0`,
> `allow_partial: true`, no overrides) the mapping is the **identity**: the
> policy-applied `score` equals the indicator's `raw_score` for every result.
> The two only diverge once a config changes the policy — a negative
> `fail_score`, `allow_partial: false`, or a per-indicator override.

Scores aggregate bottom-up:

1. **Dimension score** = weighted average of its indicator scores, using each
   indicator's _effective weight_ (`indicator_weights[id]` if set, else the
   indicator's default weight of `1.0`).
2. **Overall score** = weighted average of the dimension scores. If no custom
   `dimension_weights` are set (block omitted, or every value left at `1.0`),
   each dimension is weighted by the **total weight of its indicators** — so the
   overall score is exactly the weighted mean over _all_ indicators and the
   dimension level needs no separate weighting rationale. Setting any dimension
   weight ≠ `1.0` switches to explicit per-dimension weighting
   (`dimension_weights[dim]`). The summary reports which mode was used via
   `dimension_weight_mode`.
3. **Grade** is derived from the overall score:

   | Score ≥ | Grade |
   | ------- | ----- |
   | 0.90    | A     |
   | 0.75    | B     |
   | 0.60    | C     |
   | 0.40    | D     |
   | else    | F     |

> Note: an indicator's _score_ (continuous) and its _pass count_ are tracked
> separately — `pass_rate` counts only `pass` statuses, while the dimension
> score uses the continuous score of every indicator including `partial`.

---

## Indicator catalogue

**31 indicators** are registered across the four dimensions. The IDs are the keys
you use in `indicator_whitelist` / `indicator_blacklist` / `indicator_weights`;
which of them a given run executes is decided entirely by its config (see
[Selecting what to run](#selecting-what-to-run)).

Most Findability indicators are **ternary**; `find_issued_datetime` and
`find_modified_datetime` are **graded** (fraction of present date values that
are validly typed).

### Findability (9)

| ID                         | Checks                                                                                                                         | Scoring                                                                                  | RDF field(s)                                       | Net/LLM |
| -------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | -------------------------------------------------- | ------- |
| `find_keywords_count`      | Keyword count in a healthy range (≈3–15)                                                                                       | PASS 3–15 · PARTIAL 1–2 or 16–25 · FAIL 0 or >25                                         | `dcat:keyword`                                     | —       |
| `find_theme_valid`         | Theme present **and** from the EU data-theme vocabulary                                                                        | PASS all themes in vocab · PARTIAL some not in vocab · FAIL none                         | `dcat:theme`                                       | —       |
| `find_locn_geometry`       | Spatial geometry present                                                                                                       | PASS present · FAIL absent                                                               | `locn:geometry`                                    | —       |
| `find_political_geocoding` | Political geocoding references the DCAT-AP-DE vocabulary (primary `dcatde:politicalGeocodingURI`, fallback `locn:adminUnitL2`) | PASS URI in vocab · PARTIAL present-not-vocab or only adminUnitL2 fallback · FAIL absent | `dcatde:politicalGeocodingURI`, `locn:adminUnitL2` | —       |
| `find_geocoding_level`     | Political geocoding **level** from the DCAT-AP-DE level vocabulary (Konvention 09)                                             | PASS in vocab · PARTIAL present but not in vocab · FAIL absent                           | `dcatde:politicalGeocodingLevelURI`                | —       |
| `find_temporal_coverage`   | Temporal coverage present with a valid `xsd:date`/`dateTime`                                                                   | PASS valid start or end date · FAIL absent/invalid                                       | `dcat:startDate`, `dcat:endDate`                   | —       |
| `find_issued_datetime`     | `issued` is a valid date/dateTime (dataset + distributions)                                                                    | **Graded** = fraction of present values validly typed; FAIL if absent                    | `dct:issued`                                       | —       |
| `find_modified_datetime`   | `modified` is a valid date/dateTime (dataset + distributions)                                                                  | **Graded** = fraction of present values validly typed; FAIL if absent                    | `dct:modified`                                     | —       |
| `find_accrual_periodicity` | Update frequency present and (where possible) from controlled vocabulary                                                       | PASS present & in vocab · PARTIAL present not in vocab · FAIL absent                     | `dct:accrualPeriodicity`                           | —       |

### Accessibility (9)

| ID                            | Checks                                                                                              | Scoring                                                                                                                                                             | RDF field(s)                                                         | Net/LLM         |
| ----------------------------- | --------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- | --------------- |
| `acc_download_url`            | Fraction of distributions declaring a download URL                                                  | **Graded** = fraction with a downloadURL (per dist +1/0, no malus); label PASS ≥ 0.9 · PARTIAL ≥ 0.5                                                                | `dcat:downloadURL`                                                   | —               |
| `acc_format`                  | Fraction of distributions with a format from the EU file-type vocabulary                            | **Graded** = fraction with valid format (per dist +1/0, no malus); label PASS ≥ 0.9 · PARTIAL ≥ 0.5                                                                 | `dct:format`                                                         | —               |
| `acc_media_type`              | Fraction of distributions with a mediaType as IANA URI from the vocabulary                          | **Graded** = fraction with valid mediaType (per dist +1/0, no malus); label PASS ≥ 0.9 · PARTIAL ≥ 0.5                                                              | `dcat:mediaType`                                                     | —               |
| `acc_format_non_proprietary`  | Fraction of distributions declaring a non-proprietary format URI (EU file-type vocabulary)          | **Graded** = fraction non-proprietary (per dist +1/0, no malus); label PASS ≥ 0.9 · PARTIAL ≥ 0.5                                                                   | `dct:format`                                                         | —               |
| `acc_download_url_response`   | Reachability of each distribution's download URL (HTTP `< 400`)                                     | **Graded** = mean of per-dist +1 (reachable) / **−0.5 (dead, malus)**; label PASS ≥ 0.9 · PARTIAL ≥ 0.5                                                             | `dcat:downloadURL`                                                   | **HTTP**        |
| `acc_access_url_response`     | Reachability of each distribution's access URL (HTTP `< 400`)                                       | **Graded** = mean of per-dist +1 (reachable) / **−0.5 (dead, malus)**; label PASS ≥ 0.9 · PARTIAL ≥ 0.5                                                             | `dcat:accessURL`                                                     | **HTTP**        |
| `acc_machine_readable_access` | Machine-readable access per distribution (CSV/JSON/XML > service > archive > HTML/PDF)              | **Graded** = mean per-dist tier high +1 / mid +0.5 / none 0 (no malus); label PASS ≥ 0.8 · PARTIAL ≥ 0.4                                                            | `dcat:accessURL`, `dcat:downloadURL`, `dct:format`, `dcat:mediaType` | HTTP (optional) |
| `acc_format_congruence`       | Declared format/media-type agree with the actual HTTP `Content-Type` and URL extension              | **Graded** = mean per-dist 1.0 congruent / 0.7 congruent-with-warnings / 0.0 conflicting (unprobed distributions are not counted); label PASS ≥ 0.9 · PARTIAL ≥ 0.5 | `dct:format`, `dcat:mediaType` + HTTP                                | **HTTP**        |
| `acc_distribution_model`      | Distributions follow the DCAT pattern (one dataset, multiple formats) vs. a split-data anti-pattern | **Graded**, multi-tier 1.0 / 0.6 / 0.4 / 0.0 by how clearly the data files read as format variants of one dataset                                                   | distribution properties                                              | —               |

### Reusability (7)

`reuse_license` and `reuse_availability` are **graded** (per-distribution mean);
the rest are **ternary**.

| ID                            | Checks                                                                                                | Scoring                                                                                                            | RDF field(s)           | Net/LLM  |
| ----------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------- | -------- |
| `reuse_license`               | Free-use license per distribution from the DCAT-AP-DE vocabulary (Konvention 32)                      | **Graded** = mean per-dist free +1 / **restricted·unknown·missing −0.5 (malus)**; label PASS ≥ 0.9 · PARTIAL ≥ 0.5 | `dct:license`          | —        |
| `reuse_access_rights`         | `accessRights` references a `RightsStatement` URI from the controlled vocabulary                      | PASS URI in vocab · PARTIAL set but not in vocab · FAIL absent                                                     | `dct:accessRights`     | —        |
| `reuse_publisher`             | Publisher typed as `foaf:Agent` **and** carries an `foaf:name`                                        | PASS Agent + name · PARTIAL one of the two · FAIL neither / absent                                                 | `dct:publisher`        | —        |
| `reuse_contact`               | Contact point carries a valid email **or** URL (DCAT-AP-DE Konvention 01)                             | PASS valid email or URL · PARTIAL contact but neither · FAIL no contact                                            | `dcat:contactPoint`    | —        |
| `reuse_availability`          | Fraction of distributions with a `dcatap:availability` value from the Planned Availability vocab      | **Graded** = fraction valid (per dist +1/0, no malus); label PASS ≥ 0.9 · PARTIAL ≥ 0.5                            | `dcatap:availability`  | —        |
| `reuse_contributor_id`        | `dcatde:contributorID` present, exactly one IRI from the contributors vocabulary (DCAT-AP-DE K12/K13) | PASS exactly one IRI in vocab · FAIL absent / not in vocab / multiple                                              | `dcatde:contributorID` | —        |
| `reuse_dcat_ap_de_compliance` | Zero SHACL violations against DCAT-AP.de v2.0 rules via ITB API                                       | PASS 0 violations · FAIL ≥ 1 violation (binary)                                                                    | all fields             | **HTTP** |

### Expressiveness (6) — LLM-scored

All six read their slice from **one** `ExpressivenessAssessment` produced per
dataset by a single LLM call. With no LLM configured they all report
`not_applicable` (no tokens spent). The German prompt's per-criterion rubric
lives in the assessment schema's field descriptions (DCAT-AP.de conventions
handbook 1.7/3.4 + the Handreichung zur Metadatenqualität).

All six are **graded**. Per criterion the LLM records observable `findings` →
`reasoning` → an `applicable` flag → a continuous `score` in `[0, 1]` (used
directly in the aggregate). The `pass`/`partial`/`fail` **label is derived from
the score** (pass ≥ 0.8, partial ≥ 0.5, else fail) — the model never sets the
label, so it can't contradict the score. A criterion the model judges **not
applicable** to the dataset (mainly contextual qualifiers on a one-off static
dataset) reports `not_applicable` and is skipped neutrally instead of penalised.

| ID                                 | Checks                                                                                                                       | Scoring                                                                     | RDF field(s)                                                 |
| ---------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------ |
| `expr_title_quality`               | Title descriptive & specific for itself (no cryptic codes/abbreviations, no methodology, not just the publisher name)        | Graded 0–1 (LLM); label derived; NA without LLM                             | `dct:title`                                                  |
| `expr_description_quality`         | Description substantive for itself (what/how-structured/how-collected/purpose/particulars)                                   | Graded 0–1 (LLM); label derived; NA without LLM                             | `dct:description`                                            |
| `expr_title_description_coherence` | Title and description agree and reinforce each other                                                                         | Graded 0–1 (LLM); label derived; NA without LLM                             | `dct:title`, `dct:description`                               |
| `expr_keyword_quality`             | Keywords relevant, specific, singular, layperson-friendly, non-redundant (count checked separately, not here)                | Graded 0–1 (LLM); label derived; NA without LLM                             | `dcat:keyword`                                               |
| `expr_thematic_consistency`        | Theme, keywords, title and description form a coherent subject picture                                                       | Graded 0–1 (LLM); label derived; NA without LLM                             | `dcat:theme`, `dcat:keyword`, `dct:title`, `dct:description` |
| `expr_contextual_qualifiers`       | Needed qualifiers (reference period, cutoff date, provisional/estimated/draft …) present **where the content requires them** | Graded 0–1 (LLM); label derived; **NA when no qualifier required** / no LLM | `dct:issued`, `dct:modified`, `dct:description`              |

### Controlled vocabularies

Bundled under [src/extraction/vocabularies/](src/extraction/vocabularies/) and
loaded once at startup (paths resolve relative to the package, so they travel
with it): EU data themes, frequencies, file types, access rights and
LimitationsOnPublicAccess; DCAT-AP-DE licenses; IANA media types
([media_types.csv](src/extraction/vocabularies/media_types.csv)); and the full
DCAT-AP-DE political-geocoding key set (state/district/municipality/…).

---

## Findings

A score alone does not tell a data provider _what_ is wrong. Every `fail`,
`partial` or `error` result therefore carries a **finding**, attached inside the
scoring run so that CLI reports and the web frontend show exactly the same text.

[`core/finding.py`](src/core/finding.py) defines a single shape that all 31
indicators map onto, even though their raw `details` differ wildly:

| Field      | Content                                                                               |
| ---------- | ------------------------------------------------------------------------------------- |
| `headline` | One sentence naming the problem                                                       |
| `current`  | What the record says right now — label, value, tone, and the location it was found at |
| `target`   | What it would have to look like                                                       |
| `notes`    | Individual observations (dead links, SHACL violations, LLM critique)                  |

Built by [`scoring/findings.py`](src/scoring/findings.py) via
`attach_finding()`. Indicator-specific builders translate the evidence; a
missing builder falls back to the check message plus the indicator's guidance.
`pass` and `not_applicable` results get no finding — there is nothing to do.

Plain-language labels, field names and vocabulary links per indicator live in
[`core/guidance.py`](src/core/guidance.py) and are served to the frontend
through `GET /indicators`.

> **Note on the reference runs.** An earlier version additionally produced a
> structured `remediation` payload (`ChangePatch` / `Recommendation`); it was
> removed in August 2026. The committed reference runs under `outputs/runs/`
> were produced in July 2026 and therefore still carry a `remediation` key and
> no `finding` — the current code is the other way round.

---

## Project structure

```
src/                           # The analyzer (no web, no UI)
  main.py                      # Entry point: Hydra config, LLM wiring, the per-file run loop
  core/                        # Domain model — pure, no I/O
    indicator.py               #   Indicator base class + registry, IndicatorResult, IndicatorStatus
    dimension.py               #   QualityDimension enum + Dimension metadata
    finding.py                 #   Finding / FactLine — the Ist/Soll shape of a failed check
    guidance.py                #   Plain-language text per indicator (label, field, fix, vocabulary)
  extraction/                  # RDF graph → typed facts (+ enrichment)
    rdf_parser.py              #   Load an RDF/XML file into an rdflib Graph
    dataset_context.py         #   DatasetContext / DistributionContext — the central shared type
    distribution_model.py      #   Distribution role / pattern analysis
    distribution_probes.py     #   HTTP probing of distribution URLs (attach_probes)
    semantic_assessment.py     #   One-shot LLM expressiveness assessment (attach_semantic_assessment)
    vocabularies/              #   Controlled-vocabulary loader + RDF/CSV data files
  scoring/                     # The quality logic
    service.py                 #   QualityMetricsService — orchestrates parsing, enrichment, indicators
    indicators/                #   One module per dimension; indicators auto-register on import
    findings.py                #   Builds the Finding from an indicator's details
    score_policy.py            #   Weighting + status/score policy applied on top of raw verdicts
  reporting/                   # Run output & visualisation
    output_manager.py          #   Per-file + run-level JSON, per-file logs, cost summary
    run_visualizer.py          #   matplotlib charts from the run aggregate
  utils/                       # Logger, datetime helpers, Language enum

backend/                       # FastAPI wrapper around the analyzer
  app.py                       # App factory, CORS, lifespan (job store + runner)
  settings.py                  # Env-driven paths and limits
  analysis_adapter.py          # AnalysisConfig → QualityMetricsService; analyze_bytes()
  eval_config.py               # Reads the thesis evaluation YAML → AnalysisConfig
  catalog.py                   # Layer 1: RDF directory → descriptive dataset metadata
  runs.py                      # Layer 2: completed runs → index, single result, deficits, trend
  jobs.py                      # SQLite-backed job store + thread-pool runner
  schemas.py                   # Pydantic request/response models
  routers/                     # meta, analyze, catalogs, runs

frontend/                      # React portal mock (see Web application)
  src/api/                     # Typed HTTP client + types mirroring backend/schemas.py
  src/hooks/                   # react-query hooks (useAnalysis, usePortal)
  src/lib/                     # Config, indicator labels, RDF helpers, status/theme mapping
  src/portal/                  # The GovData-style portal (source state, views)
  src/components/results/      # Score card, radar, dimension tables, findings
  src/css/                     # GovData design tokens and components

conf/state/                    # Hydra configs (mounted under the `state` group — see Running)
data/                          # RDF/XML sample directories, one per catalogue
outputs/runs/                  # Generated run reports (timestamped)
scripts/                       # Sampling, ground-truth template, MQA fetching/comparison, guidance export
playground/notebooks/          # Exploration + evaluation notebooks; 18 produces every
                               #   figure and number of thesis chapter 5 (see Output)
thesis/                        # LaTeX sources
```

Methodology notes, evaluation write-ups and reference PDFs live outside this repo in
the Obsidian vault (`../master_thesis_obsidian/prototyp_doku/`, index in its
`README.md`). Only code and thesis sources are kept here; docstrings that cite a
methodology note point at that path.

**Dependency direction** is one-way: everything points _down_ into `core`, which
imports nothing internal. `extraction` builds the `DatasetContext` that every
indicator reads; `scoring` runs the indicators; `reporting` only consumes
results. `backend` depends on `src`, never the reverse — the analyzer runs
without the web layer. `main.py` is the only place that knows about Hydra.

---

## How a run works

For each input file, [QualityMetricsService](src/scoring/service.py) performs:

1. **Parse** the RDF/XML file into an `rdflib.Graph`
   ([rdf_parser.py](src/extraction/rdf_parser.py)).
2. **Build `DatasetContext` once** — all dataset- and distribution-level facts
   derived from the graph, so indicators don't re-query it
   ([dataset_context.py](src/extraction/dataset_context.py)).
3. **Attach HTTP probes** _only if_ an accessibility indicator that consumes them
   will actually run and the dataset has distributions
   ([distribution_probes.py](src/extraction/distribution_probes.py)). Probing is
   shared and capped, so URLs are fetched at most once per run.
4. **Attach the LLM assessment** _only if_ the LLM is configured and at least one
   expressiveness indicator will run — a single call scores the whole dimension
   ([semantic_assessment.py](src/extraction/semantic_assessment.py)).
5. **Run dimensions in parallel** (`ThreadPoolExecutor`, `quality.max_workers`),
   each indicator producing an `IndicatorResult`. Every failing result is
   immediately enriched with its **finding** — the same code
   path the API uses, so a report and a live analysis never diverge.
6. **Aggregate** into dimension scores, an overall weighted score and a grade.
7. **Persist** per-file and run-level JSON, logs and charts via
   [OutputManager](src/reporting/output_manager.py) (when `run_output_enabled`).

---

## Web application

The web layer exists to answer one question the JSON report cannot: what does a
data provider, who does not know DCAT, have to change? It is a GovData-style
portal mock, because a quality finding has to appear where the metadata is
maintained — not in a separate analytics dashboard.

### Two independent layers

The central design decision is that **metadata and assessment are decoupled** to ensure that possible integration into the actual govdata frontend is as easy as possible:

| Layer                          | Source                                              | Served by            | Knows nothing about |
| ------------------------------ | --------------------------------------------------- | -------------------- | ------------------- |
| **Catalogue** — portal content | a directory of RDF files under `ANALYZER_DATA_ROOT` | `backend/catalog.py` | scores              |
| **Assessment** — the overlay   | a completed run under `ANALYZER_RUNS_ROOT`          | `backend/runs.py`    | titles, keywords    |

They are joined **by file stem alone** (`CatalogDataset.id === RunIndexRow.stem`).
Consequences:

- The portal is complete without any assessment — titles, descriptions,
  keywords, formats, licences and publishers are read straight from the RDF.
- A run result carries no descriptive metadata. It does not need to.
- An assessment is an _overlay_ on an existing portal, not a rebuild of it —
  which is what makes the approach transferable to a real portal.

The frontend starts **empty**. The user first loads a catalogue, then optionally
lays an assessment over it: an existing run, or a fresh calculation (with or
without the LLM-scored expressiveness dimension).

### API surface

| Method | Path                                    | Purpose                                                         |
| ------ | --------------------------------------- | --------------------------------------------------------------- |
| `GET`  | `/health`                               | Liveness probe                                                  |
| `GET`  | `/indicators`                           | Indicator registry + plain-language guidance + score glossary   |
| `GET`  | `/config/default`                       | The thesis evaluation configuration (see below)                 |
| `GET`  | `/catalogs`                             | Available data directories                                      |
| `GET`  | `/catalogs/{name}/datasets`             | Descriptive metadata per RDF file                               |
| `GET`  | `/catalogs/{name}/files/{file}/rdf`     | Raw RDF source (used to highlight the offending lines)          |
| `POST` | `/catalogs/{name}/analyze`              | Score every file of the directory → job id                      |
| `POST` | `/catalogs/{name}/files/{file}/analyze` | Score a single file → job id                                    |
| `GET`  | `/runs`                                 | Completed runs with their directory, file count and LLM model   |
| `GET`  | `/runs/{name}`                          | Compact per-file assessment (score, dimensions, status counts)  |
| `GET`  | `/runs/{name}/{stem}`                   | The full `result.json` of one file                              |
| `GET`  | `/runs/deficits/{name}`                 | Per indicator, how often it failed across the run               |
| `GET`  | `/runs/trend/{catalog}`                 | Mean overall score per run over that directory, chronologically |
| `POST` | `/analyze`                              | Score uploaded files (multipart) → job id                       |
| `GET`  | `/jobs` · `/jobs/{id}`                  | Job status and results; `?results=false` returns progress only  |

Two granularities are deliberate. `/runs/{name}` is a few kilobytes and feeds
the list and the dashboard; `/runs/{name}/{stem}` is several hundred kilobytes
and is fetched only for the dataset actually opened. For the same reason a job
covering a whole directory is polled with `?results=false` and its results are
collected once at the end.

### Configuration comes from the server

Weights, score policy, indicator set and LLM model are **not** hard-coded in the
frontend. `GET /config/default` reads
[conf/state/state_evaluation_final.yaml](conf/state/state_evaluation_final.yaml)
(override with `ANALYZER_EVAL_CONFIG`) and returns it as an `AnalysisConfig`.
Every analysis started from the UI uses it, so a run triggered in the browser
produces the same numbers as the thesis evaluation. The only switch offered in
the UI is whether the expressiveness dimension participates — it is the one that
needs a language model and therefore costs tokens and time.

If the file cannot be read, the response carries `source: null` and the UI says
so instead of silently scoring with different weights.

### Frontend structure

React 18 + TypeScript + Vite, data fetching with `@tanstack/react-query`, charts
with Recharts, styling with the GovData design tokens under `src/css/`.

```
src/portal/source.tsx           # Catalogue + overlay state; the only place both layers meet
src/portal/PortalApp.tsx        # Empty → SourcePicker; otherwise the portal views
src/portal/components/
  GovDataShell.tsx              #   GovData page chrome around every portal view
  SourcePicker.tsx              #   Start screen: pick a data directory (+ two demo shortcuts)
  OverlayBar.tsx                #   Choose a run, or recalculate (with / without expressiveness)
  DatasetSearch.tsx             #   Search, facets, result list
  DatasetCard.tsx               #   One row of the result list
  DatasetDetail.tsx             #   Metadata sheet + optional quality section
  QualityDashboard.tsx          #   Distribution, dimension means, top deficits, trend
  ScoreIndicator.tsx            #   Small score badge reused across the portal views
src/components/results/         # Shared with the upload tool
  ResultsView.tsx               #   Composes the result components for one dataset
  ResultToolbar.tsx             #   Dataset switcher + export actions
  OverallScoreCard.tsx          #   Grade ring + overall score
  DimensionRadar.tsx            #   Dimension profile
  DimensionPanel.tsx            #   Indicator table per dimension
  IndicatorFinding.tsx          #   Finding (Ist/Soll) incl. the location in the RDF source
  BatchComparison.tsx           #   Score comparison across the files of one run
```

The result components take the backend's `AnalysisResult` unchanged — a run's
`result.json` and a live analysis have exactly the same shape, so nothing has to
be translated between them.

---

## Setup

Requires **Python 3.12** (analyzer + backend) and **Node 20+** (frontend only).

```bash
# Analyzer
source .venv/bin/activate          # a virtual environment lives in .venv/
pip install -r requirements.txt

# Backend (adds FastAPI on top)
pip install -r backend/requirements.txt

# Frontend
cd frontend && npm install
```

### LLM credentials (only for the expressiveness dimension)

The LLM is called through **OpenRouter**. Copy the example env file and add your
key:

```bash
cp .env.example .env
# edit .env:
# OPENROUTER_API_KEY=sk-or-...
```

Without a key (or with `llm.enabled: false`), the expressiveness indicators
report `not_applicable` and no tokens are spent — every other dimension still
runs.

### Docker

`docker compose up --build` starts both services: the backend on
`http://localhost:8000`, the frontend on `http://localhost:3000` (nginx). The
compose file mounts `./data` and `./outputs/runs` read-only into the container
and reads `OPENROUTER_API_KEY` from the repo-root `.env`.

---

## Running

### Analyzer (command line)

Run from the **project root** (the script's directory is added to the import
path automatically, so the `core` / `extraction` / `scoring` packages resolve):

```bash
python src/main.py
```

This uses the default config [conf/state/state_default.yaml](conf/state/state_default.yaml).

#### Selecting a different config

The configs live in `conf/state/`. Because that subdirectory name becomes a
Hydra config **group**, the whole file is mounted under a `state` key — which is
why the code reads `cfg.state.*`. Select a variant with `--config-name`:

```bash
python src/main.py --config-name state/state_evaluation_final
python src/main.py --config-name state/state_only_findability
python src/main.py --config-name state/state_perfect_example
```

Bundled variants: `state_default`, **`state_evaluation_final`** (the
configuration the thesis evaluation was run with, and the one the web UI uses),
`state_evaluation_weighted`, `state_weighted_tuning`, `state_perfect_example`,
`state_extreme_cases`, three presentation profiles, and one per dimension
(`state_only_findability`, `state_only_accessibility`, `state_only_reusability`,
`state_only_expressiveness`).

#### Command-line overrides

Any field can be overridden on the command line (note the `state.` prefix):

```bash
# Process a different directory
python src/main.py state.directory_path="data/sample_2026-06-25_09-57"

# Quieter logs + enable the LLM
python src/main.py state.logging.level=INFO state.llm.enabled=true

# Only the findability dimension
python src/main.py 'state.quality.dimension_whitelist=[findability]'
```

### Portal and API

Two processes in development:

```bash
# Terminal 1 — API on :8000
python -m uvicorn backend.app:app --reload --port 8000

# Terminal 2 — dev server on :5173
cd frontend && npm run dev
```

Open `http://localhost:5173`. The portal starts empty; pick a data directory, or
use the two demo buttons to load the evaluation sample with or without the
latest matching run.

The frontend calls the API at `http://localhost:8000` unless `VITE_API_BASE`
says otherwise. The backend only accepts browser requests from the origins in
`ANALYZER_CORS_ORIGINS` (defaults cover ports 5173–5175) — if Vite falls back to
another port, add it there.

#### Backend environment variables

| Variable                    | Default                                  | Purpose                                             |
| --------------------------- | ---------------------------------------- | --------------------------------------------------- |
| `ANALYZER_DATA_ROOT`        | `data/`                                  | Where catalogues (RDF directories) are looked up    |
| `ANALYZER_RUNS_ROOT`        | `outputs/runs/`                          | Where completed runs are looked up                  |
| `ANALYZER_EVAL_CONFIG`      | `conf/state/state_evaluation_final.yaml` | Reference configuration served by `/config/default` |
| `ANALYZER_DB_PATH`          | `backend/analyzer.db`                    | SQLite job store                                    |
| `ANALYZER_CORS_ORIGINS`     | localhost:5173–5175                      | Allowed browser origins                             |
| `ANALYZER_JOB_WORKERS`      | `2`                                      | Concurrent analysis jobs                            |
| `ANALYZER_MAX_FILES`        | `50`                                     | File cap per job                                    |
| `ANALYZER_MAX_UPLOAD_BYTES` | `25 MiB`                                 | Upload cap                                          |

---

## Configuration reference

Full schema (from [state_default.yaml](conf/state/state_default.yaml)). All keys
live under `state` in code (`cfg.state.<key>`):

```yaml
# --- Input ---------------------------------------------------------------
directory_path: "data/sample_2026-06-25_09-57" # folder containing the RDF files

files: [] # explicit file list; if empty, scan the directory
  # - "geo_open-data-brandenburg.rdf"

file_filter: # only used when `files` is empty
  extensions: [".rdf"]
  include_patterns: [] # filename prefixes to include (empty = all)
  exclude_patterns: [] # filename prefixes to skip

# --- Output --------------------------------------------------------------
output_dir: "outputs/runs/" # root for all run directories
run_output_dir_suffix: "" # optional explicit suffix for the run folder name
run_output_enabled: true # false = run in-memory, write nothing to disk

language: "de" # "de" | "en" — language of LLM output & messages

# --- LLM (expressiveness only) ------------------------------------------
llm:
  enabled: false # master switch; false → expressiveness = not_applicable
  provider: "openrouter" # "openrouter" | "local" (any OpenAI-compatible server)
  model: "openai/gpt-5.5" # any OpenRouter model id
  temperature: 0.0
  max_tokens: 25000

# --- Logging -------------------------------------------------------------
logging:
  level: "DEBUG" # DEBUG | INFO | WARNING | ERROR | CRITICAL
  verbose: true

# --- Quality scoring -----------------------------------------------------
quality:
  max_workers: 1 # parallel dimension workers

  scoring: # status → points; omit the block to use raw indicator scores
    pass_score: 1.0
    partial_score: 0.5
    fail_score: 0.0 # may be negative to actively penalise failures
    allow_partial: true # false = every PARTIAL counts as FAIL (ternary only)
    overrides: {} # per-indicator overrides of the four values above

  # dimension_whitelist: ["findability", "accessibility"]   # default: all
  # indicator_blacklist: ["find_keywords_count"]            # default: none
  indicator_whitelist: [] # default: all

  dimension_weights: # default 1.0 each
    findability: 1
    accessibility: 2
    reusability: 1.5
    expressiveness: 2

  # indicator_weights:         # override an indicator's default weight (1.0)
  #   reuse_license: 2.0
```

### Selecting what to run

- **`dimension_whitelist`** — run only these dimensions.
- **`indicator_whitelist`** — run only these indicator IDs (empty list = all).
- **`indicator_blacklist`** — skip these indicator IDs.

The service is smart about expensive work: HTTP probing happens only if an
accessibility indicator that needs it survives the filters, and the LLM call
happens only if an expressiveness indicator survives **and** `llm.enabled` is
true.

Since every scoring parameter lives outside the source, a config is effectively
an **assessment profile**: the same input can be scored under different quality
perspectives without touching code, and each run stores its fully resolved
config, so any result stays attributable to its profile.

### Input selection examples

```yaml
# One specific file
files: ["my_dataset.rdf"]

# All geo files, skipping test fixtures
files: []
file_filter:
  include_patterns: ["geo_"]
  exclude_patterns: ["test_"]
```

---

## Output

All generated artifacts live under `outputs/`, one subdirectory per kind:

| Directory / file                    | Written by                                     | Contents                                                            |
| ----------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------- |
| `outputs/runs/`                     | `src/main.py`, backend jobs                    | One timestamped directory per validation run                        |
| `outputs/mqa_comparison/`           | `scripts/build_indicator_join.py`, notebook 11 | MQA-vs-prototype indicator comparison                               |
| `outputs/ground_truth/`             | notebook 10                                    | Ground-truth evaluation figures & metrics                           |
| `outputs/model_comparison/`         | notebook 13                                    | Cross-run / cross-model consistency plots                           |
| `outputs/thesis_kennzahlen_final.json` | notebook 18                                 | Every number cited in chapter 5, in one file                        |

Everything under `outputs/` is generated and stays local — with one deliberate
exception. The inputs of [notebook 18](playground/notebooks/18_evaluation_kapitel5_final.ipynb),
which produces all figures and numbers of thesis chapter 5, **are committed**, so
the evaluation is reproducible from a clone alone: eight runs under
`outputs/runs/` and two cached `mqa_metrics.csv`. Only the files the notebook
actually reads are tracked (`metadata.json`, `run_aggregate.json`,
`run_cost_summary.json`, `<dataset>/result.json`); the logs and the run charts
stay local. The whitelist is in [.gitignore](.gitignore).

**Hydra writes nothing to disk.** No `outputs/<date>/<time>/` run directory, no
`.hydra/` subdir, no `main.log` — so `outputs/` belongs entirely to the artifacts
above. This is enforced by `HYDRA_NO_OUTPUT` in [src/main.py](src/main.py), which
appends the necessary overrides to the command line. It cannot live in
`conf/state/*.yaml`: those configs sit in the `state` config group, so a `hydra:`
block inside them is loaded as `state.hydra` and silently ignored by Hydra.

When `run_output_enabled: true`, each run creates a timestamped directory:

```
outputs/runs/
└── run_<timestamp>_<config-name>_<suffix>/      # e.g. run_2026-07-27_09-54-46_state-evaluation-final_EVAL_gpt5-5
    ├── metadata.json              # run config, input info, git commit hash, timestamp
    ├── run_aggregate.json         # per-file summary + run-level means/min/max + indicator status counts
    ├── run_cost_summary.json      # LLM token & USD totals (per file + run); written even with 0 LLM calls
    ├── session.log                # full log for the whole run
    ├── run_summary.png            # overall-score histogram + average score per dimension
    ├── run_overall_by_file.png    # overall score per file
    ├── run_scores_by_file.png     # per-file scores, one subplot per active dimension
    ├── run_indicator_outcomes.png # stacked pass/partial/fail/error counts per indicator
    └── <dataset-name>/            # one folder per processed file
        ├── result.json            # complete validation result (see below)
        ├── logs.log               # logs for this file only
        └── openai.log             # raw LLM request/response + HTTP traffic (only when the LLM ran)
```

The `<suffix>` of the run folder is: `run_output_dir_suffix` if set; otherwise
the single file's stem when exactly one file is processed; otherwise the input
directory name.

A run directory is also what the web frontend reads as an assessment overlay —
no conversion step in between.

### `result.json` shape

```jsonc
{
  "by_dimension": {
    "findability": {
      "dimension": "findability",
      "score": 0.5625,
      "dimension_weight": 1.0,
      "total_indicator_weight": 8.0,
      "indicator_count": 8,
      "pass_count": 5,
      "pass_rate": 0.625,
      "indicators": [
        {
          "indicator_id": "find_keywords_count",
          "name_de": "...", "name_en": "...",
          "dimension": "findability",
          "status": "partial",          // after the score policy
          "score": 0.5,                 // after the score policy
          "raw_status": "partial",      // the indicator's untouched verdict
          "raw_score": 0.5,
          "effective_score": 0.5,
          "default_weight": 1.0,
          "effective_weight": 1.0,
          "message_de": "...", "message_en": "...",
          "details": { /* indicator-specific evidence */ },
          "finding": {                  // fail / partial / error only
            "headline": "Nur 1 Schlagwort vergeben, empfohlen sind mindestens 3.",
            "current": [{ "label": "Aktuell 1 Schlagwort", "value": "…", "tone": "bad", "where": null }],
            "target": "3 bis 15 Schlagwörter, die Thema, Region und Datenart benennen.",
            "notes": []
          },
          "error": null,
          "timestamp": "..."
        }
      ]
    }
  },
  "summary": {
    "overall_score": 0.4942,
    "overall_pass_rate": 0.37,
    "dimension_scores": { "findability": 0.5625, "accessibility": 0.5132, ... },
    "dimension_weights": { ... },
    "effective_dimension_weights": { ... },
    "dimension_weight_mode": "explicit",
    "total_dimension_weight": 6.5,
    "total_indicators": 27,
    "total_pass": 10,
    "total_fail": 17,
    "quality_grade": "D"
  },
  "errors": [],
  "weights": { "dimension_weights": {...}, "indicator_weights": {...} },
  "llm_usage": [ /* one record per LLM call: model, tokens, cost_usd, latency */ ]
}
```

---

## Extending the prototype

### Add a new indicator

1. Subclass `Indicator` in the appropriate
   [scoring/indicators/](src/scoring/indicators/) module and implement
   `validate`:

   ```python
   from core.indicator import Indicator, IndicatorResult, IndicatorStatus
   from core.dimension import QualityDimension

   class MyIndicator(Indicator):
       def __init__(self):
           super().__init__(
               indicator_id="find_my_check",
               name_de="...", name_en="...",
               dimension=QualityDimension.FINDABILITY,
               weight=1.0,
           )

       def validate(self, metadata, context=None) -> IndicatorResult:
           # `context` is the shared DatasetContext — declare the keyword to opt in
           ...
           return IndicatorResult(..., status=IndicatorStatus.PASS, score=1.0)

   MyIndicator()   # instantiate at module level → auto-registers
   ```

2. Indicators **auto-register** in `Indicator._registry` on construction, so the
   module-level instantiation is what makes it active. Ensure the module is
   imported by [scoring/indicators/\_\_init\_\_.py](src/scoring/indicators/__init__.py).
3. To receive shared facts, add a `context` keyword to `validate` — the service
   passes the `DatasetContext` only to indicators whose signature accepts it.
4. Add a [`core/guidance.py`](src/core/guidance.py) entry (label, what it checks,
   affected field, how to fix, vocabulary) so the UI can label it in plain
   language, and — if the failure can be explained from `details` — a builder in
   [`scoring/findings.py`](src/scoring/findings.py). Without either, the UI falls
   back to the check message; nothing breaks.

### Add a new dimension

Add a value to `QualityDimension` in [core/dimension.py](src/core/dimension.py),
register indicators against it, and (optionally) give it a `dimension_weights`
entry.

---

## Troubleshooting

| Symptom                                              | Fix                                                                                                                           |
| ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `Directory does not exist`                           | Check `state.directory_path` (relative to the repo root).                                                                     |
| `No files to process`                                | Verify the `files` list, or the `include_/exclude_patterns`. Run with `state.logging.level=DEBUG` to see which files matched. |
| Expressiveness all `not_applicable`                  | `llm.enabled` is false or `OPENROUTER_API_KEY` is missing — see [Setup](#setup).                                              |
| `OPENROUTER_API_KEY ... must be set`                 | Create `.env` from `.env.example` with your key.                                                                              |
| `total_cost_usd` looks like a lower bound            | Some OpenRouter responses omitted cost accounting; see the `note` in `run_cost_summary.json`.                                 |
| No output written                                    | `run_output_enabled` is false.                                                                                                |
| Portal loads but the catalogue list stays empty      | A CORS rejection. The dev server's port is not in `ANALYZER_CORS_ORIGINS` — check the browser console.                        |
| No catalogues offered at all                         | `ANALYZER_DATA_ROOT` holds no subdirectory containing RDF files.                                                              |
| No runs offered as an overlay                        | A run only appears once it has finished — its `metadata.json` (written at the end) supplies the directory it belongs to.      |
| The UI warns that the reference config is unreadable | `ANALYZER_EVAL_CONFIG` does not point at a readable YAML; runs would use plain defaults instead of the evaluation profile.    |
