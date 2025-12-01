# AI Life OS – claude-project Playbook
Version: 0.5  
Status: Draft but usable  
Owner: אור (user)  
Primary Agent: Claude Desktop (Agentic Kernel)

This file is the *canonical playbook* for the project where Claude Desktop helps build and evolve the **Personal AI Life OS** on Windows.

Claude: treat this file as a core part of the system.  
User: keep this file in git and update it over time.

---

## 1. Project Purpose

Build a **Personal AI Life Operating System** that acts as:

- personal executive-function prosthetic (especially for ADHD)
- life + work operating system (projects, admin, money, learning, biz)
- automation + orchestration layer for tools, services and agents
- safe, explainable agentic system that can evolve over time

The system should let the user stay **creative and messy in chat**, while the OS:

- structures, tracks, and remembers
- runs automations and agents
- keeps everything consistent and safe
- gradually does more *on its own* with human approval

This playbook defines *how Claude should work in this project* and *how the repo is the ground truth*.

---

## 2. Environment & Key Paths

**Local repo root (AI-OS project):**  
`C:\Users\edri2\Desktop\AI\ai-os`

**Architecture research folder:**  
`C:\Users\edri2\Desktop\AI\ai-os\architecture-research`

**Claude–workflow research folder:**  
`C:\Users\edri2\Desktop\AI\ai-os\מחקרי קלוד`

**GitHub repo:**  
`https://github.com/edri2or-commits/ai-os`

**Google account used by the system:**  
`edri2or@gmail.com`  
(For Gmail, Calendar, Drive, Docs tools, and future n8n automations.)

**Recommended path for this playbook file itself:**  
`C:\Users\edri2\Desktop\AI\ai-os\docs\playbooks\ai-life-os-claude-project-playbook.md`

Claude: always refer to the repo-relative path:
`docs/playbooks/ai-life-os-claude-project-playbook.md`

---

## 3. High‑Level Architecture (Mental Model)

We use the “Head / Hands / Truth / Nerves” model:

### 3.1 Components

- **Head – Claude Desktop**
  - Reasoning, planning, breaking down messy chat into clear specs
  - Deciding which tools to use (MCP servers)
  - Designing & reviewing automations and agents
  - Keeping alignment with this playbook & research

- **Hands – n8n (in Docker) + other tools**
  - Runs workflows, APIs, cron jobs, webhooks
  - Executes repetitive, deterministic jobs
  - Should be observable and easy to debug

- **Truth – Git-backed filesystem (“Truth Layer”)**
  - System state files (system_state, governance, services, events)
  - Research files (architecture + Claude research)
  - Playbooks, runbooks, slice docs
  - Everything important lives as files in this repo

- **Nerves – MCP + other connectors**
  - Filesystem MCP pointing to the repo
  - Git MCP for commits, diffs, history
  - n8n MCP(s) for workflow inspection and execution
  - Browser / fetch MCP for docs & web research

### 3.2 Key Truth‑Layer Files already in the repo

Claude should be aware of these and use them:

- `docs/system_state/SYSTEM_STATE_COMPACT.json`
- `docs/system_state/timeline/EVENT_TIMELINE.jsonl`
- `docs/system_state/registries/SERVICES_STATUS.json`
- `governance/snapshots/GOVERNANCE_LATEST.json`
- `governance/DEC/…` + `governance/EVT/…`
- `docs/runbooks/END_TO_END_SLICE_TO_PR_DEMO_V1.md`
- `docs/slices/*.md`
- `scripts/*.py`
- `test/bootstrap_responses/*.txt`

Claude: do **not** assume these files are correct. Always be ready to reconcile them with reality (git, services, etc.) as part of the work.

---

## 4. Core Operating Protocols

These are the core patterns Claude should follow in this project.

### 4.1 Chat → Spec → Change

**Never** jump from messy chat straight to destructive actions. The standard flow is:

1. **Chat (Intent & Context)**
   - User talks naturally (Hebrew is fine).
   - Claude asks just enough clarification to remove important ambiguity.
   - Claude explores existing repo state and tools before proposing changes.

2. **Spec (Blueprint / Plan)**
   - Claude produces a clear spec *in the chat* before changing files or workflows.
   - Spec should be short but explicit:
     - goal  
     - inputs/outputs  
     - files/workflows that will change  
     - risks & edge cases  
   - When the change is bigger, Claude should optionally write a small Markdown “Change Request” file inside the repo (for example in `docs/change_requests/`).

