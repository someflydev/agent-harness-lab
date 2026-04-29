# Memory

Memory in `agent-harness-lab` is governed shared state. It is not a transcript
dump, scratchpad archive, or automatic capture of everything an assistant said
during a run.

Use these docs to decide where facts belong, how temporary context expires, and
what review is required before information becomes durable project memory.

## Start Here

- `planes.md` - memory planes, ownership, lifespan, storage location, and
  promotion paths.
- `promotion-model.md` - how temporary observations become durable memory
  through evidence and review.
- `promotion-workflow.md` - command-backed workflow for proposing, checking,
  accepting, rejecting, and pruning memory candidates.
- `handoff-lifecycle.md` - when `tmp/HANDOFF.md` is useful, how it is consumed,
  and why it remains temporary.
- `run-memory.md` - conceptual shape of compact run facts without preserving a
  full transcript.
- `retention-and-pruning.md` - retention rules, pruning triggers, and cleanup
  expectations.

## Related Artifacts

- `../../templates/memory/promotion-record.md` - compact record for a promotion
  decision.
- `../../templates/memory/promotion-candidate.md` - queued candidate scaffold
  for reviewed promotion.
- `../../templates/memory/promotion-decision.md` - accepted or rejected
  decision scaffold.
- `../../templates/memory/memory-update-record.md` - compact record for durable
  memory changes.
- `../../memory/README.md` - committed curated memory workspace.
- `../../memory/promotion-queue/README.md` - queue boundary for proposed
  memory facts.
- `../../memory/accepted/README.md` - accepted decision record boundary.
- `../../memory/rejected/README.md` - rejected decision record boundary.
- `../../templates/memory/handoff-summary.md` - short handoff format for
  temporary continuation context.
- `../../context/TASK.example.md` - example active task scaffold.
- `../../context/SESSION.example.md` - example session continuity scaffold.
- `../../context/MEMORY.example.md` - example durable repo-local memory
  scaffold.

The live files `context/TASK.md`, `context/SESSION.md`, and
`context/MEMORY.md` are local runtime state. They are intentionally ignored and
must not be treated as committed truth.
