import argparse
import sys
import os
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

def redact_secrets(text: str) -> str:
    """Xóa các chuỗi nhạy cảm như API Keys, Passwords ra khỏi text."""
    text = re.sub(r'(sk-[a-zA-Z0-9]{20,})', '[REDACTED_API_KEY]', text)
    text = re.sub(r'(password|passwd|pwd)=([^\s;&]+)', r'\1=[REDACTED_PASSWORD]', text, flags=re.IGNORECASE)
    return text

def is_safe_path(filepath: str) -> bool:
    """Kiểm tra đường dẫn không thuộc danh sách đen (Blacklist)."""
    blacklist = ['.env', 'secrets/', 'credentials.json', 'keys/']
    for bad in blacklist:
        if bad in filepath:
            return False
    return True

def call_claude_cli(prompt: str) -> str:
    """Gọi Claude CLI cục bộ (Công cụ cài sẵn của máy). Chú ý tốn API Credits."""
    try:
        temp_file = "temp_advisor_prompt.txt"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(prompt)
        
        cmd = ['claude', '-p', prompt, '--print']
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if os.path.exists(temp_file):
            os.remove(temp_file)
            
        return result.stdout.strip()
    except Exception as e:
        return f"ERROR_CALLING_ADVISOR_CLI: {str(e)}"

def handle_architect_mode(plan_path: str):
    if not os.path.exists(plan_path):
        print(f"Error: Plan file not found at {plan_path}")
        sys.exit(1)
        
    with open(plan_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    content = redact_secrets(content)
    
    prompt = (
        "You are an Elite Principal Software Architect. Review the following architecture plan.\n"
        "Do not write code. Identify coupling issues, missing edge cases, architectural smells, and security risks.\n"
        "Provide concise, critical feedback.\n\n"
        f"PLAN CONTENT:\n{content}"
    )
    
    print("Calling AI Advisor (Architect Mode via Claude CLI)...")
    feedback = call_claude_cli(prompt)
    print("\n--- ADVISOR FEEDBACK ---\n")
    print(feedback)
    print("\n------------------------\n")

def handle_debug_mode(error_log_path: str, context_file: str):
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
    
    prompt = (
        "You are an Expert Debugger (Advisor). The Worker AI encountered a critical error.\n"
        "Analyze the stack trace and context provided. Identify the ROOT CAUSE and provide a STEP-BY-STEP guide on how to fix it.\n"
        "Do not write the full code, just provide the precise guidance.\n\n"
        f"ERROR DATA:\n{payload}"
    )
    
    print("Calling AI Advisor (Debug Mode via Claude CLI)...")
    feedback = call_claude_cli(prompt)
    print("\n--- ADVISOR GUIDANCE ---\n")
    print(feedback)
    print("\n------------------------\n")

def handle_audit_mode(diff_path: str, test_results: str):
    diff_content = ""
    test_content = ""
    
    if diff_path and os.path.exists(diff_path):
        with open(diff_path, 'r', encoding='utf-8') as f:
            diff_content = f.read()
            
    if test_results and os.path.exists(test_results):
        with open(test_results, 'r', encoding='utf-8') as f:
            test_content = f.read()
            
    payload = redact_secrets(f"GIT DIFF / SNAPSHOT:\n{diff_content}\n\nTEST RESULTS:\n{test_content}")
    
    prompt = (
        "You are a Strict Security and Code Quality Auditor (Advisor).\n"
        "Review the diff and test results. Check for vulnerabilities, race conditions, memory leaks, and logic flaws.\n"
        "If 100% production-ready, conclude with EXACTLY: 'STATUS: APPROVED'.\n"
        "If issues exist, conclude with EXACTLY: 'STATUS: REJECTED' and provide a defect report.\n\n"
        f"PAYLOAD:\n{payload}"
    )
    
    print("Calling AI Advisor (Audit Mode via Claude CLI)...")
    feedback = call_claude_cli(prompt)
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
    
    args = parser.parse_args()
    
    if args.mode == "architect":
        handle_architect_mode(args.plan_path)
    elif args.mode == "debug":
        handle_debug_mode(args.error_log, args.context_file)
    elif args.mode == "audit":
        handle_audit_mode(args.diff_path, args.test_results)
