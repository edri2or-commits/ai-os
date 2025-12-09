#!/usr/bin/env python3
"""
Hetzner Cloud VPS Provisioning Script
Automates server creation via Hetzner Cloud API
"""

import requests
import time
import sys

# API Configuration
HETZNER_API_URL = "https://api.hetzner.cloud/v1"
API_TOKEN = "YOUR_API_TOKEN_HERE"  # User will paste this

# Server Configuration
SERVER_CONFIG = {
    "name": "ai-life-os-prod",
    "server_type": "cx32",
    "image": "ubuntu-24.04",
    "location": "nbg1",  # Nuremberg
    "ssh_keys": [],  # Will be populated
    "start_after_create": True,
    "labels": {
        "project": "ai-life-os",
        "environment": "production"
    }
}

# SSH Key Configuration
SSH_KEY_CONFIG = {
    "name": "ai-os-key",
    "public_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMgH3/5hc4lFOXlyCf59YArE22Bq5W5axftLxYOlH+Hj edri2or@gmail.com"
}

def api_request(method, endpoint, data=None):
    """Make authenticated API request to Hetzner"""
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    url = f"{HETZNER_API_URL}/{endpoint}"
    
    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    
    response.raise_for_status()
    return response.json()

def create_ssh_key():
    """Create or get existing SSH key"""
    print("📝 Creating SSH key...")
    
    try:
        result = api_request("POST", "ssh_keys", SSH_KEY_CONFIG)
        ssh_key_id = result["ssh_key"]["id"]
        print(f"✅ SSH key created: {ssh_key_id}")
        return ssh_key_id
    except requests.exceptions.HTTPError as e:
        if "uniqueness_error" in str(e):
            # Key already exists, get it
            keys = api_request("GET", "ssh_keys")
            for key in keys["ssh_keys"]:
                if key["name"] == SSH_KEY_CONFIG["name"]:
                    print(f"✅ SSH key found: {key['id']}")
                    return key["id"]
        raise

def create_server(ssh_key_id):
    """Create VPS server"""
    print("🖥️  Creating server...")
    
    SERVER_CONFIG["ssh_keys"] = [ssh_key_id]
    result = api_request("POST", "servers", SERVER_CONFIG)
    
    server_id = result["server"]["id"]
    server_ip = result["server"]["public_net"]["ipv4"]["ip"]
    root_password = result["root_password"]
    
    print(f"✅ Server created!")
    print(f"   ID: {server_id}")
    print(f"   IP: {server_ip}")
    print(f"   Root Password: {root_password}")
    
    return server_id, server_ip, root_password

def wait_for_server(server_id):
    """Wait for server to be ready"""
    print("⏳ Waiting for server to start...")
    
    max_attempts = 60  # 5 minutes
    for attempt in range(max_attempts):
        result = api_request("GET", f"servers/{server_id}")
        status = result["server"]["status"]
        
        if status == "running":
            print("✅ Server is running!")
            return True
        
        print(f"   Status: {status} ({attempt+1}/{max_attempts})")
        time.sleep(5)
    
    print("❌ Timeout waiting for server")
    return False

def main():
    """Main provisioning workflow"""
    print("=" * 50)
    print("🚀 Hetzner Cloud VPS Provisioning")
    print("=" * 50)
    
    try:
        # Step 1: Create SSH key
        ssh_key_id = create_ssh_key()
        
        # Step 2: Create server
        server_id, server_ip, root_password = create_server(ssh_key_id)
        
        # Step 3: Wait for server to be ready
        if not wait_for_server(server_id):
            sys.exit(1)
        
        # Success!
        print("\n" + "=" * 50)
        print("✅ VPS PROVISIONING COMPLETE!")
        print("=" * 50)
        print(f"🌐 IP Address: {server_ip}")
        print(f"🔑 Root Password: {root_password}")
        print(f"🔗 SSH Command: ssh root@{server_ip}")
        print("=" * 50)
        
        # Save credentials
        with open("vps-credentials.txt", "w") as f:
            f.write(f"Server ID: {server_id}\n")
            f.write(f"IP Address: {server_ip}\n")
            f.write(f"Root Password: {root_password}\n")
            f.write(f"SSH Command: ssh root@{server_ip}\n")
        
        print("💾 Credentials saved to: vps-credentials.txt")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
