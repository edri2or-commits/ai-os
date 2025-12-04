# CLP-001 Integration Plan: Self-Learning Architecture for AI Life OS

**Document Status:** Draft v1.0  
**Created:** 2025-12-04  
**Author:** Claude (Agentic Kernel Architect)  
**Purpose:** Integration roadmap for Continuous Learning Protocol into existing AI Life OS

---

## Executive Summary

**What:** Integrate CLP-001 (Continuous Learning Protocol) to enable autonomous self-improvement through Judge/Teacher/Librarian agents operating in a Slow Loop.

**Why:** Current system (Phase 1-2) has robust execution (Fast Loop) but no learning mechanism. The AI repeats errors across sessions because there's no feedback loop to convert failures into permanent knowledge artifacts (LHOs).

**How:** Extend existing MAPE-K architecture with CLP-001's dual-loop pattern:
- **Fast Loop** (existing): Observer → Reconciler → Executor (synchronous, user-facing)
- **Slow Loop** (new): Judge → Teacher → Librarian (asynchronous, background learning)

**Current State:** Phase 2 (~20% complete) - Architecture aligned, automation operational, no self-learning yet.

**Decision Point:** Complete Phase 2 (governance) OR pivot to Phase 2.5 (self-learning) now.

**Recommendation:** **Start Phase 2.5 now** - the infrastructure is ready, and self-learning has higher strategic value than Vale enforcement.

---

## 1. Current State Mapping: What We Have

### 1.1 Existing Architecture (ADR-001: Hexagonal + MAPE-K)

**MAPE-K Control Loop (Phase 1 Complete):**

| MAPE-K Phase | AI Life OS Component | Status | Function |
|--------------|---------------------|--------|----------|
| **Monitor** | Observer | ✅ Operational | Detects drift (Git HEAD vs Truth Layer, schema violations, orphaned entities) |
| **Analyze** | Reconciler (detect) | ✅ Operational | Generates Change Requests (CRs) with risk assessment |
| **Plan** | Reconciler (propose) | ✅ Operational | Creates action plans (JSON proposals) |
| **Execute** | Reconciler (apply) | ✅ Operational | Applies approved CRs with safety checks |
| **Knowledge** | Truth Layer (Git) | ✅ Operational | Persistent state (Markdown/YAML/JSON) |

**Supporting Infrastructure:**
- ✅ **n8n** (Docker): Automation engine, workflow orchestrator
- ✅ **Qdrant** (Docker): Vector database for semantic search
- ✅ **Desktop Commander MCP**: Subprocess management, file operations
- ✅ **Memory Bank**: Structured knowledge (PARA pattern)
- ✅ **Task Scheduler**: 3 automated processes (Observer 15 min, Watchdog, Email Watcher)

**What's Missing:**
- ❌ **Learning Loop**: No feedback from failures to future behavior
- ❌ **Judge Agent**: No automated error detection across sessions
- ❌ **Teacher Agent**: No lesson synthesis from errors
- ❌ **Librarian Agent**: No memory curation/optimization
- ❌ **LHO Database**: No structured storage for learned heuristics
- ❌ **APO (Automatic Prompt Optimization)**: No self-modification of System Prompt

---

## 2. CLP-001 Architecture Overview (From Research)

### 2.1 The Dual-Loop Pattern

**Fast Loop (Synchronous - User-Facing):**
```
User Query → Context Manager → LLM (Claude) → Tools (MCP) → Output → Logs
```
- **Goal:** Low latency, direct task execution
- **Analogy:** "System 1" thinking (Daniel Kahneman)
- **Current Status:** ✅ This is our Observer → Reconciler → Executor

**Slow Loop (Asynchronous - Background Learning):**
```
Logs → Judge (detect errors) → Teacher (synthesize lessons) → Librarian (update Memory Bank) → LHOs → Next Fast Loop
```
- **Goal:** Deep reflection, permanent learning
- **Analogy:** "System 2" thinking (Kahneman)
- **Current Status:** ❌ Completely missing

### 2.2 The Three Learning Agents

