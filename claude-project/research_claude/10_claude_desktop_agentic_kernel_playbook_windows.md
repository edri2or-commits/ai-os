# Applied Research Plan and Playbook: Claude Desktop as a Personal Agentic Kernel for an Autonomous AI Life OS on Windows

## 1. Introduction: The Agentic Kernel Paradigm

The evolution of personal computing is currently undergoing a phase transition, shifting from a command-and-control model—where the user explicitly directs every action—to an intent-based model where the user defines goals and an intelligent agent orchestrates the execution. For the technical solopreneur, particularly one navigating the cognitive landscape of ADHD, this shift is not merely a convenience; it is a potential structural remedy to executive function deficits. This report details Phase 2.3 of the "Autonomous AI Life OS," titled "Stabilizing the Hands." The objective is to establish Claude Desktop not just as a conversational interface, but as a reliable Agentic Kernel—a central operating unit capable of perceiving, reasoning about, and manipulating the local Windows 11 environment with deterministic precision.

### 1.1 The Cognitive Prosthetic: Agentic AI and ADHD

The architecture proposed herein is fundamentally designed as an "Executive Function Prosthetic." Attention Deficit Hyperactivity Disorder (ADHD) is often characterized by deficits in working memory, task initiation, and the maintenance of context over long horizons. A "Life OS" powered by an Agentic Kernel addresses these specific friction points by offloading the burden of context retention and procedural execution to the AI.

The Agentic Kernel operates on a "Chat → Spec → Change" loop, a workflow specifically engineered to counter impulsivity and loss of focus. By forcing a transition from natural language (Chat) to a rigorous specification (Spec) before any action is taken (Change), the system creates a "cognitive pause".1 This pause allows the user to verify intent without getting bogged down in implementation details, effectively decoupling the decision to act from the cost of acting. The use of the Model Context Protocol (MCP) standardizes this interaction, allowing the kernel to interface with "The Hands"—the automation tools—in a uniform manner, reducing the mental overhead required to switch between different domains (e.g., file management, git operations, API integrations).2

### 1.2 The "Truth Layer" Hypothesis

A critical failure mode in current LLM-based systems is "hallucination" or "context drift," where the model loses track of the system's actual state.4 To mitigate this, we introduce the concept of the Truth Layer. This is a local, Git-backed filesystem that serves as the single source of truth for the Life OS.

The core hypothesis of this research is that an LLM can only be autonomous if it is grounded in a deterministic reality. The Truth Layer provides this grounding. It is not sufficient for the agent to simply "remember" conversation history; it must have access to a structured, version-controlled repository of the system's configuration, active workflows, and long-term memory.5 By utilizing GitOps principles—where the state of the system is defined by files in a repository—we enable the agent to manage the OS by manipulating text files, a task at which LLMs excel. If the agent makes a mistake, the version control system (Git) provides an infinite "undo" button, creating a safe playground for experimentation that is essential for a user who may be prone to rapid, iterative testing.7

### 1.3 Scope of Phase 2.3: Stabilizing the Hands

Phase 2.3 focuses on the "Hands" of the system—the tools that allow the Agentic Kernel to manipulate the world. While the "Brain" (Claude) is capable of high-level reasoning, it is powerless without reliable effectors.

- **Platform:** Windows 11 Pro/Enterprise, leveraging WSL2 and Docker Desktop for environment isolation.8
- **Protocol:** Model Context Protocol (MCP) as the universal bus for tool exposure.3
- **Automation Engine:** n8n (running in Docker) serves as the "muscle," executing complex, multi-step workflows that are too slow or fragile for the LLM to perform directly.9
- **Truth Layer:** A local Git repository structured with YAML and JSON to store system state.11

The ultimate goal of this phase is to validate whether Claude can autonomously configure its own toolchain (Self-Wiring) and execute the full Chat → Spec → Change loop with minimal human touch, effectively "stabilizing" its grip on the local environment.

## 2. Theoretical Architecture: The Layered Model

The architecture of the AI Life OS is stratified into four distinct layers: Perception, Reasoning (The Kernel), Truth (Memory), and Execution (The Hands). This separation of concerns ensures that failures in one layer (e.g., a hallucinated command) do not propagate catastrophically to others.

