from typing import Generic, TypeVar

from pydantic import BaseModel, Field


CategoryNameT = TypeVar("CategoryNameT", bound=str)
RatingT = TypeVar("RatingT", bound=str)


class CriterionScoreBase(BaseModel):
    name: str
    score: float = Field(..., ge=0)
    max_score: float = Field(..., gt=0)
    findings: list[str] = Field(default_factory=list)
    deduction_reasons: list[str] = Field(default_factory=list)
    context_sensitive_deductions: list[str] = Field(default_factory=list)


class CategoryAssessmentBase(BaseModel, Generic[CategoryNameT]):
    name: CategoryNameT
    score: float = Field(..., ge=0)
    max_score: float = Field(..., gt=0)
    summary: str
    criteria: list[CriterionScoreBase] = Field(default_factory=list)
    category_level_context_checks: list[str] = Field(default_factory=list)


class ScoreTableBase(BaseModel, Generic[RatingT]):
    total_score: float = Field(..., ge=0, le=405)
    rating: RatingT


class RemediationActionBase(BaseModel):
    priority: int = Field(..., ge=1)
    title: str
    description: str
    target_fields: list[str] = Field(default_factory=list)
    suggested_fix: str | None = None


class MachineReadableCategorySummaryBase(BaseModel):
    score: float = Field(..., ge=0)
    max: float = Field(..., gt=0)
    issues: list[str] = Field(default_factory=list)


class MachineReadableTotalSummaryBase(BaseModel, Generic[RatingT]):
    score: float = Field(..., ge=0)
    max: float = Field(..., gt=0)
    rating: RatingT


class MachineReadableSummaryBase(BaseModel, Generic[RatingT]):
    findability: MachineReadableCategorySummaryBase
    accessibility: MachineReadableCategorySummaryBase
    interoperability: MachineReadableCategorySummaryBase
    reusability: MachineReadableCategorySummaryBase
    contextuality: MachineReadableCategorySummaryBase
    total: MachineReadableTotalSummaryBase[RatingT]


class SemanticAnalysisBase(BaseModel, Generic[CategoryNameT, RatingT]):
    overall_summary: str
    score_table: ScoreTableBase[RatingT]
    detailed_scoring: list[CategoryAssessmentBase[CategoryNameT]] = Field(
        ...,
        min_length=5,
        max_length=5,
    )
    critical_issues: list[str] = Field(default_factory=list)
    machine_readable_summary: MachineReadableSummaryBase[RatingT]
