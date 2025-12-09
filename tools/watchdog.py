"""
Memory Bank Watchdog - Automated ingestion to Qdrant

Detects changes in Memory Bank files via Git, parses by Markdown headers,
embeds chunks, and stores in Qdrant for semantic search.

Usage:
    python watchdog.py [--minutes N]  # Check last N minutes (default: 15)
    python watchdog.py --dry-run      # Test without storing to Qdrant
"""

import subprocess
import sys
import re
from datetime import datetime, timedelta
from pathlib import Path

# Qdrant imports (with fallback for testing)
try:
    from qdrant_client import QdrantClient
    from qdrant_client.models import Distance, VectorParams, PointStruct
    from sentence_transformers import SentenceTransformer
    QDRANT_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] Qdrant dependencies not available: {e}", file=sys.stderr)
    print("Install with: pip install qdrant-client sentence-transformers --break-system-packages", file=sys.stderr)
    QDRANT_AVAILABLE = False

# === Configuration ===
REPO_ROOT = Path(__file__).parent.parent
MEMORY_BANK = REPO_ROOT / "memory-bank"
TRACKED_FILES = [
    "memory-bank/01-active-context.md",
    "memory-bank/02-progress.md"
]
GIT_PATH = "C:\\Program Files\\Git\\cmd\\git.exe"

# Qdrant configuration
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
COLLECTION_NAME = "memory-bank"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Fast, 384 dimensions


def get_changed_files_since(minutes=15):
    """
    Get Memory Bank files changed in last N minutes via Git log.
    
    Args:
        minutes: Time window to check (default: 15)
        
    Returns:
        List of changed file paths (deduplicated)
    """
    since = datetime.now() - timedelta(minutes=minutes)
    since_str = since.strftime("%Y-%m-%d %H:%M:%S")
    
    cmd = [
        GIT_PATH,
        "log",
        f"--since={since_str}",
        "--name-only",
        "--pretty=format:",
        "--",
        *TRACKED_FILES
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=True
        )
        
        # Parse output: deduplicate and filter empty lines
        files = [f.strip() for f in result.stdout.split("\n") if f.strip()]
        unique_files = list(set(files))
        
        return unique_files
        
    except subprocess.CalledProcessError as e:
        print(f"[WARN] Git error: {e}", file=sys.stderr)
        return []


