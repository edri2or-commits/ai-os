import sqlite3

conn = sqlite3.connect('/home/node/.n8n/database.sqlite')
cursor = conn.cursor()

# Delete the broken workflow
cursor.execute("DELETE FROM workflow_entity WHERE id='wYIM8Rd0o0O02BEc'")
conn.commit()

print("✅ Workflow deleted successfully")
conn.close()
