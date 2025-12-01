# START HERE - New Claude Instance Onboarding

**If you are a new Claude instance in this project, this is your entry point.**

---

## Quick Context Load (< 2 minutes)

Follow these steps in order:

### Step 1: Read Project Brief
📄 **File:** `memory-bank/project-brief.md`

**What you'll learn:**
- Vision: What is AI Life OS?
- Why does it exist?
- TL;DR summary (20 seconds)

---

### Step 2: Read Current Active Context ⭐ MOST IMPORTANT
📄 **File:** `memory-bank/01-active-context.md`

**What you'll learn:**
- Current Phase and % completion
- Recent changes (last 5-8 slices)
- Next steps (2-3 proposed options)
- **This is your ground truth!**

---

### Step 3: (Optional) Read Full History
📄 **File:** `memory-bank/02-progress.md`

**Only if you need:**
- Full chronological history of all slices
- Detailed context from previous work

**Most of the time, Steps 1-2 are enough to start working!**

---

## After Reading - Summarize to User (Hebrew)

Before doing ANY work, tell the user in Hebrew:

```
היי! קראתי את Memory Bank.

📍 **איפה אנחנו:**
- Phase 2: Core Infrastructure (~27% complete)
- סיימנו לאחרונה: Reconciler Design (2.4a - CR schema, HITL workflow, 5 safety invariants)
- הבא: Reconciler Implementation (2.4b) או Scheduled Observer (2.3b)

🎯 **אפשרויות להמשך:**
1. Reconciler Implementation (2.4b) - Minimal impl for safe drift types
2. Scheduled Observer (2.3b) - n8n automation
3. CR Approval CLI (2.4c) - After 2.4b

מה תרצה לעשות?
```

**Note:** This is a real example from 2025-12-01. Always update with actual current state from `01-active-context.md`.

---

## Critical Rules

### ✅ DO:
- Read these 2 files FIRST: project-brief.md + 01-active-context.md
- Summarize current state to user in Hebrew
- Wait for user to choose direction before starting work
- Follow the Chat→Spec→Change pattern
- Auto-update Memory Bank after every slice (Protocol 1)

### ❌ DON'T:
- Start working without reading Memory Bank
- Skip the summary step
- Read all files randomly - follow the order above
- Guess the current state - check 01-active-context.md
- Ask "should I update Memory Bank?" - just do it automatically

---

## Self-Check Before Starting Work

**Ask yourself:**
- ☐ Did I read project-brief.md?
- ☐ Did I read 01-active-context.md completely?
- ☐ Did I summarize to user: Phase, %, recent work, 2-3 next options?
- ☐ Did I wait for user to choose direction?
- ☐ User confirmed before I started executing?

**If any answer is NO → STOP and complete that step first!**

---

## Additional Resources (for later)

Once you're working, you can reference:

- **Playbook:** `claude-project/ai-life-os-claude-project-playbook.md`
  - Phases, slices, protocols, anti-patterns, best practices
  
- **Life Graph Schema:** `memory-bank/docs/LIFE_GRAPH_SCHEMA.md`
  - 6 entities, relationships, ADHD metadata
  
- **Research Corpus:** `claude-project/research_claude/`
  - 18 research files organized in 7 families
  
- **Incidents:** `memory-bank/incidents/`
  - Past incidents with 5 Whys analysis
  
- **Best Practices:** `memory-bank/best-practices/`
  - BP-XXX files with validated patterns

**But don't read these until you need them!** Start with project-brief + 01-active-context.

---

## Why This Matters

**Without this context load:**
- ❌ You might redo work that's already done
- ❌ You might miss important architectural decisions
- ❌ You might ignore technical debt (TD-XXX)
- ❌ You might create drift between documentation and reality

**With this context load:**
- ✅ You continue smoothly from where we left off
- ✅ You respect the existing architecture and decisions
- ✅ You maintain system integrity
- ✅ You work efficiently with ADHD-aware workflows

---

**Now go read project-brief.md and 01-active-context.md!** 📚
