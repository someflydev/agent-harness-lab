# Repo Layout

This page describes the intended top-level areas for `agent-harness-lab`. Some
exist now; others are planned for later prompts.

## Existing Now

- `.prompts/` - ordered prompt files intended to be run one at a time in fresh
  assistant sessions.
- `docs/` - foundation documentation, guardrails, operator start guidance, repo
  layout notes, reference influence notes, doctrine, and role taxonomy.
- `README.md` - public identity and high-level project orientation.
- `AGENT.md` - assistant bootstrap guidance for future sessions.
- `.gitignore` - local reference repo, transient state, cache, and editor
  ignores.

Local reference clones such as `agent-context-base/`, `pi-mono/`, and
`claw-code/` may exist in a working copy, but they are ignored and are not part
of this repo's committed implementation.

## Planned Areas

- `runbooks/` - repeatable operator procedures for common workflows.
- `templates/` - reusable prompt, handoff, report, and review templates.
- `scripts/` - small helper scripts for checks, scaffolding, and local
  automation once the workflow is stable enough to justify them.
- `examples/` - worked examples that show how prompt-bounded sessions should
  look in practice.
- `experiments/` - bounded trials for harness ideas that are not yet doctrine.
- `reports/` - generated or manually prepared summaries of validation,
  readiness, and audit results.
- `findings/` - durable observations and lessons promoted out of session
  output.
- `runs/` - inspectable records of significant promptset or workflow runs when
  later prompts define the format.
- `tmp/` - ignored scratch space for transient handoffs and session-local
  material.

Planned areas should be created by the prompt that first gives them real
responsibility. Avoid empty structure that implies maturity the repo does not
yet have.
