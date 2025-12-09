# Side Architect Research Digest

**Purpose:** Compact architecture and research summary for side architect assistant  
**Last Updated:** 2025-12-01  
**Read Time:** ~10 minutes

---

## TL;DR: AI Life OS in 30 Seconds

**What is this?**  
A Personal AI Operating System where Claude Desktop orchestrates MCP servers against a git-backed Truth Layer, with ADHD-friendly workflows and proactive drift detection.

**Core Model:** Head/Hands/Truth/Nerves Architecture
- **Head** = Claude Desktop (reasoning, planning, orchestration)
- **Hands** = n8n + tools (execution, automation)
- **Truth** = Git-backed files (single source of truth)
- **Nerves** = MCP servers (interfaces, connectors)

**Reference:** See `docs/ARCHITECTURE_METAPHOR.md` for full details

**Workflow:** Chat → Spec → Change (HITL at decision gates)

**Life Graph:** 6 entities (Area, Project, Task, Context, Identity, Log) with ADHD-specific metadata

---

## 1. Canonical Architecture

**📄 Reference:** `docs/ARCHITECTURE_METAPHOR.md`

**What Matters for Side Architect:**
- **INV-001:** Git repo is the ONLY Truth Layer (no state fragmentation)
- **INV-003:** Heads are replaceable (Claude is not special, just current)
- **INV-006:** Git as infinite undo (all changes reversible)
- **Architecture:** Head/Hands/Truth/Nerves (NOT Hexagonal/Core/Ports/Adapters)

**Pattern Classification:**
- **Canonical (now):** Claude Desktop (Head), MCP servers (Nerves), Git-backed Truth Layer, Memory Bank
- **Future:** ChatGPT/Gemini heads, Vector Memory, LangGraph multi-day HITL
- **Deprecated:** Hexagonal terminology (Core/Ports/Adapters), "kernel" references

---

## 2. Migration Plan

**📄 Reference:** `claude-project/system_mapping/migration_plan.md`

**What Matters for Side Architect:**
- **4 Phases:** Investigation (1-2w) → Core Infrastructure (3-6w) → Governance (7-8w) → Cleanup (9-12w)
- **Current:** Phase 2 (~15% complete)
- **Pattern:** Small slices (30-60 min), safety-first (Archive > Delete), Git rollback always available
- **Technical Debt:** TD-001 (Git MCP missing, manual bridge acceptable)

---

## 3. Life Graph & Entities

**📄 Reference:** `memory-bank/docs/LIFE_GRAPH_SCHEMA.md`

**6 Core Entities:**

**Structural (define world):**
- **Area** – Life domains with no deadline (Health, Career, Finance)
- **Context** – Constraints on when/where work can happen (@laptop, @low_energy)
- **Identity** – Roles/modes you operate in (Writer, Developer, Parent)

**State-based (evolve over time):**
- **Project** – Finite goals with deadlines (Launch Website, Plan Trip)
- **Task** – Atomic work units (5-60 minutes, completable in one session)
- **Log** – Time-stamped observations, notes, journal entries

**ADHD-Specific Fields:**
- **`energy_profile`** – [high_focus | creative | admin | low_energy] – Match work to state
- **`dopamine_level`** – [high | medium | low] – Track subjective reward
- **`is_frog`** – boolean – Is this the hardest/most dreaded task?
- **`do_date` vs `due_date`** – When to START vs when to FINISH
- **`contexts`** – array – Where/how this can be done (enables "what can I do NOW?" queries)

**Why This Matters:**
- Energy management > time management (ADHD brains have variable executive function)
- Dopamine tracking prevents low-motivation spirals
- Object permanence via explicit links (graph relationships surface "forgotten" items)
- Time blindness mitigation (visual/spatial representations)

**📚 Research Grounding:** 12.md (sections 3.1-3.3), 18.md (sections 2.1-2.3)

---

## 4. ADHD Design Patterns

**📄 Reference:** `claude-project/research_claude/18.md`

