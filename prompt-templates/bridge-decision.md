# Bridge Decision

Purpose: decide whether a cheap bridge fix or temporary handoff is justified
after audit or preflight.

## Prompt

Given `<BLOCKER_OR_WARNING>`, decide whether to apply a small bridge fix, write
`tmp/HANDOFF.md`, or close with final-answer notes only.

## Placeholders

- `<CURRENT_PROMPT_ID>`: active prompt id.
- `<BLOCKER_OR_WARNING>`: concrete residual issue.
- `<AFFECTED_PATHS>`: files or indexes involved.
- `<NEXT_PROMPT_PATH>`: immediate next prompt path.

## Required Context To Load

- Completion audit result for `<CURRENT_PROMPT_ID>`
- Preflight result for `<NEXT_PROMPT_PATH>`
- `<AFFECTED_PATHS>`
- `runbooks/bridge-fix-session.md`
- `templates/handoffs/handoff.md` if a handoff may be needed

## Expected Output

- Decision: `bridge fix`, `handoff`, or `no handoff needed`.
- Reason the issue is or is not material.
- Changed files for any bridge fix.
- Handoff path and next safe action if a handoff is created.

## Stop Conditions

- The fix would require a new design decision.
- The fix would become implementation of the next prompt.
- Final-answer notes are enough to preserve the context.

