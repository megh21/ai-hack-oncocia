"""
FastAPI Backend Server
======================
Exposes the multi-agent ADK orchestrator over REST for the Next.js frontend.

Start with: uv run uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json

from adk_orchestrator import _run_grant_navigator, run_orchestrator
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService

# Import our new central schemas
from models import IntakeRequest, IntakeResponse

# Import underlying python functions from the MCP modules for direct testing
from mcp_openfda import check_generic_equivalent, verify_indication
from mcp_nadac import get_baseline_cost
from mcp_medicare import get_medicare_spending
from mcp_grants import search_grants, check_eligibility_requirements

app = FastAPI(
    title="Financial Toxicity Advocate API",
    description="Multi-agent oncology financial advocacy backend",
    version="1.0.0",
)

# Allow the Next.js dev server and production origin to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/api/health")
def health_check():
    """Quick health check for the frontend to verify the backend is live."""
    return {"status": "ok", "message": "Financial Toxicity Advocate backend is running."}


@app.post("/api/intake", response_model=IntakeResponse)
async def process_intake(request: IntakeRequest):
    """
    Core endpoint. Accepts the patient's drug, dosage, and cancer diagnosis.
    Runs the Clinical Analyzer and Grant Navigator agents concurrently
    and returns a synthesized report.
    """
    try:
        result_data = await run_orchestrator(
            drug=request.drug,
            dosage=request.dosage,
            diagnosis=request.diagnosis,
        )
        return IntakeResponse(status="success", data=result_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── MCP Testing Endpoints ────────────────────────────────────────────────────

@app.get("/api/mcp/openfda/generic", tags=["MCP Testing"])
def api_check_generic_equivalent(brand_name: str):
    """
    Check generic equivalent using OpenFDA.
    
    **Example input:**
    - `brand_name`: "Ibrance"
    """
    return check_generic_equivalent(brand_name)


@app.get("/api/mcp/openfda/indication", tags=["MCP Testing"])
def api_verify_indication(drug_name: str, cancer_type: str):
    """
    Verify drug indication for a specific cancer type using OpenFDA.
    
    **Example input:**
    - `drug_name`: "Ibrance"
    - `cancer_type`: "breast cancer"
    """
    return verify_indication(drug_name, cancer_type)


@app.get("/api/mcp/nadac/cost", tags=["MCP Testing"])
def api_get_baseline_cost(ndc_description: str, monthly_quantity: int):
    """
    Calculate baseline monthly acquisition cost using NADAC.
    
    **Example input:**
    - `ndc_description`: "IBRANCE 125 MG CAPSULE"
    - `monthly_quantity`: 21
    """
    return get_baseline_cost(ndc_description, monthly_quantity)


@app.get("/api/mcp/medicare/spending", tags=["MCP Testing"])
def api_get_medicare_spending(drug_name: str):
    """
    Get national Medicare Part D spending data for a drug.
    
    **Example input:**
    - `drug_name`: "IBRANCE"
    """
    return get_medicare_spending(drug_name)


@app.get("/api/mcp/grants/search", tags=["MCP Testing"])
def api_search_grants(cancer_type: str):
    """
    Search multiple non-profit foundations for open grants.
    Note: Can be slow because it uses headless Playwright.
    
    **Example input:**
    - `cancer_type`: "breast cancer"
    """
    result = search_grants(cancer_type)
    return json.loads(result) if isinstance(result, str) else result


@app.get("/api/mcp/grants/eligibility", tags=["MCP Testing"])
def api_check_eligibility_requirements(foundation_name: str, cancer_type: str):
    """
    Get eligibility requirements for a foundation.
    
    **Example input:**
    - `foundation_name`: "HealthWell"
    - `cancer_type`: "breast cancer"
    """
    return check_eligibility_requirements(foundation_name, cancer_type)


@app.get("/api/mcp/grants/agent", tags=["MCP Testing"])
async def api_run_grant_agent(diagnosis: str):
    """
    Run the grant agent for a specific cancer type.
    
    **Example input:**
    - `cancer_type`: "breast cancer"
    """
    grant_query = (
        f"Find financial assistance programs for a patient with '{diagnosis}'. "
        "1. Use search_grants to find OPEN funds across all foundations. "
        "2. Use check_eligibility_requirements for the general eligibility rules. "
        "Return: list of OPEN funds, direct application URLs, and any obvious disqualifiers "
        "(e.g. 'Medicare excluded', income caps). Do NOT make eligibility judgments."
    )
    session_service = InMemorySessionService()
    grant_result = await  _run_grant_navigator(
        diagnosis=diagnosis,
        session_service=session_service, 
    )
    return grant_result

   
