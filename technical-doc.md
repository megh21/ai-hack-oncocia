# Project OncoAccess Technical Documentation

This document describes the current backend architecture in the repository, the target PRD architecture, and the implementation plan for turning the prototype into a production-ready, hackathon-complete oncology financial toxicity assistant.

## 1. Product Goal

Project OncoAccess is a multi-agent healthcare access assistant for oncology patients facing high out-of-pocket drug costs. The system combines:

- clinical validation of a drug and diagnosis pair,
- baseline cost estimation from public government pricing data,
- live search for patient assistance grants,
- and future document generation for applications and medical necessity letters.

The design intent is to keep the system grounded in public, verifiable data sources and to avoid medical advice beyond navigation and financial support.

## 2. Current Repository Architecture

The repository is already organized as a monorepo with a clear backend focus.

### 2.1 Top-level layout

- `input.md`: hackathon instruction file that defines the expected Antigravity workflow, agent stack, and execution constraints.
- `PRD.md`: product-level requirements and user workflows for the financial toxicity prototype.
- `ai-hack-oncocia/`: main project folder containing architecture notes, status, and the backend source tree.

### 2.2 Backend package layout

The backend currently lives in `ai-hack-oncocia/backend/` and uses `uv` as the Python environment and dependency manager.

Current backend modules:

- `main.py`: FastAPI REST surface that exposes health, intake, and MCP test endpoints.
- `adk_orchestrator.py`: Google ADK orchestration layer that coordinates specialized agents.
- `mcp_openfda.py`: MCP tool server for FDA label lookup and indication validation.
- `mcp_nadac.py`: MCP tool server for CMS NADAC-based cost lookup.
- `mcp_grants.py`: MCP tool server for non-profit grant scraping.
- `mcp_medicare.py`: extra MCP tool server for Medicare Part D spending context.

### 2.3 Runtime shape

The current runtime is:

1. Patient submits a drug, dosage, and diagnosis to the FastAPI backend.
2. `main.py` forwards the intake payload to `run_orchestrator()` in `adk_orchestrator.py`.
3. The orchestrator spins up ADK agents with MCP toolsets.
4. The Clinical Analyzer queries openFDA, NADAC, and Medicare context.
5. The Grant Navigator queries the grants scraper.
6. Results are merged into a single JSON response returned to the frontend client.

## 3. Target Architecture From the PRD

The PRD and hackathon instruction file define a richer target architecture than the current code already implements. The intended final system has these layers:

### 3.1 Agent orchestration layer

The orchestration layer is the core of the application. It should use the Google Agent Development Kit to manage agent-to-agent workflows and tool execution.

Target agents:

- Clinical & Cost Analyzer
- Grant Navigator
- Bureaucracy Copilot

### 3.2 Tooling layer

The agents should not call external data sources directly. Instead, they should use MCP servers or tool wrappers.

Planned canonical tools:

- OpenFDA clinical mapper
- CMS NADAC cost calculator
- non-profit scraper tool

The current repo also includes an optional Medicare context tool and a broader grant aggregation implementation. Those are useful prototype extensions, but they are not part of the minimum PRD scope.

### 3.3 Frontend layer

The user-facing application should be a lightweight asynchronous interface, with Streamlit or Gradio as the preferred prototype UI. The frontend should capture only the minimum patient inputs needed for the workflow:

- drug name,
- dosage,
- cancer diagnosis,
- and optional grant-eligibility answers if the workflow expands.

### 3.4 Deployment layer

The target deployment model is stateless containerized hosting on Google Cloud Run.

## 4. Current Implementation Details

### 4.1 FastAPI application (`main.py`)

`main.py` is the service boundary for the backend.

Responsibilities:

- exposes `/api/health` for liveness checks,
- exposes `/api/intake` for the end-to-end patient workflow,
- exposes debugging endpoints for each MCP tool module,
- enables CORS for local frontend integration,
- converts backend exceptions into HTTP 500 responses.

Important implementation detail:

- the backend currently imports and calls Python functions from the MCP modules directly for testing convenience,
- but the production architecture still treats those modules as MCP-compatible tool providers.