**Core ADHD Profile:**
- **Executive Dysfunction** – Deficit in task initiation, organization, persistence
- **Working Memory Deficits** – "Object impermanence" (if not visible, doesn't exist)
- **Time Blindness** – Deadlines feel abstract until "today"
- **Dopamine Dysregulation** – Tasks with low reward are physiologically difficult

**Design Responses:**
- **Minimalism as Functional Necessity** – Low extraneous cognitive load (not aesthetic)
- **Artifacts for Visual Anchors** – Persistent UI windows prevent "out of sight, out of mind"
- **Progressive Disclosure** – Reveal complexity only as requested
- **Micro-Feedback Loops** – Continuous acknowledgment (external dopamine regulator)

**Interaction Patterns (from 18.md):**
- **Goblin Decomposer** – Break large tasks into ridiculously small steps
- **Compassionate Interrupter** – Proactive hyperfocus management (time-check after 90 min)
- **Visual Time Transformation** – Text-to-spatial (Gantt charts, ASCII timelines)
- **Shame-Free Re-entry** – "Welcome back" protocol (no judgment on gaps)

**📚 Research Grounding:** 18.md (sections 1-4), 12.md (Playbooks 1-2)

---

## 5. Memory Bank & PARA

**📄 Reference:** `memory-bank/README.md`, `memory-bank/project-brief.md`

**PARA Structure:**
- **00_Inbox/** – Temporary capture (unprocessed)
- **10_Projects/** – Finite goals (deadlines)
- **20_Areas/** – Ongoing domains (no deadlines)
- **30_Resources/** – Reference materials
- **99_Archive/** – Completed entities

**Cross-Chat Continuity:**
- Memory Bank enables ANY AI model (Claude, ChatGPT, Gemini) to load context quickly
- Model-agnostic design (INV-003: Adapters are replaceable)
- 3-level TL;DR: Quick Status (10 sec) → TL;DR (20 sec) → Full Context (5 min)

**Protocol:**
- **At Start:** Read project-brief + 01-active-context, summarize to user
- **At End:** Update 01-active-context + append to 02-progress

**📚 Research Grounding:** 12.md (PARA pattern), INV-001 (Core expansion), ADHD-aware (18.md, 11.md)

---

## 6. Meta-Learning & Protocols

**📄 Reference:** `claude-project/ai-life-os-claude-project-playbook.md`

**Protocol 1: Post-Slice Reflection (Auto-Run)**

After EVERY slice, Claude autonomously:
- Updates Memory Bank (01-active-context + 02-progress)
- Detects Meta-Learning Triggers (5 types)
- Proposes documentation (AP-XXX, BP-XXX, TD-XXX)
- Git commits changes

**Meta-Learning Triggers (Playbook Section 9):**
- **Trigger A:** Repetition (2nd+ occurrence) → propose AP-XXX
- **Trigger B:** Workaround used → propose TD-XXX
- **Trigger C:** User surprise → check spec clarity
- **Trigger D:** Research gap (3+ "not sure") → propose research slice
- **Trigger E:** Friction point → propose automation

**Incident Response Protocol (Playbook Section 8):**
- 5 steps: STOP → 5 Whys → CLASSIFY → PROPOSE → ASK
- Document in `memory-bank/incidents/`

**Anti-Patterns (AP-XXX):**
- **AP-001:** Context Window Overflow → Use surgical edits (str_replace) on large files

**📚 Research Grounding:** Meta-Process family (#7), ADHD-aware collaboration (11.md, 18.md)

---

## 7. Research Families (Quick Reference)

**📁 Location:** `claude-project/research_claude/` (18 files: 01-18.md)

**7 Families:**
1. **Architecture/Kernel** – Agentic Kernel, Semantic Microkernel, Chat→Spec→Change
2. **Claude/MCP/Tools** – How Claude Desktop interacts with MCP, safety, limits
3. **Cognition/ADHD** – Executive function, working memory, friction reduction
4. **Infrastructure** – Windows + WSL2 + Docker + n8n stability
5. **Safety/Governance** – Drift prevention, circuit breakers, HITL
6. **Memory/RAG** – Truth Layer, Memory Bank, Life Graph, vector search
7. **Meta-Process** – Slices, playbooks, experiments, meta-learning

**Key Files for Side Architect:**
- **12.md** – Life Graph design (ADHD-specific metadata, PARA, 6 entities)
- **18.md** – Neuroadaptive systems (ADHD profile, interaction patterns, Artifacts)
- **CANONICAL_ARCHITECTURE.md** – 6 invariants, contradiction resolution
- **migration_plan.md** – 4 phases, 16 slices, technical debt

---

## 8. How to Use This Digest

**For New Side Architect Chats:**
1. Read **this file** (side-architect-research-digest.md) – ~10 min
2. Read **side-architect-bridge.md** – ~2 min (current state snapshot)
3. Read **01-active-context.md** – ~2 min (what's happening NOW)
4. Optional: Dive into specific references if needed

**For Ongoing Collaboration:**
- Bookmark `side-architect-bridge.md` for quick state checks
- Reference section numbers when discussing architecture (e.g., "per Section 3 of digest")
- Update side architect if any major architectural decisions change

**Don't:**
- Don't re-read all 18 research files unless deep diving on specific topic
- Don't skip the snapshot files (they're the entry point)

---

## 9. History & Change Log

**Canonical History:**
- **`memory-bank/02-progress.md`** – Chronological log of all completed slices (date, goal, files, duration, result)
- **`claude-project/system_mapping/migration_plan.md`** – 4-phase roadmap with strategic context

**For Side-Architect Assistants:**

If you need to understand "how did we get here?" or "what happened in Slice X?":
- **Don't reconstruct from chat** – Chat history is incomplete and unreliable
- **Ask the user to:**
  1. Open `02-progress.md`
  2. Search for a keyword (e.g., "Observer", "Reconciler", "validator")
  3. Paste the relevant slice entry into the chat
- **For strategic planning:** Ask for relevant sections of `migration_plan.md`

This is faster and more accurate than trying to piece together history from conversation.

---

**Document Version:** 1.0  
**Created:** 2025-12-01  
**By:** Claude Desktop (Side Architect Bridge slice)
