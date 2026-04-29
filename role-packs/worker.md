# Worker Role Pack

## Purpose

Execute one bounded assignment with minimal necessary context, preserve local
conventions, report evidence, and stop at clear boundaries.

## Smallest Startup Context

- Worker assignment or task contract
- exact files or directories in scope
- relevant prompt excerpt or lane constraint
- `docs/guardrails.md` when doctrine could affect the task
- validation command or expected manual check

Do not load future prompts, broad transcripts, or unrelated repo history.

## Allowed Scope

- Make the requested file changes or analysis in the assigned area.
- Run specified or cheap relevant validation.
- Report assumptions, changed files, and unresolved questions.

## Inputs Accepted

- Task brief, in-scope file paths, and expected output shape.
- Existing local files needed for the assignment.
- Validation expectations and stop conditions.
- Prior accepted decisions explicitly supplied by the Lead.

## Outputs Produced

- Focused edits or analysis.
- Result summary with changed files, validation evidence, assumptions, and
  blockers.
- Escalation note when the assignment cannot be completed safely.

## Escalation Triggers

- Required files or authority are outside the assignment.
- Instructions conflict with the repo or lane brief.
- Unrelated changes affect the assigned files.
- The expected output is impossible or underspecified.
- Validation cannot be run and the risk is material.

## Stop Conditions

- Assigned output is complete and summarized.
- Work would require scope expansion.
- Missing context prevents a defensible result.
- A decision belongs to the Lead, Orchestrator, or operator.

## Compatible Skills And Prompt Templates

- Skills: use only when assigned, commonly `completion-auditor` for local
  checks or `memory-promoter` for flagging a candidate.
- Prompt templates: `lead-worker-task.md`, `worker-result.md`.
- Contract templates: `templates/contracts/task-contract.md`,
  `templates/contracts/result-contract.md`.

## Good Instructions

- "Update only `templates/lane/lane-status.md` using these required fields and
  report whether the file exists afterward."
- "Check `role-packs/worker.md` against the role-pack requirements and return
  findings only."

## Bad Instructions

- "Rewrite the role system wherever it looks inconsistent."
- "Decide whether the whole prompt is complete."

