---
name: product-ui-designer
description: Define an evidence-backed product UI direction before implementation. Use for new user-facing web or app projects, dashboard redesigns, frontend feature planning, or whenever a workflow needs wireframes, design tokens, component states, responsive behavior, and objective visual acceptance criteria before coding begins.
---

# Product UI Designer

Turn product requirements into a buildable visual contract. Do not approve vague goals such as "modern" or "clean" without concrete decisions and artifacts.

## Workflow

1. Inspect the product requirements, users, domain, existing brand assets, target framework, and current interface when one exists.
2. Define the primary journeys and information hierarchy before choosing decoration.
3. Propose two or three meaningfully different visual directions. If user selection is unavailable, choose one and record the rationale.
4. Specify the chosen system:
   - color roles and accessible contrast targets;
   - typography scale and weights;
   - spacing, radius, shadow, border, and motion tokens;
   - grid, content widths, and breakpoints;
   - icons, charts, tables, forms, navigation, and feedback patterns.
5. Define every important page and its loading, empty, error, success, disabled, destructive, and overflow states.
6. Produce desktop and mobile wireframes or a runnable prototype. Use the existing `prototype` skill when multiple UI directions need rapid comparison.
7. Write objective acceptance IDs such as `UI-ACC-001`; map each one to a page, breakpoint, state, and observable result.

## Required artifacts

Write these into the active run directory:

- `ui_design_spec.md`: users, journeys, direction, tokens, component inventory, responsive rules, and state behavior.
- `ui_acceptance.json`: acceptance IDs with `criterion`, `viewport`, `evidence_required`, and `status: pending`.
- `ui_prototype/` or `ui_wireframes.md`: sufficient visual evidence for implementation.

Use [references/design-spec-checklist.md](references/design-spec-checklist.md) as the completion checklist.

## Gate

Reject progression to task breakdown when any required artifact is absent, key screens have no responsive treatment, or acceptance language relies only on subjective adjectives. Every frontend ticket must reference applicable `UI-ACC-*` IDs.
