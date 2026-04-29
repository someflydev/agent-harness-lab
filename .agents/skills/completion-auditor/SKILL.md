---
name: completion-auditor
description: Compare an active prompt's required deliverables, constraints, and validation needs against the repo state before completion is claimed.
---

## When To Use

Use near closeout, after implementation work, or when reviewing a previous
session's result. This skill checks completion; it does not perform new
implementation except for separately approved bridge fixes.

## Required Context

- Active prompt file
- `git status --short`
- Changed files and newly created artifacts
- Validation output or explicit skipped-check notes
- Relevant quality docs when severity or done state is unclear

## Step-By-Step Behavior

1. Extract every required deliverable and validation requirement from the
   active prompt.
2. Check that each required path exists and contains task-relevant content.
3. Compare constraints and explicit non-goals against the changed files.
4. Confirm docs or registries updated by the prompt do not overstate current
   capabilities.
5. Classify each deliverable as done, partial, or missing.
6. Report blockers, warnings, and residual risks with file-level evidence.

## Expected Output

- Pass, warning, or blocker verdict
- Deliverable checklist with evidence
- Validation commands run and results
- Clear list of remaining gaps, if any

## Stop Conditions

- A required deliverable is missing.
- Evidence is not available for a completion claim.
- The audit requires future-prompt implementation to pass.

## Safety Notes

- Do not hide partial completion behind a broad summary.
- Do not rewrite implementation during the audit unless the operator or active
  Endcap asks for a bounded bridge fix.
- Treat repo files and git history as authoritative.

## References

- `runbooks/completion-audit.md`
- `docs/quality/audit-protocol.md`
- `docs/quality/definition-of-done.md`
- `docs/quality/validation-gates.md`
- `prompt-templates/completion-audit.md`
