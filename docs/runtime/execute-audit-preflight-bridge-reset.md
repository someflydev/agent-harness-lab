# Execute Audit Preflight Bridge Reset

The core prompt-execution rhythm is:

1. Execute the active bounded prompt.
2. Audit whether the active prompt is truly complete.
3. Preflight the immediate next prompt for readiness.
4. Bridge only when a cheap, high-value fix or temporary handoff is justified.
5. Reset so the next session can start fresh.

This is an operator routine, not a runtime engine.

## Execute

Perform the current bounded prompt or session work. Use the active prompt as
the unit of execution, read the files it names, preserve unrelated user
changes, and keep implementation inside the repo.

Execution is complete only when the required deliverables exist and the work is
coherent with repo guardrails. It is not complete just because edits were made.

## Audit

Compare the active prompt against the actual result. Check every required path,
explicit content requirement, constraint, and validation note. Review changed
docs for claims that overstate current capabilities.

The audit answers: "Did this session satisfy the active prompt?" It does not
answer whether future prompts are already implemented.

## Preflight

Inspect the immediate next prompt and the current repo state for readiness. A
good preflight checks whether the next session can find prerequisite docs,
shared terminology, navigation links, and any expected artifacts.

Preflight should stay adjacent. It is not a plan for the whole promptset and it
must not implement the next prompt.

## Bridge

Bridge is optional and bounded. A bridge fix is a cheap change that removes a
real blocker created or revealed by the current session, such as a missing docs
index link or a term needed by the next prompt. A bridge artifact is temporary
context, usually `tmp/HANDOFF.md`, created only when a blocker or non-trivial
warning would otherwise be lost.

Bridge must not become a hidden second implementation phase. If the work is a
future prompt's real deliverable, leave it for that prompt and report readiness
as risky or blocked.

## Reset

End cleanly. The final closeout should identify changed files, validation
performed, readiness for the next prompt, residual risks, and whether a handoff
was created. Do not commit unless the operator explicitly asks.

Reset means the next assistant can start from repo files, git state, and the
operator request without depending on unstated chat context.
