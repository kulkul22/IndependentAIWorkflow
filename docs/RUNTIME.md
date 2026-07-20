# Runtime operations

## Install

From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The workflow also expects the locally authenticated agent CLIs used by the
project skills (`agy`, `codex`, and optionally `claude`).

## Dashboard

```powershell
python dashboard/backend/main.py
```

Defaults are intentionally local-only:

- host: `127.0.0.1`
- port: `8000`
- reload: disabled
- health check: `GET /api/health`

For a controlled LAN deployment, set `DASHBOARD_HOST` and
`DASHBOARD_ALLOW_ORIGINS` explicitly. Do not use wildcard origins with
credentials enabled.

## Second Brain

```powershell
python scripts/javis_daemon.py
```

The daemon synchronizes Markdown notes into ChromaDB. Notes are chunked,
content-hashed, and stale vectors are removed during a full sync.

## Tests

```powershell
python -m unittest discover -s dashboard/backend -p "test_*.py" -v
python -m unittest discover -s scripts -p "test_*.py" -v
node --check dashboard/frontend/script.js
```

## Calling Antigravity/Gemini

Use the repository wrapper when a task should be executed by the logged-in
Antigravity account:

```powershell
python call_antigravity.py --prompt "Run the dashboard tests" --cwd (Get-Location)
python call_antigravity.py --prompt-file runs/run_x/phase4_prompt.txt --output runs/run_x/agy_result.md
```

The wrapper fails loudly on timeout, missing CLI, or non-zero agent exit.