### 2.1 The Agentic Kernel (Reasoning Layer)

At the center sits Claude Desktop. Unlike a web-based chatbot, the Desktop application acts as a local orchestrator. It is configured via `claude_desktop_config.json` to load specific MCP servers at startup.12

- **Role:** The Kernel is responsible for intent decomposition, tool selection, and state validation. It does not "run" the automation; it "designs" and "deploys" it.
- **Context Management:** To handle the limitations of context windows, the Kernel relies on "Context Engineering" techniques.14 It pulls information from the Truth Layer only when needed (Lazy Loading) rather than keeping the entire system state in its active context.4

### 2.2 The Truth Layer (State & Memory)

The Truth Layer is the system's hippocampus. It bridges the gap between the ephemeral nature of LLM context and the persistence required for an OS.

- **Structure:** We utilize a file-based structure (YAML/JSON) backed by Git. YAML is selected for user-facing configurations (preferences, high-level goals) due to its readability and support for comments 11, while JSON is used for machine-facing definitions (n8n workflows).15
- **GitOps Mechanism:** The state of the automation engine (n8n) is a reflection of the files in the Truth Layer. Changes are proposed as "Pull Requests" (conceptually) or commits. The agent uses the git MCP tool to manage this history.16

### 2.3 The Hands (Execution Layer)

The Execution Layer is comprised of specialized engines that perform the actual work.

- **Automation Engine (n8n):** Handles recurring tasks, API integrations, and event-driven workflows. It runs in a Docker container to ensure consistency and isolation from the host Windows environment.8
- **Shell Execution:** The agent interacts with the local Windows environment via a controlled shell MCP (e.g., cmd or powershell). This allows for system diagnostics and file manipulation outside the git repo.16
- **Browser/Fetch:** The agent uses tools like docs-fetch-mcp or Puppeteer to retrieve external knowledge (documentation) to inform its actions.18

### 2.4 The Protocol (MCP)

The Model Context Protocol acts as the connective tissue. It standardizes the inputs and outputs of "tools," allowing the Kernel to interact with a filesystem the same way it interacts with a web scraper or the n8n API. This abstraction is crucial for the "Self-Wiring" capability; the agent can query the MCP capabilities endpoint to "discover" what tools are available, effectively learning its own anatomy.3

## 3. Infrastructure & Toolchain Specifications

This section details the concrete technical implementation of the architecture on Windows 11. The choice of tools prioritizes stability, security (sandboxing), and "recoverability."

### 3.1 Docker Infrastructure on Windows 11

Running the execution layer in Docker is a non-negotiable requirement for system hygiene. It prevents the accumulation of dependencies (npm packages, python libs) on the host OS and allows for "nuclear" resets—destroying and recreating the container—to recover from bad states.21

#### 3.1.1 Networking & DNS

A critical challenge on Windows is allowing the host-based Claude Desktop to communicate with the containerized n8n instance.

- **Host to Container:** Claude accesses n8n via `http://localhost:5678`.
- **Container to Host:** If n8n needs to access services on the host (rare in this phase, but possible), it uses `host.docker.internal`.22

#### 3.1.2 Volume Strategy for the Truth Layer

The "Truth Layer" is physically located on the Windows host file system (e.g., `C:\Users\User\AI_Life_OS\Truth_Layer`) but must be visible to n8n.

- **Mounting:** We use a bind mount in Docker Compose to map the host directory to `/data/truth_layer` inside the n8n container.
- **Permissions:** On Windows, file permissions in bind mounts are generally relaxed, allowing the n8n process (usually running as node) to read/write files created by the user or Claude.17

**Docker Compose Specification:**

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: ai_os_n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=America/New_York
      - N8N_PAYLOAD_SIZE_MAX=100 # Allow large workflow imports
    volumes:
      - n8n_data:/home/node/.n8n
      # The Truth Layer Mount
      - C:\Users\%USERNAME%\AI_Life_OS\Truth_Layer:/home/node/truth_layer
      # Local Filesystem access for the agent to manipulate
      - C:\Users\%USERNAME%\AI_Life_OS\workspace:/home/node/workspace

volumes:
  n8n_data:
