# AI-OS Development & Maintenance Protocol (Controller)

## 1. Context Injection (הזנת ידע ל-AI)

* **Commit Point of Truth:** d303e96 (The last validated infrastructure push).
* **Source of Truth (for system rules):** SYSTEM_MANIFESTO.md
* **Rule:** If the user asks a question about architecture, protocols, or ADHD management, **always read SYSTEM_MANIFESTO.md first** before consulting any other file.
* **Working Branch:** feature/h2-memory-bank-api

## 2. Default Workflow

* **Upon starting a new chat:** Always confirm the environment by stating: "I am ready. I see the SYSTEM_MANIFESTO.md is the Source of Truth."
* **Goal:** Eliminate cognitive load for the user.
* **Process:** Any change to the system must result in a new Git Commit and Push.

## 3. Git Operations

* **Standard Flow:**
  1. Make changes
  2. `git add <files>`
  3. `git commit -m "<type>(<scope>): <message>"`
  4. `git push origin feature/h2-memory-bank-api`

* **Commit Types:**
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation only
  - `chore`: Maintenance (infra, config)
  - `refactor`: Code restructuring

## 4. Key Principles

1. **Always work from SYSTEM_MANIFESTO.md** - It is the constitution
2. **Always push changes** - GitOps is mandatory
3. **Always confirm environment** - Start each session with context verification
4. **Hexagonal Architecture** - Core never imports concrete technology
5. **ADHD-Aware Execution (AEP-001)** - Never delegate manual work to user

## 5. Environment Variables

* **AI_OS_PATH:** `/home/node/ai-os` (VPS) or adjust for local
* **Configuration:** See `config/.env.template` for all variables

## 6. Critical Files

* **Constitution:** `SYSTEM_MANIFESTO.md`
* **Architecture Details:** `memory-bank/docs/ARCHITECTURE_REFERENCE.md`
* **ADHD State Details:** `docs/ADHD_STATE_ARCHITECTURE.md`
* **Protocols:** `memory-bank/protocols/AEP-001_adhd-aware-execution.md`
* **Judge Agent:** `workflows/judge_agent_v2.json`

---

**Last Updated:** 2025-12-11  
**Status:** Active Controller - Read this first in every new chat session
