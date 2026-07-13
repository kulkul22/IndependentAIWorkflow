import sys
import argparse
from src.orchestrator import WorkflowOrchestrator

def main():
    parser = argparse.ArgumentParser(description="Independent AI Workflow Orchestrator (7-Phase Multi-Agent Model)")
    parser.add_argument("task", nargs="?", help="Task description to start a new run")
    parser.add_argument("--resume", help="Run ID to resume an existing run")
    
    args = parser.parse_args()
    
    if args.resume:
        try:
            orch = WorkflowOrchestrator(run_id=args.resume)
            orch.run_all()
        except Exception as e:
            print(f"Error resuming run: {e}")
            sys.exit(1)
    elif args.task:
        try:
            orch = WorkflowOrchestrator(task=args.task)
            orch.run_all()
        except Exception as e:
            print(f"Error starting workflow: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
