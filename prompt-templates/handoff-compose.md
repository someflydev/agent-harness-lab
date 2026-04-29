# Handoff Compose

Purpose: compose `tmp/HANDOFF.md` only when a real blocker or non-trivial
warning would otherwise be lost.

## Prompt

Write `tmp/HANDOFF.md` for `<HANDOFF_REASON>` using the repo handoff template
and keep it temporary, concise, and action-oriented.

## Placeholders

- `<HANDOFF_REASON>`: blocker or warning that justifies the file.
- `<CURRENT_PROMPT_ID>`: active prompt id.
- `<AFFECTED_PATHS>`: relevant files and directories.
- `<VALIDATION_DONE>`: checks already run.
- `<NEXT_SAFE_ACTION>`: first bounded action for the next session.

## Required Context To Load

- `templates/handoffs/handoff.md`
- `docs/memory/handoff-lifecycle.md`
- Completion audit and preflight result
- `<AFFECTED_PATHS>`

## Expected Output

- `tmp/HANDOFF.md` with current status, blocker, affected paths, validation
  already performed, next safe action, and out-of-scope boundaries.
- Closeout note explaining why final-answer notes were insufficient.

## Stop Conditions

- No real blocker or non-trivial warning remains.
- The next session does not need more context than the final answer.
- The handoff would describe broad future planning instead of a bounded action.

