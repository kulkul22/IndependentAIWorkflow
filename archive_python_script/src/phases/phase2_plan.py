import os
from src.utils.llm import call_llm
from src.state import write_run_file, get_run_path

SYSTEM_PROMPT = """You are a senior Architect and Planner.
Your job is to read the research notes and formulate a detailed, step-by-step master implementation plan.
Avoid vague generalities. Specify code layouts, database models, configuration schemas, and step-by-step changes required.
Format your output as markdown with clear headers."""

def run_phase(run_id, state, config):
    print(f"[*] Starting Phase 2 (Analyze, Plan & Approve)...")
    
    # Load research notes from Phase 1
    research_file = os.path.join(get_run_path(run_id), "research_notes.md")
    with open(research_file, "r", encoding="utf-8") as f:
        research_notes = f.read()
        
    prompt = f"Using the following research notes, formulate an Approved Master Implementation Plan:\n\n{research_notes}"
    
    provider = config["provider"]
    model_name = config["name"]
    
    master_plan = call_llm(provider, model_name, prompt, SYSTEM_PROMPT)
    
    # Save the output file
    file_path = write_run_file(run_id, "master_plan.md", master_plan)
    
    # Update state
    state["history"]["2_plan"] = "master_plan.md"
    print(f"[+] Phase 2 Complete. Output written to: {file_path}")
    return master_plan
