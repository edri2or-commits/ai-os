# n8n Infrastructure Setup

**Status:** INFRA_ONLY (Phase 2.3)  
**Purpose:** n8n Automation Kernel for AI-OS  
**Decision:** DEC-006 (approved)

---

## 🎯 What is this?

This directory contains the infrastructure setup for n8n - the automation kernel of AI-OS.

**Current Phase (2.3):**
- ✅ n8n running locally in Docker
- ✅ Basic auth configured
- ✅ Data persistence enabled
- ❌ No live workflows yet
- ❌ No connections to Gmail/Calendar/Tasks

**Future Phase (2.4+):**
- Workflows connecting to Google Workspace
- Workflows connecting to GitHub
- Controlled automation with Human-in-the-Loop

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Copy template to .env
cp ENV_TEMPLATE.env .env

# Edit .env and change:
# - N8N_BASIC_AUTH_PASSWORD (choose a secure password)
# - N8N_ENCRYPTION_KEY (generate with: openssl rand -base64 32)
```

### 2. Start n8n

```bash
# Start in background
docker-compose up -d

# Check logs
docker-compose logs -f n8n

# Check health
docker-compose ps
```

### 3. Access n8n

Open: http://localhost:5678

**Default credentials (change in .env):**
- Username: admin
- Password: CHANGE_ME

---

## 📁 Directory Structure

```
infra/n8n/
├── docker-compose.yml    # Docker setup
├── ENV_TEMPLATE.env      # Environment variables template
├── .env                  # Actual env vars (DO NOT commit)
├── data/                 # n8n data directory (created on first run)
│   ├── database.sqlite   # SQLite database
│   ├── workflows/        # Exported workflows (if any)
│   └── credentials/      # Encrypted credentials
└── README.md             # This file
```

---

## 🔐 Security Notes

1. **Never commit .env file** - it contains sensitive credentials
2. **Change default password** - use a strong password
3. **Generate encryption key** - used for credentials storage
4. **Keep data/ directory secure** - contains workflows and credentials

---

## 🛠️ Management Commands

```bash
# Start n8n
docker-compose up -d

# Stop n8n
docker-compose down

# Restart n8n
docker-compose restart

# View logs
docker-compose logs -f n8n

# Update n8n to latest version
docker-compose pull
docker-compose up -d

# Backup data
tar -czf n8n-backup-$(date +%Y%m%d).tar.gz data/

# Remove all (including data)
docker-compose down -v
```

---

## 📋 Next Steps (Phase 2.4+)

1. **Credentials Setup:**
   - Add Google OAuth credentials
   - Add GitHub token
   - Add any other integration credentials

2. **Workflow Development:**
   - Create test workflows (sandbox only)
   - Get approval from Or
   - Deploy to production with monitoring

3. **Integration:**
   - Connect to AI-OS State Layer
   - Enable webhook endpoints
   - Set up monitoring and logging

---

## 🔗 Related Documentation

- **Decision:** `docs/DECISIONS_AI_OS.md` (DEC-006)
- **Infra Map:** `docs/INFRA_MAP.md`
- **Services Status:** `docs/system_state/registries/SERVICES_STATUS.json`
- **n8n Official Docs:** https://docs.n8n.io/

---

**Last Updated:** 2025-11-26  
**Updated By:** Claude Desktop (BLOCK_N8N_INFRA_BOOTSTRAP_V1)  
**Phase:** 2.3 - INFRA_ONLY
