from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ── API LEVEL SCHEMAS ────────────────────────────────────────────────────────

class IntakeRequest(BaseModel):
    drug: str = Field(..., description="Name of the prescribed drug")
    dosage: str = Field(..., description="Dosage and frequency")
    diagnosis: str = Field(..., description="Patient's cancer diagnosis")

class PatientRegimen(BaseModel):
    drug: str
    dosage: str
    diagnosis: str

# ── AGENT / ORCHESTRATOR LEVEL SCHEMAS ───────────────────────────────────────

class ClinicalAnalysisResult(BaseModel):
    is_fda_approved: bool = Field(..., description="Whether the drug is FDA approved for the diagnosis")
    generic_name: str = Field(..., description="The generic equivalent name, or N/A")
    baseline_cost_per_unit: Optional[float] = Field(None, description="NADAC baseline cost per unit")
    medicare_cost_per_claim: Optional[float] = Field(None, description="Average CMS Medicare cost per claim")
    summary: str = Field(..., description="A short, human-readable summary of the clinical findings")
    errors: List[str] = Field(default_factory=list, description="Any tool errors encountered")

class FundDetails(BaseModel):
    foundation: str
    url: str
    requirements: List[str] = Field(default_factory=list, description="List of eligibility requirements")

class GrantNavigationResult(BaseModel):
    has_open_funds: bool = Field(..., description="True if at least one OPEN fund was found")
    recommended_funds: List[FundDetails] = Field(default_factory=list)
    human_readable_summary: str = Field(..., description="A brief summary for the patient")
    errors: List[str] = Field(default_factory=list, description="Any tool errors encountered")

class OrchestratorData(BaseModel):
    patient_regimen: PatientRegimen
    clinical_analysis: Optional[ClinicalAnalysisResult] = None
    grant_navigation: Optional[GrantNavigationResult] = None

class IntakeResponse(BaseModel):
    status: str
    data: Optional[OrchestratorData] = None
    error: Optional[str] = None

# ── MCP TOOL LEVEL SCHEMAS ───────────────────────────────────────────────────

class GrantFund(BaseModel):
    fund_name: str
    status: str
    source: str
    foundation: str

class GrantScrapePayload(BaseModel):
    cancer_type_searched: str
    total_open_funds_found: int
    open_funds: List[GrantFund] = []
    direct_urls_for_manual_check: Dict[str, str]
    errors_encountered: List[str] = []
    disclaimer: str
