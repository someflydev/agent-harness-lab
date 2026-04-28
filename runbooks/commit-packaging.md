# Commit Packaging

## Purpose

Package validated work into coherent git commits when the operator explicitly
asks.

## When To Use It

Use after implementation and validation are complete and the operator requests
a commit or commit plan. Do not commit during normal prompt execution without
that request.

## Required Context To Load

- Operator commit request.
- Active prompt id, such as `PROMPT_08`.
- `git status --short`.
- `git diff` or relevant file-level diff.
- Validation evidence and completion audit result.
- Commit guidance in `AGENT.md`.

## Roles Involved

- Operator: authorizes commit creation.
- Commit Packager: groups changes and writes messages.
- Orchestrator: protects unrelated user changes from being swept in.
- Validator: confirms checks to cite in commit body.

## Step-By-Step Procedure

1. Confirm the operator asked for a commit.
2. Inspect `git status --short` and identify unrelated modified or untracked
   files.
3. Inspect the diff for task-related changes.
4. Group changes by coherent review unit. Prefer one bounded prompt commit when
   the prompt's changes are cohesive.
5. Use the prompt id prefix in the subject, for example
   `[PROMPT_08] Add operator runbooks`.
6. Include validation evidence in the commit body when it helps review.
7. Stage only task-related files. Do not sweep unrelated user changes.
8. Commit using a multi-line message when body context is useful.
9. Report commit hash, summary, and validation cited.

## Expected Artifacts

- One or more reviewable git commits.
- Commit messages with prompt id prefixes.
- Unrelated user changes left unstaged and unmodified.

## Validation Or Evidence

- Status and diff were inspected before staging.
- Staged files match the intended commit group.
- Commit body cites meaningful validation when appropriate.
- Final status is reported after commit.

## Stop Conditions

- The operator has not asked for a commit.
- Task-related and unrelated changes cannot be separated safely.
- Validation is missing for changes that need it.
- The commit would include generated or temporary files accidentally.

## Common Failure Modes

- Committing without explicit approval.
- Staging `.` when unrelated files are present.
- Omitting the prompt id prefix.
- Hiding failed or skipped validation from the commit body.
