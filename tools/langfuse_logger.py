"""
Langfuse Logger - Protocol 1 Automation
Logs all Claude actions as traces in Langfuse.

Usage:
    from tools.langfuse_logger import log_action
    
    log_action(
        action_type="file_edit",
        details={"file": "test.py", "changes": 3},
        status="success"
    )
"""

import os
from datetime import datetime
from langfuse import Langfuse

# Initialize Langfuse client
# Keys should be in environment variables (set via .env or launcher script)
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY", ""),
    secret_key=os.getenv("LANGFUSE_SECRET_KEY", ""),
    host=os.getenv("LANGFUSE_HOST", "http://localhost:3000")
)


def log_action(
    action_type: str,
    details: dict = None,
    status: str = "success",
    user_id: str = "or",
    session_id: str = None,
    tags: list = None
):
    """
    Log a Claude action to Langfuse.
    
    Args:
        action_type: Type of action (e.g., "file_edit", "git_commit", "tool_call")
        details: Dictionary of action details (file paths, changes, etc.)
        status: "success", "error", or "warning"
        user_id: User identifier (default: "or")
        session_id: Optional session grouping
        tags: Optional list of tags for filtering
    
    Returns:
        trace_id: Langfuse trace ID for reference
    """
    if details is None:
        details = {}
    
    if tags is None:
        tags = []
    
    # Add default tags
    tags.extend(["claude_action", f"status_{status}"])
    
    # Create trace
    trace = langfuse.trace(
        name=action_type,
        user_id=user_id,
        session_id=session_id,
        metadata={
            "action_type": action_type,
            "status": status,
            "timestamp": datetime.utcnow().isoformat(),
            **details
        },
        tags=tags
    )
    
    # Flush to ensure immediate write
    langfuse.flush()
    
    return trace.id


def log_tool_call(
    tool_name: str,
    tool_args: dict,
    tool_result: dict,
    duration_ms: float = None,
    cost: float = None
):
    """
    Log a specific tool call (filesystem, git, n8n, etc.)
    
    Args:
        tool_name: Name of MCP tool called
        tool_args: Arguments passed to tool
        tool_result: Result returned from tool
        duration_ms: Execution time in milliseconds
        cost: Optional cost in USD
    """
    trace = langfuse.trace(
        name=f"tool_call_{tool_name}",
        user_id="or",
        metadata={
            "tool_name": tool_name,
            "timestamp": datetime.utcnow().isoformat()
        },
        tags=["tool_call", tool_name]
    )
    
    # Log as a span with input/output
    span = trace.span(
        name=tool_name,
        input=tool_args,
        output=tool_result,
        metadata={
            "duration_ms": duration_ms,
            "cost_usd": cost
        }
    )
    
    langfuse.flush()
    return trace.id


def log_conversation_turn(
    user_message: str,
    assistant_message: str,
    model: str = "claude-sonnet-4.5",
    tokens_used: int = None,
    cost: float = None
):
    """
    Log a complete conversation turn (user → Claude → response)
    
    Args:
        user_message: User's input message
        assistant_message: Claude's response
        model: Model used
        tokens_used: Total tokens consumed
        cost: Cost in USD
    """
    trace = langfuse.trace(
        name="conversation_turn",
        user_id="or",
        metadata={
            "model": model,
            "timestamp": datetime.utcnow().isoformat()
        },
        tags=["conversation", model]
    )
    
    # Log as a generation (LLM call)
    generation = trace.generation(
        name="claude_response",
        model=model,
        input=[{"role": "user", "content": user_message}],
        output={"role": "assistant", "content": assistant_message},
        usage={
            "total": tokens_used
        } if tokens_used else None,
        metadata={
            "cost_usd": cost
        }
    )
    
    langfuse.flush()
    return trace.id


# Example usage (for testing)
if __name__ == "__main__":
    print("Testing Langfuse Logger...")
    
    # Test 1: Simple action log
    trace_id = log_action(
        action_type="test_action",
        details={"test": True, "message": "Hello Langfuse"},
        status="success"
    )
    print(f"✅ Logged test action: {trace_id}")
    
    # Test 2: Tool call log
    tool_trace = log_tool_call(
        tool_name="filesystem",
        tool_args={"operation": "read", "file": "test.md"},
        tool_result={"success": True, "content": "File content..."},
        duration_ms=45.2
    )
    print(f"✅ Logged tool call: {tool_trace}")
    
    # Test 3: Conversation turn
    conv_trace = log_conversation_turn(
        user_message="What's the weather?",
        assistant_message="Sunny, 25°C",
        tokens_used=150,
        cost=0.0015
    )
    print(f"✅ Logged conversation: {conv_trace}")
    
    print("\n🎉 All tests passed! Check Langfuse dashboard: http://localhost:3000")
