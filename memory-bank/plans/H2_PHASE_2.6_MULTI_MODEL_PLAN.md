# H2 Phase 2.6: Multi-Model Orchestration Implementation Plan

**Created:** 2025-12-08  
**Status:** PLANNING (Not Started)  
**Research Basis:** Multi-model orchestration research (2025-12-08)  
**Expected Duration:** 7-10 days (broken into slices)

---

## 🎯 VISION: What We're Building

**End State:**
```
User (Telegram/Claude Desktop/Web)
    ↓
n8n (routing logic)
    ↓
LiteLLM Proxy :4000 (unified gateway)
    ├─ GPT-4 (reasoning)
    ├─ Claude (long context)
    └─ Gemini (speed + cost)
    ↓
Langfuse V3 (auto-logging)
    ↓
Redis Streams (events)
    ↓
Observer Agent (reconciliation)
    ↓
Git Truth Layer (commits)
```

**Value Proposition:**
- **Multi-model freedom:** Use best model for each task
- **Cost optimization:** Gemini = 1/20th of GPT-4 cost
- **Reliability:** Automatic fallbacks (GPT→Claude→Gemini)
- **Observability:** All calls logged in Langfuse
- **State sync:** Event sourcing → Git reconciliation
- **Budget safety:** Per-model spending limits

---

## 📊 CURRENT STATE (Before We Start)

### Infrastructure (GCP VPS - Already Running)
- ✅ n8n :5678 (Docker)
- ✅ Langfuse V3 :3000 (Docker)
- ✅ Qdrant :6333 (Docker)
- ✅ PostgreSQL :5432 (Docker)
- ✅ Redis :6379 (Docker)
- ✅ Caddy (reverse proxy + SSL)

### API Keys (All Available)
- ✅ `OPENAI_API_KEY` (GPT-4)
- ✅ `ANTHROPIC_API_KEY` (Claude)
- ✅ `GOOGLE_API_KEY` (Gemini)
- ✅ Location: `C:\Users\edri2\Desktop\AI\ai-os\vps.env`

### What's Missing
- ❌ LiteLLM (multi-model gateway)
- ❌ Event streaming infrastructure
- ❌ Telegram bot (async approvals)
- ❌ n8n workflows for multi-model routing

---

## 🗺️ IMPLEMENTATION PHASES

### Phase 1: Foundation (Days 1-3)
**Goal:** Add LiteLLM, establish unified API endpoint

**Slices:**
- Slice 1: LiteLLM setup + basic config
- Slice 2: Langfuse integration
- Slice 3: Test all 3 models through LiteLLM

### Phase 2: n8n Integration (Days 4-5)
**Goal:** Multi-model workflows in n8n

**Slices:**
- Slice 4: Create routing workflow (task → model selection)
- Slice 5: Add fallback logic
- Slice 6: Test end-to-end (Telegram → n8n → LiteLLM → response)

### Phase 3: Event Sourcing (Days 6-7)
**Goal:** State synchronization via Redis Streams

**Slices:**
- Slice 7: Event schema + Redis Streams setup
- Slice 8: Observer Agent (Python script)
- Slice 9: Git reconciliation loop

### Phase 4: Production Hardening (Days 8-10)
**Goal:** Backups, monitoring, reliability

**Slices:**
- Slice 10: Automated backups to GCS
- Slice 11: Cloud Monitoring alerts
- Slice 12: Load testing + performance tuning

---

## 📝 DETAILED SLICE BREAKDOWN

---

### **SLICE 1: LiteLLM Setup + Basic Config** ⏱️ 60 min

**Goal:** Add LiteLLM to docker-compose, verify it can route to all 3 models

**Prerequisites:**
- ✅ API keys in vps.env
- ✅ Docker Compose knowledge
- ✅ PostgreSQL running (reuse existing)

**Files to Create:**
1. `litellm-config.yaml` (model definitions, fallbacks)
2. Update `docker-compose.vps.yml` (add litellm service)
3. Create `litellm` database in PostgreSQL

