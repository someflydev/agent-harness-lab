# Orchestrator Lane Plan

Purpose: turn a bounded operator request or active prompt into lanes with clear
owners, context, outputs, and stop conditions.

## Prompt

Plan lanes for `<WORK_SCOPE>` and produce assignments for Leads without doing
the lane implementation.

## Placeholders

- `<WORK_SCOPE>`: active prompt, repair target, or operator request.
- `<LANE_CANDIDATES>`: expected workstreams, if known.
- `<CONSTRAINTS>`: scope, permission, sequencing, or validation limits.
- `<OUTPUT_FORMAT>`: requested plan shape.

## Required Context To Load

- `docs/roles/org-model.md`
- `docs/roles/orchestrator.md`
- `<WORK_SCOPE>` source file or operator request
- Relevant guardrails and runbooks
- Current repo status when implementation may follow

## Expected Output

- Lane list with purpose, in-scope files, owner role, required context, expected
  output, validation, escalation triggers, and stop conditions.
- Cross-lane risks or dependencies.
- Explicit items that remain operator decisions.

## Stop Conditions

- Lane planning would require implementing the work.
- Scope is ambiguous enough to create durable project direction by guessing.
- A lane would need context outside the repo or operator-approved sources.

