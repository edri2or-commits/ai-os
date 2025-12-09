#!/bin/bash
# VPS Workflow Import Script
# Purpose: Import workflows from local backup to VPS n8n

set -e

echo "🚀 Starting VPS Workflow Import..."

# Step 1: Copy backup file to VPS
echo "📦 Copying workflows backup to VPS..."
scp C:/Users/edri2/Desktop/AI/ai-os/exports/workflows_local_backup_20251206_233656.json \
    ai-life-os-prod:/tmp/workflows_backup.json

# Step 2: Import workflows using n8n CLI
echo "📥 Importing workflows into n8n..."
sudo docker exec ai-os-n8n \
    n8n import:workflow --input=/tmp/workflows_backup.json --separate

# Step 3: List imported workflows
echo "✅ Listing imported workflows..."
sudo docker exec ai-os-n8n n8n list:workflow

echo "🎉 Import complete!"
