import json
import os
import sys
import argparse
import time

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
