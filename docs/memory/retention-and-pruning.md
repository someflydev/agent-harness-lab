# Retention And Pruning

Retention keeps useful context available. Pruning keeps memory from becoming a
second, stale transcript.

## Retention Rules

- Keep durable docs when they describe stable rules, accepted decisions, or
  reusable procedures.
- Keep examples when they remain clearly illustrative and distinct from live
  runtime state.
- Keep reports and findings when they preserve evidence that future sessions
  may need.
- Keep templates when they reduce repeated decision-making without adding
  bureaucracy.

## Pruning Triggers

Prune or revise memory when:

- a fact is superseded by a newer accepted artifact
- a note describes a completed temporary task
- the same guidance is duplicated across artifacts
- an implementation claim is no longer true
- a handoff has been consumed
- a report can be summarized into a smaller durable lesson

## Temporary Artifacts

Files under `tmp/` and live runtime files such as `context/TASK.md`,
`context/SESSION.md`, and `context/MEMORY.md` are local state. They should be
deleted, regenerated, or superseded as part of normal session hygiene.

## Durable Artifacts

Durable artifacts should be pruned through normal reviewed edits. When removing
or replacing memory, preserve enough context for future readers to understand
the current rule without replaying old sessions.

## Clean Memory Test

A memory artifact is healthy when a fresh session can answer:

- what fact should I rely on?
- where did that fact belong?
- is it current?
- what temporary material can I ignore?