**Files to Edit:**
- `docker-compose.vps.yml` (add service)
- `vps.env` (add LITELLM_MASTER_KEY, LITELLM_SALT_KEY)

**Steps:**
1. Read vps.env to get API keys ✅ (already done)
2. Create litellm-config.yaml with model_list:
   - gpt-4: openai/gpt-4-turbo
   - claude-3: anthropic/claude-3-5-sonnet-20241022
   - gemini-2: gemini/gemini-2.0-flash-exp
3. Add LiteLLM service to docker-compose.vps.yml:
   - Image: ghcr.io/berriai/litellm:main-stable
   - Ports: 4000:4000, 4001:4001
   - Environment: DATABASE_URL, REDIS_HOST, API keys
   - Memory limit: 384MB
4. Create PostgreSQL database:
   ```sql
   CREATE DATABASE litellm;
   ```
5. Start LiteLLM:
   ```bash
   docker compose up -d litellm
   ```
6. Verify logs:
   ```bash
   docker logs litellm
   ```

**Success Criteria:**
- ✅ LiteLLM container running (docker ps)
- ✅ Health check passes: `curl http://localhost:4001/health/readiness`
- ✅ Models endpoint works: `curl http://localhost:4000/v1/models`
- ✅ Response includes: ["gpt-4", "claude-3", "gemini-2"]

**Testing Commands:**
```bash
# Check container
docker ps | grep litellm

# Health check
curl http://localhost:4001/health/readiness

# List models
curl http://localhost:4000/v1/models

# Test GPT-4 call
curl http://localhost:4000/v1/chat/completions \
  -H "Authorization: Bearer YOUR_LITELLM_MASTER_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**Rollback Plan:**
- If fails: `docker compose down litellm`
- Remove litellm service from docker-compose.vps.yml
- Drop database: `DROP DATABASE litellm;`

**Expected Errors & Solutions:**
| Error | Cause | Solution |
|-------|-------|----------|
| "DATABASE_URL not found" | Missing env var | Add to vps.env |
| "Invalid API key" | Wrong format | Check OpenAI key starts with sk- |
| Port 4000 in use | Conflict | Change to 4001:4000 |
| Out of memory | e2-medium limit | Reduce num_workers to 1 |

**Output:**
- LiteLLM running on port 4000
- Unified API endpoint ready
- All 3 models accessible

---

### **SLICE 2: Langfuse Integration** ⏱️ 30 min

**Goal:** Auto-log all LiteLLM calls to Langfuse V3

**Prerequisites:**
- ✅ Slice 1 complete (LiteLLM running)
- ✅ Langfuse V3 running (already done)

**Files to Edit:**
1. `litellm-config.yaml` (add success_callback)
2. `vps.env` (add Langfuse keys if missing)

**Steps:**
1. Get Langfuse API keys:
   - Login to https://cloud.langfuse.com (or self-hosted)
   - Settings → API Keys
   - Copy PUBLIC_KEY and SECRET_KEY
2. Add to vps.env:
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```
3. Update litellm-config.yaml:
   ```yaml
   litellm_settings:
     success_callback: ["langfuse"]
   ```
4. Restart LiteLLM:
   ```bash
   docker compose restart litellm
   ```
5. Make test call (use curl from Slice 1)
6. Check Langfuse dashboard for trace

**Success Criteria:**
- ✅ Trace appears in Langfuse within 10 seconds
- ✅ Trace shows: model, tokens, cost, latency
- ✅ Session ID matches (if provided)

**Testing:**
1. Call LiteLLM API (curl command from Slice 1)
2. Go to Langfuse dashboard
3. Navigate to "Traces"
4. Find trace with model="gpt-4"
5. Verify fields:
   - Input tokens
   - Output tokens
   - Cost (in USD)
   - Latency (ms)

**Rollback Plan:**
- Remove `success_callback` line from litellm-config.yaml
- Restart LiteLLM

**Output:**
- All LiteLLM calls automatically logged
- Cost tracking per model
- Performance monitoring ready

---

