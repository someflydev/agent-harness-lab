# Portable Operator

The portable-operator extension is a planned local workflow layer for using
AHL from arbitrary project repositories that contain their own `.prompts/`
directory. It keeps the same human-governed loop as the AHL promptset:
one prompt, explicit context, validation, audit, next-prompt preflight, and a
fresh-session reset.

Most of this section is design guidance for later prompts, not a claim that the
full portable lifecycle exists. The implemented portable surface starts with
the read-only `project locate`, `project status`, `lifecycle snippets`,
`lifecycle context-check`, `lifecycle run-range`, and `commit check` commands.
Current outer-loop helpers still primarily operate inside the AHL repository.

## Start Here

- `extension-plan.md` - inventory of existing AHL helper behavior, missing
  portable-project behavior, and the remaining prompt arc.
- `invocation.md` - current supported `project locate` invocation forms,
  `AHL_HOME` behavior, target-project detection, and failure reporting.
- `status.md` - read-only target-project status reporting for git state,
  promptset diagnostics, bootstrap/context files, prompt-prefixed commits, and
  likely next prompt inference.
- `lifecycle-snippets.md` - reusable prompt-run, audit, context-update,
  commit-plan, commit-check, and optional repair snippets for one prompt.
- `run-range.md` - dry-run prompt-range planning that preserves
  one-prompt-at-a-time execution and fresh-session boundaries.
- `assistant-surfaces.md` - provider-agnostic boundary for Codex, Claude Code,
  Gemini, generic chat, and manual assistant surfaces.
- `one-prompt-loop.md` - end-to-end portable one-prompt loop from planning
  blob and promptset creation through audit, commit packaging, commit check,
  and fresh-session reset.
- `context-update-policy.md` - doctrine for deciding when prompt closeout
  should update bootstrap or context files and when no edit is appropriate.
- `commit-check.md` - read-only recent-commit inspection for prompt-prefix,
  message-format, generated-boilerplate, and grouping hygiene.
- `rehearsal.md` - deterministic fixture-based rehearsal that composes
  portable helpers from project discovery through commit-check evidence.
- `human-notes-boundary.md` - explicit operator-owned boundary for
  `human-notes.md` scratch/control-zone content.
- `non-goals.md` - explicit exclusions for the portable-operator extension.
- `../../fixtures/portable-operator/README.md` - artificial target-project
  fixtures for offline status, lifecycle, context-check, bootstrap-selection,
  and range dry-run examples.
- `../../examples/portable-operator/README.md` - copy/paste examples for a
  one-prompt cycle and prompt-range dry-run using those fixtures.

## Operating Posture

- AHL home is the checkout that contains `scripts/ahl.py`, AHL docs, templates,
  registries, schemas, fixtures, and tests.
- Target project root is the operator's current project repo. It may contain
  `.prompts/`, local assistant instructions, `.context/`, and
  `human-notes.md`.
- Portable commands should distinguish those roots in reports and file writes.
- The human operator remains scheduler, reviewer, validation authority, and
  commit authority; range plans are inspectable dry-runs, not schedulers.
- AHL produces snippets, payloads, plans, reports, and validation helpers; the
  human or chosen assistant CLI executes the prompt work.
- `human-notes.md` is operator-owned scratch content. AHL may report that it
  exists, but it must not edit it or treat it as authoritative state.
- The extension must stay local, inspectable, standard-library-first, and free
  of provider credentials, network calls, daemons, and hidden state.

## Offline Fixtures

Use `../../fixtures/portable-operator/projects/basic/` when you need a fake
target project with `AGENT.md`, `.context/`, and two sequential prompts. Use
`../../fixtures/portable-operator/projects/claude-bootstrap/` to test explicit
`CLAUDE.md` bootstrap selection. Use
`../../fixtures/portable-operator/projects/gapped/` to test prompt gap
diagnostics.

The examples in `../../examples/portable-operator/` show the expected command
sequence without using private notes, provider credentials, or assistant quota.
Run `python3 scripts/ahl.py portable rehearsal --json` from the AHL checkout
for the end-to-end offline fixture rehearsal used by capstone review.
