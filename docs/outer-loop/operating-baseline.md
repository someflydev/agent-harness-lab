# Outer Loop Operating Baseline

This baseline describes the safe local operating path for the phase-two
outer-loop helper. Start with dry-run evidence, keep every approval boundary
visible, and treat generated artifacts as review aids.

## Prepare A Clean Repo

1. Review `git status --short --untracked-files=all`.
2. Commit, stash, move, or intentionally ignore unrelated work before resuming
   or executing live assistant steps.
3. Run cheap local checks:

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py promptset lint
python3 scripts/ahl.py docs check
python3 -m unittest tests/test_ahl.py
```

## Probe Drivers

Use registry checks and help-only probes before any live run:

```sh
python3 scripts/ahl.py driver check --json
python3 scripts/ahl.py driver probe codex --help-only --json
python3 scripts/ahl.py driver probe gemini --help-only --json
python3 scripts/ahl.py driver probe manual --help-only --json
```

Probe `pi` only as an availability check unless the operator has verified the
local Pi command contract:

```sh
python3 scripts/ahl.py driver probe pi --help-only --json
```

Help output does not prove authentication, quota, model availability, or
headless response semantics.

## Create A Plan For The Next N Prompts

Create an inspectable sequential plan. Review `plan.json` before using it.

```sh
python3 scripts/ahl.py outer plan --next 3 --driver manual --json
```

A cautious Codex example:

```bash
python3 scripts/ahl.py outer plan --next 10 --driver codex --model gpt-5.5 --reasoning medium --json
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<run-id>/plan.json --json
python3 scripts/ahl.py outer run --plan runs/outer-loop/<run-id>/plan.json --execute --max-prompts 1 --json
```

Do not assume every local machine has that model, subscription, CLI, or PATH
setup. Probe first and keep `--max-prompts 1` for initial live use.

## Dry-Run The Plan

```sh
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<run-id>/plan.json --json
python3 scripts/ahl.py outer run --plan runs/outer-loop/<run-id>/plan.json --dry-run --max-prompts 1 --json
```

The dry-run validates plan structure, prompt files, driver records, stop
conditions, and payload generation without invoking an assistant.

## Run One Live Prompt Step

Live execution requires explicit `--execute`. Start with one prompt:

```sh
python3 scripts/ahl.py outer run --plan runs/outer-loop/<run-id>/plan.json --execute --max-prompts 1 --json
```

For `manual`, this records the operator action and writes the payload; it does
not invoke a model. For supported local CLI drivers, this can consume quota and
depends on local authentication outside AHL.

## Inspect The Gate Result

```sh
python3 scripts/ahl.py outer gate PROMPT_41 --plan runs/outer-loop/<run-id>/plan.json --json
```

Gate statuses are conservative. `needs-human-review` is acceptable for a
structural gate that lacks a semantic completion audit. `blocked` or `failed`
requires repair before continuing.

## Stop And Recover

Inspect the ledger:

```sh
python3 scripts/ahl.py outer status --run runs/outer-loop/<run-id>/run-ledger.json --json
python3 scripts/ahl.py outer resume --run runs/outer-loop/<run-id>/run-ledger.json --dry-run --json
```

Resume refuses malformed ledgers and dirty or unsafe worktrees. If recovery
context is needed:

```sh
python3 scripts/ahl.py outer recovery-handoff --run runs/outer-loop/<run-id>/run-ledger.json
```

Review the handoff before starting another fresh session.

## Generate A Commit Plan

Commit planning is metadata only:

```sh
python3 scripts/ahl.py commit plan PROMPT_41 --json
python3 scripts/ahl.py commit plan --run runs/outer-loop/<run-id>/run-ledger.json --json
```

The planner separates unrelated changes and writes explicit file lists for
review.

## Commit Execution Boundary

Commit execution is allowed only when the operator has reviewed the plan and
explicitly approves execution:

```sh
python3 scripts/ahl.py commit execute --plan runs/outer-loop/<run-id>/commit-plan.json --operator-approved
```

It is still conservative: only files listed in the plan may be staged, and
failed or blocked validation cannot be committed unless the operator explicitly
allows that state.

## What Remains Manual

- Choosing which prompt batch is appropriate.
- Confirming provider authentication, quota, and local CLI behavior.
- Reading generated prompt payloads before live use.
- Auditing semantic prompt completion.
- Deciding whether a bridge handoff is justified.
- Reviewing generated commit plans and running commits.
- Promoting durable lessons into docs, memory records, or backlog items.
