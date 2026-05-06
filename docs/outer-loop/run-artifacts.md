# Run Artifacts

The live runner writes inspectable artifacts under the plan's
`run_artifact_dir`, normally `runs/outer-loop/<plan-id>/`.

## Created Files

- `plan.json`: created earlier by `outer plan`.
- `payloads/<PROMPT_ID>.md`: the exact bounded prompt payload for one fresh
  assistant session.
- `step-summaries/<PROMPT_ID>.md`: a concise per-step summary placeholder or
  bounded final summary when available.
- `run-ledger.json`: the structured run ledger using
  `schemas/outer-loop-run-ledger.schema.json`.

## Commit Policy

Plans, docs, schemas, templates, and artificial fixtures are safe to commit
when reviewed. Live run ledgers may be committed only when they contain no raw
transcripts, secrets, provider credentials, or sensitive operator data.

Transient local outputs, raw transcripts, provider logs, scratch files, and
conversation exports should stay out of git. Raw transcript directories and
common dump filenames are already ignored and checked by `doctor`.

## Transcript Boundary

Raw transcripts are not captured by default because assistant chatter is not a
validated durable source of truth. Durable records should be bounded summaries,
validation evidence, gate results, readiness notes, and operator-reviewed
handoffs.

When a driver later supports bounded final-message output, the final assistant
summary may be copied into a step summary. That summary must be concise and
must not include raw transcript dumps.
