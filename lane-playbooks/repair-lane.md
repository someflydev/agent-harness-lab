# Repair Lane

## Operator Setup

Use this playbook when a previous session left a justified `tmp/HANDOFF.md`, a
review finding, or a failed validation result. Start from
`role-packs/repair-agent.md` and `runbooks/repair-session.md`.

Define the named blocker, affected files, validation needed, and out-of-scope
areas before editing.

## Role Sequence

1. Orchestrator or Lead confirms the blocker is still present in repo state.
2. Repair Agent reads the handoff or finding and only the affected context.
3. Repair Agent makes the smallest fix and runs focused validation.
4. Reviewer or Auditor checks whether the named blocker is resolved.
5. Orchestrator decides whether the temporary handoff can be removed or left
   for a remaining blocker.

## Artifacts Passed Between Roles

- Handoff, review finding, or failed command output.
- Repair brief with in-scope files and stop conditions.
- Repair result summary with changed files and validation evidence.
- Audit note confirming fixed, still blocked, or escalated.

## Expected Validations

- Re-run the failing check when available.
- Run registry checks when repair touches registries.
- Manually confirm the fix does not expand future-prompt scope.
- Confirm `tmp/HANDOFF.md` remains only if a real blocker still exists.

## Merge Or Synthesis Point

The repair result merges only after focused validation and a reviewer or
auditor confirms the named blocker was addressed. The Orchestrator then updates
the closeout state.

## Failure And Escalation Handling

Escalate when the handoff is stale, the blocker has changed shape, validation
still fails, or the repair would require broader redesign. Ask the operator
before destructive cleanup or commits.

