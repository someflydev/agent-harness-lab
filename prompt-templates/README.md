# Prompt Template Library

Purpose: provide reusable, copyable prompts for recurring human-assisted
`agent-harness-lab` routines without creating another implementation promptset.

Use these templates when an operator wants to start a routine session, assign
bounded work, request a review, or package validated changes. Replace
placeholders such as `<PROMPT_ID>` and `<TARGET_SCOPE>` with concrete values
before use.

## Templates

- `prompt-run.md` - run one prompt in a fresh session.
- `completion-audit.md` - audit completed work against an active prompt.
- `next-prompt-preflight.md` - check immediate next-prompt readiness.
- `bridge-decision.md` - decide whether a bridge fix or handoff is justified.
- `handoff-compose.md` - compose `tmp/HANDOFF.md` when needed.
- `repair-session.md` - start a bounded repair session.
- `promotion-review.md` - review a candidate for durable memory promotion.
- `prompt-authoring.md` - create or revise prompt files in a dedicated session.
- `orchestrator-lane-plan.md` - plan Orchestrator lanes for bounded work.
- `lead-worker-task.md` - assign a Lead-to-Worker task.
- `worker-result.md` - report bounded Worker results upward.
- `review-findings.md` - review changes and report findings.
- `commit-package.md` - package commits only when the operator asks.

## Required Context

Load the template itself, the operator request, and the authoritative repo docs
named inside the template. Do not assume hidden context from an earlier chat.

## Expected Output

Each filled template should produce a bounded session instruction, assignment,
report, or decision note with concrete files, evidence, stop conditions, and any
operator decisions needed.

## Stop Conditions

Stop when the selected routine is complete, when required context is missing,
when the work expands beyond the template purpose, or when an operator decision
is required.

