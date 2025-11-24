# Google Workspace Client

HTTP service for Google Workspace operations via GPT Custom Actions.

---

## 📋 Overview

| Property | Value |
|----------|-------|
| **Port** | 8082 |
| **Auth** | OAuth 2.0 (edri2or@gmail.com) |
| **Status** | ✅ Operational |
| **Last Tested** | 2025-11-24 |

---

## 🚀 Quick Start

### Option 1: Use the All-in-One Script
```powershell
# From project root
.\start-all-services.bat
```

### Option 2: Manual Start
```powershell
cd C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace
python -m uvicorn services.google_workspace_client.main:app --port 8082 --reload
```

### Option 3: With ngrok (for GPT access)
```powershell
# Terminal 1: Start service
python -m uvicorn services.google_workspace_client.main:app --port 8082 --reload

# Terminal 2: Start ngrok tunnel
ngrok http 8082
```

---

## 📡 API Endpoints

All endpoints use POST and return `{ok: true/false, ...}` responses.

### Gmail (`/google/gmail`)

| Endpoint | Description | Request Body |
|----------|-------------|--------------|
| `/google/gmail/send` | Send email | `{to: [], subject, body, cc?, bcc?, is_html?}` |
| `/google/gmail/list` | List emails | `{max_results?, query?}` |

### Calendar (`/google/calendar`)

| Endpoint | Description | Request Body |
|----------|-------------|--------------|
| `/google/calendar/create-event` | Create event | `{summary, start_time, end_time, description?, location?, attendees?}` |
| `/google/calendar/list-events` | List events | `{max_results?, time_min?, time_max?}` |

### Drive (`/google/drive`)

| Endpoint | Description | Request Body |
|----------|-------------|--------------|
| `/google/drive/search` | Search files | `{query, max_results?}` |

### Sheets (`/google/sheets`)

| Endpoint | Description | Request Body |
|----------|-------------|--------------|
| `/google/sheets/create` | Create spreadsheet | `{title}` |
| `/google/sheets/read` | Read data | `{spreadsheet_id, range?}` |

### Docs (`/google/docs`)

| Endpoint | Description | Request Body |
|----------|-------------|--------------|
| `/google/docs/create` | Create document | `{title}` |

### Tasks (`/google/tasks`)

| Endpoint | Description | Request Body |
|----------|-------------|--------------|
| `/google/tasks/create` | Create task | `{title, notes?, due?}` |

---

## 🔐 Authentication

### OAuth 2.0 Setup

The service uses OAuth 2.0 with the following files:

| File | Description | Location |
|------|-------------|----------|
| `credentials.json` | OAuth client config | Project root |
| `token.json` | Saved auth token | Project root |

### Required Scopes
- `https://www.googleapis.com/auth/gmail.modify`
- `https://www.googleapis.com/auth/calendar`
- `https://www.googleapis.com/auth/drive`
- `https://www.googleapis.com/auth/spreadsheets`
- `https://www.googleapis.com/auth/documents`
- `https://www.googleapis.com/auth/tasks`

### Re-authenticate (if token expires)
```powershell
python -m services.google_workspace_client.auth
```

---

## 🤖 GPT Integration

### OpenAPI Schema

```yaml
openapi: 3.1.0
info:
  title: Google Workspace
  version: 1.0.0
servers:
  - url: https://YOUR-NGROK-URL.ngrok-free.dev

paths:
  /google/gmail/send:
    post:
      operationId: sendEmail
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                to:
                  type: array
                  items:
                    type: string
                subject:
                  type: string
                body:
                  type: string
      responses:
        '200':
          description: OK

  /google/calendar/create-event:
    post:
      operationId: createCalendarEvent
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                summary:
                  type: string
                start_time:
                  type: string
                end_time:
                  type: string
      responses:
        '200':
          description: OK

  /google/drive/search:
    post:
      operationId: searchDrive
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
      responses:
        '200':
          description: OK

  /google/sheets/create:
    post:
      operationId: createSpreadsheet
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
      responses:
        '200':
          description: OK

  /google/docs/create:
    post:
      operationId: createDocument
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                title:
                  type: string
      responses:
        '200':
          description: OK
```

### GPT Configuration
1. Go to: https://chatgpt.com/gpts/editor
2. Create new Action
3. Paste the OpenAPI schema above
4. Replace `YOUR-NGROK-URL` with actual ngrok URL
5. Set Authentication: None
6. Save

---

## 📁 File Structure

```
services/google_workspace_client/
├── main.py                 # FastAPI app entry point
├── config.py              # Settings and configuration
├── requirements.txt       # Python dependencies
├── auth.py               # OAuth authentication script
├── README.md             # This file
├── api/
│   ├── routes_gmail.py      # Gmail endpoints
│   ├── routes_calendar.py   # Calendar endpoints
│   ├── routes_drive.py      # Drive endpoints
│   ├── routes_sheets.py     # Sheets endpoints
│   ├── routes_docs.py       # Docs endpoints
│   └── routes_tasks.py      # Tasks endpoints
├── core/
│   └── google_client.py     # Google API wrapper
└── models/
    └── schemas.py           # Pydantic models
```

---

## 🧪 Testing

### Local Test (curl)
```bash
# Send email
curl -X POST http://localhost:8082/google/gmail/send \
  -H "Content-Type: application/json" \
  -d '{"to": ["test@example.com"], "subject": "Test", "body": "Hello!"}'

# Create document
curl -X POST http://localhost:8082/google/docs/create \
  -H "Content-Type: application/json" \
  -d '{"title": "My New Document"}'
```

### Via GPT
Ask the GPT:
> "Create a Google Doc called 'Test Document' and send me an email with the link"

---

## ⚠️ Known Limitations

1. **ngrok URL changes** - Must update GPT Actions on every restart
2. **Requires local machine running** - Not deployed to cloud yet
3. **Token refresh** - May need manual re-auth if token expires after 7 days

---

## 🔮 Future Improvements

- [ ] Deploy to Google Cloud Run (always-on)
- [ ] Fixed domain (no ngrok)
- [ ] Add more operations (update docs, upload to Drive)
- [ ] Merge with GitHub Client into unified service

---

**Created**: 2025-11-24  
**Author**: Claude + Or  
**Status**: ✅ Production Ready
