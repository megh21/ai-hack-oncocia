# MASTER SYSTEM SPECIFICATION: PROJECT Oncocia
*Target:* Google Antigravity 2.0 IDE / CLI
*Operation:* Scaffold, code, evaluate, and deploy a multi-agent system.

## 1. [META & HACKATHON CONTEXT]
*   *Event Context:* Kaggle 5-Day AI Agents: Intensive Vibe Coding Capstone Project With Google (https://www.kaggle.com/competitions/5-day-ai-agents-intensive-vibecoding-course-with-google).
*   *Track:* Agents for Good (Healthcare/Patient-Centric).
*   *Project Name:* Project Oncocia - The Financial Toxicity & Access Agent.
*   *Objective:* Build a "10x Agent" system using the Agent Development Kit (ADK) that mitigates financial toxicity for oncology patients by dynamically sourcing open-source cost data and non-profit grants.

## 2. [ARCHITECTURE & FRAMEWORKS]
Generate a Python-based backend using the frameworks taught in the course:
*   *Orchestration:* Use the *Agent Development Kit (ADK)* for Agent-to-Agent (A2A) communication and workflow definition.
*   *Tooling Bridge:* Implement *Model Context Protocol (MCP)* servers to connect the agents to external government REST APIs and web scraping tools.
*   *LLM Engine:* Use Gemini 1.5 Flash via Google AI Studio API for all agent reasoning (optimized for long context, tool calling, and free-tier rate limits).
*   *Frontend:* Create a lightweight asynchronous web application using nextjs and tailwind css.
*   *UI/UX design:* simple, clean, and modern. making it specifc to oncological patients, colors should be soothing for patients. Use soft colors like pastels, light blues, and gentle grays or soft warm colors. Avoid harsh or dark colors. The website should be easy to navigate and use, patient should be able to find information easily. Use font sizes of atleast 20px. Maintain consistency in the UI design and maintain it throughout the website. Provide feedback to the user at each step. Use simple and easy to understand language. Avoid technical jargon.
*   *Deployment Target:* Google Cloud 

## 3. [MCP SERVERS & DATA SOURCES]
Scaffold two distinct MCP servers to act as the canonical, machine-readable data sources for the agents. Neither requires authentication.

*MCP Server 1: OpenFDA Clinical Mapper*
*   *Endpoint:* https://api.fda.gov/drug/label.json
*   *Tools to Expose to ADK:* 
    *   check_generic_equivalent(brand_name: str) -> Queries the FDA Orange Book data via the OpenFDA API to return generic names (openfda.generic_name) and pharmacological class.
    *   verify_indication(drug_name: str, cancer_type: str) -> Parses indications_and_usage to verify clinical alignment.

*MCP Server 2: CMS NADAC Cost Calculator*
*   *Endpoint:* https://data.medicaid.gov/resource/dfa2ab14-06c2-457a-9e36-5cb6d80f8d93.json (National Average Drug Acquisition Cost Socrata API)
*   *Tools to Expose to ADK:*
    *   get_baseline_cost(ndc_description: str, monthly_quantity: int) -> Queries the dataset, extracts nadac_per_unit, and calculates the baseline monthly acquisition cost.

*Agent Tool: Non-Profit Scraper*
*   *Functionality:* Create a BeautifulSoup/Requests Python tool that searches target non-profit foundation sites (e.g., PAN Foundation, HealthWell) for the string "OPEN" adjacent to the patient's cancer type.

## 4. [AGENT DEFINITIONS (ADK)]
Define the following three agents in the ADK registry with distinct system prompts and states:

*   *Agent 1: The Clinical & Cost Analyzer*
    *   Role: Map prescribed drugs to generics and calculate financial exposure.
    *   Tools Permissions: OpenFDA MCP, CMS NADAC MCP.
    *   Output: Structured JSON passing the drug profile and financial gap to Agent 2.
*   *Agent 2: The Grant Navigator*
    *   Role: Find live, open financial assistance grants.
    *   Tools Permissions: Non-Profit Scraper Tool.
    *   Output: A verified active grant and its eligibility requirements (e.g., Household Income limits).
*   *Agent 3: The Bureaucracy Copilot*
    *   Role: Patient communication and document generation.
    *   Tools Permissions: Context Memory, PDF/DocX Generator.
    *   Output: A conversational triage identifying patient eligibility, terminating in the generation of a customized "Letter of Medical Necessity".

## 5. [SECURITY, EVALUATIONS & GUARDRAILS]
Implement the Day 4 course requirements for Security and Evaluation:
*   *Guardrails:* Hardcode system prompts enforcing "Zero-Knowledge Medical Advice." If a user asks about dropping a therapy or changing a dose, the agent must trigger a fallback response directing them to their oncologist.
*   *Threat Scans:* Implement automated testing against prompt injection (e.g., users trying to make the agent approve fake grants). 
*   *Evaluations:* Write local ADK evaluation scripts to test token optimization and trace the A2A communication trajectory.
*   *Observability:* Integrate *OpenTelemetry* to trace agent API calls, tool execution times, and context window usage.

## 6. [EXECUTION DIRECTIVE FOR ANTIGRAVITY]
1.  Initialize the project directory structure.
2.  Generate the requirements.txt encompassing ADK, MCP libraries, OpenTelemetry, and Streamlit.
3.  Write the mcp_openfda.py and mcp_nadac.py server files.
4.  Write the adk_orchestrator.py file defining the 3 agents and their workflow.
5.  Generate a Dockerfile optimized for Google Cloud Run deployment.
6.  Provide instructions on how to start the local evaluation harness.
7. developing suitable frontend.
8. testing and iterating on the frontend and backend to ensure the system is working as expected.
9. Document the code and the system architecture.