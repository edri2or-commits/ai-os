"""
Debug OS Core MCP - print all registered routes
"""
import sys
sys.path.insert(0, r"C:\Users\edri2\Desktop\AI\ai-os\services\os_core_mcp")

from server import app

print("Registered routes:")
for route in app.routes:
    print(f"  {route.methods} {route.path}")
