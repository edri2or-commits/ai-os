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

**AI Life OS | Phase 1: Infrastructure Deployment** 🚀

**Progress:** ~85% complete (7/8 core slices)

**Just Finished:**
- ✅ Email Watcher automation (Gmail → Claude classification → Telegram alerts)
- ✅ Memory Bank Watchdog (Git → Qdrant semantic search)
- ✅ Observer scheduling (Windows Task Scheduler, every 15 min)
- ✅ All protocols upgraded to v2.0 (research-backed, cited)

**Currently Operational:**
- Desktop Commander MCP ✅
- Observer (drift detection) ✅
- Validator + pre-commit hook ✅
- Reconciler (CR management) ✅
- pytest (44 tests passing) ✅
- n8n + Qdrant (24/7 Docker) ✅
- **3 Automated Processes Running (Task Scheduler):**
  - Observer (every 15 min)
  - Memory Bank Watchdog (every 15 min, offset +7)
  - Email Watcher (every 15 min, offset +10)

**Blockers:** NONE

**Next Decision Point:**
1. **Gmail cleanup** (archive 50 processed emails)
2. **Slice 1.8: Task Scheduler Dashboard** (monitoring/logging)
3. **Slice 1.9: Life Graph Integration** (extend Watchdog)

---

# CURRENT FOCUS

**Phase:** Phase 1 – Infrastructure Deployment 🚀  
**Status:** 7/8 slices COMPLETE (~85%)

**Active Work:** Email Watcher deployed and running

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

**2025-12-03 | INCIDENT: Docker AutoStart Failure** 🔴
- **Problem:** Docker not auto-starting after reboot (n8n + Qdrant down ~20 hours)
- **Root Cause:** AutoStart=false in settings-store.json (Slice 1.3 claimed true but was false)
- **Fix:** Set AutoStart=true + started Docker Desktop manually
- **5 Whys:** Validation Theater → SVP-001 gap → TFP-001 violation (claimed before verifying)
- **Actions:** AP-007 (Validation Theater anti-pattern), TD-003 (Docker monitoring gap), SVP-001 v2.1 (add "verify in reality")
- **Duration:** ~15 min investigation + fix
- **Lesson:** Memory Bank drift is real - Observer writes drift reports BUT Memory Bank not auto-updated

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

**Choose one:**

**Option A: Gmail Cleanup (15 min)** ⭐ RECOMMENDED
- Archive 50 processed emails
- Mark Email Watcher as fully deployed
- Close Phase 1

**Option B: Task Scheduler Dashboard (45 min)**
- Monitoring script (reads Task Scheduler logs)
- PowerShell: Get-ScheduledTask + log parsing
- Email Watcher health checks
- Alerts if tasks fail

**Option C: Life Graph Integration (60 min)**
- Extend Watchdog to index Life Graph entities
- Areas, Projects, Tasks → Qdrant
- Semantic search across entire system

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
