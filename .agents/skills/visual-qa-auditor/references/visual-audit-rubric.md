# Visual audit rubric

## Blocker

- Required page, action, or design-spec promise is absent.
- Primary journey cannot be completed in the browser.
- Content is unreadable, clipped, or horizontally inaccessible at a required viewport.
- Required screenshot or acceptance evidence is absent.

## High

- Information hierarchy is unclear on a primary page.
- Contrast or focus visibility prevents practical use.
- Responsive layout collapses incorrectly.
- Forms, tables, navigation, or destructive actions lack clear states and feedback.
- Raw/default controls materially conflict with the specified design system.

## Medium

- Inconsistent spacing, typography, alignment, icons, borders, or component styling.
- Secondary states are visually weak but usable.
- Motion or polish differs from the specification without harming completion.

## Approval rule

Approve only with zero blockers, zero unresolved high findings, screenshots at all required viewports, and evidence for every critical/high `UI-ACC-*` item. Medium findings may remain only when documented as accepted debt.
