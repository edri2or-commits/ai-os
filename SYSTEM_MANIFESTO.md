# AI Life OS - System Manifesto
**The Definitive Constitution**

**Version:** 2.0  
**Last Updated:** 2025-12-11  
**Authority:** Final consolidation of all system rules  
**Status:** Canonical Reference

---

## Purpose

This document is the **single source of truth** for AI Life OS architecture, protocols, and principles. All other documentation references this manifesto. When conflicts arise, this document takes precedence.

---

## Part I: The Vision

### Who This Is For

**AI Life OS** serves individuals with ADHD by providing a **cognitive prosthetic** – an external executive function system that:

1. **Remembers for you** (object permanence compensation)
2. **Organizes for you** (reduces executive function load)
3. **Executes for you** (eliminates activation energy)
4. **Defends your attention** (prevents context switching)
5. **Improves itself** (reduces maintenance burden)

### What This System Is

A **Personal AI Operating System** – a self-improving, Git-backed, AI architecture that transforms ADHD challenges into systematic strengths through:

- **External working memory** (because internal RAM is limited)
- **Ambient awareness** (tasks visible without effort)
- **Low activation energy** (near-zero friction to start)
- **Reversibility** (Git time-travel removes fear of failure)
- **Behavioral adaptation** (state-aware response patterns)

### Core ADHD Understanding

ADHD is a **performance disorder** caused by four deficits:

1. **Inhibition Deficit** → Cannot resist distractions
2. **Working Memory Deficit** → Tasks disappear from awareness
3. **Emotional Regulation Deficit** → Stress causes avoidance
4. **Temporal Processing Deficit** → Time feels binary (Now/Not Now)

Traditional productivity tools fail because they assume functional executive function. **AI Life OS compensates for these deficits systematically.**

---

## Part II: The Architecture

### Canonical Model: Hexagonal Architecture (Ports & Adapters)

AI Life OS follows **Hexagonal Architecture** (Alistair Cockburn, 2005) as its structural foundation.

#### Core Principles

**Principle 1: Dependency Inversion**  
Dependencies point INWARD toward the Application Core. The Core never imports external technologies.

```
❌ BAD: Core imports n8n library
✅ GOOD: Core defines IWorkflowExecutor port, n8n adapter implements it
```

**Principle 2: Technology Agnostic Core**  
The Application Core contains only business logic and domain rules. It has NO knowledge of:
- File systems (Windows vs Linux)
- Databases (SQLite vs PostgreSQL)
- APIs (n8n vs Zapier)
- LLM providers (Anthropic vs OpenAI)

**Principle 3: Testability via Isolation**  
Because the Core depends only on abstract Ports:
- Mock Adapters for unit tests
- Swap implementations without changing Core
- Test Core logic without running Docker/n8n/etc

#### The Hexagon Layers

```
┌─────────────────────────────────────────────┐
│         PRIMARY ADAPTERS (Driving)          │
│  CLI, Webhooks, Scheduled Tasks, User UI    │
└───────────────┬─────────────────────────────┘
                │
        ┌───────▼───────┐
        │ PRIMARY PORTS │
        │  (Inbound)    │
        └───────┬───────┘
                │
    ┌───────────▼───────────┐
    │   APPLICATION CORE    │
    │  (Business Logic +    │
    │   Claude Reasoning)   │
    └───────────┬───────────┘
                │
        ┌───────▼───────┐
        │ SECONDARY     │
        │ PORTS         │
        │ (Outbound)    │
        └───────┬───────┘
                │
┌───────────────▼─────────────────────────────┐
│        SECONDARY ADAPTERS (Driven)          │
│  MCP Servers: filesystem, git, n8n, fetch   │
└─────────────────────────────────────────────┘
```

### Component Mapping

#### Application Core
**Composition:**
- Claude Sonnet 4.5 (reasoning engine)
- System Prompts (kernel instructions)
- User's active intent (conversation context)

**Responsibilities:**
- Interpret user intent
- Make decisions based on rules (ADRs, protocols)
- Plan actions (generate specs, change requests)
- Coordinate Adapters via Ports

**What it does NOT do:**
- Read/write files directly (uses filesystem adapter)
- Execute workflows directly (uses n8n adapter)
- Store long-term memory (uses Git adapter)

#### MCP as Universal Adapter Layer

The Model Context Protocol (MCP) realizes the Adapter pattern:

