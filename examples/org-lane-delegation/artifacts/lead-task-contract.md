# Task Contract

- Artifact id: example-org-lead-task
- Date: 2026-04-28
- Owner role: Documentation Lead
- Assigned by: Orchestrator
- Prompt or lane: Examples navigation lane
- Permission posture: Local read/write only; no commit requested

## Scope

- Goal: Coordinate a small docs navigation update for examples.
- In scope: Review existing `docs/README.md` structure, assign one Worker task,
  review the Worker result, and summarize lane status upward.
- Out of scope: Editing unrelated docs sections, creating scripts, changing
  prompts, committing.
- Target files or areas: `docs/README.md`; `examples/README.md` only as
  evidence.

## Inputs

- Authoritative docs or prompts: Orchestrator brief, `../../../docs/README.md`,
  `../../../docs/guardrails.md`, `../../../docs/roles/org-model.md`.
- Existing artifacts: `../../../examples/README.md`.
- Assumptions: The examples directory exists before the navigation update is
  proposed.

## Expected Outputs

- Deliverables: Worker task contract, Worker result, Lead review.
- Result format: Review contract with accepted, repair, or escalation
  disposition.
- Completion condition: Navigation update is reviewed against docs style and
  does not overstate repo capabilities.

## Validation

- Checks to run: Inspect links and confirm target paths exist.
- Evidence required: File paths checked and review disposition.
- Reviewer: Orchestrator.

## Boundaries

- Escalation triggers: Missing examples directory, ambiguous durable location,
  or wording that claims production runtime behavior.
- Stop conditions: Worker reports a blocker or the Lead finds a blocking
  review issue.
- Open issues or blockers: None at assignment time.
- Next step: Issue bounded Worker task.
