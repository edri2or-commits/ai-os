# AI-OS Agent Kernel

**Version:** 0.1.0 (Slice 2A - Daily Context Sync v1)  
**Port:** 8084  
**Purpose:** LangGraph-based workflow execution engine for AI-OS

---

## Overview

Agent Kernel is the LangGraph execution engine for AI-OS. It provides HTTP endpoints to trigger complex AI workflows built with LangGraph.

Currently implements:
- **Daily Context Sync** - Updates system state timestamp and logs sync events

---

## Architecture

```
┌──────────────────────────────────────┐
│   HTTP Clients (Claude, GPT, n8n)   │
└──────────────┬───────────────────────┘
               │ POST /daily-context-sync/run
               ▼
┌──────────────────────────────────────┐
│   Agent Kernel (Port 8084)           │
│   ┌────────────────────────────────┐ │
│   │  LangGraph Workflows           │ │
│   │  - daily_context_sync_graph    │ │
│   └────────────┬───────────────────┘ │
└────────────────┼─────────────────────┘
                 │ HTTP API calls
                 ▼
┌──────────────────────────────────────┐
│   OS Core MCP (Port 8083)            │
│   - GET /state                       │
│   - POST /state/update               │
│   - POST /events                     │
└──────────────────────────────────────┘
```

---

## Workflows

### Daily Context Sync

**Endpoint:** `POST /daily-context-sync/run`

**Graph:** `graphs/daily_context_sync_graph.py`

**Flow:**
1. **start_node**: Read current state from OS Core MCP + log STARTED event
2. **compute_patch**: Generate patch with `last_daily_context_sync_utc` timestamp
3. **apply_patch**: Apply patch via OS Core MCP + log COMPLETED event

**Result:**
```json
{
  "status": "ok",
  "last_sync_time": "2025-11-27T15:30:00Z",
  "last_daily_context_sync_utc": "2025-11-27T15:30:00Z"
}
```

**Side Effects:**
- Updates `SYSTEM_STATE_COMPACT.json` with `last_daily_context_sync_utc` field
- Adds 2 events to `EVENT_TIMELINE.jsonl`:
  - `DAILY_CONTEXT_SYNC_STARTED`
  - `DAILY_CONTEXT_SYNC_COMPLETED`

---

## Running the Server

### Install Dependencies

```bash
cd services/agent_kernel
pip install -r requirements.txt
```

### Start Server

```bash
python kernel_server.py
```

Server will start on `http://localhost:8084`

### Test Endpoint

```bash
curl -X POST http://localhost:8084/daily-context-sync/run
```

---

## Dependencies

- **langgraph** - Graph-based AI workflow framework
- **langchain** - LangChain core library (dependency of langgraph)
- **fastapi** - HTTP server framework
- **uvicorn** - ASGI server
- **httpx** - Async HTTP client (for calling OS Core MCP)
- **pydantic** - Data validation

---

## File Structure

```
services/agent_kernel/
├── kernel_server.py           # FastAPI server
├── requirements.txt           # Python dependencies
├── graphs/                    # LangGraph workflows
│   ├── __init__.py
│   └── daily_context_sync_graph.py
└── README.md                  # This file
```

---

## Integration with OS Core MCP

Agent Kernel depends on OS Core MCP running on port 8083:

**Required OS Core MCP endpoints:**
- `GET /state` - Read system state
- `POST /state/update` - Update system state with patch
- `POST /events` - Append event to timeline

Make sure OS Core MCP is running before starting Agent Kernel.

---

## Future Enhancements (Post-Slice 2A)

1. **More Workflows**:
   - Weekly summary generation
   - Governance metrics calculation
   - Automated state validation

2. **Checkpointing**:
   - Add LangGraph memory/checkpointing for long-running workflows
   - Enable pause/resume capability

3. **n8n Integration**:
   - Trigger workflows via n8n schedules
   - Webhook endpoints for n8n callbacks

4. **Observability**:
   - Langfuse integration for workflow tracing
   - Metrics collection and dashboards

---

## Related

- **OS Core MCP:** `services/os_core_mcp/` (port 8083)
- **Governance Layer:** `governance/` (measurement scripts)
- **State Layer:** `docs/system_state/` (source of truth)
- **Decision:** See `docs/DECISIONS_AI_OS.md` (Slice 2A decision)

---

**Status:** Slice 2A complete - First LangGraph workflow operational
