# Known Limitations

`agent-harness-lab` is intentionally human-assisted first. The operator chooses
the prompt, grants permissions, reviews changes, decides whether a bridge
handoff is justified, and controls commits.

## Runtime Limits

- No provider orchestration runtime exists.
- No live multi-agent daemon exists.
- No assistant invocation layer, model router, queue worker, server, TUI, or
  background scheduler is implemented.
- Phase-two outer-loop docs in `outer-loop/` define requirements and safety
  boundaries for a possible sequential runner, but no live runner is
  implemented yet.

## Validation Limits

- Helper scripts are structural checks, not semantic proof that a prompt was
  completed correctly.
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
