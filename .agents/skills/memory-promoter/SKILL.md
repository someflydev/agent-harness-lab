---
name: memory-promoter
description: Review whether a transient fact, observation, or repeated pattern should be promoted into durable repo memory.
---

## When To Use

Use when a session note, finding, repeated observation, or operator decision
may need to become durable memory. This skill is a review routine, not an
automatic transcript ingestion path.

## Required Context

- Candidate fact or observation
- Evidence source and affected artifact boundary
- `docs/memory/promotion-model.md`
- `docs/memory/planes.md`
- Relevant target docs, findings, or report templates

## Step-By-Step Behavior

1. State the candidate fact in one sentence.
2. Identify evidence and whether it is durable, transient, or unverified.
3. Decide the appropriate memory plane and target artifact boundary.
4. Choose `promote`, `defer`, or `reject`.
5. If promoting, edit the smallest durable artifact that should own the fact.
6. If deferring or rejecting, explain why in closeout notes rather than
   creating durable clutter.

## Expected Output

- Promotion decision with rationale
- Target path when promoted
- Validation or review evidence
- Residual risk if evidence is weak

## Stop Conditions

- Evidence is unavailable or only raw transcript.
- Target artifact ownership is unclear.
- The promotion would overstate an unvalidated pattern.
- Operator approval is needed for sensitive or strategic memory.

## Safety Notes

- Raw assistant chatter is not durable memory.
- Derived indexes and temporary files are not source of truth.
- Promote only facts that future sessions need and can verify.

## References

- `runbooks/promotion-review.md`
- `docs/memory/promotion-model.md`
- `docs/memory/planes.md`
- `docs/memory/run-memory.md`
- `findings/README.md`
- `prompt-templates/promotion-review.md`
