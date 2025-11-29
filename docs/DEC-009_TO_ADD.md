

## 2025-11-27 – DEC-009: Slice 2A – Daily Context Sync V1 (Agent Kernel + LangGraph)

**Date:** 2025-11-27  
**Owner:** Or  
**Status:** Approved  

**Context:**

Following DEC-008 (Governance Layer Bootstrap + OS Core MCP Minimal), AI-OS v2 now has:
- Governance Layer structure (stubs ready for measurement)
- OS Core MCP (unified HTTP gateway to State Layer on port 8083)

Next step: First LangGraph-based workflow to demonstrate:
1. Orchestration via LangGraph (graph-based AI workflows)
2. Integration with OS Core MCP (read state, write state, log events)
3. Systematic state updates (rather than ad-hoc file edits)

This is Slice 2A of the v2 architecture - introducing the Agent Kernel as the workflow execution engine.

**Decision:**

**Part A: OS Core MCP Extension - State Update Endpoint**

Add new endpoint to `services/os_core_mcp/server.py`:
- `POST /state/update`
- Input: `{"patch": {...}, "source": "..."}`
- Behavior:
  - Reads SYSTEM_STATE_COMPACT.json
  - Merges patch (top-level keys only in V1)
  - Writes back to file
  - Returns: `{"status": "ok", "state": {...}}`
- Error handling: 404 if file missing, 500 if JSON invalid or write fails

**Part B: Agent Kernel Service - LangGraph Execution Engine**

Create new service at `services/agent_kernel/`:
- FastAPI server on port 8084
- Endpoint: `POST /daily-context-sync/run`
- Implements first LangGraph workflow: `daily_context_sync_graph`

**Graph Structure:**
1. **start_node**:
   - Reads current state: `GET http://localhost:8083/state`
   - Logs event: `POST http://localhost:8083/events` (DAILY_CONTEXT_SYNC_STARTED)

2. **compute_patch**:
   - Generates patch: `{"last_daily_context_sync_utc": "<now UTC ISO8601>"}`

3. **apply_patch**:
   - Applies patch: `POST http://localhost:8083/state/update`
   - Logs event: `POST http://localhost:8083/events` (DAILY_CONTEXT_SYNC_COMPLETED)

**Result:**
```json
{
  "status": "ok",
  "last_sync_time": "2025-11-27T16:02:21Z"
}
```

**Side Effects:**
- `SYSTEM_STATE_COMPACT.json` gets new field: `last_daily_context_sync_utc`
- `EVENT_TIMELINE.jsonl` gets 2 new events (STARTED + COMPLETED)

**Rationale:**

**Why Daily Context Sync?**
1. **Simple but complete**: Demonstrates full graph → OS Core MCP → State Layer flow
2. **Non-destructive**: Only adds/updates a timestamp, doesn't delete anything
3. **Observable**: Clear events in timeline
4. **Extensible**: Foundation for more complex workflows

**Why LangGraph?**
1. **Graph-based orchestration**: Natural fit for multi-step AI workflows
2. **State management**: Built-in state passing between nodes
3. **Integration-ready**: Works with LangChain ecosystem
4. **Observability prep**: Foundation for Langfuse integration (Slice 2B)

**Why Agent Kernel as separate service?**
1. **Separation of concerns**: State Layer (OS Core MCP) ≠ Workflow Engine (Agent Kernel)
2. **Scalability**: Can add more workflows without touching OS Core
3. **Technology isolation**: LangGraph in Agent Kernel, FastAPI in OS Core
4. **Independent deployment**: Can restart Agent Kernel without affecting State access

**Not in Slice 2A:**
- n8n integration (scheduled triggers) → Slice 2B
- Langfuse observability (tracing) → Slice 2B
- Checkpointing/pause/resume → Future
- More complex workflows → Future
- Actual governance measurement implementation → Slice 3+

**Implementation Notes:**

Files created/modified:
- `services/os_core_mcp/server.py` (added POST /state/update endpoint)
- `services/agent_kernel/` (new directory)
- `services/agent_kernel/kernel_server.py` (FastAPI server, port 8084)
- `services/agent_kernel/requirements.txt` (langgraph, fastapi, httpx, etc.)
- `services/agent_kernel/README.md` (documentation)
- `services/agent_kernel/graphs/daily_context_sync_graph.py` (LangGraph implementation)
- `services/agent_kernel/smoke_test_slice_2a.py` (end-to-end test)
- `docs/system_state/SYSTEM_STATE_COMPACT.json` (added last_daily_context_sync_utc field)
- `docs/system_state/timeline/EVENT_TIMELINE.jsonl` (added DAILY_CONTEXT_SYNC_* events)

Smoke test results:
- ✅ OS Core MCP /health: 200 OK
- ✅ Agent Kernel /health: 200 OK
- ✅ Daily Context Sync execution: 200 OK
- ✅ State updated with timestamp
- ✅ Events logged (STARTED + COMPLETED)

Next steps (Slice 2B):
1. n8n workflow to trigger daily context sync on schedule
2. Langfuse integration for workflow tracing
3. Add more workflows (weekly summary, governance metrics calculation)
4. Implement actual governance measurement scripts

**Related:**
- DEC-008: Governance Layer Bootstrap + OS Core MCP Minimal
- DEC-006: n8n as Automation Kernel (integration pending in Slice 2B)
- DEC-007: No Fixed Role Hierarchy (Agent Kernel = tool for all interfaces)
- Phase 2.3: INFRA_ONLY (this is infrastructure work, not live automations yet)

---

