"""
OS Core MCP - Main FastAPI application

Provides unified API access to AI-OS State Layer:
- SYSTEM_STATE_COMPACT.json
- SERVICES_STATUS.json
- EVENT_TIMELINE.jsonl

This is the "OS Core" - the single source of truth gateway.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI-OS Core MCP",
    description="HTTP service for AI-OS State Layer access - The OS Core gateway",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define repo root (relative paths from this file)
REPO_ROOT = Path(__file__).parent.parent.parent
DOCS_ROOT = REPO_ROOT / "docs"
STATE_ROOT = DOCS_ROOT / "system_state"
REGISTRIES_ROOT = STATE_ROOT / "registries"
TIMELINE_ROOT = STATE_ROOT / "timeline"


# --- Pydantic Models ---

class AppendEventRequest(BaseModel):
    event_type: str
    payload: Dict[str, Any]
    source: str = "os-core-mcp"


class UpdateStateRequest(BaseModel):
    patch: Dict[str, Any]
    source: str = "os-core-mcp"


# --- Helper Functions ---

def read_json_file(file_path: Path) -> Dict[str, Any]:
    """Read and parse a JSON file"""
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Invalid JSON in file: {e}")
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def append_to_jsonl(file_path: Path, event: Dict[str, Any]) -> Dict[str, Any]:
    """Append an event to a JSONL file"""
    try:
        # Create file if it doesn't exist
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.touch()
        
        # Append event as single line JSON
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(event, ensure_ascii=False) + '\n')
        
        return event
    except Exception as e:
        logger.error(f"Error appending to {file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


def update_json_file(file_path: Path, patch: Dict[str, Any]) -> Dict[str, Any]:
    """Update a JSON file by merging patch at top level"""
    try:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Read current state
        with open(file_path, 'r', encoding='utf-8') as f:
            state = json.load(f)
        
        # Merge patch (top-level only)
        state.update(patch)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        
        return state
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        raise HTTPException(status_code=500, detail=f"Invalid JSON in file: {e}")
    except Exception as e:
        logger.error(f"Error updating {file_path}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# --- API Endpoints ---

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "ok": True,
        "service": "AI-OS Core MCP",
        "version": "0.1.0",
        "message": "OS Core gateway is running",
        "endpoints": {
            "read_system_state": "/state",
            "read_services_status": "/services",
            "append_event": "/events"
        }
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    system_state_path = STATE_ROOT / "SYSTEM_STATE_COMPACT.json"
    services_path = REGISTRIES_ROOT / "SERVICES_STATUS.json"
    timeline_path = TIMELINE_ROOT / "EVENT_TIMELINE.jsonl"
    
    return {
        "ok": True,
        "service": "AI-OS Core MCP",
        "version": "0.1.0",
        "files": {
            "system_state": {
                "path": str(system_state_path),
                "exists": system_state_path.exists()
            },
            "services_status": {
                "path": str(services_path),
                "exists": services_path.exists()
            },
            "event_timeline": {
                "path": str(timeline_path),
                "exists": timeline_path.exists()
            }
        }
    }


@app.get("/state")
async def read_system_state() -> Dict[str, Any]:
    """
    Read SYSTEM_STATE_COMPACT.json
    
    Returns the current system state as JSON object.
    Raises 404 if file doesn't exist, 500 if JSON is invalid.
    """
    file_path = STATE_ROOT / "SYSTEM_STATE_COMPACT.json"
    logger.info(f"Reading system state from {file_path}")
    
    return read_json_file(file_path)


@app.get("/services")
async def read_services_status() -> Dict[str, Any]:
    """
    Read SERVICES_STATUS.json
    
    Returns the current services status as JSON object.
    Raises 404 if file doesn't exist, 500 if JSON is invalid.
    """
    file_path = REGISTRIES_ROOT / "SERVICES_STATUS.json"
    logger.info(f"Reading services status from {file_path}")
    
    return read_json_file(file_path)


@app.post("/state/update")
async def update_state(request: UpdateStateRequest) -> Dict[str, Any]:
    """
    Update SYSTEM_STATE_COMPACT.json by merging a patch
    
    Request body:
    {
        "patch": { ... keys to update ... },
        "source": "string (default: 'os-core-mcp')"
    }
    
    Merges patch at top level only.
    Returns the updated state.
    """
    file_path = STATE_ROOT / "SYSTEM_STATE_COMPACT.json"
    
    logger.info(f"Updating system state from {file_path}: {len(request.patch)} keys from {request.source}")
    
    updated_state = update_json_file(file_path, request.patch)
    
    return {
        "status": "ok",
        "source": request.source,
        "state": updated_state
    }


@app.post("/events")
async def append_event(request: AppendEventRequest) -> Dict[str, Any]:
    """
    Append an event to EVENT_TIMELINE.jsonl
    
    Request body:
    {
        "event_type": "string (e.g. 'info', 'error', 'state_change')",
        "payload": { ... arbitrary JSON ... },
        "source": "string (default: 'os-core-mcp')"
    }
    
    Returns the event object that was written (includes timestamp).
    """
    file_path = TIMELINE_ROOT / "EVENT_TIMELINE.jsonl"
    
    # Build event object
    event = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "event_type": request.event_type,
        "source": request.source,
        "payload": request.payload
    }
    
    logger.info(f"Appending event to {file_path}: {request.event_type} from {request.source}")
    
    result = append_to_jsonl(file_path, event)
    
    return {
        "ok": True,
        "message": "Event appended successfully",
        "event": result
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8083)
