# Repo Layout

This page describes the top-level areas for `agent-harness-lab`.

## Existing Now

- `.prompts/` - ordered prompt files intended to be run one at a time in fresh
  assistant sessions.
- `docs/` - foundation documentation, guardrails, operator start guidance, repo
  layout notes, reference influence notes, doctrine, roles, skills, routines,
  runtime lifecycle, memory governance, contracts, quality, metadata, future
  architecture, and capstone audits.
- `runbooks/` - repeatable operator procedures for common workflows.
- `templates/` - reusable contract, handoff, memory, report, run, and closeout
  templates.
- `scripts/` - small helper scripts for checks, scaffolding, metadata examples,
  and local workflow support.
- `examples/` - worked examples that show prompt-bounded sessions in practice.
- `experiments/` - bounded trials for harness ideas that are not yet doctrine.
- `findings/` - reviewed lessons and recurring observations that may inform
  future prompt-authoring or memory promotion.
- `reports/` - retrospective summaries of session, promptset, routine, or phase
  evidence.
- `schemas/` - JSON Schemas for selected metadata and report shapes.
- `runs/` - generated run, plan, ledger, and commit-plan artifacts when an
  operator explicitly creates them; this directory may be absent in a clean
  checkout until a helper command writes an artifact.
- `tmp/` - ignored scratch space for transient handoffs and session-local
  material.
- `README.md` - public identity and high-level project orientation.
- `AGENT.md` - assistant bootstrap guidance for future sessions.
- `.gitignore` - local reference repo, transient state, cache, and editor
  ignores.

Local reference clones such as `agent-context-base/`, `pi-mono/`, and
`claw-code/` may exist in a working copy, but they are ignored and are not part
of this repo's committed implementation.

## Possible Later Areas

- Optional local indexes or automation hook areas only after the documented
  workflow and helper-script contracts prove they need them.

Planned areas should be created by the prompt that first gives them real
responsibility. Avoid empty structure that implies maturity the repo does not
yet have.
