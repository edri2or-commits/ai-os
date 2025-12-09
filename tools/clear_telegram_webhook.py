"""Clear Telegram Bot webhook to fix conflict."""
import os
from dotenv import load_dotenv
import requests

# Load env
load_dotenv(r"C:\Users\edri2\Desktop\AI\ai-os\services\approval-bot\.env")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    print("ERROR: TELEGRAM_BOT_TOKEN not found")
    exit(1)

print(f"Token found: {TOKEN[:20]}...")

# Delete webhook (fixes conflict)
url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
response = requests.post(url, json={"drop_pending_updates": True})

if response.status_code == 200:
    print("Webhook cleared successfully!")
    print(f"Response: {response.json()}")
else:
    print(f"ERROR: {response.status_code}")
    print(response.text)
