# Parallel-Lane Docs And Scripts

## Operator Setup

Use this playbook when one lane owns documentation and another owns script or
validation changes. It can be simulated manually in sequence; actual parallel
execution is optional.

Before starting, assign disjoint ownership:

- Docs lane: named markdown, template, or registry files.
- Scripts lane: named script, test, or command documentation files.
- Shared files: one Lead owns final integration, or the Orchestrator reserves
  them for synthesis.

## Role Sequence

1. Orchestrator creates separate lane briefs with non-overlapping write scopes.
2. Docs Lead decomposes documentation tasks and reviews docs Workers.
3. Scripts Lead decomposes script or test tasks and reviews script Workers.
4. Leads return lane status with changed files and validation evidence.
5. Orchestrator checks cross-lane claims, shared references, and final
   readiness.

## Artifacts Passed Between Roles

- Lane briefs with explicit write ownership.
- Worker assignments using `templates/lane/worker-assignment.md` or
  `prompt-templates/lead-worker-task.md`.
- Lane status records using `templates/lane/lane-status.md`.
- Validation output from docs checks, script tests, or registry checks.

## Expected Validations

- Docs lane: link/navigation review and `python3 scripts/ahl.py validate`
  when relevant.
- Scripts lane: focused unit tests or command checks named in the lane brief.
- Integration: `python3 scripts/ahl.py registry check` when registries change,
  plus a manual pass that script docs match actual command behavior.

## Merge Or Synthesis Point

The Orchestrator receives both lane statuses before final synthesis. If a
shared file must be changed, only the assigned integration owner edits it after
both lane results are known.

## Failure And Escalation Handling

Stop a lane when it needs files owned by another lane. Escalate conflicting
claims, failing validation, or shared-file drift to the Orchestrator. Do not
merge a lane summary that hides failed checks or unresolved ownership conflict.

