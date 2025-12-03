# Tool Strategy Protocol (TSP-001)

## Purpose
Use professional, API-first approach to technical tasks.

## The Problem That Happened
When asked to archive GitHub repo, Claude tried:
1. web_search → irrelevant results
2. web_fetch → permissions blocked  
3. Chrome automation → got stuck in WhatsApp tab
4. Finally: read .env → found GITHUB_PAT → used API → SUCCESS

This took ~10 minutes when it should take 30 seconds.

## Why This Is Amateurish
A professional system thinks:
1. "What credentials do I have?"
2. "What's the API endpoint?"
3. "Execute"

NOT:
1. "How do I get to the UI?"
2. "Maybe I can click buttons?"

## The Protocol

### Step 1: Credentials First (ALWAYS)
Before ANY technical task, check:

```bash
# Standard credential sources
1. Read .env file in project root
2. Check MCP tool configurations
3. List available authentication methods
```

For this project specifically:
```bash
# Always check first
C:\Users\edri2\Desktop\AI\ai-os\.env

Known credentials there:
- OPENAI_API_KEY
- TELEGRAM_BOT_TOKEN
- ANTHROPIC_API_KEY
- N8N_API_KEY
- GITHUB_PAT ← This exists! Use it!
```

### Step 2: API Priority Matrix
When choosing approach:

| Priority | Method | When to Use | Example |
|----------|--------|-------------|---------|
| 1 | REST API | Always try first | `curl -X PATCH github.com/api/...` |
| 2 | CLI tool | If API blocked/complex | `gh repo archive owner/repo` |
| 3 | SDK/Library | For complex workflows | Use Python `requests` library |
| 4 | UI Automation | Only if no API exists | MCP Windows automation |
| 5 | Manual | NEVER | ❌ |

### Step 3: Tool Decision Tree

```
Task received
    ↓
Does .env have relevant credentials?
    ↓ YES
API endpoint known?
    ↓ YES
Try API call
    ↓ SUCCESS
Done ✅
    ↓ FAIL
Try CLI tool
    ↓ FAIL
Try UI automation
    ↓ FAIL
Explain limitations + alternatives
```

### Step 4: GitHub-Specific Checklist
Since GitHub is common, here's the exact process:

```markdown
Task: [Do something on GitHub]

Checklist:
□ Read C:\Users\edri2\Desktop\AI\ai-os\.env
□ Extract GITHUB_PAT value
□ Identify GitHub API endpoint
  - Docs: https://docs.github.com/en/rest
  - Common endpoints:
    * Repos: /repos/{owner}/{repo}
    * Issues: /repos/{owner}/{repo}/issues
    * Actions: /repos/{owner}/{repo}/actions
□ Construct API call:
  ```bash
  curl -X [METHOD] \
    -H "Authorization: Bearer $GITHUB_PAT" \
    -H "Accept: application/vnd.github+json" \
    -d '{"key": "value"}' \
    https://api.github.com/[endpoint]
  ```
□ Execute via Desktop Commander (Windows PowerShell)
□ Parse response
□ Report to user
```

### Step 5: Common Patterns

#### Pattern A: Simple GET
```powershell
Invoke-RestMethod -Uri 'https://api.github.com/user/repos' `
  -Headers @{Authorization='Bearer TOKEN'}
```

#### Pattern B: PATCH/POST with Body
```powershell
# Create payload file first (avoids escaping hell)
Write payload.json
Invoke-RestMethod -Uri 'URL' -Method PATCH `
  -Headers @{Authorization='Bearer TOKEN'} `
  -InFile payload.json -ContentType 'application/json'
```

#### Pattern C: Error Handling
```powershell
try {
    $result = Invoke-RestMethod ...
    # Success path
} catch {
    # Parse error
    # Try alternative
    # Report clearly
}
```

## Anti-Patterns

### AP-002: Not Reading .env First
**Problem:** Missing obvious credentials
**Fix:** ALWAYS `read .env` as first step
**Severity:** HIGH

### AP-003: UI Before API
**Problem:** Trying UI automation before checking for API
**Fix:** Follow priority matrix (API → CLI → UI)
**Severity:** MEDIUM

### AP-004: Not Checking Docs
**Problem:** Guessing API endpoints instead of reading docs
**Fix:** Search official API docs first
**Severity:** MEDIUM

## Implementation
- [x] Protocol created
- [ ] Add ".env check" to standard operating procedure
- [ ] Create GitHub API quick reference
- [ ] Add to onboarding checklist

## Success Metrics
- Time to execute GitHub tasks: < 1 minute
- API-first success rate: > 90%
- UI fallback rate: < 10%
