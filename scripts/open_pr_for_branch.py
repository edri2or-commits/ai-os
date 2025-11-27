#!/usr/bin/env python3
"""
Open PR for Branch - Wrapper Script

Creates a Pull Request from an existing, pushed branch using GitHub API.

This script is the standard way to open PRs from completed slices in AI-OS.
Every slice should end with:
  1. A pushed branch (e.g., feature/slice_name)
  2. A PR body file (e.g., slice_name_pr_body.txt)

Usage:
    python scripts/open_pr_for_branch.py \\
        --branch feature/slice_governance_truth_bootstrap_v1 \\
        --body-file governance_truth_pr_body.txt \\
        --base main \\
        --title "SLICE_GOVERNANCE_TRUTH_BOOTSTRAP_V1 - Description"
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

# Add parent directory to path to import from services
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from github import Github, GithubException
except ImportError:
    print("[ERROR] PyGithub not installed")
    print("Install with: pip install PyGithub")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("[ERROR] python-dotenv not installed")
    print("Install with: pip install python-dotenv")
    sys.exit(1)


def load_github_config() -> Dict[str, str]:
    """Load GitHub configuration from .env file"""
    # Try to load from mcp_github_client .env
    env_path = Path(__file__).parent.parent / "services" / "mcp_github_client" / ".env"
    
    if env_path.exists():
        load_dotenv(env_path)
        print(f"[INFO] Loaded config from: {env_path}")
    else:
        print(f"[WARNING] .env not found at: {env_path}")
        print("[INFO] Trying environment variables...")
    
    config = {
        "token": os.getenv("GITHUB_TOKEN"),
        "owner": os.getenv("GITHUB_OWNER", "edri2or-commits"),
        "repo": os.getenv("GITHUB_REPO", "ai-os"),
    }
    
    if not config["token"]:
        print("[ERROR] GITHUB_TOKEN not found in .env or environment")
        print("\nPlease create services/mcp_github_client/.env from .env.template:")
        print("  cp services/mcp_github_client/.env.template services/mcp_github_client/.env")
        print("  # Then edit .env and add: GITHUB_TOKEN=ghp_your_token_here")
        sys.exit(1)
    
    return config


def check_branch_exists(branch: str) -> bool:
    """Check if branch exists locally"""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--verify", branch],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"[ERROR] Failed to check branch: {e}")
        return False


def check_branch_pushed(branch: str) -> bool:
    """Check if branch is pushed to origin"""
    try:
        result = subprocess.run(
            ["git", "ls-remote", "--heads", "origin", branch],
            capture_output=True,
            text=True,
            check=False
        )
        return bool(result.stdout.strip())
    except Exception as e:
        print(f"[ERROR] Failed to check remote branch: {e}")
        return False


def read_pr_body(body_file: Path) -> str:
    """Read PR body from file"""
    if not body_file.exists():
        print(f"[ERROR] PR body file not found: {body_file}")
        sys.exit(1)
    
    try:
        return body_file.read_text(encoding="utf-8")
    except Exception as e:
        print(f"[ERROR] Failed to read PR body: {e}")
        sys.exit(1)


def create_pull_request(
    config: Dict[str, str],
    branch: str,
    base: str,
    title: str,
    body: str
) -> Optional[str]:
    """Create a Pull Request using GitHub API"""
    try:
        # Initialize GitHub client
        g = Github(config["token"])
        repo = g.get_repo(f"{config['owner']}/{config['repo']}")
        
        print(f"[INFO] Creating PR...")
        print(f"  Base: {base}")
        print(f"  Head: {branch}")
        print(f"  Title: {title}")
        
        # Create the PR
        pr = repo.create_pull(
            title=title,
            body=body,
            head=branch,
            base=base
        )
        
        print(f"\n✅ [SUCCESS] PR created!")
        print(f"  Number: #{pr.number}")
        print(f"  URL: {pr.html_url}")
        
        return pr.html_url
        
    except GithubException as e:
        print(f"\n❌ [ERROR] GitHub API error: {e.status}")
        print(f"  Message: {e.data.get('message', 'Unknown error')}")
        
        # Helpful error messages
        if e.status == 422:
            errors = e.data.get('errors', [])
            for error in errors:
                print(f"  - {error.get('message', 'Unknown validation error')}")
            
            # Check if PR already exists
            if any('pull request already exists' in str(e).lower() for e in errors):
                print("\n[INFO] A PR might already exist for this branch")
                print("Check: https://github.com/{}/{}/pulls?q=is:pr+head:{}".format(
                    config['owner'], config['repo'], branch
                ))
        
        return None
        
    except Exception as e:
        print(f"\n❌ [ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Create a Pull Request from an existing branch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python scripts/open_pr_for_branch.py \\
      --branch feature/my-slice \\
      --body-file my_pr_body.txt \\
      --title "My Slice Description"
  
  # With custom base branch
  python scripts/open_pr_for_branch.py \\
      --branch feature/my-slice \\
      --body-file my_pr_body.txt \\
      --title "My Slice" \\
      --base develop
        """
    )
    
    parser.add_argument(
        "--branch",
        required=True,
        help="Source branch name (must exist and be pushed)"
    )
    
    parser.add_argument(
        "--body-file",
        required=True,
        type=Path,
        help="Path to file containing PR body/description"
    )
    
    parser.add_argument(
        "--title",
        required=True,
        help="PR title"
    )
    
    parser.add_argument(
        "--base",
        default="main",
        help="Target base branch (default: main)"
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("  AI-OS: Open PR for Branch")
    print("=" * 70)
    
    # Step 1: Load config
    print("\n[1/5] Loading GitHub configuration...")
    config = load_github_config()
    print(f"  Repository: {config['owner']}/{config['repo']}")
    
    # Step 2: Validate branch exists locally
    print(f"\n[2/5] Checking branch exists: {args.branch}")
    if not check_branch_exists(args.branch):
        print(f"  ❌ Branch '{args.branch}' not found locally")
        print("\n  Did you mean one of these?")
        subprocess.run(["git", "branch", "--list", "*slice*"], check=False)
        sys.exit(1)
    print(f"  ✅ Branch exists locally")
    
    # Step 3: Validate branch is pushed
    print(f"\n[3/5] Checking branch is pushed to origin...")
    if not check_branch_pushed(args.branch):
        print(f"  ❌ Branch '{args.branch}' not found on origin")
        print(f"\n  Push it with: git push origin {args.branch}")
        sys.exit(1)
    print(f"  ✅ Branch pushed to origin")
    
    # Step 4: Read PR body
    print(f"\n[4/5] Reading PR body from: {args.body_file}")
    body = read_pr_body(args.body_file)
    print(f"  ✅ PR body read: {len(body)} characters")
    
    # Step 5: Create PR
    print(f"\n[5/5] Creating Pull Request...")
    pr_url = create_pull_request(
        config=config,
        branch=args.branch,
        base=args.base,
        title=args.title,
        body=body
    )
    
    if pr_url:
        print("\n" + "=" * 70)
        print("  PR Created Successfully!")
        print("=" * 70)
        print(f"\n  🔗 {pr_url}\n")
        sys.exit(0)
    else:
        print("\n" + "=" * 70)
        print("  PR Creation Failed")
        print("=" * 70)
        sys.exit(1)


if __name__ == "__main__":
    main()
