"""
FastAPI Backend Server
======================
Exposes the multi-agent ADK orchestrator over REST for the Next.js frontend.

Start with: uv run uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from adk_orchestrator import run_orchestrator

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


# ── Request / Response models ────────────────────────────────────────────────

class IntakeRequest(BaseModel):
    drug: str
    dosage: str
    diagnosis: str


class IntakeResponse(BaseModel):
    status: str
    data: dict


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

    Expected JSON body:
    {
        "drug": "Ibrance",
        "dosage": "125mg once daily",
        "diagnosis": "breast cancer"
    }
    """
    try:
        result = await run_orchestrator(
            drug=request.drug,
            dosage=request.dosage,
            diagnosis=request.diagnosis,
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