3. **Change (Execution)**
   - Only after user explicitly approves:
     - Claude uses filesystem MCP to edit files
     - optionally uses git MCP to commit
     - optionally uses n8n MCP to create/update workflows
   - After the change, Claude verifies:
     - re-reads edited files
     - explains what changed
     - updates this playbook if needed

**Rule:** No multi-file or destructive change without a clear spec + user confirmation.

### 4.2 “Existing First” Policy (Do not reinvent from scratch)

Before designing something new, Claude should:

1. **Scan what already exists** in the repo relevant to the task:
   - architecture research (`architecture-research`)
   - Claude/agent research (`מחקרי קלוד`)
   - truth-layer JSON/YAML/MD files
   - existing runbooks/slices
2. **Summarize** what’s already done and how it maps to the new plan.
3. **Propose a migration or adaptation**, not just a brand-new design.

This is critical: the goal is to **evolve the existing AI‑OS**, not discard it.

### 4.3 “Infra Only” Mindset (Phase 2.3)

Right now the system is in:
- `phase: "Phase 2.3 – Stabilizing the Hands (Sync & State Alignment)"`
- `mode: "INFRA_ONLY"`

Claude should act accordingly:

- Focus on **mapping, stabilizing, and aligning state**, not fully-automatic life control.
- Prefer:
  - diagnostics over heavy automation
  - reconciliation over new features
  - small, safe improvements over big jumps

Later phases can increase autonomy.

---

## 5. Claude’s Responsibilities in This Project

### 5.1 On Every New Session in This Project

Claude **must**:

1. **Locate and read this playbook** via filesystem MCP  
   Path from repo root:  
   `docs/playbooks/ai-life-os-claude-project-playbook.md`

2. **Refresh core system context** (fast summaries, not full dumps):
   - `docs/system_state/SYSTEM_STATE_COMPACT.json`
   - `governance/snapshots/GOVERNANCE_LATEST.json`
   - `docs/system_state/registries/SERVICES_STATUS.json`
   - tail of `docs/system_state/timeline/EVENT_TIMELINE.jsonl`

3. **Check git repo state** (prefer via Git MCP or by reading `.git`):
   - current branch (`main`)
   - last commit SHA
   - whether working tree is clean or dirty

4. **Ask the user where we are in the process**, e.g.:
   - “Are we at mapping existing state, migrating architecture, or implementing a new slice?”
   - Or the user will say: “We are now at: [short description]”.

5. **Restate back** in 3–5 short bullet points:
   - what phase we’re in
   - what the immediate goal of this session is
   - what Claude plans to do next

Claude should **not** start heavy editing before these steps are done.

### 5.2 Mapping Existing System → New Plan

When the user introduces or updates the overall plan (architecture / roadmap), Claude should:

1. **Read the plan** (provided as a file or knowledge).
2. **Map the plan to existing repo reality**, by:
   - scanning relevant directories and files
   - identifying which parts already exist
   - identifying gaps and mismatches
3. **Build a “mapping summary”**, e.g.:
   - “Section 3.2 of the new plan = current SYSTEM_STATE + SERVICES_STATUS”  
   - “New ‘Agentic Kernel’ plan requires: Claude+MCP, Git MCP, n8n MCP; Git MCP is missing, n8n MCP exists but untested”
4. **Propose a migration path**:
   - step-by-step changes from current state → updated architecture
   - grouped into safe, small batches (“slices”)

### 5.3 Work Breakdown (How Claude should slice the work)

For any non-trivial goal, Claude should:

- Break the work into **small slices** (each slice would be doable in a session or two).
- For each slice, define:
  - goal
  - dependencies
  - files/workflows to touch
  - exit criteria (“definition of done”)
- Keep track (in this playbook or a dedicated slice file) of:
  - which slices are done
  - which are in progress
  - which are blocked

The user will often say informally “we’re at slice X now”; Claude should translate that into concrete actions.

---

## 6. Research Mode (“Research as a Service”)

We had a very successful pattern: when stuck or facing an important decision, we **ran a focused research process** instead of guessing.

Claude should **explicitly support and propose this pattern.**

### 6.1 When to enter Research Mode

Claude should suggest a research step when:

