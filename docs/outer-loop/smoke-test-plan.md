# Outer Loop Smoke Test Plan

This plan separates offline-safe checks from opt-in checks that can touch real
assistant CLIs or consume quota.

## Offline And CI-Safe Tests

| Test | Command | Expected Result |
| --- | --- | --- |
| Driver registry check | `python3 scripts/ahl.py driver check --json` | Registry records and fixtures validate for `codex`, `gemini`, `pi`, and `manual`. |
| Manual driver probe | `python3 scripts/ahl.py driver probe manual --help-only --json` | Succeeds without an executable. |
| Plan creation | `python3 scripts/ahl.py outer plan --from PROMPT_41 --count 1 --driver manual --json` | Writes a plan artifact under `runs/outer-loop/`. |
| Dry-run execution | `python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<run-id>/plan.json --json` | Plan validates without assistant invocation. |
| Gate report | `python3 scripts/ahl.py outer gate PROMPT_41 --plan runs/outer-loop/<run-id>/plan.json --json` | Produces a structural gate report; `needs-human-review` is acceptable when no completion audit artifact is supplied. |
| Manual-driver run | `python3 scripts/ahl.py outer run --plan runs/outer-loop/<run-id>/plan.json --execute --max-prompts 1 --json` | Writes payload and ledger; step status is `manual-action-required`; no model is invoked. |
| Fake-driver failure | Use a fixture or temporary plan with an unknown driver id. | Dry-run or run refuses the invalid driver record. |
| Commit plan generation | `python3 scripts/ahl.py commit plan PROMPT_41 --json` | Writes a plan-only commit artifact and separates unrelated files. |
| Resume dry-run | `python3 scripts/ahl.py outer resume --run fixtures/outer-loop/runs/resumable-ledger.json --dry-run --json` | Reports the next prompt when clean, or refuses dirty worktrees. |
| Safety check | `python3 scripts/ahl.py doctor` | Passes foundational safety hygiene checks. |
| Docs and promptset checks | `python3 scripts/ahl.py docs check` and `python3 scripts/ahl.py promptset lint` | Local docs navigation and prompt structure pass. |

## Help-Only Local CLI Probes

These are safe in the sense that they do not send prompts, but they depend on
local PATH and installed CLIs:

```sh
python3 scripts/ahl.py driver probe codex --help-only --json
python3 scripts/ahl.py driver probe gemini --help-only --json
python3 scripts/ahl.py driver probe pi --help-only --json
```

Record missing executables honestly. A passing help probe does not prove
authentication, quota, or model availability.

## Opt-In Real Assistant CLI Tests

Run these only when the operator explicitly accepts quota, auth, and tool-side
effects:

```sh
python3 scripts/ahl.py outer plan --from PROMPT_41 --count 1 --driver codex --json
python3 scripts/ahl.py outer dry-run --plan runs/outer-loop/<run-id>/plan.json --json
python3 scripts/ahl.py outer run --plan runs/outer-loop/<run-id>/plan.json --execute --max-prompts 1 --json
```

Repeat with `gemini` only after a help-only probe succeeds and the operator
confirms the local CLI is authenticated. Do not use `pi` for live runs until
the print or JSON contract is verified and the registry no longer requires
manual confirmation.

## Failure Evidence To Preserve

- Command, return code, and short stderr/stdout preview.
- Generated `plan.json`, `run-ledger.json`, payload, and step summary paths.
- Gate status and problems.
- Whether the worktree was clean.
- Whether the check was skipped, unavailable, refused, failed, or passed.
