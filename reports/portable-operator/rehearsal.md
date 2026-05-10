# Portable Operator Rehearsal Report

- Date: 2026-05-10
- Rehearsal path: `python3 scripts/ahl.py portable rehearsal --json`
- Fixture projects:
  - `fixtures/portable-operator/projects/basic`
  - `fixtures/portable-operator/projects/gapped`
- Assistant invocation: disabled
- Network/provider credentials: not required

## Commands Covered

| Step | Command | Result |
| --- | --- | --- |
| AHL/project discovery | `python3 scripts/ahl.py project locate --project fixtures/portable-operator/projects/basic --json` | pass |
| Basic status | `python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/basic --json` | pass |
| Gapped status | `python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/gapped --json` | pass |
| Snippets | `python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/basic --json` | pass |
| Context update check | `python3 scripts/ahl.py lifecycle context-check PROMPT_01 --project fixtures/portable-operator/projects/basic --json` | pass |
| Run range | `python3 scripts/ahl.py lifecycle run-range 1 2 --project fixtures/portable-operator/projects/basic --dry-run --json` | pass |
| Gapped run range | `python3 scripts/ahl.py lifecycle run-range 1 3 --project fixtures/portable-operator/projects/gapped --dry-run --json` | pass, expected missing `PROMPT_02` stop |
| Commit check | `python3 scripts/ahl.py commit check --project <tempdir> --last 2 --json` | pass when git is available; skipped cleanly if git is unavailable |

## Known Limitations

- The rehearsal proves helper composition against fixtures; it does not run
  prompts or call assistant CLIs.
- The context-update check is advisory and read-only. Human review still
  decides whether durable context edits are justified.
- Commit-check evidence uses isolated temporary git data, not AHL repository
  history or a real target project.

## Residual Manual Steps

- The human operator still starts each assistant session.
- The human operator reviews implementation, validation, context updates, and
  commits.
- The human operator decides whether capstone evidence is sufficient.

## Capstone Readiness

Ready for capstone review when `python3 scripts/ahl.py portable rehearsal
--json` exits successfully. The command emits machine-checkable pass/fail/skip
records and should be used as live evidence during capstone validation.
