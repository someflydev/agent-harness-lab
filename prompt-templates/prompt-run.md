# Fresh-Session Prompt Run

Purpose: run exactly one active implementation prompt from startup through
validated closeout.

## Prompt

Run `<PROMPT_PATH>` for `<PROMPT_ID>` in a fresh assistant session.

## Placeholders

- `<PROMPT_ID>`: active prompt id, such as `PROMPT_16`.
- `<PROMPT_PATH>`: active prompt path, such as `.prompts/PROMPT_16.txt`.
- `<NEXT_PROMPT_PATH>`: immediate next prompt path for closeout preflight.
- `<OPERATOR_NOTES>`: any explicit operator constraints for this run.

## Required Context To Load

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- `<PROMPT_PATH>`
- Docs explicitly named by `<PROMPT_PATH>`
- Existing hot-spot files before editing them
- `git status --short` before editing and near closeout

## Expected Output

- Active-prompt deliverables completed in required paths.
- Validation evidence for checks that ran or could not run.
- Completion audit result.
- Readiness label for `<NEXT_PROMPT_PATH>`.
- Handoff decision, with `tmp/HANDOFF.md` only if materially justified.

## Stop Conditions

- `<PROMPT_ID>` deliverables are complete, audited, and preflighted.
- A required prerequisite is missing.
- Validation fails in a way that cannot be repaired in scope.
- The next action belongs to another prompt or requires operator approval.

