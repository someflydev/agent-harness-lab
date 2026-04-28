# Run Memory

Run memory records compact facts about a prompt execution without preserving a
giant transcript. It exists to make validation and handoff decisions
inspectable.

This is the conceptual model only. Do not add scripts or databases for run
memory yet.

## Useful Run Facts

A run note or future manifest may record:

- prompt id
- run id, when assigned by the operator or tool
- assistant or tool used
- permission posture
- changed paths
- validation performed
- blockers
- next-prompt readiness
- handoff created: yes or no

These facts should be summarized from evidence. They should not become a
verbatim session log.

## What To Omit

Run memory should not include raw assistant reasoning, full terminal logs,
large copied diffs, unrelated environment details, or metadata with no review
value.

## Relationship To Durable Memory

Most run facts expire after review. A run may identify a promotion candidate,
but the candidate still needs evidence, reviewer acceptance, and a targeted
artifact update before it becomes durable memory.

## Example Shape

```md
# Run Summary

- Prompt: PROMPT_06
- Run: local-2026-04-28
- Assistant/tool: Codex
- Permission posture: workspace-write, restricted network
- Changed paths: docs/memory/*, templates/memory/*, context/*.example.md
- Validation: required files checked; docs index checked
- Blockers: none
- Next prompt readiness: ready
- Handoff created: no
```
