import os
import json
from src.utils.llm import call_llm
from src.state import write_run_file, get_run_path

SYSTEM_PROMPT = """You are a highly efficient software Developer (Executor).
Your job is to execute the tasks outlined in the plan. Write clean, production-grade code.
You must output your code in a strict JSON format matching this schema so the orchestrator can write the files:
{
  "files": [
    {
      "path": "relative/path/to/file.py",
      "content": "the actual code content..."
    }
  ]
}
Ensure all code compiles and has no placeholders. Return ONLY valid JSON, do not wrap in markdown code blocks like ```json."""

def run_phase(run_id, state, config):
    print(f"[*] Starting Phase 4 (Execute the Tasks)...")
    
    # Load plan and tasks
    plan_file = os.path.join(get_run_path(run_id), "master_plan.md")
    with open(plan_file, "r", encoding="utf-8") as f:
        master_plan = f.read()
        
    tasks_file = os.path.join(get_run_path(run_id), "task.md")
    with open(tasks_file, "r", encoding="utf-8") as f:
        tasks = f.read()
        
    feedback_file = os.path.join(get_run_path(run_id), "feedback_report.md")
    feedback_context = ""
    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, "r", encoding="utf-8") as f:
                feedback_context = f.read()
        except Exception:
            pass
            
    prompt = f"Write the code to implement the following plan and tasks:\n\nPLAN:\n{master_plan}\n\nTASKS:\n{tasks}"
    if feedback_context:
        # Read back existing code so Executor can patch rather than rewrite
        existing_code = ""
        outputs_dir = os.path.join(get_run_path(run_id), "outputs")
        if os.path.exists(outputs_dir):
            for root, _, filenames in os.walk(outputs_dir):
                for fname in filenames:
                    full_path = os.path.join(root, fname)
                    rel_path = os.path.relpath(full_path, outputs_dir)
                    try:
                        with open(full_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        existing_code += f"--- FILE: {rel_path} ---\n{content}\n\n"
                    except Exception:
                        pass
        prompt += f"\n\nPREVIOUS CODE (fix the issues, do NOT rewrite from scratch):\n{existing_code}"
        prompt += f"\n\nCRITICAL FEEDBACK ON PREVIOUS ATTEMPT:\n{feedback_context}\n\nPlease modify the generated files to fix all errors and bugs pointed out in the feedback."
    
    provider = config["provider"]
    model_name = config["name"]
    
    execution_result = call_llm(provider, model_name, prompt, SYSTEM_PROMPT)
    
    # Write raw output
    write_run_file(run_id, "execution_raw.json", execution_result)
    
    # Try parsing and writing individual files to runs/<run_id>/outputs/
    outputs_dir = os.path.join(get_run_path(run_id), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    
    try:
        data = json.loads(execution_result.strip())
        for file_info in data.get("files", []):
            file_path = file_info["path"]
            file_content = file_info["content"]
            
            # Ensure path is relative and safe
            safe_path = os.path.normpath(file_path).lstrip(os.sep)
            full_dest = os.path.join(outputs_dir, safe_path)
            os.makedirs(os.path.dirname(full_dest), exist_ok=True)
            
            with open(full_dest, "w", encoding="utf-8") as f:
                f.write(file_content)
            print(f"    [+] Created code file: {safe_path}")
            
        state["history"]["4_execute"] = "outputs"
    except Exception as e:
        print(f"[-] Failed to parse JSON execution output: {e}. Raw response saved.")
        state["history"]["4_execute"] = "execution_raw.json"
        
    print(f"[+] Phase 4 Complete.")
    return execution_result
