# Routine Record Format

Routine records should stay small enough for humans and assistants to read
quickly. Later runbooks and scripts can reuse this shape without treating it as
a full execution manifest.

```markdown
## Routine Name

- Purpose:
- Primary role:
- Supporting roles:
- When to use:
- Required inputs:
- Expected outputs:
- Stop conditions:
- Validation or evidence:
- Escalation triggers:
- Future automation potential:
```

## Field Guidance

`Purpose` states why the routine exists. `When to use` states the trigger, not
the procedure. `Required inputs` should name files, prompts, reports, or repo
state needed to run the routine. `Expected outputs` should be inspectable
artifacts, notes, decisions, or evidence.

`Stop conditions` are required. A routine that cannot say when to stop is not
ready to become a runbook or script.

`Future automation potential` should be conservative. Use phrases like
`checklist support`, `assistant routine`, `helper-script candidate`, or
`judgment-heavy` instead of implying automation already exists.

## Example

```markdown
## Completion Audit

- Purpose: Check active-prompt deliverables against actual repo artifacts.
- Primary role: Completion Auditor.
- Supporting roles: Orchestrator, Validator.
- When to use: Before declaring prompt completion.
- Required inputs: Active prompt, changed files, validation notes.
- Expected outputs: Pass, warning, or blocker statement with evidence.
- Stop conditions: Missing required artifact, material unchecked risk, or all
  deliverables verified.
- Validation or evidence: File paths, command results, and prompt requirement
  references.
- Escalation triggers: Missing authority, conflicting instructions, or weak
  validation for a high-risk change.
- Future automation potential: Checklist and helper-script candidate.
```
