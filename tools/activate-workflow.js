// Activate workflow in n8n database
const sqlite3 = require('better-sqlite3');
const db = sqlite3('/home/node/.n8n/database.sqlite');

// Find workflow
const workflow = db.prepare("SELECT id, name, active FROM workflow_entity WHERE name LIKE '%Observer%'").get();

if (workflow) {
    console.log(`Found workflow: ${workflow.name} (ID: ${workflow.id}, Active: ${workflow.active})`);
    
    if (workflow.active === 0) {
        // Activate it
        db.prepare("UPDATE workflow_entity SET active = 1 WHERE id = ?").run(workflow.id);
        console.log('✅ Workflow activated successfully!');
    } else {
        console.log('✅ Workflow is already active!');
    }
} else {
    console.log('❌ Workflow not found');
}

db.close();
