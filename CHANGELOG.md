# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
