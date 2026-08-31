from pydantic import BaseModel, Field
from typing import List


class ScoreBreakdown(BaseModel):
    clarity: int = Field(ge=0, le=100)
    completeness: int = Field(ge=0, le=100)
    specificity: int = Field(ge=0, le=100)
    professionalism: int = Field(ge=0, le=100)
    inclusivity: int = Field(ge=0, le=100)


class Issue(BaseModel):
    title: str
    severity: str
    category: List[str]
    explanation: str
    suggestion: str


class BiasFlag(BaseModel):
    phrase: str
    concern: str
    alternative: str


class ChecklistItem(BaseModel):
    item: str
    present: bool
    priority: str
    comment: str


class JDAnalysis(BaseModel):
    score_breakdown: ScoreBreakdown
    summary: str
    issues: List[Issue]
    bias_flags: List[BiasFlag]
    checklist: List[ChecklistItem]
    recommendations: List[str]
    improved_jd: str