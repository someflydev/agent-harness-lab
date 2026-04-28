# Promotion Model

Promotion is the act of moving a useful fact from temporary context into a
durable repo artifact. Promotion requires evidence and review; existence is not
enough.

## Who Can Propose Promotion

Workers, Leads, Orchestrators, and the operator may identify a candidate. A
candidate should name the fact, source, target artifact, and reason it may
matter beyond the current run.

## Who Can Accept Promotion

The operator has final authority over durable promotion. An explicit approved
process may accept routine promotions later, but the default is human review.
Orchestrators and Leads can recommend or route candidates; Workers can flag
them but do not approve them.

## Evidence Required

Promotion should include enough evidence to make the durable update auditable:

- source path, prompt id, command, report, or observed failure
- validation performed, if the fact describes behavior
- scope of applicability
- target memory plane and artifact
- reason the fact is stable enough to preserve

Evidence can be compact. It should be traceable, not bureaucratic.

## When To Reject Promotion

Reject or defer promotion when:

- the fact is speculative, unverified, or contradicted by repo files
- the information belongs only to the active task
- the target artifact would become noisier or less navigable
- the source is raw transcript without independent review
- the claim describes future work as if it already exists
- metadata is being stored only because it exists
- a temporary handoff or run note would solve the need

## Promotion Decision Record

Use `../../templates/memory/promotion-record.md` when a promotion decision needs
an explicit record. For simple doc edits, a clear commit diff and final
validation summary may be enough.

A decision record should capture:

- candidate fact
- source evidence
- proposed target artifact
- reviewer or approver
- decision: accepted, rejected, or deferred
- durable update made, if accepted
- cleanup needed, if temporary notes should be removed

## Keeping Durable Memory Clean

Durable memory should be specific, current, and placed in the narrowest useful
artifact. Prefer editing an existing section over adding a new catch-all page.
Remove or revise superseded text when promoting a replacement fact.

Do not:

- dump raw transcripts
- copy temporary task notes into durable memory
- promote unverified implementation claims
- store metadata just because it exists
- preserve every run detail when a compact fact is enough

Promotion succeeds when the next fresh session can rely on the fact without
replaying the original session.
