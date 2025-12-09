"""
Insert LHO-001 into Qdrant collection.
For now: Store with dummy vector (zeros). Real embeddings will come from Teacher Agent.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import json
import sys

def insert_lho_001():
    try:
        # Connect to Qdrant
        client = QdrantClient(host="localhost", port=6333)
        
        # Read LHO-001
        with open("truth-layer/lhos/LHO-001.json", "r", encoding="utf-8") as f:
            lho = json.load(f)
        
        # Create point with dummy vector (will be replaced by real embedding later)
        # Vector: 1536 zeros (placeholder for text-embedding-3-small)
        dummy_vector = [0.0] * 1536
        
        point = PointStruct(
            id=1,  # LHO-001 -> ID 1
            vector=dummy_vector,
            payload=lho
        )
        
        # Insert into collection
        client.upsert(
            collection_name="lhos",
            points=[point]
        )
        
        print(f"[OK] Inserted {lho['lho_id']}: {lho['title']}")
        print(f"     Priority: {lho['priority']}")
        print(f"     Tags: {', '.join(lho['tags'])}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = insert_lho_001()
    sys.exit(0 if success else 1)
