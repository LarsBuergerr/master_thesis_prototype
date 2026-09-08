"""Pydantic request/response/job models for the analyzer API.

The response models mirror the dict that ``QualityMetricsService`` already
produces; ``extra="allow"`` keeps them forward-compatible if the service grows
new fields, so the API never silently drops data.
"""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Request: analysis configuration (mirrors quality.* in the Hydra config)
# ---------------------------------------------------------------------------


class ScoringOverride(BaseModel):
    """Per-indicator override of the global score policy."""

    pass_score: Optional[float] = None
    partial_score: Optional[float] = None
    fail_score: Optional[float] = None
    allow_partial: Optional[bool] = None


class ScoringConfig(BaseModel):
    """Status → points mapping. Absent → indicators' raw scores are used."""

    pass_score: float = 1.0
    partial_score: float = 0.5
    fail_score: float = 0.0
    allow_partial: bool = True
    overrides: dict[str, ScoringOverride] = Field(default_factory=dict)


class LLMConfig(BaseModel):
    """LLM settings for the expressiveness dimension."""

    enabled: bool = False
    provider: str = "openrouter"  # "openrouter" | "local"
    model: Optional[str] = None
    base_url: Optional[str] = None
    temperature: float = 0.0
    max_tokens: int = 4096


class AnalysisConfig(BaseModel):
    """Everything the operator can tune for a run."""

    dimension_whitelist: Optional[list[str]] = None
    indicator_blacklist: Optional[list[str]] = None
    indicator_whitelist: Optional[list[str]] = None
    dimension_weights: dict[str, float] = Field(default_factory=dict)
    indicator_weights: dict[str, float] = Field(default_factory=dict)
    scoring: Optional[ScoringConfig] = None
    llm: LLMConfig = Field(default_factory=LLMConfig)
    language: str = "de"
    max_workers: int = 4


# ---------------------------------------------------------------------------
# Response: scored result (mirrors QualityMetricsService output)
# ---------------------------------------------------------------------------


class IndicatorResultModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    indicator_id: str
    name_de: str = ""
    name_en: str = ""
    # ``dimension`` / ``score`` are absent on error-path results (an indicator
    # that raised), so they're optional to tolerate those entries.
    dimension: Optional[str] = None
    status: str
    score: Optional[float] = None
    raw_status: Optional[str] = None
    raw_score: Optional[float] = None
    effective_score: Optional[float] = None
    default_weight: Optional[float] = None
    effective_weight: Optional[float] = None
    message_de: str = ""
    message_en: str = ""
    details: dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None
    # Shape mirrors core.finding.Finding: headline / current[] / target /
    # notes[]. Set for FAIL, PARTIAL and ERROR results, ``None`` for PASS.
    finding: Optional[dict[str, Any]] = None


class DimensionResultModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    dimension: str
    score: float
    dimension_weight: float = 1.0
    total_indicator_weight: float = 0.0
    indicator_count: int = 0
    pass_count: int = 0
    pass_rate: float = 0.0
    indicators: list[IndicatorResultModel] = Field(default_factory=list)


class SummaryModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    overall_score: float = 0.0
    quality_grade: str = "F"
    overall_pass_rate: float = 0.0
    dimension_scores: dict[str, float] = Field(default_factory=dict)
    dimension_weights: dict[str, float] = Field(default_factory=dict)
    total_indicators: int = 0
    total_pass: int = 0
    total_fail: int = 0


class AnalysisResultModel(BaseModel):
    model_config = ConfigDict(extra="allow")

    by_dimension: dict[str, DimensionResultModel] = Field(default_factory=dict)
    summary: SummaryModel = Field(default_factory=SummaryModel)
    weights: dict[str, Any] = Field(default_factory=dict)
    llm_usage: list[dict[str, Any]] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Jobs
# ---------------------------------------------------------------------------


class JobProgress(BaseModel):
    done: int = 0
    total: int = 0
    current_file: Optional[str] = None


class FileResultModel(BaseModel):
    filename: str
    result: Optional[AnalysisResultModel] = None
    error: Optional[str] = None


class JobSummary(BaseModel):
    """Lightweight job view (status + progress, no per-file results)."""

    job_id: str
    status: str  # queued | running | done | error
    created_at: str
    updated_at: str
    progress: JobProgress
    files: list[str]
    error: Optional[str] = None


class JobDetail(JobSummary):
    """Full job view including per-file results and the config used.

    Beide Felder fehlen, wenn der Job mit ``results=false`` abgefragt wurde —
    dann interessiert nur der Fortschritt (siehe ``GET /jobs/{id}``).
    """

    config: Optional[AnalysisConfig] = None
    results: list[FileResultModel] = Field(default_factory=list)


