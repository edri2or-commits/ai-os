# 🛣️ Implementation Roadmap - AI Life OS Revolution

**Timeline:** 8 Weeks (3 Phases)  
**Start Date:** Week 1 of Implementation  
**Methodology:** Chat→Spec→Change με HITL Gates

---

## 📋 Phase 1: Infrastructure Hardening (Weeks 1-2)

### **Slice 1.1: n8n Production Deployment** (3 days)

**Goal:** 24/7 n8n automation bus with systemd reliability

**Pre-Flight Checklist:**
- [ ] Docker installed: `docker --version`
- [ ] systemd working: `systemctl --version`
- [ ] Ports available: `sudo netstat -tuln | grep 5678`

**Steps:**
1. **Choose deployment mode:** (Day 1)
   ```bash
   # Option A: n8n Cloud (recommended for simplicity)
   # - Sign up at n8n.cloud
   # - Get webhook URL
   # - Configure credentials
   
   # Option B: Self-hosted Docker
   docker run -d --name n8n \
     -p 5678:5678 \
     -v ~/.n8n:/home/node/.n8n \
     -e N8N_BASIC_AUTH_ACTIVE=true \
     -e N8N_BASIC_AUTH_USER=admin \
     -e N8N_BASIC_AUTH_PASSWORD=<strong_password> \
     n8nio/n8n
   ```

2. **Create systemd service:** (Day 1)
   ```bash
   sudo tee /etc/systemd/system/n8n.service <<EOF
   [Unit]
   Description=n8n Workflow Automation
   After=network.target docker.service
   
   [Service]
   Type=simple
   Restart=always
   RestartSec=10
   ExecStart=/usr/bin/docker start -a n8n
   ExecStop=/usr/bin/docker stop n8n
   
   [Install]
   WantedBy=multi-user.target
   EOF
   
   sudo systemctl daemon-reload
   sudo systemctl enable n8n.service
   sudo systemctl start n8n.service
   ```

3. **Create bootstrap workflow:** (Day 2)
   - Open n8n at `localhost:5678`
   - Create workflow: "System Health Check"
   - Trigger: Webhook
   - Action: Desktop Commander → `systemctl status n8n`
   - Output: Return JSON response

4. **Test reliability:** (Day 3)
   ```bash
   # Kill container and verify auto-restart
   docker stop n8n
   sleep 15
   systemctl status n8n.service  # Should show "active (running)"
   ```

**Success Criteria:**
- ✅ `systemctl status n8n` shows "active (running)"
- ✅ n8n accessible at `localhost:5678`
- ✅ Test workflow executes successfully
- ✅ Service auto-restarts after manual stop

**Rollback Plan:**
```bash
sudo systemctl stop n8n.service
sudo systemctl disable n8n.service
docker rm -f n8n
```

---

### **Slice 1.2: Qdrant Vector Memory** (2 days)

**Goal:** Persistent semantic memory for long-term context

**Steps:**
1. **Deploy Qdrant container:** (Day 1)
   ```bash
   docker run -d --name qdrant \
     -p 6333:6333 -p 6334:6334 \
     -v ~/ai-os/qdrant_storage:/qdrant/storage \
     qdrant/qdrant:latest
   ```

2. **Create MCP server wrapper:** (Day 1)
   ```bash
   cd ~/ai-os/mcp-servers
   mkdir qdrant-server && cd qdrant-server
   npm init -y
   npm install @qdrant/js-client @modelcontextprotocol/sdk
   ```

3. **Implement MCP server:** (Day 2)
   ```javascript
   // index.js
   import { QdrantClient } from '@qdrant/js-client';
   import { Server } from '@modelcontextprotocol/sdk/server/index.js';
   
   const client = new QdrantClient({ url: 'http://localhost:6333' });
   const server = new Server({
     name: 'qdrant-mcp',
     version: '1.0.0',
   }, {
     capabilities: {
       tools: {
         search_memory: {
           description: 'Semantic search in vector memory',
           inputSchema: {
             type: 'object',
             properties: {
               query: { type: 'string' },
               limit: { type: 'number', default: 5 }
             }
           }
         }
       }
     }
   });
   
   server.setRequestHandler('tools/call', async (request) => {
     const { name, arguments: args } = request.params;
     if (name === 'search_memory') {
       const results = await client.search('memory', {
         vector: await embed(args.query),
         limit: args.limit
       });
       return { content: [{ type: 'text', text: JSON.stringify(results) }] };
     }
   });
   ```

4. **Add to Claude Desktop config:**
   ```json
   {
     "mcpServers": {
       "qdrant": {
         "command": "node",
         "args": ["C:\\Users\\edri2\\Desktop\\AI\\ai-os\\mcp-servers\\qdrant-server\\index.js"]
       }
     }
   }
   ```

