# System Snapshot – Updated SSOT and GPT Actions Integration
### Date: 2025-11-23

## SSOT Update Service
The SSOT Update Service is a new subsystem within the aaios architecture, responsible for maintaining the accession and consistency of SSOT documentation.

- ** Endpoint:** `POST /ssot/update`
- **Scope:** SSOT-related documents under `docs/`:
  - `SYSTEM_SNAPSHOT.md`
  - `CAPABILITIES_MATRXIC.md`
  - `DECISIONS_AI_OS.md`
 - and other SSOT-related references
- **Functionality:*
  - Receives a JSON payload with target doc and new content.
  - Validates that only permitted docs can be updated.
  - Creates a automated commit with push to the git repo.
  - Logs all updates for auditability.
  - Requires explicit human approval (policy) from Or before commit - not enforced by code.

This service centralizes documentation updates and ensures consistency across all SSOT layers.

---

## GPT with Actions (ai_os_github_ssot)
The GPT with Actions operates as an SSOT Updater Agent, connected to the GitHub repository `edri2or-commits/ai-os`.

- **Type:** GitHub REST API tool
- **Permissions:*
  - Read/Write access to Markdown documents (`docs/` only).
  - Read-only access to SSOT references; no code or workflow updates.
- **Approval Model:** All write operations require explicit human approval from Or prior to commit (policy).
 - **Use Case:*
  - Automates SWOT  document alignments and structured updates after system changes.

__
The GPT stays within the documentation domain only and never changes code, workflows, or scripts.

This service is referenced by the SSOT Update Service and ensures auditable and consistent synchronization between architecture and documentation.
