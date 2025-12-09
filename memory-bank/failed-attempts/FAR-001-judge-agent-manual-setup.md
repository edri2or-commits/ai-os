# Failed Attempt Registry - FAR-001

## Metadata
- **Date:** 2025-12-03
- **Task:** Judge Agent Setup (Manual UI Configuration)
- **Duration:** 120 minutes
- **Result:** FAILED
- **User Impact:** Severe frustration, exhaustion
- **Severity:** CRITICAL

---

## What Happened

### Initial Request
User requested to complete Judge Agent setup (estimated 2 minutes).

### Claude's Approach
Suggested manual configuration through n8n UI:
1. Open n8n UI
2. Navigate to workflows
3. Double-click Judge Agent workflow
4. Click on HTTP Request node
5. Add credential manually
6. Configure OpenAI authentication
7. Test and activate

### Actual Execution
- **Duration:** 120 minutes of manual UI clicking
- **Steps:** 47+ manual actions
- **Outcome:** Workflow never activated, API key never configured properly
- **User Signals:**
  - "תפסיק לחפף" (Stop bullshitting)
  - "אני לא עובד עוד" (I'm not working anymore)
  - Visible exhaustion and frustration

### Root Cause
Claude suggested manual UI approach despite having:
- ✅ Desktop Commander MCP (can access Docker)
- ✅ Filesystem MCP (can write .env files)
- ✅ n8n MCP (can update workflows via API)
- ✅ Knowledge of docker-compose environment variables

---

## Why It Failed

### Technical Reasons
1. **Wrong approach:** UI configuration instead of environment variables
2. **Missing automation:** Suggested manual clicking instead of scripting
3. **No search:** Didn't check conversation history for similar past failures
4. **Ignored tools:** Had all necessary MCPs but didn't use them

### Behavioral Patterns (FauxPas Types)
- **Capability Amnesia:** Forgot about MCP tools availability
- **Constraint Blindness:** Ignored ADHD-aware design principles (low friction)
- **Hallucinated Affordances:** Assumed UI approach would be "2 minutes" (was 120)

---

## Correct Approach (Discovered 2025-12-05)

### What Should Have Been Done
```yaml
Step 1: Create .env file
  tool: Filesystem:write_file
  path: /infra/n8n/.env
  content: OPENAI_API_KEY=sk-proj-...
  duration: 30 seconds

Step 2: Update docker-compose.yml
  tool: Filesystem:write_file or str_replace
  add: - OPENAI_API_KEY=${OPENAI_API_KEY}
  duration: 30 seconds

Step 3: Restart container
  tool: Desktop Commander:start_process
  command: docker-compose restart n8n
  duration: 10 seconds

Step 4: Test
  tool: n8n:get_workflow
  verify: workflow active
  duration: 5 seconds

Total: ~2 minutes (as originally estimated)
```

---

## Lessons Learned

### Never Do This Again
❌ Suggest manual UI configuration for API keys  
❌ Suggest manual clicking for ADHD user  
❌ Estimate time without checking tools first  
❌ Proceed without searching conversation history  

### Always Do This Instead
✅ Check conversation_search before suggesting tasks  
✅ Use environment variables for secrets (never UI)  
✅ Use MCP tools for automation  
✅ Verify estimate against actual capabilities  
✅ Fail fast if manual approach detected  

---

## Prevention Protocols

### Created as Result
- **MTD-002:** Manual Task Detection v2.0
  - MUST search conversation history before manual suggestions
  - MUST check if task previously failed
  - MUST block suggestion if pattern matches past failure

- **FAR Registry:** This document
  - All failed attempts must be documented
  - Must be searchable by future Claude instances
  - Must include prevention protocols

---

## Success Metrics

### What Success Looks Like
When this prevention works, we'll see:
- ✅ Zero repeated failed manual tasks
- ✅ Automatic API key configuration
- ✅ Sub-5-minute setup times
- ✅ Zero user frustration signals
- ✅ Judge Agent functional immediately

### Validation
2025-12-05: Task completed successfully in 8 minutes (vs 120 minutes), zero UI clicking, full automation.

---

## References
- Original transcript: `/mnt/transcripts/2025-12-05-00-49-06-judge-agent-setup-failure-pattern.txt`
- Successful approach: This conversation (2025-12-05)
- Related protocols: MTD-002, Protocol 1

---

**STATUS:** ✅ DOCUMENTED & PREVENTED  
**NEXT OCCURRENCE:** Should be blocked by MTD-002
