"""
Test LHO retrieval from Qdrant using payload filtering.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Filter, FieldCondition, MatchValue
import sys

def test_lho_retrieval():
    try:
        client = QdrantClient(host="localhost", port=6333)
        
        print("[TEST 1] Retrieve all LHOs")
        print("=" * 50)
        
        # Get all points
        result = client.scroll(
            collection_name="lhos",
            limit=10
        )
        
        if not result[0]:
            print("[ERROR] No LHOs found in collection")
            return False
        
        for point in result[0]:
            lho = point.payload
            print(f"  ID: {lho['lho_id']}")
            print(f"  Title: {lho['title']}")
            print(f"  Priority: {lho['priority']}")
            print(f"  Tags: {', '.join(lho['tags'])}")
            print()
        
        print("[TEST 2] Filter by tag: 'csv'")
        print("=" * 50)
        
        # Filter by tag
        result = client.scroll(
            collection_name="lhos",
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="tags",
                        match=MatchValue(value="csv")
                    )
                ]
            ),
            limit=10
        )
        
        if result[0]:
            print(f"  Found {len(result[0])} LHO(s) with tag 'csv'")
            for point in result[0]:
                print(f"  - {point.payload['lho_id']}: {point.payload['title']}")
        else:
            print("  No LHOs found with tag 'csv'")
        
        print()
        print("[OK] LHO Database operational!")
        print("     Collection: lhos")
        print("     Storage: Qdrant (localhost:6333)")
        print("     Next: Judge/Teacher/Librarian will add real LHOs")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        return False

if __name__ == "__main__":
    success = test_lho_retrieval()
    sys.exit(0 if success else 1)