### **SLICE 3: Test All 3 Models** ⏱️ 30 min

**Goal:** Verify GPT-4, Claude, Gemini all work through LiteLLM

**Prerequisites:**
- ✅ Slice 2 complete (Langfuse working)

**Test Matrix:**
| Model | Test Query | Expected Behavior | Success Metric |
|-------|-----------|-------------------|----------------|
| gpt-4 | "Explain quantum computing in 10 words" | Returns concise answer | Response length < 20 words |
| claude-3 | "Summarize this 10K char text: [...]" | Handles long context | No truncation error |
| gemini-2 | "What's 2+2?" | Fast, cheap response | Latency < 500ms, cost < $0.001 |

**Steps:**
1. Test GPT-4:
   ```bash
   curl http://localhost:4000/v1/chat/completions \
     -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
     -d '{"model":"gpt-4","messages":[{"role":"user","content":"Test"}]}'
   ```
2. Test Claude:
   ```bash
   curl http://localhost:4000/v1/chat/completions \
     -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
     -d '{"model":"claude-3","messages":[{"role":"user","content":"Test"}]}'
   ```
3. Test Gemini:
   ```bash
   curl http://localhost:4000/v1/chat/completions \
     -H "Authorization: Bearer $LITELLM_MASTER_KEY" \
     -d '{"model":"gemini-2","messages":[{"role":"user","content":"Test"}]}'
   ```
4. Check Langfuse: 3 traces, different models, different costs

**Success Criteria:**
- ✅ All 3 models return valid responses
- ✅ No API errors (401, 429, 500)
- ✅ Langfuse shows 3 separate traces
- ✅ Cost tracking accurate (GPT > Claude > Gemini)

**Troubleshooting:**
| Error | Model | Fix |
|-------|-------|-----|
| 401 Unauthorized | Any | Check API key in vps.env |
| 429 Rate Limit | GPT-4 | Add retry logic in config |
| 400 Bad Request | Gemini | Add `drop_params: true` to config |
| Timeout | Claude | Increase request_timeout to 600s |

**Output:**
- Proof that all 3 models work
- Baseline latency/cost metrics
- Confidence to build n8n workflows

---

### **SLICE 4: n8n Routing Workflow** ⏱️ 90 min

**Goal:** Create n8n workflow that routes tasks to best model

**Prerequisites:**
- ✅ Slice 3 complete (all models tested)
- ✅ n8n running and accessible

**Workflow Logic:**
```
Webhook Trigger (receive task)
    ↓
Function Node: Analyze task
    ├─ IF contains "reason", "analyze", "complex" → route = "gpt-4"
    ├─ IF text length > 50,000 chars → route = "claude-3"
    └─ ELSE → route = "gemini-2"
    ↓
HTTP Request Node: Call LiteLLM
    - URL: http://litellm:4000/v1/chat/completions
    - Body: {"model": "{{ $json.route }}", "messages": [...]}
    ↓
Function Node: Format response
    ↓
Respond to Webhook
```

**Files to Create:**
- `workflows/litellm-router.json` (n8n workflow export)

