# Project Charter: RAG Mongo Demo v7 (Sprints 1-6)

Project: RAG Mongo Demo v7 - Test Case and User Story Intelligence
Focus: Retrieval quality, operational reliability, and Metrics Evaluation rollout
Status: Sprint 1-6 completed
Execution Mode: Automation-first verification with targeted manual smoke

---

## 1. Program Objective
Deliver and operationalize a production-ready RAG platform for QA assets that supports:
- Excel/Jira ingestion to structured JSON
- Batch embeddings and MongoDB Atlas indexing
- Vector, BM25, Hybrid, and reranked search
- Prompt-schema driven generation workflows
- Metrics Evaluation for generated and reference test cases

## 1.1 Scope Boundaries
- In Scope (Sprints 4-6): Complete Metrics Evaluation rollout through backend API integration, reliability hardening, and sign-off quality gates, including Ragas enablement in Sprint 5 and Ragas completion in Sprint 6.
- Out of Scope (Sprints 4-6): Full backend modularization, provider replacement, and broad UI redesign unrelated to metrics outcomes.

---

## 2. Success Metrics and SLAs

### 2.1 Baseline Continuity (must remain green)
- Retrieval Availability: Vector, BM25, Hybrid, and rerank flows remain operational.
- Data Pipeline Reliability: Conversion and embedding job orchestration remains stable with deterministic status tracking.
- Search Quality Stability: Existing hybrid/rerank relevance behavior does not regress from Sprint 3 baseline.

### 2.2 Metrics Rollout Targets (Sprints 4-6)
- Evaluation API Availability: `/api/evaluate` availability >= 99 percent during development and staging windows.
- Evaluation Latency: P95 latency <= 5 seconds for single test case evaluation under normal conditions.
- Contract Stability: 100 percent of successful responses include normalized metric payload required by Metrics Evaluation UI.
- Failure Transparency: Evaluator-unavailable scenarios return deterministic user-safe error payloads and preserve UI usability.
- Ragas Enablement (Sprint 5): Ragas evaluation path is integrated behind backend contract with deterministic timeout and error handling.
- Ragas Completion (Sprint 6): Ragas evaluation flow passes regression verification and is included in final rollout sign-off.

---

## 3. Definition of Done (DoD)
A sprint item is complete only when all mandatory gates pass.

### 3.0 Metrics Rollout DoD Gates
- [ ] Evaluation API Gate: Backend evaluation route is implemented and reachable from UI flows.
- [ ] Contract Gate: Request and response schema is validated for query, context, output, expected_output, and metric result blocks.
- [ ] UX Reliability Gate: Metrics Evaluation tab handles loading, success, and service-error states deterministically.
- [ ] Regression Gate: Existing search, summarization, and prompt-testing routes remain stable.
- [ ] Observability Gate: Evaluation calls emit traceable logs with route timing and failure context.
- [ ] Documentation Gate: Charter, context, README, and strategy references remain aligned.

### 3.1 Acceptance Evidence
- API verification for happy path and evaluator-down path.
- UI verification for evaluate action and scorecard rendering behavior.
- Regression verification for existing key APIs.
- Final rollout evidence pack at Sprint 6 close.

---

## 4. Architecture and Implementation Constraints
- Current backend runtime is server/index.js; integration work must preserve existing endpoint behavior.
- Metrics Evaluation must route through Express backend endpoint rather than frontend-direct evaluator calls.
- Evaluator service URL must be environment-driven.
- MongoDB Atlas vector and BM25 index assumptions remain unchanged.
- Mistral remains embedding provider; Groq remains rerank and summarization provider unless re-chartered.
- Security-sensitive configuration handling must not be weakened during rollout.

---

## 5. Verification Protocol

### Scenario 1: Happy Path Evaluation
Action: Select a test case and execute Metrics Evaluation.
Expected: API returns normalized metrics payload and UI renders scorecards without refresh.

### Scenario 2: Evaluator Outage or Timeout
Action: Simulate evaluator downtime or timeout.
Expected: Backend returns deterministic error payload and UI remains non-blocking.

### Scenario 3: Regression Safety
Action: Run core retrieval and generation workflows after evaluation integration.
Expected: No behavioral regression in existing endpoints.

---

## 6. Governance Alignment (Document-Before-Code)
- Strategy: [doc/VIBE_CODE_DEVELOPMENT_STRATEGY.md](doc/VIBE_CODE_DEVELOPMENT_STRATEGY.md)
- Operational context: [context.md](context.md)
- Project runbook: [README.md](README.md)

---

## 7. Sprint History (Completed)

### Sprint 1: Data and Ingestion Foundation
Delivered Excel-to-JSON conversion flow, file handling, and ingestion baseline required for embedding and retrieval.

