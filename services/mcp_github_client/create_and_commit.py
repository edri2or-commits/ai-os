"""
One-time automation script to create branch and commit MCP GitHub Client.
This script uses GitHub API to avoid manual git commands.

Usage:
    python create_and_commit.py

Requirements:
    - GITHUB_PAT environment variable set
    - pip install httpx
"""

import os
import sys
import base64
import httpx
from pathlib import Path

# Configuration
OWNER = "edri2or-commits"
REPO = "ai-os"
BRANCH_NAME = "feature/mcp-github-client-init"
BASE_BRANCH = "main"
REPO_ROOT = Path(__file__).parent.parent.parent.parent


def get_github_token():
    """Get GitHub token from environment"""
    token = os.getenv("GITHUB_PAT")
    if not token:
        print("❌ Error: GITHUB_PAT environment variable not set")
        print("   Set it with: $env:GITHUB_PAT = 'your_token_here'")
        sys.exit(1)
    return token


def create_branch_and_commit():
    """Create branch and commit all files via GitHub API"""
    token = get_github_token()
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AI-OS-Setup/1.0"
    }
    
    base_url = f"https://api.github.com/repos/{OWNER}/{REPO}"
    
    print(f"🔄 Creating branch '{BRANCH_NAME}' and committing files...")
    
    with httpx.Client(timeout=30.0) as client:
        # Step 1: Get main branch SHA
        print(f"1️⃣  Getting {BASE_BRANCH} branch SHA...")
        response = client.get(
            f"{base_url}/git/ref/heads/{BASE_BRANCH}",
            headers=headers
        )
        
        if response.status_code != 200:
            print(f"❌ Failed to get {BASE_BRANCH} SHA: {response.status_code}")
            print(response.text)
            sys.exit(1)
        
        base_sha = response.json()["object"]["sha"]
        print(f"   Base SHA: {base_sha[:8]}...")
        
        # Step 2: Create new branch
        print(f"2️⃣  Creating branch '{BRANCH_NAME}'...")
        response = client.post(
            f"{base_url}/git/refs",
            headers=headers,
            json={
                "ref": f"refs/heads/{BRANCH_NAME}",
                "sha": base_sha
            }
        )
        
        if response.status_code not in [200, 201]:
            print(f"❌ Failed to create branch: {response.status_code}")
            print(response.text)
            sys.exit(1)
        
        print(f"   ✅ Branch created")
        
        # Step 3: Get all files in services/mcp_github_client/
        print("3️⃣  Collecting files to commit...")
        service_dir = REPO_ROOT / "services" / "mcp_github_client"
        
        files_to_commit = []
        for file_path in service_dir.rglob("*"):
            if file_path.is_file() and not str(file_path).endswith(".pyc"):
                relative_path = file_path.relative_to(REPO_ROOT)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                files_to_commit.append({
                    "path": str(relative_path).replace("\\", "/"),
                    "content": content
                })
        
        print(f"   Found {len(files_to_commit)} files")
        
        # Step 4: Commit all files to the new branch
        print("4️⃣  Committing files...")
        for file_info in files_to_commit:
            path = file_info["path"]
            content = file_info["content"]
            
            # Encode content
            encoded_content = base64.b64encode(content.encode()).decode()
            
            # Create/update file
            response = client.put(
                f"{base_url}/contents/{path}",
                headers=headers,
                json={
                    "message": f"[L2-Setup] Add {path}",
                    "content": encoded_content,
                    "branch": BRANCH_NAME
                }
            )
            
            if response.status_code not in [200, 201]:
                print(f"   ⚠️  Failed to commit {path}: {response.status_code}")
            else:
                print(f"   ✅ Committed {path}")
        
        print("")
        print("✅ All files committed successfully!")
        print(f"🔗 Branch: https://github.com/{OWNER}/{REPO}/tree/{BRANCH_NAME}")
        print("")
        print("Next step: Claude will create the PR via GitHub API")


if __name__ == "__main__":
    try:
        create_branch_and_commit()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
