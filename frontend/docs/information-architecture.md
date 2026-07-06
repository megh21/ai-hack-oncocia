Excellent. Now that we know *who* we are designing for and *why*, we can build the Information Architecture (IA). For a hackathon, we need a streamlined, linear flow that tells a compelling story from start to finish without getting bogged down in edge-case screens like settings or user profiles.

Here is the Information Architecture and structural layout for the **Oncocia Hackathon Hero Flow**.

---

## The Information Architecture (IA)

We will use a linear, progressive disclosure model. The user moves forward one step at a time, preventing cognitive overload.

**Path:** `Landing & Intake` ➔ `Active Processing` ➔ `Synthesis Dashboard` ➔ `Copilot/Action`

---

## Screen-by-Screen Layout Structure

### Screen 1: The "Calm" Landing & Intake

**Goal:** Lower anxiety, establish trust instantly, and collect the required three data points with zero friction.
**Layout:** Single, centered column to focus the user's attention. Lots of breathing room (whitespace).

* **Header:**
* Soft, minimal logo.
* Trust badge: "100% Free & Private. No account required."


* **Hero Section:**
* Headline (Empathetic & Clear): *“Find financial support and alternatives for your cancer medication.”*
* Sub-headline: *“Tell us what you were prescribed, and we’ll check live grants and generic options in seconds.”*


* **The Intake Form (The 3 Asks):**
* Input 1: **Diagnosis** (e.g., Breast Cancer) – *Suggest using a smart predictive dropdown to prevent typos.*
* Input 2: **Drug Name** (e.g., Ibrance)
* Input 3: **Dosage** (e.g., 125mg)


* **Primary CTA Button:**
* Large, soft-colored button: "Find My Options"


* **Footer:**
* The permanent medical disclaimer: *"Oncocia provides estimates and educational data. This is not medical advice or an exact insurance quote."*



### Screen 2: Active Processing (The "Agent Magic" Screen)

**Goal:** Show the judges the multi-agent backend working in real-time, while reassuring the patient that their request is being handled carefully.
**Layout:** Centered loading state, but dynamic and conversational (not just a spinning wheel).

* **Main Visual:** A soft, pulsing animation (e.g., a calming breathing circle).
* **Dynamic Status Text (The Hackathon "Wow" Factor):**
* Cycles through what the Orchestrator is doing:
* *“Identifying generic alternatives via FDA databases...”*
* *“Calculating baseline costs...”*
* *“Scanning 15 non-profit foundations for live, open grants...”*
* *“Compiling your customized dashboard...”*




* **Microcopy:** *"This usually takes about 15 seconds. Hang tight."*

### Screen 3: The Synthesis Dashboard

**Goal:** Present complex, multi-source data in a scannable, non-intimidating way.
**Layout:** Two-column grid on desktop (Cost/Drug on the left, Grants on the right). Stacked vertically on mobile.

* **Top Banner:**
* Summary: *"Here are the options for **Ibrance (125mg)** to treat **Breast Cancer**."*
* Actionable breadcrumb: "Start Over"


* **Column A: Drug Intelligence (Left Side)**
* **Cost Estimate Card:** Shows the baseline wholesale cost. (e.g., *"Baseline Wholesale Cost: ~$13,000/mo"*).
* **Generic Alert Card (Crucial for UX):**
* *If yes:* Bright, encouraging badge: "Generic Available!" Details the generic name (e.g., *Palbociclib*) and the estimated savings.
* *If no:* Softly worded: "No FDA-approved generic currently available."




* **Column B: Live Grant Navigator (Right Side)**
* **Header:** *"Active Financial Assistance Programs"*
* **Grant Cards (Max 3-5 to prevent overwhelm):**
* Foundation Name (e.g., *HealthWell Foundation*).
* Status Badge: Vibrant green dot with **"FUND OPEN"** (Driven by the Playwright scraper).
* Coverage details (e.g., *"Up to $10,000/year for Medicare patients"*).
* CTA Button: "Apply on their website" (External link).




* **Floating Action Bar (Bottom):**
* A distinct, persistent banner prompting the next step: *"Need to appeal to your insurance or apply for an exception?"* ➔ CTA: **"Draft a Letter of Medical Necessity"**



### Screen 4: Copilot Action Modal

**Goal:** Provide a tangible takeaway. Solve the "blank page" syndrome for a tired patient or caregiver.
**Layout:** Split-screen layout. Left side for minimal inputs; right side for the live document preview.

* **Left Column (Input):**
* Brief conversational form asking for missing context: *"Who is your prescribing doctor?"* and *"What is your insurance provider?"*


* **Right Column (Output Preview):**
* A live, formatted preview of the Letter of Medical Necessity.
* The letter automatically weaves in the FDA data, the lack of generic alternatives (if applicable), and the specific diagnosis.


* **Action Buttons:**
* "Download PDF"
* "Copy Text"



---

## UI Component Library Strategy

To build this quickly in Next.js and Tailwind, we should define a strict, minimal component set. Remember our **20px minimum font rule**:

1. **Typography:**
* Headings: 32px - 48px, bold but rounded (e.g., a friendly sans-serif like *Nunito* or *Inter*).
* Body/Labels: 20px - 24px, medium weight.


2. **Color System (Tailwind mapping):**
* **Backgrounds:** `bg-slate-50` or `bg-blue-50` (soft, clinical but warm).
* **Cards:** `bg-white` with a very soft shadow (`shadow-sm` or `shadow-md`).
* **Primary Actions:** Soft sage green (`bg-emerald-500`) or calming blue (`bg-blue-500`).
* **Status Badges:** Soft green for open (`bg-green-100 text-green-800`), soft gray for closed/waitlisted.


3. **Spacing:** Generous padding. `p-6` or `p-8` inside cards to ensure the text isn't cramped.

---