export interface IntakePayload {
  drug: string;
  dosage: string;
  diagnosis: string;
}

export interface PatientRegimen {
  drug: string;
  dosage: string;
  diagnosis: string;
}

export interface ClinicalAnalysis {
  is_fda_approved: boolean;
  generic_name: string | null;
  baseline_cost_per_unit: number | null;
  medicare_cost_per_claim: number | null;
  summary: string;
  errors: string[];
}

export interface RecommendedFund {
  foundation: string;
  url: string;
  requirements: string[];
}

export interface GrantNavigation {
  has_open_funds: boolean;
  recommended_funds: RecommendedFund[];
  human_readable_summary: string;
  errors: string[];
}

export interface IntakeResponseData {
  patient_regimen: PatientRegimen;
  clinical_analysis: ClinicalAnalysis;
  grant_navigation: GrantNavigation;
}

export interface IntakeResponse {
  status: string;
  data: IntakeResponseData;
  error: string | null;
}
