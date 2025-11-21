"""
AI-OS - Smart start script for Chat1 without multiprocessing complications
"""

import sys
import subprocess
from pathlib import Path

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

project_root = Path(__file__).parent

print("=" * 70)
print("Starting Chat1 (Telegram Bot) + Agent Gateway")
print("=" * 70)
print()

# Start Server
print("🚀 Starting Agent Gateway Server...")
server = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "ai_core.agent_gateway_server:app", "--host", "0.0.0.0", "--port", "8000"],
    cwd=project_root
)

# Wait a bit
import time
time.sleep(3)

# Start Telegram Bot
print("🤖 Starting Telegram Bot...")
bot = subprocess.Popen(
    [sys.executable, "chat/telegram_bot.py"],
    cwd=project_root
)

print()
print("=" * 70)
print("✅ Both processes running!")
print("=" * 70)
print()
print("📍 Server: http://localhost:8000")
print("🤖 Telegram: Active (send /start to bot)")
print()
print("⏸️  Press CTRL+C to stop both")
print()

try:
    server.wait()
except KeyboardInterrupt:
    print("\n\n🛑 Stopping...")
    server.terminate()
    bot.terminate()
    print("✅ Stopped")
