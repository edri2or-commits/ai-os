"""
Quick test of LangGraph import and graph creation
"""
import sys
sys.path.insert(0, r"C:\Users\edri2\Desktop\AI\ai-os\services\agent_kernel")

try:
    from graphs.daily_context_sync_graph import create_daily_context_sync_graph
    print("[OK] Import successful")
    
    graph = create_daily_context_sync_graph()
    print("[OK] Graph created successfully")
    print(f"  Type: {type(graph)}")
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
