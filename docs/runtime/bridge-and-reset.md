# Bridge And Reset

Bridge and reset keep fresh-session work continuous without turning raw session
chatter into durable memory.

## When To Create `tmp/HANDOFF.md`

Create `tmp/HANDOFF.md` only when a real blocker or non-trivial warning remains
and the next session would lose important context without a temporary file.

Useful handoff contents include:

- active prompt and current status
- blocker or warning
- affected files
- validation already performed
- next safe action
- what is intentionally out of scope

`tmp/HANDOFF.md` is transient. It is not doctrine, a runbook, or accepted
memory.

## When Not To Create Handoffs

Do not create a handoff when the active prompt is complete, the next prompt is
ready, and the final answer can carry the closeout summary. Do not create one
just to repeat changed files, routine validation, or general advice.

Do not store raw transcript, broad speculation, or future implementation plans
in a handoff.

## What A Bridge Fix Is

A bridge fix is a small, high-value change made during closeout to remove a
real blocker. It should be cheap to review and directly tied to current or
next-prompt readiness.

Examples:

- add a missing link to a newly created docs section
- clarify a term needed by the next prompt
- correct a stale file reference introduced by the current session

## What Bridge Fixes Are Out Of Scope

Bridge fixes must not implement the next prompt, create new prompt files, build
future scripts, or add durable memory that has not been reviewed. If the fix is
large enough to need its own validation plan, it is probably a repair session or
future prompt.

## Close Without Polluting Durable Memory

Keep temporary facts temporary. A final answer can report validation and
readiness. A handoff can carry short-lived continuation context. Durable docs
should only receive facts that belong to their artifact boundary and have been
checked.

Raw assistant output, temporary task notes, and unverified claims should not be
promoted just because they exist.

## Leave The Repo Ready

Before closeout:

1. Confirm required files exist.
2. Confirm navigation points to new durable docs.
3. Confirm no task-relevant command sessions remain running.
4. Confirm the immediate next prompt is ready, risky, or blocked.
5. Leave no unnecessary temporary files.

The next fresh session should be able to start from `AGENT.md`, the repo state,
and the operator request.
