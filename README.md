# Independent AI Workflow Orchestrator (Javis OS Edition)

A fully autonomous, self-correcting multi-agent software development workflow powered by **Antigravity IDE (Worker)** + **Claude CLI (Advisor)** as an independent auditor and dynamic expert.

✨ **[NEW] Javis OS Integration:** Features a local Obsidian-style Second Brain with Vector Search (RAG) powered by ChromaDB. The AI automatically recalls past contexts, project structures, and technical decisions before starting any task.

---

## Quick Start

**1. Start the Javis Daemon (Knowledge Sync)**
```powershell
# Runs in the background to watch for changes in brain/vault/ and syncs to ChromaDB
python scripts/javis_daemon.py
```

**2. Trigger the Workflow**
```text
@hybrid-workflow "Describe your task here..."
```
*(Note: The workflow will automatically start a local Web Dashboard at `http://localhost:8000/` so you can monitor the agent's progress in real-time).*

---

## Execution Modes (Budget-Based)

At startup, you will be asked to choose one of four modes based on your API budget:

| # | Mode | Plan Review | Debug Escalate (Phases 4/5) | Code Audit | Cost Estimate |
|---|------|:-----------:|:---------------------------:|:----------:|:--------------|
| 1 | **Local Only** | — | — | — | $0 |
| 2 | **Safe Audit** | — | — | Claude CLI ✓ | Low |
| 3 | **Dynamic Helper**| — | Claude CLI ✓ (Max 3/task)| Claude CLI ✓ | Medium |
| 4 | **Max Quality** | Claude CLI ✓| Claude CLI ✓ (Max 3/task)| Claude CLI ✓ | High |

---

## Workflow Phases

```text
PHASE 0 ──────────────────────────────────────────────────────
  Brain Sync
  Agent  : Antigravity + ChromaDB RAG
  Output : Context injected from brain/vault/

PHASE 1 ──────────────────────────────────────────────────────
  Research
  Agent  : Codex
  Output : research_notes.md

PHASE 2 ──────────────────────────────────────────────────────
  Analyze & Plan
  Agent  : Codex
  Output : master_plan.md

PHASE 2.5 (Mode 4 only) ──────────────────────────────────────
  Plan Review
  Agent  : Claude CLI ← independent advisor
  Logic  : APPROVED → continue │ NEEDS REVISION → loop back to Phase 2

PHASE 3 ──────────────────────────────────────────────────────
  Break Down Tasks
  Agent  : Antigravity
  Output : task.md

PHASE 4 & 5 ──────────────────────────────────────────────────
  Execute Code, Test & Validate
  Agent  : Codex (Phase 4), Antigravity (Phase 5)
  Logic  : Write code -> Run tests
  Escalate (Modes 3, 4): If tests fail > 2 times -> Call Claude CLI (Debug Mode) 
                         context-compressed -> Fix code -> Loop (Max 3 limits)
  Output : outputs/ (source files) & test_results.txt

PHASE 6 (Modes 2, 3, 4 only) ─────────────────────────────────
  Code Audit
  Agent  : Claude CLI ← independent auditor
  Logic  : APPROVED → continue │ REJECTED → loop back to Phase 4
  Limit  : max 3 retries
  Output : feedback_report.md (on rejection)

PHASE 7 ──────────────────────────────────────────────────────
  Report
  Agent  : Antigravity
  Output : walkthrough.md & advisor_log.md

PHASE 7.5 ────────────────────────────────────────────────────
  Knowledge Archiving
  Agent  : Antigravity
  Output : Saves walkthrough summary to brain/vault/projects/
```

## Workflow Architecture

![Hybrid Workflow Architecture Diagram](docs/assets/hybrid_workflow.svg)

## Team Roles & Personas

![Team Roles Workflow](docs/assets/team_roles.svg?v=2)

---

## Directory Layout

```
brain/
├── chroma_db/                # Vector Database for Semantic Search
├── vault/                    # Second Brain Markdown Files (Obsidian compatible)
│   ├── content-ideas/
│   ├── journal/
│   └── projects/
dashboard/                    # Real-time Web Dashboard (auto-started on port 8000)
runs/
└── run_YYYYMMDD_HHMMSS/
    ├── research_notes.md     # Phase 1 — research findings
    ├── master_plan.md        # Phase 2 — architecture blueprint (Claude-approved)
    ├── task.md               # Phase 3 — execution checklist
    ├── outputs/              # Phase 4 — generated source code
    ├── test_results.txt      # Phase 5 — test logs
    ├── advisor_log.md        # Phase 4/5 — logs of all dynamic debug calls to Advisor
    ├── feedback_report.md    # Phase 6 — Claude defect report (if rejected)
    └── walkthrough.md        # Phase 7 — final summary report
```

> The `archive_python_script/` directory contains the legacy standalone Python CLI version, preserved for reference.
