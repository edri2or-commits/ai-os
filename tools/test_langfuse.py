"""
Test script to send a sample trace to Langfuse.
This helps understand the data model before Judge integration.
"""

import os
from langfuse import Langfuse
from datetime import datetime

# Initialize Langfuse client
langfuse = Langfuse(
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY", "pk-lf-123"),  # Replace with actual key
    secret_key=os.getenv("LANGFUSE_SECRET_KEY", "sk-lf-456"),  # Replace with actual key
    host="http://localhost:3000"
)

print("Testing Langfuse connection...")

# Create a trace ID
trace_id = langfuse.create_trace_id()
print(f"   [OK] Created trace ID: {trace_id}")

# Create an event (simplest form of trace)
event = langfuse.create_event(
    name="test_langfuse_connection",
    input={"message": "Testing basic Langfuse integration"},
    metadata={
        "test": True,
        "source": "test_langfuse.py",
        "timestamp": datetime.utcnow().isoformat()
    }
)
print("   [OK] Created test event")

# Flush to ensure all data is sent
print("   [..] Flushing data to Langfuse...")
langfuse.flush()
print("   [OK] Data flushed successfully")

print("\n[SUCCESS] Test completed successfully!")
print(f"   View traces at: http://localhost:3000/project/AI%20Life%20OS")
print("\nNext steps:")
print("   1. Check Langfuse dashboard for the test event")
print("   2. Import Judge V2 workflow to n8n")
print("   3. Test Judge workflow with Langfuse logging")
