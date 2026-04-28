# Runbooks

Runbooks are operator-facing procedures for recurring `agent-harness-lab`
work. They turn the routine catalog into concrete steps a human operator and a
fresh assistant session can follow without a runtime engine.

Use these runbooks with `AGENT.md`, the active prompt, the relevant runtime
docs, and the contract templates listed in `docs/contracts/README.md`.

## Runbook Index

- `fresh-session-prompt-run.md` - normal one-prompt fresh-session workflow.
- `completion-audit.md` - compare prompt requirements against delivered
  artifacts and evidence.
- `next-prompt-preflight.md` - inspect the immediate next prompt for readiness
  without implementing it.
- `bridge-fix-session.md` - apply a cheap closeout bridge fix or decide that a
  temporary handoff is needed.
- `repair-session.md` - start and constrain a bounded repair session.
- `promotion-review.md` - decide whether transient knowledge should become a
  durable artifact.
- `run-closeout.md` - leave the repo ready for review or the next session.
- `prompt-authoring.md` - create or revise prompt files in dedicated authoring
  sessions.
- `commit-packaging.md` - package validated work into commits only when asked.

## How To Use

1. Pick the runbook that matches the current session type.
2. Load only the required context named by that runbook and the active prompt.
3. Use the referenced templates when a durable or temporary record is needed.
4. Stop when the runbook's stop conditions are met.

These runbooks remain human-assisted. They name evidence to collect and
decisions to make, but they do not imply helper scripts or autonomous runtime
behavior.
