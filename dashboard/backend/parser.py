import os
import glob
import json
import re


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


def get_current_phase():
    """
    Scans the parent directory (runs) for the most recent run_ folder.
    Determines the current phase based on the presence of specific files.
    """
    # Go up from dashboard/backend/parser.py to runs/
    runs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'runs'))
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

    def state(phase, role, model, status):
        return {
            "request_title": request_title,
            "phase": phase,
            "role": role,
            "model": model,
            "status": status,
            "tasks": tasks_data
        }

    # Check for phase markers
    if os.path.exists(os.path.join(latest_run, 'walkthrough.md')):
        return state(7, "Technical Writer", "Gemini", "Completed")
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
    if os.path.exists(os.path.join(latest_run, 'master_plan.md')):
        return state(2, "Lead Software Architect", "Codex", "Analyze & Plan")
    if os.path.exists(os.path.join(latest_run, 'research_notes.md')):
        return state(1, "Senior Systems Analyst", "Codex", "Research")

    return state(0, "Global", "System", "Bootstrapping")