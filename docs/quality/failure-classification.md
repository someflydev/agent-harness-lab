# Failure Classification

Use these classes when auditing prompt execution or reviewing a session.

## Classes

- Missing deliverables: a required path or artifact was not created or updated.
- Stale docs: documentation describes behavior that the repo does not provide.
- Validation skipped: required or cheap relevant checks were not run and no
  reason was given.
- Prompt ambiguity: prompt wording allows conflicting interpretations that
  materially affect the work.
- Scope creep: the session implemented future-prompt work or unrelated
  refactors.
- Handoff misuse: `tmp/HANDOFF.md` was created for routine notes or omitted
  despite a real blocker.
- Next-prompt readiness blocker: the immediate next prompt lacks a prerequisite
  that should exist before a fresh session starts.

## Response

Classify the failure, assign severity, fix it when it is in scope, and record
the remaining risk in closeout. If the fix belongs to a future prompt, do not
hide that as done work.