### Sprint 2: Retrieval Quality and Search Coverage
Delivered vector and BM25 search coverage, metadata filtering support, and retrieval quality hardening.

### Sprint 3: Hybrid Intelligence and Prompt Workflows
Delivered hybrid search, reranking, summarization, and prompt-schema workflows, including the Metrics Evaluation UI shell and scorecard model.

---

## 8. Sprint 4 Charter: Metrics API and Contract Foundation

### 8.1 Sprint Objective
Establish backend evaluation bridge and stable contract for Metrics Evaluation integration.

### 8.2 Scope Boundaries
- In Scope:
  - Implement backend evaluation endpoint and bridge to DeepEval service.
  - Normalize evaluator response payload to UI contract.
  - Route Metrics Evaluation UI calls through backend contract.
- Out of Scope:
  - Reliability hardening beyond basic happy-path and standard failure mapping.
  - Full regression sign-off package.

### 8.3 Success Metrics and SLAs
- Endpoint Reachability: `/api/evaluate` is callable from UI and API tests.
- Contract Conformance: Successful responses match expected payload shape for scorecard rendering.
- Basic Failure Mapping: Evaluator-down response path returns controlled error payload.

### 8.4 Sprint 4 DoD Tracker (✅ COMPLETED)
- [x] `/api/evaluate` route implemented.
- [x] UI calls backend route for metrics flow.
- [x] Response contract normalized (object → array).
- [x] Deterministic fallback scoring enabled.
- [x] Metric alias mapping (faithfullness → faithfulness) across all layers.
- [x] Contract examples documented.
- [x] Happy-path verification completed.
- [x] Failure-path verification completed.
- [x] All five RAG metrics operational through UI.

### 8.5 Acceptance Evidence
- API evidence for timeout, outage, and retry outcomes.
- Logging evidence for timing and failure classification.
- Ragas enablement evidence for backend response mapping and functional execution path.
  - **Artifact-driven handoff:**
    - Ragas API contract and schema definition document (version-controlled)
    - Backend integration test pack for Ragas path (with sample requests/responses)
    - Evidence of Ragas feature flag or config gating (if applicable)
    - Signed handoff checklist reviewed by tech lead
### 8.6 Verification Protocol
- Run API tests for evaluation endpoint success and failure.
- Execute manual smoke for one representative test case evaluation.

---

## 9. Sprint 5 Charter: Reliability, Observability, and Ragas Enablement

### 9.1 Sprint Objective
Harden Metrics Evaluation behavior for evaluator outages, latency spikes, and user-safe UI operation, and enable the Ragas evaluation path.

### 9.2 Scope Boundaries
- In Scope:
  - Timeout and retry policy for evaluator integration.
  - Deterministic error mapping and UI-safe messaging.
  - Route-level observability and timing metadata for evaluation requests.
  - Ragas evaluation enablement through backend contract with stable response mapping.
- Out of Scope:
  - Final release recommendation and full sign-off package.

### 9.3 Success Metrics and SLAs
- Failure Determinism: Timeout and outage paths return stable, parseable response envelopes.
- UX Stability: Metrics tab does not crash or hang under evaluator failures.
- Observability Coverage: Evaluation failures and timings are traceable in logs.
- Ragas Enablement: Ragas path is executable via backend integration and produces mapped metric responses.

### 9.4 Sprint 5 DoD Tracker
- [x] Timeout and retry behavior implemented.
- [x] Deterministic evaluator failure responses verified.
- [x] Metrics UI handles failure states gracefully.
- [x] Observability data emitted for evaluation calls.
- [x] Ragas evaluation path enabled through backend contract.

### 9.5 Acceptance Evidence
- API evidence for timeout, outage, retry, and deterministic error envelopes (`error_class`, `retries`, `request_id`).
- UI evidence for non-blocking error handling with surfaced evaluator metadata and failure diagnostics.
- Logging and response evidence for timing/failure classification (`latency_ms`, `error_class`, `fallback_used`).
- Ragas enablement evidence for backend response mapping, evaluator selection (`PRIMARY_EVALUATOR`), and fallback chain execution.

### 9.6 Verification Protocol
- Run evaluator fault-injection scenarios.
- Validate UI behavior for repeated failure and recovery attempts.

---

## 10. Sprint 6 Charter: Ragas Completion, Regression Safety, and Sign-off

### 10.1 Sprint Objective
Complete Ragas implementation and rollout sign-off by proving regression safety, quality baseline stability, and documentation completeness.

### 10.2 Scope Boundaries
- In Scope:
  - Full regression coverage for search and generation flows after metrics integration.
  - Metrics-quality baseline validation and sign-off evidence.
  - Ragas completion validation across representative evaluation scenarios.
  - Final documentation and rollout readiness package.
- Out of Scope:
  - New feature expansion unrelated to Metrics Evaluation rollout.

