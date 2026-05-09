# Portable Run Range Plan

Plan id: `<PLAN_ID>`
Project root: `<PROJECT_ROOT>`
Prompt range: `<START_PROMPT>` through `<END_PROMPT>`
Mode: dry-run/read-only

## Boundary

This artifact is a review plan. It does not invoke assistants, edit target
project files, stage changes, commit, amend, rebase, push, tag, or schedule
automatic continuation.

## Per-Prompt Phase Order

1. Run one prompt in a fresh assistant session.
2. Audit implementation, next-prompt readiness, and context-update needs.
3. Optionally repair a bounded defect while context is fresh.
4. Plan commits after validation review.
5. Make commits only after explicit operator approval.
6. Check commits.
7. Stop at the fresh-session boundary before the next prompt.

## Restart State

Use the JSON plan's `restart_state` object for project root, prompt ids,
planned artifact path, stop reason, and next prompt pointer.