**1. Judge Agent (The Auditor)**
- **Role:** Scans interaction logs for "Faux Pas" (4 types from Research #2)
- **Input:** Event logs (EVENT_TIMELINE.jsonl) + session traces (Langfuse)
- **Output:** FauxPas_Report.json (identifies errors with severity + root cause)
- **LLM:** GPT-4o or Claude 3.5 Opus (needs reasoning depth)
- **Trigger:** Every N hours (batch processing) OR after user flags issue

**Faux Pas Taxonomy (Research #2):**
1. **Capability Amnesia** - Forgot how to do task (e.g., used regex when Python tool exists)
2. **Constraint Blindness** - Ignored rule (e.g., modified file in `/legacy/` when forbidden)
3. **Loop Paralysis** - Got stuck in retry loop (e.g., import error 5x)
4. **Hallucinated Affordances** - Invented tool parameter that doesn't exist

**2. Teacher Agent (The Synthesizer)**
- **Role:** Converts FauxPas_Report into actionable LHO (Learned Heuristic Object)
- **Input:** FauxPas_Report.json
- **Output:** LHO (JSON schema with correction_strategy, trigger_pattern, priority)
- **LLM:** GPT-4o-mini or Claude 3.5 Sonnet (speed + cost balance)
- **Example LHO:**
```json
{
  "lho_id": "LHO-042",
  "title": "Always use Python tool for CSV parsing",
  "trigger_pattern": "task contains 'CSV' AND tool_options includes 'python_csv'",
  "correction_strategy": "Before parsing CSV, call python_csv tool, not regex",
  "priority": "high",
  "created_at": "2025-12-04T15:30:00Z",
  "faux_pas_source": "FP-2025-12-04-001"
}
```

**3. Librarian Agent (The Curator)**
- **Role:** Manages LHO database - deduplication, consolidation, archival
- **Input:** New LHOs + existing LHO database
- **Output:** Updated LHO index, merged/archived LHOs
- **LLM:** GPT-4o-mini (lightweight curation task)
- **Functions:**
  - Detect duplicate LHOs (vector similarity > 0.9)
  - Merge related LHOs (e.g., 3 CSV rules → 1 comprehensive rule)
  - Archive obsolete LHOs (e.g., tool deprecated)
  - Update Memory Bank index for retrieval

### 2.3 LHO Lifecycle

```
1. Error Occurs (Fast Loop)
   ↓
2. Logged to EVENT_TIMELINE.jsonl
   ↓
3. Judge detects error (Slow Loop triggered)
   ↓
4. Teacher creates LHO
   ↓
5. Librarian indexes LHO in Qdrant
   ↓
6. Next Fast Loop: Context Manager retrieves relevant LHOs → injects into System Prompt
   ↓
7. Error prevented ✅
```

---

## 3. Gap Analysis: What's Missing

### 3.1 Architecture Gaps

| Component | Current State | CLP-001 Required | Gap |
|-----------|---------------|------------------|-----|
| **Interaction Logs** | EVENT_TIMELINE.jsonl (basic) | Structured traces with tool calls, latency, cost | Need Langfuse integration (Research #3) |
| **Error Detection** | Manual (user reports) | Automated (Judge scans logs) | Need Judge Agent + n8n workflow |
| **Lesson Storage** | Memory Bank (unstructured) | LHO database (structured) | Need Qdrant collection + schema |
| **Prompt Injection** | Static System Prompt | Dynamic (LHOs injected JIT) | Need Context Manager middleware |
| **APO** | None | Weekly optimization (DSPy/TextGrad) | Need optimization pipeline |

### 3.2 Technical Gaps

**1. Langfuse Integration (Observability)**
- **Why:** Current EVENT_TIMELINE.jsonl lacks detail (no tool call traces, no token costs)
- **What:** Self-hosted Langfuse (Docker) for structured telemetry
- **Effort:** Medium (3-4 slices)
- **Benefit:** High (enables Judge to see full reasoning chains)

**2. Judge Agent Workflow**
- **Why:** No automated error detection
- **What:** n8n workflow triggered every 6 hours → reads logs → calls Judge LLM → writes FauxPas_Report
- **Effort:** Low (1-2 slices)
- **Benefit:** High (autonomous error detection)

**3. LHO Database in Qdrant**
- **Why:** No structured storage for lessons
- **What:** New Qdrant collection `lhos` with schema (id, title, trigger, strategy, embedding)
- **Effort:** Low (1 slice)
- **Benefit:** High (retrieval for Context Manager)

**4. Context Manager (JIT Injection)**
- **Why:** System Prompt is static - doesn't adapt per task
- **What:** Middleware before LLM call: analyze task → query LHO database → inject relevant rules
- **Effort:** Medium (2-3 slices)
- **Benefit:** Critical (this is how learning affects behavior)

**5. Teacher/Librarian Agents**
- **Why:** No lesson synthesis or curation
- **What:** n8n workflows calling LLMs for each role
- **Effort:** Medium (2 slices)
- **Benefit:** Medium (automates learning pipeline)

**6. APO Pipeline (Optional Phase 3)**
- **Why:** LHOs accumulate → token bloat
- **What:** Weekly script uses DSPy/TextGrad to consolidate LHOs into System Prompt
- **Effort:** High (4-5 slices, requires research)
- **Benefit:** Medium (long-term optimization)
---

## 4. Integration Architecture: CLP-001 → MAPE-K + Hexagonal

### 4.1 Architectural Alignment with ADR-001

**ADR-001 establishes:**
- **Primary:** Hexagonal Architecture (Ports & Adapters)
- **Secondary:** MAPE-K Control Loop (autonomic behavior)

**CLP-001 fits naturally:**
- **Fast Loop** = MAPE-K loop (Monitor/Analyze/Plan/Execute)
- **Slow Loop** = Meta-MAPE-K loop (learns from MAPE-K traces)

**Hexagonal Mapping:**
```
┌─────────────────────────────────────────────────────────┐
│                  Application Core                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │          MAPE-K Control Loop (Fast Loop)        │   │
│  │  Monitor → Analyze → Plan → Execute → Knowledge │   │
│  └─────────────────────────────────────────────────┘   │
│                         ↕                                │
│  ┌─────────────────────────────────────────────────┐   │
│  │       Meta-MAPE-K (Slow Loop / CLP-001)         │   │
│  │    Judge → Teacher → Librarian → LHO Database   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
            ↕ (Ports)                    ↕
    ┌──────────────┐              ┌──────────────┐
    │   Primary     │              │  Secondary   │
    │   Adapters    │              │   Adapters   │
    │ (Driving)     │              │  (Driven)    │
    │               │              │              │
    │ • Claude      │              │ • MCP Servers│
    │   Desktop     │              │   (Desktop   │
    │               │              │   Commander) │
    │               │              │ • n8n Engine │
    │               │              │ • Qdrant DB  │
    │               │              │ • Git (Truth)│
    └──────────────┘              └──────────────┘
```

**Key Insight:** CLP-001 is a **Domain Logic** addition to Application Core, NOT a new adapter.

### 4.2 Component Integration Map

| CLP-001 Component | Maps To | Implementation | Storage |
|-------------------|---------|----------------|---------|
| **Fast Loop** | Existing MAPE-K | Observer/Reconciler/Executor | EVENT_TIMELINE.jsonl |
| **Slow Loop Trigger** | n8n Workflow | Cron trigger (every 6 hours) | n8n Docker |
| **Judge Agent** | LLM Call (n8n node) | GPT-4o API via n8n HTTP node | FauxPas_Reports/ |
| **Teacher Agent** | LLM Call (n8n node) | Claude 3.5 Sonnet API | LHOs/ (JSON) |
| **Librarian Agent** | LLM Call (n8n node) | GPT-4o-mini API | Qdrant (lhos collection) |
| **LHO Storage** | Qdrant Collection | Vector DB with metadata | Qdrant Docker |
| **Context Manager** | Python Middleware | Pre-LLM hook in Observer | In-memory (runtime) |
| **Observability** | Langfuse (Optional) | Self-hosted Docker stack | Postgres (Langfuse) |

### 4.3 Data Flow Diagram

**Fast Loop (Current - No Learning):**
```
User Request → Observer (detect drift) → Reconciler (propose CR) → User Approval → Executor (apply) → Git Commit
                                    ↓ (logged)
                          EVENT_TIMELINE.jsonl
```

**With CLP-001 (Self-Learning):**
```
User Request → [Context Manager checks LHO DB] → Observer → Reconciler → Executor → Git
                        ↑ (retrieves relevant LHOs)              ↓ (logs)
                    Qdrant                              EVENT_TIMELINE.jsonl
                                                              ↓
                                                    (every 6 hours)
                                                        Judge Agent
                                                              ↓
                                                    FauxPas_Report.json
                                                              ↓
                                                       Teacher Agent
                                                              ↓
                                                       LHO (new rule)
                                                              ↓
                                                      Librarian Agent
                                                              ↓
                                                   Qdrant (index LHO)
                                                              ↓
                                         (next Fast Loop uses this LHO) ✅
```

### 4.4 n8n Workflow Architecture

**Workflow 1: Slow Loop Orchestrator**
- **Trigger:** Cron (every 6 hours)
- **Nodes:**
  1. Read EVENT_TIMELINE.jsonl (last 6 hours)
  2. HTTP Request → Judge Agent (GPT-4o API)
  3. Parse JSON → FauxPas_Report
  4. IF errors found:
     - HTTP Request → Teacher Agent (Claude API)
     - Parse JSON → LHO
     - HTTP Request → Librarian Agent (GPT-4o-mini API)
     - Write to Qdrant (lhos collection)
     - Telegram notification: "Learned new rule: {LHO.title}"
  5. ELSE: Log "No errors detected"

**Workflow 2: Context Manager (Runtime)**
- **Trigger:** Before every Observer execution
- **Nodes:**
  1. Extract task keywords from user request
  2. Query Qdrant (lhos collection) with keywords
  3. Retrieve top 3 relevant LHOs
  4. Inject LHOs into System Prompt (temp augmentation)
  5. Execute Observer with augmented prompt

---

## 5. Phasing Decision: Phase 2 vs Phase 2.5

### 5.1 Option A: Complete Phase 2 First (Governance)

**Remaining Phase 2 Work:**
1. **Slice 2.2:** Vale Enforcement (45 min) - automated terminology drift prevention
2. **Slice 2.3:** Update research docs with canonical terms (60 min)
3. **Slice 2.4:** Documentation sweep - ensure all docs reference ADR-001

**Total Effort:** ~3 slices (~3 hours)

**Pros:**
- ✅ Completes architectural cleanup (single source of truth for terminology)
- ✅ Prevents future drift (Vale blocks forbidden terms)
- ✅ Methodical approach (finish one phase before starting next)

**Cons:**
- ❌ Low strategic value (Vale is "nice to have", not "must have")
- ❌ Delays high-value work (self-learning has compounding returns)
- ❌ ADHD risk: Vale enforcement is tedious, may cause motivation loss

**Estimated Timeline:**
- Phase 2 complete: 1 week
- Phase 2.5 start: Week 2

---

### 5.2 Option B: Start Phase 2.5 Now (Self-Learning) ⭐ RECOMMENDED

**Rationale:**
1. **Infrastructure is Ready:**
   - ✅ n8n operational (Docker 24/7)
   - ✅ Qdrant operational (vector DB ready)
   - ✅ Event logging exists (EVENT_TIMELINE.jsonl)
   - ✅ MCP tools functional (Desktop Commander)
   
2. **High Strategic Value:**
   - 🚀 Self-learning has **compounding returns** - every LHO makes system smarter forever
   - 🚀 Addresses **root cause** of user frustration (repeated errors)
   - 🚀 **ADHD-friendly:** System learns user's patterns, reduces cognitive load over time

3. **Low Risk:**
   - Slow Loop is **async** - can't break Fast Loop
   - n8n workflows are **sandboxed** - can test without affecting production
   - LHOs are **additive** - can delete/archive bad ones

4. **Motivation Preservation:**
   - Vale enforcement = tedious cleanup work (motivation killer)
   - Self-learning = exciting new capability (dopamine hit)
   - Research papers = already absorbed, momentum exists

**Phase 2 Completion:**
- Vale can wait (or be automated via LHO in Phase 2.5!)
- Research docs update is low priority (historical reference)
- ADR-001 enforcement via Vale can be Slice 2.5.8 (after core learning works)

**Estimated Timeline:**
- Slice 2.5.1 (Langfuse setup): Week 1
- Slice 2.5.2-2.5.5 (Judge/Teacher/Librarian): Week 2-3
- Slice 2.5.6 (Context Manager): Week 4
- Phase 2 cleanup (if needed): Week 5

---

## 6. Phase 2.5 Roadmap: Self-Learning Implementation

### 6.1 Slice Breakdown

**Slice 2.5.1: Langfuse Observability (60 min)** 🔬
- **Goal:** Structured telemetry for Judge Agent
- **Tasks:**
  1. Docker Compose: Add Langfuse service (Postgres + Clickhouse)
  2. Install Langfuse Python SDK (`pip install langfuse`)
  3. Instrument Observer: Wrap with `@observe()` decorator
  4. Test: Trigger Observer → Verify traces appear in Langfuse UI
- **Output:** Full interaction traces with tool calls, latency, token costs
- **Validation:** Open http://localhost:3000 → See Observer trace ✅

**Slice 2.5.2: LHO Database Schema (45 min)** 📦
- **Goal:** Qdrant collection for learned heuristics
- **Tasks:**
  1. Create Qdrant collection `lhos` (vector_size=1536 for OpenAI embeddings)
  2. Define LHO JSON schema (id, title, trigger, strategy, priority, created_at)
  3. Test: Manual insert of LHO-001 ("Always use Python for CSVs")
  4. Test: Query by keyword "CSV" → Retrieve LHO-001 ✅
- **Output:** `life-graph/schemas/lho_schema.json` + Qdrant collection
- **Validation:** Query returns LHO with cosine similarity > 0.8

**Slice 2.5.3: Judge Agent Workflow (60 min)** ⚖️
- **Goal:** Automated error detection
- **Tasks:**
  1. n8n workflow: Cron trigger (every 6 hours)
  2. Node: Read EVENT_TIMELINE.jsonl (last 6 hours using jq filter)
  3. Node: HTTP Request → OpenAI API (GPT-4o) with Judge prompt
  4. Judge Prompt Template: "Analyze these logs for Faux Pas (types 1-4). Return JSON: {errors: [{type, severity, description, root_cause}]}"
  5. Node: Write FauxPas_Report to `truth-layer/drift/faux_pas/YYYY-MM-DD-HH.json`
  6. Test: Force an error (modify forbidden file) → Wait 6 hours → Check report ✅
- **Output:** `n8n_workflows/judge_agent.json` + automated reports
- **Validation:** Report correctly identifies forced error

**Slice 2.5.4: Teacher Agent Workflow (60 min)** 👨‍🏫
- **Goal:** Convert errors into lessons
- **Tasks:**
  1. Extend Judge workflow: IF errors found → trigger Teacher
  2. Node: HTTP Request → Anthropic API (Claude 3.5 Sonnet) with Teacher prompt
  3. Teacher Prompt Template: "Given this error report, create an LHO (JSON schema). Provide: trigger_pattern (when to apply), correction_strategy (what to do instead), priority (high/medium/low)"
  4. Node: Parse LHO JSON
  5. Node: Write to `truth-layer/lhos/LHO-{timestamp}.json`
  6. Test: Force error → Wait for Judge → Wait for Teacher → Verify LHO created ✅
- **Output:** Automated LHO generation
- **Validation:** LHO JSON validates against schema, strategy is actionable

**Slice 2.5.5: Librarian Agent Workflow (45 min)** 📚
- **Goal:** Index LHOs in Qdrant for retrieval
- **Tasks:**
  1. Extend Teacher workflow: After LHO creation → trigger Librarian
  2. Node: Generate embedding (OpenAI `text-embedding-3-small` API)
  3. Node: Insert into Qdrant `lhos` collection with metadata
  4. Node: Update `truth-layer/lhos/INDEX.md` (human-readable list)
  5. Telegram notification: "🧠 Learned new rule: {LHO.title}"
  6. Test: LHO-001 indexed → Query "CSV parsing" → Returns LHO-001 ✅
- **Output:** Searchable LHO database
- **Validation:** Qdrant search returns relevant LHOs with similarity > 0.7

**Slice 2.5.6: Context Manager Integration (90 min)** 🧠
- **Goal:** LHOs actually affect behavior (JIT injection)
- **Tasks:**
  1. Create `tools/context_manager.py` (Python module)
  2. Function: `get_relevant_lhos(task_description: str) -> List[LHO]`
     - Query Qdrant with task keywords
     - Return top 3 LHOs (similarity > 0.7)
  3. Modify Observer: Before execution, call `get_relevant_lhos()`
  4. Inject LHOs into System Prompt: "LEARNED RULES:\n{LHO.strategy}\n\n"
  5. Test: Force CSV error again → Verify Observer now uses Python tool ✅
- **Output:** Self-correcting behavior
- **Validation:** Same error does NOT repeat (LHO prevents it)

**Slice 2.5.7: End-to-End Integration Test (60 min)** 🧪
- **Goal:** Prove the full loop works
- **Test Scenario:**
  1. Introduce novel error: "Modify file in /legacy/ directory" (forbidden by rule)
  2. Observer fails / user corrects
  3. Wait 6 hours → Judge detects error
  4. Teacher creates LHO: "Never modify /legacy/ - it's frozen"
  5. Librarian indexes LHO
  6. Next day: Try to modify /legacy/ again
  7. Context Manager injects LHO → Observer refuses ✅
- **Success Criteria:** Error prevented by learned rule (not hardcoded)
- **Documentation:** `memory-bank/docs/SELF_LEARNING_VALIDATION.md`

**Slice 2.5.8: Vale Enforcement (Optional - 45 min)** 🔒
- If desired, complete Phase 2 Vale enforcement now
- OR: Create LHO-002: "Use canonical terms from ADR-001" and let system self-enforce
- Recommendation: Let system learn terminology via LHOs (more elegant)

---

## 7. Success Metrics

### 7.1 Phase 2.5 Completion Criteria

**Functional:**
- ✅ Judge Agent runs every 6 hours, generates reports
- ✅ Teacher Agent creates LHOs from errors
- ✅ Librarian Agent indexes LHOs in Qdrant
- ✅ Context Manager retrieves + injects LHOs
- ✅ End-to-end test: Same error does NOT repeat

**Quality:**
- ✅ LHO database has ≥5 validated rules
- ✅ Context Manager retrieval accuracy ≥ 80% (relevant LHOs for task)
- ✅ User reports: "System stopped repeating [specific error]"

**Performance:**
- ✅ Slow Loop overhead < 5 min (doesn't block Fast Loop)
- ✅ Context Manager latency < 500ms (doesn't slow Observer)
- ✅ Qdrant query time < 100ms

### 7.2 Long-Term Impact (3 Months)

**Quantitative:**
- LHO database size: 20-50 rules
- Error recurrence rate: < 10% (same error repeats)
- User corrections per week: Decreasing trend (system learns)

**Qualitative:**
- User perception: "System is learning my preferences"
- ADHD benefit: Reduced cognitive load (less supervision needed)
- Trust: Increased (system proves it remembers lessons)

---

## 8. Risks & Mitigations

### 8.1 Technical Risks

**Risk 1: LHO Retrieval Noise**
- **Scenario:** Context Manager retrieves irrelevant LHOs → confuses Observer
- **Mitigation:** 
  - Similarity threshold 0.7 (strict filtering)
  - Top-K = 3 (limit context pollution)
  - User feedback loop: "Was this rule helpful?" → Update LHO priority

**Risk 2: Judge False Positives**
- **Scenario:** Judge flags normal behavior as error
- **Mitigation:**
  - Conservative Judge prompt: "Only flag clear errors, ignore ambiguous cases"
  - User review: Telegram notification includes FauxPas_Report → User can veto
  - Librarian deduplication: Prevents duplicate LHOs from false positives

**Risk 3: Slow Loop Performance**
- **Scenario:** Judge/Teacher/Librarian takes > 10 min → blocks n8n
- **Mitigation:**
  - Async design: Each agent is separate n8n workflow (can run parallel)
  - Timeout limits: 5 min per LLM call
  - Fallback: If timeout, skip learning for this cycle

### 8.2 ADHD-Specific Risks

**Risk 4: Complexity Overwhelm**
- **Scenario:** 7 slices feels like too much → motivation loss
- **Mitigation:**
  - Time-box: 30-60 min per slice (ADHD-friendly)
  - Quick wins: Slice 2.5.2 (LHO schema) shows immediate value
  - Optional slices: Langfuse (2.5.1) can be skipped initially (use EVENT_TIMELINE)

**Risk 5: Premature Optimization**
- **Scenario:** Get excited about APO (Phase 3) → skip foundation
- **Mitigation:**
  - Roadmap discipline: Complete 2.5.1-2.5.6 before APO
  - Archive APO ideas: `memory-bank/future/APO_BACKLOG.md` (revisit later)

---

## 9. Decision & Recommendation

### 9.1 The Decision

**Start Phase 2.5 (Self-Learning) NOW** ⭐

**Justification:**
1. **Infrastructure Ready:** n8n + Qdrant + logging = all prerequisites met
2. **High ROI:** Self-learning has compounding value (each LHO improves system forever)
3. **ADHD-Aligned:** Exciting work (not tedious cleanup) → better motivation
4. **Research Momentum:** 3 papers analyzed → context already loaded
5. **Strategic Priority:** Fixing repeated errors > enforcing terminology

**Phase 2 Completion:**
- Vale enforcement → Deferred to Slice 2.5.8 (or create LHO-002 for self-enforcement)
- Research docs update → Low priority (historical reference)
- ADR-001 already established (canonical architecture locked in)

### 9.2 Next Immediate Action

**Slice 2.5.1: Langfuse Observability** (60 min)

**User Action Required:**
1. Review this plan (CLP_001_INTEGRATION_PLAN.md)
2. Approve Phase 2.5 start
3. Confirm: Slice 2.5.1 (Langfuse) or skip to 2.5.2 (LHO schema)?

**Recommendation:** Skip Langfuse for now (optional optimization).  
**Start with:** Slice 2.5.2 (LHO Database Schema) - immediate, low-risk, high-visibility win.

---

## 10. References

**Research Papers (Analyzed):**
1. "Architecting the Cognitive Self" (note_20251204_015535.md)
   - LHOs, Frustration Index, CLP-001 pattern
2. "CLP-001 Specification" (note_clp_001.md)
   - Judge/Teacher/Librarian agents, Fast/Slow Loop, Faux Pas taxonomy
3. "Continuous Improvement Protocol" (note_20251203_113830.md)
   - Langfuse, Qdrant, DSPy/TextGrad, GitOps for Agents

**ADR-001:**
- memory-bank/docs/decisions/ADR-001-architectural-alignment.md
- Establishes Hexagonal + MAPE-K as canonical patterns

**Existing Infrastructure:**
- Observer: `truth-layer/drift/observer.py`
- Reconciler: `os_core_mcp/reconciler/`
- n8n workflows: n8n Docker instance
- Qdrant: Docker instance (port 6333)

---

**Document Version:** v1.0  
**Status:** Ready for User Review  
**Next Step:** Await approval to start Slice 2.5.1 or 2.5.2

---

**END OF DOCUMENT**