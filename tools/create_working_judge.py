"""
Create working Judge V2 with properly escaped prompt
"""
import requests
import json
from pathlib import Path

# Read files
env_path = Path(__file__).parent.parent / "infra" / "n8n" / ".env"
api_key = None
for line in env_path.read_text().split('\n'):
    if line.startswith('N8N_API_KEY='):
        api_key = line.split('=', 1)[1].strip()
        break

cred_id = (Path(__file__).parent / "langfuse_cred_id.txt").read_text().strip()
prompt_text = (Path(__file__).parent.parent / "prompts" / "judge_agent_prompt.md").read_text()

# Escape for JavaScript - use JSON encoding
prompt_json = json.dumps(prompt_text)

# Build workflow
workflow = {
    "name": "Judge Agent V2 - Working",
    "settings": {
        "executionOrder": "v1"
    },
    "nodes": [
        {
            "parameters": {
                "rule": {
                    "interval": [{"field": "hours", "hoursInterval": 6}]
                }
            },
            "name": "Schedule Trigger",
            "type": "n8n-nodes-base.scheduleTrigger",
            "typeVersion": 1,
            "position": [250, 300],
            "id": "1"
        },
        {
            "parameters": {
                "method": "GET",
                "url": "http://host.docker.internal:3000/api/public/traces",
                "authentication": "genericCredentialType",
                "genericAuthType": "httpBasicAuth",
                "sendQuery": True,
                "queryParameters": {
                    "parameters": [
                        {"name": "page", "value": "1"},
                        {"name": "limit", "value": "100"},
                        {"name": "fromTimestamp", "value": "={{new Date(Date.now() - 6 * 60 * 60 * 1000).toISOString()}}"}
                    ]
                }
            },
            "name": "Fetch Traces",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4,
            "position": [450, 300],
            "id": "2",
            "credentials": {
                "httpBasicAuth": {"id": cred_id, "name": "Langfuse API"}
            }
        },
        {
            "parameters": {
                "mode": "runOnceForAllItems",
                "jsCode": f"""
const traces = $input.first().json.data || [];
const promptText = {prompt_json};

const events = traces.map(t => ({{
  trace_id: t.id,
  name: t.name,
  timestamp: t.timestamp,
  status: t.status,
  input: t.input,
  output: t.output
}}));

const fullPrompt = promptText + '\\n\\n## Events:\\n\\n```json\\n' + JSON.stringify(events, null, 2) + '\\n```';

return [{{json: {{prompt: fullPrompt, events_count: events.length}}}}];
"""
            },
            "name": "Prepare Prompt",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [650, 300],
            "id": "3"
        },
        {
            "parameters": {
                "method": "POST",
                "url": "https://api.openai.com/v1/chat/completions",
                "sendHeaders": True,
                "headerParameters": {
                    "parameters": [
                        {"name": "Authorization", "value": "=Bearer {{$env.OPENAI_API_KEY}}"},
                        {"name": "Content-Type", "value": "application/json"}
                    ]
                },
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {"name": "model", "value": "gpt-4o"},
                        {"name": "messages", "value": "=[{\"role\": \"user\", \"content\": $json.prompt}]"},
                        {"name": "temperature", "value": "0.2"}
                    ]
                }
            },
            "name": "Call GPT",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4,
            "position": [850, 300],
            "id": "4"
        },
        {
            "parameters": {
                "mode": "runOnceForAllItems",
                "jsCode": """
const response = $input.first().json.choices[0].message.content;
console.log('Judge Report:', response);
return [{json: {report: response, timestamp: new Date().toISOString()}}];
"""
            },
            "name": "Log Report",
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [1050, 300],
            "id": "5"
        }
    ],
    "connections": {
        "Schedule Trigger": {"main": [[{"node": "Fetch Traces", "type": "main", "index": 0}]]},
        "Fetch Traces": {"main": [[{"node": "Prepare Prompt", "type": "main", "index": 0}]]},
        "Prepare Prompt": {"main": [[{"node": "Call GPT", "type": "main", "index": 0}]]},
        "Call GPT": {"main": [[{"node": "Log Report", "type": "main", "index": 0}]]}
    }
}

# Delete old workflow
print("[1] Deleting old workflow...")
requests.delete(
    "http://localhost:5678/api/v1/workflows/cJVkH8vMkTLkN875",
    headers={"X-N8N-API-KEY": api_key}
)

# Import new
print("[2] Importing fixed workflow...")
r = requests.post(
    "http://localhost:5678/api/v1/workflows",
    headers={"X-N8N-API-KEY": api_key, "Content-Type": "application/json"},
    json=workflow
)

if r.status_code in [200, 201]:
    new_id = r.json()['id']
    print(f"SUCCESS - ID: {new_id}")
    (Path(__file__).parent / "judge_workflow_id.txt").write_text(new_id)
    print(f"URL: http://localhost:5678/workflow/{new_id}")
    print("\nIMPORTANT: Activate manually in UI (toggle Active)")
else:
    print(f"FAILED: {r.status_code}")
    print(r.text)
