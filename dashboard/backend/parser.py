import os
import glob
import json
import re
from status import normalize_status


PHASE_DETAILS = {
    0: ("Global", "System", "Bootstrapping"),
    1: ("Senior Systems Analyst", "Codex", "Research"),
    2: ("Lead Software Architect", "Codex", "Analyze & Plan"),
    2.5: ("Principal Architect", "Claude", "Plan Review"),
    2.7: ("Product UI Designer", "Codex", "Product UI Design"),
    3: ("Agile Scrum Master", "Gemini", "Break Down Tasks"),
    4: ("Senior Staff Engineer", "Codex", "Execute Code"),
    5: ("Orchestrator", "Antigravity IDE", "Test & Validate"),
    5.5: ("Independent Visual Auditor", "Codex", "Visual QA"),
    6: ("Advisor / Security Auditor", "Claude", "Code Audit"),
    7: ("Technical Writer", "Gemini", "Completed"),
}

CODING_STATUSES = {
    'active', 'coding', 'in_progress', 'inprogress', 'processing', 'working'
}
TESTING_STATUSES = {'in_test', 'qa', 'test', 'testing'}


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


def _read_json(path, default):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (OSError, UnicodeError, json.JSONDecodeError):
        return default


def _normalise_status(value):
    if not isinstance(value, str):
        return ''
    return re.sub(r'[\s-]+', '_', value.strip().lower())


def _phase_from_tasks(tasks):
    statuses = {
        _normalise_status(task.get('status'))
        for task in tasks
        if isinstance(task, dict)
    }
    if statuses & CODING_STATUSES:
        return 4
    if statuses & TESTING_STATUSES:
        return 5
    return None


def _phase_marker(run_path):
    markers = []
    for path in glob.glob(os.path.join(run_path, 'phase_*.md')):
        match = re.search(r'phase_(\d+(?:\.\d+)?)\.md$', path, re.IGNORECASE)
        if not match:
            continue
        try:
            modified_at = os.path.getmtime(path)
        except OSError:
            continue
        phase = float(match.group(1))
        if phase.is_integer():
            phase = int(phase)
        markers.append((modified_at, phase, path))

    if not markers:
        return None

    modified_at, phase, path = max(markers, key=lambda marker: (marker[0], marker[1]))
    details = {}
    content = _read_text(path)
    for key in ('role', 'model', 'status'):
        match = re.search(
            rf'^\s*{key}\s*:\s*(.+?)\s*$',
            content,
            re.MULTILINE | re.IGNORECASE,
        )
        if match:
            details[key] = match.group(1).strip()
    return modified_at, phase, details


def _state_phase(state_data):
    phase = state_data.get('current_phase')
    try:
        phase = float(phase)
    except (TypeError, ValueError):
        return None

    if phase.is_integer():
        phase = int(phase)
    if phase > 7 or state_data.get('status') == 'success':
        return 7
    return phase if phase in PHASE_DETAILS else None


def _modified_at(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return None


def get_current_phase(project_dir=None):
    """
    Return dashboard state for the latest workflow run in ``project_dir``.

    Explicit workflow state and phase markers take precedence over cumulative
    output artifacts. Task activity is used before artifact-based fallback so
    a coding retry does not remain stuck on an older testing step.
    """
    if project_dir is None:
        project_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    project_dir = os.path.abspath(project_dir)
    runs_dir = project_dir if os.path.basename(project_dir) == 'runs' else os.path.join(project_dir, 'runs')
    run_folders = sorted(glob.glob(os.path.join(runs_dir, 'run_*')), reverse=True)
    if not run_folders:
        return {
            "request_title": "No request found",
            "phase": 0,
            "role": "None",
            "model": "None",
            "status": "No runs found",
            "tasks": [],
        }

    latest_run = run_folders[0]
    request_title = _get_request_title(latest_run)

    tasks_data = _read_json(os.path.join(latest_run, 'tasks.json'), [])
    if isinstance(tasks_data, dict):
        tasks_data = tasks_data.get('tasks', [])
    if not isinstance(tasks_data, list):
        tasks_data = []
    tasks_data = [
        {**task, 'status': normalize_status(task.get('status'))}
        if isinstance(task, dict) else task
        for task in tasks_data
    ]

    workspace_path = None
    run_data = _read_json(os.path.join(latest_run, 'run.json'), {})
    if isinstance(run_data, dict):
        workspace_path = run_data.get('workspace_path')

    def dashboard_state(phase, details=None):
        role, model, status = PHASE_DETAILS[phase]
        details = details or {}
        return {
            "request_title": request_title,
            "phase": phase,
            "role": details.get('role', role),
            "model": details.get('model', model),
            "status": details.get('status', status),
            "tasks": tasks_data,
            "workspace": workspace_path,
        }

    state_data = _read_json(os.path.join(latest_run, 'state.json'), {})
    if isinstance(state_data, dict):
        phase = _state_phase(state_data)
        if phase is not None:
            details = {}
            if isinstance(state_data.get('role'), str):
                details['role'] = state_data['role']
            if isinstance(state_data.get('model'), str):
                details['model'] = state_data['model']
            if state_data.get('status') == 'success':
                details['status'] = 'Completed'
            elif isinstance(state_data.get('phase_status'), str):
                details['status'] = state_data['phase_status']
            return dashboard_state(phase, details)

    candidates = []
    marker = _phase_marker(latest_run)
    if marker is not None:
        modified_at, phase, details = marker
        if phase in PHASE_DETAILS:
            candidates.append((modified_at, 2, phase, details))

    task_phase = _phase_from_tasks(tasks_data)
    if task_phase is not None:
        modified_at = _modified_at(os.path.join(latest_run, 'tasks.json'))
        if modified_at is not None:
            candidates.append((modified_at, 3, task_phase, {}))

    # Artifact candidates keep older runs compatible. Comparing modification
    # times prevents a stale later-phase artifact from masking a coding retry.
    artifact_phases = [
        ('walkthrough.md', 7),
        ('visual_audit.md', 5.5),
        ('test_results.txt', 5),
        ('outputs', 4),
        ('task.md', 3),
        ('ui_design_spec.md', 2.7),
        ('master_plan.md', 2),
        ('research_notes.md', 1),
    ]
    advisor_path = os.path.join(latest_run, 'advisor_log.md')
    advisor_modified_at = _modified_at(advisor_path)
    if advisor_modified_at is not None:
        if os.path.exists(os.path.join(latest_run, 'task.md')) or os.path.exists(os.path.join(latest_run, 'test_results.txt')) or os.path.exists(os.path.join(latest_run, 'outputs')):
            advisor_phase = 6
        else:
            advisor_phase = 2.5
        candidates.append((advisor_modified_at, 1, advisor_phase, {}))

    for filename, phase in artifact_phases:
        modified_at = _modified_at(os.path.join(latest_run, filename))
        if modified_at is not None:
            candidates.append((modified_at, 1, phase, {}))

    if candidates:
        _, _, phase, details = max(candidates, key=lambda candidate: candidate[:2])
        return dashboard_state(phase, details)

    return dashboard_state(0)
