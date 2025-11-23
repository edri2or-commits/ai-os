# MCP GitHub Client - Integration Guide for GPT

This guide contains everything you need to connect a Custom GPT to the MCP GitHub Client service.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [OpenAPI Schema for GPT Actions](#openapi-schema-for-gpt-actions)
3. [System Prompt for Custom GPT](#system-prompt-for-custom-gpt)
4. [Running the Service Locally](#running-the-service-locally)
5. [Testing the Integration](#testing-the-integration)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Step 1: Run the Service

From the project root directory:

```bash
python start_github_client.py
```

Or manually:

```bash
python -m uvicorn services.mcp_github_client.main:app --port 8081 --reload
```

The service will start at: **http://localhost:8081**

### Step 2: Verify Service is Running

Open in browser: http://localhost:8081/health

You should see:

```json
{
  "ok": true,
  "service": "AI-OS MCP GitHub Client",
  "github_configured": true,
  "openai_configured": true,
  "repository": "edri2or-commits/ai-os"
}
```

### Step 3: Add to Custom GPT

1. Go to ChatGPT → Create GPT
2. Configure → Actions → "Create new action"
3. Paste the OpenAPI schema (see below)
4. Set Authentication: "None" (for local testing)
5. Set Privacy: "Only me"
6. Add the System Prompt (see below)

---

## 📝 OpenAPI Schema for GPT Actions

Copy this YAML into the "Schema" section of your Custom GPT Action:

```yaml
openapi: 3.1.0
info:
  title: AI-OS MCP GitHub Client
  description: HTTP service for GitHub operations - all changes go through Pull Requests
  version: 0.1.0
servers:
  - url: http://localhost:8081
    description: Local development server

paths:
  /github/read-file:
    post:
      operationId: readFile
      summary: Read a file from the GitHub repository
      description: |
        Reads the content of a file from the GitHub repository.
        Use this to examine existing files before making changes.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - path
              properties:
                path:
                  type: string
                  description: Path to the file in the repository (e.g., "README.md", "src/main.py")
                  example: "README.md"
                ref:
                  type: string
                  description: Git ref (branch/tag/commit) to read from
                  default: "main"
                  example: "main"
      responses:
        '200':
          description: File read response (check 'ok' field for success/failure)
          content:
            application/json:
              schema:
                type: object
                required:
                  - ok
                properties:
                  ok:
                    type: boolean
                    description: Whether the operation succeeded
                  content:
                    type: string
                    description: File content (if ok=true)
                  path:
                    type: string
                    description: File path that was read
                  sha:
                    type: string
                    description: Git SHA of the file
                  message:
                    type: string
                    description: Human-readable message
                  error_type:
                    type: string
                    description: Error type (if ok=false)
                  status_code:
                    type: integer
                    description: HTTP status code (if error)

  /github/list-tree:
    post:
      operationId: listTree
      summary: List files in the repository tree
      description: |
        Lists files and directories in the repository.
        Use this to explore the repository structure.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                path:
                  type: string
                  description: Path to list (empty string = root)
                  default: ""
                  example: "src"
                ref:
                  type: string
                  description: Git ref (branch/tag/commit)
                  default: "main"
                  example: "main"
                recursive:
                  type: boolean
                  description: Whether to list recursively
                  default: false
      responses:
        '200':
          description: Tree listing response (check 'ok' field)
          content:
            application/json:
              schema:
                type: object
                required:
                  - ok
                properties:
                  ok:
                    type: boolean
                    description: Whether the operation succeeded
                  tree:
                    type: array
                    description: List of tree items (if ok=true)
                    items:
                      type: object
                      properties:
                        path:
                          type: string
                        type:
                          type: string
                          enum: [blob, tree]
                        sha:
                          type: string
                  path:
                    type: string
                    description: Path that was listed
                  message:
                    type: string
                    description: Human-readable message
                  error_type:
                    type: string
                    description: Error type (if ok=false)

  /github/open-pr:
    post:
      operationId: openPullRequest
      summary: Open a Pull Request with file changes
      description: |
        Creates a Pull Request with the specified file changes.
        This is the ONLY way to make changes to the repository.
        
        Process:
        1. Creates a new branch from base_branch
        2. Applies all file changes to the new branch
        3. Opens a PR from the new branch to base_branch
        
        IMPORTANT: All changes go through PR review before merging to main.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - title
                - description
                - files
              properties:
                title:
                  type: string
                  description: PR title (concise and descriptive)
                  example: "Add new feature"
                description:
                  type: string
                  description: PR description (explain what and why)
                  example: "This PR adds a new feature that..."
                files:
                  type: array
                  description: List of file changes to include in the PR
                  items:
                    type: object
                    required:
                      - path
                      - content
                    properties:
                      path:
                        type: string
                        description: File path in the repository
                        example: "src/new_feature.py"
                      content:
                        type: string
                        description: Complete new file content
                        example: "def hello():\n    print('world')"
                      operation:
                        type: string
                        description: Operation type
                        enum: [create, update, delete]
                        default: "update"
                base_branch:
                  type: string
                  description: Base branch to merge into
                  default: "main"
                  example: "main"
                use_ai_generation:
                  type: boolean
                  description: Use AI to enhance PR description
                  default: false
      responses:
        '200':
          description: PR creation response (check 'ok' field)
          content:
            application/json:
              schema:
                type: object
                required:
                  - ok
                properties:
                  ok:
                    type: boolean
                    description: Whether the operation succeeded
                  pr_number:
                    type: integer
                    description: PR number (if ok=true)
                  pr_url:
                    type: string
                    description: PR URL (if ok=true)
                  branch_name:
                    type: string
                    description: Branch name that was created
                  message:
                    type: string
                    description: Human-readable message
                  error_type:
                    type: string
                    description: Error type (if ok=false)
```

---

## 💬 System Prompt for Custom GPT

Copy this into the "Instructions" section of your Custom GPT:

```
You are an AI assistant that helps manage the AI-OS codebase through GitHub operations.

# Core Principles

1. **Read-Only by Default**: Always read files first to understand current state
2. **PR-Based Workflow**: ALL changes go through Pull Requests, never direct commits
3. **Structured Responses**: Always check the 'ok' field in API responses

# Available Operations

## Reading Files
Use `readFile` to examine existing files:
- Always read before modifying
- Use to understand current code structure
- Check if files exist before creating new ones

## Listing Repository
Use `listTree` to explore the repository:
- Start with path="" to see root
- Use recursive=true for deep exploration
- Understand project structure before changes

## Making Changes
Use `openPullRequest` to propose changes:
- ALWAYS provide complete file content (not diffs)
- Include multiple file changes in a single PR
- Write clear PR titles and descriptions
- Explain what changed and why

# Workflow Example

When asked to "add a new feature":

1. **Understand**: Use listTree to see project structure
2. **Read**: Use readFile to examine related files
3. **Plan**: Determine which files need changes
4. **Execute**: Use openPullRequest with ALL changes
5. **Report**: Share the PR URL with the user

# Important Notes

- Never assume files exist - always check first
- Always provide COMPLETE file content, not snippets
- If 'ok' is false, explain the error to the user
- PR titles should be concise (max 50 chars)
- PR descriptions should explain the "what" and "why"
- All PRs target the 'main' branch by default

# Response Handling

ALL API calls return responses with an 'ok' field:

```json
{
  "ok": true,   // Success
  "content": "...",
  "message": "..."
}
```

or

```json
{
  "ok": false,  // Failure
  "error_type": "http_404",
  "message": "File not found"
}
```

Always check 'ok' before processing the response.

# Example Interaction

User: "Add a hello world script"

You:
1. List files to see structure: listTree(path="", recursive=false)
2. Check if src/ exists: readFile(path="src/main.py") [to see pattern]
3. Create PR: openPullRequest(
     title="Add hello world script",
     description="Adds a simple hello world script in src/hello.py",
     files=[{
       path: "src/hello.py",
       content: "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()",
       operation: "create"
     }]
   )
4. Share PR URL with user

Remember: You're working with a real GitHub repository. Be thoughtful and precise.
```

---

## 🖥️ Running the Service Locally

### Prerequisites

1. Python 3.8+
2. pip installed
3. GitHub Personal Access Token (PAT) with `repo` scope

### Setup Steps

1. **Navigate to project root:**
   ```bash
   cd C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace
   ```

2. **Create `.env` file** (if not exists):
   ```bash
   cp .env.template .env
   ```

3. **Edit `.env` and set:**
   ```env
   GITHUB_PAT=ghp_your_token_here
   GITHUB_OWNER=edri2or-commits
   GITHUB_REPO=ai-os
   OPENAI_API_KEY=sk-your_key_here  # Optional, for AI features
   SERVICE_PORT=8081
   ```

4. **Install dependencies:**
   ```bash
   pip install -r services/mcp_github_client/requirements.txt
   ```

5. **Run the service:**
   ```bash
   python start_github_client.py
   ```

### Verify It's Running

Open these URLs in your browser:

- **Health Check**: http://localhost:8081/health
- **API Docs**: http://localhost:8081/docs
- **Root**: http://localhost:8081/

You should see JSON responses, not errors.

---

## 🧪 Testing the Integration

### Test 1: Read a File

```bash
curl -X POST http://localhost:8081/github/read-file \
  -H "Content-Type: application/json" \
  -d '{"path": "README.md", "ref": "main"}'
```

Expected response:
```json
{
  "ok": true,
  "content": "# AI-OS\n\n...",
  "path": "README.md",
  "sha": "...",
  "message": "File read successfully"
}
```

### Test 2: List Repository Tree

```bash
curl -X POST http://localhost:8081/github/list-tree \
  -H "Content-Type: application/json" \
  -d '{"path": "", "ref": "main", "recursive": false}'
```

Expected response:
```json
{
  "ok": true,
  "tree": [
    {"path": "README.md", "type": "blob", ...},
    {"path": "services", "type": "tree", ...}
  ],
  "message": "Tree listed successfully"
}
```

### Test 3: Open a PR (using GPT)

In your Custom GPT, try:
```
"Create a test file at test/hello.txt with the content 'Hello, World!'"
```

The GPT should:
1. Call `openPullRequest`
2. Return a PR URL like: https://github.com/edri2or-commits/ai-os/pull/X

---

## 🔧 Troubleshooting

### Service Won't Start

**Error: Port already in use**
```
Solution: Change port in .env or kill existing process
```

**Error: Module not found**
```
Solution: Install dependencies:
pip install -r services/mcp_github_client/requirements.txt
```

### GitHub API Errors

**Error: "http_401" - Bad credentials**
```
Solution: Check GITHUB_PAT in .env is valid and has 'repo' scope
```

**Error: "http_404" - Not Found**
```
Solution: Verify GITHUB_OWNER and GITHUB_REPO in .env are correct
```

### GPT Integration Issues

**GPT can't reach service**
```
Solution: For localhost, use ngrok or similar tunnel:
ngrok http 8081
Then update server URL in GPT Action to ngrok URL
```

**GPT gets "ok: false" responses**
```
Solution: Check service logs for detailed error messages
```

### Logs

Service logs are printed to console. Look for:
- `INFO` - Normal operations
- `WARNING` - Non-critical issues
- `ERROR` - Failed operations

To increase log verbosity, set in `.env`:
```env
LOG_LEVEL=DEBUG
```

---

## 📊 Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GITHUB_API_BASE_URL` | No | `https://api.github.com` | GitHub API endpoint |
| `GITHUB_PAT` | Yes* | - | GitHub Personal Access Token |
| `GITHUB_OWNER` | No | `edri2or-commits` | Repository owner |
| `GITHUB_REPO` | No | `ai-os` | Repository name |
| `OPENAI_API_KEY` | No | - | OpenAI key for AI features |
| `OPENAI_MODEL` | No | `gpt-4o-mini` | OpenAI model to use |
| `LOG_LEVEL` | No | `INFO` | Logging level |
| `SERVICE_PORT` | No | `8081` | HTTP server port |

*Required for write operations (PRs), optional for read-only

---

## 🎯 Next Steps

1. ✅ Get the service running locally
2. ✅ Test endpoints with curl
3. ✅ Create Custom GPT with schema + prompt
4. ✅ Test GPT integration
5. 🚀 Deploy to production (optional)

---

## 📞 Support

If you encounter issues:
1. Check service logs
2. Verify `.env` configuration
3. Test endpoints with curl first
4. Check GitHub PAT permissions

---

**Version**: 0.1.0  
**Last Updated**: 2025-01-23
