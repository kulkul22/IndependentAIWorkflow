# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v4.1.0] - 2026-07-20

### Added
- External workspace tracking and junction-based execution support for hybrid workflow runs.
- Headless Antigravity/Gemini CLI wrapper using the active Google-authenticated session.
- Explicit phase-to-agent skill matrix with named Phase 4 and Phase 5 worker pools.
- Product UI design and fail-closed visual QA phases with evidence-backed acceptance criteria.
- Dashboard support for fractional workflow phases and normalized task statuses.
- Regression tests for advisor failures, dashboard state, status normalization, and visual task gates.

### Changed
- Codex now owns project management and orchestration while Antigravity executes delegated phases and Claude provides independent review.
- Advisor calls use bounded mode-specific timeouts, stdin prompt delivery, and fail-closed error handling.
- Second Brain synchronization now uses file locking and cleans stale vectors safely.
- Final reporting and runtime documentation were aligned with the orchestrated workflow.

### Fixed
- Prevented IDE crashes caused by concurrent Chroma access and unsafe database tracking patterns.
- Prevented UI tasks from being marked done before visual acceptance evidence is approved.

## [v4.0.0] - 2026-07-13

### Added
- **Hybrid AI Workflow Skill**: Introduced 4 budget-based execution modes (Local Only, Safe Audit, Dynamic Helper, Max Quality).
- **Dynamic Advisor Escalation**: In Modes 3 and 4, the Worker AI will automatically compress context and call Claude CLI (`call_advisor.py --mode debug`) if testing fails more than 2 times (maximum 3 calls per task).
- **Advisor Log**: All requests and responses from the Advisor are now logged into `advisor_log.md` inside each run directory.
- **Context Compression Logic**: `call_advisor.py` now selectively reads only 100 lines of code around the error line and redacts secrets before sending data to Claude, minimizing token usage.

### Changed
- Replaced the textual execution phases architecture in `README.md` with a highly detailed SVG architecture diagram (`hybrid_workflow.svg`).
- Cleaned up the `call_advisor.py` script to exclusively use the `claude` CLI backend.

### Removed
- Removed unused and uncompressed standalone context modes that consumed excessive tokens.