def get_current_commit():
    """Get current Git commit hash (short form)."""
    try:
        result = subprocess.run(
            [GIT_PATH, "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return "unknown"


def parse_markdown_chunks(file_path):
    """
    Parse Markdown file into chunks by headers (## and ###).
    
    Args:
        file_path: Path to Markdown file
        
    Returns:
        List of dicts: [{"header": str, "text": str, "level": int}, ...]
    """
    try:
        content = Path(file_path).read_text(encoding="utf-8")
    except Exception as e:
        print(f"[WARN] Error reading {file_path}: {e}", file=sys.stderr)
        return []
    
    chunks = []
    current_chunk = {"header": "Preamble", "text": "", "level": 1}
    
    for line in content.split("\n"):
        # Match #, ##, or ### headers
        header_match = re.match(r"^(#{1,3})\s+(.+)$", line)
        
        if header_match:
            # Save previous chunk if it has content
            if current_chunk["text"].strip():
                chunks.append(current_chunk)
            
            # Start new chunk
            level = len(header_match.group(1))  # 2 for ##, 3 for ###
            header = header_match.group(2).strip()
            current_chunk = {"header": header, "text": "", "level": level}
        else:
            # Accumulate text
            current_chunk["text"] += line + "\n"
    
    # Save last chunk
    if current_chunk["text"].strip():
        chunks.append(current_chunk)
    
    return chunks


# === Qdrant Integration ===

def embed_text(text, model):
    """
    Generate embedding vector for text using sentence-transformers.
    
    Args:
        text: Text to embed
        model: SentenceTransformer model instance
        
    Returns:
        List of floats (embedding vector)
    """
    try:
        embedding = model.encode(text, show_progress_bar=False)
        return embedding.tolist()
    except Exception as e:
        print(f"[WARN] Embedding error: {e}", file=sys.stderr)
        return None


def ensure_collection(client, collection_name, vector_size=384):
    """
    Ensure Qdrant collection exists, create if missing.
    
    Args:
        client: QdrantClient instance
        collection_name: Name of collection
        vector_size: Embedding dimension (default: 384 for all-MiniLM-L6-v2)
    """
    try:
        collections = client.get_collections().collections
        exists = any(c.name == collection_name for c in collections)
        
        if not exists:
            print(f"[INFO] Creating collection: {collection_name}")
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
            )
            print(f"[OK] Collection created: {collection_name}")
        else:
            print(f"[OK] Collection exists: {collection_name}")
    except Exception as e:
        print(f"[WARN] Collection error: {e}", file=sys.stderr)
        raise


def store_to_qdrant(client, collection_name, chunks, file_path, commit_hash, model, dry_run=False):
    """
    Store parsed chunks to Qdrant with embeddings.
    
    Args:
        client: QdrantClient instance
        collection_name: Qdrant collection name
        chunks: List of parsed chunks from parse_markdown_chunks()
        file_path: Source file path (for metadata)
        commit_hash: Git commit hash (for metadata)
        model: SentenceTransformer model for embeddings
        dry_run: If True, skip actual storage
        
    Returns:
        Number of chunks stored
    """
    if dry_run:
        print(f"[DRY-RUN] [DRY RUN] Would store {len(chunks)} chunks from {file_path}")
        return len(chunks)
    
    points = []
    timestamp = datetime.now().isoformat()
    
    for i, chunk in enumerate(chunks):
        # Generate embedding
        text = f"{chunk['header']}\n\n{chunk['text']}"
        embedding = embed_text(text, model)
        
        if embedding is None:
            print(f"[WARN] Skipping chunk {i+1} (embedding failed)")
            continue
        
        # Create point
        point_id = f"{file_path}_{commit_hash}_{i}"
        point = PointStruct(
            id=hash(point_id) % (10 ** 8),  # Numeric ID from string hash
            vector=embedding,
            payload={
                "file": str(file_path),
                "header": chunk["header"],
                "level": chunk["level"],
                "text": chunk["text"][:500],  # Truncate for storage
                "commit": commit_hash,
                "timestamp": timestamp,
                "chunk_index": i
            }
        )
        points.append(point)
    
    # Batch upload
    if points:
        try:
            client.upsert(collection_name=collection_name, points=points)
            print(f"[OK] Stored {len(points)} chunks from {file_path}")
            return len(points)
        except Exception as e:
            print(f"[WARN] Storage error: {e}", file=sys.stderr)
            return 0
    else:
        print(f"[WARN] No valid chunks to store from {file_path}")
        return 0


# === Main entry point ===
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Memory Bank Watchdog - Qdrant Ingestion")
    parser.add_argument("--minutes", type=int, default=15,
                       help="Check files changed in last N minutes (default: 15)")
    parser.add_argument("--dry-run", action="store_true",
                       help="Test without storing to Qdrant")
    parser.add_argument("--test-parser", action="store_true",
                       help="Test Markdown parser on 01-active-context.md")
    parser.add_argument("--test-embed", action="store_true",
                       help="Test embedding generation")
    args = parser.parse_args()
    
    # Test parser mode
    if args.test_parser:
        print("[Testing Markdown Parser]")
        test_file = REPO_ROOT / "memory-bank" / "01-active-context.md"
        chunks = parse_markdown_chunks(test_file)
        
        print(f"\nParsed {len(chunks)} chunks from {test_file.name}:")
        for i, chunk in enumerate(chunks[:5], 1):  # Show first 5
            try:
                text_preview = chunk["text"][:80].replace("\n", " ")
                print(f"{i}. [{chunk['level']}] {chunk['header']}")
                print(f"   Text: {text_preview}...")
            except UnicodeEncodeError:
                print(f"{i}. [{chunk['level']}] {chunk['header']}")
                print(f"   Text: [preview skipped - encoding issue]")
        
        if len(chunks) > 5:
            print(f"   ... and {len(chunks) - 5} more chunks")
        sys.exit(0)
    
    # Test embedding mode
    if args.test_embed:
        if not QDRANT_AVAILABLE:
            print("[ERROR] Qdrant dependencies not available", file=sys.stderr)
            sys.exit(1)
        
        print("[Testing Embedding Generation]")
        print(f"Loading model: {EMBEDDING_MODEL}")
        model = SentenceTransformer(EMBEDDING_MODEL)
        
        test_text = "This is a test sentence for embedding generation."
        embedding = embed_text(test_text, model)
        
        if embedding:
            print(f"[OK] Embedding generated: {len(embedding)} dimensions")
            print(f"   Sample values: {embedding[:5]}")
        else:
            print("[ERROR] Embedding failed")
        sys.exit(0)
    
    # Main ingestion workflow
    print(f"[Memory Bank Watchdog - Qdrant Ingestion]")
    print(f"Checking last {args.minutes} minutes...")
    
    # Check Qdrant availability
    if not QDRANT_AVAILABLE and not args.dry_run:
        print("[ERROR] Qdrant dependencies not available", file=sys.stderr)
        print("Run with --dry-run to test without Qdrant", file=sys.stderr)
        sys.exit(1)
    
    # Get changed files
    changed = get_changed_files_since(args.minutes)
    commit = get_current_commit()
    
    print(f"Current commit: {commit}")
    print(f"Changed files: {len(changed)}")
    
    if not changed:
        print("[OK] No changes detected - nothing to ingest")
        sys.exit(0)
    
    for f in changed:
        print(f"  - {f}")
    
    # Initialize Qdrant (if not dry-run)
    if not args.dry_run:
        print(f"\n[INFO] Connecting to Qdrant at {QDRANT_HOST}:{QDRANT_PORT}")
        try:
            client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
            ensure_collection(client, COLLECTION_NAME, vector_size=384)
            
            print(f"[INFO] Loading embedding model: {EMBEDDING_MODEL}")
            model = SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            print(f"[ERROR] Qdrant connection failed: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        client = None
        model = None
    
    # Process each changed file
    total_stored = 0
    for file_path in changed:
        full_path = REPO_ROOT / file_path
        print(f"\n[FILE] Processing: {file_path}")
        
        # Parse chunks
        chunks = parse_markdown_chunks(full_path)
        print(f"   Parsed: {len(chunks)} chunks")
        
        if not chunks:
            print(f"   [WARN] No chunks found")
            continue
        
        # Store to Qdrant
        if not args.dry_run:
            stored = store_to_qdrant(client, COLLECTION_NAME, chunks, file_path, commit, model, dry_run=False)
            total_stored += stored
        else:
            print(f"   [DRY-RUN] [DRY RUN] Would store {len(chunks)} chunks")
            total_stored += len(chunks)
    
    # Summary
    print(f"\n{'=' * 50}")
    if args.dry_run:
        print(f"[DRY-RUN] DRY RUN COMPLETE")
        print(f"Would have stored {total_stored} chunks from {len(changed)} files")
    else:
        print(f"[OK] INGESTION COMPLETE")
        print(f"Stored {total_stored} chunks from {len(changed)} files to Qdrant")
