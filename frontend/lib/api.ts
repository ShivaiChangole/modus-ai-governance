export interface UseCaseRequest {
  title: string;
  industry: string;
  description: string;
  data_types: string[];
  deployment_scope: string;
}

export interface CitationItem {
  content: string;
  source: string;
  source_type: string;
  category: string;
  jurisdiction: string;
}

export interface RiskCategoryScore {
  category: string;
  risk_level: string;
  score: number;
  reasoning: string;
}

export interface GovernanceAssessmentResponse {
  use_case_title: string;
  industry: string;
  overall_risk_level: string;
  overall_score: number;
  risk_breakdown: RiskCategoryScore[];
  citations: CitationItem[];
  mandatory_actions: string[];
}

const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function submitAssessment(data: UseCaseRequest): Promise<GovernanceAssessmentResponse> {
  const response = await fetch(`${API_BASE_URL}/assess`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`Assessment failed: ${response.statusText}`);
  }

  return response.json();
}

export async function fetchAssessmentHistory() {
  const response = await fetch(`${API_BASE_URL}/assessments`);
  if (!response.ok) {
    throw new Error("Failed to fetch assessment history");
  }
  return response.json();
}