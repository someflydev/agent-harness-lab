# Data Hygiene

This repo keeps durable memory in reviewed files, not in raw session state.
Temporary files are useful during a run, but they should not become trusted
project facts by accident.

## Temporary Artifacts

Treat these as local runtime state:

- `tmp/`
- `tmp/HANDOFF.md`
- `context/TASK.md`
- `context/SESSION.md`
- `context/MEMORY.md`
- `.runtime/`
- `.session/`
- generated logs and caches

`tmp/HANDOFF.md` is only for a live bridge. If the blocker is resolved or the
next session no longer needs it, remove it or replace it with a durable doc,
report, finding, or memory decision.

## Durable Artifacts

Durable artifacts should be reviewed and scoped:

- docs describe stable rules or workflows
- reports summarize evidence without dumping raw chats
- findings preserve concrete observations and impact
- memory candidates enter review before becoming accepted memory

Do not promote scratch notes, broad transcripts, or assistant speculation
directly into durable docs. Summarize the inspected fact, cite the repo
artifact or command evidence, and keep the source narrow.
