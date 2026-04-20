from typing import Literal

from pydantic import BaseModel, Field


class CriterionScoreEN(BaseModel):
    """Score and reasoning for a single criterion."""

    name: str = Field(..., description="Name of the criterion.")
    score: float = Field(..., ge=0, description="Assigned score for the criterion.")
    max_score: float = Field(
        ..., gt=0, description="Maximum possible score for the criterion."
    )
    findings: list[str] = Field(
        default_factory=list,
        description="Observed strengths, weaknesses, and factual findings for this criterion.",
    )
    deduction_reasons: list[str] = Field(
        default_factory=list,
        description="Explicit reasons why points were deducted.",
    )
    context_sensitive_deductions: list[str] = Field(
        default_factory=list,
        description="Context-sensitive deductions applied within this criterion.",
    )


class CategoryAssessmentEN(BaseModel):
    """Assessment of one top-level metadata quality category."""

    name: Literal[
        "Findability",
        "Accessibility",
        "Interoperability",
        "Reusability",
        "Contextuality",
    ] = Field(..., description="Top-level quality category name.")
    score: float = Field(..., ge=0, description="Assigned category score.")
    max_score: float = Field(..., gt=0, description="Maximum possible category score.")
    summary: str = Field(
        ...,
        description="Short narrative summary of the category-level assessment.",
    )
    criteria: list[CriterionScoreEN] = Field(
        default_factory=list,
        description="Criterion-by-criterion scoring for this category.",
    )
    category_level_context_checks: list[str] = Field(
        default_factory=list,
        description="Cross-field contextual observations folded into this category.",
    )


class ScoreTableEN(BaseModel):
    """Compact overall score table."""

    findability: float = Field(..., ge=0, le=100)
    accessibility: float = Field(..., ge=0, le=100)
    interoperability: float = Field(..., ge=0, le=110)
    reusability: float = Field(..., ge=0, le=75)
    contextuality: float = Field(..., ge=0, le=20)
    total: float = Field(..., ge=0, le=405)
    rating: Literal["Excellent", "Good", "Sufficient", "Bad"]


class RemediationActionEN(BaseModel):
    """Concrete improvement recommendation."""

    priority: int = Field(..., ge=1, description="1 = highest priority.")
    title: str = Field(..., description="Short action label.")
    description: str = Field(..., description="Specific and actionable improvement.")
    target_fields: list[str] = Field(
        default_factory=list,
        description="Metadata fields that should be improved.",
    )
    suggested_fix: str | None = Field(
        default=None,
        description="Concrete proposed change, wording, or correction.",
    )


class MachineReadableCategorySummaryEN(BaseModel):
    """Compact machine-readable per-category result."""

    score: float = Field(..., ge=0)
    max: float = Field(..., gt=0)
    issues: list[str] = Field(
        default_factory=list,
        description="Main issues affecting the category score.",
    )


class MachineReadableTotalSummaryEN(BaseModel):
    """Compact machine-readable total result."""

    score: float = Field(..., ge=0)
    max: float = Field(..., gt=0)
    rating: Literal["Excellent", "Good", "Sufficient", "Bad"]


class MachineReadableSummaryEN(BaseModel):
    """Machine-readable summary aligned with the prompt structure."""

    findability: MachineReadableCategorySummaryEN
    accessibility: MachineReadableCategorySummaryEN
    interoperability: MachineReadableCategorySummaryEN
    reusability: MachineReadableCategorySummaryEN
    contextuality: MachineReadableCategorySummaryEN
    total: MachineReadableTotalSummaryEN


class SemanticAnalysisEN(BaseModel):
    """Typed response for metadata quality assessment based on MQA-style scoring."""

    overall_summary: str = Field(
        ...,
        description="3 to 8 sentence overall summary covering main strengths, weaknesses, and expected impact on discoverability and reuse.",
    )
    score_table: ScoreTableEN = Field(
        ...,
        description="Compact score table with per-category scores, total score, and rating band.",
    )
    detailed_scoring: list[CategoryAssessmentEN] = Field(
        ...,
        min_length=5,
        max_length=5,
        description="Detailed category-by-category scoring. Must contain exactly the five top-level categories.",
    )
    critical_issues: list[str] = Field(
        default_factory=list,
        description="Most serious defects that materially reduce metadata quality.",
    )
    machine_readable_summary: MachineReadableSummaryEN = Field(
        ...,
        description="Final machine-readable score summary.",
    )
