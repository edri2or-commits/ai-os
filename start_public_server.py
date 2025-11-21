"""
Start Agent Gateway Server with Cloudflare Tunnel

This script:
1. Starts the FastAPI server on localhost:8000
2. Creates a Cloudflare Quick Tunnel to expose it publicly
3. Prints the public URL
"""

import subprocess
import time
import sys
import re
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

print("=" * 70)
print("AI-OS Agent Gateway - Public HTTPS Server")
print("=" * 70)

# Step 1: Start FastAPI server in background
print("\n🚀 Starting FastAPI server on localhost:8000...")

server_process = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "ai_core.agent_gateway_server:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=Path(__file__).parent,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Wait for server to start
print("⏳ Waiting for server to initialize...")
time.sleep(3)

# Step 2: Start Cloudflare Tunnel
print("\n🌐 Creating Cloudflare Quick Tunnel...")
print("⏳ This may take 10-15 seconds...")

tunnel_process = subprocess.Popen(
    ["cloudflared", "tunnel", "--url", "http://localhost:8000"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
    bufsize=1
)

# Parse output to find public URL
public_url = None
print("\n📡 Tunnel starting...")

try:
    for line in tunnel_process.stderr:
        print(f"   {line.strip()}")
        
        # Look for the public URL
        if "https://" in line and ".trycloudflare.com" in line:
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
            if match:
                public_url = match.group(0)
                break
        
        # Stop after finding URL or timeout
        if public_url:
            break

    if public_url:
        print("\n" + "=" * 70)
        print("✅ PUBLIC HTTPS URL READY!")
        print("=" * 70)
        print(f"\n🌐 Public URL: {public_url}")
        print(f"\n📍 API Endpoint: {public_url}/api/v1/intent")
        print(f"\n📖 Docs: {public_url}/docs")
        print(f"\n🔒 HTTPS: Yes (Cloudflare)")
        print("\n" + "=" * 70)
        print("\n⚠️  Keep this window open to maintain the tunnel!")
        print("⏸️  Press CTRL+C to stop both server and tunnel")
        print("\n" + "=" * 70)
        
        # Keep both processes running
        try:
            tunnel_process.wait()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping server and tunnel...")
            server_process.terminate()
            tunnel_process.terminate()
            print("✅ Stopped")
    else:
        print("\n❌ Could not find public URL in tunnel output")
        server_process.terminate()
        tunnel_process.terminate()

except Exception as e:
    print(f"\n❌ Error: {e}")
    server_process.terminate()
    tunnel_process.terminate()
