from src.utils.llm import call_llm
from src.state import write_run_file

SYSTEM_PROMPT = """You are a meticulous AI Researcher.
Your job is to investigate the given task and produce comprehensive research materials.
Highlight dependencies, files involved, libraries required, architectural considerations, and potential pitfalls.
Provide your final output in clear Markdown format. Do not use placeholders."""

def run_phase(run_id, state, config):
    task = state["task"]
    print(f"[*] Starting Phase 1 (Research & Prepare) for task: {task[:50]}...")
    
    prompt = f"Please research and prepare comprehensive materials for the following task:\n\n{task}"
    
    provider = config["provider"]
    model_name = config["name"]
    
    research_notes = call_llm(provider, model_name, prompt, SYSTEM_PROMPT)
    
    # Save the output file
    file_path = write_run_file(run_id, "research_notes.md", research_notes)
    
    # Update state
    state["history"]["1_research"] = "research_notes.md"
    print(f"[+] Phase 1 Complete. Output written to: {file_path}")
    return research_notes
