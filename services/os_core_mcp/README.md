# OS Core MCP

**Version:** 0.1.0 (Minimal - Bootstrap V1)  
**Port:** 8083  
**Purpose:** Unified HTTP gateway to AI-OS State Layer

---

## Overview

OS Core MCP is the "operating system core" - a single, uniform interface for reading and writing AI-OS state.

Instead of having multiple agents directly manipulate JSON files, they go through OS Core MCP, which:
- Provides consistent API
- Handles errors gracefully
- Logs all state access
- Enables future features (caching, validation, access control)

---

## Architecture

```
┌─────────────────────────────────────────┐
│  AI Agents (Claude, GPT, n8n, etc.)    │
└─────────────┬───────────────────────────┘
              │ HTTP API
              ▼
┌─────────────────────────────────────────┐
│         OS Core MCP (Port 8083)         │
│  ┌───────────────────────────────────┐  │
│  │  GET  /state      → read state    │  │
│  │  GET  /services   → read services │  │
│  │  POST /events     → append event  │  │
│  └───────────────────────────────────┘  │
└─────────────┬───────────────────────────┘
              │ File I/O
              ▼
┌─────────────────────────────────────────┐
│         State Layer (JSON files)        │
│  - SYSTEM_STATE_COMPACT.json            │
│  - SERVICES_STATUS.json                 │
│  - EVENT_TIMELINE.jsonl                 │
└─────────────────────────────────────────┘
```

---

## API Endpoints

### `GET /` - Root / Health Check
Returns service info and available endpoints.

**Response:**
```json
{
  "ok": true,
  "service": "AI-OS Core MCP",
  "version": "0.1.0",
  "endpoints": { ... }
}
```

### `GET /health` - Detailed Health Check
Returns service status and file existence checks.

### `GET /state` - Read System State
Returns `SYSTEM_STATE_COMPACT.json` as JSON object.

**Path:** `docs/system_state/SYSTEM_STATE_COMPACT.json`

**Response:** Full system state JSON

**Errors:**
- 404: File not found
- 500: Invalid JSON or read error

### `GET /services` - Read Services Status
Returns `SERVICES_STATUS.json` as JSON object.

**Path:** `docs/system_state/registries/SERVICES_STATUS.json`

**Response:** Services status JSON

**Errors:**
- 404: File not found
- 500: Invalid JSON or read error

### `POST /events` - Append Event
Appends a new event to `EVENT_TIMELINE.jsonl`.

**Path:** `docs/system_state/timeline/EVENT_TIMELINE.jsonl`

**Request Body:**
```json
{
  "event_type": "info",
  "payload": {
    "message": "Something happened",
    "details": { ... }
  },
  "source": "architect"
}
```

**Response:**
```json
{
  "ok": true,
  "message": "Event appended successfully",
  "event": {
    "timestamp": "2025-11-27T10:30:00Z",
    "event_type": "info",
    "source": "architect",
    "payload": { ... }
  }
}
```

**Notes:**
- Timestamp is auto-generated (UTC ISO8601)
- File is created if it doesn't exist
- Each event is one line in JSONL format

---

## Running the Server

### Development Mode
```bash
cd services/os_core_mcp
python server.py
```

Server will start on `http://localhost:8083`

### Production Mode (with uvicorn)
```bash
uvicorn services.os_core_mcp.server:app --host 0.0.0.0 --port 8083
```

---

## File Paths (Relative to Repo Root)

All paths are relative to the repo root (`C:\Users\edri2\Desktop\AI\ai-os`):

- System State: `docs/system_state/SYSTEM_STATE_COMPACT.json`
- Services Status: `docs/system_state/registries/SERVICES_STATUS.json`
- Event Timeline: `docs/system_state/timeline/EVENT_TIMELINE.jsonl`

The server automatically resolves paths using `Path(__file__).parent.parent.parent`.

---

## Integration

### Claude Desktop MCP Config
To use with Claude Desktop, add to your MCP config:

```json
{
  "os-core": {
    "command": "python",
    "args": ["services/os_core_mcp/server.py"],
    "env": {}
  }
}
```

### GPT Custom Action
To use with GPT Custom Actions, configure:
- Base URL: `http://localhost:8083` (or ngrok tunnel)
- Endpoints: `/state`, `/services`, `/events`

---

## Error Handling

- **File not found:** 404 error with clear message
- **Invalid JSON:** 500 error, file is not modified
- **Write errors:** 500 error, operation is rolled back if possible
- All errors are logged to console

---

## Future Enhancements (Post-Bootstrap)

1. **Validation:** Validate JSON schemas before writing
2. **Caching:** Cache frequently-read files in memory
3. **Access Control:** Different read/write permissions per agent
4. **Webhooks:** Notify agents when state changes
5. **Metrics:** Track API usage, response times

---

## Related

- **State Layer Design:** `docs/SNAPSHOT_LAYER_DESIGN.md`
- **Governance Layer:** `governance/README.md`
- **Decision:** See `docs/DECISIONS_AI_OS.md` DEC-008 (OS Core MCP + Governance Bootstrap)

---

**Status:** Bootstrap V1 - Functional but minimal. Ready for immediate use.
