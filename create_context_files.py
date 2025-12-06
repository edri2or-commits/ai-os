#!/usr/bin/env python3
"""Create context files with proper UTF-8 encoding for GPT/Gemini"""

import requests
import json
from pathlib import Path

# API endpoints
BASE_URL = "http://localhost:8081/api/context"
ENDPOINTS = {
    "story": "story",
    "roadmap": "roadmap", 
    "summary": "summary"
}

# Output directory
OUTPUT_DIR = Path(__file__).parent

def fetch_and_save(endpoint_name: str, filename: str):
    """Fetch content from API and save as UTF-8"""
    url = f"{BASE_URL}/{endpoint_name}"
    print(f"Fetching {url}...")
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        content = data.get("content", "")
        
        # Write with explicit UTF-8 encoding
        output_path = OUTPUT_DIR / filename
        output_path.write_text(content, encoding="utf-8")
        
        print(f"[OK] Created {filename} ({len(content)} chars)")
        
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    print("Creating context files with UTF-8 encoding...\n")
    
    fetch_and_save("story", "story.txt")
    fetch_and_save("roadmap", "roadmap.txt")
    fetch_and_save("summary", "summary.txt")
    
    print("\n[OK] Done! Files ready for GPT/Gemini")
