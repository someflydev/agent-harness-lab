# Memory Workspace

The committed `memory/` directory is a curated workspace for reviewed memory
promotion. It is not session storage, a transcript archive, or a replacement
for project docs.

Use this area to hold auditable promotion candidates and decision records while
the durable source of truth remains in the narrowest useful repo artifact:
docs, runbooks, templates, findings, examples, scripts, or tests.

## What Belongs Here

- Promotion candidates that need review before becoming durable memory.
- Accepted decision records that point to the evidence and durable update.
- Rejected decision records that explain why a candidate should not be reused.
- README files that define the boundaries of each memory area.

## What Must Never Be Stored

- Raw assistant transcripts or full chat logs.
- Secrets, credentials, tokens, personal data, or private operator notes.
- Unverified implementation claims.
- Temporary scratch state that belongs in ignored `tmp/` files.
- Broad doctrine copied from elsewhere without repo-specific review.

## Workspace Areas

- `promotion-queue/` contains proposed memory facts awaiting review.
- `accepted/` contains decision records for accepted promotions.
- `rejected/` contains decision records for rejected or deferred promotions.

Accepted memory is not automatically true because a file exists here. The
decision record must point to the durable artifact that was updated, or explain
what follow-up remains.

## Difference From `tmp/`

`tmp/` is ignored local continuation state for handoffs, scratch notes, and
bridge context. It can expire as soon as a fresh session consumes it.

`memory/` is committed, reviewed, and auditable. Add to it only when the record
will help future sessions without replaying a transcript.
