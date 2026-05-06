# Readiness Gate

The readiness gate inspects the immediate next prompt after an active prompt
step. It exists to keep a sequential runner from drifting into future work or
continuing when the next fresh session cannot start cleanly.

## Inspection

For `PROMPT_36`, the gate looks for `.prompts/PROMPT_37.txt` unless a supplied
outer-loop plan shows `PROMPT_36` is the final planned prompt. The check is
intentionally local and shallow: it confirms the next prompt file exists and
records a readiness label in the gate report.

## Passing Readiness

Readiness passes when the immediate next prompt exists and no current gate
blocker makes continuation unsafe. In the report this appears as:

- `ready` when the next prompt is required and present
- `not-required` when the supplied plan makes the current prompt the final
  planned step
- `blocked` when the next prompt is required but missing

## Blockers

Blockers include a missing next prompt, unreadable git state, unmerged git
entries, a missing active prompt, a supplied plan that cannot be read, or a
supplied plan that does not contain the active prompt.

The runner should stop on blockers. It should not patch future prompts
automatically unless a prompt explicitly authorizes a cheap bridge fix, such as
repairing an index link or clarifying a reference created by the current
session. Creating or expanding future prompt deliverables belongs to the
future prompt session, not the readiness gate.
