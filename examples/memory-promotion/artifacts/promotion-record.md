# Promotion Record

- Artifact id: example-memory-promotion-record
- Date: 2026-04-28
- Owner role: Orchestrator

## Scope

- Promotion scope: Convert a repeated closeout observation into durable
  workflow guidance.
- Inputs: Temporary run note from an illustrative prompt run,
  `../../../docs/memory/handoff-lifecycle.md`,
  `../../../docs/runtime/bridge-and-reset.md`,
  `../../../examples/sequential-prompt-run/artifacts/handoff-not-created.md`.
- Expected durable output: A narrow examples artifact that teaches the
  no-handoff decision without creating a real `tmp/HANDOFF.md`.

## Source Observation

- Observation: Operators and assistants may be tempted to create
  `tmp/HANDOFF.md` for routine completion summaries even when no blocker
  remains.
- Source type: Ephemeral run memory from a fictional example scenario.
- Initial status: Untrusted until reviewed against durable docs.

## Candidate

- Fact: A handoff should be created only when a blocker or non-trivial warning
  would otherwise be lost; routine completion notes belong in closeout, not
  `tmp/HANDOFF.md`.
- Source evidence: Handoff lifecycle docs, bridge-and-reset docs, and the
  sequential prompt run no-handoff artifact.
- Proposed target artifact:
  `../../../examples/sequential-prompt-run/artifacts/handoff-not-created.md`.
- Proposed memory plane: Accepted Work Memory, with supporting Project Memory
  already present in the runtime and memory docs.

## Review

- Proposed by: Orchestrator.
- Reviewed by: Operator.
- Decision: Accepted.
- Decision date: 2026-04-28.
- Rationale: The fact is stable, already supported by existing docs, and useful
  for future fresh-session prompt runs.

## Rejection Criteria Considered

- Speculative or unverified: Rejected as a concern because durable docs already
  support the rule.
- Active-task-only detail: Rejected as a concern because the handoff decision
  recurs across prompt executions.
- Target artifact would become noisy: Rejected as a concern because the example
  uses one focused artifact.
- Raw transcript source: Avoided; the promoted fact is based on reviewed docs
  and a compact example artifact.
- Future work claimed as implemented: Avoided; the artifact states it is
  illustrative.

## Outcome

- Durable update made:
  `../../../examples/sequential-prompt-run/artifacts/handoff-not-created.md`.
- Validation performed: Reviewer checked the example against handoff lifecycle
  and bridge/reset docs.
- Temporary notes to delete or supersede: The ephemeral run note is not
  retained.
- Open issues or blockers: None.
- Follow-up: Keep future examples consistent with this handoff rule.
- Next step: Use the example as reference material, not as a mandatory runtime
  artifact.
