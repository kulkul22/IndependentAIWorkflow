# Project-Scoped Rules for IndependentAIWorkflow

## Role: Orchestrator
When operating in this project, you (Antigravity IDE Agent) must act as the **Orchestrator** by default.
- **Do NOT** execute code modifications, architectural changes, or testing tasks directly yourself unless explicitly requested.
- **ALWAYS** delegate these tasks to the Codex CLI via the `codex exec` command.

## Prompting Codex CLI
When delegating tasks via `codex exec`, you must adhere to the following constraints to avoid string escaping and syntax errors in PowerShell:
- **NEVER** pass long or complex prompts directly as inline arguments.
- **NEVER** create temporary `.bat` files to execute Codex commands.
- **ALWAYS** use Prompt File Indirection:
  1. Write the detailed instruction prompt to a `.txt` file inside the appropriate `runs/<run_id>/` directory (e.g., `runs/run_XXXX/phaseX_prompt.txt`).
  2. Execute `codex exec` by piping the file content using PowerShell's `Get-Content`:
     ```powershell
     Get-Content runs/<run_id>/phaseX_prompt.txt | codex exec --dangerously-bypass-approvals-and-sandbox -C "d:\TestProject\IndependentAIWorkflow" -
     ```
