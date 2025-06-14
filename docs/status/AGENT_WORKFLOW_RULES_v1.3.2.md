
# 🔁 Agent Workflow and Rules for Zaki-OS

**Version**: 1.3.2  
**Status**: Active  
**Last Updated**: 2025-06-14 (Unix: 1750000000)  
**ZAKI_RULES_VERSION**: 1.3.2  

---

## 🎯 Purpose

To define a complete execution, logging, dispatching, and learning lifecycle for AI agents and models working within Zaki-OS. Includes:
- Task planning, completion, feedback
- Dispatching & memory augmentation (RAG)
- Agent-to-agent coordination (A2A)
- Context compliance (MCP)
- Placeholder & mockup management
- Completion tracking and milestone audits

---

## 📈 Subcomponent Completion Tracking

All major module components must include a completion report:
```yaml
module: rag_vector_store
percent_complete: 80
status: working
notes: basic vector interface built; missing loader & persistence
```
Reports go in `/docs/status/progress_<component>.md` or to the dispatcher log under `completion_status`.

---

## 🧩 Placeholder & Mockup Registry

To prevent unfinished code from being forgotten or deployed:
- Every file or UI that is a stub or mock must be registered
- The `docs/status/placeholders.md` file should include:
  ```
  - [ ] vector_store.py  – no embedding logic yet
  - [ ] index-lessons.py – does not call actual vector DB
  - [ ] app.py UI – static dropdown only
  - [ ] sidebar.json – regenerated manually
  ```
- Dispatcher will highlight tasks linked to unresolved placeholders

---

## 🧠 RAG, MCP, A2A Enforcement (v1.3.2 Update)

### RAG Module (core/rag/)
- Inject top-N relevant lessons into PLAN.md prompts
- `vector_store.py`, `loader.py`, and `index_lessons.py` handle indexing

### A2A Module (core/a2a/)
- Subtask delegation across agents
- Supports `parent_task_id` and return routing

### MCP Module (core/mcp/)
- Context wrapper schema to enforce structured prompts
- Validates ruleset version, agent identity, and input schema

---
