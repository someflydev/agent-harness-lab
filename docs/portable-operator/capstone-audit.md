# Portable Operator Capstone Audit

Date: 2026-05-10

## Baseline Decision

The portable operator baseline is usable as a local, human-governed helper
workflow for arbitrary target projects that have `.prompts/`. It is incomplete
by design: AHL does not run assistant sessions for target projects, does not
schedule prompt ranges, does not commit automatically, and does not treat
private notes or assistant transcripts as machine state.

Every live action that can change files, run assistant commands, consume
assistant quota, or create commits remains explicit and inspectable. Portable
helpers require no provider secrets, no network access, no expensive APIs, and
no background daemon. Claude Code remains a manual or terminal workflow, not
external subscription API automation. AHL does not query subscription usage
limits programmatically.

## Validation Evidence

- `python3 -m unittest tests/test_ahl.py` - pass, 146 tests.
- `python3 scripts/ahl.py doctor` - pass.
- `python3 scripts/ahl.py promptset lint` - pass, 53 prompts.
- `python3 scripts/ahl.py docs check` - pass.
- `python3 scripts/ahl.py registry check` - pass.
- `python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/basic --json` - pass.
- `python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/basic --json` - pass.
- `python3 scripts/ahl.py lifecycle context-check PROMPT_01 --project fixtures/portable-operator/projects/basic --json` - pass.
- `python3 scripts/ahl.py lifecycle run-range 1 2 --project fixtures/portable-operator/projects/basic --dry-run --json` - pass.
- `python3 scripts/ahl.py lifecycle run-range 1 3 --project fixtures/portable-operator/projects/gapped --dry-run --json` - pass as an expected failed plan with missing `PROMPT_02`.
- `python3 scripts/ahl.py commit check --project <temporary git repo> --last 2 --json` - pass through `portable rehearsal`; reports a deliberate prefix issue without rewriting history.
- `python3 scripts/ahl.py portable rehearsal --json` - pass.
- `make help` - pass.
- `make portable-rehearsal` - pass.

## Area Audit

| Area | Status | Evidence files | Checks performed | Gaps | Blocks baseline use |
| --- | --- | --- | --- | --- | --- |
| Portable invocation and root discovery | Implemented read-only | `docs/portable-operator/invocation.md`, `scripts/ahl.py`, `tests/test_ahl.py` | `project locate` coverage in unit tests and rehearsal | No checked-in wrapper such as `bin/ahl`; operators call `scripts/ahl.py` directly or make their own alias | No |
| Project status and promptset diagnostics | Implemented read-only | `docs/portable-operator/status.md`, `fixtures/portable-operator/projects/`, `tests/test_ahl.py` | Fixture status checks for valid, gapped, and Claude-bootstrap projects | Next-prompt inference is heuristic and based on prompt files plus recent prompt-prefixed commits | No |
| Lifecycle snippet generation | Implemented read-only | `docs/portable-operator/lifecycle-snippets.md`, `runbooks/one-prompt-autopilot.md`, `tests/test_ahl.py` | Snippet tests and fixture command checks | Snippets are copy/paste text; they do not prove assistant compliance | No |
| Context-update policy and helper support | Implemented advisory helper | `docs/portable-operator/context-update-policy.md`, `docs/portable-operator/human-notes-boundary.md`, `tests/test_ahl.py` | `lifecycle context-check` fixture and unit tests | Candidate detection is intentionally conservative and cannot decide semantic context value | No |
| Commit-check helper | Implemented read-only | `docs/portable-operator/commit-check.md`, `scripts/README.md`, `tests/test_ahl.py` | Unit tests and temporary git fixture in rehearsal | Guidance may suggest amend or rebase commands, but never runs them | No |
| One-prompt autopilot runbook | Documented | `runbooks/one-prompt-autopilot.md`, `docs/portable-operator/one-prompt-loop.md` | Docs check and capstone review | It remains operator choreography, not automatic prompt execution | No |
| Run-range dry-run orchestration | Implemented dry-run planning | `docs/portable-operator/run-range.md`, `fixtures/portable-operator/run-range/valid-plan.json`, `tests/test_ahl.py` | Valid range and gapped range checks | Dry-run/read-only by default; no scheduler, continuation, or assistant invocation | No |
| Assistant-surface boundaries | Documented | `docs/portable-operator/assistant-surfaces.md`, `docs/assistants/README.md`, `docs/known-limitations.md` | Docs check and capstone review | Provider availability, quota, login, and model selection remain outside AHL | No |
| Fixtures and examples | Implemented | `fixtures/portable-operator/README.md`, `examples/portable-operator/README.md` | Fixture commands and docs check | Fixtures are artificial and do not demonstrate real implementation quality in a target repo | No |
| Rehearsal evidence | Implemented | `docs/portable-operator/rehearsal.md`, `reports/portable-operator/rehearsal.md`, `scripts/ahl.py` | `python3 scripts/ahl.py portable rehearsal --json`, `make portable-rehearsal` | Rehearsal does not run assistants or real target-project validation | No |
| Docs navigation | Implemented | `README.md`, `AGENT.md`, `docs/README.md`, `scripts/README.md`, `CHANGELOG.md` | `docs check`, manual capstone review | Some future-facing docs remain as backlog and must not be read as implemented runtime | No |
| Tests and validation | Implemented for helper surface | `tests/test_ahl.py`, `docs/release-readiness.md` | Unit tests, doctor, promptset lint, docs check, registry check, fixture commands | Structural tests do not prove semantic prompt completion | No |
| Known limitations and safety boundaries | Documented | `docs/portable-operator/known-limitations.md`, `docs/known-limitations.md`, `docs/portable-operator/non-goals.md` | Capstone review | Live assistant execution and commit authority remain manual | No |

## Safety Boundary Findings

- No background daemon, queue worker, provider credential manager, browser
  bridge, or network dependency is part of the portable baseline.
- `human-notes.md` is informational and never machine-authoritative. Portable
  commands may report that it exists but do not edit it or derive state from
  it.
- Commit inspection is read-only. It may report history hygiene issues and
  suggest manual follow-up, but it never stages files, rewrites history,
  amends, rebases, pushes, tags, or publishes.
- Run-range orchestration is one prompt at a time and dry-run/read-only by
  default. It writes an artifact only when `--artifact` is explicit and does
  not invoke assistants or continue automatically.
- Claude Code, Codex, Gemini, and generic chat are assistant surfaces the
  operator may use manually or through local CLIs. The portable baseline does
  not automate external subscription APIs or query subscription usage limits.

## Conclusion

No further prompt is required for the portable-operator extension unless the
operator creates a new follow-up promptset. Remaining gaps are future-work
items, not blockers for the documented baseline.
