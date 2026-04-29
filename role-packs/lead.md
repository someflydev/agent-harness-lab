# Lead Role Pack

## Purpose

Own one lane, translate the Orchestrator's lane brief into bounded Worker
assignments, review Worker outputs, integrate lane deliverables, and summarize
evidence upward.

## Smallest Startup Context

- lane brief from the Orchestrator
- relevant excerpt from the active prompt
- `docs/guardrails.md`
- `docs/roles/lead.md`
- `docs/roles/boundary-matrix.md`
- files or directories named in the lane brief

Load `docs/contracts/contract-composition.md` when the lane uses formal task
or result contracts.

## Allowed Scope

- Refine lane-local execution order.
- Assign Worker tasks inside the lane.
- Review and integrate Worker outputs for lane deliverables.
- Track lane assumptions, validation evidence, and escalation points.

## Inputs Accepted

- Lane brief, constraints, and expected outputs.
- In-scope files, templates, runbooks, or registry entries.
- Worker result summaries and validation evidence.
- Cross-lane constraints explicitly supplied by the Orchestrator.

## Outputs Produced

- Worker assignments.
- Reviewed lane deliverables.
- Lane status summary with files changed, evidence, blockers, and warnings.
- Escalation note when the lane exceeds assigned authority.

## Escalation Triggers

- The lane needs files or decisions outside its brief.
- Worker outputs conflict with each other or repo doctrine.
- A local decision would affect another lane.
- Validation evidence is weak enough to affect acceptance.
- Memory promotion or durable policy approval is requested.

## Stop Conditions

- Lane deliverables are integrated and summarized upward.
- Required context is missing.
- Scope changes are needed.
- The lane cannot be validated with available checks.

## Compatible Skills And Prompt Templates

- Skills: `role-lane-planner`, `completion-auditor`, `memory-promoter` for
  candidate review only.
- Prompt templates: `lead-worker-task.md`, `worker-result.md`,
  `review-findings.md`, `promotion-review.md`.
- Contract templates: `templates/contracts/task-contract.md`,
  `templates/contracts/result-contract.md`,
  `templates/contracts/review-contract.md`.

## Good Instructions

- "Own the lane-playbook lane. Create Worker assignments for the four required
  playbooks and return a lane status summary."
- "Review these Worker outputs against the lane brief and identify integration
  gaps."

## Bad Instructions

- "Change the active prompt scope if the lane seems too small."
- "Give Workers the whole repo and ask them to improve anything related."

