"""
SSOT Writer - Automated SSOT Document Updates

This module enables automated updates to AI-OS SSOT documents (Single Source of Truth).
External agents (GPT, Telegram, n8n) can update SYSTEM_SNAPSHOT, CAPABILITIES_MATRIX,
and DECISIONS_AI_OS through this service.

Core capabilities:
- Read current SSOT document content
- Update with new full content
- Auto-commit and push to GitHub
- Validation and safety checks

Author: AI-OS System
Created: 2025-11-23
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Optional, Tuple
from datetime import datetime


# Valid SSOT document targets
VALID_TARGETS = {
    "system_snapshot": "docs/SYSTEM_SNAPSHOT.md",
    "capabilities_matrix": "docs/CAPABILITIES_MATRIX.md",
    "decisions": "docs/DECISIONS_AI_OS.md"
}


class SSOTWriter:
    """
    Handles automated updates to SSOT documents.
    
    This class provides safe, validated methods to update AI-OS SSOT documents
    and automatically commit/push changes to GitHub.
    
    Example:
        writer = SSOTWriter()
        result = writer.update_ssot(
            target="system_snapshot",
            mode="replace_full",
            content="# New content..."
        )
    """
    
    def __init__(self, repo_root: Optional[Path] = None):
        """
        Initialize SSOT Writer.
        
        Args:
            repo_root: Path to repository root. If None, auto-detects from module location.
        """
        if repo_root is None:
            # Auto-detect: go up two levels from ai_core/ssot_writer.py
            self.repo_root = Path(__file__).parent.parent
        else:
            self.repo_root = Path(repo_root)
        
        # Verify we're in the right repo
        if not (self.repo_root / "docs").exists():
            raise ValueError(f"Invalid repo root: {self.repo_root} - docs/ not found")
    
    def validate_target(self, target: str) -> Tuple[bool, str, Optional[Path]]:
        """
        Validate that the target is a valid SSOT document.
        
        Args:
            target: Target identifier (e.g., "system_snapshot")
        
        Returns:
            Tuple of (is_valid, message, file_path)
        """
        if target not in VALID_TARGETS:
            return (
                False,
                f"Invalid target '{target}'. Valid targets: {list(VALID_TARGETS.keys())}",
                None
            )
        
        file_path = self.repo_root / VALID_TARGETS[target]
        
        if not file_path.exists():
            return (
                False,
                f"SSOT file not found: {file_path}",
                None
            )
        
        return (True, "Valid target", file_path)
    
    def read_current_content(self, target: str) -> Optional[str]:
        """
        Read the current content of an SSOT document.
        
        Args:
            target: Target identifier (e.g., "system_snapshot")
        
        Returns:
            Current content as string, or None if error
        """
        is_valid, msg, file_path = self.validate_target(target)
        
        if not is_valid:
            raise ValueError(msg)
        
        try:
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            raise IOError(f"Failed to read {file_path}: {str(e)}")
    
    def update_ssot(
        self,
        target: str,
        mode: str,
        content: str,
        commit_message: Optional[str] = None
    ) -> Dict:
        """
        Update an SSOT document with new content.
        
        Args:
            target: Target identifier ("system_snapshot", "capabilities_matrix", "decisions")
            mode: Update mode (currently only "replace_full" is supported)
            content: New full content for the document
            commit_message: Optional custom commit message
        
        Returns:
            Dict with:
                - ok: bool - Success status
                - file_path: str - Path to updated file
                - commit_sha: str - Git commit SHA (if successful)
                - commit_message: str - The commit message used
                - error: Optional[str] - Error message if failed
        
        Raises:
            ValueError: If target or mode is invalid
            IOError: If file operations fail
        """
        # Validate inputs
        if mode != "replace_full":
            raise ValueError(f"Unsupported mode '{mode}'. Only 'replace_full' is currently supported.")
        
        is_valid, msg, file_path = self.validate_target(target)
        if not is_valid:
            raise ValueError(msg)
        
        if not content or len(content.strip()) == 0:
            raise ValueError("Content cannot be empty")
        
        # Prepare result dict
        result = {
            "ok": False,
            "file_path": str(file_path),
            "commit_sha": "",
            "commit_message": "",
            "error": None
        }
        
        try:
            # Step 1: Write new content
            file_path.write_text(content, encoding='utf-8')
            
            # Step 2: Git add
            subprocess.run(
                ["git", "add", str(file_path)],
                cwd=self.repo_root,
                check=True,
                capture_output=True
            )
            
            # Step 3: Git commit
            if commit_message is None:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                commit_message = f"feat(ssot): update {target} via SSOT Writer [{timestamp}]"
            
            commit_result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Step 4: Get commit SHA
            sha_result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            commit_sha = sha_result.stdout.strip()
            
            # Step 5: Git push
            push_result = subprocess.run(
                ["git", "push"],
                cwd=self.repo_root,
                check=True,
                capture_output=True,
                text=True
            )
            
            # Success!
            result["ok"] = True
            result["commit_sha"] = commit_sha
            result["commit_message"] = commit_message
            
        except subprocess.CalledProcessError as e:
            result["error"] = f"Git operation failed: {e.stderr if e.stderr else str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"
        
        return result


# Convenience function for simple usage
def update_ssot_document(
    target: str,
    content: str,
    commit_message: Optional[str] = None
) -> Dict:
    """
    Convenience function to update an SSOT document.
    
    Args:
        target: Target identifier ("system_snapshot", "capabilities_matrix", "decisions")
        content: New full content for the document
        commit_message: Optional custom commit message
    
    Returns:
        Dict with update results (see SSOTWriter.update_ssot for details)
    
    Example:
        result = update_ssot_document(
            target="system_snapshot",
            content="# New content..."
        )
        if result["ok"]:
            print(f"Updated! Commit: {result['commit_sha']}")
    """
    writer = SSOTWriter()
    return writer.update_ssot(
        target=target,
        mode="replace_full",
        content=content,
        commit_message=commit_message
    )


if __name__ == "__main__":
    # Quick test
    print("SSOT Writer Module")
    print("=" * 60)
    print("\nValid targets:")
    for target, path in VALID_TARGETS.items():
        print(f"  - {target}: {path}")
    print("\n" + "=" * 60)
