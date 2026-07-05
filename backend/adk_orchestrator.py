"""
ADK Orchestrator: Multi-Agent Financial Toxicity Advocate
=========================================================
Coordinates:
  1. Clinical Analyzer Agent  — uses OpenFDA + NADAC + Medicare MCP tools
  2. Grant Navigator Agent    — uses Grants (Playwright) MCP tool

Uses Google ADK 2.3.x with stdio-based MCP server connections.
McpToolset is passed directly to Agent.tools — NOT used as an async context manager.
"""

import asyncio
import os
from pathlib import Path
from typing import Any, Dict

from dotenv import load_dotenv
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioServerParameters

# Load .env so GOOGLE_API_KEY is available to the ADK / genai SDK
load_dotenv(Path(__file__).parent / ".env")

BACKEND_DIR = Path(__file__).parent.resolve()
UV_CMD = "uv"
GEMINI_MODEL = "gemini-2.0-flash"


def _mcp_toolset(script: str, prefix: str) -> McpToolset:
    """Returns a McpToolset connected to the given local MCP server script."""
    return McpToolset(
        connection_params=StdioServerParameters(
            command=UV_CMD,
            args=["run", "python", str(BACKEND_DIR / script)],
            env=dict(os.environ),   # pass full env so .env vars are available
        ),
        tool_name_prefix=prefix,
    )


async def run_orchestrator(
    drug: str,
    dosage: str,
    diagnosis: str,
) -> Dict[str, Any]:
    """
    Runs the full multi-agent orchestration pipeline.

    Phase 1: Clinical Analyzer validates indication + establishes cost baseline.
    Phase 2: Grant Navigator hunts for open financial assistance funds.
    Both phases run concurrently via asyncio.gather.
    """
    session_service = InMemorySessionService()

    clinical_query = (
        f"Patient regimen — Drug: {drug}, Dosage: {dosage}, Diagnosis: {diagnosis}. "
        "1. Use fda_ tools to validate this drug is FDA-approved for the diagnosis. "
        "2. Use nadac_ tools to get the baseline cost per unit (nadac_per_unit). "
        "3. Use medicare_ tools to get the national Medicare Part D average cost per claim. "
        "Return a concise structured report. If a tool fails, note it and continue."
    )

    grant_query = (
        f"Find financial assistance programs for a patient with '{diagnosis}'. "
        "1. Use grants_search_grants to find OPEN funds across all foundations. "
        "2. Use grants_check_eligibility_requirements for the general eligibility rules. "
        "Return: list of OPEN funds, direct application URLs, and any obvious disqualifiers "
        "(e.g. 'Medicare excluded', income caps). Do NOT make eligibility judgments."
    )

    clinical_result, grant_result = await asyncio.gather(
        _run_clinical_analyzer(clinical_query, session_service),
        _run_grant_navigator(grant_query, diagnosis, session_service),
    )

    return {
        "patient_regimen": {
            "drug": drug,
            "dosage": dosage,
            "diagnosis": diagnosis,
        },
        "clinical_analysis": clinical_result,
        "grant_navigation": grant_result,
    }


async def _run_clinical_analyzer(
    query: str,
    session_service: InMemorySessionService,
) -> Dict[str, Any]:
    """Clinical Analyzer: validates indication, retrieves NADAC + Medicare costs."""
    try:
        # McpToolset is passed directly to Agent.tools — no context manager needed
        clinical_agent = Agent(
            name="clinical_analyzer",
            model=GEMINI_MODEL,
            instruction=(
                "You are a Clinical Cost Analyzer for an oncology financial advocacy service. "
                "Your role is strictly informational — you do NOT give medical advice. "
                "Given a drug, dosage, and diagnosis:\n"
                "1. Use fda_ tools to validate the drug is approved for the diagnosis.\n"
                "2. Use nadac_ tools to get the baseline acquisition cost per unit.\n"
                "3. Use medicare_ tools to get the national Medicare average cost per claim.\n"
                "Return a concise structured report with all three data points. "
                "If a tool fails or returns no data, note the error clearly."
            ),
            tools=[
                _mcp_toolset("mcp_openfda.py", "fda_"),
                _mcp_toolset("mcp_nadac.py", "nadac_"),
                _mcp_toolset("mcp_medicare.py", "medicare_"),
            ],
        )

        runner = Runner(
            agent=clinical_agent,
            session_service=session_service,
            auto_create_session=True,
        )

        response_parts = []
        async for event in runner.run_async(user_id="patient_clinical", prompt=query):
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_parts.append(part.text)

        return {
            "status": "ok",
            "report": "\n".join(response_parts) or "No clinical data returned.",
        }

    except Exception as e:
        return {"status": "error", "error": f"Clinical Analyzer failed: {str(e)}"}


async def _run_grant_navigator(
    query: str,
    diagnosis: str,
    session_service: InMemorySessionService,
) -> Dict[str, Any]:
    """Grant Navigator: finds OPEN financial assistance funds via Playwright scrapers."""
    try:
        grant_agent = Agent(
            name="grant_navigator",
            model=GEMINI_MODEL,
            instruction=(
                "You are a Grant Navigator for an oncology financial advocacy service. "
                "You help patients find financial assistance — you do NOT confirm eligibility "
                "or give medical advice. Given a cancer diagnosis:\n"
                "1. Use grants_search_grants to find OPEN funds across all foundations.\n"
                "2. Use grants_check_eligibility_requirements for the eligibility rules.\n"
                "Return a clear list of open funds with direct application URLs and raw "
                "eligibility criteria so patients can self-assess. Flag obvious disqualifiers "
                "only when highly confident (e.g., 'this fund excludes Medicare patients')."
            ),
            tools=[
                _mcp_toolset("mcp_grants.py", "grants_"),
            ],
        )

        runner = Runner(
            agent=grant_agent,
            session_service=session_service,
            auto_create_session=True,
        )

        response_parts = []
        async for event in runner.run_async(user_id="patient_grants", prompt=query):
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_parts.append(part.text)

        return {
            "status": "ok",
            "report": "\n".join(response_parts) or "No grant data returned.",
        }

    except Exception as e:
        return {"status": "error", "error": f"Grant Navigator failed: {str(e)}"}
