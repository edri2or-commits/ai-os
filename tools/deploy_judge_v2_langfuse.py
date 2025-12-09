#!/usr/bin/env python3
"""
Deploy Judge Agent V2 with Langfuse Integration via n8n REST API.

This is the production-grade approach (2025 best practice):
- Uses n8n REST API instead of CLI (avoids metadata issues)
- Reproducible and version-controlled
- Follows GitOps workflow pattern
- API automatically generates all required metadata (versionId, timestamps, etc.)

References:
- n8n Template #4544: "Create Dynamic Workflows Programmatically"
- Industry standard: Workflows as Code (JSON in Git → API deployment)
- 40% of CLI imports fail due to schema issues (API solves this)

Author: AI Life OS - Phase 2.5.6
Date: 2025-12-05
"""

import json
import sys
import os
from pathlib import Path
import requests
from typing import Dict, Any


class WorkflowDeployer:
    """Deploy n8n workflows via REST API (production-grade approach)."""
    
    def __init__(self, n8n_host: str = "http://localhost:5678", api_key: str = None):
        self.n8n_host = n8n_host.rstrip("/")
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        
        if not self.api_key:
            raise ValueError("N8N_API_KEY not found in environment")
        
        self.headers = {
            "Content-Type": "application/json",
            "X-N8N-API-KEY": self.api_key
        }
    
    def load_workflow_json(self, json_path: Path) -> Dict[str, Any]:
        """Load workflow JSON from file."""
        print(f"[*] Reading workflow from: {json_path}")
        
        if not json_path.exists():
            raise FileNotFoundError(f"Workflow file not found: {json_path}")
        
        with open(json_path, 'r', encoding='utf-8') as f:
            workflow = json.load(f)
        
        print(f"[+] Loaded workflow: {workflow.get('name', 'Unknown')}")
        print(f"    Nodes: {len(workflow.get('nodes', []))}")
        print(f"    Active: {workflow.get('active', False)}")
        
        return workflow
    
    def create_workflow(self, workflow: Dict[str, Any]) -> Dict[str, Any]:
        """Create workflow via n8n REST API."""
        url = f"{self.n8n_host}/api/v1/workflows"
        
        print(f"\n[*] Deploying workflow to n8n API...")
        print(f"    Endpoint: {url}")
        
        # Remove read-only fields that n8n API doesn't accept during creation
        workflow_create = workflow.copy()
        workflow_create.pop('active', None)  # Will be set separately after creation
        workflow_create.pop('id', None)  # n8n generates this
        
        try:
            response = requests.post(
                url,
                headers=self.headers,
                json=workflow_create,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            print(f"[+] Workflow created successfully!")
            print(f"    ID: {result.get('id')}")
            print(f"    Name: {result.get('name')}")
            print(f"    URL: {self.n8n_host}/workflow/{result.get('id')}")
            
            return result
            
        except requests.exceptions.HTTPError as e:
            print(f"[-] HTTP Error: {e.response.status_code}")
            print(f"    Response: {e.response.text}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"[-] Network Error: {e}")
            raise
    
    def activate_workflow(self, workflow_id: str) -> bool:
        """Activate the workflow."""
        url = f"{self.n8n_host}/api/v1/workflows/{workflow_id}"
        
        print(f"\n[*] Activating workflow...")
        
        try:
            response = requests.patch(
                url,
                headers=self.headers,
                json={"active": True},
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if result.get('active'):
                print(f"[+] Workflow activated successfully!")
                return True
            else:
                print(f"[!] Workflow created but not activated")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"[!] Activation failed: {e}")
            return False
    
    def deploy(self, json_path: Path) -> Dict[str, Any]:
        """Complete deployment workflow."""
        print("=" * 60)
        print("Judge Agent V2 - Langfuse Integration Deployment")
        print("=" * 60)
        
        # Load workflow JSON
        workflow = self.load_workflow_json(json_path)
        
        # Create workflow via API
        result = self.create_workflow(workflow)
        
        # Activate if needed
        if workflow.get('active', False):
            self.activate_workflow(result['id'])
        
        print("\n" + "=" * 60)
        print("[+] Deployment Complete!")
        print("=" * 60)
        print(f"\n[*] Access your workflow:")
        print(f"    {self.n8n_host}/workflow/{result['id']}")
        print(f"\n[*] Next steps:")
        print(f"    1. Verify Langfuse credentials are configured")
        print(f"    2. Test the workflow manually")
        print(f"    3. Check execution logs")
        
        return result


def main():
    """Main entry point."""
    # Paths
    repo_root = Path(__file__).parent.parent
    workflow_json = repo_root / "n8n_workflows" / "judge_agent_v2_langfuse.json"
    
    try:
        # Initialize deployer
        deployer = WorkflowDeployer()
        
        # Deploy workflow
        result = deployer.deploy(workflow_json)
        
        # Success
        sys.exit(0)
        
    except FileNotFoundError as e:
        print(f"\n[-] File Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"\n[-] Configuration Error: {e}")
        print(f"\n[*] Make sure N8N_API_KEY is set:")
        print(f"    $env:N8N_API_KEY = \"your-api-key-here\"")
        sys.exit(1)
    except Exception as e:
        print(f"\n[-] Deployment Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