### 10.3 Success Metrics and SLAs
- Regression Safety: No critical regressions in existing retrieval and prompt workflows.
- Quality Baseline: Metrics output and UI rendering remain stable across representative scenarios.
- Ragas Completion: Ragas evaluation is validated in regression runs and accepted in release-readiness review.
- Documentation Completeness: Charter, context, README, and strategy are aligned with final behavior.

### 10.4 Sprint 6 DoD Tracker
- [x] Regression verification completed across core APIs and UI flows.
- [x] Metrics baseline report created and reviewed.
- [x] Ragas evaluation completion validated and signed off.
- [x] Final evidence package completed.
- [x] Release recommendation documented with residual risks.

### 10.7 Sprint 6 Execution Log (Initial)
- 2026-04-02: Core API smoke checks executed for `health`, `preprocess`, `analyze`, `deduplicate`, and `evaluate`.
- 2026-04-02: Ragas evaluator path validated directly through `/eval-ragas` with normalized response contract.
- 2026-04-02: Summarization regression check executed successfully through `/api/search/summarize`.
- 2026-04-02: Backend-primary Ragas validation passed through `/api/evaluate` (`details.evaluator = ragas`).
- 2026-04-02: UI metrics validation confirmed (Ragas visible in metric output with score rendering).
- Evidence file: `doc/sprint6-regression-evidence.md`

### 10.8 Sprint 6 Release Recommendation
- Decision: **GO** for Metrics Evaluation rollout closure.
- Basis:
  - Regression matrix passed for core search, preprocessing, deduplication, summarization, and metrics routes.
  - Ragas completion criteria met across direct evaluator path and backend-primary mode.
  - Metrics UI displays evaluator source and per-metric diagnostics (`explanation`, `input_arguments`, `score_breakdown`).
  - Documentation set aligned across charter, context, README, and Sprint 6 evidence artifacts.
- Residual Risks (non-blocking):
  - Evaluator quality path may fall back to heuristic scoring when model credentials are unavailable.
  - Backend remains monolithic (`server/index.js`), increasing long-term maintenance risk.
  - Legacy lint warnings exist in unrelated frontend files.
- Mitigation Plan:
  - Keep evaluator observability fields (`error_class`, `retries`, `evaluator`, `fallback_used`) in release monitoring.
  - Track backend modularization and lint cleanup as post-rollout backlog items.

### 10.5 Acceptance Evidence
- Test run summary for unit, integration, and metrics black-box checks.
- Manual smoke summary for metrics flow and recovery behavior.
- Final documentation review sign-off.
  - **Artifact-driven Ragas completion:**
    - Ragas regression test matrix and results archive
    - Final Ragas API contract and schema validation evidence
    - Release sign-off checklist with Ragas-specific acceptance gates
    - Evidence pack (screenshots, logs, and sample payloads) for Ragas evaluation scenarios

### 10.6 Verification Protocol
- Execute full verification matrix.
- Review and approve release readiness checklist.

---


## 11. Sprint Dependency Map
- Sprint 4 outputs are prerequisites for Sprint 5.
- Sprint 5 hardening and Ragas enablement outputs are prerequisites for Sprint 6 sign-off.
- Sprint 6 closes the Metrics Evaluation rollout and Ragas completion for release recommendation.

---

## Ragas Sequencing Rationale

**Why is Ragas (Raaga) scheduled for Sprint 5 instead of Sprint 4?**

1. **Dependency Sequencing:** Sprint 4 is focused on enabling the UI and backend contract for RAG metrics evaluation. Ragas integration requires foundational work (API, data model, evaluation harness) that depends on the completion and stabilization of the generic metrics framework. Starting Ragas in Sprint 4 risks rework if the core evaluation contract changes.

2. **Incremental Integration:** Best practice is to first validate the generic metrics pipeline (e.g., DeepEval) in Sprint 4, ensuring stability, correctness, and performance. Only after this baseline is proven should a new evaluation framework (Ragas) be integrated, to avoid compounding bugs and to isolate root causes during testing.

3. **Enterprise Readiness & Verification:** Enterprise standards require that new frameworks like Ragas be gated behind measurable SLAs, security reviews, and artifact-driven handoff. These controls are only possible once the initial metrics evaluation path is production-ready, which is the goal of Sprint 4.

4. **Risk Mitigation:** Parallelizing Ragas with the core metrics work in Sprint 4 increases risk of instability, unclear ownership of bugs, and missed acceptance criteria. Sequencing Ragas in Sprint 5 allows for focused, verifiable delivery and easier rollback if issues arise.

**Summary:** Ragas is scheduled for Sprint 5 to ensure the core metrics evaluation path is stable, to follow best practices for incremental integration, and to meet enterprise verification and risk management standards. Starting Ragas in Sprint 4 would violate these principles and increase project risk.
