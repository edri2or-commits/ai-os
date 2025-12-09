"""
Create LHO collection in Qdrant for semantic search of learned heuristics.

Collection schema:
- vectors: OpenAI text-embedding-3-small (1536 dimensions)
- payload: LHO JSON (id, title, trigger, strategy, priority, tags)
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
import sys

def create_lho_collection():
    try:
        # Connect to Qdrant (Docker on localhost:6333)
        client = QdrantClient(host="localhost", port=6333)
        
        collection_name = "lhos"
        
        # Check if collection exists
        collections = client.get_collections().collections
        if any(c.name == collection_name for c in collections):
            print(f"[OK] Collection '{collection_name}' already exists")
            return True
        
        # Create collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=1536,  # OpenAI text-embedding-3-small
                distance=Distance.COSINE
            )
        )
        
        print(f"[OK] Created collection '{collection_name}'")
        print(f"     Vector size: 1536 (text-embedding-3-small)")
        print(f"     Distance: COSINE")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = create_lho_collection()
    sys.exit(0 if success else 1)
