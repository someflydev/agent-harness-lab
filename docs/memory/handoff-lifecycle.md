# Handoff Lifecycle

`tmp/HANDOFF.md` is temporary bridge memory. It helps the next fresh session
resume safely when a real blocker or non-trivial warning remains.

## When A Handoff Is Appropriate

Create `tmp/HANDOFF.md` only when all of these are true:

- the active prompt is blocked, incomplete, or leaves a meaningful warning
- the next session needs context that is not already clear from durable docs,
  git status, and the final answer
- the handoff can name the next safe action
- the content is short enough to consume quickly

Useful contents include active prompt, status, blocker, affected files,
validation already performed, next safe action, and out-of-scope boundaries.

## When No Handoff Should Be Created

Do not create a handoff when the active prompt is complete, the next prompt is
ready, and the final answer can carry the closeout summary. Do not create one
to repeat changed files, routine validation, broad advice, or raw transcript
content.

## How A Repair Session Should Consume It

A repair session should:

1. Read `AGENT.md`, the active repair request, and `tmp/HANDOFF.md`.
2. Verify the handoff against current repo state instead of trusting it
   blindly.
3. Fix the blocker or warning within the repair scope.
4. Record durable changes only in the appropriate reviewed artifacts.
5. Delete or supersede `tmp/HANDOFF.md` when it no longer helps.

## Deletion And Supersession

Delete `tmp/HANDOFF.md` after the blocker is resolved or when the next session
has consumed it. Supersede it only if a blocker remains and the old file would
mislead the next run. Since `tmp/` is ignored, handoffs should not appear in
reviewable git history.

## Handoffs Are Not Doctrine

Handoffs are situational. They may mention doctrine, but they do not create it.
If a handoff reveals a durable rule, propose that rule through the promotion
model and update the correct artifact after review.