```
┌──────────────────────────────────────────┐
│         APPLICATION CORE                 │
│  (Claude + System Prompts)               │
└──────────────┬───────────────────────────┘
               │
       Secondary Port: IFileSystem
               │
┌──────────────▼───────────────────────────┐
│      MCP CLIENT (inside Claude Desktop)  │
│  Translates Port calls → JSON-RPC 2.0    │
└──────────────┬───────────────────────────┘
               │
        stdio transport (pipe)
               │
┌──────────────▼───────────────────────────┐
│    MCP SERVER: @modelcontextprotocol/    │
│            server-filesystem             │
│  Translates JSON-RPC → OS File API       │
└──────────────┬───────────────────────────┘
               │
       ┌───────▼─────────┐
       │  Operating System│
       └─────────────────┘
```

**Why MCP is perfect for Hexagonal:**
- Standardized interface (JSON-RPC 2.0) = Port
- Multiple transport options (stdio, SSE) = Swappable
- Tool discovery = Runtime Port composition
- No Core code changes needed to add new MCP server

---

## Part III: ADHD State Management (NAES v1.0)

### The Innovation

**NAES** (Neuro-Adaptive Executive Scaffold) transforms AI Life OS from generic assistance into genuine neuro-adaptive partnership through **behavioral differentiation based on executive function capacity**.

### 6 Core State Signals

Each signal maps to a specific executive function domain (BRIEF-A):

1. **Energy (Spoons): 1-10 scale**
   - Red zone (1-3): Critical depletion → CRISIS mode
   - Yellow zone (4-6): Moderate capacity
   - Green zone (7-10): Full capacity

2. **Cognitive Clarity:** clear / foggy / mud
   - Maps to: Shifting + Organization domains

3. **Emotional Valence:** negative / neutral / positive
   - Maps to: Emotional Control domain
   - Negative may indicate RSD (Rejection Sensitive Dysphoria)

4. **Sensory Load:** low / medium / high
   - Maps to: Self-Monitor domain

5. **Task Urgency:** low / medium / high / critical
   - **CANONICAL DEFINITION:** "Urgent" = less than 24 hours
   - Maps to: Plan/Organize domains

6. **Time Since Break:** Minutes
   - **CANONICAL DEFINITION:** "Hyperfocus Risk" = over 90 minutes
   - Maps to: Self-Monitor + Shifting domains

### 4 System Modes

**Mode Selection Logic (Priority Order):**

```python
def select_mode(state):
    # Priority 1: Safety (prevent burnout)
    if state["energy_spoons"] <= 3:
        return "CRISIS_RECOVERY"
    
    # Priority 2: Unblock (restore function)
    if state["clarity"] == "mud" or state["initiation_status"] == "stuck":
        return "PARALYSIS_BREAKER"
    
    # Priority 3: Emotional support
    if state["valence"] == "negative" and state["energy_spoons"] > 5:
        return "BODY_DOUBLE"
    
    # Priority 4: Standard operation
    return "FLOW_SUPPORT"
```

#### Mode 1: CRISIS_RECOVERY (Priority 1)
**Trigger:** `energy_spoons <= 3`

**Rules:**
- ❌ Do NOT accept task requests
- ❌ Do NOT provide options
- ✅ Validate rest: "Rest is work"
- ✅ Ultra-minimal response (1-2 sentences max)

#### Mode 2: PARALYSIS_BREAKER (Priority 2)
**Trigger:** `clarity == "mud"` OR `initiation_status == "stuck"`

**Rules:**
- ❌ No multi-step plans
- ❌ No options
- ✅ ONE micro-step per message
- ✅ Binary completion request (👍 emoji)
- ✅ Max 3 sentences

#### Mode 3: BODY_DOUBLE (Priority 3)
**Trigger:** `valence == "negative"` AND `energy_spoons > 5`

**Rules:**
- ✅ Validate emotion FIRST
- ✅ 2-minute commitment (not full task)
- ✅ Stay present
- ❌ NO cheerleading (RSD trigger)
- ❌ NO minimizing

#### Mode 4: FLOW_SUPPORT (Priority 4 - Default)
**Trigger:** All other states

**Rules:**
- ✅ Provide 2-3 options (not 10)
- ✅ Structure: TL;DR + Details
- ✅ Clear next steps
- ✅ Hyperfocus protection at 90 minutes

---

## Part IV: Core Protocols

### AEP-001: ADHD-Aware Execution

