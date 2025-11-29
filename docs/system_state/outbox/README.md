# PR Intents - Transactional Outbox

This file stores PR creation intents for the Sync Write Contract.

## Format
JSONL (one JSON object per line)

## Schema
See: docs/sync_contracts/SLICE_SYNC_WRITE_CONTRACT_PR_V1_SPEC.md

## Usage
- Create intents: python scripts/create_pr_intent.py
- Process intents: python scripts/pr_worker.py
