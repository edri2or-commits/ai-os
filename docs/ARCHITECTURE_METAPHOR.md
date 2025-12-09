# AI Life OS Architecture Metaphor

**Version:** 1.0  
**Date:** 2025-12-01  
**Status:** Canonical Reference  

---

## Purpose

This document defines the **single, authoritative architectural metaphor** for AI Life OS. All other documentation must reference this metaphor consistently.

**Rule:** If you're writing documentation for AI Life OS and need to describe the architecture, reference this file, don't create new metaphors.

---

## The Metaphor: Head / Hands / Truth / Nerves

AI Life OS uses a body-inspired metaphor to make the architecture intuitive and ADHD-friendly:

```
┌─────────────────────────────────────────────┐
│                    HEAD                     │
│           (Claude Desktop)                  │
│     Reasoning · Planning · Orchestration    │
└────────────────┬────────────────────────────┘
                 │
         ┌───────┴────────┐
         │     NERVES     │
         │  (MCP Servers) │
         │   Interfaces   │
         └───────┬────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
┌───▼────┐              ┌─────▼─────┐
│ HANDS  │              │   TRUTH   │
│ (n8n)  │              │   (Git)   │
│ Tools  │              │   Files   │
└────────┘              └───────────┘
Execution               Memory
Automation              State
```

---

## Components

### 1. Head = Claude Desktop
**Role:** The thinking, planning, orchestrating brain

**Responsibilities:**
- Break down messy chat into clear specs
- Decide which tools to use (via MCP)
- Design workflows and automations
- Keep alignment with playbook & research
- Human-facing communication

**Why "Head":** Because it reasons, plans, and makes decisions - but doesn't directly manipulate the world.

---

### 2. Hands = n8n + Tools
**Role:** The executing, doing, physical part

**Responsibilities:**
- Run workflows, APIs, cron jobs, webhooks
- Execute repetitive, deterministic jobs
- Interact with external services (Gmail, Calendar, Drive)
- Perform file operations via scripts

**Why "Hands":** Because it does the actual work - manipulating files, sending emails, running code - but doesn't think about strategy.

---

### 3. Truth = Git-backed Files
**Role:** The stable, persistent memory

**Structure:**
- System state files (`docs/system_state/`)
- Memory Bank (PARA structure)
- Life Graph entities (YAML files)
- Research documents
- Playbooks, runbooks, policies

**Why "Truth":** Because git-backed files are the single source of truth. The system never relies on chat history or external memory - everything important lives in files.

**Key Principle:** If it's not in git, it doesn't exist.

---

### 4. Nerves = MCP Servers
**Role:** The interface layer, the connectors

**Examples:**
- Filesystem MCP (read/write local files)
- Git MCP (commits, diffs, history)
- Windows MCP (system operations)
- Google Workspace MCP (Gmail, Calendar, Drive)

**Why "Nerves":** Because they carry signals between the Head and the Hands/Truth - they're the communication channels, not the thinking or doing.

---

## Core Workflow: Chat → Spec → Change

The architecture enforces this pattern:

1. **Chat (Intent & Context)** - Head
   - User talks naturally (Hebrew OK)
   - Head (Claude) asks clarifications
   - Head explores existing state (Truth)

2. **Spec (Blueprint)** - Head → Nerves → Truth
   - Head produces clear spec
   - Spec written to Truth (as file if needed)
   - User reviews and approves

3. **Change (Execution)** - Head → Nerves → Hands → Truth
   - Head orchestrates via Nerves (MCP)
   - Hands execute (n8n, scripts, tools)
   - Changes committed to Truth (git)
   - Head verifies result

**Safety:** Human-in-the-loop at Spec approval. All changes reversible via git.

---

## Why This Metaphor?

### 1. **ADHD-Friendly**
- Physical metaphor is intuitive
- Body parts = clear roles
- No abstract technical jargon

### 2. **Role Clarity**
- Each component has ONE job
- No confusion about responsibilities
- Easy to explain to anyone

### 3. **Naturally Extensible**
- Need more automation? Add Hands
- Need more interfaces? Add Nerves
- Core metaphor stays stable

### 4. **Aligns with Human Experience**
- Users with ADHD often struggle with executive function (Head)
- AI Life OS acts as external executive function prosthetic
- Head/Hands separation mirrors delegating physical tasks while retaining decision control

---

## What This Metaphor Replaces

**Deprecated terms (DO NOT USE):**
- ❌ "Agentic Kernel" (too abstract)
- ❌ "Semantic Microkernel" (too technical)
- ❌ "Core/Ports/Adapters" (Hexagonal Architecture - too technical)
- ❌ "Control Plane" (too infrastructure-focused)
- ❌ "Agents as Family" (confusing with Head/Hands)

**If you find these terms in documentation, replace them with Head/Hands/Truth/Nerves.**

---

## References in Other Documents

**This metaphor is defined in:**
- ✅ `docs/ARCHITECTURE_METAPHOR.md` (this file - canonical source)

**This metaphor is used in:**
- ✅ `memory-bank/project-brief.md` (Vision section)
- ✅ `claude-project/ai-life-os-claude-project-playbook.md` (Section 3)
- ✅ `docs/CONSTITUTION.md` (Core Principles)

**If creating new documentation:** Reference this file for architectural descriptions.

---

## Evolution of This Metaphor

**Version History:**
- **v1.0** (2025-12-01): Established as canonical metaphor, replaced competing metaphors

**Future Changes:**
- Any proposed changes to this metaphor must be discussed and approved explicitly
- Changes should be rare (maybe 1-2 times in entire project lifecycle)
- Changes must update ALL referencing documents

---

**Last Updated:** 2025-12-01  
**Maintained By:** System Architect (Claude Desktop)  
**Status:** Canonical - do not create competing metaphors