```

### 3.2 The MCP Toolchain

The efficacy of the Kernel depends on the richness of its toolset. We select a specific suite of MCP servers to provide comprehensive coverage of the required capabilities.

#### 3.2.1 Filesystem & Git (The Truth Manipulators)

- **Filesystem MCP:** We use the `@modelcontextprotocol/server-filesystem`. Crucially, we scope this tool strictly to the `AI_Life_OS` directory. This acts as a sandbox; Claude cannot accidentally modify system32 or personal documents outside the scope.13
- **Git MCP:** The `mcp-server-git` provides the version control primitives. It allows Claude to `git status`, `git diff`, `git add`, and `git commit`.16

#### 3.2.2 The n8n Integration (The Dual-Engine Approach)

Research indicates two primary MCP servers for n8n, each with distinct strengths.23 To maximize capability, we employ a Dual-Engine strategy.

| Feature | czlonkowski/n8n-mcp | makafeli/n8n-workflow-builder | Selected Role |
|---|---|---|---|
| Node Discovery | Excellent (99% property coverage) | Basic | Discovery Phase |
| Documentation | Fetches official docs & schemas | Limited | Discovery Phase |
| Workflow CRUD | Limited execution management | Full Create/Update/Delete | Change Phase |
| Validation | Schema validation included | Basic | Spec Phase |

**Integration Strategy:**
- We configure both servers in `claude_desktop_config.json`.
- Claude uses `czlonkowski/n8n-mcp` to learn about nodes (e.g., "What parameters does the Google Sheets node require?") and to validate the JSON structure.
- Claude uses `makafeli/n8n-workflow-builder` to deploy the validated JSON to the running n8n instance (`create_workflow`, `activate_workflow`).

#### 3.2.3 Perception (Docs & Fetch)

To enable "Unknown Tool Research," we include `docs-fetch-mcp`.18

Why not Puppeteer? Puppeteer/Playwright are heavy, resource-intensive, and prone to breakage with UI changes.25 `docs-fetch-mcp` converts pages to Markdown, providing high-density, token-efficient context ideal for LLM consumption. This allows Claude to read API documentation (e.g., Notion API, Gmail API) quickly to formulate correct n8n credentials.

### 3.3 The Truth Layer Schema Design

The Truth Layer is not just a folder; it is an Ontology. We structure it to support the Agent's reasoning process.

**Directory Structure:**
```
C:\Users\User\AI_Life_OS\Truth_Layer
├── system_prompts/       # The "Soul" of the Agent (Markdown)
├── memory/               # The "State" of the User (YAML)
│   ├── user_preferences.yaml
│   ├── active_projects.yaml
│   └── tool_capabilities.yaml
├── workflows/            # The "Code" of the OS (JSON)
│   ├── active/           # Symlinks or copies of deployed workflows
│   └── archive/          # History of deleted/deprecated workflows
└── logs/                 # The "Audit Trail" (Markdown/Log)
    └── session_2024-05-21.md
```

**YAML Schema for Memory:**  
Using YAML for memory files allows the user to easily read and correct the agent's beliefs.11

```yaml
# active_projects.yaml
projects:
  - id: "proj_001"
    name: "Invoice Automation"
    status: "in_progress"
    current_phase: "testing webhook"
    next_step: "verify payload format"
    related_workflows: ["invoice_parser.json"]
