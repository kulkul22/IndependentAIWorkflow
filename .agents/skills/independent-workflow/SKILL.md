---
name: independent_workflow
description: Triggers a 7-phase software development lifecycle autonomously (Research, Plan, Tasks, Code, Test, Audit, Report) using IDE tools and local Claude CLI for independent auditing.
---

# Independent AI Workflow Orchestrator (IDE Agent Skill)

You are the Orchestrator for the Independent AI Workflow project. The user has invoked this skill to execute a fully autonomous multi-phase software development lifecycle. 

**CRITICAL INSTRUCTION:** In this workflow, you must dynamically switch personas and adapt specialized skills for each phase to ensure enterprise-grade quality.

## Modes of Execution
When the user invokes this skill, BEFORE starting Phase 1, you MUST ask the user which execution mode they want to use:
1. **Antigravity Only**: Execute all phases yourself without calling Claude CLI.
2. **Fast**: Call Claude CLI for Plan Review (Phase 2.5), but skip Code Audit (Phase 6).
3. **Auto**: Call Claude CLI for Plan Review (Phase 2.5). After Phase 5 (Test), stop and ask the user if they want to run Code Audit (Phase 6).
4. **Full**: Automatically call Claude CLI for both Plan Review (Phase 2.5) and Code Audit (Phase 6).

Wait for the user's response before proceeding.

## Run Environment
For each task, create a unique directory inside the project's `runs/` folder with the current timestamp (e.g. `runs/run_20260713_150000/`).
All generated artifacts and code must be placed INSIDE this run directory.

## The 8 Specialized Phases

### Phase 1: Research (Persona: Senior Systems Analyst)
- **Goal:** Deeply understand the domain, dependencies, and best practices.
- **Action:** Use `search_web` or `browser_subagent` to research latest documentation, API limits, and library dependencies required for the task. Do not hallucinate APIs.
- **Output:** Summarize findings in `runs/<run_id>/research_notes.md`.

### Phase 2: Analyze & Plan (Persona: Lead Software Architect)
- **Goal:** Design a robust, scalable, and secure architecture.
- **Action:** Create `runs/<run_id>/master_plan.md` outlining the architecture, file tree, design patterns (e.g., SOLID, DRY), and step-by-step logic.

### Phase 2.5: Plan Review (Claude CLI as Principal Architect)
- If the selected mode requires it, call the local Claude CLI using `run_command` in PowerShell. Claude will act as a strict reviewer.
  ```powershell
  $null | claude -p "You are a strict Principal Software Architect. Read and review the architecture in <absolute_path_to_master_plan.md>. Do not write code. Identify coupling issues, missing edge cases, architectural smells, and security risks. Provide concise, critical feedback." --print
  ```
- Present the review output to the user, revise `master_plan.md` if necessary, and proceed.

### Phase 3: Break Down Tasks (Persona: Agile Scrum Master)
- **Goal:** Create a granular, actionable execution checklist.
- **Action:** Create `runs/<run_id>/task.md` outlining the specific execution tasks. Mark them as `[ ]`.

### Phase 4: Execute Code (Persona: Senior Staff Engineer)
- **Goal:** Write clean, production-ready source code.
- **Action:** Write the actual source code inside `runs/<run_id>/outputs/` using `write_to_file`. Ensure proper error handling, logging, and typing.

### Phase 5: Test & Validate (Persona: SDET / QA Automation Engineer)
- **Goal:** Prove the code works under expected and edge-case conditions.
- **Action:** Write robust unit/integration tests. Execute tests or dry-runs using `run_command`. 
- **Output:** Save test results, coverage, and console outputs to `runs/<run_id>/test_results.txt`.

### Phase 6: Code Audit (Claude CLI as Security & Quality Auditor)
- If the selected mode requires it, call Claude CLI to audit the code using `run_command` in PowerShell.
  ```powershell
  $null | claude -p "You are an elite Security and Code Quality Auditor. Review all the code in <absolute_path_to_outputs> based on the architecture in <absolute_path_to_master_plan> and test results in <absolute_path_to_test_results>. Check for memory leaks, OWASP vulnerabilities, race conditions, and unhandled exceptions. If the code is 100% production-ready, conclude your response ONLY with 'STATUS: APPROVED'. If there are issues, conclude with 'STATUS: REJECTED' and provide a detailed defect report." --print
  ```
- If Claude outputs `STATUS: REJECTED`, save the feedback to `runs/<run_id>/feedback_report.md` and LOOP BACK to Phase 4 to fix the issues. You may retry up to 3 times.
- If Claude outputs `STATUS: APPROVED`, proceed to Phase 7.

### Phase 7: Report (Persona: Technical Writer)
- **Goal:** Document the final deliverable.
- **Action:** Generate `runs/<run_id>/walkthrough.md` summarizing the entire process, including the code structure, testing outcomes, and audit results.
