
## What documents does a real oncology financial-toxicity patient actually have?
In practice, a patient (or their caregiver) navigating this problem is typically holding some subset of:

Prescription / Rx — from the oncologist, drug name + dosage + frequency
EOB (Explanation of Benefits) — from their insurer, showing what was billed, what insurance paid, and what patient owes
Prior Authorization denial letter — if insurance refused to cover the drug or required step-therapy first
Pharmacy cost statement/receipt — actual specialty pharmacy quote, often wildly different from EOB estimates
Insurance card — plan type (commercial/Medicare/Medicaid), which changes which grant programs they even qualify for (many foundations exclude Medicare patients due to anti-kickback law restrictions — this is a real, important eligibility filter your Grant Navigator should know about)
Income verification — pay stub or last year's tax return (needed for grant eligibility, e.g. "under 500% FPL")
Letter of Medical Necessity — sometimes already drafted by the oncologist, sometimes needs to be generated (this is your Bureaucracy Copilot's output, interestingly — patients sometimes arrive with one already, other times need one generated)

## What does exist and is legitimately real:

Template/sample EOBs and denial letters that CMS, insurers, and patient-advocacy orgs (Patient Advocate Foundation, Triage Cancer) publish publicly as educational examples — these are real-format documents, just not tied to a real person. That's your realistic middle ground: real document structure, fabricated person.

## Note
sorry but without actually dealing with the docs as EOB (Explanation of Benefits) and other from insurer, doctors diagnosis some document this doesn't seem to give justice. we will Skip BAA will just mention that in ppt. will skip PII/PHI redaction will mention in ppt. 

## Suggested documents to support (pick 2-3, not all, given time)
Ranked by demo impact vs. build effort:

Explanation of Benefits (EOB) — highest value. It contains billed amount, insurance-allowed amount, and patient responsibility — this is the single richest document for validating your NADAC-based cost estimate against something "real." CMS and several insurers (BCBS, UHC) publish sample EOB templates publicly for member education — use one of those as your test fixture.
Prior Authorization Denial Letter — high narrative value for the demo ("look, the agent sees the denial reason and adapts the grant search accordingly"). Sample templates are published by Patient Advocate Foundation and Triage Cancer as denial-appeal educational examples.
Prescription/Rx — simplest to parse (drug, dose, frequency, prescriber NPI), good as your "baseline" document, lowest ambiguity.

I'd deprioritize income verification (pay stubs/tax returns) — highest PHI sensitivity, lowest agentic payoff, since your persona already states income directly.
Preprocessing pipeline (conceptual, per document)

Ingestion & format normalization — accept PDF/image, run OCR diorectly with llms from gemini probably while preserving rough spatial layout (needed for table-heavy EOBs). for pdfs we treat them as images, and send each page as image(png) to llm, and then create the ingestion. where a diagram is explained with prompt and a table is enriched with context along with having the text layout of it preserved. and converting to md.
Document classification — a quick classifier/prompt step to identify which of the 3 document types this is, since each has a different extraction schema downstream.
PII/PHI redaction pass — we skip this
Structured field extraction — schema-driven extraction per document type (e.g., for EOB: billed amount, allowed amount, patient responsibility, denial reason code if present; for Rx: drug name, dose, frequency, prescriber). This is where you'd use a constrained/structured-output LLM call. with a proper json output for easier parsing.
Validation & cross-check — the extracted drug name gets cross-checked against openFDA (same call your Clinical Analyzer already makes) to catch OCR errors (e.g., "Ibrance" misread as "Ibrarice"). This ensures the drug and dose are correct.
Ephemeral session state only — per your original PRD's HIPAA-conscious constraint, extracted structured fields live in session memory for the demo run only, nothing persisted to a database. Worth stating explicitly on a slide.

## Question 4: 

How does the Bureaucracy Copilot's "conversational triage" interact with the new document upload — does the agent ask the patient questions only for fields it couldn't extract from the uploaded documents, or does it always ask the full standard question set regardless of what was uploaded?

This matters because your Phase 3 business logic (from the architecture doc) currently describes a fixed question flow ("The HealthWell fund requires income under 500% FPL — is your household income under $150,000?") — but now that documents can supply some of these answers, judges will notice if the agent asks a question it should already know the answer to from the EOB it just parsed.
My recommendation: gap-filling only — the orchestrator maintains a single patient-state object; each field the document-extraction step successfully populates is marked "confirmed from document" and skipped in conversational triage; only genuinely missing fields (usually household income, since none of your 3 documents contain it) get asked conversationally. This is also a great demo beat: "notice the agent already knows the patient's diagnosis and drug from the EOB — it only asks what it couldn't find."

basically that gap-filling approach match what you want, or should the agent always confirm extracted fields conversationally (e.g., "I see from your EOB this is for breast cancer — is that correct?") for accuracy/trust reasons before proceeding

## Single structured review screen 

For "Confirm and Continue" here's what I propose for the UI (your frontend/designer can mock this up in Figma and you can attach the image to the slide):

Section Header: "Please review the information we extracted from your documents"
Layout: 2-column grid that roughly preserves the visual hierarchy of the uploaded docs (left column: EOB, middle: Rx, right: Denial Letter). This immediately communicates "we understood the structure of what you uploaded."
For each document, show a mini-card with:
Document name (e.g., "Explanation of Benefits") with a small thumbnail preview of the PDF/image (just enough so the patient knows which page we're talking about).
Underneath the thumbnail, a collapsible "Parsed Fields" section that shows the key-value pairs extracted by the LLM (e.g., Billed Amount, Patient Responsibility, etc.). Use small inline edit icons (pencil icon) next to each field so the user *can* correct it if they want to.
Example: "Billed Amount: $11,200 ✏️" — clicking the pencil lets them type a correction. The backend should validate and re-run the extraction if they edit, updating the confidence score and the final patient-state object.
At the top right of the card, a small confidence badge (e.g., "Extraction Confidence: 89%") — green if >85%, yellow 70-85%, red <70%.
This gives the patient clear signals about where the agent is sure and where it's guessing, but still lets them correct anything they spot.
Why this is better than chat:
Trust/accuracy: Explicit correction capability builds more trust than "believe me, I got it right." Judges can see the patient *can* intervene, which satisfies the "trust and accuracy" requirement in a way that's much more tangible than just narrating the logic.
Time savings: One single "Confirm & Continue" click instead of 5-8 turns of back-and-forth ("Is this the right diagnosis?", "Is this the right drug?"). Especially for a timed demo, you want the flow to be fast and decisive.
Realistic: Real patient intake tools (like those used by patient navigators or in large health systems) almost always use a structured review screen for exactly this reason — it's way more efficient and less error-prone than a pure chat interface for this specific UX pattern.
Your visual prompt for the designer: "Show me a 2-column desktop-style intake review screen. Left column has a small thumbnail of the uploaded EOB PDF on top, then 'Parsed Fields' as an accordion/expandable section with key:value pairs like 'Billed Amount: $11,200' with pencil icons next to each. Same pattern for Rx and Denial Letter on the right. Top right corner of each doc card has a green/yellow/red confidence badge. Big blue 'Confirm & Continue' button at the bottom. When I click edit, show a small inline text input and update the value with a subtle slide transition."

## Live scrape with a cached fallback


Live scrape with a cached fallback — you scrape live during the demo (so it's genuinely real, verifiable data), but the code has a graceful fallback to the most recent successful scrape (cached with a visible timestamp, e.g., "Live data unavailable, showing last successful scrape from 2 hours ago") if the live call fails or times out. This preserves the "real data" claim honestly while eliminating catastrophic demo failure.

##  Next dependency: your Grant Navigator currently scrapes for OPEN/CLOSED status, but real eligibility for these foundations depends on several other things buried in unstructured page text — insurance type (many foundations explicitly exclude Medicare patients due to anti-kickback statute restrictions, some exclude uninsured/self-pay), income threshold (% of Federal Poverty Level), and sometimes diagnosis sub-type specificity (e.g., "metastatic breast cancer" fund vs. general "breast cancer" fund — not interchangeable).

## Question 7: Does the Grant Navigator only report OPEN/CLOSED status (leaving the patient to click through and verify eligibility themselves), or does it also extract and pre-filter by eligibility criteria (insurance type, income %FPL, diagnosis specificity) before presenting results — and if the latter, how confident are you this extraction will be reliable enough to state as fact rather than "possibly eligible"?
This matters because eligibility criteria live in unstructured prose scattered across different sections of each foundation's site (not a clean table like OPEN/CLOSED status), so the extraction is meaningfully harder and higher-stakes if wrong — telling a patient "you're eligible" when they're not wastes their time on a denied application, and telling them "you're not eligible" when they are means you cost them a grant they needed.
Options:

(A) Status-only: Report OPEN/CLOSED + a direct link, explicitly tell the patient "verify eligibility on the foundation's site" — safer, less impressive, honest about system limits.
(B) Full eligibility pre-filtering: Extract and match insurance type + income + diagnosis specificity automatically, present as "You appear eligible for X" — more impressive agentic behavior, but needs a confidence/hedging layer since a wrong "eligible" claim is the worst possible failure mode for this product.
(C) Hybrid: Report status + surface the raw eligibility text snippet the agent found (not a yes/no judgment), so the patient/case-manager sees the source and confirms fit themselves, with the agent only flagging obvious disqualifiers it's highly confident about (e.g., "this fund is Medicare-only, and your persona is on a commercial plan — likely not eligible").

My recommendation: (C). It's the most defensible for "AI for Good" judging (no false confidence on medical/financial eligibility), still demonstrates real agentic reasoning (the obvious-disqualifier flagging is genuinely useful and impressive), and is achievable in your remaining time since you're not building a robust eligibility-classification system from scratch.

