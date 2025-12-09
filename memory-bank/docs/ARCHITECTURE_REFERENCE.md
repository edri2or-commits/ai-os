# Architecture Reference - AI Life OS

**Version:** 1.0.0  
**Authority:** ADR-001  
**Last Updated:** 2025-12-04

---

## Purpose

This document provides the **detailed technical description** of the AI Life OS architecture.  
Read this when you need to understand **how components connect** and **why they're structured this way**.

**Quick Links:**
- Terminology → `CANONICAL_TERMINOLOGY.md`
- Decisions → `docs/decisions/ADR-001-architectural-alignment.md`
- Metaphors → `METAPHOR_GUIDE.md`

---

## 1. The Primary Architecture: Hexagonal (Ports & Adapters)

### 1.1 Core Principles

The Hexagonal Architecture (Alistair Cockburn, 2005) is built on three principles:

**Principle 1: Dependency Inversion**  
Dependencies always point INWARD toward the Application Core.  
The Core never imports or references external technologies.

```
❌ BAD: Core imports n8n library
✅ GOOD: Core defines IWorkflowExecutor port, n8n adapter implements it
```

**Principle 2: Technology Agnostic Core**  
The Application Core contains only business logic and domain rules.  
It has NO knowledge of:
- File systems (Windows vs Linux)
- Databases (SQLite vs PostgreSQL)
- APIs (n8n vs Zapier)
- LLM providers (Anthropic vs OpenAI)

**Principle 3: Testability via Isolation**  
Because the Core depends only on abstract Ports, we can:
- Mock Adapters for unit tests
- Swap implementations without changing Core
- Test Core logic without running Docker/n8n/etc

### 1.2 The Hexagon Layers

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

---

## 2. AI Life OS Component Mapping

### 2.1 The Application Core

**What it is:**  
The aggregation of:
- Claude Sonnet 4.5 (the reasoning engine)
- System Prompts (kernel instructions, governance rules)
- User's active intent (current conversation context)

**What it does:**
- Interprets user intent
- Makes decisions based on rules (ADRs, protocols)
- Plans actions (generates specs, change requests)
- Coordinates Adapters via Ports

**What it does NOT do:**
- Read/write files directly (uses filesystem adapter)
- Execute workflows directly (uses n8n adapter)
- Store long-term memory (uses Git adapter)

**Technology:**  
- LLM: Claude Sonnet 4.5 (via Claude Desktop app)
- Prompts: Project Instructions + Memory Bank context
- State: Ephemeral (context window only)

### 2.2 Primary Ports (Inbound - Driving Side)

**Definition:**  
Entry points where external actors initiate interactions with the Core.

**Examples in AI Life OS:**

| Port Name | Purpose | Driving Actor | Adapter Implementation |
|---|---|---|---|
| IChatInterface | User sends natural language commands | User (human) | Claude Desktop UI |
| IScheduledTrigger | Time-based automation triggers | Windows Task Scheduler | Python scripts |
| IWebhookReceiver | External events trigger workflows | n8n webhook | n8n HTTP Request node |

### 2.3 Secondary Ports (Outbound - Driven Side)

**Definition:**  
Exit points where the Core requests services from the outside world.

**Examples in AI Life OS:**

| Port Name | Purpose | Called By | Adapter Implementation |
|---|---|---|---|
| IFileSystem | Read/write files | Core (Memory Bank access) | filesystem MCP |
| IVersionControl | Git operations | Core (commit changes) | git MCP |
| IWorkflowExecutor | Execute automations | Core (run n8n workflow) | n8n MCP |
| IWebFetcher | Retrieve web content | Core (external info) | fetch MCP |
| IChangeDetector | Monitor for drift | MAPE-K Monitor | Observer script |
| IChangeApplier | Apply approved changes | MAPE-K Executor | Executor script |

### 2.4 MCP as the Universal Adapter Layer

**The Model Context Protocol (MCP) is the realization of the Adapter pattern.**

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
│  Translates JSON-RPC → Windows File API  │
└──────────────┬───────────────────────────┘
               │
       ┌───────▼─────────┐
       │  Windows 11 FS  │
       └─────────────────┘
```

**Why MCP is perfect for Hexagonal:**
- Standardized interface (JSON-RPC 2.0) = Port
- Multiple transport options (stdio, SSE) = Swappable
- Tool discovery = Runtime Port composition
- No Core code changes needed to add new MCP server

**For complete capability map:**  
See `memory-bank/TOOLS_INVENTORY.md` - comprehensive reference of all available tools (MCP servers, REST APIs, Docker services, automations) with capability matrix ("Can I...?" quick lookup).

---

## 3. The MAPE-K Control Loop (Autonomic Layer)

### 3.1 Purpose

MAPE-K (Monitor-Analyze-Plan-Execute-Knowledge) is an **IBM pattern for self-managing systems**.  
It runs **within** the Hexagonal Architecture to provide autonomic behavior.

### 3.2 Component Mapping

```
┌─────────────────────────────────────────────────┐
│                  KNOWLEDGE                      │
│  Truth Layer: Git + Memory Bank + Schemas      │
└───────┬─────────────────────────────────────┬───┘
        │                                     │
