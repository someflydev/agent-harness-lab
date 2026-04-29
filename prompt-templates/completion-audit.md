# Completion Audit

Purpose: decide whether an active prompt is done by comparing requirements,
actual files, and validation evidence.

## Prompt

Audit `<PROMPT_ID>` against the current repo state and report whether the result
is `done`, `incomplete`, or `blocked`.

## Placeholders

- `<PROMPT_ID>`: active prompt id.
- `<PROMPT_PATH>`: active prompt path.
- `<CHANGED_SCOPE>`: changed files, directories, or artifact families.
- `<VALIDATION_EVIDENCE>`: commands and manual checks already performed.

## Required Context To Load

- `<PROMPT_PATH>`
- `git status --short`
- Relevant diffs or file inventories for `<CHANGED_SCOPE>`
- Validation section from `<PROMPT_PATH>`
- Relevant indexes such as `docs/README.md` or `registry/*.json`

## Expected Output

- Requirement-by-requirement audit summary.
- Missing, weak, or overclaimed items, if any.
- Validation evidence and skipped checks.
- Final classification: `done`, `incomplete`, or `blocked`.

## Stop Conditions

- A required deliverable is absent.
- A prompt constraint has been violated.
- Evidence cannot be gathered without unavailable tools or operator approval.
- Remaining work belongs to a future prompt.

