import os
import glob
import json
import re
from status import normalize_status


def _read_text(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    except (OSError, UnicodeError):
        return ''


def _get_request_title(run_path):
    """Return the request title stored in, or inferred from, a workflow run."""
    state_path = os.path.join(run_path, 'state.json')
    try:
        with open(state_path, 'r', encoding='utf-8') as file:
            state = json.load(file)
        for key in ('title', 'task'):
            value = state.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
    except (OSError, UnicodeError, json.JSONDecodeError):
        pass

    research = _read_text(os.path.join(run_path, 'research_notes.md'))
    task_match = re.search(r'^\s*\*\*Task:\*\*\s*(.+?)\s*$', research, re.MULTILINE | re.IGNORECASE)
    if task_match:
        return task_match.group(1).strip()

    summary_match = re.search(
        r'^#{1,6}\s+Task Summary\s*$\s*(.+?)\s*$',
        research,
        re.MULTILINE | re.IGNORECASE,
    )
    if summary_match:
        return summary_match.group(1).strip()

    plan = _read_text(os.path.join(run_path, 'master_plan.md'))
    heading_match = re.search(r'^#\s+(.+?)\s*$', plan, re.MULTILINE)
    if heading_match:
        heading = re.sub(
            r'^(?:\[?Phase\s+\d+(?:\.\d+)?\]?\s*[:\-]?\s*)?(?:Master Plan\s*[:\-]\s*)?',
            '',
            heading_match.group(1),
            flags=re.IGNORECASE,
        ).strip()
        if heading:
            return heading

    return 'Untitled request'


def get_current_phase(project_dir=None):
    """
    Scans the parent directory (runs) for the most recent run_ folder.
    Determines the current phase based on the presence of specific files.
    """
    # Go up from dashboard/backend/parser.py to runs/
    project_dir = project_dir or os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    runs_dir = os.path.join(os.path.abspath(project_dir), 'runs')
    run_folders = sorted(glob.glob(os.path.join(runs_dir, 'run_*')), reverse=True)
    if not run_folders:
        return {
            "request_title": "No request found",
            "phase": 0,
            "role": "None",
            "model": "None",
            "status": "No runs found",
        }

    latest_run = run_folders[0]
    request_title = _get_request_title(latest_run)

    tasks_data = []
    tasks_path = os.path.join(latest_run, 'tasks.json')
    if os.path.exists(tasks_path):
        try:
            with open(tasks_path, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass

    if isinstance(tasks_data, list):
        tasks_data = [
            {**task, 'status': normalize_status(task.get('status'))}
            if isinstance(task, dict) else task
            for task in tasks_data
        ]

    workspace_path = None
    run_json_path = os.path.join(latest_run, 'run.json')
    if os.path.exists(run_json_path):
        try:
            with open(run_json_path, 'r', encoding='utf-8') as f:
                run_data = json.load(f)
                workspace_path = run_data.get("workspace_path")
        except (OSError, UnicodeError, json.JSONDecodeError):
            pass

    def state(phase, role, model, status):
        return {
            "request_title": request_title,
            "phase": phase,
            "role": role,
            "model": model,
            "status": status,
            "tasks": tasks_data,
            "workspace": workspace_path
        }


    state_path = os.path.join(latest_run, "state.json")
    if os.path.exists(state_path):
        try:
            persisted = json.loads(_read_text(state_path))
            phase = float(persisted.get("current_phase", 0))
            if phase.is_integer():
                phase = int(phase)
            if phase in (1, 2, 2.5, 2.7, 3, 4, 5, 5.5, 6, 7):
                role = persisted.get("role", "")
                model = persisted.get("model", "")
                status = persisted.get("phase_status") or persisted.get("status") or "Running"
                return state(phase, role, model, status)
        except (TypeError, ValueError, json.JSONDecodeError):
            pass
    # Check for phase markers
    if os.path.exists(os.path.join(latest_run, 'walkthrough.md')):
        return state(7, "Technical Writer", "Gemini", "Completed")
    if os.path.exists(os.path.join(latest_run, 'visual_audit.md')):
        return state(5.5, "Independent Visual Auditor", "Codex", "Visual QA")
    if os.path.exists(os.path.join(latest_run, 'advisor_log.md')):
        if os.path.exists(os.path.join(latest_run, 'task.md')) or os.path.exists(os.path.join(latest_run, 'test_results.txt')) or os.path.exists(os.path.join(latest_run, 'outputs')):
            return state(6, "Advisor / Security Auditor", "Claude", "Code Audit")
        else:
            return state(2.5, "Principal Architect", "Claude", "Plan Review")
    if os.path.exists(os.path.join(latest_run, 'test_results.txt')):
        return state(5, "SDET", "Gemini", "Test & Validate")
    if os.path.exists(os.path.join(latest_run, 'outputs')):
        return state(4, "Senior Staff Engineer", "Codex", "Execute Code")
    if os.path.exists(os.path.join(latest_run, 'task.md')):
        return state(3, "Agile Scrum Master", "Gemini", "Break Down Tasks")
    if os.path.exists(os.path.join(latest_run, 'ui_design_spec.md')):
        return state(2.7, "Product UI Designer", "Codex", "Product UI Design")
    if os.path.exists(os.path.join(latest_run, 'master_plan.md')):
        return state(2, "Lead Software Architect", "Codex", "Analyze & Plan")
    if os.path.exists(os.path.join(latest_run, 'research_notes.md')):
        return state(1, "Senior Systems Analyst", "Codex", "Research")

    return state(0, "Global", "System", "Bootstrapping")
