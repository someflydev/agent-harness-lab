# Resume And Recovery

Resume support is a planning layer over run ledgers. It helps an operator see
which prompt would run next after an interruption, while preserving the fresh
session and approval boundaries of the repo.

## Commands

```sh
python3 scripts/ahl.py outer status --run <run-id> --json
python3 scripts/ahl.py outer resume --run <run-id> --dry-run --json
python3 scripts/ahl.py outer recovery-handoff --run <run-id>
```

`--run` accepts a run id under `runs/outer-loop/<run-id>/run-ledger.json` or a
repo-relative ledger path.

## Resume Behavior

`outer status` reads the ledger and reports completed, failed, skipped, and
pending prompt steps.

`outer resume --dry-run` identifies the next prompt, refuses malformed ledgers,
refuses dirty or unsafe worktrees, and avoids completed prompt steps. Use
`--rerun` only when the operator explicitly wants to re-enter a recorded step.

`outer recovery-handoff` creates
`runs/outer-loop/<run-id>/recovery-handoff.md` from the template and refuses to
overwrite it unless `--force` is supplied.

## When Not To Resume

Do not resume when:

- The ledger is missing, malformed, or inconsistent with the plan.
- The worktree has unreviewed changes.
- A prompt step failed validation or completion audit.
- Next-prompt readiness is blocked.
- The driver is unauthenticated, missing, over quota, or otherwise unavailable.
- The stop reason is unknown.

Repair those conditions first, then run `outer resume --dry-run` again.

## Boundary

Resume does not create a daemon, scheduler, hidden queue, or transcript store.
Live assistant invocation remains limited to the explicit `outer run --execute`
path.
