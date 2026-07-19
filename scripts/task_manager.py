import argparse
import json
import os

def main():
    parser = argparse.ArgumentParser(description="Update task status in tasks.json")
    parser.add_argument("--file", required=True, help="Path to tasks.json")
    parser.add_argument("--task_id", type=str, required=True, help="Task ID to update (e.g., T1)")
    parser.add_argument("--status", required=True, help="New status (e.g., in_progress, in_test, done)")
    parser.add_argument("--assignee", help="Assignee to update (optional)")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: {args.file} not found.")
        return

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
        
        if not isinstance(tasks, list):
            print(f"Error: Expected a JSON array in {args.file}.")
            return

        found = False
        for task in tasks:
            if str(task.get('id')) == args.task_id:
                task['status'] = args.status
                if args.assignee:
                    task['assignee'] = args.assignee
                found = True
                break
                
        if not found:
            print(f"Warning: Task ID {args.task_id} not found in {args.file}.")
            return
            
        with open(args.file, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2)
            
        print(f"Successfully updated task {args.task_id} to status '{args.status}'.")
    except Exception as e:
        print(f"Error processing {args.file}: {e}")

if __name__ == "__main__":
    main()
