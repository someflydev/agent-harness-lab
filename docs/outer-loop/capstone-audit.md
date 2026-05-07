# Outer Loop Capstone Audit

This audit records the phase-two outer-loop baseline as of Prompt 41. It is an
honest implementation audit, not a production-readiness claim.

## Summary

The outer loop is usable as a bounded local helper when the operator keeps the
worktree reviewable, starts with dry-runs, and enables live execution only with
explicit consent. It supports driver contracts, capability probes, batch plans,
plan dry-runs, gate reports, prompt payloads, run ledgers, a dry-run-default
sequential runner, commit planning, approval-gated commit execution, resume
planning, recovery handoffs, and a conservative Pi adapter record.

Semantic prompt completion remains manual. Provider authentication, quota, and
CLI behavior remain outside AHL. Pi live use is not verified on this machine.

## Check Evidence

- `python3 -m unittest tests/test_ahl.py`: passed, 95 tests.
- `python3 scripts/ahl.py doctor`: passed.
- `python3 scripts/ahl.py docs check`: passed before editing, 238 markdown
  files scanned, 1 local link checked, 0 missing; passed after editing, 243
  markdown files scanned, 1 local link checked, 0 missing.
- `python3 scripts/ahl.py promptset`: passed, 41 prompts, numbering ok.
- `python3 scripts/ahl.py driver check --json`: passed for `codex`, `gemini`,
  `pi`, and `manual` registry records and fixtures.
- `python3 scripts/ahl.py driver probe manual --help-only --json`: passed.
- `python3 scripts/ahl.py driver probe codex --help-only --json`: passed;
  `codex` was found on `PATH` and help returned 0.
- `python3 scripts/ahl.py driver probe gemini --help-only --json`: passed;
  `gemini` was found on `PATH` and help returned 0.
- `python3 scripts/ahl.py driver probe pi --help-only --json`: failed because
  `pi` was not found on `PATH`.
- `python3 scripts/ahl.py outer plan --from PROMPT_41 --count 1 --driver manual
  --json`: passed and wrote a Prompt 41 manual-driver plan.
- `python3 scripts/ahl.py outer dry-run --plan
  runs/outer-loop/outer-prompt_41-prompt_41-manual-20260507t172142z/plan.json
  --json`: passed.
- `python3 scripts/ahl.py outer gate PROMPT_41 --plan
  runs/outer-loop/outer-prompt_41-prompt_41-manual-20260507t172142z/plan.json
  --json`: passed with status `needs-human-review`.
- `python3 scripts/ahl.py outer run --plan
  runs/outer-loop/outer-prompt_41-prompt_41-manual-20260507t172142z/plan.json
  --dry-run --max-prompts 1 --json`: passed and wrote a dry-run ledger.
- `python3 scripts/ahl.py outer run --plan
  runs/outer-loop/outer-prompt_41-prompt_41-manual-20260507t172142z/plan.json
  --execute --max-prompts 1 --json`: passed for the `manual` driver; no
  assistant CLI was invoked and the step status was `manual-action-required`.
- `python3 scripts/ahl.py outer status --run
  fixtures/outer-loop/runs/resumable-ledger.json --json`: passed.
- `python3 scripts/ahl.py outer resume --run
  fixtures/outer-loop/runs/resumable-ledger.json --dry-run --json`: refused
  because the worktree had untracked files, which is the expected safety
  behavior.
- `python3 scripts/ahl.py commit plan PROMPT_41 --json`: passed in plan-only
  mode and separated unrelated untracked files from prompt-scoped changes.

## Area Audit

