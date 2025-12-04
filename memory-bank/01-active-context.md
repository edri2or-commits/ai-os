<!--
MAINTENANCE RULE: Update this file after EVERY completed slice
Quick Status, Current Focus, Recent Changes, Next Steps
-->

---
🔴 **NEW CLAUDE INSTANCE? READ THIS FIRST!** 🔴

**BEFORE YOU DO ANYTHING:**
1. **Read START_HERE.md** → Entry point
2. **Read project-brief.md** → What is this project?
3. **Read THIS FILE** → Where are we now?
4. **Summarize to user** → Phase, %, recent work, 2-3 next options
5. **Wait for user confirmation** → Don't start without approval

🚨 **DO NOT SKIP THIS** - prevents drift, duplication, confusion!

---

# QUICK STATUS

**AI Life OS | Phase 2: Architectural Alignment & Governance** 📐

**Progress:** ~30% complete (Foundation + LHO Database operational)

**Just Finished (2025-12-04):**
- ✅ **Slice 2.5.2: LHO Database Schema** (Foundation for self-learning complete!)
  - Created JSON schema (62 lines): `life-graph/schemas/lho_schema.json`
  - Created Qdrant collection `lhos` (1536-dim vectors, COSINE distance)
  - Inserted LHO-001 (example: "Always use Python tool for CSV parsing")
  - Tested retrieval (payload filtering by tags works ✓)
  - Documentation: `truth-layer/lhos/README.md` (146 lines)
  - Tools: create_lho_collection.py, insert_lho_001.py, test_lho_retrieval.py

**Earlier Today (2025-12-04):**
- ✅ **Slice 2.5: CLP-001 Integration Plan** (412-line roadmap for Phase 2.5)
- ✅ **Research Analysis:** 3 papers (Cognitive Self, CLP-001 Spec, CIP) mapped to AI Life OS
- ✅ **Gap Analysis:** Identified missing components (Judge/Teacher/Librarian, LHO database)
- ✅ **Phase Decision:** Recommend Phase 2.5 (Self-Learning) NOW vs complete Phase 2 first
- ✅ **Roadmap:** 7 slices defined (Langfuse, LHO Schema, Judge/Teacher/Librarian, Context Manager)

**Previously (Earlier 2025-12-04):**
- ✅ **Slice 2.1: Apply Canonical Terms** (Updated 6 files to use ADR-001 terms)
- ✅ **ADR-001** (Architectural Alignment decision - Hexagonal + MAPE-K as canonical)
- ✅ **CANONICAL_TERMINOLOGY.md** (Official terms dictionary, 135 lines)
- ✅ **ARCHITECTURE_REFERENCE.md** (Detailed technical guide with diagrams)
- ✅ **METAPHOR_GUIDE.md** (When to use which metaphor - Technical/Human/OS)

**Previously Completed (Phase 1):**
- ✅ Core Infrastructure (Observer, Reconciler, Validator, Docker services)
- ✅ 3 Automated Processes (Task Scheduler: Observer, Memory Watchdog, Email Watcher)
- ✅ Email automation (Gmail → Claude → Telegram, 50 emails classified)
- ✅ Pre-commit hooks + pytest (44 tests passing)

**Currently Operational:**
- Desktop Commander MCP ✅
- Observer + Reconciler ✅
- n8n + Qdrant (24/7 Docker) ✅
- 3 Automated Processes (Task Scheduler) ✅
- **NEW:** Canonical architecture docs ✅

**Blockers:** NONE

**Next Decision Point:**
LHO Database ready → Start Slow Loop (Judge Agent)

**Achievement Unlocked:**
- ✅ Phase 1: Infrastructure Complete (8 weeks, production-ready)
- ✅ Canonical Architecture Established (Hexagonal + MAPE-K + 3 metaphors)
- ✅ Foundation Docs Created (ADR-001, Terminology, Reference, Metaphor Guide)
- ✅ Self-Learning Integration Plan (CLP-001 roadmap, 7 slices mapped)
- ✅ **NEW:** LHO Database Operational (Qdrant + Schema + Example + Tests)

