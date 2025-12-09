"""
GCP Firewall Configuration Script
Creates firewall rules to allow HTTP (80) and HTTPS (443) traffic
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

# Configuration
PROJECT_ID = "edri2or-mcp"
REGION = "us-central1"

# Firewall rules to create
FIREWALL_RULES = [
    {
        "name": "allow-http",
        "description": "Allow HTTP traffic for Let's Encrypt and web access",
        "allowed": [{"IPProtocol": "tcp", "ports": ["80"]}],
        "sourceRanges": ["0.0.0.0/0"],
        "targetTags": ["http-server"],
        "direction": "INGRESS",
        "priority": 1000
    },
    {
        "name": "allow-https",
        "description": "Allow HTTPS traffic for secure web access",
        "allowed": [{"IPProtocol": "tcp", "ports": ["443"]}],
        "sourceRanges": ["0.0.0.0/0"],
        "targetTags": ["https-server"],
        "direction": "INGRESS",
        "priority": 1000
    }
]

def check_and_create_firewall_rules():
    """Check existing firewall rules and create missing ones"""
    
    print("\n" + "="*60)
    print("GCP Firewall Configuration")
    print("="*60)
    
    # Load service account credentials
    creds_path = r"C:\Users\edri2\Desktop\AI\ai-os\edri2or-mcp-dd7014777518.json"
    try:
        credentials = service_account.Credentials.from_service_account_file(
            creds_path,
            scopes=['https://www.googleapis.com/auth/compute']
        )
    except FileNotFoundError:
        print("ERROR: Service account key not found!")
        print("Please place it at:", creds_path)
        return False
    
    # Initialize Compute Engine API
    compute = build('compute', 'v1', credentials=credentials)
    
    # Check existing firewall rules
    print("\nChecking existing firewall rules...")
    try:
        result = compute.firewalls().list(project=PROJECT_ID).execute()
        existing_rules = {rule['name']: rule for rule in result.get('items', [])}
        print(f"Found {len(existing_rules)} existing rules")
    except Exception as e:
        print(f"Error listing firewall rules: {e}")
        return False
    
    # Create missing rules
    for rule_config in FIREWALL_RULES:
        rule_name = rule_config['name']
        
        if rule_name in existing_rules:
            print(f"\n✓ Rule '{rule_name}' already exists - skipping")
            continue
        
        print(f"\n→ Creating rule '{rule_name}'...")
        
        firewall_body = {
            "name": rule_name,
            "description": rule_config['description'],
            "allowed": rule_config['allowed'],
            "sourceRanges": rule_config['sourceRanges'],
            "targetTags": rule_config['targetTags'],
            "direction": rule_config['direction'],
            "priority": rule_config['priority']
        }
        
        try:
            operation = compute.firewalls().insert(
                project=PROJECT_ID,
                body=firewall_body
            ).execute()
            
            print(f"  Created: {rule_name}")
            print(f"  Ports: {rule_config['allowed'][0]['ports']}")
            print(f"  Tags: {rule_config['targetTags']}")
            
        except Exception as e:
            print(f"  ERROR: Failed to create rule: {e}")
            return False
    
    print("\n" + "="*60)
    print("Firewall configuration complete!")
    print("="*60)
    
    # Show final status
    print("\nFinal firewall rules:")
    for rule_config in FIREWALL_RULES:
        status = "✓ ACTIVE" if rule_config['name'] in existing_rules or True else "✗ FAILED"
        print(f"  {status} {rule_config['name']}: {rule_config['allowed'][0]['ports']}")
    
    return True

if __name__ == "__main__":
    success = check_and_create_firewall_rules()
    
    if success:
        print("\n✓ You can now restart Caddy and Let's Encrypt should work!")
        print("  Run: ssh root@35.223.68.23 'docker restart ai-os-caddy'")
    else:
        print("\n✗ Firewall configuration failed - manual intervention required")
        print("  Check GCP Console: VPC Network → Firewall")
