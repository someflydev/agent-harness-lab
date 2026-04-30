# Secrets And Transcripts

Secrets and raw transcripts should not be stored in this repo. They create
review burden, leak risk, and stale memory that future sessions may trust
without enough context.

## Secrets

Do not commit:

- `.env` files
- private keys
- credential exports
- service tokens
- password files
- provider API keys

The safety doctor uses conservative path-name checks for common secret-looking
files. It does not read file contents and is not a replacement for careful
review before committing.

## Raw Transcripts

Do not store raw assistant chats, provider exports, or conversation dumps as
project memory. When a session contains a reusable lesson, promote only the
reviewed fact into the right durable artifact:

- update a doc when the rule is stable
- create a report when evidence matters
- create a finding when there is a repeatable pattern
- queue a memory candidate when the fact needs promotion review

Keep private system prompts, user conversations, and provider exports outside
the repo unless the operator has explicitly approved a narrow sanitized excerpt.
