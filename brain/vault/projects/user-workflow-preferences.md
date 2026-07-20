# User workflow preferences

## Bug-fix completion contract

When the user asks to fix a bug, follow this bounded lifecycle:

1. Reproduce the reported symptom.
2. Fix the root cause.
3. Add or update a regression test.
4. Run validation proportional to the change.
5. Immediately report the root cause, changed files, and exact validation results.
6. End the request after reporting completion.

Do not leave the request pending after validation succeeds. Do not continue monitoring, waiting, auditing, refactoring, or running background work unless the user explicitly requests it. If a command is unusually slow, provide a status update rather than appearing stuck.

This preference was explicitly requested by the user on 2026-07-20 after completed bug fixes remained pending without an immediate final report.
