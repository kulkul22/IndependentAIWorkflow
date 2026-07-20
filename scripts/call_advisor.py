import argparse
import sys
import os
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

DEFAULT_TIMEOUTS = {
    "architect": 180,
    "debug": 120,
    "audit": 180,
}

def redact_secrets(text: str) -> str:
    """Xóa các chuỗi nhạy cảm như API Keys, Passwords ra khỏi text."""
    text = re.sub(r'(sk-[a-zA-Z0-9]{20,})', '[REDACTED_API_KEY]', text)
    text = re.sub(r'(AKIA[0-9A-Z]{16})', '[REDACTED_AWS_KEY]', text)
    text = re.sub(r'(eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+)', '[REDACTED_JWT]', text)
    text = re.sub(r'(password|passwd|pwd)=([^\s;&]+)', r'\1=[REDACTED_PASSWORD]', text, flags=re.IGNORECASE)
    text = re.sub(r'(postgres|mysql|mongodb)(\+srv)?:\/\/[^:]+:[^@]+@', r'\1\2://[REDACTED_USER]:[REDACTED_PASS]@', text)
    return text

def is_safe_path(filepath: str) -> bool:
    """Kiểm tra đường dẫn an toàn (chặn các file nhạy cảm)."""
    blacklist = ['.env', 'secrets', 'credentials', 'keys', '.pem', '.key', 'id_rsa']
    filepath_lower = filepath.lower()
    for bad in blacklist:
        if bad in filepath_lower:
            return False
    return True

def call_claude_cli(prompt: str, timeout: int = 180) -> str:
    """Call Claude and fail closed when the advisor is unavailable."""
    try:
        result = subprocess.run(
            ['claude', '--print'],
            input=prompt,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return f"ERROR_ADVISOR_TIMEOUT_AFTER_{timeout}S"
    except OSError as exc:
        return f"ERROR_ADVISOR_UNAVAILABLE: {exc}"

    output = result.stdout.strip()
    if result.returncode != 0:
        detail = result.stderr.strip() or output or "unknown advisor failure"
        return f"ERROR_ADVISOR_EXIT_{result.returncode}: {detail}"
    return output or "ERROR_ADVISOR_EMPTY_RESPONSE"
def load_skill_prompt(skill_name: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skill_path = os.path.join(base_dir, '.agents', 'skills', skill_name, 'SKILL.md')
    if os.path.exists(skill_path):
        with open(skill_path, 'r', encoding='utf-8') as f:
            return f.read()
    return ""

def check_budget(target_file: str):
    import json
    if not target_file:
        return
    run_dir = os.path.dirname(os.path.abspath(target_file))
    budget_file = os.path.join(run_dir, "advisor_budget.json")
    
    count = 0
    if os.path.exists(budget_file):
        try:
            with open(budget_file, "r") as f:
                data = json.load(f)
                count = data.get("calls", 0)
        except Exception:
            pass
            
    if count >= 3:
        print("ERROR: Advisor budget exceeded! (Max 3 calls per run). Call rejected.")
        sys.exit(1)
        
    count += 1
    try:
        with open(budget_file, "w") as f:
            json.dump({"calls": count}, f)
    except Exception:
        pass

def handle_architect_mode(plan_path: str, timeout: int = DEFAULT_TIMEOUTS["architect"]):
    check_budget(plan_path)
    if not os.path.exists(plan_path):
        print(f"Error: Plan file not found at {plan_path}")
        sys.exit(1)
        
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = redact_secrets(content)
    
    skill_prompt = load_skill_prompt("advisor-architect")
    prompt = f"{skill_prompt}\n\nPLAN CONTENT:\n{content}"
    
    print("Calling AI Advisor (Architect Mode via Claude CLI)...")
    feedback = call_claude_cli(prompt, timeout=timeout)
    print("\n--- ADVISOR FEEDBACK ---\n")
    print(feedback)
    print("\n------------------------\n")

def handle_debug_mode(error_log_path: str, context_file: str, timeout: int = DEFAULT_TIMEOUTS["debug"]):
    check_budget(error_log_path)
    if not os.path.exists(error_log_path):
        print(f"Error: Error log not found at {error_log_path}")
        sys.exit(1)
        
    with open(error_log_path, 'r', encoding='utf-8') as f:
        error_content = f.read()
    
    context = ""
    if context_file and os.path.exists(context_file):
        if is_safe_path(context_file):
            with open(context_file, 'r', encoding='utf-8') as f:
                # Nén context: Chỉ lấy 100 dòng code gần đây nhất nếu file quá dài
                lines = f.readlines()
                if len(lines) > 200:
                    context = f"CONTEXT FILE (Partial - last 100 lines of {context_file}):\n{''.join(lines[-100:])}\n\n"
                else:
                    context = f"CONTEXT FILE ({context_file}):\n{''.join(lines)}\n\n"
        else:
            print(f"Warning: File {context_file} is blacklisted for security. Ignoring context.")
            
    payload = redact_secrets(context + error_content)
    
    skill_prompt = load_skill_prompt("advisor-debugger")
    prompt = f"{skill_prompt}\n\nERROR DATA:\n{payload}"
    
    print("Calling AI Advisor (Debug Mode via Claude CLI)...")
    feedback = call_claude_cli(prompt, timeout=timeout)
    print("\n--- ADVISOR GUIDANCE ---\n")
    print(feedback)
    print("\n------------------------\n")

def handle_audit_mode(diff_path: str, test_results: str, timeout: int = DEFAULT_TIMEOUTS["audit"]):
    check_budget(diff_path if diff_path else test_results)
    diff_content = ""
    test_content = ""
    
    if diff_path and os.path.exists(diff_path):
        with open(diff_path, 'r', encoding='utf-8') as f:
            diff_content = f.read()
            
    if test_results and os.path.exists(test_results):
        with open(test_results, 'r', encoding='utf-8') as f:
            test_content = f.read()
            
    payload = redact_secrets(f"GIT DIFF / SNAPSHOT:\n{diff_content}\n\nTEST RESULTS:\n{test_content}")
    
    skill_prompt = load_skill_prompt("advisor-auditor")
    prompt = f"{skill_prompt}\n\nPAYLOAD:\n{payload}"
    
    print("Calling AI Advisor (Audit Mode via Claude CLI)...")
    feedback = call_claude_cli(prompt, timeout=timeout)
    print("\n--- ADVISOR AUDIT RESULT ---\n")
    print(feedback)
    print("\n------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Advisor Wrapper (Cost Optimized - Uses installed Claude CLI)")
    parser.add_argument("--mode", choices=["architect", "debug", "audit"], required=True, help="Mode of execution")
    parser.add_argument("--plan_path", help="Path to master_plan.md (for architect mode)")
    parser.add_argument("--error_log", help="Path to error log (for debug mode)")
    parser.add_argument("--context_file", help="Path to relevant code file (for debug mode)")
    parser.add_argument("--diff_path", help="Path to git diff or output snapshot (for audit mode)")
    parser.add_argument("--test_results", help="Path to test results (for audit mode)")
    parser.add_argument("--timeout", type=int, help="Override mode timeout in seconds")
    
    args = parser.parse_args()
    
    timeout = args.timeout or DEFAULT_TIMEOUTS[args.mode]
    if timeout <= 0:
        parser.error("--timeout must be greater than zero")

    if args.mode == "architect":
        handle_architect_mode(args.plan_path, timeout)
    elif args.mode == "debug":
        handle_debug_mode(args.error_log, args.context_file, timeout)
    elif args.mode == "audit":
        handle_audit_mode(args.diff_path, args.test_results, timeout)
