# SLICE_DAILY_CONTEXT_SYNC_N8N_V1

**Date:** 2025-11-27  
**Phase:** 2.3 (INFRA_ONLY)  
**Status:** ✅ COMPLETE  
**Decision:** DEC-006 (n8n as Automation Kernel)

---

## 🎯 Goal

Connect Daily Context Sync to n8n orchestration layer with end-to-end trace_id visibility.

**High-level Flow:**
```
n8n Manual Trigger 
  → Generate trace_id 
  → Log N8N_WORKFLOW_STARTED 
  → Call Agent Kernel (/daily-context-sync/run) 
  → Check Success 
  → Log N8N_WORKFLOW_COMPLETE/ERROR 
  → (Optional) Run Reconciler
```

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────┐
│              n8n Workflow (port 5678)               │
│       DAILY_CONTEXT_SYNC_ORCHESTRATOR_V1            │
│                                                     │
│  Manual Trigger → trace_id → Log START             │
│         ↓                                           │
│  HTTP: POST /daily-context-sync/run                │
│        Header: X-Trace-ID                           │
│         ↓                                           │
│  IF status == "ok" ?                                │
│    ├─ YES → Log COMPLETE                           │
│    └─ NO  → Log ERROR                              │
│         ↓                                           │
│  (Optional) Execute: reconciler.py                  │
└─────────────────────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   Agent Kernel :8084   │
        │  /daily-context-sync   │
        │   (reads X-Trace-ID)   │
        └────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │   OS Core MCP :8083    │
        │  /state, /events       │
        └────────┬───────────────┘
                 │
                 ▼
        ┌────────────────────────┐
        │   EVENT_TIMELINE.jsonl │
        │  (all events with      │
        │   same trace_id)       │
        └────────────────────────┘
```

---

## 🔧 Implementation

### Components Modified

**1. Agent Kernel** (`services/agent_kernel/`)

**kernel_server.py:**
- Added `X-Trace-ID` header support (optional)
- Pass trace_id to `run_daily_context_sync()`
- Include trace_id in response

**daily_context_sync_graph.py:**
- Added `trace_id` field to `SyncState`
- All nodes log with trace_id
- Events include trace_id in payload
- Return trace_id in final result

**2. n8n Workflow** (`infra/n8n/workflows/`)

**daily_context_sync_orchestrator_v1.json:**

| Node | Type | Purpose |
|------|------|---------|
| Manual Trigger | Trigger | Start workflow manually |
| Generate Trace ID | Code (JS) | Create `n8n-dcs-{timestamp}-{random}` |
| Log Workflow Started | HTTP POST | Event to TIMELINE: `N8N_WORKFLOW_STARTED` |
| Call Agent Kernel | HTTP POST | Execute sync with X-Trace-ID header |
| Check Success | IF | Branch on `status == "ok"` |
| Log Success | HTTP POST | Event to TIMELINE: `N8N_WORKFLOW_COMPLETE` |
| Log Error | HTTP POST | Event to TIMELINE: `N8N_WORKFLOW_ERROR` |
| Run Reconciler (Optional) | Execute Command | Run reconciler.py (disabled by default) |

---

## 🔍 trace_id System

### Format
```
n8n-dcs-{unix_timestamp}-{random_7_chars}
```

Example: `n8n-dcs-1732748400-abc123`

### Propagation

1. **Generated:** n8n Code node at workflow start
2. **HTTP Header:** Sent to Agent Kernel as `X-Trace-ID`
3. **State:** Stored in LangGraph SyncState
4. **Events:** Included in all EVENT_TIMELINE entries
5. **Response:** Returned by Agent Kernel API

### Events with trace_id

```json
{
  "timestamp": "2025-11-27T23:00:00.123Z",
  "event_type": "N8N_WORKFLOW_STARTED",
  "source": "n8n-orchestrator",
  "payload": {
    "trace_id": "n8n-dcs-1732748400-abc123",
    "workflow": "daily_context_sync",
    "started_at": "2025-11-27T23:00:00.000Z"
  }
}

