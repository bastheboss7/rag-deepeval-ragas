# Enterprise Vibe Code Development Strategy

**Version:** 1.4.3  
**Status:** Baseline Standard  
**Target:** Lead QA & Engineering Teams  

---

## 📝 Abstract: High-Impact Strategy Highlights
This strategy defines a **Dual-AI Verification Model** designed to eliminate the risks of AI-assisted development. By using Gemini as a Lead Architect Auditor and GitHub Copilot as an Execution Engine, we achieve a **62.5% efficiency gain** while maintaining strict **TMMi Level 5** standards.

### Key Innovations:
* **Dual-AI Governance:** Every task is "primed" in Gemini with 13+ years of QA Governance before being executed in Copilot.
* **Framework Governance:** LangChain is mandatory for prompt orchestration and provider abstraction across QA Bot runtime flows.
* **Prompt Customization Loop:** No AI-generated prompt is used blindly; a mandatory manual review is performed to align prompts with the Design Document.
* **Business-Language Verification:** Technical Unit Tests are automatically translated into business-value reports for non-technical stakeholders.
* **Deterministic Resilience:** A focus on Graceful Degradation, ensuring the system remains functional even during AI provider outages.

---

## 🏗️ 1. The "Governance-First" Workflow
We follow a strict **Document-Before-Code** sequence. The LLM must read the "Architect's Manual" before starting any task.

1.  **Step 1: [Development Strategy](VIBE_CODE_DEVELOPMENT_STRATEGY.md)** The Governance "How." Defines the execution model, quality gates, and AI collaboration rules.
2.  **Step 2: [Design Document](UI_Design_Document.md)** The UI & Feature Plan. Finalizes UI layout, buttons, and dropdowns.
3.  **Step 3: [architecture.md](../architecture.md)** The System "Map." Defines module boundaries, request/data flow, and integration contracts across frontend, API routes, loaders, chain, model, and validation components.
4.  **Step 4: [PROJECT_CHARTER.md](../PROJECT_CHARTER.md)** The Business Contract. Defines Sprint Goals and SLA Success Metrics.
5.  **Step 5: [context.md](../context.md)** The Daily Focus File. Provides the AI with the immediate "To-Do" list to prevent context-bloat.

---

## 🧠 2. The Tri-Agent "Ingestion" Strategy
We do not use AI blindly. We use Gemini to "prime" the environment.

* **Strategic Ingestion:** Upload your QA Governance and this [Development Strategy](VIBE_CODE_DEVELOPMENT_STRATEGY.md) into Gemini.
* **Prompt Creation:** Gemini generates a context-aware prompt for the specific task.
* **The Human Gate:** Review the Gemini prompt and verify it matches the [Design Doc](UI_Design_Document.md) (buttons, dropdowns, etc.).
* **Copilot Execution:** The customized prompt is pasted into the Copilot Workspace for coding.

---

## 🛡️ 3. Sprint Completion Workflow (Testing Gates)
Every Sprint must pass through the Test Pyramid before sign-off:

| Testing Level | Type | Focus |
| :--- | :--- | :--- |
| **Unit Tests** | White Box | Internal logic. Reports use Business English (e.g., *Ensure search stability during LLM outages*). |
| **Integration Tests** | IT | Checks API contracts and Hybrid Search logic. |
| **Metrics Evaluation** | Black Box | Validates evaluation contract, scorecard payload stability, and evaluator failure handling. |
| **Manual Smoke** | Risk-Based | Final human check of UI features based on the [Design Document](UI_Design_Document.md); optional in early sprints when UI readiness is limited. |
| **Documentation Gate** | Static Validation | Run markdown link checks and fix broken links before Sprint sign-off. |

**Sprint Policy Note:** Unit and Integration tests are mandatory in all sprints. Manual Smoke remains part of the general strategy and is required once UI flows are sprint-ready.

**Technology Policy Note:** LangChain is mandatory for chain orchestration in all sprints; direct provider-specific orchestration outside approved model adapters is not allowed.

