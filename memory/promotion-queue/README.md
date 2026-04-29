# Promotion Queue

The promotion queue holds candidate facts that may deserve durable memory after
review. A queued file is a proposal, not accepted truth.

## What Belongs Here

- Specific facts, patterns, or workflow lessons with traceable evidence.
- Candidates that name a proposed target artifact.
- Candidates that explain why the fact may matter beyond the current run.
- Candidates created with `python3 scripts/ahl.py memory propose <slug>`.

## What Does Not Belong Here

- Raw transcripts or pasted assistant chatter.
- Speculation without evidence.
- Active-task scratch notes that belong in `tmp/` or `context/`.
- Claims that should directly become docs without review.

Run `python3 scripts/ahl.py memory check` before relying on the queue. The check
validates required headings and fields but does not approve promotion.
