import json
import os
import sys
import argparse
import time


def visual_gate_error(tasks_file, task):
    """Return a fail-closed message when a UI task lacks visual approval."""
    acceptance_ids = task.get("ui_acceptance_ids")
    if not acceptance_ids:
        return None
    if not isinstance(acceptance_ids, list) or not all(isinstance(item, str) for item in acceptance_ids):
        return "ui_acceptance_ids must be a list of acceptance ID strings"

    run_dir = os.path.dirname(os.path.abspath(tasks_file))
    acceptance_path = os.path.join(run_dir, "ui_acceptance.json")
    audit_path = os.path.join(run_dir, "visual_audit.md")
    try:
        with open(acceptance_path, "r", encoding="utf-8") as handle:
            acceptance = json.load(handle)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return "ui_acceptance.json is missing or invalid"

    rows = acceptance if isinstance(acceptance, list) else acceptance.get("acceptance", [])
    indexed = {row.get("id"): row for row in rows if isinstance(row, dict)}
    failed = [item for item in acceptance_ids if indexed.get(item, {}).get("status") != "pass"]
    if failed:
        return f"visual acceptance has not passed: {', '.join(failed)}"

    try:
        with open(audit_path, "r", encoding="utf-8") as handle:
            approved = handle.read().rstrip().endswith("STATUS: APPROVED")
    except (OSError, UnicodeError):
        approved = False
    if not approved:
        return "visual_audit.md is missing or not approved"
    return None

def acquire_lock(lock_path, timeout=10):
    start_time = time.time()
    while True:
        try:
            os.mkdir(lock_path)
            return True
        except FileExistsError:
            if time.time() - start_time > timeout:
                return False
            time.sleep(0.1)

def release_lock(lock_path):
    try:
        os.rmdir(lock_path)
    except OSError:
        pass

def main():
    parser = argparse.ArgumentParser(description="Update tasks.json atomically")
    parser.add_argument("--file", required=True, help="Path to tasks.json")
    parser.add_argument("--task_id", required=True, help="Task ID to update")
    parser.add_argument("--status", help="New status")
    parser.add_argument("--assignee", help="New assignee")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Error: {args.file} not found.")
        sys.exit(1)

    lock_path = args.file + ".lockdir"

    if not acquire_lock(lock_path):
        print(f"Error: Could not acquire lock for {args.file}")
        sys.exit(1)

    try:
        with open(args.file, 'r', encoding='utf-8') as f:
            tasks = json.load(f)

        updated = False
        for task in tasks:
            if task.get("id") == args.task_id:
                if args.status == "done":
                    gate_error = visual_gate_error(args.file, task)
                    if gate_error:
                        print(f"Error: UI task {args.task_id} cannot be completed: {gate_error}")
                        sys.exit(1)
                if args.status:
                    task["status"] = args.status
                if args.assignee:
                    task["assignee"] = args.assignee
                updated = True
                break

        if updated:
            tmp_file = args.file + ".tmp"
            with open(tmp_file, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2)
            os.replace(tmp_file, args.file)
            print(f"Task {args.task_id} updated successfully.")
        else:
            print(f"Warning: Task {args.task_id} not found.")

    except Exception as e:
        print(f"Error updating task: {e}")
        sys.exit(1)
    finally:
        release_lock(lock_path)

if __name__ == "__main__":
    main()
