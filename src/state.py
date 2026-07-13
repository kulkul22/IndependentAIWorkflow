import os
import json
from datetime import datetime

RUNS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs")

def init_run(task_description):
    run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
    run_path = os.path.join(RUNS_DIR, run_id)
    os.makedirs(run_path, exist_ok=True)
    
    state = {
        "run_id": run_id,
        "task": task_description,
        "current_phase": 1,
        "attempts": 1,
        "history": {
            "1_research": None,
            "2_plan": None,
            "3_tasks": None,
            "4_execute": None,
            "5_test": None,
            "6_audit": None,
            "7_report": None
        },
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    
    save_state(run_id, state)
    return run_id, state

def get_run_path(run_id):
    return os.path.join(RUNS_DIR, run_id)

def load_state(run_id):
    path = os.path.join(get_run_path(run_id), "state.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"State file not found for run {run_id}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(run_id, state):
    path = os.path.join(get_run_path(run_id), "state.json")
    state["updated_at"] = datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

def write_run_file(run_id, filename, content):
    path = os.path.join(get_run_path(run_id), filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path
