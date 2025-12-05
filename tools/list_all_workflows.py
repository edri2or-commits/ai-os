"""
List all workflows from n8n instance
"""
import requests
import json
import sys
from pathlib import Path

# Read API key from .env
env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None

if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('N8N_API_KEY='):
                api_key = line.split('=', 1)[1].strip()
                break

if not api_key:
    print("ERROR: N8N_API_KEY not found in .env")
    sys.exit(1)

# Query n8n API
url = "http://localhost:5678/api/v1/workflows"
headers = {"X-N8N-API-KEY": api_key}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    
    workflows = response.json()
    
    print(f"\n=== Total Workflows: {len(workflows.get('data', []))} ===\n")
    
    for wf in workflows.get('data', []):
        print(f"ID: {wf.get('id')}")
        print(f"Name: {wf.get('name')}")
        print(f"Active: {wf.get('active')}")
        print(f"Created: {wf.get('createdAt', 'N/A')[:19]}")
        print(f"Updated: {wf.get('updatedAt', 'N/A')[:19]}")
        print("-" * 60)
        
except requests.exceptions.RequestException as e:
    print(f"ERROR: {e}")
    sys.exit(1)
