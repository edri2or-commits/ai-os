# MAPPING_SYSTEM_STATE.md — System State Documentation Analysis

**Created:** 2025-11-25  
**Author:** Claude Desktop (Mapping Block 1)  
**Purpose:** Map existing documentation related to system state, control plane, and snapshots — both in the repo and Google Drive.  
**Status:** 📊 Analysis Complete — No edits made

---

## Repo Docs (Current)

| File Path | Description | Freshness | Relevance to Snapshot Layer |
|-----------|-------------|-----------|----------------------------|
| `docs/SYSTEM_SNAPSHOT.md` | Current system state — architecture diagram, active services (GitHub Client 8081, Google 8082), GPT integration status, Chat1 status | ✅ Fresh (2025-11-24) | **CORE** — This IS the current snapshot, but repo-only |
| `docs/CONTROL_PLANE_SPEC.md` | System mode (INFRA_ONLY), phase (2), core variables, sync cycle definition | ✅ Fresh (v0.2) | **CORE** — Defines how state should be tracked |
| `docs/CONSTITUTION.md` | 9 founding principles + Human-Approved Writes amendment | ✅ Fresh (2025-11-25) | **GOVERNANCE** — Rules that govern any snapshot system |
| `docs/DECISIONS_AI_OS.md` | 5 locked decisions: MCP Legacy, Executor not deployed, GPT DRY RUN, Phase 1 Complete, Telegram Chat1 Official | ✅ Fresh (2025-11-24) | **CONTEXT** — Historical decisions affecting current state |
| `docs/SESSION_INIT_CHECKLIST.md` | Session initialization protocol for agents | ✅ Fresh (v0.1) | **PROTOCOL** — How agents should load state at session start |
| `docs/PHASE2_CHECKLIST.md` | Phase 2 progress tracker (5 items, all unchecked) | ✅ Fresh | **TRACKING** — Could feed into snapshot "Active Phase" section |
| `docs/EVENT_TIMELINE_SPEC.md` | Event logging format (JSONL), fields, flow | ✅ Fresh (v0.1) | **LOGGING** — Basis for "Recent Key Events" in snapshot |
| `agents/AGENTS_INVENTORY.md` | Lists all agents (GPT, MCP, Chat1, etc.) with roles and status | ✅ Fresh (2025-11-24) | **AGENTS** — Source for "Agents & Roles" section |
| `docs/CAPABILITIES_MATRIX.md` | 22 capabilities mapped | 🟡 Likely fresh | **CAPABILITIES** — Could complement agents section |
| `tools/TOOLS_INVENTORY.md` | 24 tools mapped | 🟡 Likely fresh | **TOOLS** — Supports services/integrations view |
| `policies/SECURITY_SECRETS_POLICY.md` | Security policies (720 lines) | ✅ Fresh | **GOVERNANCE** — Risks/Tech Debt source |
| `workflows/*.md` | Various workflow definitions | ✅ Fresh | **WORKFLOWS** — Automation documentation |

### Key Observations — Repo

1. **SYSTEM_SNAPSHOT.md is already comprehensive** — It covers architecture, services, ports, GPT integration, Chat1 status, and version history.

2. **CONTROL_PLANE_SPEC.md defines the "what should be tracked"** — Variables like `SYSTEM_MODE`, `ACTIVE_PHASE`, `AUTOMATIONS_ENABLED`.

3. **No AUTOMATIONS_REGISTRY exists yet** — This is explicitly part of the GPT's proposed design.

4. **EVENT_TIMELINE exists only as spec** — No actual `EVENT_TIMELINE.jsonl` file found.

5. **Strong foundation exists** — The repo has solid state documentation, but it's fragmented across files.

---

## Drive Docs (Historical)

