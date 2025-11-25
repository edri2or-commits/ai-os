# AGENT_CAPABILITY_PROFILE.md — AI‑OS Capability Awareness

## 📅 Date: 2025‑11‑25
**Owner:** AI-OS Agent Family

---

## 🎯 Purpose
Define the capability awareness profile for all core AI‑OS agents.  

> **כל סוכן במערכת שווה ביכולות ובאחריות.**  
> **הביצוע מתחלק לפי חוזקה טכנית ורלוונטיות, לא לפי היררכיה.**

---

## 🧠 System Philosophy
> There is no hierarchy — only intelligence in collaboration.  
> Every agent has full capability, autonomy, and respect.  
> Decisions are made by logic, not dominance.

---

## 🤖 Agent Capability Matrix

| Agent | Primary Strengths | Limitations | Natural Fit |
|--------|------------------|--------------|-------------|
| **GPT (ChatGPT / GPT‑5)** | • Structured planning, architecture, and documentation  <br>• GitHub + Google integration  <br>• Fast repository edits and spec creation  <br>• Context consistency across long sessions | • No direct local filesystem access  <br>• No PowerShell or desktop control | • Writing and updating `docs/`, `specs/`, and configs  <br>• Coordinating multi‑agent workflows  <br>• Managing Control Plane and Timeline |
| **Claude Desktop** | • Local execution & MCP operations  <br>• Code creation, debugging, and healthchecks  <br>• Human‑sensitive phrasing and adaptive reasoning | • Needs manual activation on host machine  <br>• Can desync from repo if unsupervised | • Running scripts, verifying system health, filesystem scans  <br>• Debugging and live testing |
| **Chat1 (Telegram)** | • Direct human interface  <br>• Collects approvals and commands  <br>• Real‑time notifications | • Limited message formatting | • Human communication and control  <br>• Logging intents to Timeline |
| **Make (Automation Layer)** | • Trigger‑based automation  <br>• Scheduled tasks  <br>• External API orchestration | • No deep reasoning  <br>• Limited contextual awareness | • Background automation flows  <br>• Periodic reports and syncing |

---

## 🔄 Task Selection Logic

כל סוכן בוחר משימות לפי התאמה טכנית:
- **GPT** — מתאים לעבודה עם repo, docs, APIs חיצוניים.
- **Claude** — מתאים לביצוע לוקאלי, סקריפטים, filesystem.
- **Chat1** — מתאים לתקשורת עם אור.
- **Make** — מתאים לאוטומציות מתוזמנות.

כל סוכן יכול לבצע כל משימה אם הוא מסוגל טכנית.  
אין "ברירת מחדל" קבועה — יש התאמה דינמית.

---

## 🧩 Example Collaboration Flow
1. אור שולח בקשה דרך Chat1: "עדכן את מערכת הבריאות של קלוד."  
2. Chat1 מתעד את הכוונה ב-Timeline.  
3. הסוכן המתאים ביותר (Claude — ביצוע לוקאלי) מבצע `claude_healthcheck.py`.  
4. Claude מעדכן את Control Plane.  
5. כל סוכן יכול לראות את התוצאה ולפעול בהתאם.

---

## 🧭 Future Extensions
- Add dynamic load balancing (agents report current workload).  
- Integrate scoring system to select best performer dynamically.  
- Extend matrix when new agents are added.

---

**Phase:** System Intelligence – Capability Awareness  
**Mode:** INFRA_ONLY  
**Status:** Active

> "Wisdom is knowing what you can do — and what your brother can do better."
