import requests
import json

url = "http://localhost:8082/google/gmail/send"
payload = {
    "to": ["edri2or@gmail.com"],
    "subject": "H1 Test - Headless Migration POC",
    "body": "This email was sent by Python requests without Claude Desktop.\n\nTimestamp: 2025-12-05 22:48\nTest: H1 Gmail REST API Verification",
    "is_html": False
}

response = requests.post(url, json=payload)
print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
