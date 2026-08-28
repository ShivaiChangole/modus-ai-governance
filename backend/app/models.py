from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class UseCaseRequest(BaseModel):
    title: str = Field(..., example="Automated Resume Screening Tool")
    industry: str = Field(..., example="Human Resources")
    description: str = Field(..., example="AI model that ranks candidate resumes based on historical hiring data.")
    data_types: List[str] = Field(default=[], example=["PII", "Employment History"])
    deployment_scope: str = Field(default="Internal", example="Internal")

class CitationItem(BaseModel):
    content: str
    source: str
    source_type: str  # Law / Regulation, Regulatory Guidance, Industry Standard, etc.
    category: str
    jurisdiction: str

class RiskCategoryScore(BaseModel):
    category: str
    risk_level: str  # Low, Medium, High, Critical
    score: int       # 0 - 100 scale
    reasoning: str

class GovernanceAssessmentResponse(BaseModel):
    use_case_title: str
    industry: str
    overall_risk_level: str
    overall_score: int
    risk_breakdown: List[RiskCategoryScore]
    citations: List[CitationItem]
    mandatory_actions: List[str]
