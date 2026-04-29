# Prompt Authoring

Purpose: create or revise prompt files in a dedicated authoring session without
executing those prompts.

## Prompt

Author or revise `<PROMPT_SCOPE>` according to `<AUTHORING_GOAL>` while keeping
prompt execution out of scope.

## Placeholders

- `<PROMPT_SCOPE>`: prompt files or planning artifacts in scope.
- `<AUTHORING_GOAL>`: requested sequencing or content change.
- `<ADJACENT_PROMPTS>`: nearby prompts needed for dependency checks.
- `<VALIDATION_CHECKS>`: promptset or manual checks to run.

## Required Context To Load

- Operator authoring request
- `docs/runtime/prompt-authoring-vs-execution.md`
- Existing prompt files in `<PROMPT_SCOPE>`
- `<ADJACENT_PROMPTS>` only as needed
- `git status --short`

## Expected Output

- New or revised prompt text with startup, deliverables, constraints,
  validation, and endcap guidance.
- Sequencing risks or unresolved decisions.
- Confirmation that implementation work was not performed.

## Stop Conditions

- Authoring requires implementing the prompts to know what to write.
- Sequencing conflicts require operator direction.
- The work becomes broad promptset redesign without authorization.

