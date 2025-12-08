import requests
import json

headers = {
    "Authorization": "Bearer sk-litellm-ailifeos-2025",
    "Content-Type": "application/json"
}

with open("test-gemini-25.json") as f:
    data = json.load(f)

response = requests.post("http://localhost:4000/v1/chat/completions", headers=headers, json=data)
result = response.json()

print("Status:", response.status_code)
print("\nResponse:")
if "choices" in result:
    print(result["choices"][0]["message"]["content"])
    print(f"\nTokens: {result['usage']['total_tokens']}")
else:
    print(json.dumps(result, indent=2))
