
# Zaki‑OS v1.3.1‑MVP

This repository bootstraps the **Phase One** minimal viable product described in the Zaki‑OS rulebook.

## Quick‑start

```bash
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn pydantic
# Initialise DB
python scripts/agent_runner.py --init-only
# Start dispatcher
uvicorn ui.dispatcher.app:app --reload
```

## Contents

* **docs/** – Knowledge base markdown, onboarding, plans, reports  
* **scripts/** – Helper utilities (agent runner, port guard, indexer)  
* **sql/** – Schema definitions & migrations  
* **ui/** – Dispatcher (FastAPI web app) and Docs UI stub  
