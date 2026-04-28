# Result Contract

- Artifact id: example-org-worker-result
- Date: 2026-04-28
- Owner role: Documentation Worker
- Source task contract: example-org-worker-task
- Prompt or lane: Examples navigation lane

## Inputs

- Task inputs: Worker task contract and current docs index.
- Authoritative docs or prompts: `../../../docs/README.md`,
  `../../../examples/README.md`, `../../../docs/guardrails.md`.

## Scope Completed

- Work completed: Added an examples section to the docs index with a valid
  relative link to the examples index.
- Work not completed: No script, prompt, or runtime changes were made.
- Changed files: `docs/README.md`.

## Outputs

- Deliverables produced: Docs index navigation entry for examples.
- Decisions made within scope: Placed examples after contracts and before
  runtime because examples demonstrate multiple existing artifact categories.
- Assumptions confirmed or rejected: Confirmed `examples/README.md` exists.

## Evidence

- Validation performed: Inspected `docs/README.md` and
  `examples/README.md`.
- Checks skipped and reason: No command-line check was necessary for a one-link
  docs index update in this illustrative example.
- Files or commands reviewed: `docs/README.md`; `examples/README.md`.

## Issues

- Open issues or blockers: None.
- Escalations raised: None.
- Promotion candidates: None.

## Closeout

- Reviewer or next owner: Documentation Lead.
- Recommended next step: Review wording and accept the lane if no capability
  overstatement is found.
