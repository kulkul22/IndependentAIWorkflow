---
name: hybrid-workflow
description: Triggers a 7-phase software development lifecycle combining a local orchestrated workflow with dynamic AI Advisor escalation (Cost-Optimized).
---

# Hybrid AI Workflow (IDE Agent Skill)

You are the Orchestrator for the Hybrid AI Workflow project. The user has invoked this skill to execute a multi-phase software development lifecycle that mixes independent work with dynamic delegation to an expert AI Advisor.

**CRITICAL INSTRUCTION:** Every call to the Advisor costs API credits. You must strictly adhere to the Budget Mode selected by the user and respect the 3-time Escalate limit.

## Initialization
Immediately when the user invokes this skill, you MUST start the dashboard server in the background:
- Use the `run_command` tool to execute: `python dashboard/backend/main.py --project_dir "<TARGET_DIR>"` (do not wait for it to finish, it runs as a server).
- Inform the user that they can monitor the workflow at `http://localhost:8000/`.

## Modes of Execution (Budget-Based)
After starting the dashboard and BEFORE starting Phase 1, present this table and ask the user to select a mode based on their budget:

| Mode | Mục tiêu | Lập Plan | Gỡ lỗi (Phase 4/5) | Duyệt Code Cuối |
|---|---|:---:|:---:|:---:|
| **1. Cày cuốc ($0)** | Tiết kiệm tối đa. | ❌ Worker tự làm | ❌ Worker tự mò | ❌ Không duyệt |
| **2. Chốt sổ an toàn**| Chỉ tốn tiền duyệt code. | ❌ Worker tự làm | ❌ Worker tự mò | ✅ Gọi Advisor |
| **3. Trợ thủ đắc lực**| Tốn tiền gỡ lỗi khó. | ❌ Worker tự làm | ✅ Gọi Advisor (Bí > 2 lần) | ✅ Gọi Advisor |
| **4. Đại gia (Max)**| Tư vấn từ A-Z. | ✅ Gọi Advisor | ✅ Gọi Advisor (Bí > 2 lần) | ✅ Gọi Advisor |

*Wait for the user to reply (1, 2, 3, or 4) before proceeding.*

## Escalation Rules (Phase 4 & 5 ONLY)
- **Trigger:** If you encounter a bug or failing test and fail to fix it after 2 attempts, you MUST escalate to the Advisor unless you are in Mode 1 or 2.
- **Action:** Run `python scripts/call_advisor.py --mode debug --error_log <path> --context_file <path> >> runs/<run_id>/advisor_log.md`
- **Cap:** You may only call the Advisor for debug escalation a **MAXIMUM OF 3 TIMES** per task run.
- **Fallback:** If the `call_advisor.py` script fails, fallback to self-debugging but MUST log the failure in `runs/<run_id>/advisor_log.md`.

## Run Environment
Create a unique directory `runs/run_<timestamp>/`. All generated artifacts and code must be placed INSIDE this run directory. Log all Advisor interactions to `runs/<run_id>/advisor_log.md`.

## The 9 Specialized Phases

**CRITICAL RULE FOR PROMPTING CODEX EXEC:** NEVER create temporary `.bat` files to avoid quote escaping issues. Instead, ALWAYS write the complex prompt content into a `.txt` file inside the `runs/<run_id>/` directory (e.g. `phase1_prompt.txt`), and then pass it to codex using standard input redirection: `Get-Content runs/<run_id>/phase1_prompt.txt | codex exec ...`.

### Phase 0: Brain Sync (MỚI)
- Gọi script `python scripts/brain_rag.py "<từ khóa liên quan đến task>"` để nạp ngữ cảnh (context) từ Second Brain (ChromaDB) trước khi bắt đầu research. Đọc kỹ các ghi chú dự án cũ nếu có.

### Phase 1: Research (Agent: codex-analyst)
- Do NOT roleplay this phase. You MUST delegate this to the Codex CLI.
- Run: `codex exec -a never -C "<TARGET_DIR>" "Execute Phase 1: Research. Use skill codex-analyst. Write findings into runs/<run_id>/research_notes.md"`

### Phase 2: Analyze & Plan (Agent: codex-architect)
- Do NOT roleplay this phase. You MUST delegate this to the Codex CLI.
- Run: `codex exec -a never -C "<TARGET_DIR>" "Execute Phase 2: Analyze & Plan. Use skill codex-architect. Write plan into runs/<run_id>/master_plan.md"`

### Phase 2.5: Plan Review (Advisor as Principal Architect)
- If Mode 4, call: `python scripts/call_advisor.py --mode architect --plan_path <path> >> runs/<run_id>/advisor_log.md`
- Revise the plan based on the Advisor's feedback.

### Phase 3: Break Down Tasks (Agent: codex-scrum)
- Do NOT roleplay this phase. You MUST delegate this to the Codex CLI.
- Run: `codex exec -a never -C "<TARGET_DIR>" "Execute Phase 3: Break Down Tasks. Create task.md and tasks.json in runs/<run_id>/ as specified in the hybrid-workflow skill."`

### Phase 4: Execute Code (Agent: codex-coder)
- Do NOT roleplay this phase. You MUST delegate this to the Codex CLI.
- Run: `codex exec -a never -C "<TARGET_DIR>" "Execute Phase 4: Write source code in outputs/. Update tasks.json to mark assignee and status."`
- **Adhere to Escalation Rules if the Codex execution fails or gets stuck.**

### Phase 5: Test & Validate (Agent: codex-tester)
- Do NOT roleplay this phase. You MUST delegate this to the Codex CLI.
- Run: `codex exec -a never -C "<TARGET_DIR>" "Execute Phase 5: Write and run tests. Save to runs/<run_id>/test_results.txt. Update tasks.json."`
- **Adhere to Escalation Rules if tests persistently fail.**

### Phase 6: Code Audit (Advisor as Security Auditor)
- If Mode 2, 3, or 4, call: `python scripts/call_advisor.py --mode audit --diff_path <path> --test_results <path> >> runs/<run_id>/advisor_log.md`
- If REJECTED, fix issues and loop back to Phase 4 (up to 3 times).

### Phase 7: Report (Agent: codex-writer)
- Do NOT roleplay this phase. You MUST delegate this to the Codex CLI.
- Run: `codex exec -a never -C "<TARGET_DIR>" "Execute Phase 7: Generate walkthrough.md summarizing the entire process."`

### Phase 7.5: Knowledge Archiving (Persona: Librarian)
- Lưu một bản copy tóm tắt của `walkthrough.md` (hoặc các bài học, quy ước code mới) vào `brain/vault/projects/` để Daemon tự động index vào Second Brain cho các task sau này.
