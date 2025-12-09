# Email Watcher - Production Grade Gmail Automation

## 🎯 Overview

Automated Gmail monitoring system that:
- Searches for unread emails every 15 minutes
- Classifies them with Claude Sonnet 4.5
- Generates drift reports for Observer/Reconciler
- Logs structured JSONL for observability

## 🏗️ Architecture

```
Email Watcher (Python)
  ├─ Google OAuth (reuses MCP tokens)
  ├─ Gmail API (unread search)
  ├─ Claude API (classification)
  ├─ YAML drift reports (Observer compatible)
  └─ JSONL logs (MCP Logger compatible)
```

## ✅ Prerequisites

1. **Google MCP configured** (OAuth tokens at `~/.google-mcp-tokens.json`)
2. **Anthropic API key** (in `.env` as `ANTHROPIC_API_KEY`)
3. **Python 3.11+** with packages:
   - requests
   - python-dotenv
   - pyyaml
   - pytest (for tests)

## 📦 Installation

### Step 1: Verify Prerequisites

```bash
# Check Google MCP tokens exist
ls ~/.google-mcp-tokens.json

# Check Anthropic API key in .env
cat .env | grep ANTHROPIC_API_KEY

# Install Python packages
pip install requests python-dotenv pyyaml pytest
```

### Step 2: Test Manually

```bash
# Dry run (preview without saving)
python tools/email_watcher.py --dry-run --verbose

# Real run
python tools/email_watcher.py --verbose
```

### Step 3: Schedule with Task Scheduler

```bash
# Import task (run as Administrator)
schtasks /Create /TN "AI-OS\Email Watcher" /XML "tools\email_watcher_task.xml" /F

# Verify task created
schtasks /Query /TN "AI-OS\Email Watcher"

# Run manually to test
schtasks /Run /TN "AI-OS\Email Watcher"
```

## 📊 Output

### Drift Reports
Location: `memory-bank/drift/email-drift-YYYY-MM-DD-HHMMSS.yaml`

Format:
```yaml
timestamp: "2025-12-03T12:00:00+00:00"
type: email_drift
unread_count: 5
classified_count: 5
classified_emails:
  - id: "msg_001"
    from: "bank@example.com"
    subject: "Your statement"
    category: bureaucracy
    priority: medium
    action_needed: true
    suggested_action: "Review bank statement"
```

### Logs
Location: `logs/email_watcher.jsonl`

Format (one JSON per line):
```json
{"timestamp": "2025-12-03T12:00:00Z", "event_type": "start", "message": "Email Watcher starting", "metadata": {}}
{"timestamp": "2025-12-03T12:00:01Z", "event_type": "info", "message": "Found 5 unread emails", "metadata": {}}
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/test_email_watcher.py -v

# Run with coverage
pytest tests/test_email_watcher.py --cov=tools.email_watcher

# Run integration tests (requires real credentials)
pytest tests/test_email_watcher.py -m integration
```

## 🔧 Configuration

Edit `.env`:
```bash
ANTHROPIC_API_KEY=sk-ant-api03-...
```

Edit Task Scheduler settings:
```bash
# Open Task Scheduler GUI
taskschd.msc

# Navigate to: Task Scheduler Library > AI-OS > Email Watcher
# Right-click > Properties
# Adjust: Triggers, Actions, Conditions
```

## 📈 Monitoring

### Check logs
```bash
# View recent logs
tail -20 logs/email_watcher.jsonl

# Count errors
grep '"event_type": "error"' logs/email_watcher.jsonl | wc -l
```

### Check drift reports
```bash
# List recent reports
ls -lt memory-bank/drift/email-drift-*.yaml | head -5

# View latest report
cat memory-bank/drift/email-drift-*.yaml | tail -1
```

### Task Scheduler status
```bash
# Check last run time
schtasks /Query /TN "AI-OS\Email Watcher" /V /FO LIST

# View task history
# Open Event Viewer > Task Scheduler > History
```

## 🐛 Troubleshooting

### "Google MCP tokens not found"
**Solution:** Run Google MCP OAuth flow first:
```bash
# In Claude Desktop, trigger any Google tool
# This will create ~/.google-mcp-tokens.json
```

### "Claude API failed: 401"
**Solution:** Check API key in `.env`:
```bash
# Test API key
python tools/test_anthropic_key.py
```

### "No unread emails found"
**Solution:** This is normal! Task will exit gracefully.

### Task not running
**Solution:** Check Task Scheduler:
```bash
# Verify task enabled
schtasks /Query /TN "AI-OS\Email Watcher"

# Check last result (0 = success)
# Open taskschd.msc > AI-OS > Email Watcher > History
```

## 🔗 Integration

### Observer
Observer will detect drift reports automatically (every 15 minutes):
```bash
# Observer finds: memory-bank/drift/email-drift-*.yaml
# Observer generates: Drift Detection report
```

### Reconciler
Reconciler converts drift to Change Requests:
```bash
# Reconciler reads drift report
# Reconciler proposes: "Mark emails as processed"
# User approves via HITL
```

## 📝 Development

### Add new classification categories
Edit `tools/email_watcher.py`:
```python
prompt = """Classify into: bureaucracy/personal/work/shopping/news"""
```

### Change run frequency
Edit `tools/email_watcher_task.xml`:
```xml
<Interval>PT30M</Interval>  <!-- 30 minutes -->
```

### Add Telegram notifications
Create new file: `tools/email_notifier.py`
Integrate with existing `chat/telegram_bot.py`

## 📚 References

- Observer: `tools/observer.py`
- Watchdog: `tools/watchdog.py`
- MCP Logger: `tools/mcp_logger.py`
- Playbook: `claude-project/ai-life-os-claude-project-playbook.md`
