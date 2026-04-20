from typing import Literal

from pydantic import BaseModel, Field


class CriterionScore(BaseModel):
    """Punktzahl und Begründung für ein einzelnes Kriterium."""

    name: str = Field(..., description="Name des Kriteriums.")
    score: float = Field(
        ..., ge=0, description="Vergebene Punktzahl für das Kriterium."
    )
    max_score: float = Field(
        ..., gt=0, description="Maximal erreichbare Punktzahl für das Kriterium."
    )
    findings: list[str] = Field(
        default_factory=list,
        description="Festgestellte Stärken, Schwächen und sachliche Befunde zu diesem Kriterium.",
    )
    deduction_reasons: list[str] = Field(
        default_factory=list,
        description="Explizite Gründe für Punktabzüge.",
    )
    context_sensitive_deductions: list[str] = Field(
        default_factory=list,
        description="Kontextsensitive Abzüge, die innerhalb dieses Kriteriums angewendet wurden.",
    )


class CategoryAssessment(BaseModel):
    """Bewertung einer übergeordneten Metadatenqualitätskategorie."""

    name: Literal[
        "Auffindbarkeit",
        "Zugänglichkeit",
        "Interoperabilität",
        "Nachnutzbarkeit",
        "Kontextualität",
    ] = Field(..., description="Name der übergeordneten Qualitätskategorie.")
    score: float = Field(
        ..., ge=0, description="Vergebene Punktzahl für die Kategorie."
    )
    max_score: float = Field(
        ..., gt=0, description="Maximal erreichbare Punktzahl für die Kategorie."
    )
    summary: str = Field(
        ...,
        description="Kurze narrative Zusammenfassung der Bewertung auf Kategorieebene.",
    )
    criteria: list[CriterionScore] = Field(
        default_factory=list,
        description="Bewertung je Einzelkriterium innerhalb dieser Kategorie.",
    )
    category_level_context_checks: list[str] = Field(
        default_factory=list,
        description="Kontextbezogene Beobachtungen über mehrere Felder hinweg, die in diese Kategorie eingeflossen sind.",
    )


class ScoreTable(BaseModel):
    """Kompakte Übersicht der Gesamtbewertung."""

    auffindbarkeit: float = Field(..., ge=0, le=100)
    zugaenglichkeit: float = Field(..., ge=0, le=100)
    interoperabilitaet: float = Field(..., ge=0, le=110)
    nachnutzbarkeit: float = Field(..., ge=0, le=75)
    kontextualitaet: float = Field(..., ge=0, le=20)
    gesamt: float = Field(..., ge=0, le=405)
    bewertungsband: Literal["Excellent", "Good", "Sufficient", "Bad"]


class RemediationAction(BaseModel):
    """Konkrete Empfehlung zur Verbesserung."""

    priority: int = Field(..., ge=1, description="1 = höchste Priorität.")
    title: str = Field(..., description="Kurze Bezeichnung der Maßnahme.")
    description: str = Field(
        ..., description="Spezifische und umsetzbare Verbesserung."
    )
    target_fields: list[str] = Field(
        default_factory=list,
        description="Metadatenfelder, die verbessert werden sollten.",
    )
    suggested_fix: str | None = Field(
        default=None,
        description="Konkreter Änderungsvorschlag oder Formulierung, soweit möglich.",
    )


class MachineReadableCategorySummary(BaseModel):
    """Kompakte maschinenlesbare Zusammenfassung je Kategorie."""

    score: float = Field(..., ge=0)
    max: float = Field(..., gt=0)
    issues: list[str] = Field(
        default_factory=list,
        description="Wesentliche Probleme, die die Punktzahl dieser Kategorie beeinflussen.",
    )


class MachineReadableTotalSummary(BaseModel):
    """Kompakte maschinenlesbare Gesamtauswertung."""

    score: float = Field(..., ge=0)
    max: float = Field(..., gt=0)
    rating: Literal["Exzellent", "Gut", "Ausreichend", "Schlecht"]


class MachineReadableSummary(BaseModel):
    """Maschinenlesbare Zusammenfassung entsprechend der Prompt-Struktur."""

    findability: MachineReadableCategorySummary
    accessibility: MachineReadableCategorySummary
    interoperability: MachineReadableCategorySummary
    reusability: MachineReadableCategorySummary
    contextuality: MachineReadableCategorySummary
    total: MachineReadableTotalSummary


class SemanticAnalysis(BaseModel):
    """Typisierte Antwort für eine Metadatenqualitätsbewertung nach MQA-Logik."""

    overall_summary: str = Field(
        ...,
        description="Gesamtzusammenfassung in 3 bis 8 Sätzen mit Hauptstärken, Hauptschwächen und erwarteten Auswirkungen auf Auffindbarkeit und Nachnutzung.",
    )
    score_table: ScoreTable = Field(
        ...,
        description="Kompakte Bewertungstabelle mit Kategorien, Gesamtpunktzahl und Bewertungsband.",
    )
    detailed_scoring: list[CategoryAssessment] = Field(
        ...,
        min_length=5,
        max_length=5,
        description="Detaillierte Bewertung je Kategorie. Muss genau die fünf Hauptkategorien enthalten.",
    )
    critical_issues: list[str] = Field(
        default_factory=list,
        description="Die gravierendsten Mängel, die die Metadatenqualität materiell mindern.",
    )
    machine_readable_summary: MachineReadableSummary = Field(
        ...,
        description="Abschließende maschinenlesbare Zusammenfassung der Bewertung.",
    )
