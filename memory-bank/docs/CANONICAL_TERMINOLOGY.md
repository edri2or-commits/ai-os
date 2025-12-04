# Canonical Terminology - AI Life OS

**Version:** 1.0.0  
**Last Updated:** 2025-12-04  
**Authority:** ADR-001 (Architectural Alignment)  
**Purpose:** Single source of truth for ALL system terminology

---

## 🚨 IRON LAW: Use ONLY These Terms

This document is the **ONLY** authoritative source for system terminology.  
Any term not listed here requires an ADR before use.

---

## Core Architecture Terms

### Primary Architecture: Hexagonal (Ports & Adapters)

| Canonical Term | Meaning | Synonyms (Acceptable) | ❌ DO NOT USE |
|---|---|---|---|
| **Application Core** | Business logic + reasoning layer (Claude + prompts) | Core, Hexagon | Semantic Microkernel, Brain, Kernel |
| **Port** | Abstract interface contract (defined by Core) | Interface | API, Endpoint |
| **Adapter** | Concrete implementation of a Port | Implementation, Plugin | Driver, Module |
| **Primary Port** | Entry point driven by external actors (user, scheduler) | Driving Port, Inbound Port | Input, Consumer |
| **Secondary Port** | Exit point to external services (filesystem, n8n) | Driven Port, Outbound Port | Output, Provider |
| **Primary Adapter** | Implements Primary Port (e.g., CLI, webhook receiver) | Driving Adapter | Controller |
| **Secondary Adapter** | Implements Secondary Port (e.g., MCP servers) | Driven Adapter | Service |

**Source:** <cite>Alistair Cockburn (2005), Hexagonal Architecture</cite>

---

## Control Loop Terms (MAPE-K Pattern)

| Canonical Term | Meaning | Component in AI Life OS | ❌ DO NOT USE |
|---|---|---|---|
| **Monitor** | Detects changes in managed resources | Observer (drift detection) | Watcher, Scanner |
| **Analyze** | Interprets monitored data, classifies issues | Change Classifier | Processor, Evaluator |
| **Plan** | Generates adaptation strategies | Reconciler (generates CRs) | Planner, Strategizer |
| **Execute** | Applies approved changes | Executor (applies CRs) | Runner, Deployer |
| **Knowledge** | Shared data/rules for the loop | Truth Layer (Git + Memory Bank) | Memory, Storage |

**Source:** <cite>IBM Autonomic Computing (2001), MAPE-K Reference Model</cite>

---

## MCP (Model Context Protocol) Terms

| Canonical Term | Meaning | Example | ❌ DO NOT USE |
|---|---|---|---|
| **MCP Host** | Container application | Claude Desktop | Client, App |
| **MCP Client** | Translator inside Host | Embedded in Claude Desktop | Proxy, Connector |
| **MCP Server** | External tool/service provider | filesystem MCP, git MCP, n8n MCP | Plugin, Extension, Driver |
| **Tool** | Exposed function via MCP | read_file, git_commit, n8n_trigger | Command, Action, Function |
| **Resource** | Data source exposed via MCP | File contents, Git log | Data, Content |
| **Transport** | Communication method | stdio (pipes), sse (HTTP) | Channel, Protocol |

**Source:** <cite>Model Context Protocol Specification (Anthropic)</cite>

---

## System Components

| Canonical Term | Meaning | Technology | ❌ DO NOT USE |
|---|---|---|---|
| **Application Core** | Reasoning + decision-making | Claude Sonnet 4.5 + system prompts | AI, Agent, Brain, LLM |
| **Truth Layer** | Persistent, version-controlled state | Git repository (ai-os) | Memory, Database, Storage |
| **Memory Bank** | Structured context for continuity | /memory-bank directory (PARA) | Knowledge Base, Docs |
| **Life Graph** | Entity relationship model | YAML files (Projects/Areas/Tasks/etc) | Data Model, Graph DB |
| **Observer** | Drift detection automation | Python script (scheduled via Task Scheduler) | Monitor, Watcher, Daemon |
| **Reconciler** | Change request generator | Python script | Planner, Fixer |
| **Executor** | Approved change applier | Python script | Runner, Deployer, Automator |
| **Automation Engine** | Deterministic workflow execution | n8n (Docker container) | Orchestrator, Scheduler, Bot |

---

## Metaphor Terms (For Communication ONLY)

These are **NOT architecture terms** - use for explaining concepts to humans.

| Metaphor | When to Use | Core Idea | ❌ Architectural Use |
|---|---|---|---|
| **LLM as OS** | Explaining resource management (context = RAM) | LLM = kernel, tools = drivers | Don't call Claude "the kernel" in specs |
| **Cognitive Prosthetic** | Describing user benefit (ADHD support) | System extends executive function | Don't call Git "prosthetic memory" in code |
| **External Executive Cortex** | Motivation / vision | Offload planning/working memory | Don't use in ADRs |

---

## Forbidden Terms (Generate ADR Violations)

| ❌ NEVER USE | Why | Use Instead |
|---|---|---|
| **Semantic Microkernel** | Not a canonical term | Application Core |
| **QAL Machine** | No academic/industry reference | N/A - remove from docs |
| **The Brain** | Vague metaphor | Application Core or Claude |
| **The Hands** | Vague metaphor | Automation Engine or n8n |
| **Script** | Too informal for architecture | Adapter, Tool, Workflow |
| **Plugin** | Conflicts with MCP terminology | MCP Server or Adapter |
| **AI Agent** | Overloaded term | Application Core or System |

---

## Migration Map (Old → New)

If you see these in old docs, update them:

| Old Term (Research Docs) | New Canonical Term | Notes |
|---|---|---|
| Semantic Microkernel | Application Core | Per ADR-001 |
| The Hands | Automation Engine (n8n) | Metaphor → Technical term |
| Truth Layer (when = storage) | Git Repository or Memory Bank | Clarify which |
| Observer Pattern | Monitor (MAPE-K) | Use MAPE-K terminology |
| Drift Detector | Observer + Analyzer (MAPE-K) | Two distinct components |

---

## Version History

- **1.0.0** (2025-12-04): Initial canonical terminology based on ADR-001

---

## Enforcement

**Pre-Commit:** (Future) Vale linter checks all `.md` files  
**Code Review:** PRs must reference canonical terms  
**ADR Requirement:** Any new term requires ADR justification

**Violation Severity:**
- Using forbidden term → ❌ **Block merge**
- Missing synonym → ⚠️ **Request clarification**
- New term without ADR → ❌ **Block merge**
