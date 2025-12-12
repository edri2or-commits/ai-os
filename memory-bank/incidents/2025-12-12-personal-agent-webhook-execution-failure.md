# Incident Report: Personal Agent v1 Webhook Execution Failure

**Date:** 2025-12-12  
**Severity:** 🔴 High (Core Agent Non-Functional, Environment Variables Missing)  
**Duration:** ~2 hours (discovery to diagnosis)  
**Status:** 🔴 OPEN (Root Cause Identified, Fix Pending)

---

## Summary

Personal Agent v1 workflow successfully activated but fails execution with blank responses. Root cause: Missing critical environment variables (`AI_OS_PATH`, `ANTHROPIC_API_KEY`) in n8n Docker container preventing Claude agent from accessing SYSTEM_MANIFESTO.md and making API calls.

---

## Timeline

**2025-12-12 01:05** - Workflow activated successfully (status changed from inactive → active)  
**2025-12-12 01:14** - First webhook test via gcloud ssh: HTTP 200 but blank response  
**2025-12-12 01:14:01** - Execution #1 failed (error status, 0s duration)  
**2025-12-12 01:14:47** - Execution #2 failed (error status, 0s duration)  
**2025-12-12 01:15** - Investigation revealed missing environment variables  
**2025-12-12 03:11** - User requested comprehensive documentation of issue

---

## Impact

**Systems Affected:**
- ❌ Personal Agent v1 (workflow ID: yLPedfaZcfadRTKO) - Non-functional
- ⚠️ n8n MCP integration - Working but agent cannot execute
- ✅ n8n infrastructure - Healthy (container running, API accessible)
- ✅ VPS connectivity - Operational

**Business Impact:**
- Core ADHD task decomposition system unusable
- Cannot process user requests through Personal Agent
- Webhook endpoint accessible but non-responsive (silent failure)
- n8n MCP tools functional but workflow unusable

**User Impact:**
- User attempted activation through UI (successful)
- Testing revealed silent failure (HTTP 200, blank body)
- No error visibility in webhook response
- Requires deep diagnostics to understand failure

---

## Technical Details

### Environment Setup

**VPS Configuration:**
- Instance: ai-life-os-prod (35.223.68.23, us-central1-a)
- n8n: Running in Docker container, port 5678
- Docker Compose: C:\Users\edri2\Desktop\AI\ai-os\docker-compose.vps.yml

**Workflow Details:**
- Name: "Personal Agent v1 - ADHD Task Decomposer"
- ID: yLPedfaZcfadRTKO
- Webhook path: `/webhook/personal-agent`
- Status: Active ✅
- Executions: 2 failed attempts

### Execution Pattern

**Test Command (from VPS via localhost):**
```bash
curl -X POST http://localhost:5678/webhook/personal-agent \
  -H "Content-Type: application/json" \
  -d '{"message": "System test - can you hear me?"}'
```

**Response:**
- HTTP Status: 200 OK
- Body: Empty (blank response)
- Execution logged in n8n: Status "error", Duration 0s

**Execution Details (ID: 2):**
```json
{
  "id": "2",
  "workflowId": "yLPedfaZcfadRTKO",
  "status": "❌ error",
  "startedAt": "2025-12-12T01:14:47.370Z",
  "stoppedAt": "2025-12-12T01:14:47.469Z",
  "duration": "0s",
  "finished": false,
  "mode": "webhook",
  "nodeResults": {}
}
```

**Key Observation:** `nodeResults` is empty, indicating workflow failed before any nodes executed.

### Workflow Architecture

**Expected Flow:**
1. **webhook_trigger** - Receives user request via POST /webhook/personal-agent
2. **read_manifesto** - Loads SYSTEM_MANIFESTO.md from `$env.AI_OS_PATH`
3. **prepare_context** - Extracts user_request, user_state, manifesto_content
4. **claude_agent** - HTTP request to Anthropic API (claude-sonnet-4-20250514)
5. **parse_response** - Parse JSON response
6. **webhook_response** - Return to user

**Critical Dependencies:**
- `$env.AI_OS_PATH` → Must point to `/home/node/ai-os` (SYSTEM_MANIFESTO.md location)
- `$env.ANTHROPIC_API_KEY` → Required for Claude API authentication

