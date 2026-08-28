import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UseCaseRequest(BaseModel):
    title: str
    industry: str
    description: str
    data_types: List[str]
    deployment_scope: str = "Internal"

@app.post("/api/assess")
async def assess_use_case(request: UseCaseRequest):
    try:
        # --- Sample Fallback Assessment Logic ---
        # Replace or integrate this with your ChromaDB / LLM retrieval logic
        
        # Query ChromaDB (if initialized)
        citations = [
          {
            "content": "High-risk AI systems in employment and worker management require strict risk management and data governance.",
            "source": "EU AI Act - Annex III",
            "source_type": "Regulatory Framework",
            "category": "Employment & HR",
            "jurisdiction": "EU"
          },
          {
            "content": "Organizations must conduct Privacy Impact Assessments when processing sensitive PII and biometrics.",
            "source": "GDPR / DPDP Standard",
            "source_type": "Data Privacy Directive",
            "category": "Data Privacy",
            "jurisdiction": "Global"
          }
        ]

        return {
            "use_case_title": request.title,
            "industry": request.industry,
            "overall_risk_level": "High Risk",
            "overall_score": 78,
            "risk_breakdown": [
                {
                    "category": "Data Privacy & PII",
                    "risk_level": "High Risk",
                    "score": 85,
                    "reasoning": "Processing candidate PII and CV documents triggers strict compliance requirements under GDPR and local data protection regulations."
                },
                {
                    "category": "Algorithmic Bias & Fairness",
                    "risk_level": "High Risk",
                    "score": 80,
                    "reasoning": "Automated candidate screening models pose documented risks of systematic bias against protected attributes."
                },
                {
                    "category": "Transparency & Explainability",
                    "risk_level": "Medium Risk",
                    "score": 65,
                    "reasoning": "Scoring outputs require explainability mechanisms so candidates can appeal automated rejection decisions."
                }
            ],
            "citations": citations,
            "mandatory_actions": [
                "Perform formal Bias & Fairness Audits before production deployment.",
                "Implement human-in-the-loop oversight for all rejection decisions.",
                "Maintain explicit opt-in consent and data deletion options for applicants.",
                "Document technical specifications and risk mitigation controls in an AI Register."
            ]
        }
    except Exception as e:
        print("\n" + "="*50)
        print("EXCEPTION IN /api/assess ROUTE:")
        traceback.print_exc()
        print("="*50 + "\n")
        raise HTTPException(status_code=500, detail=str(e))