# Bridge Fix Session

## Purpose

Remove a cheap readiness blocker or write a temporary handoff when the current
session cannot close cleanly without preserving context.

## When To Use It

Use after a completion audit or next-prompt preflight finds a real blocker,
warning, broken reference, missing navigation link, or small terminology gap.

Do not use it to implement the next prompt, build scripts, create new prompt
files, or perform broad cleanup.

## Required Context To Load

- Active prompt and completion audit result.
- Immediate next prompt and preflight result.
- Affected files or indexes.
- `templates/handoffs/handoff.md`.
- `docs/runtime/bridge-and-reset.md`.

## Roles Involved

- Orchestrator: decides whether bridge work is justified.
- Worker: applies a narrow fix when authorized by scope.
- Handoff Composer: writes `tmp/HANDOFF.md` when a file is needed.
- Operator: resolves decisions that exceed scope.

## Step-By-Step Procedure

1. Name the blocker or warning in one sentence.
2. Decide whether it is cheap, concrete, and adjacent to the current prompt.
3. Apply a bridge fix only when the change is small, reviewable, and tied to
   current or next-prompt readiness.
4. Re-run the specific manual check that exposed the issue.
5. If the issue cannot be fixed safely, decide whether final-answer notes are
   enough.
6. Create `tmp/HANDOFF.md` only when the next fresh session would otherwise
   lose material context.
7. In the handoff, include current status, blocker, affected files, validation
   already performed, next safe action, and out-of-scope boundaries.
8. Stop after the blocker is removed or clearly recorded.

## Expected Artifacts

- A small docs or reference fix, when appropriate.
- Optional `tmp/HANDOFF.md` shaped by `templates/handoffs/handoff.md`.
- Closeout statement explaining the bridge decision.

## Validation Or Evidence

- The broken link, missing reference, or unclear term is checked after the fix.
- The fix is visible in a small diff.
- The handoff names a real blocker or non-trivial warning.
- No future-prompt deliverable is added.

## Stop Conditions

- The fix would require a new design decision.
- The fix would become a second implementation phase.
- The issue belongs to a future prompt's primary deliverables.
- Final-answer notes are sufficient and no temporary file is needed.

## Common Failure Modes

- Creating handoffs by default.
- Using bridge time for broad refactors.
- Hiding next-prompt work inside a readiness fix.
- Writing vague handoffs that omit affected files or next action.
