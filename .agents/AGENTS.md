# Project-Scoped Rules for IndependentAIWorkflow

## Role: Codex Project Manager
When operating in this project, Codex is the primary Project Manager and Orchestrator.
- Codex owns phase selection, skill loading, delegation, state transitions, verification, and final handoff.
- Antigravity is a worker surface for execution, browser, and local agent tasks; it is not the project manager.
- Claude is an independent advisor/auditor and never controls workflow state.
- Every phase must record its active skill and output artifact.

## Prompting Codex CLI
When delegating tasks via `codex exec`, you must adhere to the following constraints to avoid string escaping and syntax errors in PowerShell:
- **NEVER** pass long or complex prompts directly as inline arguments.
- **NEVER** create temporary `.bat` files to execute Codex commands.
- **ALWAYS** use Prompt File Indirection:
  1. Write the detailed instruction prompt to a `.txt` file inside a `prompts/` subfolder in the appropriate `runs/<run_id>/` directory (e.g., `runs/run_XXXX/prompts/phaseX_prompt.txt`).
  2. Execute `codex exec` by piping the file content using PowerShell's `Get-Content`:
     ```powershell
     Get-Content runs/<run_id>/prompts/phaseX_prompt.txt | codex exec --dangerously-bypass-approvals-and-sandbox -C "d:\TestProject\IndependentAIWorkflow" -
     ```

## CLI Delegation Explicit Rules
- When the user explicitly requests to call **Claude**, you MUST invoke the `claude` CLI directly (e.g. `claude --model ...`).
- When the user explicitly requests to call **Codex**, you MUST invoke the `codex` CLI directly (`codex exec ...`).
- Do NOT confuse the two CLIs. Codex remains the orchestrator and delegates to the precise worker requested by the active phase or user.
