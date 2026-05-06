# Batch Planning

Batch planning turns an operator request into a reviewable artifact before any
assistant CLI can be invoked. The current implementation creates JSON plans
with `python3 scripts/ahl.py outer plan`; it does not execute prompts, stage
files, commit, or call models.

## Explicit Ranges

Use `--from` with `--count` when the operator knows the first prompt for the
batch:

```sh
python3 scripts/ahl.py outer plan --from PROMPT_33 --count 3 --driver codex --model gpt-5.5 --reasoning medium --json
```

This is the clearest mode for phase-two work because it records the exact
starting prompt and fails if any prompt file in the requested sequence is
missing.

## Next N

Use `--next N` for a small fixture promptset or a future workspace that has a
separate way to define what "next" means:

```sh
python3 scripts/ahl.py outer plan --next 10 --driver codex --json
```

In the current helper, `--next` resolves the first `N` strict prompt files found
in `.prompts/` and verifies that selection is sequential. It does not infer
completed work from git history, run ledgers, or commits. For real phase-two
batches, prefer explicit `--from` until a later prompt adds durable progress
tracking.

## Promptset Lint

Promptset lint remains a planning prerequisite. A plan records required AHL
checks such as:

```sh
python3 scripts/ahl.py promptset lint
python3 scripts/ahl.py doctor
```

The planner checks prompt files in the requested range, but it does not replace
full promptset linting. A failing lint result should stop review before live
execution is considered.

## Driver And Settings

The driver id must exist in `registry/assistant-drivers.json`. Model and
reasoning values are recorded as operator-supplied strings so reviewers can see
the intended assistant configuration. The planner does not validate that a
model exists, that the local CLI supports it, or that the operator is
authenticated.

## Artifact Boundary

Plans are written under `runs/outer-loop/<plan-id>/plan.json` and refuse to
overwrite an existing plan. A plan is an artifact, not an execution guarantee:
it records intent, prompt order, validation commands, stop conditions, commit
policy, transcript policy, and the run artifact directory for review.

The default commit policy is `none`. `plan-only` may be used to record future
commit packaging intent. `explicit` only records that commits would require a
separate operator approval boundary; it does not authorize staging or commits.
