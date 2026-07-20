# Phase execution contract

Every workflow run must use the phase mapping in
[`config/phase_skills.yaml`](../config/phase_skills.yaml). The mapping prevents
a phase from silently running with the wrong agent or without its required
skill guidance.

| Phase | Responsibility | Executor | Required skill | Output |
|---:|---|---|---|---|
| 0 | Brain context | Codex | — | context |
| 1 | Research | Codex | `codex-analyst` | `research_notes.md` |
| 2 | Architecture plan | Codex | `codex-architect` | `master_plan.md` |
| 2.5 | Plan review | Claude | `advisor-architect` | `advisor_log.md` |
| 2.7 | Product UI design | Codex | `product-ui-designer` | `ui_design_spec.md`, `ui_acceptance.json`, `ui_prototype/` |
| 3 | Task breakdown | Antigravity | `triage` | `task.md`, `tasks.json` |
| 4 | Implementation | Codex | `codex-coder` | `outputs/` |
| 5 | Testing | Antigravity | `tdd` | `test_results.txt` |
| 5.5 | Visual QA | Codex | `visual-qa-auditor` | `visual_audit.md`, `visual_evidence/`, updated `ui_acceptance.json` |
| 6 | Security audit | Claude | `advisor-auditor` | `audit_report.md` |
| 7 | Final report | Antigravity | `technical-change-tracker` | `walkthrough.md` |
| 7.5 | Knowledge archive | Antigravity | — | `brain/vault/projects/` |

Rules:

1. The executor must load the listed skill before acting.
2. A phase is incomplete until its artifact exists and is reflected in
   `state.json`.
3. Phase 4 may not bypass `codex-coder`; Phase 5 may not bypass `tdd`.
4. Advisor phases are fail-closed: unavailable or timed-out review is not an
approval.
5. For user-facing projects, Phase 2.7 is mandatory before task breakdown. Every
frontend ticket must reference one or more `UI-ACC-*` acceptance IDs.
6. Phase 5.5 is fail-closed. UI tickets and the run cannot be marked `done`
without live browser screenshots at desktop, tablet, and mobile viewports and
`STATUS: APPROVED` in `visual_audit.md`.

Phase 4 uses the worker pool `codex-tu`, `codex-loc`, `codex-mao`,
`codex-thong`, and `codex-lien`. At most three workers run concurrently while
Codex retains the orchestrator slot. Task status and assignee changes go through
`scripts/task_manager.py`; the dashboard streams those fields from
`tasks.json`.

Phase 5 uses `gemi-chi`, `gemi-lucy`, and `gemi-na` as parallel testing workers.
Codex assigns non-overlapping test scopes, records each worker in `tasks.json`,
and consolidates their results into `test_results.txt` before Phase 6. A test
ticket becomes `done` only after its command output has been recorded.

Functional component tests do not constitute visual approval. Phase 5.5 must
inspect the rendered application in a browser, reconcile every critical/high
`UI-ACC-*` item, and return failed frontend tickets to Phase 4.


## Ownership
Codex is the project manager and owns the full lifecycle. Antigravity executes delegated worker tasks; Claude provides independent review only. Phase 0 is therefore initiated by Codex, which invokes the brain query and injects the result into Phase 1.