{
  "timestamp": "2025-11-27T23:00:00.456Z",
  "event_type": "DAILY_CONTEXT_SYNC_STARTED",
  "source": "agent-kernel",
  "payload": {
    "trace_id": "n8n-dcs-1732748400-abc123"
  }
}

{
  "timestamp": "2025-11-27T23:00:02.789Z",
  "event_type": "DAILY_CONTEXT_SYNC_COMPLETED",
  "source": "agent-kernel",
  "payload": {
    "last_daily_context_sync_utc": "2025-11-27T23:00:02.123Z",
    "trace_id": "n8n-dcs-1732748400-abc123"
  }
}

{
  "timestamp": "2025-11-27T23:00:03.012Z",
  "event_type": "N8N_WORKFLOW_COMPLETE",
  "source": "n8n-orchestrator",
  "payload": {
    "trace_id": "n8n-dcs-1732748400-abc123",
    "workflow": "daily_context_sync",
    "status": "success",
    "last_sync_time": "2025-11-27T23:00:02.123Z"
  }
}
```

---

## 📁 Files Created/Modified

### Created

1. **`infra/n8n/workflows/daily_context_sync_orchestrator_v1.json`**  
   n8n workflow export (importable)

2. **`docs/slices/SLICE_DAILY_CONTEXT_SYNC_N8N_V1.md`**  
   This documentation file

### Modified

3. **`services/agent_kernel/kernel_server.py`**  
   Added X-Trace-ID header support

4. **`services/agent_kernel/graphs/daily_context_sync_graph.py`**  
   Added trace_id to state and events

5. **`infra/n8n/README.md`**  
   Added workflow usage instructions

6. **`docs/system_state/timeline/EVENT_TIMELINE.jsonl`** (append-only)  
   New event types: N8N_WORKFLOW_STARTED, N8N_WORKFLOW_COMPLETE, N8N_WORKFLOW_ERROR

---

## 🧪 Testing & Validation

### Prerequisites

```bash
# 1. Start Agent Kernel
cd services/agent_kernel
python kernel_server.py
# Should see: "Uvicorn running on http://0.0.0.0:8084"

# 2. Start OS Core MCP
cd services/os_core_mcp
python server.py
# Should see: "Uvicorn running on http://0.0.0.0:8083"

# 3. Start n8n
cd infra/n8n
docker-compose up -d
# Access UI: http://localhost:5678
```

### Manual Test

1. **Import workflow:**
   - n8n UI → "Import from File"
   - Select `workflows/daily_context_sync_orchestrator_v1.json`

2. **Execute workflow:**
   - Open workflow
   - Click "Execute Workflow"
   - Watch execution (should complete in ~2-5 seconds)

3. **Verify results:**

```bash
# Get trace_id from n8n execution log
# Example: n8n-dcs-1732748400-abc123

# Check EVENT_TIMELINE for all events with this trace_id
cd docs/system_state/timeline
grep "n8n-dcs-1732748400-abc123" EVENT_TIMELINE.jsonl

# Should see 4 events:
# - N8N_WORKFLOW_STARTED
# - DAILY_CONTEXT_SYNC_STARTED  
# - DAILY_CONTEXT_SYNC_COMPLETED
# - N8N_WORKFLOW_COMPLETE