class JobCreatedResponse(BaseModel):
    job_id: str
    status: str


# ---------------------------------------------------------------------------
# Meta
# ---------------------------------------------------------------------------


class VocabularyInfo(BaseModel):
    """Kontrolliertes Vokabular, aus dem ein Feldwert stammen muss."""

    label_de: str
    url: str


class GuidanceInfo(BaseModel):
    """Klartext-Beschreibung eines Indikators (siehe core.guidance)."""

    label_de: str
    what_de: str
    field: str
    fix_de: str
    vocabulary: Optional[VocabularyInfo] = None
    #: Was unter dem Befund steht: ``template`` (Vorlage), ``location``
    #: (Fundstelle in der geprüften Datei) oder ``none``.
    detail: str = "location"
    #: RDF/XML-Vorlage, nur bei ``detail == "template"``.
    template: Optional[str] = None


class DimensionInfo(BaseModel):
    dimension: str
    label_de: str
    what_de: str


class IndicatorInfo(BaseModel):
    indicator_id: str
    name_de: str
    name_en: str
    dimension: str
    description_de: str = ""
    description_en: str = ""
    default_weight: float = 1.0
    graded: bool = False
    #: ``None``, solange für eine neue Indikator-ID noch kein Klartext
    #: hinterlegt ist — Oberflächen fallen dann auf ``name_de`` zurück.
    guidance: Optional[GuidanceInfo] = None


class IndicatorsResponse(BaseModel):
    dimensions: list[str]
    indicators: list[IndicatorInfo]
    #: Deutsche Bezeichnung und Erklärung je Dimension.
    dimension_info: list[DimensionInfo] = Field(default_factory=list)
    #: Erklärung der Kennzahlen (status / score / raw / weight).
    score_glossary: dict[str, str] = Field(default_factory=dict)


class CatalogInfo(BaseModel):
    """Ein Datenverzeichnis, das sich als Portalinhalt laden lässt."""

    name: str
    dataset_count: int


class CatalogDataset(BaseModel):
    """Beschreibende Metadaten eines Datensatzes — ohne jede Bewertung."""

    model_config = ConfigDict(extra="allow")

    file: str
    id: str
    slug: str
    uri: Optional[str] = None
    title: str
    description: str = ""
    keywords: list[str] = Field(default_factory=list)
    themes: list[str] = Field(default_factory=list)
    formats: list[str] = Field(default_factory=list)
    license: Optional[str] = None
    license_uri: Optional[str] = None
    modified: str = ""
    issued: str = ""
    publisher_name: str = ""
    #: ``geo`` / ``non_geo``, sofern der Dateiname es hergibt.
    category: Optional[str] = None
    #: Herkunftsportal, aus dem Dateinamen abgeleitet.
    source: Optional[str] = None


class RunInfo(BaseModel):
    """Ein abgeschlossener Lauf, wie er zur Auswahl angeboten wird."""

    name: str
    dataset_count: int
    #: Datenverzeichnis, über das der Lauf lief — zeigt, ob er zum Katalog passt.
    directory: Optional[str] = None
    #: Modell der Aussagekraft-Bewertung; ``None`` heißt: ohne Sprachmodell.
    llm_model: Optional[str] = None
    dimensions: list[str] = Field(default_factory=list)


class RunIndexRow(BaseModel):
    """Bewertung einer Datei in Kurzform (Liste und Übersichtsseite)."""

    stem: str
    overall: Optional[float] = None
    grade: Optional[str] = None
    dims: dict[str, float] = Field(default_factory=dict)
    dim_weights: dict[str, float] = Field(default_factory=dict)
    total_indicators: int = 0
    n_pass: int = 0
    n_partial: int = 0
    n_fail: int = 0


class RunDeficit(BaseModel):
    """Wie oft ein Indikator über einen Lauf hinweg nicht erfüllt wurde."""

    indicator_id: str
    dimension: Optional[str] = None
    fail: int
    partial: int
    total: int


class RunTrendPoint(BaseModel):
    """Ein Lauf im Qualitätsverlauf eines Datenbestands."""

    run: str
    timestamp: Optional[str] = None
    dataset_count: int
    mean_overall: float
    min_overall: float
    max_overall: float
    llm_model: Optional[str] = None


class DefaultConfigResponse(BaseModel):
    """Ausgangskonfiguration für Läufe im Frontend (siehe backend/eval_config)."""

    config: AnalysisConfig
    #: Dateiname der gelesenen Referenz-YAML. ``None`` heißt: Datei nicht
    #: lesbar, es gelten die Feld-Defaults — dann laufen Frontend-Läufe *nicht*
    #: mit der Konfiguration der Evaluation, und die Oberfläche sagt das auch.
    source: Optional[str] = None
