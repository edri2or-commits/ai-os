# CHAT1_STABILIZATION_PLAN.md — Phase 2.3

## 📅 Date: 2025-11-25
**Owner:** GPT Operator (under Or’s supervision)

---

## 🎯 Objective
Ensure that **Chat1 (Telegram bot)** becomes a stable, always‑on, human‑in‑the‑loop communication interface between Or and the AI‑OS ecosystem.

---

## 🧩 Scope
Covers the following components:
- `chat/telegram_bot.py`
- `start_chat1.py`
- ngrok / webhook configuration
- Environment variables (`TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`)
- Integration with Control Plane and Event Timeline

---

## 🏗️ Stabilization Goals
| Goal | Description | Status |
|------|--------------|---------|
| 1 | Ensure persistent Chat1 service via Google Cloud Run | 🔜 Planned |
| 2 | Fix webhook stability (avoid URL resets) | 🚧 In Progress |
| 3 | Document Chat1 environment setup in `docs/chat1/ENV_SETUP.md` | 🔜 Next |
| 4 | Add `chat1_status` to Control Plane | ✅ Done |
| 5 | Log user intents and actions to `EVENT_TIMELINE.md` | 🔜 Next |

---

## ⚙️ Architecture Overview
```
User (Or) → Telegram → Chat1 Bot → Agent Gateway (ai_core/agent_gateway.py)
                                   ↓
                            GPT Operator (Planner)
                                   ↓
                          Claude / Make / Google Clients
```

---

## 🧾 Stabilization Tasks

### Phase 2.3.1 — Webhook Reliability
- Use **static ngrok domain** or **Cloud Run URL**.
- Update bot startup script (`start_chat1.py`) to auto‑refresh webhook if expired.
- Log all webhook events to `logs/chat1_webhook.log`.

### Phase 2.3.2 — Persistent Service Deployment
- Containerize Chat1 (Dockerfile.chat1).
- Deploy to Cloud Run with auto‑restart.
- Add health endpoint `/healthz` to verify uptime.

### Phase 2.3.3 — Documentation & Control Plane Integration
- Create `docs/chat1/ENV_SETUP.md`.
- Update Control Plane `chat1_status` dynamically from runtime logs.
- Add Chat1 startup confirmation message in Telegram UI.

### Phase 2.3.4 — Timeline Logging
- Every intent → append JSON line to `EVENT_TIMELINE.jsonl`.
- Include: timestamp, actor, message, approved, executed_by.

---

## 🔮 Deliverables
1. Stable Chat1 service reachable 24/7.
2. Environment docs + setup script.
3. Logged interactions in Timeline.
4. Control Plane reflecting Chat1’s real status.

---

## 🧠 Notes
- No automation is executed without explicit approval from Or.
- Keep human‑in‑the‑loop at every stage.
- Use Phase 2 principles: DRY, SSOT, Transparency.

---

**Phase:** 2.3 – Chat1 Stabilization  
**Next Phases:** 2.4 Make Integration → 2.5 Consolidation → 3 Google Stabilization  
**Mode:** INFRA_ONLY  

> “When the voice is stable, the system becomes human again.”