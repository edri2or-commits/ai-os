# AGENT_CAPABILITY_PROFILE.md — AI‑OS Capability Awareness

## 📅 Date: 2025‑11‑25
**Owner:** GPT Operator (under Or’s supervision)

---

## 🎯 Purpose
Define the capability awareness profile for all core AI‑OS agents.  
This document ensures that every agent (GPT, Claude, Chat1, Make) knows its own strengths and weaknesses, understands others’, and can choose the optimal executor for each task.

---

## 🧠 System Philosophy
> There is no hierarchy — only intelligence in collaboration.  
> Every agent has full capability, autonomy, and respect.  
> Decisions are made by logic, not dominance.

---

## 🤖 Agent Capability Matrix
| Agent | Primary Strengths | Limitations | Preferred Use Cases | Delegation Logic |
|--------|------------------|--------------|----------------------|------------------|
| **GPT (ChatGPT / GPT‑5)** | • Structured planning, architecture, and documentation  <br>• GitHub + Google integration  <br>• Fast repository edits and spec creation  <br>• Context consistency across long sessions | • No direct local filesystem access  <br>• No PowerShell or desktop control | • Writing and updating `docs/`, `specs/`, and configs  <br>• Coordinating multi‑agent workflows  <br>• Managing Control Plane and Timeline | If task = `repo`, `docs`, or `workflow logic` → GPT executes.  <br>If task = `local execution` → delegate to Claude. |
| **Claude Desktop** | • Local execution & MCP operations  <br>• Code creation, debugging, and healthchecks  <br>• Human‑sensitive phrasing and adaptive reasoning | • Needs manual activation on host machine  <br>• Can desync from repo if unsupervised | • Running scripts, verifying system health, filesystem scans  <br>• Debugging and live testing | If task = `repo sync` or `healthcheck` → Claude executes.  <br>If task = `documentation` → delegate to GPT. |
| **Chat1 (Telegram)** | • Direct human interface  <br>• Collects approvals and commands  <br>• Real‑time notifications | • No execution power  <br>• Limited message formatting | • Human communication and control  <br>• Logging intents to Timeline | If task = `user interaction` → Chat1 executes.  <br>If task = `action execution` → delegate to GPT or Claude. |
| **Make (Automation Layer)** | • Trigger‑based automation  <br>• Scheduled tasks  <br>• External API orchestration | • No deep reasoning  <br>• Limited contextual awareness | • Background automation flows  <br>• Periodic reports and syncing | If task = `scheduled` or `triggered` → Make executes. |

---

## 🔄 Decision Priority Map
1. **GPT** → default for repo & docs.  
2. **Claude** → default for execution & local access.  
3. **Chat1** → default for human communication.  
4. **Make** → default for automations.

Agents must always check this file before delegating tasks.  
Each session init loads this map into memory (see `SESSION_INIT_CHECKLIST.md`, Step 2.6).

---

## 🧩 Example Delegation Flow
1. User sends request via Chat1 → “עדכן את מערכת הבריאות של קלוד.”  
2. Chat1 logs intent → passes to GPT.  
3. GPT determines that task = `healthcheck`.  
4. GPT delegates to Claude.  
5. Claude executes `claude_healthcheck.py` → updates Control Plane.  
6. GPT logs result to Timeline.

---

## 🧭 Future Extensions
- Add dynamic load balancing (agents report current workload).  
- Integrate scoring system to select best performer dynamically.  
- Extend matrix when new agents are added.

---

**Phase:** System Intelligence – Capability Awareness  
**Mode:** INFRA_ONLY  
**Status:** Active

> “Wisdom is knowing what you can do — and what your brother can do better.”