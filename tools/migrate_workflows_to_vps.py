"""
Export workflows from local n8n and import to VPS n8n.
Uses the new VPS API key provided by user.
"""
import requests
import json

# Configuration
LOCAL_URL = 'http://localhost:5678/api/v1'
LOCAL_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYWQwNDlhYi0xNDIxLTRlY2YtYTdkOC0zZGVjMzAwMjI5MGMiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY0NzI2NDI3LCJleHAiOjE3NjcyNDM2MDB9.sX8wz2BiqnCYHExCjsLqUmXB8d-ZAdioOXEjvY5E2io'

VPS_URL = 'https://n8n.35.223.68.23.nip.io/api/v1'
VPS_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZDkzZjUzZC0wYmU1LTRjNzUtYmZiOS1mNDUwOTNmM2NhYzEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY1MDU4NjAwLCJleHAiOjE3Njc2NTA0MDB9.PG_jISgSnSwoy21dJFR7pkM6qpQ9EzngcI2EaRnAoVQ'

# Workflows to import (critical ones)
WORKFLOWS_TO_IMPORT = [
    'Au6xiDyk8Zjn8Px7',  # Judge Agent V2 - Active
    'wYIM8Rd0o0O02BEc',  # Observer - Drift Detection
    '3CBsD70avEmYwuA3',  # Email Watcher
]

def export_workflow(workflow_id, api_key, base_url):
    """Export workflow from n8n instance."""
    url = f'{base_url}/workflows/{workflow_id}'
    headers = {'X-N8N-API-KEY': api_key}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error exporting {workflow_id}: {response.status_code}')
        return None

def import_workflow(workflow_data, api_key, base_url):
    """Import workflow to n8n instance."""
    url = f'{base_url}/workflows'
    headers = {
        'X-N8N-API-KEY': api_key,
        'Content-Type': 'application/json'
    }
    
    # Clean workflow data - keep only fields needed for import
    # Remove all metadata fields that n8n adds automatically
    workflow_clean = {
        'name': workflow_data.get('name'),
        'nodes': workflow_data.get('nodes', []),
        'connections': workflow_data.get('connections', {}),
        'settings': workflow_data.get('settings', {}),
        'staticData': workflow_data.get('staticData'),
    }
    
    # Remove None values
    workflow_clean = {k: v for k, v in workflow_clean.items() if v is not None}
    
    response = requests.post(url, headers=headers, json=workflow_clean)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f'Error importing workflow: {response.status_code}')
        print(response.text)
        return None

def activate_workflow(workflow_id, api_key, base_url):
    """Activate workflow in n8n."""
    url = f'{base_url}/workflows/{workflow_id}/activate'
    headers = {'X-N8N-API-KEY': api_key}
    
    response = requests.patch(url, headers=headers)
    if response.status_code == 200:
        return True
    else:
        print(f'Error activating {workflow_id}: {response.status_code}')
        return False

def main():
    print('=== WORKFLOW MIGRATION: LOCAL -> VPS ===\n')
    
    results = []
    
    for wf_id in WORKFLOWS_TO_IMPORT:
        print(f'Processing workflow {wf_id}...')
        
        # Step 1: Export from local
        print('  [1/3] Exporting from local n8n...')
        workflow_data = export_workflow(wf_id, LOCAL_API_KEY, LOCAL_URL)
        
        if not workflow_data:
            print(f'  [FAILED] Could not export {wf_id}')
            results.append({'id': wf_id, 'status': 'FAILED_EXPORT'})
            continue
        
        workflow_name = workflow_data.get('name', 'Unknown')
        print(f'  [OK] Exported: {workflow_name}')
        
        # Step 2: Import to VPS
        print('  [2/3] Importing to VPS n8n...')
        imported = import_workflow(workflow_data, VPS_API_KEY, VPS_URL)
        
        if not imported:
            print(f'  [FAILED] Could not import {workflow_name}')
            results.append({'id': wf_id, 'name': workflow_name, 'status': 'FAILED_IMPORT'})
            continue
        
        new_id = imported.get('id')
        print(f'  [OK] Imported with new ID: {new_id}')
        
        # Step 3: Activate if original was active
        was_active = workflow_data.get('active', False)
        if was_active:
            print('  [3/3] Activating workflow...')
            activated = activate_workflow(new_id, VPS_API_KEY, VPS_URL)
            if activated:
                print('  [OK] Activated successfully')
                results.append({
                    'id': wf_id,
                    'name': workflow_name,
                    'new_id': new_id,
                    'status': 'IMPORTED_ACTIVE'
                })
            else:
                print('  [WARNING] Imported but activation failed')
                results.append({
                    'id': wf_id,
                    'name': workflow_name,
                    'new_id': new_id,
                    'status': 'IMPORTED_INACTIVE'
                })
        else:
            print('  [3/3] Left inactive (original was inactive)')
            results.append({
                'id': wf_id,
                'name': workflow_name,
                'new_id': new_id,
                'status': 'IMPORTED_INACTIVE'
            })
        
        print()
    
    # Summary
    print('\n=== MIGRATION SUMMARY ===\n')
    for r in results:
        status_icon = '[OK]' if 'IMPORTED' in r['status'] else '[FAIL]'
        print(f'{status_icon} {r.get("name", "Unknown")} - {r["status"]}')
        if 'new_id' in r:
            print(f'      VPS ID: {r["new_id"]}')
    
    # Save results
    with open('migration_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print('\nResults saved to migration_results.json')

if __name__ == '__main__':
    main()
