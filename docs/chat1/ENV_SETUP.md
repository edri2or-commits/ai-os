# ENV_SETUP.md — Chat1 Environment Configuration

## 📅 Date: 2025-11-25
**Owner:** GPT Operator (under Or’s supervision)

---

## 🎯 Purpose
Define a clear, reproducible setup for **Chat1 (Telegram bot)** to ensure stable runtime and connectivity across reboots or deployments.

---

## 🧩 Required Environment Variables
| Variable | Description | Example |
|-----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Telegram bot API token | `123456789:ABC-xyz` |
| `OPENAI_API_KEY` | Key for GPT actions | `sk-...` |
| `CHAT1_WEBHOOK_URL` | Public HTTPS endpoint (ngrok / Cloud Run) | `https://chat1.aios.app/webhook` |
| `AIOS_ENV` | Environment mode | `production` / `sandbox` |
| `CONTROL_PLANE_PATH` | Path to `docs/CONTROL_PLANE_SPEC.md` | `docs/CONTROL_PLANE_SPEC.md` |

---

## ⚙️ Setup Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/edri2or-commits/ai-os.git
   cd ai-os
   ```

2. Create `.env.local` file:
   ```bash
   TELEGRAM_BOT_TOKEN=123456789:ABC-xyz
   OPENAI_API_KEY=sk-...
   CHAT1_WEBHOOK_URL=https://chat1.aios.app/webhook
   AIOS_ENV=production
   CONTROL_PLANE_PATH=docs/CONTROL_PLANE_SPEC.md
   ```

3. Run the Chat1 service:
   ```bash
   python start_chat1.py
   ```

4. Verify webhook:
   ```bash
   curl -X GET https://chat1.aios.app/healthz
   ```

---

## 🩺 Healthcheck
- Chat1 should respond with `{ "status": "ok" }` when `/healthz` is hit.
- Failures are logged to `logs/chat1_health.log`.
- GPT Operator updates `chat1_status` in the Control Plane accordingly.

---

## 🧠 Notes
- Webhook URL must be HTTPS and static.
- Never commit `.env.local` to GitHub.
- Use `AIOS_ENV=sandbox` for testing modes.

---

**Phase:** 2.3 – Chat1 Stabilization  
**Next Phases:** 2.4 Make Integration → 2.5 Consolidation → 3 Google Stabilization  
**Mode:** INFRA_ONLY  

> “When environment is clear, communication becomes truth.”