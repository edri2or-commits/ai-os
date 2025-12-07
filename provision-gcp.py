#!/usr/bin/env python3
"""
Google Cloud VPS Provisioning Script
Automates VM creation via Google Compute Engine API
"""

import json
import time
from google.oauth2 import service_account
from googleapiclient import discovery
from googleapiclient.errors import HttpError

# Configuration
GCP_KEY_PATH = r"C:\Users\edri2\Desktop\AI\ai-os\edri2or-mcp-dd7014777518.json"
SSH_PUBLIC_KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMgH3/5hc4lFOXlyCf59YArE22Bq5W5axftLxYOlH+Hj edri2or@gmail.com"

# VM Configuration
VM_CONFIG = {
    "name": "ai-life-os-prod",
    "machine_type": "e2-medium",  # 2 vCPU, 4GB RAM (~$24/mo)
    "zone": "us-central1-a",  # Iowa - cheapest region
    "image_project": "ubuntu-os-cloud",
    "image_family": "ubuntu-2404-lts-amd64",
    "disk_size_gb": 80,
    "tags": ["ai-os", "http-server", "https-server"]
}

def create_compute_client():
    """Create authenticated Compute Engine client"""
    credentials = service_account.Credentials.from_service_account_file(
        GCP_KEY_PATH,
        scopes=['https://www.googleapis.com/auth/compute']
    )
    return discovery.build('compute', 'v1', credentials=credentials)

def get_image_url(compute, project, family):
    """Get the latest image URL for a family"""
    result = compute.images().getFromFamily(
        project=project,
        family=family
    ).execute()
    return result['selfLink']

def create_instance(compute, project, zone, name, machine_type, image_url, ssh_key):
    """Create a VM instance"""
    print(f"Creating VM: {name}")
    print(f"   Type: {machine_type}")
    print(f"   Zone: {zone}")
    
    config = {
        'name': name,
        'machineType': f"zones/{zone}/machineTypes/{machine_type}",
        'disks': [{
            'boot': True,
            'autoDelete': True,
            'initializeParams': {
                'sourceImage': image_url,
                'diskSizeGb': VM_CONFIG['disk_size_gb']
            }
        }],
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [{
                'type': 'ONE_TO_ONE_NAT',
                'name': 'External NAT'
            }]
        }],
        'metadata': {
            'items': [{
                'key': 'ssh-keys',
                'value': f"root:{ssh_key}"
            }]
        },
        'tags': {
            'items': VM_CONFIG['tags']
        }
    }
    
    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config
    ).execute()

def wait_for_operation(compute, project, zone, operation):
    """Wait for a zone operation to complete"""
    print("Waiting for VM to start...")
    
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation
        ).execute()
        
        status = result['status']
        if status == 'DONE':
            if 'error' in result:
                raise Exception(result['error'])
            print("VM is running!")
            return result
        
        print(f"   Status: {status}")
        time.sleep(5)

def get_instance_info(compute, project, zone, name):
    """Get instance details including external IP"""
    result = compute.instances().get(
        project=project,
        zone=zone,
        instance=name
    ).execute()
    
    external_ip = result['networkInterfaces'][0]['accessConfigs'][0]['natIP']
    internal_ip = result['networkInterfaces'][0]['networkIP']
    
    return {
        'name': result['name'],
        'external_ip': external_ip,
        'internal_ip': internal_ip,
        'machine_type': result['machineType'].split('/')[-1],
        'status': result['status']
    }

def main():
    """Main provisioning workflow"""
    print("=" * 60)
    print("Google Cloud VPS Provisioning")
    print("=" * 60)
    
    try:
        # Load credentials
        with open(GCP_KEY_PATH) as f:
            creds = json.load(f)
            project = creds['project_id']
        
        print(f"Project: {project}")
        print(f"Zone: {VM_CONFIG['zone']}")
        
        # Create compute client
        compute = create_compute_client()
        
        # Get latest Ubuntu image
        print("Finding latest Ubuntu 24.04 image...")
        image_url = get_image_url(
            compute,
            VM_CONFIG['image_project'],
            VM_CONFIG['image_family']
        )
        print(f"Image: {VM_CONFIG['image_family']}")
        
        # Create instance
        operation = create_instance(
            compute,
            project,
            VM_CONFIG['zone'],
            VM_CONFIG['name'],
            VM_CONFIG['machine_type'],
            image_url,
            SSH_PUBLIC_KEY
        )
        
        # Wait for completion
        wait_for_operation(
            compute,
            project,
            VM_CONFIG['zone'],
            operation['name']
        )
        
        # Get instance info
        info = get_instance_info(
            compute,
            project,
            VM_CONFIG['zone'],
            VM_CONFIG['name']
        )
        
        # Success!
        print("\n" + "=" * 60)
        print("VPS PROVISIONING COMPLETE!")
        print("=" * 60)
        print(f"External IP: {info['external_ip']}")
        print(f"Internal IP: {info['internal_ip']}")
        print(f"Machine Type: {info['machine_type']}")
        print(f"Zone: {VM_CONFIG['zone']}")
        print(f"SSH Command: ssh root@{info['external_ip']}")
        print("=" * 60)
        
        # Save credentials
        with open("vps-credentials.txt", "w") as f:
            f.write(f"Provider: Google Cloud Platform\n")
            f.write(f"Project: {project}\n")
            f.write(f"Instance Name: {info['name']}\n")
            f.write(f"External IP: {info['external_ip']}\n")
            f.write(f"Internal IP: {info['internal_ip']}\n")
            f.write(f"Zone: {VM_CONFIG['zone']}\n")
            f.write(f"Machine Type: {info['machine_type']}\n")
            f.write(f"SSH Command: ssh root@{info['external_ip']}\n")
            f.write(f"\nSSH Private Key: C:\\Users\\edri2\\.ssh\\hetzner_ai_os\n")
        
        print("Credentials saved to: vps-credentials.txt")
        
    except HttpError as e:
        print(f"Google Cloud API Error: {e}")
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise

if __name__ == "__main__":
    main()
