"""Check if Telegram Bot was already tested."""
import sqlite3
import os

db_path = r"C:\Users\edri2\Desktop\AI\ai-os\services\approval-bot\approvals.db"

if not os.path.exists(db_path):
    print("Database not found - Bot never ran")
    exit(0)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check if table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='approvals'")
if not cursor.fetchone():
    print("No approvals table - Bot never initialized")
    conn.close()
    exit(0)

# Count total records
cursor.execute('SELECT COUNT(*) FROM approvals')
count = cursor.fetchone()[0]
print(f"Total approval records: {count}")

if count == 0:
    print("Database exists but empty - Bot ran but no approvals processed yet")
    conn.close()
    exit(0)

# Show recent records
print("\nRecent approvals:")
cursor.execute('SELECT cr_id, status, created_at FROM approvals ORDER BY created_at DESC LIMIT 5')
for row in cursor.fetchall():
    cr_id, status, created_at = row
    print(f"  - {cr_id}: {status} (created: {created_at})")

conn.close()
