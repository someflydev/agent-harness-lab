# Repair Session

Purpose: fix a bounded blocker, validation failure, or small reviewed gap
without reopening the whole original prompt.

## Prompt

Repair `<DEFECT>` in `<AFFECTED_PATHS>` and stop when `<DONE_CHECK>` proves the
issue is resolved.

## Placeholders

- `<DEFECT>`: specific issue to repair.
- `<AFFECTED_PATHS>`: files or directories in scope.
- `<ORIGINAL_PROMPT_PATH>`: original prompt, if needed.
- `<DONE_CHECK>`: command or manual check proving repair.
- `<HANDOFF_PATH>`: active handoff path, if relevant.

## Required Context To Load

- `AGENT.md`
- Operator repair request
- `<HANDOFF_PATH>` if present and relevant
- `<ORIGINAL_PROMPT_PATH>` only if needed to verify the defect
- `<AFFECTED_PATHS>`
- `runbooks/repair-session.md`

## Expected Output

- Focused repair changes.
- Validation evidence from `<DONE_CHECK>`.
- Remaining risk or operator decision, if any.
- Clear distinction between repair changes and unrelated worktree changes.

## Stop Conditions

- The defect cannot be reproduced or explained.
- The repair scope expands beyond `<DEFECT>`.
- Fixing the issue requires an operator policy or sequencing decision.
- Validation cannot run for reasons unrelated to the repair.

