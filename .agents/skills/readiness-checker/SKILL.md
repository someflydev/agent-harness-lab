---
name: readiness-checker
description: Inspect the immediate next prompt and current repo state to decide whether the next fresh session is READY, RISKY, or BLOCKED.
---

## When To Use

Use during closeout after the active prompt is implemented and audited. Inspect
only the immediate next prompt unless the operator asks for broader promptset
review.

## Required Context

- Immediate next `.prompts/PROMPT_YY.txt`
- Current `git status --short`
- Docs or artifacts the next prompt names in Startup Instructions
- Current session's completion audit and residual-risk notes

## Step-By-Step Behavior

1. Read the next prompt's startup instructions, goal, deliverables, and
   validation section.
2. Verify referenced prerequisites and docs exist.
3. Check whether current changes created missing links, registry gaps, or
   ambiguous foundations for that prompt.
4. Run a lightweight adversarial pass: name one way the next prompt could fail
   despite startup files existing, or state that none was found after checking
   its startup instructions, deliverables, constraints, and validation.
5. Classify readiness as `READY`, `RISKY`, or `BLOCKED`.
6. For `READY`, include one evidence sentence explaining why the next fresh
   session can start cleanly.
7. Name cheap bridge fixes only when they directly unblock startup.
8. Avoid implementing the next prompt's deliverables.

## Expected Output

- Readiness verdict
- Concrete reason and affected files or docs
- Lightweight adversarial note and any verdict impact
- Optional bridge-fix recommendation
- Explicit statement when no handoff is needed

## Stop Conditions

- The check would require implementing future-prompt work.
- A missing prerequisite must be repaired before a fresh session can start.
- Operator direction is needed to choose between competing prompt paths.

## Safety Notes

- Adjacent readiness is not a full future-prompt execution.
- Do not inspect the whole promptset unless using `promptset-inspector`.
- Prefer final-answer notes over `tmp/HANDOFF.md` for routine ready states.

## References

- `runbooks/next-prompt-preflight.md`
- `docs/runtime/adjacent-prompt-readiness.md`
- `docs/runtime/bridge-and-reset.md`
- `templates/reports/readiness-report.md`
- `prompt-templates/next-prompt-preflight.md`
