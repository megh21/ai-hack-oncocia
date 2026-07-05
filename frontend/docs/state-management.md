This is the perfect next step. Bridging the gap between UI/UX design and frontend architecture ensures the experience actually functions the way we designed it.

Since this is a hackathon, we need to optimize for **speed of development** and **smooth transitions**. We want to avoid full page reloads because they break the "magic" of the AI feeling fast and responsive.

Here is the conceptual component hierarchy and state management strategy—keeping things strictly architectural without writing the actual React code.

---

## 1. State Management Strategy (The "Hackathon Fast-Track")

For a high-stakes, linear flow, avoid heavy libraries like Redux. They add unnecessary boilerplate. Instead, we have two excellent options:

* **Option A: Top-Level React State (Recommended for Hackathons).** Wrap the entire flow in a single parent component (e.g., `HeroFlowController`). This parent holds the `patientData` and `apiResults` state, and simply conditionally renders Screen 1, 2, or 3 based on a `currentStep` variable. It creates a seamless, app-like feel.
* **Option B: React Context.** If you want to break the screens into completely separate route pages (e.g., `/intake` and `/dashboard`), use a React Context Provider to pass the patient's drug and diagnosis data between routes without prop-drilling.

*UX Note on URLs:* Avoid putting the patient's diagnosis and drug in the URL search parameters (e.g., `?drug=Ibrance`). Even though we aren't saving it to a database, patients are sensitive about their medical data being visible in web history.

---

## 2. The Component Hierarchy Tree

Here is how we should break down the UI into modular Next.js components.

**`🗂️ App / Layout`** (Provides the global background, accessibility wrappers, and fonts)

* **`🧩 HeroFlowController`** (The brain. Holds the state: `step`, `intakeData`, `resultsData`)
* **`🖥️ Screen 1: IntakeView`** (Rendered if `step === 1`)
* `Header` (Logo and trust badge)
* `IntakeForm` (Inputs for Diagnosis, Drug, Dose)
* `DisclaimerFooter` (Global medical disclaimer)


* **`🖥️ Screen 2: ProcessingView`** (Rendered if `step === 2`)
* `PulsingAnimation` (Visual anchor)
* `StatusCycler` (Updates text: "Scanning...", "Analyzing...")


* **`🖥️ Screen 3: DashboardView`** (Rendered if `step === 3`)
* `DashboardHeader` (Breadcrumbs and summary)
* **`DrugIntelligenceColumn`**
* `CostCard` (Displays wholesale cost)
* `GenericAlertCard` (Conditional: Only renders if a generic exists)


* **`GrantNavigatorColumn`**
* `GrantCard` (Maps through the array of scraped grants)


* `ActionBar` (Sticky bottom CTA)


* **`🪟 CopilotModal`** (Rendered conditionally over the Dashboard if `isModalOpen === true`)
* `ContextForm` (Left side: Doctor name, Insurance)
* `LetterPreview` (Right side: Live document)





---

## 3. The Data Payload (What state are we tracking?)

To make the components talk to each other, we only need to track a few specific state objects in the `HeroFlowController`.

**1. The Intake State (Collected in Screen 1):**

* `diagnosis` (string)
* `drugName` (string)
* `dosage` (string)

**2. The Results State (Populated during Screen 2, consumed by Screen 3):**

* `baselineCost` (number/string)
* `genericAlternative` (object containing `name`, `exists` boolean, and `estimatedSavings`)
* `liveGrants` (array of objects containing `foundationName`, `status`, `coverageAmount`, `applyUrl`)

**3. The UI State:**

* `currentStep` (integer: 1, 2, or 3)
* `isModalOpen` (boolean)
* `isAgentFailed` (boolean - triggers the graceful degradation UX if the scraper times out)

---

## 4. UX Logic: The "Processing" Transition

The transition between Screen 1 and Screen 3 is the most critical UX moment. If the backend agents take 15–20 seconds to scrape live grants, staring at a static screen will cause the user to panic and hit refresh.

**The Logic Flow:**

1. User clicks "Find My Options" in `IntakeView`.
2. `HeroFlowController` updates `currentStep` to `2`. The UI instantly swaps to the `ProcessingView`.
3. Simultaneously, `HeroFlowController` fires the async API call to your multi-agent backend.
4. While waiting for the promise to resolve, the `ProcessingView` uses a simple `useEffect` timer to cycle through the status messages every 3.5 seconds (creating the illusion that the UI knows exactly what the AI is doing at every second).
5. Once the promise resolves and `resultsData` is populated, `currentStep` updates to `3`, fading in the `DashboardView`.