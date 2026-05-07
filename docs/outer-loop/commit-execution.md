# Commit Execution

Commit execution is an explicit approval boundary. The default workflow is to
create and review a commit plan before running any executor.

## Command

```sh
python3 scripts/ahl.py commit execute --plan runs/outer-loop/<run-id>/commit-plan.json --operator-approved
```

Use `--dry-run` to validate the plan and render message files without staging
or committing.

## Safety Rules

- `--operator-approved` is required for execution.
- Only files listed in the commit plan are staged.
- `git add .` and `git add -A` are not used.
- Missing files block execution.
- Pre-existing staged files outside the plan block execution.
- Failed or blocked validation status blocks execution unless `--allow-failed`
  is explicitly supplied.
- Commit messages are written to files under `tmp/commit-messages/` and passed
  to `git commit -F`.

## Result Recording

Successful execution reports the resulting commit hash. The current executor
reports hashes in command output; operators may copy them into run ledgers or
trace records when those artifacts are being maintained.

The executor does not push, tag, publish, amend, delete files, or invoke
assistant CLIs.
