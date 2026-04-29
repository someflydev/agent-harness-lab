# Lead Plan

## Lane

- Lane id: `lane-demo`
- Lead role: documentation lane lead
- Source: `orchestrator-brief.md`

## Decomposition

The lane has one Worker task: inspect the fictional template documentation
refresh request and report whether the files needed for a manual lane are
present, understandable, and locally checkable.

## Worker Assignment

- Worker: `worker-01`
- Task file: `worker-01-task.md`
- Expected result file: `worker-01-result.md`
- Files in scope: this simulation directory and `templates/lane/`
- Files out of scope: application code, provider integrations, prompt files,
  and unrelated docs

## Review Plan

The Reviewer checks whether the Worker result answers the assignment, whether
stop conditions were respected, and whether any findings block closeout.

## Escalation

Escalate to the operator if the Worker needs authority to edit real templates,
if the lane status cannot represent the current state, or if validation fails
after the lane artifacts are complete.

