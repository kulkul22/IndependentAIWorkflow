import os
from src.utils.llm import call_llm
from src.state import write_run_file, get_run_path

SYSTEM_PROMPT = """You are an independent Code Auditor.
Your job is to perform a security and quality audit on the code and test report against the master plan.
Verify if there are security vulnerabilities, logical flaws, architectural mismatches, or poor coding patterns.
Provide your report in markdown format.
You MUST end your report with exactly either "STATUS: APPROVED" or "STATUS: REJECTED" (on a new line). Do not add any punctuation or text after this status line."""

def run_phase(run_id, state, config):
    print(f"[*] Starting Phase 6 (Audit & Approve)...")
    
    # Load plan, test report, and outputs context
    plan_file = os.path.join(get_run_path(run_id), "master_plan.md")
    with open(plan_file, "r", encoding="utf-8") as f:
        master_plan = f.read()
        
    test_file = os.path.join(get_run_path(run_id), "test_report.md")
    with open(test_file, "r", encoding="utf-8") as f:
        test_report = f.read()
        
    outputs_dir = os.path.join(get_run_path(run_id), "outputs")
    files_context = ""
    if os.path.exists(outputs_dir):
        for root, _, filenames in os.walk(outputs_dir):
            for fname in filenames:
                full_path = os.path.join(root, fname)
                rel_path = os.path.relpath(full_path, outputs_dir)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    files_context += f"--- FILE: {rel_path} ---\n{content}\n\n"
                except Exception:
                    pass
                    
    prompt = f"PLAN:\n{master_plan}\n\nCODE:\n{files_context}\n\nTEST REPORT:\n{test_report}"
    
    provider = config["provider"]
    model_name = config["name"]
    
    audit_report = call_llm(provider, model_name, prompt, SYSTEM_PROMPT)
    
    # Save the output file
    file_path = write_run_file(run_id, "audit_report.md", audit_report)
    
    # Update state
    state["history"]["6_audit"] = "audit_report.md"
    print(f"[+] Phase 6 Complete. Output written to: {file_path}")
    return audit_report
