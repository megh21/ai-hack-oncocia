
# Project Oncocia

Private monorepo for the oncology financial toxicity and access assistant.

## Structure

- `backend/` FastAPI app, ADK orchestration, and MCP tools
- `frontend/` patient-facing web UI
- `misc/` supporting notes and experiments

## Local setup

1. Install Python dependencies in `backend/`.
2. Keep secrets out of git; use `.env` or local token files only.
3. Run the backend first, then connect the frontend to `/api/intake`.

## Repository notes

- Default branch: `main`
- GitHub visibility: private
