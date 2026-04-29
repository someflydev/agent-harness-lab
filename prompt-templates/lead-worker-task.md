# Lead-To-Worker Task

Purpose: assign one bounded Worker task from a Lead while preserving lane scope
and escalation boundaries.

## Prompt

Worker: complete `<TASK_SCOPE>` for `<LANE_NAME>` using only the context and
files listed below, then report results in the requested format.

## Placeholders

- `<LANE_NAME>`: Lead-owned lane.
- `<TASK_SCOPE>`: narrow Worker assignment.
- `<IN_SCOPE_PATHS>`: files or directories the Worker may inspect or edit.
- `<REQUIRED_CONTEXT>`: docs or contracts the Worker must load.
- `<DONE_CHECK>`: validation or manual check proving completion.

## Required Context To Load

- `<REQUIRED_CONTEXT>`
- `<IN_SCOPE_PATHS>`
- Relevant task contract if one exists
- Current `git status --short` when edits are allowed

## Expected Output

- Changed files or explicit no-change result.
- Evidence from `<DONE_CHECK>`.
- Assumptions, unresolved questions, and escalation triggers hit.
- Stop condition reached.

## Stop Conditions

- The task requires editing outside `<IN_SCOPE_PATHS>`.
- Required context is missing.
- The Worker needs a design, policy, or sequencing decision.
- Validation cannot be performed.