### 4.2 ADK orchestrator (`adk_orchestrator.py`)

This file is the current control plane.

Responsibilities:

- loads `GOOGLE_API_KEY` from the backend `.env` file,
- builds MCP tool connections using stdio transport,
- constructs ADK `Agent` instances for the clinical and grant flows,
- runs both flows concurrently with `asyncio.gather`,
- returns a synthesized report object to the API layer.

Observed current design:

- the orchestrator is already split into two concurrent lanes,
- session handling is in-memory,
- tool access is prefix-scoped by MCP toolset name,
- the LLM model is configured as Gemini Flash.

### 4.3 OpenFDA MCP server (`mcp_openfda.py`)

This server validates whether a drug label exists and whether a diagnosis appears in the label’s indication text.

Capabilities:

- `check_generic_equivalent(brand_name)`
- `verify_indication(drug_name, cancer_type)`

Behavior:

- queries `https://api.fda.gov/drug/label.json`,
- retries with broader search terms if exact brand matches fail,
- extracts `openfda.generic_name`, `openfda.pharm_class_epc`, and related label metadata,
- returns structured warning flags if the label looks unstructured or non-prescription.

### 4.4 NADAC MCP server (`mcp_nadac.py`)

This server estimates acquisition cost using CMS NADAC data.

Capabilities:

- `get_baseline_cost(ndc_description, monthly_quantity)`

Behavior:

- queries the Medicaid data endpoint,
- tries exact and partial matches,
- reads `nadac_per_unit`, `pricing_unit`, and `effective_date`,
- computes a baseline monthly cost,
- emits a freshness warning when the data is older than 90 days.

### 4.5 Grants MCP server (`mcp_grants.py`)

This server aggregates non-profit assistance opportunities.

Capabilities:

- scrapes HealthWell,
- scrapes TotalAssist / PAN-style sources,
- queries NeedyMeds,
- queries RxAssist,
- normalizes funds into open, closed, and direct-link output.

Behavior:

- uses Playwright for JS-heavy sources,
- uses Requests and BeautifulSoup for static sites,
- returns a consolidated, source-tagged grant response.

### 4.6 Medicare MCP server (`mcp_medicare.py`)

This module extends the prototype beyond the minimum PRD scope.

Purpose:

- provide Medicare Part D spending context,
- help compare national payer context against NADAC acquisition cost.

This is a useful enhancement but should be treated as optional if the final submission wants to stay tightly aligned to the PRD.

## 5. Data Flow and Business Logic

### 5.1 Intake flow

1. User enters a prescribed oncology drug, dosage, and diagnosis.
2. FastAPI validates the request schema.
3. The orchestrator sends the case to the Clinical Analyzer.
4. The Clinical Analyzer checks FDA labeling and baseline acquisition cost.
5. The Grant Navigator searches for matching open grants.
6. The API returns a combined JSON report.

### 5.2 Clinical decision boundaries

The system should never tell the patient to:

- stop therapy,
- change dose,
- switch to a generic,
- or treat the output as medical advice.

Instead, it should direct the patient back to the prescribing oncologist for treatment decisions.

### 5.3 Financial logic

The output should clearly distinguish between:

- wholesale baseline cost from NADAC,
- possible real-world spending context,
- and actual patient copay or assistance outcomes.

The system should make the pricing caveat explicit because NADAC is not the same as the patient’s final out-of-pocket cost.

## 6. Environment and Local Development

The backend is intended to run inside a `uv`-managed virtual environment.

### 6.1 Local setup

Recommended steps:

1. Change into `ai-hack-oncocia/backend`.
2. Sync dependencies with `uv sync`.
3. Ensure `.env` contains `GOOGLE_API_KEY`.
4. Start the API with `uv run uvicorn main:app --reload --port 8000`.

### 6.2 Useful local endpoints

- `GET /api/health` for service health.
- `POST /api/intake` for the main workflow.
- `/api/mcp/openfda/*` for OpenFDA checks.
- `/api/mcp/nadac/*` for cost estimation.
- `/api/mcp/grants/*` for grant discovery.

## 7. Security, Privacy, and Compliance Constraints