---

## 📝 4. Quick Reference: Sprints 1–3

### A. [PROJECT_CHARTER.md](../PROJECT_CHARTER.md) (The Intelligence Goal)
* **Goal:** Establish a production-ready baseline for ingestion, validation, and observability.
* **Resilience:** Ensure deterministic upload cleanup and request traceability.
* **DoD (Definition of Done):**
    * [x] Unit tests for `loaders.ts` cover `.pdf`, `.docx`, `.csv`, and `.txt`.
    * [x] Business-language test reporting includes `[EXPECTED_ACTUAL][BUSINESS]` tags.
    * [x] `FileUploadSchema` validates multipart inputs before processing.

### B. [context.md](../context.md) (The Current Task)
* **Current Focus:** Sprint 1 — Building core server and file ingestion pipeline.
* **Active Constraint:** Keep document conversion logic out of `server.ts` and enforce strict layering.
* **Next Task:** Define `src/types.ts` Zod schemas before implementing ingestion business logic.

### C. Sprint 2 (Retrieval Hardening & UI Readiness)
* **Goal:** Strengthen retrieval quality and complete UI readiness for stable human verification.
* **Testing Policy:** Unit + Integration mandatory; Manual Smoke executed for sprint-ready UI flows.
* **DoD Highlights:**
    * [ ] Retrieval quality benchmark scenarios pass.
    * [ ] UI loading/error states are verified by automated integration/UI tests.
    * [ ] Manual smoke evidence is captured for stable workflows.

### D. Sprint 3 (Hybrid Retrieval & Resilience)
* **Goal:** Deliver hybrid retrieval improvements with robust graceful-degradation behavior.
* **Testing Policy:** Full Test Pyramid required, including Manual Smoke for resilience UX.
* **DoD Highlights:**
    * [ ] Hybrid retrieval and fallback paths pass integration tests.
    * [ ] Resilience behavior is observable in logs/metadata and business reports.
    * [ ] Governance gates (LangChain mandate, documentation, security, coverage) remain compliant.

### E. Sprint 4 (Metrics API and Contract Foundation)
* **Goal:** Establish backend evaluation bridge and stable response contract for Metrics Evaluation workflows.
* **Testing Policy:** Unit + Integration mandatory for happy path and baseline evaluator-down behavior.
* **DoD Highlights:**
    * [ ] `/api/evaluate` route is implemented and reachable from Metrics UI.
    * [ ] Normalized scorecard payload contract is stable for UI rendering.
    * [ ] Baseline success and evaluator-down evidence is captured.

### F. Sprint 5 (Metrics Reliability Hardening)
* **Goal:** Harden evaluation reliability with deterministic timeout, retry, and outage behavior.
* **Testing Policy:** Integration + Metrics Evaluation black-box checks mandatory; targeted manual smoke for failure UX.
* **DoD Highlights:**
    * [ ] Timeout and retry policies are implemented and verified.
    * [ ] Failure responses remain deterministic and user-safe.
    * [ ] Evaluation call observability and timing data are available.

### G. Sprint 6 (Regression Safety and Sign-off)
* **Goal:** Complete regression-safe rollout and final sign-off package for Metrics Evaluation.
* **Testing Policy:** Full gate execution: unit, integration, metrics black-box, and manual smoke.
* **DoD Highlights:**
    * [ ] Existing retrieval and generation workflows remain regression-safe.
    * [ ] Metrics baseline report and final evidence package are complete.
    * [ ] Release recommendation and residual risk log are documented.

---

## 📊 5. Summary of Team Execution
1.  **Input:** Ingest QA Strategy into Gemini.
2.  **Process:** Gemini generates the Task Prompt.
3.  **Quality Gate:** Customize the prompt for the [Design Doc](UI_Design_Document.md) and run markdown link validation.
4.  **Output:** Copilot writes Code + White Box tests in Business Language.
5.  **Final Sign-off:** Integration verifies sprint scope; Manual Smoke is included when UI flows are ready.