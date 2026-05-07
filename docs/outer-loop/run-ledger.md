# Run Ledger

The outer-loop run ledger is the durable state file for one sequential run. It
stores derived metadata and concise summaries only. It must not store raw
assistant transcripts, provider logs, credentials, or copied conversation
dumps.

The canonical artifact is `runs/outer-loop/<run-id>/run-ledger.json`, using
`schemas/outer-loop-run-ledger.schema.json`. Artificial examples live under
`fixtures/outer-loop/runs/`.

## Required Semantics

A ledger records:

- Run id, plan id, driver id, model, reasoning or thinking value, and
  permission posture.
- Started and ended timestamps.
- Current status.
- Per-prompt step records with prompt id, prompt file, status, payload path,
  validation commands, driver result, gate result, summary path, and problems.
- Command metadata, including whether the run was dry-run or explicit
  execution and which driver arguments were supplied.
- Validation results and gate results as bounded structured summaries.
- Commit plan metadata and commit hashes when present.
- Resume pointer with completed, failed, skipped, pending, and next prompt
  values.
- Stop reason and recovery recommendation.

## Status Meaning

- `completed` means all planned steps that were attempted by this run finished.
- `running` means the ledger was written before a final closeout status.
- `interrupted`, `user-interrupted`, `driver-timeout`, and
  `driver-rate-limit` may be resumable after operator review.
- `blocked`, `failed-validation`, `unsafe-git-state`,
  `unexpected-plan-mutation`, `unexpected-changed-files`, and
  `commit-plan-refused` require repair before resume.
- `unknown-failure` requires manual inspection before any resume attempt.

## Resume Pointer

The resume pointer is advisory. `outer resume` recomputes completed, failed,
skipped, and pending prompts from step records and refuses to continue when the
worktree is not clean. Completed prompt steps are not rerun unless the operator
uses `--rerun`.

## Boundary

The ledger is not a scheduler queue and not a proof of semantic completion.
Completion still depends on prompt closeout, gate evidence, validation output,
and operator review.