┌───────▼─────────┐                   ┌───────▼─────────┐
│    MONITOR      │                   │    EXECUTE      │
│  (Observer)     │                   │  (Executor)     │
│  Detects drift  │                   │  Applies CRs    │
└───────┬─────────┘                   └───────▲─────────┘
        │                                     │
        │  Drift detected                     │  CR approved
        │                                     │
┌───────▼─────────┐                   ┌───────┴─────────┐
│    ANALYZE      │──── Classifies ───▶    PLAN         │
│  (Classifier)   │     severity      │  (Reconciler)   │
│                 │                   │  Generates CRs  │
└─────────────────┘                   └─────────────────┘
```

**Implementation as Hexagonal Adapters:**

| MAPE-K Component | Implements Port | Technology | Scheduling |
|---|---|---|---|
| Monitor (Observer) | IChangeDetector | Python script | Task Scheduler (15 min) |
| Analyze | (in Reconciler) | Python logic | Triggered by Monitor |
| Plan (Reconciler) | IChangeRequestGenerator | Python script | Triggered by Analyzer |
| Execute (Executor) | IChangeApplier | Python script | Manual (user approval) |
| Knowledge | ITruthLayer | Git + filesystem | Always available |

---

## 4. n8n's Dual Role

n8n is unique - it acts as BOTH a Driven Adapter AND a Driving Adapter.

### 4.1 n8n as Driven Adapter (Secondary)

**When:** Core decides to execute a workflow

```
User: "Send me a daily summary email at 8 AM"
  ↓
Core: Plans the automation
  ↓
Core: Calls IWorkflowExecutor.create_workflow()
  ↓
n8n MCP Server: Translates to n8n API call
  ↓
n8n: Stores workflow, activates schedule
```

### 4.2 n8n as Driving Adapter (Primary)

**When:** n8n triggers autonomously (timer, webhook, email)

```
n8n: Timer fires at 8:00 AM
  ↓
n8n: Executes workflow (fetch data, format email)
  ↓
n8n: (Optional) Calls webhook that triggers Core
  ↓
Core: Responds to trigger via IWebhookReceiver port
```

**The Rule:**  
Deterministic, repetitive tasks → n8n drives  
Creative, reasoning-heavy tasks → Core drives

---

## 5. Data Flow Example: "Create a New Project"

**User:** "Create a new project called 'Invoice Automation'"

### Step-by-Step Flow

```
1. User types in Claude Desktop (Primary Adapter: UI)
   ↓
2. Input enters Core via IChatInterface (Primary Port)
   ↓
3. Core reasons: "This is a new project → need to create file"
   ↓
4. Core calls: IFileSystem.write_file(path, content) (Secondary Port)
   ↓
5. MCP Client translates to JSON-RPC
   ↓
6. filesystem MCP Server writes file to Windows (Secondary Adapter)
   ↓
7. Core calls: IVersionControl.commit(message) (Secondary Port)
   ↓
8. git MCP Server commits file (Secondary Adapter)
   ↓
9. Core returns response to user via IChatInterface
```

**Later (Autonomous):**

```
10. Observer (Monitor) runs on schedule
    ↓
11. Detects new file in /10_Projects
    ↓
12. Reconciler (Plan) generates CR: "Update project list in 01-active-context.md"
    ↓
13. User approves CR
    ↓
14. Executor (Execute) applies change via git MCP
```

---

## 6. Anti-Patterns (What NOT to Do)

### ❌ Core Imports Concrete Technology
```python
# BAD
from n8n_client import N8nAPI
api = N8nAPI("http://localhost:5678")
```

```python
# GOOD
# Core calls:
workflow_executor.execute("daily-summary")
# Adapter handles n8n details
```

### ❌ Adapter Contains Business Logic
```python
# BAD (in n8n adapter)
if user.is_premium():
    execute_premium_workflow()
```

```python
# GOOD (in Core)
if user.is_premium():
    executor.execute("premium-workflow")
else:
    executor.execute("standard-workflow")
```

### ❌ Bypassing Ports
```python
# BAD (direct access)
with open("memory-bank/file.txt") as f:
    content = f.read()
```

```python
# GOOD (via Port)
content = filesystem_adapter.read_file("memory-bank/file.txt")
```

---

## References

1. Cockburn, A. (2005). *Hexagonal Architecture*. https://alistair.cockburn.us/hexagonal-architecture/
2. Kephart, J. O. (2003). *The Vision of Autonomic Computing*. Computer, 36(1), 41-50.
3. Netflix Tech Blog. (2020). *Ready for changes with Hexagonal Architecture*.
4. AWS Prescriptive Guidance. *Hexagonal architecture pattern*.
