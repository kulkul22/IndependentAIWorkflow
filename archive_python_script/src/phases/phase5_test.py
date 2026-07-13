import os
from src.utils.llm import call_llm
from src.state import write_run_file, get_run_path

SYSTEM_PROMPT = """You are a QA Engineer and Tester.
Your job is to read the implemented files and write test scripts or evaluate the correctness of the code.
Highlight edge cases, input validation issues, error handling adequacy, and overall correctness.
Provide your final verification report in markdown format."""

def run_phase(run_id, state, config):
    print(f"[*] Starting Phase 5 (Test & Validate)...")
    
    outputs_dir = os.path.join(get_run_path(run_id), "outputs")
    
    # Read generated files to provide as context
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
    # Load master plan for business logic context
    plan_file = os.path.join(get_run_path(run_id), "master_plan.md")
    master_plan = ""
    if os.path.exists(plan_file):
        with open(plan_file, "r", encoding="utf-8") as f:
            master_plan = f.read()
            
    prompt = f"MASTER PLAN (what the code should accomplish):\n{master_plan}\n\nIMPLEMENTATION FILES TO TEST:\n{files_context}"
    
    provider = config["provider"]
    model_name = config["name"]
    
    test_report = call_llm(provider, model_name, prompt, SYSTEM_PROMPT)
    
    # Save the output file
    file_path = write_run_file(run_id, "test_report.md", test_report)
    
    # Update state
    state["history"]["5_test"] = "test_report.md"
    print(f"[+] Phase 5 Complete. Output written to: {file_path}")
    return test_report