---

## Root Cause Analysis

### Primary Cause: Missing Environment Variables

**Evidence:**
```bash
docker exec n8n env | grep -E "(AI_OS_PATH|ANTHROPIC_API_KEY)"
# Expected output: Two environment variables
# Actual output: [PENDING VERIFICATION]
```

**Node Failure Point:** `read_manifesto` node attempts to access `$env.AI_OS_PATH` which is undefined, causing immediate workflow termination.

### Secondary Issues

**1. Silent Failure Pattern**
- Webhook returns HTTP 200 even when execution fails
- No error message in response body
- Error only visible through n8n API execution query
- User has zero visibility into failure

**2. Security: "Host not allowed"**
- External IP (35.223.68.23) blocked from accessing webhooks
- Only localhost can trigger (tested successfully via gcloud ssh)
- Prevents direct testing from user machine
- **Impact:** Cannot test workflows externally, must SSH into VPS

**3. Incomplete Deployment**
- Workflow imported and activated ✅
- Environment variables not configured ❌
- SYSTEM_MANIFESTO.md present on VPS ✅ (confirmed: /home/node/ai-os/SYSTEM_MANIFESTO.md)
- Docker container lacks variable injection ❌

---

## 5 Whys Root Cause Analysis

**1. Why did Personal Agent execution fail?**  
→ Because `read_manifesto` node cannot access `$env.AI_OS_PATH`

**2. Why is `$env.AI_OS_PATH` undefined?**  
→ Because n8n Docker container does not have environment variables injected

**3. Why are environment variables not injected?**  
→ Because docker-compose.vps.yml does not define them in n8n service

**4. Why does docker-compose.vps.yml lack environment variables?**  
→ Because deployment process did not include environment configuration step

**5. Why was environment configuration step skipped?**  
→ Because **SVP-001 violation**: Activation claimed "✅ COMPLETE" without verifying runtime environment

---

## Resolution Steps (Pending)

### Immediate Fix Required

**Step 1: Verify Current Environment**
```bash
# SSH into VPS
gcloud compute ssh ai-life-os-prod --zone=us-central1-a

# Check current n8n environment
docker exec n8n env | grep -E "(AI_OS_PATH|ANTHROPIC_API_KEY|N8N_)"

# Check docker-compose configuration
cat /home/node/docker-compose.vps.yml | grep -A 10 "n8n:"
```

**Step 2: Add Environment Variables to docker-compose.vps.yml**
```yaml
services:
  n8n:
    environment:
      - AI_OS_PATH=/home/node/ai-os
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      # Existing N8N_ variables...
```

**Step 3: Create .env File on VPS**
```bash
# /home/node/.env
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx  # From 1Password or user
```

**Step 4: Restart n8n Container**
```bash
cd /home/node
docker-compose -f docker-compose.vps.yml down
docker-compose -f docker-compose.vps.yml up -d
```

**Step 5: Verify Fix**
```bash
# Check environment variables are present
docker exec n8n env | grep AI_OS_PATH
docker exec n8n env | grep ANTHROPIC_API_KEY

# Test workflow again
curl -X POST http://localhost:5678/webhook/personal-agent \
  -H "Content-Type: application/json" \
  -d '{"message": "System test - can you hear me?"}'

# Expected: JSON response with mode, next_action, rationale, etc.
```

**Step 6: Verify Execution Success**
```bash
# Via n8n MCP
n8n:list_executions(workflowId="yLPedfaZcfadRTKO", limit=1)
# Expected: status="success", duration >0s, nodeResults populated
```

---

## Lessons Learned

### What Went Wrong

1. **Deployment Incomplete:** Workflow activated without runtime dependencies
2. **SVP-001 Violation:** Claimed "activated ✅" without end-to-end testing
3. **Silent Failure:** Webhook gives HTTP 200 on error (misleading success signal)
4. **No Pre-Flight Checklist:** Missing verification of environment variables before activation
5. **Documentation Gap:** docker-compose.vps.yml not documented as requiring .env file

### What Went Right

