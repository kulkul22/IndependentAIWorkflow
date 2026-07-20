"""Headless Antigravity/Gemini wrapper for requested repository tasks.

Examples:
    python call_antigravity.py --prompt "Run the dashboard tests"
    python call_antigravity.py --prompt-file runs/run_x/phase4_prompt.txt

The wrapper is intentionally explicit: it runs only when invoked as a script
and returns a non-zero exit code when Antigravity cannot complete the request.
"""

import argparse
import os
import shutil
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")


def resolve_agy():
    """Resolve the installed Antigravity CLI on Windows or PATH."""
    candidates = [
        shutil.which("agy"),
        os.path.expandvars(r"%LOCALAPPDATA%\agy\bin\agy.exe"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    raise FileNotFoundError("Antigravity CLI (agy) was not found")


def call_antigravity(prompt, *, cwd=None, timeout=300):
    """Run one headless Antigravity prompt and return its text output."""
    command = [
        resolve_agy(),
        "--dangerously-skip-permissions",
        "-p",
        prompt,
        "--print-timeout",
        f"{timeout}s",
    ]
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout + 30,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"Antigravity timed out after {timeout}s") from exc
    except OSError as exc:
        raise RuntimeError(f"Unable to start Antigravity: {exc}") from exc

    output = result.stdout.strip()
    if result.returncode != 0:
        detail = result.stderr.strip() or output or "unknown Antigravity failure"
        raise RuntimeError(f"Antigravity exited with code {result.returncode}: {detail}")
    return output


def main():
    parser = argparse.ArgumentParser(description="Call Antigravity/Gemini headlessly")
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="Prompt to send to Antigravity")
    source.add_argument("--prompt-file", help="UTF-8 file containing the prompt")
    parser.add_argument("--cwd", default=os.getcwd(), help="Workspace directory")
    parser.add_argument("--timeout", type=int, default=300, help="Timeout in seconds")
    parser.add_argument("--output", help="Optional file for the response")
    args = parser.parse_args()

    prompt = args.prompt
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as file:
            prompt = file.read()

    try:
        response = call_antigravity(prompt, cwd=args.cwd, timeout=args.timeout)
    except (OSError, RuntimeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write(response)
    else:
        print(response)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
