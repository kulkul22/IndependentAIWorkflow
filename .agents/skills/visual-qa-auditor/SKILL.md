---
name: visual-qa-auditor
description: Audit a live user interface with browser evidence and issue a fail-closed visual approval. Use after frontend implementation, before release, for UI redesign verification, responsive checks, design-spec comparison, accessibility presentation review, or whenever functional tests pass but product visual quality must be independently validated.
---

# Visual QA Auditor

Evaluate the running product, not only source code or component tests. Treat missing visual evidence as a failed audit.

## Inputs

Require the live URL, `ui_design_spec.md`, `ui_acceptance.json`, and relevant test results. If a legacy project lacks a design spec, document that gap and audit against the product requirements plus standard usability principles.

## Audit workflow

1. Start or connect to the real application and verify API health.
2. Use `browser:control-in-app-browser` when available to inspect actual rendered state and interactions.
3. Exercise primary user journeys with realistic data, including empty, loading, error, success, and destructive flows.
4. Capture evidence at minimum viewports:
   - desktop: 1440 × 900;
   - tablet: 768 × 1024;
   - mobile: 390 × 844.
5. Compare each `UI-ACC-*` item with the implementation and attach an evidence path.
6. Inspect hierarchy, typography, spacing rhythm, alignment, contrast, focus visibility, control consistency, overflow, density, feedback, and responsive reflow.
7. Inspect source only to explain observed defects; never substitute source inspection for browser evidence.

Use [references/visual-audit-rubric.md](references/visual-audit-rubric.md) for severity and approval rules.

## Required artifacts

- `visual_evidence/` containing timestamped screenshots for all required viewports and critical states.
- `visual_audit.md` containing the tested URL, viewports, acceptance matrix, findings, and remediation.
- Updated `ui_acceptance.json` with `pass` or `fail` and evidence paths.

## Decision

Conclude `visual_audit.md` with exactly one line:

- `STATUS: APPROVED` only when all critical and high acceptance items pass and required evidence exists.
- `STATUS: REJECTED` when any blocker remains, evidence is missing, or an implementation promise is not visible in the live product.

On rejection, return affected tickets to implementation. Do not waive visual defects because lint, unit tests, or API tests pass.