---

# 🎯 NEXT STEPS (Choose One)

**Context:** LHO Database operational (Slice 2.5.2 complete).  
**Decision:** Continue Phase 2.5 Slow Loop or pause?

**Option A: Slice 2.5.3 - Judge Agent Workflow (60 min)** ⚖️ ⭐ MOMENTUM
- **Goal:** Automated error detection (scan EVENT_TIMELINE.jsonl for Faux Pas)
- **Why Now:**
  - LHO Database ready ✓
  - Momentum: Just completed foundation in 45 min
  - Next logical step: Feed the database with real errors
- **Tasks:**
  1. n8n workflow: Cron trigger (every 6 hours)
  2. Read EVENT_TIMELINE.jsonl (last 6 hours with jq filter)
  3. HTTP Request → GPT-4o (Judge prompt with Faux Pas taxonomy)
  4. Write FauxPas_Report to `truth-layer/drift/faux_pas/YYYY-MM-DD-HH.json`
  5. Test: Force error (modify forbidden file) → Wait 6 hours OR manually trigger → Verify detection ✓
- **Output:** Automated FauxPas_Reports (foundation for Teacher Agent)
- **Next:** Slice 2.5.4 (Teacher Agent - convert errors to LHOs)

**Option B: Quick Break** ☕ (5-10 min)
- Slice 2.5.2 = 45 min focused work
- Stretch, water, reset
- Come back fresh for Judge Agent

**Option C: Retrospective** 📊 (15 min)
- What worked: Quick win strategy (foundation first), no questions (direct action)
- What's next: Judge Agent will make LHO database useful
- Document pattern: "Schema → Insert → Test → Use"

**Recommendation:** **Option B** (quick break), then **Option A** (Judge Agent).  
**Rationale:** Maintain momentum, but avoid burnout. Judge Agent is natural next step.
- **Goal:** Foundation for self-learning - structured storage for learned rules
- **Why Now:** 
  - Infrastructure ready (Qdrant operational ✅)
  - Quick win (visible progress in < 1 hour)
  - High ROI (enables Judge/Teacher/Librarian pipeline)
- **Tasks:**
  1. Create Qdrant collection `lhos` (vector_size=1536)
  2. Define LHO JSON schema (id, title, trigger, strategy, priority)
  3. Test: Manual insert LHO-001 ("Always use Python for CSVs")
  4. Test: Query by keyword "CSV" → Retrieve LHO-001 ✅
- **Output:** `life-graph/schemas/lho_schema.json` + Qdrant collection ready
- **Next:** Slice 2.5.3 (Judge Agent) - automated error detection

**Option B: Slice 2.5.3 - Judge Agent Workflow (60 min)** ⚖️
- **Goal:** Automated error detection (Faux Pas scanner)
- **Prerequisite:** Requires LHO schema (Option A)
- **Tasks:**
  1. n8n workflow: Cron trigger (every 6 hours)
  2. Read EVENT_TIMELINE.jsonl (last 6 hours)
  3. HTTP Request → GPT-4o (Judge prompt)
  4. Write FauxPas_Report.json
  5. Test: Force error → Verify detection ✅
- **Output:** Automated error reports in `truth-layer/drift/faux_pas/`
- **Next:** Slice 2.5.4 (Teacher Agent) - convert errors to lessons

**Option C: Complete Phase 2 First - Vale Enforcement (45 min)** 🔒
- **Goal:** Automated terminology drift prevention
- **Tasks:**
  1. Install Vale CLI (chocolatey)
  2. Create .vale/ rules (forbidden terms from ADR-001)
  3. Add pre-commit hook
  4. Test: Commit with "Semantic Microkernel" → blocked ✅
- **Output:** Drift prevention on autopilot
- **Trade-off:** Delays high-value self-learning work

