# Single-Lane Docs Work

## Operator Setup

Choose a documentation target, active prompt or operator request, expected
files, and validation checks. Start with `role-packs/orchestrator.md` or use
`prompt-templates/orchestrator-lane-plan.md` to create one lane brief.

Use `templates/lane/lane-brief.md` when the lane needs a durable brief.

## Role Sequence

1. Orchestrator defines the docs lane, scope, deliverables, and validation.
2. Lead reads the lane brief and assigns one or more bounded Worker tasks.
3. Workers edit only assigned docs and return result summaries.
4. Lead reviews Worker results, integrates the lane, and summarizes upward.
5. Orchestrator audits completion and next-prompt readiness when required.

## Artifacts Passed Between Roles

- Orchestrator to Lead: lane brief, active prompt excerpt, in-scope paths,
  validation expectations, and escalation triggers.
- Lead to Worker: worker assignment, exact files, expected output shape, and
  stop conditions.
- Worker to Lead: changed files, validation evidence, assumptions, and
  blockers.
- Lead to Orchestrator: lane status, accepted outputs, unresolved risks, and
  validation summary.

## Expected Validations

- Confirm every required docs file exists.
- Check links and registry references when relevant.
- Run `python3 scripts/ahl.py validate` or `python3 scripts/ahl.py registry
  check` when the lane touches docs navigation or registries.
- Manually confirm the docs do not claim unavailable automation.

## Merge Or Synthesis Point

The Lead synthesizes Worker outputs into the lane. The Orchestrator performs
the final prompt-level audit and decides whether a handoff is justified.

## Failure And Escalation Handling

Escalate to the Orchestrator when the docs lane requires future-prompt scope,
changes to role authority, or validation that cannot be run. Escalate to the
operator for commits, destructive actions, or durable direction changes.