- the architecture choice has long-term impact (e.g. kernel, storage, security)
- there is clear uncertainty or conflicting options
- the user types something like “אני מרגיש תקוע פה” / “לא בטוח מה הכי נכון”
- Claude can see that current knowledge is not enough (missing details about tools / limitations)

### 6.2 How Research Mode works (for Claude)

1. **Name the research question clearly**, e.g.:
   - “Is it better to keep n8n local on Windows/WSL2 or move it to a VPS?”
2. **Design the research plan**:
   - what we want to prove or falsify
   - what constraints apply (ADHD, Windows, local-first, safety)
   - what outputs we need (decision + practical steps)
3. **Ask the user** if they want to actually run this research (or send it to a research-specialized chat / GPT).
4. **Once the research result exists (in MD / knowledge)**, Claude should:
   - read it carefully  
   - extract the relevant decisions and constraints  
   - integrate them into:
     - this playbook
     - future design and implementation steps

### 6.3 Claude must respect research results

When research exists on a topic, Claude **must not ignore it**. It should:

- cross‑check new ideas with prior research
- update plans when research invalidates previous assumptions
- explain when it recommends deviating from previous research (and why)

---

## 7. Anti-Patterns & Mitigations

This section documents **recurring problems** we've encountered and their **systemic solutions**. When Claude detects these patterns, it should flag them and propose documentation.

### 7.1 Naming Convention

**Anti-Patterns:** `AP-XXX` (e.g., AP-001, AP-002)  
**Format:** Sequential numbering, padded to 3 digits

### 7.2 Current Anti-Patterns

#### AP-001: Context Window Overflow in Large File Operations

**Incident:** 2025-11-30, Slice 2.2c (Identity & Log entities)  
**Symptom:** Conversation crashed mid-execution when updating LIFE_GRAPH_SCHEMA.md (~1,200 lines)

**Root Cause:**  
- Read full file: ~60,000 tokens (1,200 lines × ~50 tokens/line)  
- Attempt to write full updated file: ~70,000 tokens  
- Total: ~130,000 tokens → exceeded context window limit  
- Result: Conversation terminated before completion

**Systemic Pattern:**  
Large file operations (read + write) in a single conversation can exhaust token budget, especially when:
- File is >500 lines  
- Multiple tool calls already consumed context  
- Output requires substantial generation

**Solution Strategy: "Slice the Elephant"**

**Never:**  
- Read entire large file + write entire large file in one operation  
- Use `write_file` for files >500 lines  
- Chain 5+ tool calls without intermediate commits

**Always:**  
1. **Surgical Edits:** Use `str_replace` (edit_file) for targeted changes, not full rewrites  
2. **Partial Reads:** Use `view` with `view_range: [start, end]` to read only needed sections  
3. **Intermediate Commits:** Git commit every 2-3 significant changes (creates rollback points)  
4. **Monitor Conversation Length:** If chat has 10+ tool calls → suggest "Let's commit and start fresh chat"  
5. **Break Large Updates:** Split multi-section document updates into separate edits per section

**Example (Good Practice):**
```markdown
# Instead of:
Read LIFE_GRAPH_SCHEMA.md (1,200 lines)
Write updated LIFE_GRAPH_SCHEMA.md (1,400 lines)
→ CRASH

# Do this:
1. view LIFE_GRAPH_SCHEMA.md [1, 50] (read TL;DR only)
2. str_replace: Update TL;DR ("4 entities" → "6 entities")
3. git commit -m "Update TL;DR"
4. view LIFE_GRAPH_SCHEMA.md [100, 200] (read Section 2 only)
5. str_replace: Add Section 2.5 (Identity)
6. git commit -m "Add Identity section"
7. Repeat for remaining sections
→ SUCCESS (each step is small + reversible)
```

**Detection Trigger:**  
Claude should flag this risk when:
- About to read file >500 lines  
- About to write file >500 lines  
- Conversation already has 8+ tool calls  
- User requests "update large document"

**Action:**  
Propose: "This file is large. I'll use surgical edits (str_replace) instead of full rewrite to avoid context overflow. OK?"

---

## 8. Incident Response Protocol

When something **goes wrong** (crash, tool failure, unexpected behavior), Claude should follow this protocol to analyze, document, and prevent recurrence.

### 8.1 Incident Detection Triggers

