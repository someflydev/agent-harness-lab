# Outer Loop Gates

Outer-loop gates collect the evidence a sequential runner needs after each
prompt step. The gate is a stop-and-review layer, not a semantic proof engine.
It combines deterministic local checks with explicit placeholders for the
human or assistant judgment that still has to happen at closeout.

## Statuses

- `pass` - deterministic evidence is present, no blockers were found, and an
  explicit audit artifact exists.
- `pass-with-warnings` - the runner may continue, but named warnings should be
  reviewed first.
- `blocked` - a required artifact such as the active prompt, supplied plan, or
  required next prompt is missing.
- `failed-validation` - an allowlisted AHL structural check failed.
- `needs-human-review` - structural checks ran, but no explicit completion
  audit artifact is available, so semantic completion remains unclaimed.
- `driver-failed` - reserved for a later live runner when an assistant driver
  invocation fails before gate evaluation can complete.
- `unsafe-git-state` - git status could not be inspected or contains unmerged
  entries that make continuation unsafe.

## Expected Evidence

Each gate report should include:

- prompt id
- changed files from `git status --short`
- validation commands run or recorded
- validation outcomes, including skipped commands and reasons
- AHL structural checks run, skipped, or unavailable
- completion audit status
- next-prompt readiness status
- handoff status
- commit-plan status
- stop-or-continue decision

The schema is `schemas/outer-loop-gate-report.schema.json`, the markdown
template is `templates/outer-loop/gate-report.md`, and artificial examples live
under `fixtures/outer-loop/gates/`.

## CLI

Use:

```sh
python3 scripts/ahl.py outer gate PROMPT_36 --json
python3 scripts/ahl.py outer gate PROMPT_36 --plan runs/outer-loop/<run-id>/plan.json --json
```

The command inspects the current working tree, checks that the active prompt
exists, checks that the immediate next prompt exists unless the supplied plan
marks the prompt as the final planned step, records validation commands, runs
allowlisted AHL checks when available, and emits a structured report.

Prompt validation commands are recorded in record-only mode. The gate does not
execute arbitrary validation commands because plans can contain shell strings.
Later work may add a narrow execution allowlist, but that should be explicit
and reviewed.

## Limits

The gate cannot prove that the assistant satisfied a prompt. A clean structural
report only means the local artifacts needed for review are present. Completion
still depends on the audit protocol, changed-file inspection, validation
evidence, and operator judgment. Raw transcripts are not accepted as durable
gate evidence.
