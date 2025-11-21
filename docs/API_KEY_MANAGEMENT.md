# API Key Management - SSOT Mapping

**Created**: 2025-11-21  
**Purpose**: Document automatic API key management from SSOT  
**Status**: ✅ Implemented

---

## 🎯 Overview

AI-OS automatically manages OPENAI_API_KEY by reading from a Single Source of Truth (SSOT) location, eliminating the need for manual copy-paste.

---

## 📍 SSOT Location

**Primary SSOT**:
```
C:\Users\edri2\make-ops-clean\SECRETS\.env.local
```

**Target Location** (AI-OS):
```
C:\Users\edri2\Work\AI-Projects\ai-os-claude-workspace\.env
```

---

## 🔄 How It Works

### **Automatic Sync**

The system automatically:
1. Reads `OPENAI_API_KEY` from SSOT
2. Creates/updates `.env` in AI-OS workspace
3. Configures for Real GPT mode (not Demo)

### **Manual Sync** (if needed)

```bash
python sync_api_key.py
```

This script:
- Reads key from SSOT
- Updates `.env` automatically
- Verifies configuration
- **Never prints the full key**

---

## ✅ Verification

After sync, verify with:

```bash
python test_real_gpt.py
```

**Expected output**:
```
✅ GPT PLANNER MODE: REAL
✅ API Key: Valid and working
✅ Model: gpt-4o-mini
✅ OpenAI API: Responding
```

---

## 🔒 Security

### **What's Protected**

- ✅ `.env` is **git-ignored** (never committed)
- ✅ Full key **never printed** to console/logs
- ✅ Only masked key shown: `sk-proj...qU8A`
- ✅ SSOT location kept private

### **What's Safe to Commit**

- ✅ `sync_api_key.py` (doesn't contain key)
- ✅ `test_real_gpt.py` (doesn't contain key)
- ✅ This documentation (no keys)

---

## 📋 Configuration Details

### **.env Structure**

```bash
# Mode: Real GPT
DEMO_MODE=false

# API Key (auto-synced)
OPENAI_API_KEY=sk-proj-...

# Model
OPENAI_MODEL=gpt-4o-mini

# Port
SERVER_PORT=8000
```

### **SSOT Structure**

The SSOT file contains:
```
OPENAI_API_KEY=sk-proj-...
```

The sync script automatically extracts this value.

---

## 🔧 Troubleshooting

### **Problem: "SSOT file not found"**

Check:
```bash
dir C:\Users\edri2\make-ops-clean\SECRETS\.env.local
```

If missing, the SSOT location may have changed.

### **Problem: "Still in DEMO mode"**

Run:
```bash
python sync_api_key.py
python test_real_gpt.py
```

Verify `.env` has:
```
DEMO_MODE=false
```

### **Problem: "Invalid API key"**

Check SSOT file contains:
- Key starts with `sk-`
- Key is recent (not expired)

Get new key at: https://platform.openai.com/api-keys

---

## 📊 Modes Comparison

| Aspect | Demo Mode | Real GPT Mode |
|--------|-----------|---------------|
| **API Key** | Not required | Required |
| **SSOT** | Not used | Auto-synced |
| **GPT Planner** | Simulated | Real OpenAI |
| **Cost** | Free | ~$0.01-0.05/intent |
| **Setup** | Automatic | One-time sync |

---

## 🚀 Quick Start

### **First Time Setup**

```bash
# Option 1: Automatic (recommended)
python start.py
# Will detect SSOT and sync automatically

# Option 2: Manual
python sync_api_key.py
python test_real_gpt.py
python start.py
```

### **Daily Use**

```bash
python start.py
# That's it! Key already synced.
```

---

## 🔄 Future: Multiple Environments

If you need different keys for different environments:

```bash
# Development
python sync_api_key.py --env dev

# Production
python sync_api_key.py --env prod
```

(Not implemented yet, but the architecture supports it)

---

## 📝 Change Log

### **v1.0** (2025-11-21)
- ✅ Automatic SSOT detection
- ✅ Auto-sync on startup
- ✅ Real GPT verification test
- ✅ Manual sync script
- ✅ Masked key display
- ✅ Security: never commit keys

---

**Status**: ✅ Working  
**Mode**: Real GPT  
**Next**: Use `python start.py` normally
