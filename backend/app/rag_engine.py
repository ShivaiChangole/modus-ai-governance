from typing import List
from app.models import UseCaseRequest, GovernanceAssessmentResponse, RiskCategoryScore, CitationItem
from app.vector_store import query_governance_rules

def evaluate_ai_use_case(use_case: UseCaseRequest) -> GovernanceAssessmentResponse:
    # 1. Retrieve relevant governance rules & citations from ChromaDB
    query_text = f"{use_case.industry} {use_case.title} {use_case.description} {' '.join(use_case.data_types)}"
    retrieved_citations = query_governance_rules(query_text, n_results=4)
    
    citations = [
        CitationItem(
            content=item["content"],
            source=item["source"],
            source_type=item["source_type"],
            category=item["category"],
            jurisdiction=item["jurisdiction"]
        ) for item in retrieved_citations
    ]
    
    # 2. Dynamic Risk Evaluation Rules across Governance Pillars
    desc_lower = (use_case.description + " " + " ".join(use_case.data_types)).lower()
    
    # Privacy Assessment
    has_pii = any(term in desc_lower for term in ["pii", "personal", "medical", "health", "biometric", "financial"])
    privacy_risk = "High" if has_pii else "Medium" if "user" in desc_lower else "Low"
    privacy_score = 85 if privacy_risk == "High" else 50 if privacy_risk == "Medium" else 20
    
    # Bias & Fairness Assessment
    has_hr_or_finance = any(term in desc_lower for term in ["hiring", "resume", "credit", "lending", "scoring", "salary", "recruitment"])
    bias_risk = "High" if has_hr_or_finance else "Medium"
    bias_score = 90 if bias_risk == "High" else 40
    
    # Human Oversight Assessment
    has_automation = any(term in desc_lower for term in ["automated", "autonomous", "screening", "filtering", "auto-decision"])
    oversight_risk = "High" if has_automation else "Low"
    oversight_score = 80 if oversight_risk == "High" else 30
    
    # Regulatory Exposure Assessment
    laws_found = any(c.source_type == "Law / Regulation" for c.source_type in [c.source_type for c.citations in [citations]])
    reg_risk = "Critical" if (has_hr_or_finance or has_pii) else "Medium"
    reg_score = 95 if reg_risk == "Critical" else 50
    
    risk_breakdown = [
        RiskCategoryScore(
            category="Data Privacy",
            risk_level=privacy_risk,
            score=privacy_score,
            reasoning="Processes sensitive user datasets or personal attributes requiring explicit consent and zero-retention controls." if has_pii else "Low exposure to sensitive personal data attributes."
        ),
        RiskCategoryScore(
            category="Bias / Fairness",
            risk_level=bias_risk,
            score=bias_score,
            reasoning="High vulnerability to algorithmic bias and disparate impact in employment or financial decision systems." if has_hr_or_finance else "Standard operational scope with minimal demographic sensitivity."
        ),
        RiskCategoryScore(
            category="Human Oversight",
            risk_level=oversight_risk,
            score=oversight_score,
            reasoning="Automated decision pipeline requires a mandatory Human-in-the-Loop (HITL) review checkpoint under Article 14." if has_automation else "System operates under continuous human supervision."
        ),
        RiskCategoryScore(
            category="Regulatory Exposure",
            risk_level=reg_risk,
            score=reg_score,
            reasoning="Triggers High-Risk AI System classification under EU AI Act and regulatory oversight frameworks." if reg_risk == "Critical" else "Subject to standard industry guidance and internal compliance policies."
        )
    ]
    
    # 3. Calculate Overall Risk Score
    avg_score = int(sum(item.score for item in risk_breakdown) / len(risk_breakdown))
    overall_level = "Critical Risk" if avg_score >= 80 else "High Risk" if avg_score >= 60 else "Medium Risk" if avg_score >= 35 else "Low Risk"
    
    # 4. Mandatory Action Items
    actions = [
        "Perform a formal AI Bias & Disparate Impact Audit prior to production deployment.",
        "Implement mandatory logging and audit trails for all model recommendations.",
        "Establish Human-in-the-Loop override mechanisms for edge cases.",
        "Verify data encryption at rest and in transit for all ingested metadata."
    ]
    
    return GovernanceAssessmentResponse(
        use_case_title=use_case.title,
        industry=use_case.industry,
        overall_risk_level=overall_level,
        overall_score=avg_score,
        risk_breakdown=risk_breakdown,
        citations=citations,
        mandatory_actions=actions
    )
