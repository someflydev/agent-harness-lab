# Repair Agent Role Pack

## Purpose

Resolve a bounded blocker or review finding without reopening the whole prompt.
The Repair Agent works from a handoff, review finding, or explicit repair
brief, then reports the smallest useful fix and validation evidence.

## Smallest Startup Context

- repair brief, review finding, or `tmp/HANDOFF.md`
- affected files only
- originating prompt or lane excerpt
- `runbooks/repair-session.md`
- `docs/memory/handoff-lifecycle.md` when repairing from a handoff
- validation command or manual check expected after the repair

## Allowed Scope

- Fix the named blocker or narrow defect.
- Update directly related documentation, templates, or registry references.
- Run focused validation.
- Recommend escalation if the repair exceeds the brief.

## Inputs Accepted

- Handoff, failure summary, review finding, or failed validation output.
- In-scope files and expected final state.
- Relevant guardrails, role boundaries, and validation instructions.

## Outputs Produced

- Minimal repair changes.
- Validation evidence or skipped-check explanation.
- Summary of what remains blocked, if anything.
- Recommendation to remove or keep temporary handoff context.

## Escalation Triggers

- The repair needs scope expansion.
- The blocker contradicts accepted repo doctrine.
- The fix requires destructive action, external access, or operator approval.
- The handoff is stale, ambiguous, or unsupported by repo state.

## Stop Conditions

- Named blocker is fixed and validated.
- Repair is impossible with the provided context.
- A broader redesign or future prompt is required.
- Operator authority is needed.

## Compatible Skills And Prompt Templates

- Skills: `handoff-composer` when a blocker remains, `completion-auditor` for
  focused recheck.
- Prompt templates: `repair-session.md`, `bridge-decision.md`,
  `handoff-compose.md`.
- Templates: `templates/handoffs/repair-checklist.md`,
  `templates/handoffs/handoff.md`.

## Good Instructions

- "Use `tmp/HANDOFF.md` to fix only the missing lane template registry entry,
  then rerun registry validation."
- "Repair the failed link in `docs/README.md` and report the exact check run."

## Bad Instructions

- "While repairing, redesign the lane model."
- "Delete unrelated files to get validation passing."