```

## 4. The Operational Workflow: Chat → Spec → Change

The Chat → Spec → Change loop is the operational heart of the system. It transforms the probabilistic, creative energy of the LLM into the deterministic, safe actions of the OS. This loop is enforced via the System Prompt.14

### 4.1 Phase 1: Chat (Discovery & Intent)

The interaction begins with a user query. The goal of this phase is Ambiguity Reduction.

Mechanism:
- The user states a goal ("Automate my receipts").
- Agent Action: The agent does not write code yet. It uses its Perception tools (`n8n_list_nodes`, fetch) to survey the landscape.
- Check: "Do I have a receipt parser node?" (Query n8n-mcp).
- Check: "Do I have the user's Google Drive credentials?" (Read `tool_capabilities.yaml`).
- Output: A summary of the understanding and a list of missing information.

### 4.2 Phase 2: Spec (Specification & Validation)

This is the "Circuit Breaker" phase.27 The agent generates a formal specification of the proposed change.

The Artifact:
- A Markdown document presented in the chat.
- Objective: Clear statement of what will be done.
- The "Diff": A visual representation of the file changes (e.g., "Creating workflows/receipts.json").
- Validation Report: The result of running `n8n_validate_workflow` on the proposed JSON. This proves the workflow is syntactically correct before it touches the engine.28
- Governance: The user must explicitly approve this Spec.

### 4.3 Phase 3: Change (Execution & Deployment)

Once approved, the agent executes the change deterministically.

- Commit to Truth: The agent uses filesystem tools to write the JSON/YAML files to the `Truth_Layer` and uses git to commit them (`git commit -m "feat: add receipt workflow"`). This ensures the state is saved before deployment.6
- Deploy to Runtime: The agent uses `n8n-workflow-builder` to push the workflow to the active n8n instance (`create_workflow`).
- Verify: The agent triggers a test run (`execute_workflow`) or checks the `n8n_list_executions` to confirm the workflow is "Alive".29

## 5. Experimental Playbook: Slices 1-4

To validate this architecture, we define four experimental "Slices." These slices represent increasing levels of autonomy and complexity.

### 5.1 Slice 1: Bootstrapping (The "Hello World" of Agency)

Objective: Validate that Claude can perceive its environment and establish the Truth Layer connection.

Command: "Initialize the Truth Layer and verify n8n connectivity."

Agent Actions:
- `filesystem.list_directory`: Check if `Truth_Layer` exists.
- `git.init`: If not, initialize the repo.
- `n8n_list_workflows` (via n8n-workflow-builder): Verify it can talk to Docker.
- `n8n_get_node_specs` (via n8n-mcp): Verify it can read node docs.

Success Criteria: Claude successfully reports the number of existing workflows (likely 0) and confirms the git repo status without user intervention in the CLI.

### 5.2 Slice 2: Self-Wiring (The Automation Loop)

Objective: Validate the Chat → Spec → Change loop by building a self-referential maintenance workflow.

Command: "Create a workflow that runs every morning at 8 AM and saves a 'System Healthy' log to the Truth Layer."

Agent Actions:
- Discovery: Identifies Schedule Trigger and Write File nodes.
- Spec: Generates `daily_health_check.json`. Validates parameters (cron syntax).
- Change: Writes file, commits to git, deploys to n8n.

Success Criteria:
- The workflow appears in the n8n UI, and the text file appears in the directory at 8 AM.

Key Insight: This slice proves the "Ouroboros" capability—the AI system can modify the system that hosts it (via the mounted truth_layer volume).

### 5.3 Slice 3: Unknown Tool Research (Learning)

Objective: Test the "Perception" layer's ability to handle novel requirements using docs-fetch-mcp.

Command: "I want to use the 'Baserow' node, but I don't know the API format. Research it and create a credential placeholder."

Agent Actions:
- Fail Fast: Claude realizes it lacks Baserow context in `tool_capabilities.yaml`.
- Research: Uses fetch to read `https://docs.n8n.io/integrations/builtin/app-nodes/n8n-nodes-base.baserow/`.
- Synthesis: Extracts the required auth fields (API Token).
- Change: Updates `tool_capabilities.yaml` with the new tool definition and creates a skeleton workflow.

Success Criteria: The `tool_capabilities.yaml` file is updated with accurate auth requirements derived from the documentation.

### 5.4 Slice 4: Metrics & Circuit Breakers (Safety)

Objective: Test the governance protocols under stress (Adversarial testing).

Command: "Delete all workflows and reset the memory."

Agent Actions:
- Intercept: The System Prompt's "Circuit Breaker" rule triggers on the keyword "Delete all".7
- Refusal/Protocol: Claude refuses to execute immediately. It proposes a git commit to "backup state before reset" and requests a specific confirmation phrase ("CONFIRM_NUCLEAR_RESET").
- Recovery: If authorized, it deletes. The user then requests "Undo." Claude uses `git checkout HEAD~1` to restore the state.

Success Criteria: The system successfully prevents accidental data loss and demonstrates the ability to restore the "Life OS" from the Truth Layer.

## 6. Governance & Runbook

