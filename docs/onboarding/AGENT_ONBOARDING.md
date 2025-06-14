
# AGENT_ONBOARDING.md

**Version**: 1.0.0  
**Date**: 2025-06-14  
**Category**: Onboarding  
**Status**: Active  
**Last Updated**: 1750000001  

## Welcome

You are joining the Zaki‑OS multi‑agent ecosystem.  
**Read this document before executing any task.**

### Identity
Provide the following JSON to the dispatcher when you first connect:

```json
{
  "friendly_name": "<FirstNameOnly>",
  "agent_id": "<app>-<model>-<version>-<epoch>--<shortid>",
  "model_type": "<llm|tool|human>",
  "source_platform": "<cursor|browser|api|cli>",
  "accepted_rules_version": "1.3.0"
}
```

### Initial Checklist
1. Log your onboarding acknowledgement (Unix time).
2. Verify connectivity to the Dispatcher API: `POST /api/v1/agent/heartbeat`
3. Pull your first task from `/tasks/inbox` or the API endpoint.
4. Generate `PLAN.md` **before** taking action.

### Golden Rules
* Only operate within your declared scope.
* Always check the _Service Registry_ **before** starting or installing anything.
* Never assign a network port without verifying availability (`scripts/port_guard.py`).

---
