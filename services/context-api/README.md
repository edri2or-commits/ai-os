# Memory Bank Context API

REST API for external LLMs (GPT, Gemini, o1) to load AI Life OS project context in under 30 seconds.

## 🎯 Purpose

Enable external LLMs to access project context without manual copy-paste:
- **Current state**: Phase, progress %, recent changes, next steps
- **Project vision**: Why this exists, what we're building
- **Active protocols**: How we work (Chat→Spec→Change, HITL, etc.)
- **Research corpus**: Deep dives by family (architecture, MCP, ADHD, safety)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd services/context-api
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example config
copy .env.example .env

# Edit .env if needed (default: localhost:8081)
```

### 3. Run Server

```bash
python main.py
```

Server starts on: http://localhost:8081  
API Docs (Swagger): http://localhost:8081/docs

## 📡 API Endpoints

### Health Check
```bash
GET /health
```

Returns service status and Git SHA.

### Current State
```bash
GET /api/context/current-state
```

Returns `01-active-context.md` with metadata:
- Phase name and progress %
- File size, last modified time
- Git commit SHA

### Project Brief
```bash
GET /api/context/project-brief
```

Returns `project-brief.md` (vision, purpose, TL;DR).

### Protocols
```bash
GET /api/context/protocols
```

Extracts PROTOCOLS section from current state.

### Research by Family
```bash
GET /api/context/research/{family}
```

Returns research files matching family keyword:
- `architecture` - Agentic Kernel, Hexagonal design
- `mcp` - Claude Desktop, MCP integration
- `adhd` - Cognitive load, executive function
- `safety` - Security, governance, drift detection
- `infra` - Windows, Docker, n8n
- `memory` - Life Graph, PARA, vector memory
- `meta` - Playbooks, slices, meta-learning

## 🧪 Testing

### Local Testing (curl)

```bash
# Health check
curl http://localhost:8081/health

# Current state
curl http://localhost:8081/api/context/current-state

# Project brief
curl http://localhost:8081/api/context/project-brief

# Protocols
curl http://localhost:8081/api/context/protocols

# Research (architecture)
curl http://localhost:8081/api/context/research/architecture
```

### GPT Integration Test

**Goal:** GPT loads context in < 30 seconds ✅

1. Start a fresh GPT conversation
2. Paste this prompt:

```
Load my AI Life OS project context from http://localhost:8081/api/context/current-state

Then answer these 4 questions:
1. What Phase are we in?
2. What % complete?
3. What was done recently?
4. What are the next step options?
```

3. **Success Criteria:**
   - All 4 answers accurate
   - Response time < 30 seconds
   - No manual context loading needed

## 🔒 Security

### H2 (localhost): No Authentication
- Read-only API
- Localhost binding only
- Safe for local development

### H4 (VPS deployment): API Key Required
- `Authorization: Bearer {API_KEY}` header
- Chat ID whitelist for Telegram integration
- Rate limiting enabled

## 📁 Response Format

All endpoints return:

```json
{
  "content": "markdown content...",
  "metadata": {
    "path": "memory-bank/01-active-context.md",
    "size_bytes": 68432,
    "last_modified": "2025-12-06T00:50:00Z",
    "git_sha": "a1b2c3d",
    "phase": "Phase 2: Architectural Alignment",
    "progress_pct": 72
  }
}
```

## 🛠️ Development

### Auto-Reload

Server runs with `reload=True` - code changes trigger automatic restart.

### API Documentation

Interactive docs: http://localhost:8081/docs

### Error Handling

- `404`: File not found (helpful message with path)
- `500`: Server error (exception details for debugging)

## 📊 Performance

- **Target:** < 30 second onboarding for external LLMs
- **Typical:** 2-5 seconds per endpoint
- **Bottleneck:** LLM processing time, not API latency

## 🗺️ Roadmap Context

This is **H2** in Headless Migration Roadmap:
- ✅ **H1**: MCP→REST Gateway (Gmail POC)
- ⏳ **H2**: Memory Bank API (this service)
- 🔜 **H3**: Telegram Approval Bot (async HITL)
- 🔜 **H4**: VPS Deployment (24/7 uptime)

## 🐛 Troubleshooting

### Server won't start
- Check port 8081 not in use: `netstat -ano | findstr :8081`
- Verify venv activated: `which python` should show venv path

### Endpoints return 404
- Verify Memory Bank files exist:
  - `memory-bank/01-active-context.md`
  - `memory-bank/project-brief.md`
  - `claude-project/research_claude/*.md`

### Git SHA shows "unknown"
- Verify git installed: `git --version`
- Verify in git repo: `git status`

## 📝 License

Private - AI Life OS Project
