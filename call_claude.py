import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

prompt_file = "d:\\TestProject\\IndependentAIWorkflow\\temp_architect_prompt_v2.txt"
with open(prompt_file, 'r', encoding='utf-8') as f:
    prompt = f.read()

cmd = ['claude', '-p', prompt, '--print']
result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

with open("d:\\TestProject\\IndependentAIWorkflow\\temp_architect_plan.txt", "w", encoding="utf-8") as f:
    f.write(result.stdout)
    f.write(result.stderr)
