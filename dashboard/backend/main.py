import asyncio
import os
import json
import argparse
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sse_starlette.sse import EventSourceResponse
from parser import get_current_phase

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--project_dir", default=None)
args, _ = arg_parser.parse_known_args()
PROJECT_DIR = args.project_dir or os.environ.get("PROJECT_DIR", ".")

app = FastAPI(title="Hybrid Workflow Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
app.mount("/static", StaticFiles(directory=frontend_path), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_file = os.path.join(frontend_path, 'index.html')
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            return f.read()
    return "Frontend not built yet."

@app.get("/api/stream")
async def message_stream(request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            current_state = get_current_phase(PROJECT_DIR)
            yield {
                "event": "update",
                "data": json.dumps(current_state)
            }
            await asyncio.sleep(2)
    return EventSourceResponse(event_generator())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
