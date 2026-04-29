---
name: handoff-composer
description: Compose tmp/HANDOFF.md for a justified bridge only when a blocker or non-trivial warning would otherwise be lost.
---

## When To Use

Use after a bridge decision determines that the next session needs temporary
context. Do not use for routine completion summaries that fit in the final
answer.

## Required Context

- Completion audit result
- Next-prompt readiness verdict
- Specific blocker, warning, or continuation risk
- Affected files and current repo state
- `templates/handoffs/handoff.md`

## Step-By-Step Behavior

1. Confirm the handoff is justified by a blocker or non-trivial warning.
2. Identify the next session's concrete first action.
3. Use the handoff template shape where practical.
4. Keep the note concise and temporary.
5. Include validation status and residual risk.
6. Avoid copying transcript history or routine summaries.

## Expected Output

- `tmp/HANDOFF.md` with concise context, status, risks, and next action
- Or a no-handoff decision when the final answer is sufficient

## Stop Conditions

- No material blocker or warning remains.
- Durable docs already contain the needed context.
- The handoff would become a substitute for required repo changes.

## Safety Notes

- `tmp/HANDOFF.md` is transient and should not become durable memory by
  default.
- Do not include raw assistant chatter.
- Do not use a handoff to defer required deliverables that can be completed
  cheaply now.

## References

- `runbooks/bridge-fix-session.md`
- `runbooks/run-closeout.md`
- `docs/runtime/bridge-and-reset.md`
- `docs/memory/handoff-lifecycle.md`
- `templates/handoffs/handoff.md`
- `prompt-templates/handoff-compose.md`
