# Operator Console

The operator console is a small Makefile surface for common
`agent-harness-lab` checks. It wraps `scripts/ahl.py` commands so an operator
can discover routine actions quickly without remembering every subcommand.

Use direct `python3 scripts/ahl.py ...` calls when you need JSON output, command
arguments, a non-default prompt id, or a scaffold command that is not exposed as
a stable Makefile target. The Makefile is a convenience layer, not the source
of command behavior.

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
make trace PROMPT=PROMPT_26
make dry-run
make registry
make memory-check
make experiment-check
```

`make help` calls `python3 scripts/ahl.py help`, which also supports
`--json` for machine-readable command discovery.

## Target Safety

Read-only targets:

- `help`
- `doctor`
- `resume`
- `promptset`
- `lint-prompts`
- `check-docs`
- `test`
- `trace`
- `dry-run`
- `registry`
- `memory-check`
- `experiment-check`

Scaffold-capable target:

- `checkpoint` creates missing `context/TASK.md`, `context/SESSION.md`, and
  `context/MEMORY.md`. It does not overwrite existing context files unless the
  underlying script is called directly with `--force`.

The console does not include destructive targets, staging, commits, provider
calls, batch prompt execution, a daemon, a TUI, or a REPL.

## Runtime Boundary

This console differs from a runtime because it does not choose work, invoke an
assistant, run prompts, maintain hidden state, or decide completion. It exposes
local checks and scaffolds small inspectable files. The active prompt, durable
repo files, validation evidence, and operator judgment remain authoritative.

Batch prompt execution and provider or assistant invocation remain
post-baseline automation candidates. They need stronger evidence around
permissions, cost control, failure recovery, traceability, and human approval
before becoming initial console targets.
