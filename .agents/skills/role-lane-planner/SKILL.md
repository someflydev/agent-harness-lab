---
name: role-lane-planner
description: Decompose bounded work into Orchestrator, Lead, and Worker lanes with clear ownership, outputs, and escalation points.
---

## When To Use

Use when work is large enough to need role boundaries or parallel lanes, or when
an operator asks for Orchestrator, Lead, or Worker decomposition. Do not use for
small single-file changes where a role split adds overhead.

## Required Context

- Active prompt or task brief
- `docs/roles/org-model.md`
- `docs/roles/boundary-matrix.md`
- `docs/contracts/contract-composition.md`
- Relevant prompt templates for lane assignments

## Step-By-Step Behavior

1. Extract the task goal, required outputs, and constraints.
2. Assign Orchestrator responsibilities for scope, validation, and closeout.
3. Split Lead lanes by artifact boundary or problem area.
4. Define Worker tasks with disjoint write scopes when edits are delegated.
5. Name expected contracts, evidence, and escalation triggers.
6. Keep lane count proportional to the task.

## Expected Output

- Lane plan with role ownership
- Inputs, outputs, and stop conditions for each lane
- Escalation path for conflicts or blocked work
- Validation and integration responsibilities

## Stop Conditions

- The task is too small for lane planning.
- Ownership boundaries cannot be made disjoint enough for delegation.
- Operator approval is needed to spawn or assign agents.

## Safety Notes

- Roles describe responsibility; they are not separate tools by themselves.
- Do not create hidden autonomy or bypass operator control.
- Preserve repo artifact boundaries when splitting work.

## References

- `docs/roles/org-model.md`
- `docs/roles/boundary-matrix.md`
- `docs/contracts/contract-composition.md`
- `prompt-templates/orchestrator-lane-plan.md`
- `prompt-templates/lead-worker-task.md`
- `prompt-templates/worker-result.md`
