"""
Memory Bank Context API
=======================
REST API for external LLMs to load AI Life OS project context.

Endpoints:
- GET /health - Health check
- GET /api/context/current-state - Current phase, progress, recent changes
- GET /api/context/project-brief - Project vision and TL;DR
- GET /api/context/protocols - Active protocols from current state
- GET /api/context/research/{family} - Research files by family

Author: AI Life OS
License: Private
"""

import os
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8081"))

# Paths (relative to repo root)
REPO_ROOT = Path(__file__).parent.parent.parent
MEMORY_BANK = REPO_ROOT / "memory-bank"
RESEARCH_DIR = REPO_ROOT / "claude-project" / "research_claude"

# Initialize FastAPI
app = FastAPI(
    title="AI Life OS Context API",
    description="Provides project context for external LLMs (GPT, Gemini, o1)",
    version="1.0.0"
)

# CORS Configuration (allow all origins for localhost safety)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Safe for localhost; restrict in H4 (VPS)
    allow_credentials=True,
    allow_methods=["GET"],  # Read-only API
    allow_headers=["*"],
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_git_sha() -> str:
    """Get current Git commit SHA (short form)."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return "unknown"
    except Exception:
        return "unknown"


def extract_phase_info(content: str) -> Dict[str, Any]:
    """Extract Phase name and progress % from active context content."""
    phase_match = re.search(r'Phase\s+\d+:\s+([^(]+)\s+\(~?(\d+)%', content)
    if phase_match:
        return {
            "phase": f"Phase {phase_match.group(0).split(':')[0].split()[-1]}: {phase_match.group(1).strip()}",
            "progress_pct": int(phase_match.group(2))
        }
    return {"phase": "Unknown", "progress_pct": 0}


def get_file_metadata(filepath: Path) -> Dict[str, Any]:
    """Get file metadata including size, modified time, and Git SHA."""
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
    
    stats = filepath.stat()
    git_sha = get_git_sha()
    
    return {
        "path": str(filepath.relative_to(REPO_ROOT)),
        "size_bytes": stats.st_size,
        "last_modified": datetime.fromtimestamp(stats.st_mtime).isoformat() + "Z",
        "git_sha": git_sha
    }


def extract_protocols_section(content: str) -> str:
    """Extract PROTOCOLS section from active context."""
    # Look for ## PROTOCOLS heading
    match = re.search(r'##\s+PROTOCOLS\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if match:
        return match.group(1).strip()
    return "No PROTOCOLS section found in current state."


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "context-api",
        "version": "1.0.0",
        "git_sha": get_git_sha()
    }


@app.get("/api/context/current-state")
async def get_current_state():
    """
    Get current project state from 01-active-context.md
    
    Returns:
        - content: Full markdown content
        - metadata: File stats + Phase info + Git SHA
    """
    try:
        filepath = MEMORY_BANK / "01-active-context.md"
        content = filepath.read_text(encoding="utf-8")
        
        # Extract metadata
        metadata = get_file_metadata(filepath)
        
        # Extract phase info from content
        phase_info = extract_phase_info(content)
        metadata.update(phase_info)
        
        return {
            "content": content,
            "metadata": metadata
        }
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Current state file not found. Check Memory Bank structure. ({str(e)})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading current state: {str(e)}"
        )


@app.get("/api/context/project-brief")
async def get_project_brief():
    """
    Get project vision and TL;DR from project-brief.md
    
    Returns:
        - content: Full markdown content
        - metadata: File stats + Git SHA
    """
    try:
        filepath = MEMORY_BANK / "project-brief.md"
        content = filepath.read_text(encoding="utf-8")
        metadata = get_file_metadata(filepath)
        
        return {
            "content": content,
            "metadata": metadata
        }
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Project brief not found. Check Memory Bank structure. ({str(e)})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading project brief: {str(e)}"
        )


@app.get("/api/context/protocols")
async def get_protocols():
    """
    Extract PROTOCOLS section from current state
    
    Returns:
        - content: PROTOCOLS section only
        - metadata: Parent file stats + Git SHA
    """
    try:
        filepath = MEMORY_BANK / "01-active-context.md"
        full_content = filepath.read_text(encoding="utf-8")
        
        # Extract protocols section
        protocols = extract_protocols_section(full_content)
        metadata = get_file_metadata(filepath)
        metadata["section"] = "PROTOCOLS"
        
        return {
            "content": protocols,
            "metadata": metadata
        }
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Current state file not found. ({str(e)})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error extracting protocols: {str(e)}"
        )


@app.get("/api/context/summary")
async def get_context_summary():
    """
    Get quick summary (first 100 lines) of current state
    
    Returns:
        - content: First 100 lines of 01-active-context.md
        - metadata: File stats + Phase info + Git SHA
    """
    try:
        filepath = MEMORY_BANK / "01-active-context.md"
        full_content = filepath.read_text(encoding="utf-8")
        
        # Get first 100 lines
        lines = full_content.split('\n')
        summary_content = '\n'.join(lines[:100])
        
        # Extract metadata
        metadata = get_file_metadata(filepath)
        phase_info = extract_phase_info(full_content)
        metadata.update(phase_info)
        metadata["lines_returned"] = min(100, len(lines))
        metadata["total_lines"] = len(lines)
        
        return {
            "content": summary_content,
            "metadata": metadata
        }
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Current state file not found. ({str(e)})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading summary: {str(e)}"
        )


@app.get("/api/context/roadmap")
async def get_roadmap():
    """
    Get Headless Migration Roadmap (VPS deployment plan)
    
    Returns:
        - content: HEADLESS_MIGRATION_ROADMAP_TLDR.md content
        - metadata: File stats + Git SHA
    """
    try:
        filepath = MEMORY_BANK / "plans" / "HEADLESS_MIGRATION_ROADMAP_TLDR.md"
        content = filepath.read_text(encoding="utf-8")
        metadata = get_file_metadata(filepath)
        
        return {
            "content": content,
            "metadata": metadata
        }
    
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Roadmap file not found. ({str(e)})"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading roadmap: {str(e)}"
        )


@app.get("/api/context/research/{family}")
async def get_research_by_family(family: str):
    """
    Get research files by family keyword
    
    Args:
        family: Keyword like 'architecture', 'mcp', 'adhd', 'safety', etc.
    
    Returns:
        - files: List of matching research files with content
        - metadata: Search info + Git SHA
    """
    try:
        if not RESEARCH_DIR.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Research directory not found: {RESEARCH_DIR}"
            )
        
        # Find matching files (case-insensitive search in filename)
        family_lower = family.lower()
        matching_files = []
        
        for md_file in RESEARCH_DIR.glob("*.md"):
            if family_lower in md_file.stem.lower():
                content = md_file.read_text(encoding="utf-8")
                file_metadata = get_file_metadata(md_file)
                matching_files.append({
                    "filename": md_file.name,
                    "content": content,
                    "metadata": file_metadata
                })
        
        if not matching_files:
            return {
                "files": [],
                "metadata": {
                    "family": family,
                    "count": 0,
                    "message": f"No research files found matching '{family}'. Available families: architecture, mcp, adhd, safety, infra, memory, meta.",
                    "git_sha": get_git_sha()
                }
            }
        
        return {
            "files": matching_files,
            "metadata": {
                "family": family,
                "count": len(matching_files),
                "git_sha": get_git_sha()
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching research files: {str(e)}"
        )


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print(f"[*] Starting Context API on http://{HOST}:{PORT}")
    print(f"[*] Memory Bank: {MEMORY_BANK}")
    print(f"[*] Research Dir: {RESEARCH_DIR}")
    print(f"[*] API Docs: http://localhost:{PORT}/docs")
    print(f"[*] Git SHA: {get_git_sha()}")
    
    uvicorn.run(
        "main:app",
        host=HOST,
        port=PORT,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )
