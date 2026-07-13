import os
import yaml
from src.state import load_state, save_state, init_run
from src.phases import (
    phase1_research,
    phase2_plan,
    phase3_tasks,
    phase4_execute,
    phase5_test,
    phase6_audit,
    phase7_report
)

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config", "settings.yaml")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found at: {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

class WorkflowOrchestrator:
    def __init__(self, run_id=None, task=None):
        self.config = load_config()
        if run_id:
            self.run_id = run_id
            self.state = load_state(run_id)
            if self.state.get("status") == "success":
                raise ValueError(f"Run {run_id} completed successfully and cannot be resumed.")
            elif self.state.get("status") == "failed":
                print(f"🔄 Resuming a failed run. Resetting attempt counter.")
                self.state["status"] = "running"
                self.state["attempts"] = 1
                save_state(self.run_id, self.state)
        else:
            if not task:
                raise ValueError("Must provide a task description to initialize a new run.")
            self.run_id, self.state = init_run(task)
            
    def run_all(self):
        print(f"\n==================================================")
        print(f"🚀 Running Independent AI Workflow (Run ID: {self.run_id})")
        print(f"==================================================\n")
        
        phases = [
            (1, "phase1_research", phase1_research),
            (2, "phase2_plan", phase2_plan),
            (3, "phase3_tasks", phase3_tasks),
            (4, "phase4_execute", phase4_execute),
            (5, "phase5_test", phase5_test),
            (6, "phase6_audit", phase6_audit),
            (7, "phase7_report", phase7_report)
        ]
        
        for phase_num, config_key, module in phases:
            if self.state["current_phase"] <= phase_num:
                phase_config = self.config["models"][config_key]
                
                try:
                    result = module.run_phase(self.run_id, self.state, phase_config)
                    
                    if phase_num == 6:
                        # Fail-closed check: Only proceed if status is explicitly APPROVED
                        is_approved = "STATUS: APPROVED" in result
                        
                        if not is_approved:
                            attempts = self.state.get("attempts", 1)
                            print(f"\n⚠️ Phase 6 (Auditor) REJECTED or failed to approve the implementation! (Attempt {attempts}/3)")
                            if attempts < 3:
                                # Save the critique for the Executor
                                from src.state import write_run_file
                                write_run_file(self.run_id, "feedback_report.md", result)
                                
                                # Reset back to Phase 4 (Execute) and increment attempt count
                                self.state["current_phase"] = 4
                                self.state["attempts"] = attempts + 1
                                save_state(self.run_id, self.state)
                                
                                # Recurse to run execution again with feedback context
                                return self.run_all()
                            else:
                                print("❌ Maximum self-correction attempts reached (3/3). Stopping.")
                                self.state["status"] = "failed"
                                save_state(self.run_id, self.state)
                                return False
                    
                    self.state["current_phase"] = phase_num + 1
                    save_state(self.run_id, self.state)
                except Exception as e:
                    print(f"\n❌ Error during Phase {phase_num} ({config_key}): {e}")
                    print("Workflow paused. Correct the issue and rerun to resume.")
                    return False
                    
        print(f"\n==================================================")
        print(f"🎉 Workflow completed successfully!")
        print(f"==================================================\n")
        self.state["status"] = "success"
        save_state(self.run_id, self.state)
        return True