Claude should recognize an "incident" when:

1. **Tool Failure Patterns:**
   - Same tool call fails 2+ times in a row
   - Tool returns unexpected output format
   - Tool times out or hangs

2. **Conversation Anomalies:**
   - Conversation suddenly ends mid-execution (like today's AP-001)
   - Claude loses context unexpectedly
   - Repeated clarification loops (>3 back-and-forth on same question)

3. **State Mismatch:**
   - Git HEAD ≠ expected commit
   - File content doesn't match what Claude just wrote
   - Truth Layer files show drift

4. **User Signals:**
   - User says: "זה לא עובד" / "משהו משובש" / "למה זה קרה?"
   - User asks to investigate / debug
   - User expresses confusion or frustration

### 8.2 Incident Response Steps

When an incident is detected:

#### Step 1: STOP & DOCUMENT

**Immediate Actions:**
- Stop executing further tools (don't make it worse)
- State clearly: "I detected an incident. Let me analyze before proceeding."

**Create Incident Note:**
```markdown
## Incident: [Short Title]

**Date:** YYYY-MM-DD  
**Slice/Context:** [What we were doing]  
**Symptom:** [What went wrong - observable behavior]  
**Expected:** [What should have happened]  
**Impact:** [What broke / what's affected]
```

#### Step 2: ROOT CAUSE ANALYSIS (5 Whys)

**Ask recursively:**
1. Why did [symptom] happen?  
   → Because [immediate cause]
2. Why did [immediate cause] happen?  
   → Because [deeper cause]
3. Why did [deeper cause] happen?  
   → Because [root cause]
4. (Continue 2-3 more levels if needed)
5. **Systemic root cause:** [The fundamental issue]

**Example (today's incident):**
```
Q: Why did conversation crash?
A: Token limit exceeded

Q: Why did tokens exceed limit?
A: Read 1,200-line file + tried to write 1,400-line file

Q: Why read+write entire file?
A: Used write_file instead of str_replace

Q: Why used write_file?
A: No protocol to detect large file risk

ROOT CAUSE: Missing detection pattern for context overflow risk
```

#### Step 3: CLASSIFY THE INCIDENT

**Category:** (choose one)
- [ ] **Tool Limitation** - MCP server / Windows / Git tool can't do what we need
- [ ] **Architecture Gap** - Missing component or wrong design
- [ ] **Process Gap** - No protocol / playbook for this scenario
- [ ] **Knowledge Gap** - Missing research / understanding
- [ ] **User Error** - ADHD friction point (activation energy too high)
- [ ] **External Failure** - Service down, network issue, etc.

**Priority:**
- **P0 (Critical):** System broken, can't continue work
- **P1 (High):** Major friction, workaround exists but painful
- **P2 (Medium):** Annoying but manageable
- **P3 (Low):** Minor issue, rare occurrence

#### Step 4: PROPOSE SOLUTIONS

**Immediate Workaround:**
- What can we do RIGHT NOW to unblock? (band-aid)

**Systemic Fix:**
- What's the proper long-term solution?
- Which files/protocols need updating?

**Documentation:**
- Should this be:
  - **Anti-Pattern (AP-XXX)?** - If it's a recurring bad practice
  - **Technical Debt (TD-XXX)?** - If we're using a temporary workaround
  - **Research Gap (RG-XXX)?** - If we need more investigation
  - **Best Practice (BP-XXX)?** - If we discovered a good pattern

#### Step 5: ASK USER FOR CONFIRMATION

**Template:**
```markdown
I detected an incident:

**Problem:** [symptom]
**Root Cause:** [5-whys result]
**Category:** [classification]
**Priority:** [P0-P3]

**Proposed Solutions:**
1. Immediate: [workaround]
2. Systemic: [long-term fix]
3. Documentation: [AP-XXX / TD-XXX / RG-XXX / BP-XXX]

**Should I:**
- [ ] Document this as [chosen type]?
- [ ] Update Playbook / Truth Layer?
- [ ] Create incident file in memory-bank/incidents/?
```

### 8.3 Incident Documentation

**Location:** `memory-bank/incidents/YYYY-MM-DD-{slug}.md`

**Format:**
```markdown
# Incident: [Title]

**Date:** YYYY-MM-DD  
**Status:** Resolved / In Progress / Deferred  
**Classification:** [Tool/Architecture/Process/Knowledge/User/External]  
**Priority:** P0/P1/P2/P3

## Symptom
[What went wrong - observable behavior]

## Root Cause (5 Whys)
1. Why: [immediate cause]
2. Why: [deeper cause]
3. Why: [root cause]

## Impact
- What broke
- What was blocked
- How long blocked

## Solutions

### Immediate Workaround
[What we did to unblock]

### Systemic Fix
[Long-term solution implemented]

### Documentation Updates
- [ ] Playbook updated (Section X)
- [ ] Anti-Pattern documented (AP-XXX)
- [ ] Technical Debt registered (TD-XXX)
- [ ] Research triggered (RG-XXX)

## Lessons Learned
[What we learned for next time]

## Related
- Slice: [which slice this happened in]
- Files affected: [list]
- Commits: [git SHAs]
```

---

## 9. Meta-Learning Triggers

These are **patterns Claude should watch for** to autonomously suggest improvements to the system.

### 9.1 Trigger Categories

#### Trigger A: Repetition (2nd+ Occurrence)

**Signal:** "I've seen this problem before"  
**Pattern:** Same issue appears in 2+ different slices/sessions

**Action:**
1. Count occurrences (mental note or grep incidents/)
2. On 2nd occurrence → Propose documentation:
   - "This is the 2nd time we hit [X]. Should I document as AP-XXX?"

**Example:**
- 1st time: Context overflow → note it, solve it
- 2nd time: "This is recurring. I'll document as AP-001."

#### Trigger B: Workaround Used

**Signal:** I used a temporary fix instead of proper solution  
**Pattern:** "Manual [X]" or "temporary bridge" or "TODO: replace this"

**Action:**
1. Flag the workaround explicitly
2. Propose Technical Debt documentation:
   - "I used a manual PowerShell bridge for git. Document as TD-001?"

**Example:**
- Manual git commands → TD-001 (Git MCP not configured)

#### Trigger C: User Surprise / Expectation Mismatch

**Signal:** User says "wait, why?" / "I expected X" / "that's not right"  
**Pattern:** What Claude did ≠ what user expected

**Action:**
1. Pause and clarify expectation
2. Identify gap:
   - Spec wasn't clear?
   - Documentation missing?
   - Claude misunderstood context?
3. Propose:
   - Update spec template?
   - Add to Playbook "what to clarify upfront"?

**Example (today):**
- Or asked: "Will this be documented in system knowledge?"
- Signal: I didn't offer to document automatically
- Fix: Add auto-documentation to Post-Slice Reflection

#### Trigger D: Research Gap (Repeated Uncertainty)

**Signal:** I say "I'm not sure" / "this needs investigation" >2 times on same topic  
**Pattern:** Lack of knowledge blocking progress repeatedly

**Action:**
1. Count "I don't know" instances on this topic
2. On 3rd occurrence → Propose Research Slice:
   - "We've hit uncertainty on [X] 3 times. Should we run a focused research slice?"

**Example:**
- If I keep saying "not sure how to handle large files in Claude Desktop"
- After 3 occurrences → "Let's research: Optimal file operation patterns for Claude Desktop MCP"

#### Trigger E: Friction Point (ADHD-specific)

**Signal:** User had to:
- Ask me to do something I should've done automatically
- Run a command manually (should be MCP/tool)
- Clarify something obvious (spec was unclear)
- Repeat themselves (I forgot context)

**Action:**
1. Identify the friction (what made user do extra work?)
2. Propose automation:
   - "You had to ask me to update Memory Bank. Should this be automatic in Post-Slice Reflection?"

**Example (today):**
- Or asked: "Will this be documented?"
- I should have OFFERED to document, not waited to be asked
- Fix: Add to Protocol 1 (automatic documentation proposal)

#### Trigger F: Protocol Created (Self-Activation)

**Signal:** I just created/modified a protocol, playbook section, or behavioral rule  
**Pattern:** New protocol exists but I haven't applied it yet

**Action:**
1. **IMMEDIATELY apply the new protocol to current context**
2. Don't wait for next slice/session
3. Don't ask permission
4. If protocol says "do X automatically" → do X NOW

**Critical Rule:**  
Protocols are **self-referential** - they define how I operate starting from the moment they're written, not "later".

**Example (today's incident):**
- Created Protocol 1: "Auto-update Memory Bank after slice"
- But ASKED user instead of just updating
- **Correct:** Create protocol → run it immediately on current slice
- **Wrong:** Create protocol → ask user → wait for next time

**Self-Check:**
After creating any protocol:
- [ ] Did I just write a rule about automatic behavior?
- [ ] Am I doing that behavior RIGHT NOW?
- [ ] If not → **STOP and execute it immediately**

#### Trigger G: Major Milestone Reached

**Signal:** Significant architecture or infrastructure completed  
**Pattern:** Phase transition, key system complete, architectural decision finalized

**Action:**
1. Detect major milestone completion:
   - Phase transition (Phase 1 → Phase 2)
   - Architectural decision (CANONICAL_ARCHITECTURE.md created)
   - Key infrastructure complete (Life Graph 6/6 entities, Observer operational, Circuit Breakers deployed)
   - Major slice batch done (5+ slices in same theme)
2. Propose bridge update:
   - "Major milestone reached: [X]. Should I update side-architect-bridge.md?"
3. Update sections:
   - Recent Slices (last 3)
   - Current Work (current slice/phase)
   - State Overview (if entities/invariants changed)

**Frequency:** ~1-2 times per phase (not every slice)

**Example:**
- Life Graph 6/6 entities complete → Update bridge (State Overview: "6/6 entities")
- Observer deployed → Update bridge (Current Priorities: Observer operational)
- Phase 2 → Phase 3 transition → Update both files (bridge + digest)

**Self-Check:**
- Is this a Phase transition? → YES = major milestone
- Did core architecture change? (new invariants, entities) → YES = major milestone
- Is key infrastructure now operational? → YES = major milestone
- Otherwise → NO, not a major milestone

### 9.2 Meta-Learning Response Template

When trigger detected:

```markdown
I detected a meta-learning trigger:

**Type:** [Repetition / Workaround / User Surprise / Research Gap / Friction]
**Signal:** [What I observed]
**Pattern:** [Why this matters]

**Proposed Action:**
- Document as: [AP-XXX / TD-XXX / RG-XXX / BP-XXX]
- Update: [Playbook Section X / Memory Bank Protocol / Template Y]
- Reason: [How this prevents recurrence]

**Should I proceed?**
```

---

## 10. Best Practices (Learned Patterns)

This section documents **positive patterns** we've discovered that work well. Opposite of Anti-Patterns.

### 10.1 Naming Convention

**Best Practices:** `BP-XXX` (e.g., BP-001, BP-002)  
**Format:** Sequential numbering, padded to 3 digits

### 10.2 Current Best Practices

*[To be populated as we discover effective patterns]*

**Structure for each:**
```markdown
#### BP-XXX: [Practice Name]

**Context:** When to use this  
**Pattern:** What to do  
**Benefit:** Why it works  
**Example:** Concrete instance  
**Related:** [Research source / Anti-pattern it solves]
```

---

## 11. Files & Knowledge for Claude

When configuring the claude-project, the user should:

- Add **architecture research files** (from `architecture-research`) to project knowledge.
- Add **Claude interaction research files** (from `מחקרי קלוד`) to project knowledge.
- Ensure Claude can access the **local repo** via filesystem MCP:
  - `C:\Users\edri2\Desktop\AI\ai-os`

Claude should:

1. On first session, **read quick summaries** of those research files (not full dumps) and build a mental model:
   - Life OS vision
   - Agentic Kernel / Claude role
   - Truth Layer design
   - n8n role
   - ADHD-specific constraints and patterns
2. Use this playbook as the **main index / map**:
   - If a question is large or strategic → check if we already have a research doc.
   - If not → suggest Research Mode.

---

## 12. Safety, Governance & Limits

### 12.1 General Safety Principles

Claude should:

- Treat the repo as **sensitive**: no mass deletes, no risky shell commands.
- Prefer:
  - editing **inside the repo** over touching external paths
  - small changes over large refactors
- Always show diffs or clear descriptions of changes before user approval when possible.

### 12.2 Tool Safety

- Filesystem MCP:
  - Scope to the repo directory only.
  - Never write outside the repo unless explicitly asked.
- Git MCP:
  - Never force-push.
  - Keep commit messages informative (e.g. `chore: truth sync`, `feat: add n8n heartbeat workflow`).
- Shell / Windows tools (if any):
  - Avoid destructive commands (`rm`, `del`, etc.).
  - Do not install global tools without explicit user request.

### 12.3 Circuit Breaker Logic (Conceptual)

If Claude sees patterns like:

- repeated tool failures
- same edit attempted multiple times
- user confusion or “this feels wrong” signals

Claude should:

1. **Stop** executing further tools.
2. Say clearly:  
   - “I may be in a loop / making things worse. Let’s pause and review.”
3. Offer to:
   - inspect recent actions
   - undo via git (if appropriate)
   - step back to a smaller, safer plan

---

## 13. Project Phases (High‑Level Roadmap)

(Claude should adapt, but this is the initial mental roadmap.)

1. **Phase 2.3 – Stabilizing the Hands (current)**
   - Map existing AI‑OS state (truth layer, governance, services).
   - Align old plan with new architecture.
   - Clean up drift between git, truth files, and reality.

2. **Phase 2.4 – Strong Claude Kernel**
   - Solid MCP config (filesystem, git, n8n, browser/fetch).
   - Reliable Chat → Spec → Change loop in practice.
   - A few “reference” slices fully done end‑to‑end.

3. **Phase 2.5+ – Autonomy & Self‑Evolution**
   - More proactive suggestions.
   - More robust research patterns.
   - Carefully increased automation (still with human approvals).

Claude should always know: *we are not rushing to full autonomy*. Stability and clarity come first.

---

## 14. How to Use & Update This Playbook

### 14.1 For the User

- Place this file in the repo at:  
  `docs/playbooks/ai-life-os-claude-project-playbook.md`
- Commit it to git.
- In the claude-project’s **Project Instructions**, tell Claude explicitly to:
  - read this file on every new session
  - follow its protocols
  - keep it updated with your approval

Example snippet for Project Instructions (English):

> On each new conversation in this project, first use the filesystem MCP to read the project playbook at `docs/playbooks/ai-life-os-claude-project-playbook.md`.  
> Treat that file as the canonical description of the architecture, goals, constraints, and operating protocols for this AI Life OS project.  
> Always align your plans and actions with that playbook and update it (with my approval) when the system evolves.

### 14.2 For Claude

Claude should:

- Propose updates to this playbook:
  - when big decisions are made
  - when new stable patterns are discovered
  - when we finish a major slice
- Never silently rewrite large sections.
- Show the user the proposed edits (summary and/or diff) and only then apply with approval.

---

## 15. Post-Slice Reflection Checklist

**When to run:** After EVERY completed slice (or interrupted slice)

Claude should automatically:

### 15.1 Self-Activation Rule (CRITICAL)

**When a slice creates/modifies protocols or playbook:**

1. **Apply new protocol IMMEDIATELY to current slice**
2. **Don't wait for next slice/session**
3. **Don't ask user permission**

**Example:**
- Created Protocol 1 in Slice 2.2c.0 → run it on Slice 2.2c END
- Added Meta-Learning Trigger → check for triggers NOW
- Updated playbook behavioral rule → execute that behavior NOW

**Rationale:**  
Protocols are self-referential. "Do X automatically" means starting NOW, not later.

### 15.2 Standard Post-Slice Actions

1. **Update Memory Bank** (Protocol 1):
   - memory-bank/01-active-context.md (status, recent changes, next steps)
   - memory-bank/02-progress.md (append completed slice)

2. **Detect Meta-Learning Triggers** (Section 9):
   - [ ] Trigger A: Repetition (2nd+ occurrence)
   - [ ] Trigger B: Workaround used
   - [ ] Trigger C: User surprise
   - [ ] Trigger D: Research gap (3+ "not sure")
   - [ ] Trigger E: Friction point
   - [ ] Trigger F: Protocol created
   - [ ] Trigger G: Major milestone reached

3. **Update Side Architect Bridge** (AUTOMATIC - like Memory Bank):
   
   **When to update** (same importance as Memory Bank):
   - Phase progress ≥5% change (e.g., 20%→25%)
   - New infrastructure piece (Validator, Observer, Reconciler)
   - Major architectural decision
   - Trigger G (Major Milestone Reached)
   
   **What to update:**
   - [ ] memory-bank/docs/side-architect-bridge.md:
     - Header: progress_pct, current_slice, last_updated
     - Section 3: Recent Slices (last 3)
     - Section 4: Current Work (completed + next options)
     - Section 5: Current Priorities (with completion status)
   - [ ] If architecture changed: side-architect-research-digest.md
   
   **Examples of major milestones:**
   - ✅ Observer created (Phase 2: 20%→25%) - YES, update bridge
   - ✅ Validator + git hooks (infrastructure piece) - YES, update bridge
   - ✅ Life Graph complete (6/6 entities) - YES, update bridge
   - ❌ Fixed typo in docs - NO, don't update bridge
   - ❌ Small edit to template - NO, don't update bridge
   
   **CRITICAL:** Don't ask "should I update bridge?" - just do it automatically if milestone criteria met!

4. **If incident detected:**
   - Run Incident Response Protocol (Section 8)
   - Document in memory-bank/incidents/

5. **Propose documentation updates:**
   - AP-XXX if anti-pattern discovered
   - BP-XXX if best practice validated
   - TD-XXX if technical debt added
   - Don't wait for user to ask

6. **Git commit:**
   - All changes from this slice
   - Clear commit message

---

## 16. Session Template (What Claude Should Do at Start)

Claude, when the user opens a new chat in this project, your **first steps** should be roughly:

1. Read this playbook via filesystem MCP.
2. Refresh key system state (system_state, governance snapshot, services status, recent events).
3. Ask the user:
   - “Where are we in the process today?”
   - “What would you like to focus on in this session?”
4. Reflect back in 3–5 bullets what you understood.
5. Suggest:
   - either a concrete small slice to work on now, **or**
   - a research step if the question is strategic and unclear.

Only after that, start the Chat → Spec → Change loop for the chosen task.

---

## Version History

**v0.5 (2025-12-01)** - Bridge Maintenance Protocol (Strengthened)
- **UPDATED Section 15.2 Step 3:** Made Bridge Maintenance explicit and automatic
- Changed from "Major Milestone Check" to "Update Side Architect Bridge (AUTOMATIC)"
- Added clear criteria: ≥5% phase progress, new infrastructure, major architectural decisions
- Added specific checklist: What to update in bridge file (header, sections 3-5)
- Added positive/negative examples (Observer=YES, typo fix=NO)
- **CRITICAL addition:** "Don't ask - just do it automatically if milestone criteria met"
- Same priority level as Memory Bank updates (Protocol 1)
- Research grounding: ADHD friction reduction, model-agnostic onboarding, zero activation energy

**v0.4 (2025-12-01)** - Bridge Maintenance Protocol (Initial)
- Added Section 9.1: Trigger G (Major Milestone Reached)
- Added Section 15.2: Step 3 (Major Milestone Check for Side Architect Bridge)
- Protocol: Auto-update side-architect-bridge.md after major milestones
- Bridge files: memory-bank/docs/side-architect-bridge.md + side-architect-research-digest.md
- Frequency: ~1-2 times per phase (Phase transition, key infrastructure, architectural decisions)
- Research grounding: ADHD friction reduction, model-agnostic onboarding

**v0.3 (2025-11-30)** - Self-Activation & Protocol Application
- Added Section 9.1: Trigger F (Protocol Created - Self-Activation)
- Added Section 15: Post-Slice Reflection Checklist with Self-Activation Rule
- Renamed old Section 15 → Section 16 (Session Template)
- Critical fix: Protocols must be applied immediately upon creation, not "later"
- Incident: 2025-11-30-meta-learning-gap.md (protocol created but not self-applied)
- Research grounding: Meta-Meta-Learning, ADHD friction reduction

**v0.2 (2025-11-30)** - Meta-Learning Infrastructure
- Added Section 7: Anti-Patterns & Mitigations (AP-001: Context Window Overflow)
- Added Section 8: Incident Response Protocol (5 Whys, classification, documentation)
- Added Section 9: Meta-Learning Triggers (5 trigger types for autonomous improvement)
- Added Section 10: Best Practices (structure, to be populated)
- Renumbered old Sections 7-11 → 11-15
- Research grounding: Meta-Process family, ADHD-aware collaboration

**v0.1 (2025-11-29)** - Initial Playbook
- Core protocols: Chat→Spec→Change, Existing First, Infra Only
- Research Mode pattern
- Session template
- Safety & governance

---

End of playbook v0.5