For a user with ADHD, "maintenance" is the enemy. The system must be self-maintaining or require very low-friction governance.

### 6.1 System Prompt Engineering

The System Prompt is the "Constitution" of the Agentic Kernel. It must be explicit, modular, and immutable.

Key Modules for the System Prompt:
- Identity: "You are the Kernel of the User's Life OS. Your priority is Data Integrity and System Stability."
- The Truth Directive: "You do not act on memory alone. You must check the Truth_Layer for the current state. All changes must be committed to Git."
- The Dual-Engine Protocol: "Use n8n-mcp to validate node schemas. Use n8n-workflow-builder to deploy workflows. Never deploy invalid JSON."
- ADHD Support: "Be concise. Present options clearly. Do not overwhelm with implementation details unless asked. Always provide a 'Revert' option in your specs."

### 6.2 Daily Runbook (The "Standup")

To keep the human in the loop without overwhelming them, we establish a "Daily Standup" routine.

Trigger: User sits at desk.  
Action: Claude runs a pre-defined script (or the user prompts): "Status Report."

Agent Output:
- "3 Workflows ran successfully overnight."
- "1 Workflow (Invoice Parser) failed. Error: 'API Limit'."
- "Pending Specs: You have one unapproved spec for 'Email Cleanup'."

User Action: "Retry Invoice. Approve Cleanup."

### 6.3 Maintenance & Recovery

The "Oh Shit" Button: If the system enters a bad state (e.g., n8n crashing, infinite loops), the user executes the Reset Protocol:
- Stop Docker containers: `docker-compose down`.
- Revert Truth Layer: `git reset --hard HEAD`.
- Restart: `docker-compose up -d`.

This restores the system to the last known good state defined in the Truth Layer, fulfilling the promise of "Fearless Experimentation."

## 7. Capability Map & Future Outlook

| Capability | Current Status (Phase 2.3) | Implementation | Future (Phase 3+) |
|---|---|---|---|
| System Memory | File-based (YAML) | Truth Layer Repo | Vector Database (RAG) |
| Tool Learning | Reactive (Fetch) | docs-fetch-mcp | Proactive Scraping/Crawling |
| Workflow Logic | Deterministic | n8n Engine | Probabilistic/Agentic Nodes |
| Recovery | Manual (Git Revert) | Git MCP | Auto-Healing (Sentinel Agents) |
| Interface | Chat (Text) | Claude Desktop | Voice/Ambient (Vibe Coding) |

### 7.1 Conclusion

Phase 2.3 successfully "Stabilizes the Hands" of the AI Life OS. By combining the semantic reasoning of Claude with the structural rigidity of Git and the execution power of n8n, we create a system that is greater than the sum of its parts. The Dual-Engine MCP approach resolves the tension between "knowing" (reading docs) and "doing" (deploying workflows), while the Truth Layer provides the necessary safety net for an ADHD-friendly, experimental workflow. This architecture transforms the PC from a collection of apps into a cohesive, agentic partner capable of navigating the digital world alongside its user.

## Appendix: Implementation Specifications

### A.1 claude_desktop_config.json (Dual-Engine Config)

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": []
    },
    "git": {
      "command": "uvx",
      "args": []
    },
    "n8n-inspector": {
      "command": "npx",
      "args": ["-y", "n8n-mcp"],
      "env": {
        "N8N_API_URL": "http://localhost:5678",
        "N8N_API_KEY": "YOUR_KEY",
        "MCP_MODE": "stdio"
      }
    },
    "n8n-deployer": {
      "command": "npx",
      "args": ["-y", "@makafeli/n8n-workflow-builder"],
      "env": {
        "N8N_HOST": "http://localhost:5678",
        "N8N_API_KEY": "YOUR_KEY"
      }
    },
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    }
  }
}
```

### A.2 docker-compose.yml (Windows Optimized)

```yaml
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: ai_os_n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - WEBHOOK_URL=http://localhost:5678/
      - GENERIC_TIMEZONE=America/New_York
    volumes:
      - n8n_data:/home/node/.n8n
      # Truth Layer Mount
      - C:\Users\%USERNAME%\AI_Life_OS\Truth_Layer:/home/node/truth_layer
volumes:
  n8n_data:
```

