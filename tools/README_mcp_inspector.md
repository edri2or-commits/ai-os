# MCP Inspector

Quick tool to check which MCP servers are configured in Claude Desktop.

## Usage

```bash
python tools/mcp_inspector.py [--verbose]
```

## What it does

- Reads `%APPDATA%\Claude\claude_desktop_config.json`
- Lists all configured MCP servers
- Shows command, args, and env variables (with --verbose)

## Output Example

```
[SERVER] google-mcp
  Status:  configured
  Command: C:\Users\edri2\.bun\bin\google-mcp.exe
  Env:     3 variable(s)
```

## Use Cases

- **Before debugging:** Check which servers are actually configured
- **After config changes:** Verify new servers were added correctly
- **Troubleshooting:** See full command + args for each server

## Exit Codes

- `0` - Success
- `1` - Error (config not found or parse error)
- `130` - Cancelled (Ctrl+C)

## Notes

- Read-only tool (never modifies config)
- Windows-specific (uses %APPDATA% path)
- No dependencies (uses stdlib only)

---

**Created:** 2025-12-02  
**Part of:** VAL-1b validation slice
