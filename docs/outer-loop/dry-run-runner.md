# Dry-Run Runner

The outer-loop dry-run runner validates an existing batch plan without calling
assistant CLIs, editing files through assistants, staging, or committing.

Run it with:

```sh
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<plan-id>/plan.json --json
```

## What It Validates

The dry-run checks that:

- the plan artifact exists and parses as JSON;
- every prompt path referenced by the plan still exists;
- the driver id still exists in `registry/assistant-drivers.json`;
- each step has validation commands;
- required AHL checks and stop conditions are present;
- the report emits stable `ok`, `plan_id`, `steps`, and `problems` fields.

Each step is simulated as `pass` or `fail` based only on plan and file
structure.

## What It Cannot Prove

Dry-run cannot prove assistant authentication, provider quota, CLI invocation
behavior, model availability, prompt quality, validation success after real
edits, completion audit quality, or next-prompt readiness after a live run. It
also does not prove that generated run records are complete.

## Difference From Live Execution

Dry-run reads a plan and local repo files. Live execution, which belongs to a
later prompt, would need explicit `--execute`-style consent and would start a
fresh assistant session per prompt. Dry-run never invokes an assistant driver,
never sends prompt text to a model, and never interprets assistant output.

## Reviewing Reports

Review the dry-run report before any future `--execute` path is used. Treat any
non-empty `problems` list as a stop condition. A passing dry-run only means the
plan is structurally ready for the next safety gate; it does not authorize live
assistant invocation or commit execution.
