# Write Locations Guide

**Purpose:** Define WHERE to update WHAT when completing work  
**Last Updated:** 2025-12-06  
**Rule:** Follow this guide in Protocol 1 (Post-Slice Reflection)

---

## Quick Reference

| Event | Files to Update | Priority |
|-------|----------------|----------|
| **Slice completed** | 01-active-context, 02-progress | ALWAYS |
| **Tool/API deployed** | TOOLS_INVENTORY | ALWAYS |
| **Architecture changed** | ARCHITECTURE_REFERENCE | IF MAJOR |
| **Pattern discovered** | AP-XXX or BP-XXX | IF LEARNABLE |
| **External LLMs need update** | side-architect-bridge | IF MILESTONE |

---

## Protocol 1: Post-Slice Reflection (AUTOMATIC)

After EVERY completed or interrupted slice, you MUST automatically update:

### 1. `memory-bank/01-active-context.md`

**ALWAYS update these sections:**

**Section: "Quick Status"**
- Update: `progress_pct` (e.g., 76% → 78%)
- Update: Phase description if changed

**Section: "Just Finished"**
- Add new entry at TOP of list:
  ```markdown
  - **H3 Telegram Approval Bot** (2025-12-06) - TESTED & OPERATIONAL
    - End-to-end test passed (CR → Telegram → Approval → Database)
    - Backend detects CR in 5 seconds
    - User approved via inline button
    - Database updated successfully
  ```
- Keep last 5-8 entries (move older to 02-progress)

**Section: "Next Steps"**
- Update based on what was just completed
- Remove completed option
- Add new options if unlocked
- Keep 2-3 clear choices

**Example update:**
```markdown
## Next Steps

1. **H4 VPS Deployment** (4-6h, HIGH impact)
   - Hetzner Cloud setup
   - Docker orchestration
   - 24/7 uptime (true headless)
   - Cost: ~$16/month

2. **Judge V2 + Langfuse Integration** (60 min, DEPTH)
   - Verify Langfuse V3 operational
   - Test trace logging
   - Validate error detection

3. **Document Victory Lap** (30 min, MORALE)
   - H3 is major milestone
   - Write success story
   - Update external docs
```

---

### 2. `memory-bank/02-progress.md`

**ALWAYS append chronological entry:**

```markdown
### Slice: H3 Telegram Approval Bot - Testing
**Date:** 2025-12-06  
**Duration:** 60 minutes  
**Status:** ✅ COMPLETE

**Goal:** End-to-end test of H3 approval workflow

**What Was Done:**
1. Created test CR (CR_TEST_001.yaml)
2. Backend detected file in 5 seconds
3. Telegram notification sent successfully
4. User approved via inline button
5. Approval file written to approved/
6. Database updated with approval record

**Outcome:**
- ✅ H3 Telegram Approval Bot is TESTED & OPERATIONAL
- Backend: Reliable file watching + Telegram integration
- Database: SQLite approvals.db working correctly
- User Experience: Clean, fast, mobile-friendly

**Lessons Learned:**
- Watchdog library works well on Windows
- Telegram inline buttons are intuitive
- File-based CR system is simple and reliable

**Next:** H4 VPS Deployment (move to always-on infrastructure)
```

---

## Conditional Updates (IF conditions met)

### 3. `memory-bank/TOOLS_INVENTORY.md`

**Update when:** New tool, API, service, or automation deployed

**Sections to update:**

**If NEW MCP Server:**
```markdown
## MCP Servers (Claude Desktop)

**X. New MCP Server Name**
- **Package:** `@org/package-name`
- **Capabilities:** List what it does
- **Endpoint:** URL if applicable
- **Auth:** Auth method
- **Status:** ✅ OPERATIONAL
- **Documentation:** Link to README
```

**If NEW REST API:**
```markdown
## REST APIs (localhost)

### HX: Service Name

**Service:** Description  
**Port:** XXXX  
**URL:** http://localhost:XXXX  
**Status:** ✅ OPERATIONAL

**Endpoints:**
- `METHOD /path` - Description

**Auth:** Auth method  
**Documentation:** Path to README
```