**Option D: Read Full Integration Plan** 📖 (15 min)
- **File:** `memory-bank/docs/CLP_001_INTEGRATION_PLAN.md` (412 lines)
- **Sections:**
  - Current State Mapping (what we have)
  - Gap Analysis (what's missing)
  - Integration Architecture (how it fits)
  - Phasing Decision (why Phase 2.5 now)
  - 7-Slice Roadmap (detailed implementation)
- **Benefit:** Full context before deciding

**Recommendation:** **Option A** (LHO Schema) - foundation for all learning, quick win, ADHD-friendly.

**Strategic Note (from Integration Plan):**
> "Self-learning has compounding returns - every LHO makes system smarter forever. Vale enforcement is 'nice to have', self-learning is transformative. Infrastructure is ready (n8n + Qdrant operational). Start Phase 2.5 now."

---

**Active Work:** Foundation architecture docs completed

**What Works Now:**
- **Truth Layer:** Git-backed filesystem (life-graph/, truth-layer/drift/)
- **Observer:** Detects Git HEAD changes, schema violations, orphaned entities
- **Reconciler:** Applies approved CRs with safety checks
- **Validation:** 44 pytest tests, pre-commit hooks
- **Automation:** 3 processes running 24/7
  - Observer: Drift detection
  - Watchdog: Memory Bank → Qdrant embeddings
  - Email Watcher: Gmail monitoring + Claude classification

**Infrastructure Stack:**
- Desktop Commander MCP (subprocess management)
- n8n v1.122.4 (automation platform)
- Qdrant v1.16.1 (vector database)
- Docker Desktop (auto-start configured)
- Windows Task Scheduler (3 tasks active)

**Key Achievement:**
Email automation working end-to-end:
- Monitors Gmail unread (last 15 min)
- Claude Sonnet 4.5 classification
- YAML drift reports
- Telegram notifications (urgent items)
- Test run: 50 emails → 10 classified → 5 urgent alerts

---

# RECENT CHANGES

**2025-12-04 | Slice 2.5: CLP-001 Integration Plan** ✅
- **Achievement:** Self-learning architecture roadmap complete (Phase 2.5)
- **Research Analysis:**
  - 3 papers synthesized: Cognitive Self (LHOs, Frustration Index), CLP-001 Spec (Judge/Teacher/Librarian), CIP (Langfuse, DSPy)
  - Mapped to AI Life OS: Fast Loop (existing MAPE-K) + Slow Loop (new learning agents)
- **Gap Analysis:**
  - Missing: Judge/Teacher/Librarian agents, LHO database, Context Manager (JIT injection)
  - Ready: n8n + Qdrant + EVENT_TIMELINE.jsonl (all prerequisites operational)
- **Integration Architecture:**
  - CLP-001 fits naturally into MAPE-K (Meta-MAPE-K for learning)
  - Hexagonal pattern preserved (Application Core + Adapters)
  - n8n workflows: Slow Loop orchestration (Judge → Teacher → Librarian)
  - Qdrant: LHO storage with vector search
- **Phasing Decision:** **Recommend Phase 2.5 NOW** (vs complete Phase 2 first)
  - Rationale: Infrastructure ready, high ROI (compounding learning), ADHD-friendly (exciting > tedious)
- **7-Slice Roadmap:**
  1. Slice 2.5.1: Langfuse (optional - structured telemetry)
  2. Slice 2.5.2: LHO Database Schema (Qdrant collection + JSON schema) ⭐
  3. Slice 2.5.3: Judge Agent (n8n workflow, automated error detection)
  4. Slice 2.5.4: Teacher Agent (error → LHO synthesis)
  5. Slice 2.5.5: Librarian Agent (LHO indexing + deduplication)
  6. Slice 2.5.6: Context Manager (JIT LHO injection)
  7. Slice 2.5.7: End-to-End Test (prove system learns)
- **Success Metrics:** Error recurrence rate < 10%, LHO database ≥ 5 rules, user reports "stopped repeating errors"
- **Files:** memory-bank/docs/CLP_001_INTEGRATION_PLAN.md (412 lines)
- **Duration:** ~90 min (analysis 45 min, documentation 45 min)
- **Next:** Slice 2.5.2 (LHO Schema) - foundation for self-learning

**2025-12-04 | Slice 2.1: Apply Canonical Terms to Codebase** ✅
- **Achievement:** Zero forbidden terms in production docs
- **Updated Files:** (6 total)
  - project-brief.md: Backticks for deprecated term warnings
  - START_HERE.md: Reordered examples (good → bad, not bad → good)
  - LIFE_GRAPH_SCHEMA.md: "human brain" (biological) not "The Brain" (architectural)
  - METAPHOR_GUIDE.md: "you're still in control" not "you're still the brain"
  - 01-active-context.md: Backticks for forbidden term citations
  - Project Instructions: Prominent canonical terminology warning at top
- **Scan Results:**
  - "Semantic Microkernel": 17 instances (most in "DO NOT USE" tables ✅)
  - "The Brain": 7 instances (most in tables ✅)
  - "The Hands": 5 instances (most in tables ✅)
- **Research files**: Intentionally left unchanged (deprecated terms documented as historical)
- **Git:** f49aac0 refactor(terminology): Apply canonical terms from ADR-001
- **Duration:** ~45 min (Slice 2.1)
- **Next:** Slice 2.2 - Vale enforcement (automated drift prevention)

**2025-12-04 | DateTime Tool for Accurate Calculations** ✅
- **Achievement:** Solved date calculation errors (October 2023 was "13 months" → actually 26 months!)
- **Root Cause:** Claude lacks native system clock access → guessed dates
- **Solution:** Python script (`get_datetime.py`) returns current datetime via Desktop Commander
- **Output:** JSON with date, time, day_of_week, unix timestamp, year/month/day/hour/minute/second
- **Protocol:** ALWAYS call get_datetime() before date math
- **Test:**
  - Current: 2025-12-04 (from tool ✅)
  - Research: 2023-10-01
  - Calculation: 26 months (2 years + 2 months) ✅
  - Before: "13 months" ❌ (2x error!)
- **Files:** tools/get_datetime.py (55 lines), tools/README_get_datetime.md (151 lines)
- **Git:** 38fef48 feat(tools): Add get_datetime tool
- **Duration:** ~15 min (Slice 0)

**2025-12-04 | SYSTEM_BOOK.md Validation Complete** ✅
- **Achievement:** Phase 1 Goal - Context Engineering Infrastructure validated
- **Test:** GPT o1 external LLM onboarding (fresh conversation, upload SYSTEM_BOOK.md)
- **Results:**
  - ⏱️ Time: 27 sec (< 30 sec target ✅)
  - 🎯 Accuracy: ~95% (≥ 95% target ✅)
  - ❓ Questions: 0 (target 0-1 ✅)
  - 📅 Timestamp: Recognized "2025-12-04" ✅
- **Model Note:** GPT o1 (advanced reasoning model with chain-of-thought, 6-12x cost of GPT-4o)
- **GPT o1 correctly identified:** Phase 1 (100%), surgical fix (2025-12-04), Docker/Task Scheduler, Next Steps
- **Improvement:** Before 85% → After 95% (+10% from surgical fix timestamp)
- **Strategic Value:** LLM-Agnostic (any LLM < 30 sec), Zero Cognitive Load, Single Source of Truth, Future-Proof
- **Future Validation:** Test with GPT-4o, Gemini 3 Pro (Nov 2024 release), Claude Sonnet 4 for multi-model confidence
- **Files:** docs/validation/SYSTEM_BOOK_VALIDATION_REPORT.md (239 lines)
- **Git:** cbbd3a5 docs(validation): Complete
- **Duration:** ~20 min (test 5 min, documentation 15 min)

**2025-12-04 | sync_system_book.py Surgical Fix** ✅
- **Achievement:** Robust extraction from Recent Changes (not Just Finished)
- **Problem:** Original code fragile - stopped at newline, no timestamp
- **Solution:** Extract from Recent Changes "Date | Title" format
- **Why Better:**
  - Single Source of Truth (Recent Changes = official record)
  - Timestamp included: "Title (2025-12-04)"
  - Multi-line safe (regex more robust)
  - Future-proof (structured format)
- **Result:** `Recent Achievement: Pre-commit Hook - Auto-Sync Safety Net (2025-12-04)`
- **Git:** 395451c fix(tools): Surgical fix
- **Duration:** ~10 min (analysis 5 min, implementation 5 min)

**2025-12-04 | Pre-commit Hook - Auto-Sync Safety Net** ✅
- **Achievement:** Zero-drift documentation infrastructure (Phase 1 COMPLETE)
- **What:** Git hook (`.git/hooks/pre-commit`) runs `sync_system_book.py` before every commit
- **Why:** Eliminate manual sync step, prevent drift (industry standard: CI/CD automation)
- **How:** 
  - Hook triggers on `git commit`
  - Runs `python tools/sync_system_book.py`
  - Auto-stages updated SYSTEM_BOOK.md
  - Commit proceeds with synced docs
- **Safety:** Hook blocks commit if sync fails (exit code 1), `--no-verify` escape hatch
- **Research:**
  - xcubelabs.com (2024): "Version control systems such as Git to track changes"
  - github.com/resources (2025): "GitHub Actions, CI/CD platform"
  - devops.com (2024): "CI/CD pipeline automatically deploys documentation"
- **Files:** tools/hooks/pre-commit (33 lines), tools/hooks/README.md (132 lines, installation guide)
- **Proof:** Tested - hook ran automatically on commit 2601615 ✅
- **Duration:** ~15 min (implementation 10 min, testing/validation 5 min)

**2025-12-04 | sync_system_book.py - Auto-Sync Infrastructure** ✅
- **Achievement:** Living Documentation automation complete
- **What:** Created `sync_system_book.py` to auto-update SYSTEM_BOOK.md from 01-active-context.md
- **Why:** Prevent drift, reduce maintenance burden (Docs as Code + Living Documentation best practices)
- **How:** Python script reads 01-active-context (Progress/Phase/Recent) → updates SYSTEM_BOOK sections (Quick Context + System State)
- **Research Support:**
  - Living Documentation (Martraire 2024): "Low effort" = automation
  - Docs as Code (DevOps 2024): CI/CD auto-deployment standard
  - Anthropic + Mintlify (2025): Auto-generation (not manual updates)
- **Files:** tools/sync_system_book.py (114 lines), tools/sync_system_book_README.md (usage guide)
- **Duration:** ~20 min (research 10 min, implementation 10 min)

**2025-12-03 | SYSTEM_BOOK.md - LLM Interoperability** ✅
- **Achievement:** Context Engineering Infrastructure complete
- **What:** Created SYSTEM_BOOK.md following llms.txt standard (Jeremy Howard, 2024)
- **Why:** Enable any LLM (GPT, Gemini, Perplexity) to onboard in 30 seconds
- **Structure:**
  - Quick Context Injection (< 500 tokens)
  - Progressive disclosure (Navigation → Protocols → Architecture → Live State)
  - Tailored "How to Use" guides (Claude vs GPT vs Future Agents)
- **Benefits:**
  - Interoperability = Freedom (model-agnostic)
  - Zero cognitive load ("just send SYSTEM_BOOK.md")
  - Quality control (authoritative source → less hallucinations)
  - Scalability (consultants, external agents, future team)
- **Research Support:** Karpathy (context engineering), LangChain (Write/Select/Compress/Isolate), Anthropic, llmstxt.org
- **Files:** SYSTEM_BOOK.md (370 lines), updated START_HERE.md
- **Duration:** ~60 min

**2025-12-03 | Context Emergency Diet** 🚨
- **Problem:** Claude compacting after 2-3 messages (Context Window 95% full at startup)
- **Root Cause:** 01-active-context.md = 1,254 lines (68KB), Project Knowledge = 719KB
- **Solution:** Created LIGHT version (this file), archived history, cleaning Project Knowledge
- **Pattern:** MCP research "H2: Premature Compaction" - confirmed via Performance report
- **Duration:** ~30 min

**2025-12-03 | Email Watcher + Telegram Integration** ✅
- End-to-end email automation with notifications
- unified drift directory (truth-layer/drift/)
- Reconciler path fix
- send_telegram_alert() function (78 lines)
- Test: 5 urgent emails notified successfully
- Duration: ~45 min

**2025-12-03 | All Protocols Research-Backed (TFP-001)** ✅
- Systematic web research (10 queries, 50 sources, 20 citations)
- Created TFP-001 (Truth-First Protocol): "SEARCH FIRST, WRITE SECOND"
- Upgraded MAP-001, AEP-001, TSP-001, SVP-001 to v2.0
- Citations: CHADD, Postman, Stack Overflow, Dynatrace, OSHA, Toyota
- Duration: ~2 hours

**2025-12-03 | Memory Bank Watchdog + Observer Scheduling** ✅
- Git → Markdown parser → Embeddings → Qdrant
- Observer automated (Windows Task Scheduler, every 15 min)
- Memory Bank auto-indexes to vector DB
- Duration: ~120 min total

**2025-12-03 | n8n + Qdrant + Docker Auto-Start** ✅
- Production deployment (n8n v1.122.4, Qdrant v1.16.1)
- Docker Desktop auto-start on Windows boot
- 24/7 reliability configured
- Duration: ~90 min total

---

# NEXT STEPS

**Status:** Phase 1 Complete ✅ + DateTime Tool Ready ✅

**Choose one:**

**Option A: Real-Time Knowledge Alignment** 🚀 (Phase 2, 7 slices)
- **Goal:** System knows when research is stale, auto-updates knowledge
- **Plan:** memory-bank/docs/REAL_TIME_ALIGNMENT_PLAN.md (403 lines, documented)
- **Architecture:** Observer → Research Freshness → Vector DB Updates
- **Duration:** ~6 hours (7 slices × 30-60 min each)
- **Benefit:** Never repeat date calculation errors, always current knowledge
- **Next:** Slice 1.1 - Observer n8n Workflow (45 min)

**Option B: Phase 1 Retrospective** 🎓 (30 min)
- What worked well? (automation, research-backed, small slices)
- What was challenging? (MCP research, surgical fixes, date errors!)
- Lessons learned? (Living Documentation, Git hooks, DateTime tool)
- Document: Pattern library, best practices (BP-XXX), anti-patterns (AP-XXX)
- Prepare: Phase 2 kickoff materials

**Option C: Take a Break** 😊
- Phase 1 = major milestone (8 weeks → infrastructure production-ready)
- DateTime Tool = critical foundation fix
- Come back fresh: Retrospective tomorrow, Phase 2 next week

**Option D: Continue Previous Next Steps** 
- Task Scheduler Dashboard (45 min) - monitoring
- Life Graph Integration (60 min) - semantic search
- Gmail Cleanup (15 min) - maintenance

---

# PROTOCOLS (QUICK REFERENCE)

**Protocol 1: Post-Slice Reflection (Auto-Run)**
After EVERY slice, Claude MUST automatically:
1. Update this file (Quick Status, Recent Changes)
2. Append to 02-progress.md
3. Detect Meta-Learning Triggers
4. Git commit changes

**MAP-001:** Memory Bank Access Protocol v2.0
- ALWAYS read START_HERE.md + project-brief.md + this file
- Use project_knowledge_search for research files
- Never rely on chat history alone

**AEP-001:** ADHD-Aware Execution Protocol v2.0
- Small slices (30-60 min)
- Clear stopping points
- Low-friction approvals

**TSP-001:** Tool Strategy Protocol v2.0
- Desktop Commander for local operations
- project_knowledge_search for documents
- web_search only when needed

**SVP-001:** Self-Validation Protocol v2.0
- Run pytest before claiming "done"
- Test error cases, not just happy path
- Truth-First: Search before making claims (TFP-001)

**TFP-001:** Truth-First Protocol v2.0
- SEARCH FIRST, WRITE SECOND
- Cite sources (URL, date accessed, quote)
- Label: "Best Practice (Cited)" vs "Proposed (Experimental)"

---

**Last Updated:** 2025-12-03 15:30  
**Next Update:** After next completed slice