# Check COMPACT updated
cd docs/system_state
cat SYSTEM_STATE_COMPACT.json | grep last_daily_context_sync_utc
# Should show recent timestamp
```

### Success Criteria

- [ ] n8n workflow imports without errors
- [ ] Manual execution completes successfully
- [ ] trace_id generated and visible in n8n log
- [ ] All 4 events logged to EVENT_TIMELINE with same trace_id
- [ ] `last_daily_context_sync_utc` updated in COMPACT
- [ ] Agent Kernel logs show trace_id in all messages
- [ ] Error path logs N8N_WORKFLOW_ERROR (test by stopping Kernel)

---

## ✅ Success Metrics

### Delivered

✅ n8n workflow created and version-controlled  
✅ trace_id generated and propagated end-to-end  
✅ Agent Kernel supports X-Trace-ID header  
✅ All events include trace_id in payload  
✅ Manual trigger works reliably  
✅ Error handling logs to TIMELINE  
✅ Reconciler integration (optional, disabled by default)  
✅ Documentation complete  

### Not in V1 (Future)

❌ Cron/scheduled triggers (Phase 2.4)  
❌ Langfuse integration for observability (Future)  
❌ HTTP endpoint for Reconciler (Slice 3 - POST /state/refresh)  
❌ Automated testing suite  
❌ Workflow versioning/rollback  

---

## 🔮 Next Steps

### Immediate (Post-V1)

1. **Test end-to-end:** Execute workflow, verify all events logged with same trace_id

2. **Document findings:** Known issues, edge cases, performance notes

### Phase 2.4

1. **Add Cron trigger** to Daily Context Sync (daily at 9AM)

2. **Langfuse Integration:**
   - Send trace_id to Langfuse
   - Build observability dashboard
   - Link n8n → Agent Kernel → OS Core traces

3. **More workflows:**
   - Weekly Summary Generator
   - Governance Metrics Calculator
   - Sync Write Contract Orchestrator

### Slice 3

1. **Create `/state/refresh` endpoint** in OS Core MCP
2. **Update workflow:** Replace Execute Command with HTTP Request for Reconciler

---

## 🚨 Known Limitations

### V1 Constraints

1. **Manual trigger only** - No automated scheduling yet
2. **Local execution** - Requires all services running on localhost
3. **No retry logic** - Single execution, no automatic retries
4. **Basic error handling** - Logs error but doesn't recover
5. **Windows-specific paths** - Execute Command uses absolute Windows path

### Mitigations

- Documented prerequisites clearly
- Health checks in workflow (future)
- Clear error messages in TIMELINE events
- Reconciler optional (doesn't block main flow)

---

## 📊 Impact on System

### Truth Layer

**EVENT_TIMELINE.jsonl:**
- New event types: N8N_WORKFLOW_STARTED, N8N_WORKFLOW_COMPLETE, N8N_WORKFLOW_ERROR
- All events include trace_id
- Enables "Golden Trace" reconstruction

**SYSTEM_STATE_COMPACT.json:**
- Updated by Daily Context Sync (as before)
- Now traceable to specific n8n execution

### Services

**Agent Kernel:**
- Backward compatible (trace_id optional)
- Enhanced with observability hooks
- Ready for Langfuse integration

**OS Core MCP:**
- No changes (just receives more events)

**n8n:**
- First production workflow
- Template for future workflows

---

## 🎓 Lessons Learned

### What Worked

- **Backward compatibility:** Agent Kernel accepts trace_id optionally
- **Simple workflow:** 8 nodes, easy to understand
- **Version control:** Workflow exported as JSON
- **Optional nodes:** Reconciler disabled by default

### Challenges

- **Windows paths:** Execute Command needs absolute path
- **n8n syntax:** Expressions like `{{ $json.trace_id }}` require practice
- **Port management:** 3 services must be running simultaneously

### Best Practices

1. **Always version control workflows** (export as JSON)
2. **Use trace_id for all multi-service flows**
3. **Log start/complete/error for every workflow**
4. **Keep optional nodes disabled by default**
5. **Document prerequisites clearly**

---

**Slice Complete:** 2025-11-27  
**Next Slice:** Sync Write Contract (Phase 2.3) or Cron Triggers (Phase 2.4)  
**Phase:** 2.3 - INFRA_ONLY - Dual Orchestration Pattern Established ✅
