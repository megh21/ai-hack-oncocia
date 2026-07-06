Here is a comprehensive, enterprise-grade Product Requirements Document (PRD) for the Oncology Financial Toxicity & Access Agent. We are stepping away from the hackathon constraints to map out a robust, scalable prototype that leverages your IQVIA data analytics background and strict open-source data integrations.
# Product Requirements Document (PRD)
*Product Name:* Project Oncocia (Financial Toxicity Multi-Agent System)
*Document Version:* 1.0
*Target Audience:* Oncology patients prescribed tier-3/tier-4 specialty oral oncolytics (e.g., Ibrance, Tagrisso, Imbruvica) facing therapy abandonment due to out-of-pocket costs.
## 1. Executive Summary
### 1.1 The Problem
"Financial toxicity" is a clinically recognized side effect of modern oncology. Patients frequently face $2,000 to $15,000 monthly out-of-pocket costs for oral oncolytics. Navigating generic alternatives, calculating real-world costs, and sourcing non-profit financial grants requires analyzing disjointed datasets while the patient is physically and emotionally compromised.
### 1.2 The Solution
Project Oncocia is an autonomous, multi-agent LLM system that acts as a financial advocate. It ingests a patient’s prescribed regimen, dynamically queries federal databases to calculate acquisition costs and generic availability, scrapes non-profit sites for active funding cycles, and automates the burdensome application paperwork (Letters of Medical Necessity).
## 2. Multi-Agent Architecture (A2A Workflow)
The prototype relies on an Agent-to-Agent (A2A) orchestration model, ensuring complex tasks are divided among specialized "experts."
| Agent Role | Primary Function | Primary Tools & Capabilities |
|---|---|---|
| *The Clinical & Cost Analyzer* | Identifies the drug, maps it to generic equivalents, and calculates baseline national acquisition cost. | openFDA API, CMS NADAC API |
| *The Grant Navigator* | Scrapes live non-profit foundation sites to identify currently open funding cycles for the specific cancer indication. | Web Scraper/Search Tool (BeautifulSoup) |
| *The Bureaucracy Copilot* | Interviews the patient for eligibility (household size, income) and generates tailored PDF application documents. | Context memory, PDF/DocX Generator |
## 3. Data Source Integrations & API Specifications
To build a resilient prototype without paid data vendors, the system relies on live Model Context Protocol (MCP) servers connected to verifiable U.S. government endpoints.
### 3.1 OpenFDA API (Generic & Clinical Mapping)
 * *Purpose:* To verify the drug classification, active ingredients, and check the FDA Orange Book for generic equivalents.
 * *Endpoint:* [https://api.fda.gov/drug/label.json](https://api.fda.gov/drug/label.json)
 * *Query Structure:* ?search=openfda.brand_name:"[DRUG_NAME]"
 * *Key JSON Extraction Targets:*
   * openfda.generic_name (To map to cheaper alternatives)
   * openfda.pharm_class_epc (To verify the oncological drug class)
   * indications_and_usage (To cross-reference the patient's cancer type with approved uses)
### 3.2 CMS NADAC API (Cost Calculation)
 * *Purpose:* The National Average Drug Acquisition Cost (NADAC) dataset provides the actual baseline cost pharmacies pay for the drug. This anchors the financial reality before insurance.
 * *Endpoint:* Socrata API [https://data.medicaid.gov/resource/](https://data.medicaid.gov/resource/)[DATASET_IDENTIFIER].json
 * *Query Structure:* SoQL (Socrata Query Language) filtering by ndc_description.
 * *Key JSON Extraction Targets:*
   * nadac_per_unit (The cost per pill/ml)
   * pricing_unit (EA, ML, GM)
   * effective_date (To ensure the agent uses the most recent pricing data)
### 3.3 Non-Profit Grant Scraping (Real-Time Availability)
 * *Purpose:* REST APIs do not exist for most patient assistance non-profits (e.g., PAN Foundation, HealthWell Foundation). Grants open and close daily based on funding.
 * *Mechanism:* Python-based web scraper tool given to the *Grant Navigator Agent*.
 * *Target Logic:* The agent parses the target foundation's "Disease Funds" HTML tables. It searches for regex matches of the patient's cancer type (e.g., "Breast Cancer") and evaluates the adjacent sibling elements for the text "OPEN" or "CLOSED".
## 4. Core User Workflows
### Phase 1: Intake & Assessment
 1. *User Input:* The patient inputs their prescribed drug, dosage, and specific cancer diagnosis.
 2. *Validation:* The Clinical Analyzer queries the openFDA API to confirm the drug matches the indication.
 3. *Cost Baseline:* The Clinical Analyzer queries the NADAC database, multiplying the nadac_per_unit by the patient's monthly dosage to establish the "Worst-Case Uninsured Cost" as a baseline.
### Phase 2: The Funding Hunt
 1. *Generic Check:* The system alerts the patient if a generic equivalent was recently approved via the FDA Orange Book.
 2. *Live Scraping:* The Grant Navigator accesses predefined URLs for the top 5 oncology assistance foundations. It extracts only funds matching the user's specific cancer type and filters out "Waitlisted" or "Closed" funds.
### Phase 3: Action & Bureaucracy
 1. *Conversational Triage:* The Bureaucracy Copilot asks 2-3 targeted questions based on the specific open grant's requirements (e.g., "The HealthWell fund requires your income to be under 500% of the Federal Poverty Level. Is your household income under $150,000?").
 2. *Document Generation:* Upon confirmation, the agent drafts a customized "Letter of Medical Necessity." The letter automatically incorporates the drug's active ingredient, the FDA indication, and placeholders for the oncologist's NPI number and signature.
## 5. Product Refinements, Guardrails & Constraints
In healthcare analytics, the cost of a "hallucination" is high. The prototype must implement strict boundaries.
 * *Financial Disclaimer Overlays:* The UI must permanently display that calculated NADAC costs are wholesale averages and do not represent exact copays, which are dictated by specific insurance formularies.
 * *Zero-Knowledge Medical Advice:* System prompts for the Clinical Analyzer must include strict negative constraints: "You are a financial navigator, not an oncologist. Under no circumstances will you suggest dropping a therapy, altering a dose, or switching to a generic without explicit instruction for the patient to consult their prescribing physician."
 * *Data Freshness Enforcement:* The system must validate the effective_date on all NADAC pulls. If the pricing data is older than 90 days, the agent must inform the user that the cost estimate may be outdated.
 * *PII/HIPAA Compliance (Even for Prototype):* Ensure the frontend does not log or store the patient's income, exact name, or household size in the database. All conversation state should exist only in the temporary session context window.
This PRD moves you from a conceptual hackathon idea to a structured, data-driven software architecture using verifiable government endpoints.
To refine the actual backend development of this prototype, should we write the exact Python data-fetching script for the openFDA API, or focus on the web-scraping logic for the non-profit foundation sites?