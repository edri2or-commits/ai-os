# Metaphor Usage Guide - AI Life OS

**Version:** 1.0.0  
**Authority:** ADR-001  
**Last Updated:** 2025-12-04

---

## Purpose

This guide explains **when and how to use** each metaphor for the AI Life OS.

**Critical Rule:**  
Metaphors are for **communication and explanation** - NOT for architectural decisions.  
For architecture → use `CANONICAL_TERMINOLOGY.md`

---

## The Three Metaphors

### 1. 🏛️ Hexagonal Architecture (Technical)

**Use when:**
- Writing code, specs, ADRs
- Explaining system structure to developers
- Making architectural decisions
- Documenting component relationships

**Core concepts:**
- Application Core (business logic)
- Ports (interfaces)
- Adapters (implementations)
- Dependency Inversion

**Example usage:**
> "The Observer implements the IChangeDetector port, acting as a Secondary Adapter that monitors the filesystem."

**Audience:** Technical (developers, architects, AI assistants)

---

### 2. 🧠 Cognitive Prosthetic (Human-Centric)

**Use when:**
- Explaining the system's purpose to non-technical users
- Discussing ADHD support and cognitive augmentation
- Describing user benefits
- Motivating design choices related to executive function

**Core concepts:**
- External Executive Function
- Working Memory offload
- Attention management
- Neuroplasticity and adaptation
- Extended Mind Hypothesis

**Example usage:**
> "The Memory Bank acts as your external working memory, storing context you don't need to hold in your head."

**Audience:** Users, stakeholders, yourself (when explaining "why")

---

### 3. 💻 LLM as Operating System (LLM-OS)

**Use when:**
- Explaining resource management (context = RAM)
- Discussing tool orchestration (MCP = drivers)
- Describing memory hierarchy (context → RAG → Git)
- Analyzing performance bottlenecks

**Core concepts:**
- Semantic Kernel (LLM)
- Context Window (RAM)
- Tools (Drivers/Peripherals)
- Vector DB (Virtual Memory/Swap)
- Git (Hard Drive)

**Example usage:**
> "Loading the entire research corpus into context would be like loading your entire hard drive into RAM - slow and wasteful. Instead, we use RAG as virtual memory."

**Audience:** Technical users familiar with OS concepts

---

## Decision Matrix: Which Metaphor to Use?

| Context | Best Metaphor | Why |
|---|---|---|
| Writing ADR | Hexagonal | Technical precision required |
| Code comments | Hexagonal | Developers need architecture terms |
| Explaining to friend | Cognitive Prosthetic | Human benefit focus |
| User documentation | Cognitive Prosthetic | Relatable, non-technical |
| Discussing context limits | LLM-OS | Resource management analogy |
| Performance optimization | LLM-OS | Helps reason about bottlenecks |
| Project pitch | Cognitive Prosthetic | Vision and purpose |
| Implementation spec | Hexagonal | Clear technical boundaries |

---

## ⚠️ Common Mistakes

### ❌ Mixing Metaphors in Technical Docs
```markdown
BAD: "The Semantic Kernel (brain) acts as the hexagonal core..."
```
**Problem:** Mixes OS metaphor ("kernel") with anatomy ("brain") and architecture ("hexagonal core")

```markdown
GOOD: "The Application Core coordinates Adapters via Ports."
```

### ❌ Using Metaphors Instead of Architecture Terms
```python
# BAD code comment
# The brain tells the hands to execute the workflow
workflow_executor.run()
```

```python
# GOOD code comment
# Core calls IWorkflowExecutor port via n8n adapter
workflow_executor.run()
```

### ❌ Technical Terms in User-Facing Docs
```markdown
BAD: "The system uses Hexagonal Architecture with Ports and Adapters to achieve Dependency Inversion."
```

```markdown
GOOD: "The system keeps your goals and logic separate from specific tools, so you can switch tools without relearning everything."
```

---

## 📖 Metaphor Cheat Sheet

### When Someone Asks...

**"What is this system?"**
→ Use **Cognitive Prosthetic**: "It's an external executive function layer that helps manage ADHD challenges by offloading working memory and planning."

**"How does it work?"**
→ Use **Hexagonal**: "The Core (Claude) makes decisions and coordinates external tools (n8n, Git) through standardized interfaces (MCP)."

**"Why is it slow sometimes?"**
→ Use **LLM-OS**: "The context window (RAM) is limited. When we load too much, it thrashes. We need to use RAG (virtual memory) for larger datasets."

**"Can I change from n8n to Zapier?"**
→ Use **Hexagonal**: "Yes! n8n is just an Adapter. We can swap it without touching the Core logic."

**"Why do I need to approve changes?"**
→ Use **Cognitive Prosthetic**: "Think of it like a prosthetic limb - you're still in control. The prosthetic extends your reach but you decide where to reach."

---

## Forbidden Hybrid Terms

These mix metaphors and create confusion:

| ❌ DO NOT USE | Why | Use Instead |
|---|---|---|
| Semantic Microkernel | Mixes OS + vague "semantic" | Application Core |
| Brain Port | Mixes anatomy + architecture | Primary Port |
| Memory Adapter | Ambiguous (RAM? Storage? Human?) | Git Adapter or Memory Bank |
| Cognitive Driver | Mixes psychology + OS | Adapter |
| Executive Function Port | Mixes psychology + architecture | Port (specify which) |

---

## Evolution Guidelines

### Adding a New Metaphor

If you discover a new useful metaphor:

1. **Create ADR** proposing it
2. **Define scope**: Technical/Human-centric/Resource-focused
3. **Identify overlaps** with existing metaphors
4. **Provide examples** of when to use vs not use
5. **Update this guide**

### Deprecating a Metaphor

If a metaphor becomes confusing:

1. **Create ADR** proposing deprecation
2. **Document migration** (which terms to use instead)
3. **Update all docs** systematically
4. **Add to Forbidden Terms** in CANONICAL_TERMINOLOGY.md

---

## References

- Cockburn, A. (2005). *Hexagonal Architecture* - Source of technical architecture
- Clark, A., & Chalmers, D. (1998). *The Extended Mind* - Source of Cognitive Prosthetic concept
- Karpathy, A. (2023). *LLM OS* - Source of Operating System metaphor

---

**Quick Navigation:**
- Technical terms → `CANONICAL_TERMINOLOGY.md`
- Architecture details → `ARCHITECTURE_REFERENCE.md`
- Decisions → `docs/decisions/ADR-001-architectural-alignment.md`
