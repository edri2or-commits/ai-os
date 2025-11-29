# AI Life OS – Claude Project Playbook
Version: 0.1  
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
`C:\Users\edri2\Desktop\AI\ai-os\מחקרי ארכיטקטורה`

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
   - architecture research (`מחקרי ארכיטקטורה`)
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

## 7. Files & Knowledge for Claude

When configuring the Claude project, the user should:

- Add **architecture research files** (from `מחקרי ארכיטקטורה`) to project knowledge.
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

## 8. Safety, Governance & Limits

### 8.1 General Safety Principles

Claude should:

- Treat the repo as **sensitive**: no mass deletes, no risky shell commands.
- Prefer:
  - editing **inside the repo** over touching external paths
  - small changes over large refactors
- Always show diffs or clear descriptions of changes before user approval when possible.

### 8.2 Tool Safety

- Filesystem MCP:
  - Scope to the repo directory only.
  - Never write outside the repo unless explicitly asked.
- Git MCP:
  - Never force-push.
  - Keep commit messages informative (e.g. `chore: truth sync`, `feat: add n8n heartbeat workflow`).
- Shell / Windows tools (if any):
  - Avoid destructive commands (`rm`, `del`, etc.).
  - Do not install global tools without explicit user request.

### 8.3 Circuit Breaker Logic (Conceptual)

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

## 9. Project Phases (High‑Level Roadmap)

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

## 10. How to Use & Update This Playbook

### 10.1 For the User

- Place this file in the repo at:  
  `docs/playbooks/ai-life-os-claude-project-playbook.md`
- Commit it to git.
- In the Claude project’s **Project Instructions**, tell Claude explicitly to:
  - read this file on every new session
  - follow its protocols
  - keep it updated with your approval

Example snippet for Project Instructions (English):

> On each new conversation in this project, first use the filesystem MCP to read the project playbook at `docs/playbooks/ai-life-os-claude-project-playbook.md`.  
> Treat that file as the canonical description of the architecture, goals, constraints, and operating protocols for this AI Life OS project.  
> Always align your plans and actions with that playbook and update it (with my approval) when the system evolves.

### 10.2 For Claude

Claude should:

- Propose updates to this playbook:
  - when big decisions are made
  - when new stable patterns are discovered
  - when we finish a major slice
- Never silently rewrite large sections.
- Show the user the proposed edits (summary and/or diff) and only then apply with approval.

---

## 11. Session Template (What Claude Should Do at Start)

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

End of playbook v0.1
