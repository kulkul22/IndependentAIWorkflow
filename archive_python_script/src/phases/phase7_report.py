import os
from src.utils.llm import call_llm
from src.state import write_run_file, get_run_path

SYSTEM_PROMPT = """You are a technical Writer and Reporter.
Your job is to read the state of all 6 previous phases and generate a final detailed Work Report (walkthrough.md).
Summarize what was requested, the design plan, the files created, the test outcomes, and the audit decision.
Present it in a beautiful, user-facing markdown format suitable for executive review."""

def run_phase(run_id, state, config):
    print(f"[*] Starting Phase 7 (Report & Document)...")
    
    # Read plan, test, and audit summaries
    plan_file = os.path.join(get_run_path(run_id), "master_plan.md")
    test_file = os.path.join(get_run_path(run_id), "test_report.md")
    audit_file = os.path.join(get_run_path(run_id), "audit_report.md")
    
    plan = ""
    test = ""
    audit = ""
    
    research_file = os.path.join(get_run_path(run_id), "research_notes.md")
    research = ""
    if os.path.exists(research_file):
        with open(research_file, "r", encoding="utf-8") as f: research = f.read()
        
    # Read generated code file list
    outputs_dir = os.path.join(get_run_path(run_id), "outputs")
    files_list = ""
    if os.path.exists(outputs_dir):
        for root, _, filenames in os.walk(outputs_dir):
            for fname in filenames:
                rel_path = os.path.relpath(os.path.join(root, fname), outputs_dir)
                files_list += f"- {rel_path}\n"
                
    prompt = (
        f"TASK:\n{state['task']}\n\n"
        f"RESEARCH NOTES:\n{research}\n\n"
        f"MASTER PLAN:\n{plan}\n\n"
        f"FILES GENERATED:\n{files_list}\n\n"
        f"TEST REPORT:\n{test}\n\n"
        f"AUDIT REPORT:\n{audit}\n\n"
        f"ATTEMPTS: {state.get('attempts', 1)}"
    )
    
    provider = config["provider"]
    model_name = config["name"]
    
    final_report = call_llm(provider, model_name, prompt, SYSTEM_PROMPT)
    
    # Save the output file
    file_path = write_run_file(run_id, "walkthrough.md", final_report)
    
    # Update state
    state["history"]["7_report"] = "walkthrough.md"
    print(f"[+] Phase 7 Complete. Output written to: {file_path}")
    return final_report
