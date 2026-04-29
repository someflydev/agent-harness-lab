# Worker Result

Purpose: report a bounded Worker task upward without raw transcript or unrelated
context.

## Prompt

Summarize the result of `<TASK_SCOPE>` for `<LANE_NAME>` with concrete evidence
and any escalation needs.

## Placeholders

- `<LANE_NAME>`: lane that owned the task.
- `<TASK_SCOPE>`: assigned Worker task.
- `<CHANGED_PATHS>`: paths changed or inspected.
- `<VALIDATION_EVIDENCE>`: checks run and outcomes.
- `<STOP_CONDITION>`: reason the Worker stopped.

## Required Context To Load

- Original Worker assignment.
- Relevant changed files or diff.
- `<VALIDATION_EVIDENCE>`.
- Any error, blocker, or unresolved question.

## Expected Output

- Result status: `complete`, `incomplete`, or `blocked`.
- Changed paths and behavior or documentation impact.
- Validation evidence.
- Open questions, risks, and next safe action if blocked.

## Stop Conditions

- The report would require inventing context not present in the assignment or
  evidence.
- The Worker is being asked to approve lane completion.
- Missing evidence prevents a reliable result statement.

