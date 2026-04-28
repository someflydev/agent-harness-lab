# Adjacent Prompt Readiness

Adjacent-prompt awareness is a superpower because it catches handoff failures
at the moment they are cheapest to fix. It gives the current session enough
future context to leave a clean runway without turning into broad future
planning.

## Why The Current Prompt Is Not Enough

Current-prompt completion asks whether this session delivered what it promised.
The next session also needs navigation, terminology, prerequisites, and repo
state that make its own prompt executable from a fresh context.

A session can be complete while the next prompt is risky. For example, Prompt
05 can satisfy its runtime docs while Prompt 06 remains risky if memory docs
cannot find bridge terminology or if `docs/README.md` omits runtime navigation.

## Why Whole-Future Planning Is Wasteful

Inspecting the whole promptset burns context and encourages speculative work.
Later prompts may be revised, reordered, or superseded. The useful closeout
question is narrower: can the immediate next prompt start safely?

## How To Inspect The Immediate Next Prompt

Read the next prompt's startup instructions, required deliverables, explicit
prerequisites, constraints, and endcap. Then compare those requirements against
the current repo. Look for missing docs, broken navigation, conflicting terms,
and obvious uncommitted task-related state.

Do not implement next-prompt deliverables during preflight.

## Complete Vs Ready

Current prompt complete means the active prompt's deliverables and validation
requirements are satisfied.

Next prompt ready means the next prompt can start in a fresh session with its
named prerequisites available and no obvious blocker caused by the current
state.

Use direct readiness labels in closeout:

- `ready` - no obvious blocker or material warning.
- `risky` - the next prompt can start, but a warning should be called out.
- `blocked` - the next prompt lacks a required prerequisite or cannot proceed
  safely.

## Fix Now Or Record

Fix immediately when the issue is cheap, clearly in scope, and improves
navigation or terminology for the next prompt. Examples include adding a docs
index link to a newly created section or correcting a misleading runtime term.

Record for handoff when the issue is real but cannot be fixed safely within the
current prompt. Examples include a missing prerequisite that belongs to another
prompt, a validation failure that needs operator input, or an unresolved design
choice.

Leave alone when the issue is speculative, belongs to future implementation, or
would require broad planning beyond the immediate next prompt.
