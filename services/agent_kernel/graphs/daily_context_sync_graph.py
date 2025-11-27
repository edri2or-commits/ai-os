"""
Daily Context Sync Graph - LangGraph Implementation

This graph performs a simple daily context sync:
1. Read current state from OS Core MCP
2. Compute patch with updated timestamp
3. Apply patch and log completion
"""

import httpx
from datetime import datetime
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END


# --- State Definition ---

class SyncState(TypedDict):
    """State passed between graph nodes"""
    current_state: Dict[str, Any]
    patch: Dict[str, Any]
    updated_state: Dict[str, Any]
    last_sync_time: str
    error: str | None


# --- Configuration ---

OS_CORE_MCP_BASE_URL = "http://localhost:8083"
SOURCE = "agent-kernel"


# --- Node Functions ---

def start_node(state: SyncState) -> SyncState:
    """
    Node 1: Read current state and log sync start
    """
    print("[START_NODE] Reading current state from OS Core MCP...")
    
    try:
        # Read current state
        response = httpx.get(f"{OS_CORE_MCP_BASE_URL}/state", timeout=10.0)
        response.raise_for_status()
        current_state = response.json()
        
        print(f"[START_NODE] Current phase: {current_state.get('system', {}).get('phase', 'N/A')}")
        
        # Log sync started event
        event_payload = {
            "event_type": "DAILY_CONTEXT_SYNC_STARTED",
            "payload": {},
            "source": SOURCE
        }
        
        event_response = httpx.post(
            f"{OS_CORE_MCP_BASE_URL}/events",
            json=event_payload,
            timeout=10.0
        )
        event_response.raise_for_status()
        
        print("[START_NODE] Logged DAILY_CONTEXT_SYNC_STARTED event")
        
        return {
            **state,
            "current_state": current_state,
            "error": None
        }
        
    except Exception as e:
        print(f"[START_NODE] ERROR: {e}")
        return {
            **state,
            "error": str(e)
        }


def compute_patch(state: SyncState) -> SyncState:
    """
    Node 2: Compute patch with updated timestamp
    """
    print("[COMPUTE_PATCH] Computing state patch...")
    
    if state.get("error"):
        print("[COMPUTE_PATCH] Skipping due to previous error")
        return state
    
    try:
        # Generate timestamp
        now_utc = datetime.utcnow().isoformat() + "Z"
        
        # Create patch
        patch = {
            "last_daily_context_sync_utc": now_utc
        }
        
        print(f"[COMPUTE_PATCH] Patch: last_daily_context_sync_utc = {now_utc}")
        
        return {
            **state,
            "patch": patch,
            "last_sync_time": now_utc
        }
        
    except Exception as e:
        print(f"[COMPUTE_PATCH] ERROR: {e}")
        return {
            **state,
            "error": str(e)
        }


def apply_patch(state: SyncState) -> SyncState:
    """
    Node 3: Apply patch and log sync completion
    """
    print("[APPLY_PATCH] Applying patch to state...")
    
    if state.get("error"):
        print("[APPLY_PATCH] Skipping due to previous error")
        return state
    
    try:
        patch = state.get("patch", {})
        
        # Apply patch via OS Core MCP
        update_payload = {
            "patch": patch,
            "source": "daily-context-sync"
        }
        
        response = httpx.post(
            f"{OS_CORE_MCP_BASE_URL}/state/update",
            json=update_payload,
            timeout=10.0
        )
        response.raise_for_status()
        result = response.json()
        
        updated_state = result.get("state", {})
        
        print(f"[APPLY_PATCH] State updated successfully")
        
        # Log sync completed event
        event_payload = {
            "event_type": "DAILY_CONTEXT_SYNC_COMPLETED",
            "payload": {
                "last_daily_context_sync_utc": state.get("last_sync_time")
            },
            "source": SOURCE
        }
        
        event_response = httpx.post(
            f"{OS_CORE_MCP_BASE_URL}/events",
            json=event_payload,
            timeout=10.0
        )
        event_response.raise_for_status()
        
        print("[APPLY_PATCH] Logged DAILY_CONTEXT_SYNC_COMPLETED event")
        
        return {
            **state,
            "updated_state": updated_state
        }
        
    except Exception as e:
        print(f"[APPLY_PATCH] ERROR: {e}")
        return {
            **state,
            "error": str(e)
        }


# --- Graph Construction ---

def create_daily_context_sync_graph():
    """
    Create and return the Daily Context Sync graph
    """
    workflow = StateGraph(SyncState)
    
    # Add nodes
    workflow.add_node("start", start_node)
    workflow.add_node("compute", compute_patch)
    workflow.add_node("apply", apply_patch)
    
    # Define edges (flow)
    workflow.add_edge("start", "compute")
    workflow.add_edge("compute", "apply")
    workflow.add_edge("apply", END)
    
    # Set entry point
    workflow.set_entry_point("start")
    
    return workflow.compile()


# --- Execution Function ---

def run_daily_context_sync() -> Dict[str, Any]:
    """
    Execute the daily context sync graph
    
    Returns:
        Dict with status, last_sync_time, and error (if any)
    """
    print("=" * 60)
    print("DAILY CONTEXT SYNC - Starting execution")
    print("=" * 60)
    
    # Create graph
    graph = create_daily_context_sync_graph()
    
    # Initial state
    initial_state: SyncState = {
        "current_state": {},
        "patch": {},
        "updated_state": {},
        "last_sync_time": "",
        "error": None
    }
    
    # Run graph
    final_state = graph.invoke(initial_state)
    
    print("=" * 60)
    print("DAILY CONTEXT SYNC - Execution complete")
    print("=" * 60)
    
    # Return result
    if final_state.get("error"):
        return {
            "status": "error",
            "error": final_state["error"],
            "last_sync_time": None
        }
    else:
        return {
            "status": "ok",
            "last_sync_time": final_state.get("last_sync_time"),
            "last_daily_context_sync_utc": final_state.get("last_sync_time")
        }


if __name__ == "__main__":
    # Test execution
    result = run_daily_context_sync()
    print(f"\nResult: {result}")
