# Judge Vision Fix Plan - Research-Based Architecture

## Metadata
- **Plan ID:** PLAN-2025-12-05-001
- **Title:** Professional Auto-Learning Infrastructure (LHO + Reflexion + APO)
- **Status:** APPROVED - Ready for Implementation
- **Research Source:** "Architecting the Cognitive Self: The 2025 Personal AI Life Operating System"
- **Created:** 2025-12-05T03:30:00Z
- **Estimated Duration:** 6-8 hours (5 slices)
- **Priority:** 🔴 CRITICAL - Foundation for all learning

---

## Executive Summary

Replace naive JSONL-based event logging with professional **Langfuse + LHO + Reflexion** architecture based on 2025 state-of-the-art research. This establishes the foundation for a self-improving system that learns from every failure.

### Current State (Naive)
- ❌ Events in raw JSONL (no structure, no UI, no integration)
- ❌ Judge Agent can't see conversations/transcripts
- ❌ No learning consolidation (hundreds of events, no synthesis)
- ❌ No retrieval mechanism (learned knowledge not applied)
- ❌ Manual Protocol 1 (Claude forgets to log)

### Target State (Professional)
- ✅ **Langfuse** - Industry standard observability (OpenTelemetry)
- ✅ **LHOs** - Structured knowledge artifacts (not raw events)
- ✅ **Reflexion Loop** - Automated post-mortem analysis
- ✅ **Retrieval** - On-demand injection of learned rules
- ✅ **APO** - Automatic prompt optimization (system evolves itself)
- ✅ **Frustration Index** - Alignment tracking

---

## Architecture Overview

### The Five Layers

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: LANGFUSE (Professional Observability)             │
│  • Replaces EVENT_TIMELINE.jsonl                            │
│  • Structured traces (OpenTelemetry standard)               │
│  • Cost tracking, prompt versioning, beautiful UI           │
│  • Open source (self-hostable) or cloud                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: JUDGE AGENT (Reflector - Enhanced)               │
│  • Reads Langfuse traces (last 6 hours)                    │
│  • Performs structured post-mortem on failures              │
│  • Root cause analysis (5 Whys)                             │
│  • Outputs pre-LHO JSON (not just FauxPas report)          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: TEACHER AGENT (LHO Creator)                      │
│  • Triggered by Judge (when FauxPas detected)               │
│  • Converts Judge analysis → LHO (structured artifact)      │
│  • Schema: trigger, failure_pattern, correction, code       │
│  • Writes to Qdrant (vector DB for semantic search)        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4: LIBRARIAN AGENT (Context Manager)                │
│  • Before each Claude task, query Qdrant for relevant LHOs │
│  • Semantic search: task description → top 3 LHOs          │
│  • Inject into Claude's system prompt (JIT learning)        │
│  • "You have learned: [LHO-089: Never suggest manual UI]"  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 5: APO (Automatic Prompt Optimization) - Optional   │
│  • Weekly consolidation (cron job)                          │
│  • Clusters similar LHOs (e.g., 15 about Python standards) │
│  • GPT-4: "Rewrite system prompt to internalize these"     │
│  • Evolves: hundreds of LHOs → updated system prompt       │
└─────────────────────────────────────────────────────────────┘
```

---

## Memory Hierarchy (Research-Based)

| Memory Tier | Function | Storage | Retention | Implementation |
|-------------|----------|---------|-----------|----------------|
| **Working** | Active context | Context Window | Volatile | Claude's current conversation |
| **Episodic** | Chronicle of events | Langfuse Traces | Permanent | Timestamped action log |
| **Semantic** | Crystallized facts | Knowledge Graph | Mutable | User preferences, world facts |
| **Procedural** | Skill Library (LHOs) | Qdrant Vector DB | Permanent | Learned rules + code snippets |

**Key Insight:** We're building the **Procedural Memory** layer (the missing piece!)

---

## Life Handling Object (LHO) Schema

```json
{
  "lho_id": "LHO-001",
  "title": "Manual Task Detection - Never Repeat UI Clicking",
  "type": "correction",
  "severity": "critical",
  
  "trigger_context": "When suggesting setup/configuration tasks",
  
  "failure_pattern": {
    "description": "Claude suggests manual UI configuration despite having MCP tools",
    "example": "Suggested 'Complete Judge Agent Setup (2 min)' via n8n UI clicking",
    "user_signal": "תפסיק לחפף (Stop bullshitting)",
    "duration": 120,
    "timestamp": "2025-12-03T12:00:00Z"
  },
  
  "correction_strategy": {
    "principle": "ALWAYS use MCP tools for automation, NEVER suggest manual UI steps",
    "steps": [
      "1. Check conversation_search for similar past failures",
      "2. Verify available MCP tools (Desktop Commander, Filesystem, n8n API)",
      "3. Use environment variables for secrets (Docker-native)",
      "4. Automate via CLI/API, not UI"
    ],
    "code_snippet": "# Create .env file\nFilesystem:write_file(...)\n# Update docker-compose\nstr_replace(...)\n# Restart container\nDesktop Commander:start_process('docker-compose restart')"
  },
  
  "success_metrics": {
    "application_count": 1,
    "success_rate": 1.0,
    "time_saved_minutes": 112,
    "user_satisfaction": "positive"
  },
  
  "metadata": {
    "created_at": "2025-12-05T03:00:00Z",
    "created_by": "teacher_agent",
    "source_faux_pas_id": "FP-2025-12-05-01",
    "related_far": "FAR-001"
  }
}
```

---

## The Reflexion Loop (Learning Cycle)

```
1. FAILURE EVENT
   ↓
   [Something goes wrong: 120-min manual UI failure]
   ↓

