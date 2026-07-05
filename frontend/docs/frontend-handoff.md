Here is the **Frontend Engineering Handoff Blueprint** for Project OncoAccess. This document translates all our UX, UI, and architectural decisions into strict, actionable guidelines for development.

You can hand this directly to your frontend team (or use it as your own master reference) to start building the Next.js and Tailwind application immediately, plugging directly into your existing backend.

---

# 🛠️ Frontend Engineering Handoff: Project OncoAccess

## 1. Project Configuration & Constraints

**Tech Stack:** Next.js (App Router or Pages Router), React, Tailwind CSS, TypeScript (Highly Recommended).
**Target Audience:** Compromised oncology patients and stressed caregivers.

### The "Hard" UI Guardrails

* **Typography:** The absolute minimum font size is **20px**.
* *Dev Action:* Set your default body text to `text-xl`. Never use `text-sm`, `text-xs`, or `text-base`.


* **Color Palette:** Strictly soft, low-anxiety colors.
* *Backgrounds:* `bg-slate-50`, `bg-white`
* *Primary Actions:* `bg-emerald-500` (success/action), `bg-blue-600` (copilot/secondary action)
* *Text:* `text-slate-800` (headings), `text-slate-600` (body), `text-slate-500` (subtext/disclaimers)
* *BANNED:* Pure black (`text-black`), pure white on dark backgrounds (dark mode disabled), and harsh reds (`bg-red-500`).


* **Accessibility:** All form inputs must have visible labels. Buttons must have generous padding (e.g., `py-4 px-6`).

---

## 2. Expected Data Models (TypeScript Interfaces)

Since the backend is already running, the frontend needs to handle these exact data structures to map to the UI state.

```typescript
// 1. What the frontend sends to your existing backend
interface IntakePayload {
  diagnosis: string;
  drugName: string;
  dosage: string;
}

// 2. What the frontend expects back from the Orchestrator
interface OrchestratorResponse {
  drugIntelligence: {
    baselineCost: string; // e.g., "$13,000"
    generic: {
      exists: boolean;
      name: string | null;
      estimatedSavings: string | null;
    };
  };
  liveGrants: Array<{
    id: string;
    foundationName: string;
    status: 'OPEN' | 'WAITLISTED' | 'CLOSED';
    coverageDetails: string;
    applyUrl: string;
  }>;
}

```

---

## 3. Tailwind Configuration (`tailwind.config.js`)

To support the polished micro-interactions without writing custom CSS, add these animations to your Tailwind config file:

```javascript
module.exports = {
  theme: {
    extend: {
      keyframes: {
        'fade-in-up': {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        'soft-pulse': {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(0.98)' },
        }
      },
      animation: {
        'fade-in-up': 'fade-in-up 0.5s ease-out forwards',
        'soft-pulse': 'soft-pulse 3s ease-in-out infinite',
      }
    }
  }
}

```

---

## 4. Component Tree & State Architecture

Build the app inside a single view controller to prevent jarring page reloads.

**State to Initialize in `HeroFlowController.tsx`:**

```javascript
const [currentStep, setCurrentStep] = useState<1 | 2 | 3>(1);
const [intakeData, setIntakeData] = useState<IntakePayload | null>(null);
const [resultsData, setResultsData] = useState<OrchestratorResponse | null>(null);
const [isModalOpen, setIsModalOpen] = useState(false);

```

**File Structure Setup:**

* `/components/HeroFlowController.tsx` (Parent wrapper & logic)
* `/components/views/IntakeView.tsx` (Screen 1)
* `/components/views/ProcessingView.tsx` (Screen 2)
* `/components/views/DashboardView.tsx` (Screen 3)
* `/components/ui/GrantCard.tsx` (Reusable UI)
* `/components/ui/CopilotModal.tsx` (The Letter of Medical Necessity generator)

---

## 5. Interaction & API Logic (The "Handoff" Sequence)

When the user clicks "Find My Options" on `IntakeView`, execute this exact sequence to ensure UX smoothness:

1. **Button State:** Change button text to `"Initializing..."`, disable it (`disabled:opacity-70 active:scale-[0.98]`).
2. **Delay:** Wait `500ms` (allows the user to register the click).
3. **UI Switch:** Update `currentStep` to `2` (triggers the `ProcessingView` to fade in).
4. **Network Call:** Fire the API `POST` request to your backend.
5. **Agent Magic (While waiting):** Inside `ProcessingView`, use a `useEffect` with `setInterval` to cycle an array of strings every 3 seconds (e.g., *"Scanning FDA databases..."* -> *"Checking 15 non-profits..."*).
6. **Resolution:** When the API returns the `OrchestratorResponse`, save it to `resultsData` and set `currentStep` to `3`.
7. **Staggered Render:** In `DashboardView`, use Tailwind delay classes to load elements sequentially:
* Header: `animate-fade-in-up`
* Cost Card: `animate-fade-in-up delay-[150ms]`
* Grant Cards: `animate-fade-in-up delay-[300ms]`



---

## 6. Error Handling (Graceful Degradation)

Hackathon live demos fail. Your frontend must protect the demo:

* **Timeout Check:** If the API takes longer than 25 seconds, automatically resolve to a mocked "Cached Response" (using realistic fallback data like *HealthWell Foundation*).
* **UI Flag:** Render a small, dismissible banner at the top of the dashboard: *"Live connection timed out. Showing last verified data."* Do not show an error boundary, stack trace, or red text.

---

You are fully cleared for development. This blueprint contains everything your engineering environment needs to map the UI components to your backend while maintaining the strict empathetic design rules we established. Good luck with the build!