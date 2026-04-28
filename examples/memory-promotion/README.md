# Memory Promotion Example

This scenario shows how a temporary observation becomes durable memory only
after review, following `../../docs/memory/promotion-model.md` and
`../../runbooks/promotion-review.md`.

The fictional observation is that prompt-execution sessions repeatedly need a
quick reminder not to create `tmp/HANDOFF.md` for routine closeout notes. The
reviewer accepts a narrow durable update because it is supported by existing
handoff lifecycle docs and examples.

## Artifacts

- `artifacts/promotion-record.md` - candidate fact, evidence, reviewer,
  accepted memory plane, rejected alternatives, and durable outcome.

## What This Teaches

- Raw observation is not trusted memory by itself.
- Evidence must be traceable to repo artifacts or validation.
- The reviewer chooses the narrowest useful memory plane.
- Rejection criteria are considered before acceptance.
- The durable update is targeted; temporary notes are not copied wholesale.
