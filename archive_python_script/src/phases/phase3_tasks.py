import os
from src.utils.llm import call_llm
from src.state import write_run_file, get_run_path

SYSTEM_PROMPT = """You are a Project Planner.
Your job is to read the master plan and decompose it into a flat or nested checklist of tasks using the GFM markdown checklist format:
- [ ] Task 1
- [ ] Task 2
Be extremely specific. Do not omit any files or details from the plan."""

def run_phase(run_id, state, config):
    print(f"[*] Starting Phase 3 (Break Down & Create Tasks)...")
    
    # Load master plan
    plan_file = os.path.join(get_run_path(run_id), "master_plan.md")
    with open(plan_file, "r", encoding="utf-8") as f:
        master_plan = f.read()
        
    prompt = f"Using the following master plan, decompose it into a task checklist (task.md):\n\n{master_plan}"
    
    provider = config["provider"]
    model_name = config["name"]
    
    tasks = call_llm(provider, model_name, prompt, SYSTEM_PROMPT)
    
    # Save the output file
    file_path = write_run_file(run_id, "task.md", tasks)
    
    # Update state
    state["history"]["3_tasks"] = "task.md"
    print(f"[+] Phase 3 Complete. Output written to: {file_path}")
    return tasks
