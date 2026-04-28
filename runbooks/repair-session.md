# Repair Session

## Purpose

Fix a bounded blocker, validation failure, or small gap identified by review,
audit, or handoff without reopening the whole original prompt.

## When To Use It

Use when the operator asks to repair a specific issue or when a previous session
left `tmp/HANDOFF.md` with a bounded next action. Use
`templates/handoffs/repair-checklist.md` when a checklist helps constrain the
repair.

## Required Context To Load

- `AGENT.md`
- The operator's repair request.
- Active `tmp/HANDOFF.md`, if present and relevant.
- Original prompt only if needed to verify the defect.
- Affected files and nearest docs indexes.
- Validation command or manual check that failed.

## Roles Involved

- Operator: names or accepts the repair target.
- Recovery Planner: defines the repair boundary and stop condition.
- Worker: makes the smallest coherent fix.
- Validator: confirms the defect is resolved.

## Step-By-Step Procedure

1. State the defect, affected paths, expected outcome, and stop condition.
2. Run `git status --short` and preserve unrelated changes.
3. Load only the context needed to understand the defect.
4. Decide whether the repair is bounded. If it requires broad redesign, stop
   and ask for operator direction.
5. Edit only the affected artifacts and necessary navigation.
6. Run the check that proves the defect is resolved.
7. Re-run any adjacent manual checks that could have been affected.
8. Remove or update `tmp/HANDOFF.md` only when the repair makes it obsolete and
   the operator's workflow expects cleanup.
9. Close with the repaired issue, evidence, and remaining risk.

## Expected Artifacts

- Focused changes to affected files.
- Optional repair checklist if the work has multiple small checks.
- Validation evidence proving the named defect is fixed.
- No broad refactor or future-prompt implementation.

## Validation Or Evidence

- The original failure mode no longer reproduces.
- Required links or files exist after the repair.
- Changed docs make claims that match current repo capabilities.
- Git status distinguishes repair changes from unrelated user changes.

## Stop Conditions

- The defect cannot be reproduced or explained.
- The repair scope expands beyond the named issue.
- Fixing the issue requires operator policy or sequencing decisions.
- Validation cannot run for reasons unrelated to the repair.

## Common Failure Modes

- Re-running the original prompt instead of fixing the named gap.
- Treating a repair as permission to rewrite surrounding docs.
- Ignoring a handoff's stop condition.
- Failing to run the specific check that exposed the problem.
