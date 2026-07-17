import os
import time
import json
import shutil

runs_dir = 'runs'
run_folders = [f for f in os.listdir(runs_dir) if f.startswith('run_')]
run_folders.sort(reverse=True)
latest_run = os.path.join(runs_dir, run_folders[0])

tasks_file = os.path.join(latest_run, 'tasks.json')
request_file = os.path.join(latest_run, 'request.md')

# Ensure clean state
def clear_phases():
    for f in ['research_notes.md', 'master_plan.md', 'task.md', 'test_results.txt']:
        p = os.path.join(latest_run, f)
        if os.path.exists(p):
            os.remove(p)
    out_dir = os.path.join(latest_run, 'outputs')
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    if os.path.exists(tasks_file):
        os.remove(tasks_file)

print("Starting simulation for UI...")
clear_phases()

with open(request_file, 'w', encoding='utf-8') as f:
    f.write("Xây dựng tính năng giỏ hàng cho Website E-commerce")

# Phase 1
print("Phase 1: Research")
with open(os.path.join(latest_run, 'research_notes.md'), 'w', encoding='utf-8') as f:
    f.write("**Task:** Dashboard Kanban & Sub-agents Simulation\n\nPhân tích tài liệu...")
time.sleep(3)

# Phase 2
print("Phase 2: Plan")
with open(os.path.join(latest_run, 'master_plan.md'), 'w', encoding='utf-8') as f:
    f.write("# Master Plan: Dashboard Kanban & Sub-agents Simulation\nLên kiến trúc Database...")
time.sleep(3)

# Phase 3: Create tasks
print("Phase 3: Breakdown Tasks")
with open(os.path.join(latest_run, 'task.md'), 'w', encoding='utf-8') as f:
    f.write("Tạo task...")

initial_tasks = [
  {"id": "T1", "title": "Tạo DB Table cho Giỏ hàng", "assignee": None, "status": "todo", "priority": "High", "sp": 2},
  {"id": "T2", "title": "API Thêm sản phẩm vào giỏ", "assignee": None, "status": "todo", "priority": "High", "sp": 3},
  {"id": "T3", "title": "UI hiển thị popup giỏ hàng", "assignee": None, "status": "todo", "priority": "Medium", "sp": 3}
]

with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(4)

# Phase 4: Execute
print("Phase 4: Codex executing and spawning sub-agents")
os.makedirs(os.path.join(latest_run, 'outputs'), exist_ok=True)

# codex-alex takes T1
initial_tasks[0]['assignee'] = 'codex-alex'
initial_tasks[0]['status'] = 'in_progress'
with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(3)

# codex-thong takes T2
initial_tasks[1]['assignee'] = 'codex-thong'
initial_tasks[1]['status'] = 'in_progress'
with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(3)

# codex-alex finishes T1 -> in_test
initial_tasks[0]['status'] = 'in_test'
with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(2)

# codex-ui takes T3
initial_tasks[2]['assignee'] = 'codex-ui'
initial_tasks[2]['status'] = 'in_progress'
with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(2)

# Phase 5: Test
print("Phase 5: Gemini testing")
with open(os.path.join(latest_run, 'test_results.txt'), 'w', encoding='utf-8') as f:
    f.write("Chạy test...")

# gemini-tester takes T1
initial_tasks[0]['assignee'] = 'gemini-tester1'
with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(2)

# tester completes T1
initial_tasks[0]['status'] = 'done'
with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(2)

# codex-thong gets stuck on T2
initial_tasks[1]['status'] = 'stuck'
with open(tasks_file, 'w', encoding='utf-8') as f:
    json.dump(initial_tasks, f)
time.sleep(2)

print("Simulation finished!")
