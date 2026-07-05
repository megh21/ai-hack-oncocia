# Project Status: Financial Toxicity Advocate

> Last updated: 2026-07-04

## ✅ Completed

### MCP Data Layer (Tool Servers)
| File | Purpose | Status |
|---|---|---|
| `backend/mcp_openfda.py` | FDA drug validation (Rx-only, indication matching) | ✅ Tested |
| `backend/mcp_nadac.py` | CMS NADAC cost per unit (DKAN API, exact+partial match) | ✅ Tested |
| `backend/mcp_medicare.py` | CMS Medicare Part D avg cost per claim | ✅ Built |
| `backend/mcp_grants.py` | Non-profit grant scraper (Playwright headless — HealthWell, TotalAssist, NeedyMeds, RxAssist) | ✅ Playwright working |

### Backend Infrastructure
| File | Purpose | Status |
|---|---|---|
| `backend/main.py` | FastAPI server with CORS, `/api/health`, `/api/intake` | ✅ Running on :8000 |
| `backend/adk_orchestrator.py` | Google ADK orchestrator — Clinical Analyzer + Grant Navigator agents | ✅ Wired, fixing runtime |
| `backend/.env` | `GOOGLE_API_KEY` configured | ✅ Set |
| `backend/pyproject.toml` | `uv` project with all deps | ✅ `uv sync` done |

---

## 🔧 In Progress / Fixing Now

| Item | Issue | Fix |
|---|---|---|
| `McpToolset` async context manager error | ADK 2.3.x changed the API — toolsets are passed directly to `Agent.tools`, not used with `async with` | ✅ Fixed in latest `adk_orchestrator.py` |
| ADK `Runner` init + run_async args | `app_name` was missing from `Runner` and `run_async` kwargs were changed | ✅ Fixed (`app_name`, `session_id`, `new_message` passed correctly) |
| LLM not connected | `.env` was empty, `GOOGLE_API_KEY` not loaded | ✅ Fixed — key written to `.env`, `load_dotenv` added |

---

## 🔲 Not Yet Started (PRD Remaining)

### Phase 1 PRD — Core workflow (Priority)
| Item | Description |
|---|---|
| **End-to-end test** | Verify `/api/intake` returns real FDA + NADAC + grant data (not placeholders) |
| **Next.js frontend** | Patient intake form (`drug` + `dosage` + `diagnosis`), results dashboard |
| **Frontend → Backend wiring** | POST to `/api/intake`, render clinical report + open grant funds |

### Phase 2 PRD — Enhancements
| Item | Description |
|---|---|
| **Bureaucracy Copilot Agent** | Agent 3 — draft appeal/prior auth letters based on clinical + grant results |
| **CMS Medicare UUID fix** | The Part D dataset UUID may be stale; verify correct UUID or switch to CSV download |
| **Grant scraping accuracy** | HealthWell returns 1 closed fund via Playwright — tune CSS selectors to extract names + direct apply links |

### Phase 3 PRD — Polish
| Item | Description |
|---|---|
| **System prompt guardrails** | Hard "no medical advice" guardrail layer on all agents |
| **Streaming responses** | Stream agent output chunks to frontend via SSE instead of waiting for full completion |
| **Error UX** | Frontend handles partial failures gracefully (e.g., "Grant data unavailable, try these direct links") |
| **Dockerize** | `Dockerfile` for `backend/` for production deployment |

---

## 📋 Architecture Summary
```
Patient Input (Next.js) → POST /api/intake (FastAPI)
  → ADK Orchestrator (asyncio.gather)
      ├── Clinical Analyzer Agent
      │     ├── mcp_openfda → FDA validation
      │     ├── mcp_nadac   → baseline cost ($/unit)
      │     └── mcp_medicare → avg Medicare cost/claim
      └── Grant Navigator Agent
            └── mcp_grants → Playwright scrape (HealthWell, TotalAssist, NeedyMeds, RxAssist)
  → Synthesized JSON report → Frontend dashboard
```
