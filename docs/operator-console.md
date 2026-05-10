# Operator Console

The operator console is a small Makefile surface for common
`agent-harness-lab` checks. It wraps `scripts/ahl.py` commands so an operator
can discover routine actions quickly without remembering every subcommand.

Use direct `python3 scripts/ahl.py ...` calls when you need JSON output, command
arguments that are not exposed as variables, live `outer run --execute`, commit
execution, or a scaffold command that is not exposed as a stable Makefile
target. The Makefile is a convenience layer, not the source of command
behavior.

## Common Recipes

```sh
make help
make doctor
make resume
make checkpoint
make promptset
make lint-prompts
make check-docs
make test
make domain-pack
make trace PROMPT=PROMPT_26
make dry-run
make lane-check
make registry
make driver
make project-status PROJECT=/path/to/project
make lifecycle-snippets PROJECT=/path/to/project PORTABLE_PROMPT=PROMPT_45
make lifecycle-context-check PROJECT=/path/to/project PORTABLE_PROMPT=PROMPT_45
make lifecycle-run-range PROJECT=/path/to/project RANGE_START=18 RANGE_END=27
make portable-fixtures
make portable-rehearsal
make outer-plan OUTER_FROM=PROMPT_33 OUTER_COUNT=3 DRIVER=manual
make outer-dry-run PLAN=runs/outer-loop/<plan-id>/plan.json
make outer-gate PROMPT=PROMPT_36
make outer-run PLAN=runs/outer-loop/<plan-id>/plan.json
make outer-resume RUN=runs/outer-loop/<run-id>/run-ledger.json
make memory-check
make experiment-check
```

`make help` calls `python3 scripts/ahl.py help`, which also supports
`--json` for machine-readable command discovery.

## Target Safety

Read-only for the AHL checkout:

- `help`
- `doctor`
- `resume`
- `promptset`
- `lint-prompts`
- `check-docs`
- `test`
- `domain-pack`
- `trace`
- `dry-run`
- `lane-check`
- `registry`
- `driver`
- `project-status`
- `lifecycle-snippets`
- `lifecycle-context-check`
- `lifecycle-run-range`
- `portable-fixtures`
- `portable-rehearsal`
- `outer-dry-run`
- `outer-gate`
- `outer-resume`
- `memory-check`
- `experiment-check`

Artifact-writing targets:

- `checkpoint` creates missing `context/TASK.md`, `context/SESSION.md`, and
  `context/MEMORY.md`. It does not overwrite existing context files unless the
  underlying script is called directly with `--force`.
- `outer-plan` writes an inspectable `runs/outer-loop/<plan-id>/plan.json`.
- `outer-run` through the Makefile path passes `--dry-run`; it can write
  payload and ledger artifacts, but it does not invoke an assistant.

Targets that need existing artifact paths:

- `outer-dry-run` and `outer-run` require `PLAN=...`.
- `outer-resume` requires `RUN=...`.

The console does not include destructive targets, staging, commits, live
provider calls, a daemon, a TUI, or a REPL. Live assistant invocation remains a
direct script action requiring explicit `python3 scripts/ahl.py outer run
--execute`.

## Runtime Boundary

This console differs from a runtime because it does not choose work, run
prompts by default, maintain hidden state, or decide completion. It exposes
local checks, read-only portable helpers, dry-run outer-loop helpers, and small
inspectable artifacts. The active prompt, durable repo files, validation
evidence, and operator judgment remain authoritative.
