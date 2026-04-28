# Run Closeout

## Purpose

Leave the repo understandable, validated, and ready for review or the next
fresh session.

## When To Use It

Use at the end of prompt-execution, repair, bridge, review, or prompt-authoring
sessions.

## Required Context To Load

- Active prompt or operator request.
- Completion audit or repair result.
- Validation evidence.
- Immediate next prompt readiness result, when applicable.
- `git status --short`.
- `templates/session-closeout.md` when a structured closeout record is needed.

## Roles Involved

- Orchestrator: owns closeout and reset.
- Completion Auditor: supplies active-work result.
- Next-Prompt Readiness Checker: supplies readiness label when applicable.
- Operator: decides whether to commit or start another session.

## Step-By-Step Procedure

1. Confirm no task-relevant command sessions are still running.
2. Confirm required artifacts exist.
3. Confirm navigation links to new durable artifacts.
4. Review changed docs for claims that exceed current capabilities.
5. Run or summarize validation checks.
6. Run `git status --short` and distinguish task changes from unrelated user
   changes.
7. State whether a bridge fix or `tmp/HANDOFF.md` was created.
8. State next-prompt readiness when the workflow requires it.
9. State that no commit was made unless the operator asked for one.
10. Keep routine completion notes in the final answer instead of creating
    unnecessary temporary memory.

## Expected Artifacts

- Final closeout summary.
- Optional session closeout record using `templates/session-closeout.md`.
- Optional `tmp/HANDOFF.md` only for a real blocker or non-trivial warning.
- No leftover temporary files without a purpose.

## Validation Or Evidence

- Required paths and links were checked.
- Validation commands or manual checks are listed.
- Readiness is labeled `ready`, `risky`, or `blocked` when applicable.
- Git status is known at closeout.

## Stop Conditions

- A required deliverable is missing.
- A validation command is still running or failed without disposition.
- Task-related changes are unexplained.
- A blocker requires handoff or operator direction.

## Common Failure Modes

- Ending before validation finishes.
- Omitting immediate next-prompt readiness.
- Leaving a handoff for routine summary notes.
- Forgetting to mention unrelated pre-existing changes.
