import requests
import json

headers = {"Authorization": "Bearer sk-litellm-ailifeos-2025"}
response = requests.get("http://localhost:4000/health", headers=headers)
print(json.dumps(response.json(), indent=2))
