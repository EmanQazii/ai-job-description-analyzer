from pydantic import BaseModel, Field
from typing import List


class ScoreBreakdown(BaseModel):
    clarity: int = Field(ge=0, le=100)
    completeness: int = Field(ge=0, le=100)
    specificity: int = Field(ge=0, le=100)
    professionalism: int = Field(ge=0, le=100)
    inclusivity: int = Field(ge=0, le=100)


class Issue(BaseModel):
    issue: str
    category: str
    severity: str
    explanation: str
    suggestion: str


class BiasFlag(BaseModel):
    phrase: str
    concern: str
    suggested_alternative: str


class ChecklistItem(BaseModel):
    item: str
    present: bool
    comment: str


class JDAnalysis(BaseModel):
    overall_score: int = Field(ge=0, le=100)
    score_breakdown: ScoreBreakdown
    summary: str
    issues: List[Issue]
    bias_flags: List[BiasFlag]
    checklist: List[ChecklistItem]
    recommendations: List[str]