1. **n8n MCP Integration:** Successfully connected, API working perfectly
2. **Workflow Structure:** Clean import, no structural errors
3. **VPS Infrastructure:** Stable, SSH access working, Docker healthy
4. **Systematic Diagnosis:** Execution logs provided clear failure signal
5. **Root Cause Clarity:** Environment variables identified quickly

---

## Anti-Patterns Identified

### AP-XXX: Activation Without Runtime Verification
**Pattern:** Claiming "workflow activated ✅" without testing execution with real data  
**Example:** Personal Agent activated but never tested with actual webhook call  
**Prevention:** Add to SVP-001 checklist:
- [ ] Workflow structurally valid (imported successfully)
- [ ] Workflow activated (n8n shows "active")
- [ ] **NEW:** Workflow executed successfully (test webhook call returns expected data)
- [ ] **NEW:** All environment variables present (`docker exec n8n env`)

### AP-XXX: Silent Failure Acceptance
**Pattern:** Accepting HTTP 200 as "success" without inspecting response body  
**Example:** curl returned HTTP 200, assumed working, but body was empty  
**Prevention:** Always check response body, not just status code

---

## Action Items

### Critical (Do Now)

- [ ] **FIX-001: Add Environment Variables** - Inject AI_OS_PATH and ANTHROPIC_API_KEY into n8n container
  - Files: docker-compose.vps.yml, .env (VPS)
  - Estimated time: 15 minutes
  - Verification: docker exec n8n env + test webhook call

- [ ] **FIX-002: End-to-End Test** - Execute Personal Agent with real Hebrew request
  - Test input: "בדיקת מערכת - האם אתה שומע אותי?"
  - Expected output: JSON with mode (FLOW/PARALYSIS/CRISIS), next_action, rationale
  - Verification: n8n execution status="success"

### High Priority (Soon)

- [ ] **SEC-001: Webhook Security Review** - Understand "Host not allowed" restriction
  - Is this intentional? (prevent external abuse)
  - Does it need IP whitelist? (allow specific IPs)
  - Document security model

- [ ] **SVP-001 Update:** Add "runtime verification" checklist item
  - Example: "Execute workflow with test payload, verify response body"
  - Prevents "activation theater" (active but broken)

- [ ] **DEPLOYMENT_MANUAL Update:** Add environment variables section
  - Document required variables for Personal Agent
  - Add .env file creation step
  - Include verification commands

### Medium Priority (Later)

- [ ] **Silent Failure Pattern:** Research n8n webhook error handling
  - Can we force error responses instead of HTTP 200?
  - Add error_handler node to workflow?
  - Log errors to external system?

- [ ] **Monitoring:** Add Personal Agent health check
  - Scheduled workflow that tests Personal Agent every hour
  - Alerts if execution fails
  - Prevents silent degradation

---

## Related Documents

- **SYSTEM_MANIFESTO.md:** Source of Truth referenced by Personal Agent
- **docker-compose.vps.yml:** n8n container configuration (needs update)
- **DEPLOYMENT_MANUAL.md:** VPS deployment guide (needs environment section)
- **SVP-001:** Self-Validation Protocol (violated, needs update)
- **memory-bank/incidents/2025-12-03-docker-autostart-false.md:** Similar pattern (claimed done, not verified)

---

## Technical Debt Created

- **TD-XXX:** n8n MCP cannot trigger webhooks externally (security restriction)
- **TD-XXX:** No automated health check for Personal Agent workflow
- **TD-XXX:** Silent failure pattern (HTTP 200 on error) unresolved
- **TD-XXX:** No pre-deployment checklist for n8n workflows

---

## Meta-Learning

**Trigger Type:** Trigger A (Critical Failure in Production)  
**Pattern:** Deployment validation theater (activated ≠ functional)  
**Anti-Pattern:** AP-XXX (Activation Without Runtime Verification)  
**Protocol Violation:** SVP-001 (claimed complete without execution test)  
**Similar Incident:** 2025-12-03-docker-autostart-false.md (claimed configured, not verified)

---

**Incident Status:** 🔴 OPEN  
**Next Action:** Execute FIX-001 (add environment variables)  
**Estimated Resolution Time:** 30 minutes  
**Owner:** Or (user) + Claude (AI-OS agent)
