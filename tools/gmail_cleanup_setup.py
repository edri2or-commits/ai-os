#!/usr/bin/env python3
"""
Gmail Cleanup - Setup Script
=============================

This script sets up OAuth authentication for Gmail and Drive APIs.
Run this ONCE before using gmail_cleanup.py
"""

import os
import sys
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/drive.file'
]

def setup_oauth():
    """Run OAuth flow to get credentials"""
    print("🔐 Gmail Cleanup - OAuth Setup")
    print("="*60)
    
    # Check if credentials already exist
    creds_dir = Path.home() / '.credentials'
    token_path = creds_dir / 'gmail_cleanup_token.json'
    
    if token_path.exists():
        print(f"⚠️  Credentials already exist at: {token_path}")
        response = input("Do you want to re-authenticate? (yes/no): ").strip().lower()
        if response != 'yes':
            print("✅ Setup cancelled")
            return True
    
    # Create credentials directory
    creds_dir.mkdir(parents=True, exist_ok=True)
    
    # Check for client secrets
    secrets_path = Path(__file__).parent / 'client_secrets.json'
    if not secrets_path.exists():
        print("\n❌ ERROR: client_secrets.json not found!")
        print(f"   Expected location: {secrets_path}")
        print("\n📝 To get client_secrets.json:")
        print("   1. Go to: https://console.cloud.google.com/apis/credentials")
        print("   2. Create OAuth 2.0 Client ID (Desktop app)")
        print("   3. Download JSON file")
        print("   4. Rename to client_secrets.json")
        print(f"   5. Place in: {secrets_path.parent}")
        return False
    
    # Run OAuth flow
    print("\n🌐 Starting OAuth flow...")
    print("   A browser window will open.")
    print("   Please authorize the application.\n")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(secrets_path),
            SCOPES
        )
        
        creds = flow.run_local_server(port=0)
        
        # Save credentials
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        
        print(f"\n✅ Authentication successful!")
        print(f"   Token saved to: {token_path}")
        print(f"\n🎉 Setup complete! You can now run gmail_cleanup.py")
        
        return True
    except Exception as e:
        print(f"\n❌ Authentication failed: {str(e)}")
        return False


if __name__ == '__main__':
    success = setup_oauth()
    sys.exit(0 if success else 1)