**Success Criteria:**
- ✅ `docker ps | grep qdrant` shows running container
- ✅ `curl localhost:6333/collections` returns JSON
- ✅ MCP server listed in Claude Desktop
- ✅ Test search returns relevant results

---

### **Slice 1.3: Observer Automation** (2 days)

**Goal:** Scheduled drift detection every 30 minutes

**Steps:**
1. **Create systemd timer:** (Day 1)
   ```bash
   sudo tee /etc/systemd/system/observer.service <<EOF
   [Unit]
   Description=AI Life OS Observer (Drift Detection)
   
   [Service]
   Type=oneshot
   WorkingDirectory=/mnt/c/Users/edri2/Desktop/AI/ai-os
   ExecStart=C:/Program Files/Git/cmd/git.exe status --short
   ExecStartPost=/usr/bin/python3 tools/observer.py --mode=scheduled
   StandardOutput=append:/var/log/observer.log
   StandardError=append:/var/log/observer_errors.log
   EOF
   
   sudo tee /etc/systemd/system/observer.timer <<EOF
   [Unit]
   Description=Run Observer every 30 minutes
   
   [Timer]
   OnBootSec=5min
   OnUnitActiveSec=30min
   
   [Install]
   WantedBy=timers.target
   EOF
   
   sudo systemctl daemon-reload
   sudo systemctl enable observer.timer
   sudo systemctl start observer.timer
   ```

2. **Create n8n notification workflow:** (Day 2)
   - Trigger: Webhook (called by observer.py on drift detected)
   - Condition: Check drift severity (high/medium/low)
   - Action: Send Discord/Slack notification (batched if low severity)

3. **Update observer.py:**
   ```python
   # Add webhook notification
   import requests
   
   def notify_drift(drift_report):
       if drift_report['severity'] == 'high':
           # Immediate notification
           requests.post('http://localhost:5678/webhook/observer-drift', 
                         json=drift_report)
       else:
           # Batch for Daily Standup
           with open('truth-layer/drift/pending_notifications.jsonl', 'a') as f:
               f.write(json.dumps(drift_report) + '\n')
   ```

**Success Criteria:**
- ✅ `systemctl list-timers | grep observer` shows active timer
- ✅ 48 drift reports generated in 24 hours
- ✅ n8n workflow triggered on drift detection
- ✅ Low severity drifts batched (not spamming)

---

### **Slice 1.4: Watchdog Reconciler** (1 day)

**Goal:** Auto-commit Memory Bank updates (Protocol 1 automation)

**Steps:**
1. **Install watchdog library:**
   ```bash
   pip install --break-system-packages watchdog
   ```

2. **Create watchdog script:**
   ```python
   # tools/watchdog.py
   import time
   from watchdog.observers import Observer
   from watchdog.events import FileSystemEventHandler
   import subprocess
   
   class MemoryBankHandler(FileSystemEventHandler):
       def __init__(self):
           self.last_commit = time.time()
           self.debounce_seconds = 5
       
       def on_modified(self, event):
           if event.src_path.endswith('.md'):
               now = time.time()
               if now - self.last_commit > self.debounce_seconds:
                   self.commit_changes(event.src_path)
                   self.last_commit = now
       
       def commit_changes(self, filepath):
           subprocess.run([
               'C:/Program Files/Git/cmd/git.exe',
               'add', filepath
           ])
           subprocess.run([
               'C:/Program Files/Git/cmd/git.exe',
               'commit', '-m',
               f'Auto: Memory Bank update - {filepath}'
           ])
   
   if __name__ == '__main__':
       observer = Observer()
       handler = MemoryBankHandler()
       observer.schedule(handler, 'memory-bank/', recursive=True)
       observer.start()
       print("Watchdog active - monitoring Memory Bank...")
       try:
           while True:
               time.sleep(1)
       except KeyboardInterrupt:
           observer.stop()
       observer.join()
   ```

3. **Create systemd service:**
   ```bash
   sudo tee /etc/systemd/system/watchdog.service <<EOF
   [Unit]
   Description=Memory Bank Watchdog (Auto-commit)
   
   [Service]
   Type=simple
   Restart=always
   WorkingDirectory=/mnt/c/Users/edri2/Desktop/AI/ai-os
   ExecStart=/usr/bin/python3 tools/watchdog.py
   
   [Install]
   WantedBy=multi-user.target
   EOF
   
   sudo systemctl daemon-reload
   sudo systemctl enable watchdog.service
   sudo systemctl start watchdog.service
   ```

**Success Criteria:**
- ✅ Edit `01-active-context.md` → wait 5s → `git log` shows auto-commit
- ✅ `systemctl status watchdog` shows "active (running)"
- ✅ No commit spam (debounce working)

---

## 📋 Phase 2: Layer 3 Kernel (Weeks 3-5)

### **Slice 2.1: LangGraph Installation + Basic Graph** (3 days)

**Goal:** Supervisor-Worker pattern operational

**Steps:**
1. **Install dependencies:** (Day 1)
