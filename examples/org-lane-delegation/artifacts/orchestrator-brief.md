# Orchestrator Brief

- Artifact id: example-org-orchestrator-brief
- Date: 2026-04-28
- Owner role: Orchestrator
- Prompt or lane: Examples navigation lane
- Permission posture: Local read/write only; no commit requested

## Lane Definition

- Goal: Add a compact examples entry to `docs/README.md` after the examples
  directory exists.
- Reason: Future fresh sessions should be able to discover illustrative
  examples from the main docs index.
- Lane owner: Documentation Lead.
- Worker need: One Worker can inspect existing navigation style and propose a
  small index patch.

## Authoritative Inputs

- `../../../docs/README.md`
- `../../../docs/guardrails.md`
- `../../../runbooks/fresh-session-prompt-run.md`
- `../../../templates/contracts/task-contract.md`
- `../../../templates/contracts/result-contract.md`
- `../../../templates/contracts/review-contract.md`

## Boundaries

- In scope: Navigation wording for examples and reports adjacency.
- Out of scope: New scripts, prompt generation, runtime automation, broad docs
  rewrite.
- Escalate if: The docs index has no clear place for examples, the examples
  directory is missing, or the change would imply implemented runtime features
  that do not exist.

## Expected Upward Summary

- Files changed.
- Evidence reviewed.
- Whether the lane is accepted, needs repair, or should be escalated.