The project operates in a healthcare-adjacent context, so the architecture needs strong data handling rules even in prototype form.

Required constraints:

- do not store exact patient name, household size, or income in persistent logs,
- keep conversation state ephemeral unless explicitly needed for the live session,
- display a cost disclaimer wherever NADAC estimates are surfaced,
- treat all data-source results as informational rather than diagnostic or therapeutic guidance.

Recommended engineering controls:

- in-memory session state only for the prototype,
- no database persistence for PII,
- structured prompt guardrails for medical boundaries,
- explicit freshness checks on cost datasets,
- basic prompt-injection testing for grant-source manipulation.

## 8. Observability and Evaluation

The PRD calls for a more mature control plane around tracing and quality checks.

Planned observability surface:

- OpenTelemetry traces for agent execution,
- tool-call timing metrics,
- context size and token usage inspection,
- structured logs for success/failure and data freshness.

Planned evaluation surface:

- regression tests for common drug/diagnosis combinations,
- injection tests that try to coerce fake grants or medical advice,
- trace review for A2A sequence correctness,
- latency checks for the scraping toolchain.

## 9. Implementation Plan

This is the recommended build order to finish the prototype in a disciplined way.

### Phase 1: Stabilize the existing backend

Goals:

- keep the current FastAPI and ADK integration working end-to-end,
- verify the current MCP modules return structured outputs consistently,
- confirm the `uv` workflow is reproducible.

Deliverables:

- working `/api/intake` flow,
- validated MCP server calls,
- stable local startup instructions.

### Phase 2: Align the architecture with the PRD

Goals:

- reduce the system to the PRD core tools where necessary,
- formalize the three-agent workflow,
- add explicit guardrail prompts and output schemas.

Deliverables:

- Clinical Analyzer agent prompt contract,
- Grant Navigator agent prompt contract,
- Bureaucracy Copilot stub or implementation plan.

### Phase 3: Add the frontend

Goals:

- build a minimal but polished Streamlit or Gradio interface,
- keep the input form simple,
- present structured results with a prominent disclaimer.

Deliverables:

- input form,
- results dashboard,
- state-safe session handling.

### Phase 4: Add deployment and hardening

Goals:

- produce a Cloud Run-ready Dockerfile,
- ensure stateless runtime behavior,
- add observability and testing.

Deliverables:

- container build,
- runtime configuration docs,
- guardrail and injection tests.

## 10. Recommended Technical Contracts

To keep the codebase maintainable, the following contracts should stay stable.

### 10.1 Intake request schema

Expected fields:

- `drug`
- `dosage`
- `diagnosis`

### 10.2 Clinical analyzer output schema

Expected fields:

- drug identity and label match result,
- generic equivalent data,
- baseline cost estimate,
- freshness / warning metadata,
- medical-boundary disclaimer.

### 10.3 Grant navigator output schema

Expected fields:

- open grants,
- closed or waitlisted grants,
- foundation source metadata,
- application or verification URLs,
- eligibility hints and disclaimers.

### 10.4 Bureaucracy copilot output schema

Expected fields:

- triage questions,
- eligibility checkpoint responses,
- generated document artifact path or content reference,
- disclaimer that the letter is not legal or medical advice.

## 11. Risks and Gaps

Current gaps relative to the PRD:

- the Bureaucracy Copilot agent is not yet implemented,
- frontend work is still missing,
- observability is not yet wired end-to-end,
- guardrail prompts are still implicit rather than formalized,
- the extra Medicare integration may complicate scope if the submission needs to stay minimal.

Primary technical risks:

- scraping instability on JS-rendered foundation sites,
- stale or changing government dataset schemas,
- overreliance on in-memory session state for multi-step user flows,
- prompt injection into grant discovery or document generation.

## 12. Final Recommendation

The current codebase already has the right skeleton: FastAPI as the service boundary, ADK as the orchestrator, and MCP modules for data access. The next work should not be new architecture for its own sake. It should be a disciplined completion of the PRD contract: harden the existing agents, add the missing Bureaucracy Copilot and frontend, and wrap the system in guardrails, tracing, and deployment hygiene.
