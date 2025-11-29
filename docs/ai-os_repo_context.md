# ai-os – Repo Context for GPT (Route Recalculation Phase)

**Date (UTC):** 2025-11-24  
**Repo:** edri2or-commits/ai-os  
**Branch:** main  
**Purpose:** Provide GPT with a full synchronized context of the system’s architecture, principles, and state.

---

## REPO_ROOT_TREE
```
.
├── .dockerignore
├── .env.template
├── .gitignore
├── Dockerfile
├── Dockerfile.google
├── HOTFIX_CONFIG.txt
├── README.md
├── SSOT_UPDATE_SERVICE_README.md
├── START_README.md
├── agents/
├── ai_core/
├── archive/
├── chat/
├── check_health.py
├── demo_loop.py
├── demo_plan.json
├── docs/
├── execute_demo.py
├── plan_output.json
├── policies/
├── requirements.txt
├── run_intent.py
├── run_iron_test.py
├── services/
├── setup_env.py
├── start-all-services.bat
├── start.bat
├── start.py
├── start_chat1.py
├── start_github_client.py
├── start_public_server.py
├── sync_api_key.py
├── temp_plan.json
├── test_e2e.py
├── test_gateway.py
├── test_real_gpt.py
├── test_slice2.py
├── test_slice3.py
├── test_ssot_update.py
├── tools/
├── workflows/
└── test-gpt-integration.txt
```

---

## DOCS_TREE
```
docs/
├── ACTION_EXECUTION_SCHEMA.md
├── AGENT_GATEWAY_API.md
├── AGENT_GATEWAY_HTTP_API.md
├── AGENT_ONBOARDING.md
├── API_KEY_MANAGEMENT.md
├── CAPABILITIES_MATRIX.md
├── CHAT1_INTEGRATION.md
├── CHAT1_STATUS.md
├── CLAUDE_DESKTOP_CAPABILITIES.md
├── CONSTITUTION.md
├── DECISIONS_AI_OS.md
├── GPT_MCP_SPEC.md
├── GPT_PLANNER_CONTRACT.md
├── HUMAN_TECH_POLICY_SOURCES.md
├── IRON_TEST_SUMMARY.md
├── LOCAL_WORKSPACES.md
├── PUBLIC_HTTPS_SETUP.md
├── SECURITY_DISCOVERY_REPORT_config_2025-11-20.md
├── SESSION_INIT_CHECKLIST.md
├── SETUP.md
├── SYSTEM_SNAPSHOT.md
├── TEST_ACTION_EXECUTOR.md
└── TOOL_LIMITATIONS.md
```

---

## SYNTHESIS_FOR_GPT
- AI-OS operates as a **self-documenting personal AI operating system** with layered architecture linking GPT, Claude, and human-in-the-loop decision-making.
- The repo itself acts as **SSOT (Single Source of Truth)**: every agent, policy, and workflow references these Markdown documents.
- **Human approval** is mandatory for destructive or system-changing actions.
- **Claude Desktop** = local executor (MCP access), **GPT** = architect/planner, **Or** = human owner.
- System state (per `SYSTEM_SNAPSHOT.md`) confirms two MCP clients (GitHub + Google) are active, fully operational, and tunnelled via ngrok.
- `AGENT_ONBOARDING.md` defines onboarding, safety, and workflow discipline for all AI agents joining the system.
- `SESSION_INIT_CHECKLIST.md` introduces a standard session boot procedure ensuring all agents start with synced state.
- `GPT_MCP_SPEC.md` details future architecture for GPT’s direct MCP access with strict safety/approval tiers (L0–L4).
- `LOCAL_WORKSPACES.md` maps all local and legacy folders, clarifying canonical workspaces and reducing risk of version drift.
- **Direction of evolution:** consolidation, safety automation, and migration from local execution to MCP-enabled hybrid autonomy.

---

**End of export – 2025-11-24**