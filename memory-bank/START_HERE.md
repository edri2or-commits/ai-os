# START HERE - New Claude Instance Onboarding

**If you are a new Claude instance in this project, this is your entry point.**

---

## ?? If You're Lost: Start Here

**Feeling confused about WHY this system exists? Lost in technical details?**

?? **Read FIRST:** `memory-bank/00_The_Sovereign_AI_Manifesto.md`

This is your **"North Star"** - it explains:
- WHY AI Life OS exists (it's a Prosthetic Executive Cortex for ADHD)
- 4 Core Principles (Cognitive Sovereignty, Attention Defense, Executive Prosthesis, The Gardener)
- Journey Map connecting to all other documentation
- ADHD-specific justifications for every architectural choice

**When to read it:**
- First time in this project ? Read it
- User says "������ �����" (lost control) ? Point them to Manifesto
- Confused about WHY a decision was made ? Check Manifesto principles
- Need to explain the system to someone ? Start with Manifesto

**Then proceed with normal onboarding:**

---

## Quick Context Load (< 2 minutes)

Follow these steps in order:

### Step 1: Read Project Brief
?? **File:** `memory-bank/project-brief.md`

**What you'll learn:**
- Vision: What is AI Life OS?
- Why does it exist?
- TL;DR summary (20 seconds)

---

### Step 2: Read Current Active Context ? MOST IMPORTANT
?? **File:** `memory-bank/01-active-context.md`

**What you'll learn:**
- Current Phase and % completion
- Recent changes (last 5-8 slices)
- Next steps (2-3 proposed options)
- **This is your ground truth!**

---

### Step 3: (Optional) Read Full History
?? **File:** `memory-bank/02-progress.md`

**Only if you need:**
- Full chronological history of all slices
- Detailed context from previous work

**Most of the time, Steps 1-2 are enough to start working!**

---

### Step 4: (Special Context) Active Work Handoffs
?? **If working on specific subsystems, check for handoff docs:**

**Validation Sprint:**
- **File:** `memory-bank/docs/VALIDATION_SPRINT_HANDOFF.md`
- **When to read:** If continuing validation work (VAL-* slices)
- **Contains:** 
  - Completed work (VAL-7, VAL-4) with test results
  - Remaining items (VAL-1b, VAL-1, VAL-6, VAL-8, VAL-9)
  - Tool setup instructions (MCP Inspector, pytest, etc.)
  - 3 recommended approaches (Quick Win, Security-First, ADHD-Optimized)
  - Success criteria (95% empirical confidence target)

**Other handoff docs:** Check `memory-bank/docs/` for subsystem-specific handoffs.

---

### Step 5: ?? Research Corpus (13 Reports - FOR DEEP DIVES ONLY)
?? **Location:** `claude-project/revolution-research/`

**IMPORTANT: You don't need to read all 350 pages to start working!**

**When to reference:**
- Building Layer 0-4 features
- Validating architectural decisions
- Understanding WHY a pattern was chosen
- Resolving technical questions with empirical evidence

**Quick Navigation:**
1. **File:** `RESEARCH_INDEX.md` - Overview of all 13 reports (Quick Reference Table)
2. **File:** `REVOLUTION_INTEGRATION.md` ? **MOST IMPORTANT** - Maps research to 5 Layers + 7 Critical Gaps

**The 13 Research Reports:**
1. Human-AI Collaboration Theory (LOA Framework)
2. Reinforcement Learning for Self-Improvement
3. Multi-Agent Orchestration Patterns
4. Vector Memory & Context Management
5. Production AI Reliability & Monitoring
6. ADHD-Optimized Design Patterns (THE BIBLE)
7. Security in Agentic AI Systems
8. n8n Enterprise Production Patterns
9. Claude Desktop + MCP + Windows Integration
10. Git-Based Autonomous AI Operating Systems
11. Production Operations & Maintenance
12. Local LLM Optimization
13. Layer 4 Observability & Trust Calibration

**Coverage:**
- **Layer 0 (Substrate):** Research 4, 8, 10, 11
- **Layer 1 (Router):** Research 5, 11
- **Layer 2 (Assistant):** Research 9, 12
- **Layer 3 (Architect):** Research 1, 1.5, 3, 13
- **Layer 4 (Strategist):** Research 2, 13
- **Cross-Cutting:** Research 6 (ADHD), Research 7 (Security)

**How to use:**
1. Check `REVOLUTION_INTEGRATION.md` first (maps research to your current work)
2. Read specific research report sections as needed (not entire reports!)
3. Every architectural decision should reference research for 95% confidence

**DON'T:**
- Read all 13 reports upfront (cognitive overload!)
- Try to memorize everything (use as reference)
- Ignore research when making architectural decisions

**DO:**
- Reference research when user asks "why this pattern?"
- Cite research numbers when validating decisions (e.g., "Research #9 shows...")
- Use REVOLUTION_INTEGRATION.md as your navigation map

---

## After Reading - Summarize to User (Hebrew)

Before doing ANY work, tell the user in Hebrew:

```
���! ����� �� Memory Bank.

?? **���� �����:**
- Phase 2: Core Infrastructure (~32% complete)
- ������ �������: Architecture Cleanup (single metaphor established - Head/Hands/Truth/Nerves)
- ���: Fix TD-002 (Windows MCP stdout) �� Reconciler Apply (2.4c) �� Scheduled Observer (2.3b)

?? **�������� �����:**
1. Fix TD-002 - Investigate Windows MCP stdout issue (blocker for apply validation)
2. Continue Reconciler - Apply Logic (2.4c) if willing to skip validation
3. Scheduled Observer (2.3b) - n8n automation

�� ���� �����?
```

**Note:** This is updated as of 2025-12-01. Always update with actual current state from `01-active-context.md`.

---

## Critical Rules

### ? DO:
- Read these 2 files FIRST: project-brief.md + 01-active-context.md
- Summarize current state to user in Hebrew
- Wait for user to choose direction before starting work
- Follow the Chat?Spec?Change pattern
- Auto-update Memory Bank after every slice (Protocol 1)

### ? DON'T:
- Start working without reading Memory Bank
- Skip the summary step
- Read all files randomly - follow the order above
- Guess the current state - check 01-active-context.md
- Ask "should I update Memory Bank?" - just do it automatically

---

## Self-Check Before Starting Work

**Ask yourself:**
- ? Did I read project-brief.md?
- ? Did I read 01-active-context.md completely?
- ? Did I summarize to user: Phase, %, recent work, 2-3 next options?
- ? Did I wait for user to choose direction?
- ? User confirmed before I started executing?

**If any answer is NO ? STOP and complete that step first!**

---

## Additional Resources (for later)

Once you're working, you can reference:

### Narrative Layer (WHY & HOW)

- **Manifesto:** `memory-bank/00_The_Sovereign_AI_Manifesto.md` ?
  - WHY this system exists (Prosthetic Executive Cortex for ADHD)
  - 4 Core Principles with ADHD justifications
  - Journey Map to all other docs
  
- **ADRs (Architecture Decision Records):** `memory-bank/docs/decisions/`
  - WHY specific technical choices were made
  - Example: ADR-001 explains Git Truth Layer decision
  - Each ADR includes ADHD Relevance section
  
- **Design Guide:** `docs/ATTENTION_CENTRIC_DESIGN.md`
  - HOW to build ADHD-friendly interfaces
  - 5 Core Patterns (North Star, Time Materialization, Bouncer, Scaffolding, Panic Button)
  - Visual Grammar rules + Implementation Checklist

### Technical Layer

- **Playbook:** `claude-project/ai-life-os-claude-project-playbook.md`
  - Phases, slices, protocols, anti-patterns, best practices
  
- **Life Graph Schema:** `memory-bank/docs/LIFE_GRAPH_SCHEMA.md`
  - 6 entities, relationships, ADHD metadata
  
- **Architecture:** `docs/ARCHITECTURE_METAPHOR.md`
  - Head/Hands/Truth/Nerves metaphor (canonical)
  
- **Research Corpus:** `claude-project/research_claude/`
  - 18 research files organized in 7 families
  
- **Incidents:** `memory-bank/incidents/`
  - Past incidents with 5 Whys analysis
  
- **Best Practices:** `memory-bank/best-practices/`
  - BP-XXX files with validated patterns

**Navigation Tips:**
- Confused about WHY? ? Read Manifesto or ADRs
- Building UI? ? Read ATTENTION_CENTRIC_DESIGN.md
- Technical question? ? Read Playbook or Architecture
- Historical context? ? Read 02-progress.md

**But don't read these until you need them!** Start with project-brief + 01-active-context.

---

## Why This Matters

**Without this context load:**
- ? You might redo work that's already done
- ? You might miss important architectural decisions
- ? You might ignore technical debt (TD-XXX)
- ? You might create drift between documentation and reality

**With this context load:**
- ? You continue smoothly from where we left off
- ? You respect the existing architecture and decisions
- ? You maintain system integrity
- ? You work efficiently with ADHD-aware workflows

---

**Now go read project-brief.md and 01-active-context.md!** ??
