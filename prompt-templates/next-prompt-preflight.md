# Next-Prompt Preflight

Purpose: check whether the immediate next prompt can start cleanly without
implementing it.

## Prompt

Preflight `<NEXT_PROMPT_PATH>` after completing `<CURRENT_PROMPT_ID>` and label
readiness as `ready`, `risky`, or `blocked`.

## Placeholders

- `<CURRENT_PROMPT_ID>`: current completed prompt id.
- `<NEXT_PROMPT_PATH>`: immediate next prompt file.
- `<CURRENT_CHANGES>`: paths changed by the current prompt.
- `<KNOWN_WARNINGS>`: unresolved validation or audit warnings.

## Required Context To Load

- `<NEXT_PROMPT_PATH>` only from the future promptset.
- Current completion audit result.
- `git status --short`
- Docs and indexes named by `<NEXT_PROMPT_PATH>`
- `<KNOWN_WARNINGS>`, if any

## Expected Output

- Readiness label: `ready`, `risky`, or `blocked`.
- Concrete prerequisite checks performed.
- Any cheap bridge fix recommended or applied.
- Confirmation that no next-prompt deliverables were implemented.

## Stop Conditions

- The check would require reading beyond the immediate next prompt.
- A proposed fix would implement `<NEXT_PROMPT_PATH>`.
- Readiness depends on an operator sequencing decision.

