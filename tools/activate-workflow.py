import sqlite3
import sys

# Connect to n8n database
db_path = '/home/node/.n8n/database.sqlite'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Find workflow
cursor.execute("SELECT id, name, active FROM workflow_entity WHERE name LIKE '%Observer%'")
workflow = cursor.fetchone()

if workflow:
    wf_id, wf_name, is_active = workflow
    print(f"Found workflow: {wf_name} (ID: {wf_id}, Active: {is_active})")
    
    if is_active == 0:
        # Activate it
        cursor.execute("UPDATE workflow_entity SET active = 1 WHERE id = ?", (wf_id,))
        conn.commit()
        print("✅ Workflow activated successfully!")
    else:
        print("✅ Workflow is already active!")
else:
    print("❌ Workflow not found")
    sys.exit(1)

conn.close()
