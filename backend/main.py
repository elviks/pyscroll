from tips import TIPS
from typing import Optional
import json
import os
import subprocess
import sys
import tempfile
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()


try:
    from groq import Groq
except ImportError:  # pragma: no cover
    Groq = None

app = FastAPI(title="PyScroll API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_PROMPT = (
    "You are a strict Python coding tutor."
    "You ONLY answer questions related to the Python programming language, "
    "its standard library, common libraries, and Python-specific programming concepts. "
    "If the user asks about anything unrelated to Python, politely refuse and "
    "redirect them to a Python topic. Be concise, precise, and friendly. "
    "When sharing code, prefer small, runnable examples in markdown code blocks."
    "AND MOST IMPORTANT PART: answer in short and simple way."
)


@app.get("/api/tips")
def get_tips() -> dict:
    """Return the static feed of Python tips."""
    return {"tips": TIPS}


@app.get("/api/tips/{tip_id}")
def get_tip(tip_id: int) -> dict:
    tip = next((t for t in TIPS if t["id"] == tip_id), None)
    if tip is None:
        raise HTTPException(status_code=404, detail="tip not found")
    return {"tip": tip}


class ChatRequest(BaseModel):
    message: str
    history: Optional[list[dict]] = None


class RunRequest(BaseModel):
    code: str


@app.post("/api/run")
def run_code(req: RunRequest):
    """Execute a snippet of Python and return stdout/stderr. Local dev sandbox."""
    if not req.code.strip():
        return {"stdout": "", "stderr": "Nothing to run.", "returncode": 1}
    with tempfile.TemporaryDirectory() as workdir:
        script = os.path.join(workdir, "main.py")
        with open(script, "w", encoding="utf-8") as f:
            f.write(req.code)
        try:
            proc = subprocess.run(
                [sys.executable, "-u", script],
                capture_output=True,
                text=True,
                timeout=8,
                cwd=workdir,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            )
        except subprocess.TimeoutExpired as timeout:
            return {
                "stdout": (timeout.stdout or "")[-2000:],
                "stderr": "⏱️ Timed out after 8 seconds.",
                "returncode": -1,
            }
        if proc.returncode == 0:
            return {"stdout": proc.stdout[-4000:], "stderr": "", "returncode": 0}
        return {
            "stdout": proc.stdout[-2000:],
            "stderr": proc.stderr[-4000:],
            "returncode": proc.returncode,
        }


@app.post("/api/chat")
async def chat(req: ChatRequest):
    """Stream a Python tutor response from Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        def no_key():
            yield 'data: {"content": "⚠️ GROQ_API_KEY not set on the backend. Add it to backend/.env and restart."}\n\n'
            yield 'data: {"done": true}\n\n'
        return StreamingResponse(no_key(), media_type="text/event-stream")
    if Groq is None:  # pragma: no cover
        def no_groq():
            yield 'data: {"content": "groq package is not installed on the backend."}\n\n'
            yield 'data: {"done": true}\n\n'
        return StreamingResponse(no_groq(), media_type="text/event-stream")

    client = Groq(api_key=api_key)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in (req.history or [])[-12:]:
        role = turn.get("role")
        content = turn.get("content")
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})

    if messages[-1]["role"] != "user" or messages[-1]["content"] != req.message:
        messages.append({"role": "user", "content": req.message})

    model = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")

    async def event_stream():
        try:
            stream = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.4,
                max_tokens=1024,
                stream=True,
            )
            for chunk in stream:
                delta = chunk.choices[0].delta.content if chunk.choices else None
                if delta:
                    payload = json.dumps({"content": delta})
                    yield f"data: {payload}\n\n"
        except Exception as exc:
            payload = json.dumps(
                {"content": f"Error talking to the tutor: {exc}"})
            yield f"data: {payload}\n\n"
        yield 'data: {"done": true}\n\n'

    return StreamingResponse(event_stream(), media_type="text/event-stream")
