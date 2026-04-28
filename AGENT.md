# AGENT.md

This file is the first-read bootstrap for coding assistants working in
`agent-harness-lab`.

## First Read Order

1. `AGENT.md`
2. `README.md`
3. `docs/guardrails.md`
4. The single `.prompts/PROMPT_XX.txt` the operator asked you to run
5. Any docs that prompt explicitly references

Do not scan local reference repos by default. Inspect them only when the active
prompt asks for reference influence or when a narrow comparison is needed.

## Before Acting

- Run `git status --short` and identify untracked or modified files before
  editing.
- Read existing hot-spot files before changing them.
- Treat user changes as intentional. Do not revert unrelated work.
- Modify files inside this repo only. Do not edit local clones of
  `agent-context-base`, `pi-mono`, or `claw-code`.

## Session Types

- Prompt-authoring sessions create or refine prompts, promptsets, or planning
  material. They should not quietly execute implementation work unless asked.
- Prompt-execution sessions run exactly one prompt in a fresh assistant session.
- Repair or bridge sessions fix blockers, fill small gaps, or prepare a clean
  handoff when a previous execution could not finish cleanly.

When running the promptset, execute one prompt per fresh session unless the
operator explicitly says otherwise.

## Endcap Routine

Use this closeout loop for prompt-execution sessions:

1. Execute the requested prompt.
2. Audit every required deliverable against the prompt.
3. Preflight the next prompt for obvious readiness issues.
4. Bridge only if there is a real blocker or non-trivial warning.
5. Reset by leaving the repo ready for the next fresh session.

Create `tmp/HANDOFF.md` only when it materially helps the next session. Do not
create or update it for routine completion notes that fit in the final answer.

## Validation

Before claiming completion:

- Verify required files and paths exist.
- Review changed docs for claims that overstate implemented features.
- Run available checks when the prompt requires them or when they are cheap and
  relevant.
- State any checks you could not run.

## Commit Hygiene

Do not commit unless the operator asks. When commits are requested, prefer
small reviewable groups and prefix messages with the prompt id, for example
`[PROMPT_01] Bootstrap foundation docs`.

## Hot-Spot Files

Treat shared files as integration targets. Read them first, preserve useful
existing structure, and update them surgically instead of rewriting them just to
fit a new outline.

Current and expected hot spots include:

- `README.md`
- `AGENT.md`
- `docs/README.md`
- `scripts/README.md`
- `scripts/ahl.py`
- `tests/test_ahl.py`
- `Makefile`

## Core Guardrails

Follow `docs/guardrails.md`. In short: keep this repo distinct from the
reference projects, favor inspectable artifacts before automation, preserve the
human-assisted subscription-friendly workflow, and treat repo files plus git
history as the durable source of truth.