| Area | Status | Evidence Files | Checks Performed | Gaps | Blocks Baseline Use |
| --- | --- | --- | --- | --- | --- |
| Requirements and safety boundary | Implemented as docs and enforced guardrails | `docs/outer-loop/requirements.md`, `docs/outer-loop/safety-boundary.md`, `docs/outer-loop/non-goals.md` | Docs check, Prompt 41 audit review | Safety still depends on operator discipline and local permission posture | No |
| Driver contracts and capability probes | Implemented | `registry/assistant-drivers.json`, `fixtures/assistant-drivers/`, `docs/outer-loop/driver-contracts.md`, `docs/outer-loop/capability-probes.md` | `driver check`, help-only probes | Help probes do not prove auth, quota, or stable headless output | No |
| Batch planning | Implemented | `docs/outer-loop/batch-planning.md`, `schemas/outer-loop-plan.schema.json`, generated `plan.json` artifacts | Prompt 41 manual plan creation | `--next` depends on prompt registry/status conventions and operator review | No |
| Dry-run runner | Implemented | `docs/outer-loop/dry-run-runner.md`, generated dry-run output | Prompt 41 plan dry-run | Structural dry-runs do not prove prompt success | No |
| Validation, audit, and readiness gates | Implemented conservatively | `docs/outer-loop/gates.md`, `docs/outer-loop/completion-audit-integration.md`, `docs/outer-loop/readiness-gate.md`, `schemas/outer-loop-gate-report.schema.json` | Prompt 41 gate with plan | Prompt validation commands are record-only unless allowlisted; semantic audit remains manual | No |
| Live sequential runner | Implemented MVP | `docs/outer-loop/live-runner.md`, `docs/outer-loop/sequential-runner-model.md`, generated run ledger | Manual-driver dry-run and explicit execute run | Real Codex/Gemini live runs were not executed in this capstone | No |
| Prompt payloads | Implemented | `docs/outer-loop/prompt-payloads.md`, generated `payloads/PROMPT_41.md` | `outer run` generated payloads | Payload quality still depends on the prompt and startup docs | No |
| Run artifacts and ledger | Implemented | `docs/outer-loop/run-artifacts.md`, `docs/outer-loop/run-ledger.md`, generated `run-ledger.json` | `outer run`, `outer status` | Raw transcripts remain intentionally off by default | No |
| Commit planner | Implemented | `docs/outer-loop/commit-planning.md`, `schemas/commit-plan.schema.json`, generated `commit-plan` artifact | `commit plan PROMPT_41 --json` | Plans require operator review before staging | No |
| Explicit commit executor | Implemented with approval boundary | `docs/outer-loop/commit-execution.md`, `scripts/README.md` | Unit tests cover helper behavior; capstone did not execute commits | No commit was executed because the operator did not ask for one | No |
| Resume and recovery | Implemented | `docs/outer-loop/resume-and-recovery.md`, `docs/outer-loop/failure-classification.md`, `templates/handoffs/recovery-handoff.md`, fixture ledgers | `outer status`; `outer resume --dry-run` refused dirty worktree | Resume requires a clean reviewed worktree; dirty-state refusal is intentional | No |
| Pi adapter experiment | Implemented as guarded design and registry record | `docs/outer-loop/pi-adapter.md`, `docs/outer-loop/pi-vs-ahl.md`, `fixtures/assistant-drivers/pi.json` | `driver check`; Pi help probe attempted | `pi` is not on `PATH`; print/JSON/RPC behavior is unverified | No for baseline; yes for Pi live use |
| Docs navigation | Implemented with capstone pages added | `README.md`, `AGENT.md`, `docs/README.md`, `scripts/README.md` | `docs check` before and after edit | External links are not audited | No |
| Script tests | Passing | `tests/test_ahl.py` | Unit test suite passed, 95 tests | Tests mock or structurally exercise provider surfaces; they do not consume real provider quota | No |
| Known limitations | Documented | `docs/known-limitations.md`, `docs/outer-loop/known-limitations.md`, `docs/release-readiness.md` | Prompt 41 audit review | Limitations must be revisited after real provider runs | No |

## Baseline Decision

The phase-two outer-loop baseline is usable with limits. It is appropriate for
local planning, dry-run validation, manual-driver rehearsal, explicit one-step
live runs through supported local driver contracts, gate reporting, resume
planning, and commit plan generation. It is not an autonomous runner, semantic
completion oracle, provider authentication layer, transcript store, scheduler,
or production orchestration system.
