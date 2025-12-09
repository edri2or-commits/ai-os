# ADR-001: Architectural Alignment and Canonical Reference Model

**Status:** ✅ Accepted  
**Date:** 2025-12-04  
**Authors:** Or (with Claude as research assistant)  
**Supersedes:** N/A  
**Research Sources:** 
- GPT Deep Research Report (2025-12-04)
- Claude Web Research (Microkernel, Hexagonal, MAPE-K, Cognitive Architecture)

---

## Context

The AI Life OS project uses multiple architectural patterns and metaphors (Microkernel, Hexagonal, Cognitive, OS metaphors) across research documents. This creates **terminology confusion** and **architectural drift risk**:

1. **Multiple competing metaphors:** "Semantic Microkernel" vs "Hexagonal Core" vs "Cognitive Prosthetic"
2. **Inconsistent terms:** Same concept called different names in different docs
3. **No enforcement:** Nothing prevents mixing patterns or inventing new terms
4. **Solo developer challenge:** No team consensus to maintain consistency

Without a single canonical reference, the system will drift into a "Big Ball of Mud."

---

## Decision

We adopt **Hexagonal Architecture (Ports & Adapters)** as the PRIMARY reference architecture, with **MAPE-K Control Loop** as a secondary pattern for autonomic behavior.

### Primary: Hexagonal Architecture (Ports & Adapters)

**Source:** Alistair Cockburn (2005) - [Original Article](https://alistair.cockburn.us/hexagonal-architecture/)

**Core Components:**
- **Application Core:** Business logic + LLM reasoning (Claude + System Prompts)
- **Ports:** Abstract interfaces defining contracts (MCP protocol definitions)
- **Adapters:** Concrete implementations (MCP servers: filesystem, git, n8n)

**Official Terminology:**
- Core / Application / Hexagon (synonyms)
- Primary Port (driving side) / Secondary Port (driven side)
- Primary Adapter / Secondary Adapter
- Alternative terms accepted: Inbound/Outbound, Driving/Driven

**Key Principle:**  
Dependencies point INWARD. The Core never depends on specific technologies. All external integrations happen through Ports, implemented by swappable Adapters.

### Secondary: MAPE-K Control Loop (for Observer/Reconciler)

**Source:** IBM Autonomic Computing (2001) - [Wikipedia](https://en.wikipedia.org/wiki/Autonomic_computing)

**Components:**
- **Monitor:** Observer - detects drift (Life Graph, Git, Email)
- **Analyze:** Classifies changes, determines severity
- **Plan:** Reconciler - generates Change Requests (YAML)
- **Execute:** Executor - applies approved changes
- **Knowledge:** Truth Layer (Git + Memory Bank + schemas)

**Integration:**  
MAPE-K operates WITHIN the Hexagonal Architecture. The Observer/Reconciler/Executor are Adapters that implement specific Ports (IChangeDetector, IChangeExecutor).

---

## Consequences

### Positive ✅

1. **Single Source of Truth:** All architectural decisions reference Hexagonal + MAPE-K
2. **Swappable Components:** Can replace n8n/Claude/Git without rewriting Core
3. **Clear Boundaries:** Core logic isolated from infrastructure
4. **Professional Terminology:** Uses established, recognized patterns
5. **Testability:** Can mock Adapters to test Core in isolation
6. **Documented Precedent:** Hexagonal used by Netflix, AWS, enterprise systems

### Negative ⚠️

1. **Learning Curve:** Team (just Or) must learn Hexagonal terminology
2. **Initial Overhead:** Requires discipline to maintain boundaries
3. **Complexity:** More structure than a simple "script collection"

### Neutral ℹ️

1. **Rejects "Semantic Microkernel":** Not a canonical term, creates confusion
2. **Rejects "QAL Machine":** No established academic/industry reference
3. **Metaphors remain valid:** "Cognitive Prosthetic" and "LLM-OS" are metaphors for communication, not architectural patterns

---

## Alternatives Considered

### Option A: Layered Architecture
**Rejected because:** Tight coupling between layers. Changing database requires rewriting business logic.

### Option B: "Semantic Microkernel" as primary
**Rejected because:** Not a recognized term in software engineering. Mixes metaphor with architecture.

### Option C: Event-Driven Architecture
**Rejected because:** While relevant for async workflows, it doesn't provide the modularity and testability of Hexagonal.

---

## Compliance Requirements

All future architectural work MUST:

1. **Use canonical terminology** from CANONICAL_TERMINOLOGY.md
2. **Reference this ADR** when making design decisions
3. **Create new ADR** if deviating from Hexagonal/MAPE-K patterns
4. **Justify deviations** with concrete trade-off analysis

---

## Related Documents

- `CANONICAL_TERMINOLOGY.md` - Official terms dictionary
- `ARCHITECTURE_REFERENCE.md` - Detailed pattern descriptions
- `METAPHOR_GUIDE.md` - When to use which metaphor

---

## References

1. Cockburn, A. (2005). *Hexagonal Architecture*. Retrieved from https://alistair.cockburn.us/hexagonal-architecture/
2. Kephart, J. O., & Chess, D. M. (2003). *The vision of autonomic computing*. Computer, 36(1), 41-50.
3. Netflix Tech Blog. (2020). *Ready for changes with Hexagonal Architecture*. 
4. AWS Prescriptive Guidance. *Hexagonal architecture pattern*.
5. Wikipedia. (2025). *Autonomic Computing*.
