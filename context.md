Current Context: Sprint 6 Completed (Metrics Rollout Closed)
Project: RAG Mongo Demo v7 - Metrics Evaluation Enablement

Active Task: Post-rollout monitoring and backlog transition.

Status:
- Sprint 1-3 completed
- Sprint 4 completed (backend bridge, contract normalization, fallback scoring, alias mapping)
- Sprint 5 completed (timeout/retry, observability, Ragas enablement, UI error diagnostics)
- Sprint 6 completed (regression validation, Ragas completion, sign-off)
- Ragas timeline: enablement in Sprint 5, completion in Sprint 6

Execution Mode: Automation-first (API and UI verification) with targeted manual smoke

## 1. Active Objective (Post Sprint 6)
Maintain rollout stability with observability-driven monitoring and prepare next-phase hardening backlog.

## 2. Constraints and Patterns
- UI integration pattern: Metrics tab should call backend API route, not evaluator service directly.
- Contract pattern: Normalize evaluator responses into stable UI scorecard payload shape.
- Configuration pattern: Keep evaluator URL environment-driven.
- Safety pattern: Evaluator failures must remain non-blocking for Prompt and Schema workflows.
- Regression guard: Existing retrieval, summarization, and prompt-generation flows must remain stable.
- Documentation gate: Charter, context, README, and strategy must maintain the same Sprint 4/5/6 framing.

## 3. Sprint 5 Completion Snapshot
- Timeout and retry policy implemented (exponential backoff + jitter).
- Route-level observability fields added (`latency_ms`, `error_class`, `request_id`, `retries`, `evaluator`, `fallback_used`).
- Ragas evaluation path enabled via backend contract and evaluator selection config.
- UI consumes backend observability metadata and failure diagnostics without blocking the workflow.
- Fault-injection scenarios executed for outage and deterministic failure mapping.
- Feature gating completed via environment configuration (`PRIMARY_EVALUATOR`, `RAGAS_URL`, `DEEPEVAL_URL`).

## 4. Sprint 5 Exit Criteria (✅ MET)
- Timeout and retry behavior is implemented, tested, and verified via fault-injection scenarios.
- Observability data is emitted for all evaluation calls (latency, error classification, request correlation).
- Ragas evaluation path is enabled through backend contract with confirmed response mapping.
- UI handles all failure states gracefully without crashes or hangs.
- Ragas feature gating (config/environment flags) is in place for Sprint 6 cross-environment validation.

## 5. Sprint 5 Entry Criteria (✅ MET)
- Sprint 4 exit criteria completed.
- Baseline integration path stable (all five metrics operational through UI).
- Initial failure mapping available (deterministic fallback scoring, error classification).
- Ragas enablement tasks and acceptance checks are finalized for Sprint 5 execution.

## 6. Next Actions (Post-Rollout)
1. Monitor production/staging telemetry for evaluator fallback frequency.
2. Prioritize backend modularization and lint cleanup as technical debt tasks.
3. Keep Ragas/DeepEval contract parity under change-control for future metric additions.

## 7. Sprint 6 Final Evidence Snapshot (2026-04-02)
- API smoke checks passed for `/api/health`, `/api/search/preprocess`, `/api/search/analyze`, `/api/search/deduplicate`, `/api/evaluate`, and `/api/search/summarize`.
- Direct Ragas evaluator check passed on `/eval-ragas` with normalized result payload.
- Backend-primary Ragas mode check passed on `/api/evaluate` (`details.evaluator = ragas`, `fallback_used = false`).
- Score explanation diagnostics and per-metric input arguments are present in evaluation responses.
- Evidence reference: `doc/sprint6-regression-evidence.md`
- Release recommendation: `doc/sprint6-release-readiness.md` (Decision: GO)
