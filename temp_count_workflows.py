import json

with open(r'C:\Users\edri2\Desktop\AI\ai-os\exports\workflows_local_backup_20251206_233656.json', encoding='utf-8') as f:
    data = json.load(f)

print(f'Total workflows: {len(data)}\n')
for i, w in enumerate(data):
    print(f'{i+1}. {w["name"]} (active={w["active"]})')