| Document Name | Location | Created | Description | Alignment with Current Repo |
|---------------|----------|---------|-------------|----------------------------|
| **AI-OS שדרוג כלים לאוטומציה** | [Drive Link](https://docs.google.com/document/d/1qinE6mNy4HcptvXn00syWL22M24ahJV_x1ZP5xuisJM/edit) | 2025-11-22 | Comprehensive research doc: AI-OS architecture, Gold Tools (n8n, Telegram, MCP, Railway, Supabase), phased implementation plan | 🟡 **PARTIAL ALIGNMENT** — Describes a *different* architecture direction (n8n-centric) than current repo (FastAPI + Custom GPT Actions) |
| **אינסטרוקשן GPTs והגדרות** | [Drive Link](https://docs.google.com/document/d/1Mwuy2uJ02wdFqM597sqdxy1xdptgJMK3OGjdyY5kHZY/edit) | 2025-10-04 | GPT instructions for "Astrateg Architecture" and others | 🔴 **OUTDATED** — From ~2 months ago, different GPT structure |
| **My AI-OS Test Document** (x2) | Drive | 2025-11-24 | Empty test documents | ❌ **NOT RELEVANT** — Test artifacts |
| **Test Doc from AI-OS** | Drive | 2025-11-24 | Empty test document | ❌ **NOT RELEVANT** — Test artifact |
| **Older docs (Oct 2025)** | Drive | 2025-10-xx | Various conversation exports, process docs | 🔴 **LIKELY OUTDATED** — From pre-current-repo phase |

### Key Observations — Drive

1. **"AI-OS שדרוג כלים לאוטומציה" is the most significant Drive doc** — But it describes a *different* tooling approach:
   - Drive doc proposes: n8n as orchestrator, Telegram as primary UI, Railway hosting, Supabase for memory
   - Current repo uses: Custom GPT Actions, FastAPI services, ngrok tunnels, local execution

2. **The Drive doc is more "vision/research"**, while the repo is "implementation reality"

3. **No "SYSTEM_SNAPSHOT_DRIVE" exists yet** — This is what the GPT Planning Model wants to create

4. **Historical value exists** — The research doc contains valuable thinking about:
   - Gold Tools selection rationale
   - Risk mitigation strategies
   - Phased implementation approach
   - Brain-GPT system prompt

---

## Alignment with Proposed Snapshot Structure

The GPT Planning Model proposed this structure for `SYSTEM_SNAPSHOT_DRIVE.md`:

| Proposed Section | Existing Coverage in Repo | Gap Analysis |
|-----------------|---------------------------|--------------|
| **1. Metadata** (ID, time, generated-by, phase, confidence) | Partial in SYSTEM_SNAPSHOT.md (has date, version) | ⚠️ Missing: snapshot ID, generated-by agent, confidence level |
| **2. Architecture Overview** | ✅ Strong in SYSTEM_SNAPSHOT.md | ✅ Covered |
| **3. Agents & Roles** | ✅ Strong in AGENTS_INVENTORY.md | ✅ Covered (needs consolidation) |
| **4. Active Plans & Phase** | Partial: PHASE2_CHECKLIST.md + CONTROL_PLANE_SPEC.md | ⚠️ Fragmented across files |
| **5. Services Status** | ✅ Strong in SYSTEM_SNAPSHOT.md (ports, endpoints) | ✅ Covered |
| **6. Automations Summary** | ❌ Missing | 🔴 **GAP**: No AUTOMATIONS_REGISTRY.jsonl exists |
| **7. Risks & Tech Debt** | Partial in SECURITY_SECRETS_POLICY.md | ⚠️ Not consolidated |
| **8. TODO by Actor** | ❌ Missing | 🔴 **GAP**: No actor-based task tracking |
| **9. Recent Key Events** | Spec exists (EVENT_TIMELINE_SPEC.md), no data | 🔴 **GAP**: No actual event log exists |

---

## Gaps / Duplications / Risks

### 🔴 Gaps

1. **No AUTOMATIONS_REGISTRY** — Critical for "No-Orphan-Automations" principle
   - Current state: Automations are described in prose across docs
   - Needed: JSONL file with structured records

2. **No EVENT_TIMELINE data** — Spec exists but no actual log
   - Current state: Only spec file (EVENT_TIMELINE_SPEC.md)
   - Needed: `logs/EVENT_TIMELINE.jsonl` with actual entries

3. **No Drive-synced snapshot** — Repo snapshot exists, but GPT Planning Model can't see it directly
   - Current state: SYSTEM_SNAPSHOT.md in repo only
   - Needed: SYSTEM_SNAPSHOT_DRIVE.md in Google Drive (synced/mirrored)

4. **No "TODO by Actor" tracking** — Tasks aren't organized by who should do them
   - Current state: Tasks scattered or implicit
   - Needed: Clear section in snapshot with tasks per agent

5. **No confidence/freshness metadata** — Snapshots don't indicate reliability
   - Current state: Only manual dates
   - Needed: Auto-generated timestamps, staleness indicators

### 🟡 Duplications

1. **Agent info appears in multiple places:**
   - `agents/AGENTS_INVENTORY.md`
   - `docs/SYSTEM_SNAPSHOT.md` (GPT section, Chat1 section)
   - `docs/CAPABILITIES_MATRIX.md`
   - Risk: Drift between files

2. **Phase/status tracking is fragmented:**
   - `docs/CONTROL_PLANE_SPEC.md` (ACTIVE_PHASE variable)
   - `docs/PHASE2_CHECKLIST.md` (Phase 2 tasks)
   - `docs/SYSTEM_SNAPSHOT.md` (implicit phase info)
   - Risk: Conflicting phase statements

### ⚠️ Risks

1. **Drive research doc describes different architecture**
   - The "Gold Tools" research proposes n8n + Railway
   - Current repo uses Custom GPT + FastAPI + ngrok
   - Risk: Confusion about "official" direction

2. **Snapshot is manually updated**
   - Currently Or or agents update it by hand
   - Risk: Staleness, drift from reality

3. **No automated sync mechanism**
   - Repo ≠ Drive automatically
   - Risk: GPT Planning Model may see outdated state

---

## Suggestions for Next Step

### Option A: Extend Existing Structure (Conservative)

**Approach:** Build on what already exists in the repo, add missing pieces incrementally.

1. Create `logs/EVENT_TIMELINE.jsonl` — Start logging events today
2. Create `docs/AUTOMATIONS_REGISTRY.jsonl` — Register existing automations
3. Add metadata section to `SYSTEM_SNAPSHOT.md` — ID, generated-by, confidence
4. Create Drive mirror manually — Copy SYSTEM_SNAPSHOT to Drive after each update

**Pros:** Low risk, builds on proven structure  
**Cons:** Still manual, doesn't solve sync problem

### Option B: Create SYSTEM_SNAPSHOT_DRIVE.md (GPT's Proposal)

**Approach:** Create a new dedicated Drive document that aggregates repo state.

1. Create `SYSTEM_SNAPSHOT_DRIVE.md` in Google Drive with all proposed sections
2. Establish update protocol: After repo changes → Update Drive doc
3. Keep repo's `SYSTEM_SNAPSHOT.md` as SSOT, Drive as "synced view"
4. Add `docs/AUTOMATIONS_REGISTRY.jsonl` in repo

**Pros:** GPT Planning Model gets direct access, cleaner separation  
**Cons:** Two places to maintain (even if one is "derivative")

### Option C: Hybrid — Consolidate First, Then Mirror (Recommended)

**Approach:** First fix fragmentation in repo, then create Drive sync layer.

**Phase 1: Repo Cleanup**
1. Consolidate agent info into single `AGENTS_INVENTORY.md`
2. Add missing sections to `SYSTEM_SNAPSHOT.md`:
   - Metadata (ID, timestamp, generated-by)
   - Automations Summary (link to registry)
   - Risks & Tech Debt (consolidated)
   - TODO by Actor
3. Create `docs/AUTOMATIONS_REGISTRY.jsonl`
4. Create `logs/EVENT_TIMELINE.jsonl` with first entry

**Phase 2: Drive Layer**
5. Create `SYSTEM_SNAPSHOT_DRIVE.md` in Drive
6. Define update trigger: When do we sync?
7. Consider automation: GPT Operator or Claude updates Drive after repo changes

**Pros:** Clean foundation, then clean layer  
**Cons:** More work upfront

---

## Decision for Or

Before proceeding to implementation, please confirm:

1. **Which option do you prefer?** (A / B / C / Other)

2. **What's the priority?**
   - Get GPT Planning Model visibility fast → Option B
   - Fix repo fragmentation first → Option C
   - Minimal change, just add missing files → Option A

3. **Who should update the Drive snapshot?**
   - Manual (Or triggers update)
   - Semi-auto (Claude/GPT updates after major changes)
   - Full auto (webhook/CI triggers — future)

4. **Should the Drive doc "AI-OS שדרוג כלים לאוטומציה" be marked as:**
   - 🗄️ Historical/Research (not current direction)
   - 📋 Alternative Architecture (parallel track)
   - 🔄 Future Roadmap (to be implemented later)

---

## Summary

| Aspect | Current State | Proposed State |
|--------|---------------|----------------|
| **System Snapshot** | Repo only (SYSTEM_SNAPSHOT.md) | Repo + Drive mirror |
| **Automations Tracking** | ❌ None | AUTOMATIONS_REGISTRY.jsonl |
| **Event Log** | Spec only | EVENT_TIMELINE.jsonl with data |
| **Agent Info** | Fragmented (3 files) | Consolidated (1 file) |
| **Phase Tracking** | Fragmented (3 files) | Single source in snapshot |
| **GPT Planning Model Access** | Via Or (manual) | Direct Drive access |

---

**End of Mapping Block 1**  
**Next Step:** Await Or's decision on direction, then proceed to Design block.