**If NEW Docker Service:**
```markdown
## Services (Docker)

### Service Name

**Image:** `org/image:tag`  
**Container:** `container-name`  
**Port:** XXXX  
**URL:** http://localhost:XXXX  
**Status:** ✅ OPERATIONAL

**Purpose:** What it does
```

**If NEW Windows Automation:**
```markdown
## Windows Automations (Task Scheduler)

### X. Automation Name

**Task Name:** `\AI-OS\Task-Name`  
**Schedule:** Frequency  
**Script:** `tools/script.py`  
**Output:** Where it writes

**Purpose:** What it does

**Status:** ✅ OPERATIONAL
```

**If CAPABILITY CHANGED:**
Update the **"Can I...?" Table** section

---

### 4. `memory-bank/docs/ARCHITECTURE_REFERENCE.md`

**Update when:** Major architectural change (not minor tweaks)

**Examples of MAJOR changes:**
- New layer added (e.g., Routing Layer)
- Core pattern changed (e.g., Hexagonal → Event-Driven)
- New component in MAPE-K loop
- Infrastructure paradigm shift

**What to update:**
- Diagrams (if ASCII art)
- Component descriptions
- Integration points
- Data flow diagrams

**Examples of MINOR changes (don't update):**
- Bug fix in existing component
- Performance improvement
- Refactoring without interface change

---

### 5. `memory-bank/patterns/AP-XXX.md` or `BP-XXX.md`

**Update when:** Meta-Learning Trigger fires (Playbook Section 9)

**Trigger A: Repetition** (2nd+ occurrence)
- **Action:** Create `AP-XXX-{slug}.md` (Anti-Pattern)
- **Example:** Same error happened twice → Document as anti-pattern

**Trigger E: Friction Point**
- **Action:** Create `BP-XXX-{slug}.md` (Best Practice)
- **Example:** Found efficient workflow → Document as best practice

**Template for AP-XXX:**
```markdown
# AP-XXX: {Anti-Pattern Name}

**ID:** AP-XXX  
**Created:** YYYY-MM-DD  
**Category:** {technical|process|cognitive}  
**Severity:** {low|medium|high}

## Problem
{What keeps happening wrong}

## Why It Happens
{Root cause - usually cognitive load or tool misuse}

## How to Avoid
{Specific mitigation strategy}

## Related
- BP-YYY (better alternative)
- Playbook Section X
```

**Template for BP-XXX:**
```markdown
# BP-XXX: {Best Practice Name}

**ID:** BP-XXX  
**Created:** YYYY-MM-DD  
**Category:** {technical|process|cognitive}  
**Benefit:** {time saved|quality improved|friction reduced}

## Context
{When this applies}

## Practice
{Step-by-step what to do}

## Why It Works
{Underlying principle}

## Example
{Concrete instance of use}
```

---

### 6. `memory-bank/side-architect-bridge.md`

**Update when:** Major milestone that external LLMs should know

**Examples of milestones:**
- Phase progress jumps (e.g., 70% → 80%)
- Major component operational (e.g., H3 Telegram Bot)
- Architecture shift
- New capabilities unlocked

**What to update:**

**Section: "Current State"**
```markdown
## Current State

**Phase 2:** Architectural Alignment (~78% complete)

**Recently Completed:**
- ✅ H3 Telegram Approval Bot (TESTED & OPERATIONAL - 2025-12-06)
- ✅ Judge Agent V2 with Langfuse integration
- ✅ Memory Bank API (H2) for external LLMs
```

**Section: "Recent Achievements"**
Add bullet at top:
```markdown
- **H3 Telegram Approval Bot** - Async HITL via Telegram, tested end-to-end
```

---

## Git Commit Rules

After updating files, ALWAYS commit:

### Commit Message Format:
```
{type}({scope}): {description} ({slice-id})

{optional body}
```

**Types:**
- `feat` - New feature/slice complete
- `fix` - Bug fix
- `docs` - Documentation only
- `refactor` - Code change without new feature
- `test` - Test additions/changes
- `chore` - Maintenance (dependencies, config)

**Scope:**
- `h1`, `h2`, `h3`, `h4` - Headless migration slices
- `memory` - Memory Bank updates
- `tools` - Tools/scripts
- `infra` - Infrastructure

**Examples:**
```bash
git commit -m "feat(h3): Complete Telegram Approval Bot testing

- End-to-end test passed (CR → Telegram → Approval)
- Backend detects CR in 5 seconds
- Inline button workflow verified
- Database approvals.db working"

git commit -m "docs(memory): Update 01-active-context for H3 completion"

git commit -m "feat(tools): Add TOOLS_INVENTORY.md and WRITE_LOCATIONS.md"
```

---

## Example: Complete Post-Slice Update

**Scenario:** Just completed H3 Telegram Approval Bot testing

**Step 1: Update 01-active-context.md**
```markdown
## Quick Status
progress_pct: 78  # was 76

## Just Finished
- **H3 Telegram Approval Bot** (2025-12-06) - TESTED & OPERATIONAL
  [details...]

## Next Steps
1. H4 VPS Deployment (4-6h)  # NEW - unlocked by H3
2. Judge V2 + Langfuse (60 min)
3. Document victory lap (30 min)  # NEW - celebrate H3
```

**Step 2: Update 02-progress.md**
```markdown
### Slice: H3 Telegram Approval Bot - Testing
**Date:** 2025-12-06
[full entry...]
```

**Step 3: Update TOOLS_INVENTORY.md**
```markdown
### H3: Telegram Approval Bot
**Status:** ✅ TESTED & OPERATIONAL (2025-12-06)
[details...]

**Test Results (2025-12-06):**
- ✅ End-to-end test passed
[results...]
```

**Step 4: Update side-architect-bridge.md**
```markdown
**Phase 2:** ~78% complete  # was 76%

**Recently Completed:**
- ✅ H3 Telegram Approval Bot (TESTED - 2025-12-06)
[...]
```

**Step 5: Git commit**
```bash
git add memory-bank/01-active-context.md
git add memory-bank/02-progress.md
git add memory-bank/TOOLS_INVENTORY.md
git add memory-bank/side-architect-bridge.md

git commit -m "feat(h3): Complete Telegram Approval Bot testing

- Updated progress: 76% → 78%
- Documented H3 test results in TOOLS_INVENTORY
- Added next steps: H4 VPS unlocked
- External LLMs can now see H3 status"
```

---

## Troubleshooting

### "Which file do I update for X?"

| Question | Answer |
|----------|--------|
| **"Where are we now?"** | 01-active-context.md (Quick Status) |
| **"What did we just do?"** | 01-active-context.md (Just Finished) + 02-progress.md |
| **"What tools do we have?"** | TOOLS_INVENTORY.md |
| **"How does it work?"** | ARCHITECTURE_REFERENCE.md |
| **"What should we avoid?"** | patterns/AP-XXX.md |
| **"What works well?"** | patterns/BP-XXX.md |
| **"Tell external LLM"** | side-architect-bridge.md |

---

### "How often do I update each file?"

| File | Update Frequency |
|------|-----------------|
| 01-active-context.md | EVERY slice (Protocol 1) |
| 02-progress.md | EVERY slice (Protocol 1) |
| TOOLS_INVENTORY.md | When tool/API deployed |
| ARCHITECTURE_REFERENCE.md | Major changes only |
| AP-XXX / BP-XXX | When trigger fires |
| side-architect-bridge.md | Major milestones |

---

## Meta-Learning Triggers (Quick Ref)

**From Playbook Section 9:**

- **Trigger A:** Repetition (2nd+ occurrence) → `AP-XXX`
- **Trigger B:** Workaround used → `TD-XXX`
- **Trigger C:** User surprise → Check spec clarity
- **Trigger D:** Research gap (3+ "not sure") → Research slice
- **Trigger E:** Friction point → `BP-XXX` or automation
- **Trigger F:** Protocol created → Apply immediately

---

**End of WRITE_LOCATIONS.md**
