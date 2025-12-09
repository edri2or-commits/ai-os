#!/usr/bin/env python3
"""
MCP Inspector - Tool for checking connected MCP servers

Usage:
    python mcp_inspector.py [--verbose]

Reads Claude Desktop config and reports on MCP server status.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

def get_config_path() -> Optional[Path]:
    """
    Find Claude Desktop config file.
    
    Returns:
        Path to config file or None if not found
    """
    # Windows: %APPDATA%\Claude\claude_desktop_config.json
    appdata = Path.home() / "AppData" / "Roaming" / "Claude"
    config_path = appdata / "claude_desktop_config.json"
    
    if config_path.exists():
        return config_path
    
    return None

def load_config(config_path: Path) -> Optional[Dict]:
    """
    Load and parse Claude Desktop config.
    
    Args:
        config_path: Path to config file
        
    Returns:
        Parsed config dict or None if error
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading config: {e}", file=sys.stderr)
        return None

def check_server(name: str, config: Dict, verbose: bool = False) -> Dict:
    """
    Check status of an MCP server.
    
    Args:
        name: Server name
        config: Server config dict
        verbose: Show detailed info
        
    Returns:
        Status dict with server info
    """
    status = {
        "name": name,
        "command": config.get("command", "N/A"),
        "args": config.get("args", []),
        "env": config.get("env", {}),
        "status": "configured"  # Basic check - just sees if it's in config
    }
    
    # Check if command exists (basic validation)
    command = status["command"]
    if command == "N/A":
        status["status"] = "error: no command"
    elif not Path(command).exists() and not command.startswith("npx"):
        # npx downloads on-demand, so we can't check if it exists
        status["status"] = "warning: command not found"
    
    return status

def inspect_servers(verbose: bool = False) -> int:
    """
    Main inspection logic.
    
    Args:
        verbose: Show detailed info
        
    Returns:
        Exit code (0 = success)
    """
    # Find config
    config_path = get_config_path()
    if not config_path:
        print("[ERROR] Could not find Claude Desktop config file")
        print("Expected location: %APPDATA%\\Claude\\claude_desktop_config.json")
        return 1
    
    if verbose:
        print(f"[INFO] Config found: {config_path}")
    
    # Load config
    config = load_config(config_path)
    if not config:
        return 1
    
    # Extract MCP servers
    mcp_servers = config.get("mcpServers", {})
    if not mcp_servers:
        print("[WARN] No MCP servers configured")
        return 0
    
    # Inspect each server
    print(f"\n{'='*60}")
    print(f"MCP Inspector - Found {len(mcp_servers)} server(s)")
    print(f"{'='*60}\n")
    
    for name, server_config in mcp_servers.items():
        status = check_server(name, server_config, verbose)
        
        # Print server info
        print(f"[SERVER] {status['name']}")
        print(f"  Status:  {status['status']}")
        print(f"  Command: {status['command']}")
        
        if verbose:
            if status['args']:
                print(f"  Args:    {' '.join(status['args'])}")
            if status['env']:
                print(f"  Env:     {len(status['env'])} variable(s)")
        
        print()
    
    print(f"{'='*60}")
    print(f"[OK] Inspection complete")
    print(f"{'='*60}\n")
    
    return 0

def main():
    """Entry point."""
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    
    try:
        return inspect_servers(verbose)
    except KeyboardInterrupt:
        print("\n[CANCELLED]")
        return 130

if __name__ == "__main__":
    sys.exit(main())