**Core Principle:**
```
DEFAULT MODE: I do it
EXCEPTION MODE: User explicitly asks me NOT to do it
```

**Rule 1: NEVER Delegate Manual Work**

FORBIDDEN phrases:
- "Do X" / "Open Y" / "Click Z"

ALLOWED phrases:
- "I'm doing X now"
- "Let me do Y"

**Rule 2: Self-Check Before Every Response**

Before responding, ask:
1. Am I asking the user to do something manually?
2. Can I do it programmatically instead?
3. Do I have the tools/credentials to do it?

If answer to #1 is YES and #2 is YES → STOP. Rewrite response.

**Rule 3: Tool Strategy Priority**

1. API call (best)
2. CLI command (good)
3. UI automation via MCP (acceptable)
4. Ask user for credentials (last resort)
5. Ask user to do it manually (FORBIDDEN)

### MAP-001: Memory Bank Access Protocol

**Truth Layer:**
- Git-backed files = single source of truth
- "If it's not in git, it doesn't exist"
- All important information lives in files

**PARA Structure:**
- 10_Projects: Active work
- 20_Areas: Ongoing responsibilities
- 30_Resources: Reference material
- 40_Archives: Completed/deprecated

---

## Part V: Anti-Patterns & Violations

### Architecture Anti-Patterns

❌ **Core Imports Concrete Technology**
```python
# BAD
from n8n_client import N8nAPI
```

```python
# GOOD
# Core calls:
workflow_executor.execute("daily-summary")
```

❌ **Adapter Contains Business Logic**
```python
# BAD (in n8n adapter)
if user.is_premium():
    execute_premium_workflow()
```

```python
# GOOD (in Core)
if user.is_premium():
    executor.execute("premium-workflow")
```

### ADHD Support Anti-Patterns

❌ **Cheerleading during RSD**
```
User: "I messed up the email"
Bad: "You did great! Don't worry!" [invalidating]
Good: "That feels awful. Mistakes are loud." [validating]
```

❌ **Asking for manual work**
```
Bad: "Open GitHub and click Archive"
Good: "I'm archiving the repo via API now"
```

---

## Part VI: Success Metrics

### System Health

**Architecture Compliance:**
- Core never imports concrete technology: 100%
- All file operations via MCP: 100%
- Port abstraction maintained: 100%

**ADHD Support Effectiveness:**
- Manual delegation rate: 0% (was 100% in incidents)
- Mode accuracy: User overrides < 10% per week
- Crisis prevention: CRISIS mode activated BEFORE burnout
- Hyperfocus prevention: Break acceptance >80% after 90-min nudge

**User Sovereignty:**
- All changes in git (reversible): 100%
- Privacy preserved (local-first): 100%
- User approval required for state changes: 100%

---

## Part VII: References & Authority

### Architecture

1. Cockburn, A. (2005). *Hexagonal Architecture*. https://alistair.cockburn.us/hexagonal-architecture/
2. Kephart, J. O. (2003). *The Vision of Autonomic Computing*. Computer, 36(1), 41-50.

### ADHD Research

1. CHADD (2025). "Harnessing Artificial Intelligence to Live Better with ADHD"
2. Occupational Therapy Now (2025). "Artificial intelligence for adults with ADHD"
3. Roth et al. (2013). BRIEF-A: Behavior Rating Inventory of Executive Function – Adult Version

### System Documentation

**Canonical Sources:**
- This file: `SYSTEM_MANIFESTO.md` (supreme authority)
- Architecture Detail: `memory-bank/docs/ARCHITECTURE_REFERENCE.md`
- ADHD State Detail: `docs/ADHD_STATE_ARCHITECTURE.md`
- Protocols: `memory-bank/protocols/AEP-001_adhd-aware-execution.md`
- Protocols: `memory-bank/protocols/AEP-002_state-management.md`

---

## Part VIII: Evolution & Governance

### Change Process

1. Propose change (ADR format)
2. Test in isolated context
3. Update this manifesto
4. Propagate to referencing documents
5. Commit with clear rationale

### Version History

- **v2.0** (2025-12-11): Final consolidation
  - Resolved architectural conflicts (Hexagonal as canonical)
  - Established ADHD timing definitions (24h urgent, 90min hyperfocus)
  - Unified all system rules into single document

- **v1.x** (2025-11-01 to 2025-12-10): Multiple scattered documents

---

**Status:** CANONICAL - This is the constitution. All documentation must align with this manifesto.