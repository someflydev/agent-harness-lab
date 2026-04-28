# Task Contract

- Artifact id: example-org-worker-task
- Date: 2026-04-28
- Owner role: Documentation Worker
- Assigned by: Documentation Lead
- Prompt or lane: Examples navigation lane
- Permission posture: Local read/write only; no commit requested

## Scope

- Goal: Add one concise examples navigation section to `docs/README.md`.
- In scope: Match existing docs index style, link to the examples index, and
  keep wording illustrative rather than runtime-like.
- Out of scope: Reorganizing the docs index, changing example content, adding
  scripts, committing.
- Target files or areas: `docs/README.md`.

## Inputs

- Authoritative docs or prompts: `../../../docs/README.md`,
  `../../../examples/README.md`, `../../../docs/guardrails.md`.
- Existing artifacts: Examples directory README.
- Assumptions: The docs index can point from `docs/README.md` to the examples
  index with a valid relative link.

## Expected Outputs

- Deliverables: A compact docs index update and a result contract.
- Result format: `result-contract.md` style summary with changed files and
  evidence.
- Completion condition: The index can navigate to examples and wording does
  not claim examples are real session transcripts.

## Validation

- Checks to run: Confirm `examples/README.md` exists; inspect the link target.
- Evidence required: Files reviewed and any skipped checks.
- Reviewer: Documentation Lead.

## Boundaries

- Escalation triggers: Link target missing, no suitable docs index location, or
  requested wording conflicts with guardrails.
- Stop conditions: Do not invent new artifact categories beyond examples.
- Open issues or blockers: None at assignment time.
- Next step: Make the scoped docs index update and report back.
