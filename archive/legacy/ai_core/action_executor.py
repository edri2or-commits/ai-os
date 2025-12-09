"""
Action Executor v1.0 - Execute validated actions from Intent Router

This module executes structured Actions from GPT Planner after validation.
Supports file operations and git operations via MCP tools.

Status: IMPLEMENTED v1.0
- Executes: file.create, file.update, git.commit, git.push
- Respects approval (auto vs manual)
- Full error handling and reporting
"""

import os
from pathlib import Path
from typing import Dict, Any, List


# Repository root (where .git lives)
REPO_ROOT = Path(__file__).resolve().parents[1]


def execute_file_create(action: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute file.create action.
    
    Args:
        action: {
            "type": "file.create",
            "params": {"path": "...", "content": "..."},
            "approval": "auto",
            "description": "..."
        }
    
    Returns:
        {"success": bool, "message": str, "details": {...}}
    """
    try:
        params = action["params"]
        file_path = REPO_ROOT / params["path"]
        content = params["content"]
        
        # Ensure parent directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        file_path.write_text(content, encoding="utf-8")
        
        return {
            "success": True,
            "message": f"Created: {params['path']}",
            "details": {
                "path": str(file_path),
                "size": len(content)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to create {params['path']}: {str(e)}",
            "details": {"error": str(e)}
        }


def execute_file_update(action: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute file.update action.
    
    Args:
        action: {
            "type": "file.update",
            "params": {
                "path": "...",
                "edits": [{"old_text": "...", "new_text": "..."}, ...]
            },
            "approval": "auto",
            "description": "..."
        }
    
    Returns:
        {"success": bool, "message": str, "details": {...}}
    """
    try:
        params = action["params"]
        file_path = REPO_ROOT / params["path"]
        
        if not file_path.exists():
            return {
                "success": False,
                "message": f"File not found: {params['path']}",
                "details": {"error": "File does not exist"}
            }
        
        # Read current content
        content = file_path.read_text(encoding="utf-8")
        original_content = content
        
        # Apply edits
        edits_applied = 0
        for edit in params["edits"]:
            old_text = edit["old_text"]
            new_text = edit["new_text"]
            
            if old_text in content:
                # Check that old_text appears exactly once
                count = content.count(old_text)
                if count != 1:
                    return {
                        "success": False,
                        "message": f"old_text appears {count} times (must be exactly 1): {old_text[:50]}...",
                        "details": {"error": f"Ambiguous edit: {count} matches"}
                    }
                
                content = content.replace(old_text, new_text)
                edits_applied += 1
            else:
                return {
                    "success": False,
                    "message": f"old_text not found in file: {old_text[:50]}...",
                    "details": {"error": "Text not found"}
                }
        
        # Write updated content
        file_path.write_text(content, encoding="utf-8")
        
        return {
            "success": True,
            "message": f"Updated: {params['path']} ({edits_applied} edits)",
            "details": {
                "path": str(file_path),
                "edits_applied": edits_applied,
                "size_before": len(original_content),
                "size_after": len(content)
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update {params['path']}: {str(e)}",
            "details": {"error": str(e)}
        }


def execute_git_commit(action: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute git.commit action.
    
    Args:
        action: {
            "type": "git.commit",
            "params": {"files": [...], "message": "..."},
            "approval": "auto",
            "description": "..."
        }
    
    Returns:
        {"success": bool, "message": str, "details": {...}}
    """
    try:
        params = action["params"]
        files = params["files"]
        message = params["message"]
        
        # Build git command
        files_str = " ".join(f'"{f}"' for f in files)
        git_add_cmd = f'cd "{REPO_ROOT}" && git add {files_str}'
        git_commit_cmd = f'cd "{REPO_ROOT}" && git commit -m "{message}"'
        
        # Execute git add
        import subprocess
        add_result = subprocess.run(
            git_add_cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if add_result.returncode != 0:
            return {
                "success": False,
                "message": f"git add failed: {add_result.stderr}",
                "details": {"error": add_result.stderr}
            }
        
        # Execute git commit
        commit_result = subprocess.run(
            git_commit_cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if commit_result.returncode != 0:
            return {
                "success": False,
                "message": f"git commit failed: {commit_result.stderr}",
                "details": {"error": commit_result.stderr}
            }
        
        return {
            "success": True,
            "message": f"Committed: {message}",
            "details": {
                "files": files,
                "message": message,
                "output": commit_result.stdout
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to commit: {str(e)}",
            "details": {"error": str(e)}
        }


def execute_git_push(action: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute git.push action.
    
    Args:
        action: {
            "type": "git.push",
            "params": {},
            "approval": "auto",
            "description": "..."
        }
    
    Returns:
        {"success": bool, "message": str, "details": {...}}
    """
    try:
        git_push_cmd = f'cd "{REPO_ROOT}" && git push'
        
        import subprocess
        push_result = subprocess.run(
            git_push_cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if push_result.returncode != 0:
            return {
                "success": False,
                "message": f"git push failed: {push_result.stderr}",
                "details": {"error": push_result.stderr}
            }
        
        return {
            "success": True,
            "message": "Pushed to GitHub",
            "details": {
                "output": push_result.stdout + push_result.stderr
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to push: {str(e)}",
            "details": {"error": str(e)}
        }


# Action type → executor function mapping
ACTION_EXECUTORS = {
    "file.create": execute_file_create,
    "file.update": execute_file_update,
    "git.commit": execute_git_commit,
    "git.push": execute_git_push,
}


def execute_actions(actions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Execute a list of validated actions from Intent Router.
    
    Args:
        actions: List of action dicts from Intent Router's actions_for_claude
                Each action must have: type, params, approval, description
    
    Returns:
        {
            "executed_actions": List[Dict],  # Actions that were executed
            "pending_approval": List[Dict],  # Actions waiting for manual approval
            "errors": List[Dict],            # Actions that failed
            "summary": {
                "total": int,
                "executed": int,
                "pending": int,
                "failed": int
            }
        }
    
    Example:
        >>> actions = [
        >>>     {
        >>>         "type": "file.create",
        >>>         "params": {"path": "test.md", "content": "# Test"},
        >>>         "approval": "auto",
        >>>         "description": "Create test file"
        >>>     }
        >>> ]
        >>> result = execute_actions(actions)
        >>> print(result["summary"])
        {"total": 1, "executed": 1, "pending": 0, "failed": 0}
    """
    executed = []
    pending = []
    errors = []
    
    for i, action in enumerate(actions, 1):
        action_type = action.get("type")
        approval = action.get("approval", "manual")
        description = action.get("description", "No description")
        
        # Check if manual approval needed
        if approval == "manual":
            pending.append({
                "action_index": i,
                "action": action,
                "reason": "Requires manual approval"
            })
            continue
        
        # Check if we have an executor for this type
        if action_type not in ACTION_EXECUTORS:
            errors.append({
                "action_index": i,
                "action": action,
                "error": f"Action type '{action_type}' not implemented yet"
            })
            continue
        
        # Execute action
        try:
            executor = ACTION_EXECUTORS[action_type]
            result = executor(action)
            
            if result["success"]:
                executed.append({
                    "action_index": i,
                    "action": action,
                    "result": result
                })
            else:
                errors.append({
                    "action_index": i,
                    "action": action,
                    "error": result["message"],
                    "details": result.get("details", {})
                })
        except Exception as e:
            errors.append({
                "action_index": i,
                "action": action,
                "error": f"Unexpected error: {str(e)}"
            })
    
    return {
        "executed_actions": executed,
        "pending_approval": pending,
        "errors": errors,
        "summary": {
            "total": len(actions),
            "executed": len(executed),
            "pending": len(pending),
            "failed": len(errors)
        }
    }


if __name__ == "__main__":
    import sys
    import json
    
    # Fix encoding for Windows console
    if sys.platform == 'win32':
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    
    # Simple smoke test
    print("Action Executor v1.0 - Smoke Test")
    print("=" * 50)
    
    test_actions = [
        {
            "type": "file.create",
            "params": {
                "path": "docs/TEST_ACTION_EXECUTOR.md",
                "content": "# Action Executor Test\n\nThis file was created by action_executor.py smoke test.\n\n**Status**: ✅ Working!\n"
            },
            "approval": "auto",
            "description": "Create test file for executor"
        }
    ]
    
    print("\nExecuting test actions...")
    result = execute_actions(test_actions)
    
    print(f"\n✅ Execution complete!")
    print(json.dumps(result, ensure_ascii=False, indent=2))
