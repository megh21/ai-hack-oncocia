Here is the detailed UX foundation for **Project OncoAccess**. Building these artifacts ensures that when we eventually design the screens, every pixel serves a specific, empathetic purpose for our users, while keeping the hackathon scope razor-sharp.

---

## 1. Problem Statements

Before solving a problem, we must define it clearly. For OncoAccess, the problems are both financial and systemic:

* **The Primary Problem (Financial Toxicity):** Cancer patients prescribed specialty oral oncolytics frequently abandon their life-saving therapies due to out-of-pocket costs ranging from $2,000 to $15,000 per month.
* **The Secondary Problem (Information Fragmentation):** To find financial relief, patients must navigate a fragmented ecosystem of non-profit foundations. Checking if a specific grant is "open" or "depleted" requires manually refreshing dozens of disjointed websites, which is exhausting for someone undergoing chemotherapy.
* **The Tertiary Problem (Bureaucratic Burden):** Understanding generic alternatives, deciphering baseline costs, and writing medical appeal letters require health literacy and energy that compromised patients often do not have.

---

## 2. User Personas

We will focus on two distinct personas to ensure the application is accessible for the compromised patient, but efficient enough for a proactive caregiver.

### Persona 1: Elena, The Overwhelmed Patient (Primary)

* **Profile:** 58 years old, recently diagnosed with advanced breast cancer. Taking multiple medications; dealing with severe fatigue and "chemo brain" (cognitive fog).
* **Tech Literacy:** Moderate. Uses an iPad and smartphone, but struggles with small text and complex navigation.
* **Motivations:** Wants to survive her diagnosis without bankrupting her family. Needs a clear, simple path forward.
* **Frustrations:** Medical jargon, hidden fees, websites requiring her to create accounts just to view information, and forms that ask for too much personal data.
* **UX Mandate:** Zero friction. No login walls, maximum legibility (20px+ font), and deeply empathetic language.

### Persona 2: Marcus, The Exhausted Caregiver (Secondary)

* **Profile:** 42 years old, working full-time while caring for his wife who has leukemia. Manages all household finances and medical logistics.
* **Tech Literacy:** High. Can navigate complex systems but is severely time-poor and stressed.
* **Motivations:** Needs actionable, accurate data *right now*. Wants to automate the heavy lifting of appeals and grant hunting.
* **Frustrations:** Broken links, outdated information (e.g., grants that say "Open" but are actually closed), and repeating the same information across different forms.
* **UX Mandate:** Accuracy and speed. Clear indicators of data freshness (e.g., "Grant status verified 2 mins ago") and quick access to exportable documents (like the Letter of Medical Necessity).

---

## 3. Empathy Map (Focus: Elena)

To truly design with empathy, we must map Elena’s internal and external experience when she first gets a $3,500 pharmacy bill.

| Quadrant | Details |
| --- | --- |
| **Says** | "I can't afford this."<br>

<br>"Is there a cheaper version?"<br>

<br>"I don't want to be a burden to my kids." |
| **Thinks** | "Maybe I can skip every other dose to make the bottle last longer."<br>

<br>"If I do this treatment, we might lose the house." |
| **Does** | Leaves the prescription at the pharmacy counter.<br>

<br>Spends hours searching Google for coupons.<br>

<br>Gives up after seeing "Funds Depleted" on the first two charity sites. |
| **Feels** | **Paralyzed** by the cost.<br>

<br>**Ashamed** that she can't afford it.<br>

<br>**Exhausted** by the bureaucratic maze.<br>

<br>**Vulnerable** when sites ask for her SSN or income. |

---

## 4. User Journey Map (The OncoAccess "Happy Path")

This maps the exact emotional and interactive journey we want to present to the judges during the hackathon demo.

1. **Trigger / Discovery:**
* *Action:* Elena gets a massive bill at the pharmacy. A social worker gives her the OncoAccess link.
* *Emotion:* High anxiety, desperation.
* *UX Goal:* The landing page must instantly lower her heart rate. Soft colors, clear value proposition: "Find financial assistance for your cancer medication in 2 minutes."


2. **Intake (The 3-Step Ask):**
* *Action:* Elena enters her Drug Name, Dosage, and Diagnosis.
* *Emotion:* Hesitant but hopeful.
* *UX Goal:* Keep it dead simple. No sign-ups. Reassure her: "We do not store your personal information."


3. **Processing / Waiting:**
* *Action:* The AI Orchestrator checks FDA, NADAC, and scrapes live grant sites.
* *Emotion:* Anticipation, worry that it will fail.
* *UX Goal:* Transparent loading states. Instead of a spinning wheel, show real-time progress: "Analyzing generic alternatives..." -> "Scanning 15 non-profits for open grants..."


4. **The Synthesis Dashboard:**
* *Action:* Elena views her results: Baseline costs, generic availability, and exactly 3 non-profits with *currently open* funds for breast cancer.
* *Emotion:* Relief, empowerment.
* *UX Goal:* High scannability. Use clear visual tags (e.g., a green "Fund Open Today" badge). Separate data logically.


5. **Action / Copilot:**
* *Action:* Elena clicks "Generate Appeal Letter" to take to her doctor.
* *Emotion:* Motivated, supported.
* *UX Goal:* A one-click export that formats the complex medical data into a professional, ready-to-print document.



---

## 5. Key Use Cases

These are the functional scenarios the design must accommodate:

* **Use Case 1: Finding Baseline Cost & Alternatives.** User enters a brand-name drug (e.g., *Gleevec*); the system returns the average wholesale price and flags if an FDA-approved generic (e.g., *Imatinib*) exists.
* **Use Case 2: Discovering Live Grants.** User inputs their diagnosis; the system displays a filtered list of grants, explicitly highlighting which ones are actively accepting applications *today*.
* **Use Case 3: Generating Medical Appeals.** User utilizes the AI copilot to draft a "Letter of Medical Necessity" based on the FDA data and their specific diagnosis, removing the blank-page syndrome for the patient.
* **Use Case 4 (Edge Case / Hackathon Safety):** The live grant scraper times out or fails. The system gracefully degrades by showing a cached list of foundations with a message: "Live status currently unavailable, but here are the direct links to apply."

---

## 6. UX & UI Requirements

To translate these findings into design rules, we must enforce the following requirements:

### Non-Functional (Design & Empathy) Constraints

* **Typography:** Absolute minimum font size of `20px` across the entire application for readability.
* **Color Theory:** Strictly use soft, calming palettes (e.g., pale blues, soft sage greens, warm off-whites). No stark blacks, alarming reds, or aggressive neon colors.
* **Tone of Voice:** Grade 6-8 reading level. Eradicate medical jargon or define it immediately inline. Use encouraging, supportive microcopy.
* **Accessibility:** High contrast ratios (WCAG AA compliant) even within the soft color palette. Generous touch targets for buttons.

### Functional Constraints

* **Frictionless Entry:** Zero authentication or account creation required for the core flow.
* **Progressive Disclosure:** Do not overwhelm the user with all data at once. Show the high-level summary first, with clear options to expand for more details.
* **Permanent Guardrails:** A persistent, non-intrusive disclaimer must be visible stating that OncoAccess provides estimates and educational data, not exact insurance copays.
* **Error Handling:** The UI must never show a raw technical error or stack trace if a backend agent fails.

---