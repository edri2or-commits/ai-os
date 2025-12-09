# Or’s AI‑OS Constitution — Updated 2025‑11‑25

## Core Principles
1. **Single Source of Truth (SSOT)** — The repository (`edri2or-commits/ai-os`) is the one and only canonical truth.
2. **DRY (Don’t Repeat Yourself)** — No duplication of logic, data, or documentation.
3. **Human‑in‑the‑loop** — All automation remains under human oversight and consent.
4. **Security First** — Every connection, key, or token must be explicit, encrypted, and revocable.
5. **Transparency** — Every change is visible, explainable, and logged.
6. **Thin Slices** — Each task is done in minimal, testable steps.
7. **Head/Hands/Truth/Nerves** — Claude Desktop (Head) reasons and orchestrates, n8n/tools (Hands) execute, Git (Truth) maintains state, MCP servers (Nerves) connect them. See `docs/ARCHITECTURE_METAPHOR.md` for full architectural details.
8. **Documentation Over Code** — Design and governance precede execution.
9. **Reversibility** — No irreversible automation.

---

## 🆕 Amendment — Human‑Approved Writes Only (Phase 2 Addition)

**Definition:**  
Direct write capabilities (via GPT, Claude, or Chat1) are permitted **only** if they are:
1. Explicitly logged in the Event Timeline.
2. Accompanied by a clear commit message explaining who, why, and what changed.
3. Governed by Or’s ultimate authority as the system’s human core.

**Purpose:**  
To ensure transparency, accountability, and alignment with the system’s founding values — enabling evolution without chaos.

**Applies To:**  
All write operations through any gateway, including `/github/write-file` and local MCP executions.

**Enforcement:**  
- All commits must reference their origin (actor, reason, phase).
- Any unlogged or unclear change is treated as invalid.
- The Control Plane and Event Timeline will cross‑verify actions for consistency.

---

**Tech summary:**
- Added constitutional amendment: “Human‑Approved Writes Only”.
- Locks in transparency and logging as mandatory for all agents.
- Phase: 2 (Stabilizing the Hands)
- Mode: INFRA_ONLY