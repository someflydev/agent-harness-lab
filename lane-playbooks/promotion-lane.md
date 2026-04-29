# Promotion Lane

## Operator Setup

Use this playbook when a temporary observation, finding, or lane lesson may
deserve durable memory. Start with `runbooks/promotion-review.md`,
`role-packs/lead.md` for review ownership, or `role-packs/auditor.md` when the
promotion is evidence-heavy.

Promotion requires explicit review. A Worker may flag a candidate but does not
approve it.

## Role Sequence

1. Orchestrator or Lead frames the candidate and source evidence.
2. Reviewer checks whether the candidate is durable, specific, and useful.
3. Lead recommends promote, revise, defer, or reject.
4. Operator or approved process decides final promotion.
5. Assigned role updates the narrowest durable artifact and records evidence.

## Artifacts Passed Between Roles

- Candidate statement, source file, and reason it might be durable.
- Evidence links from docs, reports, findings, or validation output.
- Promotion review note or `templates/memory/promotion-record.md`.
- Final changed artifact and validation evidence.

## Expected Validations

- Confirm the candidate is not raw unreviewed assistant chatter.
- Confirm the target artifact is the narrowest useful durable home.
- Check docs navigation or registries if the promotion adds new artifact
  surfaces.
- Run `python3 scripts/ahl.py validate` when docs or metadata are updated.

## Merge Or Synthesis Point

The synthesis point is the promotion decision. Only after approval should the
assigned role update durable docs, findings, or memory records.

## Failure And Escalation Handling

Reject or defer candidates with weak evidence, broad claims, or unclear future
value. Escalate to the operator when the promotion changes doctrine, workflow
policy, or long-lived project direction.

