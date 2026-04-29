# Metadata

Metadata in this repo is helper data for bounded prompt execution. It should
make review, closeout, prompt authoring, and later pattern reuse easier without
becoming a second source of truth.

## Documents

- `run-record.md` - compact run record fields that pay rent during closeout and
  later review.
- `prompt-to-commit-traceability.md` - how prompt id commit prefixes connect
  prompt-bounded work to git history.
- `derived-metadata-rules.md` - rules that keep metadata derived,
  inspectable, and bounded.

## Schemas

- `../../schemas/run-record.schema.json` - JSON shape for a run record.
- `../../schemas/readiness-report.schema.json` - JSON shape for next-prompt
  readiness reports.
- `../../schemas/promptset-index.schema.json` - JSON shape for
  `python3 scripts/ahl.py promptset --json`.
- `../../schemas/lane-record.schema.json` - JSON shape for compact lane
  records.
- `../../schemas/traceability-record.schema.json` - JSON shape for compact
  prompt-to-commit traceability records.
- `../../fixtures/README.md` - artificial fixture examples and the documented
  limits of `python3 scripts/ahl.py fixtures check`.

## Use

Use metadata when it helps answer concrete questions:

- Which prompt produced this change?
- What validation was run?
- Did closeout find the next prompt ready?
- Was a handoff created, and why?
- Which commits later packaged the work?
- Did the run reveal a reusable pattern worth reviewing?

Do not create metadata just to preserve chat history or speculative future
state.
