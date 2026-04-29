# Commit Package

Purpose: package validated work into commits only after the operator explicitly
asks.

## Prompt

Package `<COMMIT_SCOPE>` for `<PROMPT_ID>` into reviewable git commit(s) using
the repo commit hygiene rules.

## Placeholders

- `<PROMPT_ID>`: prompt id for commit subject prefix.
- `<COMMIT_SCOPE>`: task-related changed files to consider.
- `<VALIDATION_EVIDENCE>`: checks to cite.
- `<UNRELATED_CHANGES>`: files that must not be staged.

## Required Context To Load

- Operator commit request.
- `AGENT.md` commit hygiene section.
- `git status --short`
- Relevant `git diff` for `<COMMIT_SCOPE>`.
- `<VALIDATION_EVIDENCE>`.

## Expected Output

- One or more commits with subjects prefixed by `[<PROMPT_ID>]`.
- Staged files limited to `<COMMIT_SCOPE>`.
- Commit hash, summary, and validation cited.
- `<UNRELATED_CHANGES>` preserved unstaged and unmodified.

## Stop Conditions

- The operator has not asked for a commit.
- Task-related and unrelated changes cannot be separated safely.
- Validation is missing for changes that need it.
- The commit would include temporary files accidentally.

