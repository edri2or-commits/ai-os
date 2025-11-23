# MCP GitHub Client - The Heart of AI-OS

HTTP service that provides GitHub operations for AI-OS through a secure PR-based workflow.

## 🎯 Purpose

This service is the **single point of control** for all GitHub operations in AI-OS:
- GPT (Custom Actions) talks to THIS service
- This service talks to GitHub API
- ALL changes go through Pull Requests (no direct writes to main)

## 🏗️ Architecture

```
GPT Custom Action
    ↓ (HTTP)
MCP GitHub Client (this service)
    ↓ (GitHub API)
GitHub Repository (edri2or-commits/ai-os)
```

## 📡 Endpoints

### `POST /github/read-file`
Read a file from the repository.

**Request:**
```json
{
  "path": "README.md",
  "ref": "main"
}
```

**Response:**
```json
{
  "ok": true,
  "content": "file content here...",
  "path": "README.md",
  "sha": "abc123...",
  "message": "File read successfully"
}
```

### `POST /github/list-tree`
List files in the repository tree.

**Request:**
```json
{
  "path": "",
  "ref": "main",
  "recursive": false
}
```

**Response:**
```json
{
  "ok": true,
  "tree": [
    {"path": "README.md", "type": "blob", "sha": "..."},
    {"path": "services", "type": "tree", "sha": "..."}
  ],
  "message": "Tree listed successfully"
}
```

### `POST /github/open-pr`
Create a Pull Request with file changes.

**Request:**
```json
{
  "title": "Add new feature",
  "description": "This PR adds...",
  "files": [
    {
      "path": "src/new_file.py",
      "content": "print('hello')",
      "operation": "create"
    }
  ],
  "base_branch": "main",
  "use_ai_generation": false
}
```

**Response:**
```json
{
  "ok": true,
  "pr_number": 42,
  "pr_url": "https://github.com/edri2or-commits/ai-os/pull/42",
  "branch_name": "ai-os-pr-20250101-120000",
  "message": "Pull Request created successfully"
}
```

## 🔧 Configuration

Create a `.env` file (see `.env.template`):

```env
# GitHub Configuration
GITHUB_API_BASE_URL=https://api.github.com
GITHUB_PAT=your_github_personal_access_token
GITHUB_OWNER=edri2or-commits
GITHUB_REPO=ai-os

# OpenAI Configuration (optional, for AI-powered PR descriptions)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4o-mini

# Service Configuration
LOG_LEVEL=INFO
SERVICE_PORT=8081
```

## 🚀 Running Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set environment variables (see Configuration above)

3. Run the service:
```bash
python -m uvicorn services.mcp_github_client.main:app --port 8081
```

Or from the project root:
```bash
python -m services.mcp_github_client.main
```

The service will be available at `http://localhost:8081`

## 🧪 Testing

Run tests with pytest:
```bash
pytest services/mcp_github_client/tests/
```

## 📋 Response Format

ALL endpoints follow the same response pattern:

**Success:**
```json
{
  "ok": true,
  "message": "Operation succeeded",
  ... (additional fields specific to the operation)
}
```

**Error:**
```json
{
  "ok": false,
  "error_type": "http_404",
  "message": "File not found",
  "status_code": 404
}
```

The `ok` field is ALWAYS present and determines success/failure.

## 🔐 Security Notes

- Never commit `.env` or secrets to git
- GitHub PAT should have repo scope
- In production, restrict CORS origins
- All changes require PR review before merging to main

## 🎨 Integration with GPT

To connect this service to a Custom GPT:

1. Run the service locally or deploy it
2. In GPT Custom Actions, add the OpenAPI schema (see below)
3. Set the server URL to `http://localhost:8081` (or your deployed URL)
4. GPT can now read files and open PRs automatically

## 📝 Version

Current version: **0.1.0**
