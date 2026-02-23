# Prompt-Driven AI Agent (GitHub-ready)

A production-style starter project for a **prompt-driven AI agent** that supports:

- Multi-step reasoning workflows
- Controlled backend tool execution
- Modular architecture separating AI reasoning from backend logic
- JSON + REST interfaces for integration
- A lightweight frontend connected to the backend API

## Architecture

```text
app/main.py        -> FastAPI REST entrypoints + serves frontend
app/agent.py       -> Orchestration: plan -> execute -> summarize
app/llm.py         -> LLM abstraction layer (API + local fallback)
app/tools.py       -> Tool registry and controlled tool execution
app/schemas.py     -> Request/response and planning models
app/static/        -> Browser UI wired to POST /agent/run
```

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Port Link

- Frontend: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Example API Call

```bash
curl -X POST http://127.0.0.1:8000/agent/run \
  -H 'content-type: application/json' \
  -d '{
    "prompt": "Please add 12 and 30 then provide a quick summary",
    "context": {"request_id": "demo-001"}
  }'
```

## Optional LLM API Configuration

By default, the project runs in local fallback mode (no API calls). To use a real LLM endpoint:

```bash
export AI_API_URL="https://your-llm-provider/v1/chat/completions"
export AI_API_KEY="<secret>"
export AI_MODEL="gpt-4o-mini"
```

The API expects an OpenAI-compatible `chat/completions` JSON response format.

## Run Tests

```bash
pytest -q
```
