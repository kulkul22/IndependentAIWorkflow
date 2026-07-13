# Independent AI Workflow Orchestrator

A fully autonomous, self-correcting multi-agent software development workflow powered by **Antigravity IDE** + **Claude CLI** as an independent auditor.

---

## Quick Start

```
/independent_workflow "Describe your task here..."
```

---

## Execution Modes

At startup, you will be asked to choose one of four modes:

| # | Mode | Plan Review | Code Audit | Cost | Time |
|---|------|:-----------:|:----------:|------|------|
| 1 | **Antigravity Only** | — | — | $0 | ~5 min |
| 2 | **Fast** | Claude CLI ✓ | — | ~$0.003 | ~10 min |
| 3 | **Auto** | Claude CLI ✓ | Ask after test | ~$0.01–0.10 | ~15 min |
| 4 | **Full** | Claude CLI ✓ | Claude CLI ✓ | ~$0.05–0.10 | ~20 min |

---

## Workflow Phases

```
PHASE 1 ──────────────────────────────────────────────────────
  Research
  Agent  : Antigravity
  Output : research_notes.md

PHASE 2 ──────────────────────────────────────────────────────
  Analyze & Plan
  Agent  : Antigravity
  Output : master_plan.md

PHASE 2.5 (Modes 2, 3, 4 only) ──────────────────────────────
  Plan Review
  Agent  : Claude CLI ← independent auditor
  Logic  : APPROVED → continue │ NEEDS REVISION → loop back to Phase 2

PHASE 3 ──────────────────────────────────────────────────────
  Break Down Tasks
  Agent  : Antigravity
  Output : task.md

PHASE 4 ──────────────────────────────────────────────────────
  Execute Code
  Agent  : Antigravity
  Output : outputs/ (all source files)

PHASE 5 ──────────────────────────────────────────────────────
  Test & Validate
  Agent  : Antigravity
  Output : test_results.txt

PHASE 6 (Modes 3, 4 only) ───────────────────────────────────
  Code Audit
  Agent  : Claude CLI ← independent auditor
  Logic  : APPROVED → continue │ REJECTED → loop back to Phase 4
  Limit  : max 3 retries
  Output : feedback_report.md (on rejection)

PHASE 7 ──────────────────────────────────────────────────────
  Report
  Agent  : Antigravity
  Output : walkthrough.md
```

## Workflow Diagram

```mermaid
flowchart TD
    Start(["/independent_workflow 'task'"]):::input --> Mode

    Mode["Choose Execution Mode\n────────────────────\n1 · Antigravity Only\n2 · Fast\n3 · Auto\n4 · Full"]:::decision

    subgraph ANTIGRAVITY["  ⚙️  Antigravity Engine  "]
        P1["Phase 1\nResearch\n📄 research_notes.md"]
        P2["Phase 2\nAnalyze & Plan\n📄 master_plan.md"]
        P3["Phase 3\nBreak Down Tasks\n📄 task.md"]
        P4["Phase 4\nExecute Code\n📁 outputs/"]
        P5["Phase 5\nTest & Validate\n📄 test_results.txt"]
        P7["Phase 7\nReport\n📄 walkthrough.md"]
    end

    subgraph CLAUDE["  🤖  Claude CLI — Independent Auditor  "]
        P25["Phase 2.5\nPlan Review"]
        P6["Phase 6\nCode Audit"]
    end

    Mode --> P1 --> P2

    P2 -->|"Modes 2 · 3 · 4"| P25
    P25 -->|"✅ APPROVED"| P3
    P25 -.->|"✏️ NEEDS REVISION"| P2

    P2 -->|"Mode 1 only"| P3
    P3 --> P4 --> P5

    P5 -->|"Modes 3 · 4"| P6
    P5 -->|"Modes 1 · 2"| P7

    P6 -->|"✅ APPROVED"| P7
    P6 -.->|"❌ REJECTED\nmax 3 retries"| P4

    P7 --> Done(["✅ Complete"]):::done

    classDef input    fill:#6366f1,color:#fff,stroke:none
    classDef decision fill:#0f172a,color:#e2e8f0,stroke:#334155
    classDef done     fill:#10b981,color:#fff,stroke:none

    style ANTIGRAVITY fill:#1e293b,color:#94a3b8,stroke:#334155
    style CLAUDE      fill:#1c1a0f,color:#fbbf24,stroke:#92400e

    style P25 fill:#f59e0b,color:#000,stroke:none
    style P6  fill:#f59e0b,color:#000,stroke:none
```

---

## Output Directory Layout

Each run gets its own isolated folder:

```
runs/
└── run_YYYYMMDD_HHMMSS/
    ├── research_notes.md     # Phase 1 — research findings
    ├── master_plan.md        # Phase 2 — architecture blueprint (Claude-approved)
    ├── task.md               # Phase 3 — execution checklist
    ├── outputs/              # Phase 4 — generated source code
    ├── test_results.txt      # Phase 5 — test logs
    ├── feedback_report.md    # Phase 6 — Claude defect report (if rejected)
    └── walkthrough.md        # Phase 7 — final summary report
```

> The `archive_python_script/` directory contains the legacy standalone Python CLI version, preserved for reference.
