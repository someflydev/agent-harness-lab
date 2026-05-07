# Known Limitations

`agent-harness-lab` is intentionally human-assisted first. The operator chooses
the prompt, grants permissions, reviews changes, decides whether a bridge
handoff is justified, and controls commits.

## Runtime Limits

- No provider credential manager, model router, queue worker, server, TUI, or
  background scheduler is implemented.
- No live multi-agent daemon exists.
- Phase-two outer-loop helpers can plan batches, dry-run plans, collect gates,
  build prompt payloads and run ledgers, rehearse manual-driver runs, plan
  resumes, generate commit plans, and invoke supported local assistant CLIs
  only through explicit `outer run --execute` consent.
- Live assistant CLI runs can consume quota and depend on local authentication
  outside AHL.
- Pi support remains guarded by `manual-confirmation-required` unless the local
  command and output contract are verified.

## Validation Limits

- Helper scripts are structural checks, not semantic proof that a prompt was
  completed correctly.
- Outer-loop gate reports do not replace human completion audits.
- Dry-runs validate deterministic scenario fixtures; they do not replace real
  prompt execution or human closeout review.
- Documentation link checks are local navigation checks, not external link
  audits or content-quality proofs.
- The doctor command performs conservative path and repo hygiene checks; it is
  not a full secret scanner or security product.

## Architecture Limits

- Graph and vector retrieval are future architecture only.
- Future architecture docs do not imply implemented runtime capability.
- Raw assistant transcripts are not durable repo memory. Durable memory must be
  promoted through reviewed artifacts.
- The outer loop is not a daemon, autonomous coding platform, transcript store,
  graph database, or vector retrieval system.
