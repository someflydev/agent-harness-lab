# Live Sequential Runner

`python3 scripts/ahl.py outer run` is the first live sequential runner MVP. It
starts from an existing `outer plan` artifact, processes prompts in the plan
order, builds one bounded prompt payload per step, runs the outer gate after
each step, and writes a run ledger under `runs/outer-loop/`.

The command is dry-run by default:

```sh
python3 scripts/ahl.py outer run --plan runs/outer-loop/<run-id>/plan.json --dry-run --json
```

Live assistant CLI invocation requires explicit consent:

```sh
python3 scripts/ahl.py outer run --plan runs/outer-loop/<run-id>/plan.json --execute --max-prompts 1 --json
```

## Execution Model

- The plan file must already exist.
- Prompts must be strictly sequential.
- Parallel execution is rejected.
- Driver records must exist in `registry/assistant-drivers.json`.
- `manual` never invokes a model; it records the operator action and payload.
- `codex` and `gemini` use a small temporary internal mapping that sends the
  payload on stdin to the configured executable.
- `pi` can appear in plans and dry-run ledgers, but live invocation is disabled
  while its registry record is marked `manual-confirmation-required`.
- Model and reasoning values are passed only when the driver contract marks
  that selection as supported or verified. Otherwise they stay recorded in the
  plan and ledger but are not put on the command line.
- `--driver-arg` is the explicit escape hatch for operator-approved extra CLI
  arguments.

## Stop Conditions

The runner stops on missing or mutated plan files, invalid driver records,
non-sequential prompts, unsupported parallel mode, driver failure, timeout,
blocked or failed gate status, unsafe git state, and unexpected plan mutation.

The MVP does not stage, commit, push, tag, publish, retry indefinitely, run a
daemon, or capture raw transcripts.

## Timeout

`--timeout-seconds` bounds each live assistant CLI invocation. Timeout failures
are recorded as `driver-failed` in the ledger.