2. OBSERVATION (Langfuse)
   ↓
   [Traces captured: tool calls, duration, user signals]
   ↓

3. POST-MORTEM (Judge Agent)
   ↓
   [Root cause analysis: "Capability Amnesia - forgot MCP tools"]
   ↓

4. DIAGNOSIS (Judge Output)
   ↓
   [Pre-LHO JSON: trigger, failure pattern, correction needed]
   ↓

5. CODIFICATION (Teacher Agent)
   ↓
   [Creates LHO-001: "Manual Task Detection" with code snippet]
   ↓

6. STORAGE (Qdrant)
   ↓
   [Vector embedding: "manual setup" → retrieves LHO-001]
   ↓

7. RETRIEVAL (Librarian Agent)
   ↓
   [Next time: Task involves "setup" → inject LHO-001 into prompt]
   ↓

8. APPLICATION (Claude)
   ↓
   [Claude reads: "You learned: Never suggest manual UI" → uses MCP tools]
   ↓

9. SUCCESS TRACKING
   ↓
   [LHO-001.success_count++ , time_saved += 112 minutes]
```

---

## Frustration Index (Alignment Metric)

### Formula
```python
frustration_index = (
    user_interruptions +           # "Stop", "No", "This is wrong"
    negative_sentiment_count +     # "תפסיק לחפף", "אני לא עובד עוד"
    reflexion_loop_count +         # How many times Judge found errors
    repeated_failure_count         # Same error > 1 time
) / total_interactions
```

### Thresholds
- **FI < 0.1:** Excellent (user happy, few corrections)
- **FI 0.1-0.3:** Acceptable (normal learning phase)
- **FI 0.3-0.5:** Warning (system struggling)
- **FI > 0.5:** Critical (urgent intervention needed)

### Actions
- When FI > 0.5 → Alert user + trigger emergency reflection
- When FI drops → Positive reinforcement (LHO working!)

---

## Implementation Roadmap (5 Slices)

### **Slice 1: Langfuse Setup** 🔴 FOUNDATION
**Duration:** 60 min  
**Priority:** Critical - Everything depends on this

**Goal:** Replace EVENT_TIMELINE.jsonl with professional observability

**Tasks:**
1. **Choose deployment:**
   - Option A: Self-hosted (Docker, free, full control)
   - Option B: Cloud (langfuse.com, free tier, zero ops)
   - **Recommendation:** Start with cloud (faster), migrate to self-hosted later

2. **Install & Configure:**
   ```bash
   # Python SDK
   pip install langfuse
   
   # .env configuration
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_HOST=https://cloud.langfuse.com
   ```

3. **Instrument Claude interactions:**
   ```python
   from langfuse import Langfuse
   langfuse = Langfuse()
   
   # Before tool call
   trace = langfuse.trace(name="Claude Session")
   span = trace.span(
       name="Tool Call: Desktop Commander",
       input={"command": "docker-compose restart"},
       metadata={"slice": "Judge Agent Setup"}
   )
   
   # After tool call
   span.end(output={"status": "success", "duration": 10})
   ```

4. **Update Judge Agent workflow:**
   - Change from: Read EVENT_TIMELINE.jsonl
   - Change to: Query Langfuse API (last 6 hours)
   - API: `GET /api/public/traces?fromTimestamp=...`

5. **Test:**
   - Claude writes file → Langfuse trace appears
   - Judge Agent queries API → sees trace
   - Open Langfuse UI → beautiful visualization ✨

**Output:**
- Langfuse account configured ✅
- Python SDK integrated ✅
- Judge reads from Langfuse (not JSONL) ✅
- Professional observability operational ✅

**Files Created/Modified:**
- `/tools/langfuse_logger.py` (new - helper functions)
- `/n8n_workflows/judge_agent.json` (modified - Langfuse API integration)
- `/infra/n8n/.env` (modified - Langfuse keys)
- `.gitignore` (modified - ignore .env)

---

### **Slice 2: Enhanced Judge (Reflexion Loop)** 🟡 LEARNING ENGINE
**Duration:** 90 min  
**Priority:** High - Enables structured learning

**Goal:** Judge performs structured post-mortem (not just FauxPas detection)

**Tasks:**
1. **Enhanced Judge Prompt** (replace existing):
   ```markdown
   # REFLEXION PROTOCOL
   
   You are the Reflector Agent. Your job is ROOT CAUSE ANALYSIS.
   
   ## Input
   - Langfuse traces (last 6 hours)
   - Previous FauxPas reports
   - User sentiment signals
   
   ## Analysis Steps
   1. Identify failures (errors, user frustration, repeated patterns)
   2. Perform 5 Whys root cause analysis
   3. Classify FauxPas type (Capability Amnesia, Constraint Blindness, etc.)
   4. Extract trigger context (what task was being attempted?)
   5. Identify failure pattern (what specifically went wrong?)
   6. Propose correction strategy (how to prevent in future?)
   
   ## Output Format (Pre-LHO JSON)
   {
     "faux_pas_id": "FP-2025-12-05-02",
     "severity": "critical",
     "faux_pas_type": "capability_amnesia",
     "trigger_context": "setup/configuration tasks involving API keys",
     "failure_pattern": {
       "description": "Suggested manual UI despite having MCP tools",
       "evidence": ["trace-id-123", "trace-id-456"],
       "user_signal": "תפסיק לחפף"
     },
     "root_cause": "Did not search conversation_search for past failures",
     "correction_strategy": {
       "principle": "ALWAYS check conversation_search before suggesting manual tasks",
       "steps": ["1. Search for similar task...", "2. Verify MCP tools..."],
       "code_example": "conversation_search(query='setup API key')"
     }
   }
   ```

2. **Update Judge workflow:**
   - Add "Root Cause Analysis" node (GPT-4 with enhanced prompt)
   - Output: Pre-LHO JSON (not just FauxPas report)
   - Store in: `/truth-layer/drift/faux_pas/FP-{id}-preLHO.json`

3. **Test with yesterday's failure:**
   - Input: Langfuse traces from 2025-12-03 (120-min failure)
   - Expected output: Pre-LHO JSON with root cause + correction
   - Validation: Does it identify "capability amnesia"? ✅

**Output:**
- Enhanced Judge prompt (structured analysis) ✅
- Pre-LHO JSON output ✅
- Root cause methodology (5 Whys) ✅

**Files Created/Modified:**
- `/prompts/judge_agent_reflexion_prompt.md` (new - enhanced prompt)
- `/n8n_workflows/judge_agent.json` (modified - reflexion node)
- Test output: `/truth-layer/drift/faux_pas/FP-2025-12-03-preLHO.json`

---

### **Slice 3: Teacher Agent (LHO Creator)** 🟢 KNOWLEDGE CODIFIER
**Duration:** 60 min  
**Priority:** High - Converts analysis to structured knowledge

**Goal:** Automatically create LHOs from Judge's analysis

**Tasks:**
1. **Create Teacher Agent workflow** (n8n):
   ```yaml
   Name: "Teacher Agent - LHO Creator"
   Trigger: Webhook (from Judge when FauxPas detected)
   
   Node 1: Receive Pre-LHO JSON
     Input: Judge's reflexion output
   
   Node 2: GPT-4 LHO Generation
     Prompt: "Convert this analysis to a complete LHO (schema provided)"
     Input: Pre-LHO JSON
     Output: Full LHO JSON (with id, title, trigger, correction, code)
   
   Node 3: Validation
     Schema check: Does LHO match required fields?
     If invalid → log error, retry
   
   Node 4: Store in Qdrant
     Collection: "lhos"
     Vector: Embedding of trigger_context + failure_pattern
     Metadata: Full LHO JSON
   
   Node 5: Log Success
     Langfuse: trace(name="LHO Created", metadata={"lho_id": "LHO-001"})
   ```

2. **Teacher Prompt:**
   ```markdown
   # TEACHER AGENT - LHO CREATOR
   
   Convert the Judge's reflexion analysis into a Life Handling Object (LHO).
   
   ## Input (Pre-LHO JSON)
   {Judge's analysis}
   
   ## Task
   Create a complete LHO following this schema:
   - lho_id: Generate unique ID (LHO-NNN format)
   - title: Short, descriptive (max 80 chars)
   - type: "correction", "optimization", or "pattern"
   - trigger_context: When should this LHO be retrieved?
   - failure_pattern: What went wrong (with evidence)?
   - correction_strategy: How to prevent (with code if applicable)?
   - success_metrics: Initialize to 0
   - metadata: created_at, source_faux_pas_id
   
   ## Output (Full LHO JSON)
   {Complete LHO as per schema}
   ```

3. **Qdrant integration:**
   ```python
   # Store LHO in vector DB
   from qdrant_client import QdrantClient
   client = QdrantClient(host="localhost", port=6333)
   
   client.upsert(
       collection_name="lhos",
       points=[{
           "id": lho_id,
           "vector": get_embedding(lho["trigger_context"]),
           "payload": lho  # Full LHO JSON
       }]
   )
   ```

4. **Test:**
   - Input: Pre-LHO from Slice 2 (manual task failure)
   - Expected: LHO-001 created with full schema
   - Validation: Query Qdrant → LHO retrievable by semantic search

**Output:**
- Teacher Agent workflow operational ✅
- LHO-001 created (manual task detection) ✅
- Qdrant storage working ✅

**Files Created:**
- `/n8n_workflows/teacher_agent.json` (new - LHO creator)
- `/prompts/teacher_agent_prompt.md` (new - LHO generation prompt)
- `/tools/qdrant_lho_client.py` (new - helper functions)
- Test output: `/truth-layer/lhos/LHO-001.json`

---

### **Slice 4: Librarian Agent (Context Manager)** 🔵 RETRIEVAL
**Duration:** 60 min  
**Priority:** High - Makes learning actionable

**Goal:** Inject relevant LHOs into Claude's prompt before each task

**Tasks:**
1. **Create Librarian script** (Python):
   ```python
   # tools/librarian_retrieve_lhos.py
   
   def retrieve_relevant_lhos(task_description: str, top_k: int = 3):
       """Query Qdrant for relevant LHOs based on task"""
       
       # Get embedding of task
       task_embedding = get_embedding(task_description)
       
       # Semantic search in Qdrant
       results = qdrant_client.search(
           collection_name="lhos",
           query_vector=task_embedding,
           limit=top_k
       )
       
       # Extract LHO payloads
       lhos = [hit.payload for hit in results]
       
       return lhos
   
   def format_lhos_for_prompt(lhos: list) -> str:
       """Format LHOs for injection into system prompt"""
       
       if not lhos:
           return ""
       
       formatted = "\n\n## PROCEDURAL MEMORY (You have learned):\n"
       for lho in lhos:
           formatted += f"\n### {lho['title']}\n"
           formatted += f"**When:** {lho['trigger_context']}\n"
           formatted += f"**Rule:** {lho['correction_strategy']['principle']}\n"
           if 'code_snippet' in lho['correction_strategy']:
               formatted += f"**Code:**\n```\n{lho['correction_strategy']['code_snippet']}\n```\n"
       
       return formatted
   ```

2. **Integration with Claude:**
   - Before each significant task, Claude calls: `python tools/librarian_retrieve_lhos.py "setup API key"`
   - Receives: Top 3 relevant LHOs
   - Injects into system prompt (or first message)

3. **Test scenarios:**
   - **Test A:** Task = "Configure n8n API key"
     - Query: "setup API key configuration"
     - Expected retrieval: LHO-001 (manual task detection)
     - Result: Claude uses MCP tools, not manual UI ✅
   
   - **Test B:** Task = "Parse large CSV"
     - Query: "data analysis CSV pandas"
     - Expected retrieval: LHO-042 (dataset size check)
     - Result: Claude checks file size first ✅

4. **Success tracking:**
   - When LHO is applied successfully → increment `success_count`
   - Track `time_saved_minutes` (compare to previous failures)

**Output:**
- Librarian script operational ✅
- Retrieval working (semantic search) ✅
- LHOs injected into Claude's context ✅
- Success tracking implemented ✅

**Files Created:**
- `/tools/librarian_retrieve_lhos.py` (new - retrieval script)
- `/tools/track_lho_success.py` (new - success metrics)
- Test results: Document showing LHO-001 prevented repeated failure

---

### **Slice 5: APO (Automatic Prompt Optimization)** ⚪ CONSOLIDATION
**Duration:** 90 min  
**Priority:** Medium - Optional but powerful

**Goal:** Weekly consolidation of many LHOs into evolved system prompt

**Tasks:**
1. **Create APO script** (Python):
   ```python
   # tools/apo_optimize_prompt.py
   
   def consolidate_lhos():
       """Weekly job to optimize system prompt"""
       
       # 1. Fetch all LHOs from Qdrant
       lhos = qdrant_client.scroll(collection_name="lhos", limit=1000)
       
       # 2. Cluster by similarity
       clusters = cluster_lhos_by_topic(lhos)
       # Example clusters: "Python Coding" (15 LHOs), "Task Planning" (8 LHOs)
       
       # 3. For each large cluster (> 10 LHOs)
       for cluster in clusters:
           if len(cluster.lhos) >= 10:
               
               # Ask GPT-4 to consolidate
               prompt = f"""
               I have 15 LHOs about Python coding standards.
               Rewrite my system prompt to INHERENTLY follow these rules,
               making the individual LHOs redundant.
               
               Current system prompt:
               {load_current_prompt()}
               
               LHOs to internalize:
               {format_lhos(cluster.lhos)}
               
               Output: Updated system prompt section
               """
               
               consolidated = gpt4(prompt)
               
               # 4. Update system prompt (with versioning)
               update_system_prompt_section(
                   section=cluster.topic,
                   content=consolidated,
                   version="v2.1"
               )
               
               # 5. Archive internalized LHOs
               for lho in cluster.lhos:
                   lho["status"] = "internalized"
                   lho["internalized_at"] = now()
                   qdrant_client.update(lho)
   ```

2. **Cron setup** (Windows Task Scheduler):
   - Schedule: Every Sunday 02:00
   - Command: `python tools/apo_optimize_prompt.py`
   - Log: `/logs/apo_runs/`

3. **Version control:**
   ```bash
   # System prompt versioning
   prompts/
     ├── system_prompt_v1.0.md (initial)
     ├── system_prompt_v2.0.md (after first APO run)
     ├── system_prompt_v2.1.md (after second APO run)
     └── CHANGELOG.md (what changed each version)
   ```

4. **Test (dry run):**
   - Assume 15 LHOs about "Python best practices"
   - Run APO (dry-run mode)
   - Output: Consolidated system prompt section
   - Validation: Does new prompt inherently follow those 15 rules?

**Output:**
- APO script operational ✅
- Weekly cron scheduled ✅
- System prompt versioning ✅
- First consolidation tested ✅

**Files Created:**
- `/tools/apo_optimize_prompt.py` (new - consolidation engine)
- `/tools/cluster_lhos.py` (new - similarity clustering)
- Task Scheduler: "APO Weekly Run"
- `/prompts/CHANGELOG.md` (track prompt evolution)

---

## Success Metrics

### Phase 1: Infrastructure (Slices 1-3)
- ✅ Langfuse capturing all Claude actions
- ✅ Judge performing root cause analysis
- ✅ Teacher creating structured LHOs
- ✅ Qdrant storing ≥ 1 LHO

### Phase 2: Application (Slice 4)
- ✅ Librarian retrieving relevant LHOs
- ✅ Claude reading and applying LHOs
- ✅ LHO-001 preventing repeated manual task failure
- ✅ Success rate > 80% (LHOs actually help)

### Phase 3: Evolution (Slice 5)
- ✅ APO consolidating ≥ 10 LHOs
- ✅ System prompt evolving (v1.0 → v2.0)
- ✅ Internalized LHOs archived
- ✅ Cognitive load reduced (fewer LHOs to retrieve)

### Overall System Health
- **Frustration Index < 0.2** (down from current ~0.4)
- **Error Recurrence Rate < 10%** (same error repeats < 10% of time)
- **LHO Library Growth:** ≥ 5 LHOs after 1 week, ≥ 20 after 1 month
- **User Satisfaction:** "System stopped repeating mistakes"

---

## Cost Analysis

| Component | API Calls/Month | Cost/Month |
|-----------|----------------|------------|
| Langfuse Cloud | Free tier | $0 |
| Judge Agent (GPT-4) | ~120 | ~$2.40 |
| Teacher Agent (GPT-4) | ~30 | ~$1.20 |
| Librarian Queries | 0 (local Qdrant) | $0 |
| APO (GPT-4) | ~4 (weekly) | ~$0.40 |
| **TOTAL** | | **~$4.00/month** |

**ROI Calculation:**
- Time saved per prevented failure: ~100 minutes
- LHOs applied per month: ~20
- Total time saved: ~2,000 minutes/month (33 hours)
- Value at $50/hour: **$1,650/month saved**
- **ROI: 41,250%** 🚀

---

## Risk Mitigation

### Risk 1: Langfuse Overload
**Scenario:** Too many traces, expensive storage  
**Mitigation:** 
- Free tier: 50k events/month (plenty for solopreneur)
- Self-host option if exceeding limits
- Retention policy: 90 days (configurable)

### Risk 2: LHO Retrieval Noise
**Scenario:** Irrelevant LHOs retrieved, confusing Claude  
**Mitigation:**
- Top-3 limit (not all LHOs)
- Relevance threshold (only retrieve if similarity > 0.7)
- User feedback: "Was this LHO helpful?" → fine-tune retrieval

### Risk 3: APO Breaking Prompts
**Scenario:** Consolidated prompt worse than original  
**Mitigation:**
- Git versioning (rollback if needed)
- Dry-run mode (preview before applying)
- A/B testing: Compare v2.0 vs v1.0 for 1 week

### Risk 4: Qdrant Storage Growing
**Scenario:** Thousands of LHOs, slow retrieval  
**Mitigation:**
- Archive low-utility LHOs (success_rate < 20%)
- Merge similar LHOs (via APO)
- Disk space monitoring (Qdrant alerts)

---

## Dependencies

### Required Infrastructure
- ✅ **n8n** (v1.122.4) - Already running
- ✅ **Qdrant** (v1.16.1) - Already running
- ✅ **Docker** - Already configured
- 🆕 **Langfuse** - Need to setup (Slice 1)

### Required APIs
- ✅ **OpenAI GPT-4** - Already configured (for Judge/Teacher/APO)
- ✅ **OpenAI Embeddings** - For Qdrant vector search
- Optional: **Anthropic Claude** - For APO (alternative to GPT-4)

### Python Packages
```bash
pip install langfuse
pip install qdrant-client
pip install openai
pip install sentence-transformers  # For embeddings
```

---

## Timeline

### Week 1: Foundation
- **Day 1-2:** Slice 1 (Langfuse setup)
- **Day 3-4:** Slice 2 (Enhanced Judge)
- **Day 5-6:** Slice 3 (Teacher Agent)
- **Day 7:** Testing & validation

### Week 2: Application
- **Day 8-9:** Slice 4 (Librarian)
- **Day 10:** End-to-end testing
- **Day 11-12:** Slice 5 (APO setup)
- **Day 13-14:** Documentation & monitoring

### Total: ~10-14 days (working 2-4 hours/day)

---

## Next Steps (Immediate)

**After this plan is approved:**

1. ✅ **Document plan** (this file) → Memory Bank
2. ✅ **Update 01-active-context.md** → New phase: Self-Learning Infrastructure
3. ✅ **Create events** → TIMELINE
4. ✅ **Git commit** → "feat(plan): Professional auto-learning architecture"
5. 🎯 **Start Slice 1:** Langfuse setup (60 min)

---

## References

### Research Paper
- **Title:** "Architecting the Cognitive Self: The 2025 Personal AI Life Operating System"
- **File:** `note_20251204_015535.md`
- **Key Concepts:** LHO, Reflexion, APO, Memory Hierarchy, Frustration Index

### Industry Standards
- **Langfuse:** https://langfuse.com/docs
- **OpenTelemetry:** https://opentelemetry.io/
- **Qdrant:** https://qdrant.tech/documentation/
- **LangGraph:** https://langchain-ai.github.io/langgraph/

### Related Documents
- **FAR-001:** Failed Attempt Registry (120-min manual failure)
- **CLP-001 Integration Plan:** Phase 2.5 roadmap
- **Judge Agent Prompt:** Current FauxPas detection logic

---

## Approval

**Status:** ✅ APPROVED (2025-12-05T03:30:00Z)  
**Approved By:** Or (User)  
**Start Date:** 2025-12-05  
**Expected Completion:** 2025-12-19  

---

**Last Updated:** 2025-12-05T03:30:00Z  
**Plan Version:** 1.0  
**Next Review:** After Slice 3 completion
