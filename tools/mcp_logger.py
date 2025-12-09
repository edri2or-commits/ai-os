"""
MCP Logger - Structured logging for AI Life OS tool calls
Logs all MCP tool invocations to JSONL for audit trail and analysis.
"""

import json
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional, Dict, Any
import functools
import time


class MCPLogger:
    """Logger for MCP tool calls with JSONL output"""
    
    def __init__(self, log_dir: str = None):
        if log_dir is None:
            log_dir = Path(__file__).parent.parent / "logs"
        else:
            log_dir = Path(log_dir)
        
        self.log_dir = log_dir
        self.log_dir.mkdir(exist_ok=True)
        
        self.tool_calls_log = self.log_dir / "tool_calls.jsonl"
        self.errors_log = self.log_dir / "errors.jsonl"
        self.metrics_log = self.log_dir / "metrics.jsonl"
    
    def log_tool_call(
        self,
        tool_name: str,
        duration_ms: float,
        success: bool,
        error: Optional[Exception] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Log a tool call with timing and outcome"""
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "event_type": "tool_call",
            "tool_name": tool_name,
            "duration_ms": round(duration_ms, 2),
            "success": success,
            "error": str(error) if error else None,
            "metadata": metadata or {}
        }
        
        self._write_log(self.tool_calls_log, log_entry)
        
        if not success and error:
            self._write_log(self.errors_log, log_entry)
    
    def log_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "count",
        tags: Optional[Dict[str, str]] = None
    ):
        """Log a metric for analysis"""
        log_entry = {
            "timestamp": datetime.now(UTC).isoformat(),
            "metric_name": metric_name,
            "value": value,
            "unit": unit,
            "tags": tags or {}
        }
        
        self._write_log(self.metrics_log, log_entry)
    
    def _write_log(self, log_file: Path, entry: Dict[str, Any]):
        """Append log entry to JSONL file"""
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    
    def track_tool(self, tool_name: str, metadata: Optional[Dict[str, Any]] = None):
        """Decorator to automatically track tool execution"""
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                success = False
                error = None
                
                try:
                    result = func(*args, **kwargs)
                    success = True
                    return result
                except Exception as e:
                    error = e
                    raise
                finally:
                    duration_ms = (time.time() - start_time) * 1000
                    self.log_tool_call(
                        tool_name=tool_name,
                        duration_ms=duration_ms,
                        success=success,
                        error=error,
                        metadata=metadata
                    )
            
            return wrapper
        return decorator


# Global logger instance
logger = MCPLogger()


# Example usage:
if __name__ == "__main__":
    # Test logging
    @logger.track_tool("test_tool", metadata={"version": "1.0"})
    def test_function():
        time.sleep(0.1)
        return "success"
    
    # Test success case
    test_function()
    
    # Test error case
    @logger.track_tool("failing_tool")
    def failing_function():
        raise ValueError("Test error")
    
    try:
        failing_function()
    except ValueError:
        pass
    
    # Test metric logging
    logger.log_metric("memory_usage_mb", 512.5, unit="megabytes", tags={"process": "observer"})
    
    print("[OK] Logs written to:")
    print(f"  - {logger.tool_calls_log}")
    print(f"  - {logger.errors_log}")
    print(f"  - {logger.metrics_log}")