**Steps:**
1. Open n8n UI (http://n8n.YOUR_DOMAIN.com)
2. Create new workflow
3. Add Webhook Trigger:
   - Path: /litellm-route
   - Method: POST
4. Add Function Node (Task Analyzer):
   ```javascript
   const task = $input.item.json.task;
   const keywords = ["reason", "analyze", "explain", "complex"];
   
   if (keywords.some(k => task.toLowerCase().includes(k))) {
     return { route: "gpt-4", reason: "Complex reasoning" };
   } else if (task.length > 50000) {
     return { route: "claude-3", reason: "Long context" };
   } else {
     return { route: "gemini-2", reason: "Simple/fast" };
   }
   ```
5. Add HTTP Request Node:
   - URL: http://litellm:4000/v1/chat/completions
   - Auth: Header (Bearer $LITELLM_MASTER_KEY)
   - Body JSON:
     ```json
     {
       "model": "{{ $json.route }}",
       "messages": [{"role": "user", "content": "{{ $json.task }}"}]
     }
     ```
6. Test workflow:
   ```bash
   curl http://n8n.YOUR_DOMAIN.com/webhook/litellm-route \
     -d '{"task": "Explain quantum physics"}'
   ```
7. Export workflow: Workflow → Download → Save to repo

**Success Criteria:**
- ✅ Webhook responds within 3 seconds
- ✅ Correct model selected based on task
- ✅ Response includes reasoning (why this model)
- ✅ Langfuse shows trace with correct model

**Testing Scenarios:**
| Input | Expected Model | Reason |
|-------|---------------|--------|
| "Explain AI" | gpt-4 | Contains "explain" keyword |
| "2+2=?" | gemini-2 | Simple query |
| [60K char text] | claude-3 | Long context |

**Output:**
- Intelligent routing live in n8n
- Foundation for complex workflows

---

### **SLICE 5: Fallback Logic** ⏱️ 60 min

**Goal:** Automatic retry with different model if primary fails

**Prerequisites:**
- ✅ Slice 4 complete (routing works)

**Fallback Chains:**
- GPT-4 → Claude → Gemini → OpenRouter
- Claude → GPT-4 → Gemini → OpenRouter
- Gemini → Claude → GPT-4 → OpenRouter

**Implementation Options:**

**Option A: LiteLLM Config (Recommended)**
```yaml
# litellm-config.yaml
router_settings:
  fallbacks:
    - {"gpt-4": ["claude-3", "gemini-2"]}
    - {"claude-3": ["gpt-4", "gemini-2"]}
    - {"gemini-2": ["claude-3", "gpt-4"]}
```

**Option B: n8n Workflow**
```
HTTP Request (GPT-4)
    ↓
IF error → HTTP Request (Claude)
    ↓
IF error → HTTP Request (Gemini)
    ↓
IF error → Notify user (all failed)
```

**Recommendation:** Use Option A (LiteLLM handles it automatically)

**Steps:**
1. Edit litellm-config.yaml, add fallbacks
2. Restart LiteLLM: `docker compose restart litellm`
3. Test by disabling OpenAI key temporarily:
   ```bash
   # Edit vps.env, set OPENAI_API_KEY=invalid
   docker compose restart litellm
   # Call gpt-4 model → should automatically use claude-3
   ```
4. Verify Langfuse shows: attempted gpt-4, fell back to claude-3

**Success Criteria:**
- ✅ Failed model triggers automatic retry
- ✅ Fallback succeeds within 5 seconds
- ✅ Langfuse logs both attempts
- ✅ User receives response (no manual intervention)

**Output:**
- Resilient system: 99.9% uptime even if 1 provider down
- Automatic failover

---

### **SLICE 6: End-to-End Test (Telegram → n8n → LiteLLM)** ⏱️ 45 min

**Goal:** Full integration test with Telegram bot

**Prerequisites:**
- ✅ Slice 5 complete (fallbacks work)
- ✅ Telegram bot token available

**Workflow:**
```
User sends Telegram message
    ↓
Telegram Bot (aiogram) receives message
    ↓
POST to n8n webhook
    ↓
n8n routes to LiteLLM
    ↓
LiteLLM calls GPT/Claude/Gemini
    ↓
Response → n8n
    ↓
n8n → Telegram Bot
    ↓
Bot sends reply to user
```

**Steps:**
1. Create simple Telegram handler:
   ```python
   # telegram_test_bot.py
   from aiogram import Bot, Dispatcher
   import requests
   
   bot = Bot(token=TELEGRAM_BOT_TOKEN)
   
   @dp.message()
   async def handle_message(message):
       response = requests.post(
           'http://n8n:5678/webhook/litellm-route',
           json={'task': message.text}
       )
       await message.reply(response.json()['result'])
   ```
2. Add to docker-compose (optional, or run locally for test)
3. Send message: "/test Hello from Telegram"
4. Verify response arrives within 5 seconds

**Success Criteria:**
- ✅ Telegram bot responds
- ✅ Message logged in Langfuse
- ✅ Round-trip latency < 5 seconds
- ✅ No errors in logs

**Output:**
- Proof of concept: full stack working
- Foundation for H3 (Telegram async approvals)

---

### **SLICE 7: Event Schema + Redis Streams** ⏱️ 90 min

**Goal:** Define event format, set up Redis Streams for coordination

**Prerequisites:**
- ✅ Redis running (already done)
- ✅ Understanding of Event Sourcing (from research)

**Event Schema Design:**
```json
{
  "event_id": "evt_20241208_abc123",
  "event_type": "agent.action.completed",
  "aggregate_id": "project:life-os",
  "version": 47,
  "timestamp": "2024-12-08T10:30:00Z",
  "agent": {
    "model": "claude-3.5-sonnet",
    "agent_id": "agent-main",
    "session_id": "session-xyz"
  },
  "payload": {
    "action": "task_created",
    "resource": "/tasks/task-456",
    "data": {...},
    "reasoning": "User requested..."
  },
  "metadata": {
    "correlation_id": "req-789",
    "approval_required": false
  }
}
```

**Files to Create:**
1. `tools/event_publisher.py` (write events to Redis)
2. `tools/event_consumer.py` (read events, process)
3. `docs/EVENT_SCHEMA.md` (documentation)

**Steps:**
1. Create event publisher:
   ```python
   import redis
   import json
   from datetime import datetime
   
   r = redis.Redis(host='redis', port=6379, decode_responses=True)
   
   def publish_event(event_type, payload):
       event = {
           "event_id": f"evt_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
           "event_type": event_type,
           "timestamp": datetime.utcnow().isoformat(),
           "payload": payload
       }
       r.xadd('agent_events', event)
       return event['event_id']
   ```
2. Test publish:
   ```python
   publish_event("test.event", {"message": "Hello"})
   ```
3. Verify in Redis:
   ```bash
   redis-cli XREAD COUNT 10 STREAMS agent_events 0
   ```

**Success Criteria:**
- ✅ Events written to Redis Streams
- ✅ Events readable via XREAD
- ✅ Schema documented
- ✅ Python scripts tested

**Output:**
- Event infrastructure ready
- Foundation for Observer Agent

---

### **SLICE 8: Observer Agent** ⏱️ 120 min

**Goal:** Python script that monitors events, detects drift

**Prerequisites:**
- ✅ Slice 7 complete (events working)

**Observer Responsibilities:**
1. Read events from Redis Streams
2. Detect version conflicts (optimistic locking)
3. Create Change Requests for Git updates
4. Flag approval requirements

**Files to Create:**
1. `tools/observer_agent.py` (main script)
2. `tools/change_request_generator.py` (CR logic)
3. `docs/OBSERVER_AGENT.md` (documentation)

**Observer Logic:**
```python
while True:
    events = redis.xread({'agent_events': last_id}, count=10, block=5000)
    
    for event in events:
        # Check version
        current_version = get_git_version(event['aggregate_id'])
        if event['version'] != current_version:
            create_change_request(event)
        else:
            log_event_to_jsonl(event)
```

**Success Criteria:**
- ✅ Observer runs continuously (systemd service)
- ✅ Detects version mismatches
- ✅ Creates Change Requests (JSON files)
- ✅ Logs to JSONL (append-only)

**Output:**
- Automated drift detection
- Change Request workflow ready

---

### **SLICE 9: Git Reconciliation Loop** ⏱️ 90 min

**Goal:** Observer Agent commits approved changes to Git

**Prerequisites:**
- ✅ Slice 8 complete (Observer running)

**Workflow:**
```
Observer detects event
    ↓
IF no conflict → Auto-approve (low-risk)
IF conflict → Create CR, send to Telegram
    ↓
User approves via Telegram
    ↓
Observer reads approval from Redis Pub/Sub
    ↓
Apply change to Git:
    - Update file
    - Git add
    - Git commit
    - Git push
```

**Steps:**
1. Add approval check to Observer:
   ```python
   if change_request['approval_required']:
       send_to_telegram(change_request)
       wait_for_approval(change_request['id'])
   
   apply_to_git(change_request)
   ```
2. Implement git operations:
   ```python
   def apply_to_git(cr):
       file_path = cr['target_file']
       with open(file_path, 'w') as f:
           f.write(cr['new_content'])
       
       subprocess.run(['git', 'add', file_path])
       subprocess.run(['git', 'commit', '-m', cr['commit_message']])
       subprocess.run(['git', 'push'])
   ```
3. Test with manual event injection

**Success Criteria:**
- ✅ Low-risk changes auto-commit
- ✅ High-risk changes wait for approval
- ✅ Git history shows Observer commits
- ✅ No data loss (event log preserved)

**Output:**
- Fully automated Truth Layer updates
- Human-in-the-loop for critical changes

---

### **SLICE 10: Automated Backups** ⏱️ 60 min

**Goal:** Daily PostgreSQL + Qdrant + Git backups to Google Cloud Storage

**Prerequisites:**
- ✅ GCP account with Cloud Storage bucket

**Backup Strategy:**
| Data | Backup Method | Frequency | Retention |
|------|--------------|-----------|-----------|
| PostgreSQL | pg_dump | Daily 2 AM | 30 days |
| Qdrant | Snapshot API | Daily 2 AM | 30 days |
| Git repo | Push to remote | Real-time | Infinite |
| Docker volumes | Tar archive | Weekly | 4 weeks |

**Steps:**
1. Create GCS bucket:
   ```bash
   gsutil mb -l us-central1 gs://ai-life-os-backups
   ```
2. Create backup script:
   ```bash
   #!/bin/bash
   # backup.sh
   
   DATE=$(date +%Y%m%d)
   
   # PostgreSQL
   docker exec postgres pg_dumpall -U postgres | \
     gzip > /tmp/postgres_$DATE.sql.gz
   gsutil cp /tmp/postgres_$DATE.sql.gz gs://ai-life-os-backups/postgres/
   
   # Qdrant
   curl -X POST http://localhost:6333/collections/life-os/snapshots
   # ... upload snapshot to GCS
   
   # Git
   cd /opt/ai-os && git push origin main
   ```
3. Add to crontab:
   ```
   0 2 * * * /opt/ai-os/scripts/backup.sh
   ```

**Success Criteria:**
- ✅ Backup runs daily
- ✅ Files appear in GCS
- ✅ Restore test succeeds
- ✅ Email notification on failure

**Output:**
- Peace of mind: 30-day recovery window
- Compliance: audit trail preserved

---

### **SLICE 11: Cloud Monitoring Alerts** ⏱️ 45 min

**Goal:** Alerts for: high memory, disk full, LiteLLM errors

**Prerequisites:**
- ✅ Google Cloud Monitoring enabled

**Alerts to Create:**
| Alert | Condition | Action |
|-------|-----------|--------|
| High Memory | RAM > 90% for 5 min | Email + Telegram |
| Disk Full | Disk > 85% | Email + Telegram |
| LiteLLM Down | Health check fails 3x | Email + Telegram |
| High API Cost | Daily spend > $10 | Email only |

**Steps:**
1. Create alerting policy in GCP Console
2. Add notification channel (email + Telegram webhook)
3. Test alert:
   ```bash
   # Fill memory temporarily
   stress --vm 1 --vm-bytes 3G --timeout 60s
   ```

**Success Criteria:**
- ✅ Alert fires within 5 minutes
- ✅ Notification received (email + Telegram)
- ✅ Alert auto-resolves when condition clears

**Output:**
- Proactive monitoring
- Sleep better at night

---

### **SLICE 12: Load Testing** ⏱️ 90 min

**Goal:** Validate system handles 100 concurrent requests

**Prerequisites:**
- ✅ All previous slices complete

**Load Test Plan:**
| Scenario | Concurrent Users | Duration | Success Rate |
|----------|-----------------|----------|-------------|
| Steady Load | 10 | 5 min | >99% |
| Spike Load | 100 | 1 min | >95% |
| Sustained | 50 | 30 min | >98% |

**Tools:**
- Locust (Python load testing)
- OR: k6 (Go-based)

**Steps:**
1. Install Locust:
   ```bash
   pip install locust
   ```
2. Create locustfile.py:
   ```python
   from locust import HttpUser, task
   
   class LiteLLMUser(HttpUser):
       @task
       def call_gpt4(self):
           self.client.post("/v1/chat/completions", json={
               "model": "gpt-4",
               "messages": [{"role": "user", "content": "Test"}]
           }, headers={"Authorization": f"Bearer {LITELLM_KEY}"})
   ```
3. Run test:
   ```bash
   locust -f locustfile.py --host http://YOUR_VPS:4000
   ```
4. Monitor in Langfuse: request rate, latency P95, error rate

**Success Criteria:**
- ✅ No 500 errors under load
- ✅ P95 latency < 3 seconds
- ✅ Memory stays < 90%
- ✅ No container restarts

**Tuning if Fails:**
- Increase LiteLLM num_workers
- Add Redis caching (already configured)
- Upgrade to e2-standard-2 (8GB RAM)

**Output:**
- Confidence in production readiness
- Performance baseline documented

---

## 💰 COST ANALYSIS

### Infrastructure (Monthly)
| Component | Cost |
|-----------|------|
| GCP e2-medium | $24.46 |
| 50GB pd-balanced | $5.00 |
| Egress (~10GB) | $1.00 |
| **Total** | **~$30/month** |

### API Calls (Estimated - Moderate Use)
| Model | Monthly Tokens | Cost |
|-------|---------------|------|
| GPT-4 | 500K in + 100K out | $8.50 |
| Claude | 500K in + 100K out | $4.50 |
| Gemini | 1M in + 200K out | $0.30 |
| **Total** | | **~$13/month** |

**Total COO: ~$43-45/month**

**Budget Controls:**
- LiteLLM max_budget: $50/month
- Alert when >$40 spent
- Automatic shutdown at $55

---

## 🚨 RISK ASSESSMENT

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Memory exhaustion** | Medium | High | Container limits (384MB), swap enabled |
| **API rate limits** | Medium | Medium | Fallback chains, retry logic |
| **Data loss** | Low | Critical | Daily backups to GCS, Git remote |
| **Model API outage** | Low | High | 3-model redundancy + OpenRouter |
| **Cost overrun** | Low | Medium | Budget alerts, auto-cutoff at $55 |
| **Security breach** | Low | Critical | Secret Manager, firewall rules, Caddy auth |

---

## 🛠️ TOOLS & PREREQUISITES

### Required Tools (Already Installed)
- ✅ Docker + Docker Compose
- ✅ Git
- ✅ Python 3.11+
- ✅ Node.js 20+ (for n8n)
- ✅ Redis CLI (for debugging)

### Skills Needed
- ✅ Docker Compose syntax
- ✅ YAML configuration
- ✅ Basic Python (for Observer Agent)
- ✅ n8n workflow design
- ⚠️ Event Sourcing concepts (will learn via research docs)

---

## 📅 TIMELINE

### Week 1 (Foundation)
- **Day 1:** Slices 1-3 (LiteLLM + testing)
- **Day 2:** Slices 4-5 (n8n routing + fallbacks)
- **Day 3:** Slice 6 (end-to-end test)

### Week 2 (Events + Production)
- **Day 4-5:** Slices 7-9 (Event Sourcing + Observer)
- **Day 6:** Slice 10 (Backups)
- **Day 7:** Slices 11-12 (Monitoring + Load Testing)

### Buffer
- **Days 8-10:** Refinement, documentation, unexpected issues

---

## ✅ SUCCESS METRICS (End State)

**Technical:**
- [ ] All 3 models callable via unified API
- [ ] <3s P95 latency for 95% of requests
- [ ] >99% uptime (3 nines)
- [ ] <$50/month total spend
- [ ] Daily backups to GCS
- [ ] Monitoring alerts configured

**Functional:**
- [ ] n8n routes to optimal model automatically
- [ ] Fallbacks work (tested via disabled key)
- [ ] Events logged to Redis Streams
- [ ] Observer Agent running 24/7
- [ ] Git commits reflect agent actions
- [ ] Langfuse shows all traces

**ADHD-Aware:**
- [ ] Single command to deploy (`docker compose up`)
- [ ] Clear rollback plan for each slice
- [ ] <90 min per slice (stopping points)
- [ ] Telegram notifications (async approvals)

---

## 📖 DECISION LOG

### Key Decisions Made During Planning

**Decision 1: LiteLLM over Alternatives**
- **Options:** LiteLLM, OpenRouter, Orq.ai, LangChain
- **Chosen:** LiteLLM
- **Rationale:** Free, lightweight (384MB), production-proven (8ms P95 latency)
- **Trade-off:** Manual deployment vs managed service (Orq.ai)

**Decision 2: n8n over LangGraph for Orchestration**
- **Options:** n8n, LangGraph, CrewAI
- **Chosen:** n8n
- **Rationale:** Already deployed, visual workflows, ADHD-friendly
- **Trade-off:** Less programmatic control vs LangGraph

**Decision 3: Redis Streams over Kafka for Events**
- **Options:** Kafka, Redis Streams, JSONL files only
- **Chosen:** Redis Streams
- **Rationale:** Already running Redis, simpler ops, sufficient scale
- **Trade-off:** Less ecosystem (Kafka Connect) vs complexity

**Decision 4: Event Sourcing + CQRS over Simple Git Sync**
- **Options:** Manual Git sync, Event Sourcing, Database-first
- **Chosen:** Event Sourcing
- **Rationale:** Prevents race conditions, audit trail, time-travel debugging
- **Trade-off:** More complex architecture vs immediate consistency

**Decision 5: GCP Compute Engine over Cloud Run**
- **Options:** Compute Engine, Cloud Run, GKE
- **Chosen:** Compute Engine (current)
- **Rationale:** 24/7 cheaper (~$30/mo vs $70/mo), full control
- **Trade-off:** Manual scaling vs auto-scaling

---

## 🔄 ROLLBACK STRATEGY

### If Things Go Wrong

**Slice-Level Rollback:**
Each slice has specific rollback steps (see slice details above).

**Full System Rollback:**
```bash
# 1. Stop new services
docker compose down litellm

# 2. Restore docker-compose.vps.yml from Git
git checkout HEAD~1 docker-compose.vps.yml

# 3. Restart stack
docker compose up -d

# 4. Verify n8n still works
curl http://n8n.YOUR_DOMAIN.com/healthz
```

**Nuclear Option (Last Resort):**
```bash
# Restore from last night's backup
gsutil cp gs://ai-life-os-backups/postgres/$(date +%Y%m%d).sql.gz /tmp/
docker exec -i postgres psql -U postgres < /tmp/backup.sql
```

---

## 📚 DOCUMENTATION TO CREATE

During implementation, we'll create:

1. **README.md** (how to deploy from scratch)
2. **ARCHITECTURE.md** (system design with diagrams)
3. **RUNBOOK.md** (operations: start, stop, debug)
4. **EVENT_SCHEMA.md** (event format reference)
5. **API.md** (LiteLLM endpoint documentation)
6. **COST_TRACKING.md** (monthly spend breakdown)
7. **TROUBLESHOOTING.md** (common errors + fixes)

---

## 🎯 NEXT STEP

**When you're ready to start:**

Say: **"Let's start Slice 1"**

I will:
1. Read vps.env to get API keys ✅ (already done)
2. Create litellm-config.yaml
3. Update docker-compose.vps.yml
4. Provide exact commands to run
5. Verify success together

---

**Created:** 2025-12-08  
**Status:** READY TO START  
**Estimated Completion:** 2025-12-18 (10 days)  
**Owner:** Or (with Claude as architect)