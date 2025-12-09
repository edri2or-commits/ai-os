import requests
import json
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("ANTHROPIC_API_KEY")

print(f"[KEY] Testing API Key: {api_key[:20]}...")

response = requests.post(
    "https://api.anthropic.com/v1/messages",
    headers={
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    },
    json={
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 32,
        "messages": [{"role": "user", "content": "Say: API works!"}]
    }
)

print(f"[STATUS] Status Code: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    message = data["content"][0]["text"]
    print(f"[OK] SUCCESS! Claude says: {message}")
else:
    print(f"[ERROR] {response.text}")
