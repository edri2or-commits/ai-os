# ADR-001: Git-Based Truth Layer for AI Life OS

**Status:** Accepted  
**Date:** 2024-11-15 *(retroactive documentation)*  
**Energy State:** High Clarity  
**Tags:** #storage, #architecture, #sovereignty, #core-decision

---

## Context and Problem Statement

**The Problem:**
My personal data was scattered across multiple platforms:
- Google Drive (documents, but opaque sync)
- Notion (notes, but platform lock-in)
- Claude.ai conversations (valuable context, but ephemeral)
- Local files (unstructured, no version control)

**The ADHD Factor:**
I have **Object Permanence issues**. If I can't see a file, it doesn't exist for me. If I can't easily find something I created last week, it's gone forever. This creates:
- Anxiety about losing work
- Paralysis around organizing (fear of "wrong" folder structure)
- Repeated work (redoing what I already did but can't find)

**The Question:**
What storage system serves as the "single source of truth" for my AI Life OS?

---

## Decision Drivers

1. **Cognitive Sovereignty** (Manifesto Principle I)
   - I must OWN my data completely
   - No vendor should control my "second brain"
   - Must survive business failures, price changes, policy shifts

2. **Visibility** (ADHD Object Permanence)
   - I need to SEE my files in a file browser
   - Human-readable formats (not binary databases)
   - Searchable with basic tools (grep, file explorer)

3. **Safety Net** (ADHD Impulsivity)
   - I make mistakes when hyperfocused
   - I need an "undo button for life"
   - Fear of irreversible mistakes prevents action

4. **AI-Friendly** (Technical Requirement)
   - LLMs work best with text
   - Need easy read/write for agents
   - Standard formats (Markdown, JSON, YAML)

5. **Longevity** (Manifesto Principle IV)
   - Must be readable in 20 years
   - Not dependent on specific software
   - Universal formats

---

## Options Considered

### Option 1: PostgreSQL (Local or Cloud)
**Description:** Structured database with SQL queries

**Pros:**
- Fast queries
- Relational integrity
- Powerful for complex data

**Cons:**
- ❌ **Binary files** (can't just "open in text editor")
- ❌ **High maintenance** (schema migrations, backups)
- ❌ **Not ADHD-friendly** (can't visually browse data)
- ❌ **Opaque to LLMs** (requires ORM or SQL generation)

**ADHD Impact:** Cognitive overhead of DB administration. Object permanence suffers (can't "see" data).

---

### Option 2: Notion API
**Description:** Use Notion as backend via API

**Pros:**
- Beautiful UI
- Easy mobile editing
- Built-in organization

**Cons:**
- ❌ **Platform lock-in** (if Notion dies, my data is hostage)
- ❌ **API latency** (spinners break flow state)
- ❌ **Proprietary format** (export is messy)
- ❌ **No version control** (can't undo 3 weeks ago)

**ADHD Impact:** Network spinners cause distraction. Fear of data loss creates anxiety. Violates Manifesto I.1 (Local-First).

---

### Option 3: Git + Markdown/JSON (Flat Files) ✅
**Description:** File-based storage with Git version control

**Pros:**
- ✅ **Human-readable** (Markdown, JSON, YAML)
- ✅ **Version controlled** (Git = undo button)
- ✅ **Universal** (works with any text editor, OS, tool)
- ✅ **LLM-native** (models trained on text)
- ✅ **Zero lock-in** (files are portable)
- ✅ **Offline-first** (no network required)
- ✅ **Visible** (file explorer = instant object permanence)

**Cons:**
- ⚠️ No built-in mobile UI (need Obsidian or similar)
- ⚠️ Querying is slower than SQL (use grep/ripgrep)
- ⚠️ Merge conflicts possible (but rare in solo work)

**ADHD Impact:** Positive! Visual file structure, instant undo, no spinners, no anxiety.

---

## Decision: Git + Markdown/JSON

**We chose Option 3: Git-Based Flat Files**

---

## Justification

### Core Principle (from Manifesto)
**Manifesto I: Cognitive Sovereignty**
> "The Truth Layer resides on hardware I control. The cloud is a utility for sync and backup, not the primary residence of my cognition."

### Background Problem
ADHD presents three specific challenges:
1. **Working Memory Deficit:** I can't hold complex structures in my head
2. **Impulsivity:** I make changes without thinking through consequences
3. **Object Permanence:** If I can't see it, it doesn't exist

### ADHD Relevance: Why Git Solves This
1. **Externalized Memory:**
   - Git is my "external hard drive" for decisions
   - Every commit message documents WHY I did something
   - I can review my "past self's" reasoning without relying on biological memory

2. **Safety Net for Impulsivity:**
   - Git provides "time travel" (checkout any commit)
   - Mistakes are **reversible** (Barkley: ADHD needs external scaffolding)
   - Fear of messing up no longer paralyzes me → I can experiment freely

3. **Visibility for Object Permanence:**
   - Files in file explorer = immediate visual confirmation
   - Markdown files open in any editor = no "where did I put that?" anxiety
   - GitHub/GitLab provide web-based browsing if needed

4. **Cognitive Ease:**
   - Plain text = no cognitive load of database schemas
   - `git log` = instant history without complex queries
   - Branching = safe "what if?" exploration (aligns with ADHD novelty-seeking)

### Trade-offs (Conscious Downsides)
**Negative:**
- No fancy UI out of box (less polished than Notion)
- Mobile editing requires Obsidian or Working Copy (extra setup)
- Merge conflicts if multi-device editing (rare in solo work)

**Mitigation:**
- Use **Obsidian** as frontend (beautiful UI, mobile apps, Git plugin)
- Use **`ripgrep`** or **`fzf`** for fast text search (faster than SQL for small datasets)
- Use **GitHub Desktop** or **Lazygit** for visual Git operations (reduces command-line friction)

---

## Consequences

### Positive
✅ **Complete data sovereignty** (files live on my machine)  
✅ **Zero vendor lock-in** (can move repo anywhere)  
✅ **LLM-friendly** (agents read/write Markdown natively)  
✅ **Version control built-in** (Git history = audit trail)  
✅ **ADHD-compatible** (visible, reversible, no spinners)  
✅ **Future-proof** (Markdown will be readable in 2050)

### Negative
⚠️ No native mobile UI (mitigated by Obsidian)  
⚠️ Slower complex queries (mitigated by ripgrep + future vector search)  
⚠️ Git learning curve (mitigated by GUI tools)

### System Integration
This decision enables:
- **Truth Layer** as single source of truth (Manifesto I)
- **Memory Bank** structure (PARA organization in folders)
- **Life Graph entities** as Markdown files with YAML frontmatter
- **Observer/Reconciler** tools (can parse file diffs via Git)
- **AI agents** (read/write via filesystem tools)

---

## Validation

**How do we know this was the right choice?**

After 6+ months of use:
- ✅ Zero data loss incidents
- ✅ Git history has saved me 5+ times (accidental deletes)
- ✅ Agents (Claude, GPT) successfully read/write files
- ✅ Memory Bank operational (START_HERE.md, 01-active-context.md work)
- ✅ Object permanence anxiety eliminated (I can SEE my files)
- ✅ No regrets about platform lock-in

---

## References

**Manifesto Sections:**
- Section I.1: Local-First by Default
- Section I.2: Memory Independence
- Section IV.11: Evolutionary Resilience

**Research Families:**
- Architecture / Truth Layer design
- ADHD / Object Permanence (Barkley theory)
- Safety / Git as undo button

**Related Decisions:**
- (Future) ADR-002: Obsidian as frontend UI
- (Future) ADR-003: PARA folder structure

---

**This ADR documents a foundational decision. All subsequent architectural choices build on Git as the Truth Layer.**
