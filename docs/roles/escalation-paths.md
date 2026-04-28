# Escalation Paths

Escalation protects the harness from silent guessing. Each role should stop
when a decision belongs above its authority or when continuing would create
unreviewed durable project direction.

## Worker To Lead

A Worker escalates to the Lead when:

- The assignment cannot be completed with the provided context.
- The task would require files, decisions, or scope outside the brief.
- Existing files conflict with the assignment.
- Validation evidence is unavailable or materially weak.
- The Worker finds an assumption that affects lane completion.

The Worker record should include the task, the exact blocker, files inspected,
evidence gathered, and a recommended next question. It should not include a raw
session transcript.

## Lead To Orchestrator

A Lead escalates to the Orchestrator when:

- The lane requires active-prompt scope changes.
- Lane work conflicts with another lane or with doctrine.
- Worker outputs cannot be integrated without a broader decision.
- Lane validation is insufficient for completion claims.
- A bridge handoff, readiness warning, or memory promotion decision may be
  needed.

The Lead record should summarize lane status, decisions already made, Worker
outputs reviewed, unresolved assumptions, and the specific Orchestrator
decision requested.

## Orchestrator To Human Operator

The Orchestrator escalates to the operator when:

- The prompt conflicts with operator intent, doctrine, or repo guardrails.
- Continuing requires product direction, commit approval, destructive action,
  external access, or authority not granted by the active prompt.
- The repo cannot be left ready for the next prompt without a non-trivial
  bridge decision.
- Completion would require overstating validation evidence.

The Orchestrator record should be concise: decision needed, options if known,
risks, evidence, and recommended next action.

## When To Stop Instead Of Guessing

Stop instead of guessing when the next step would:

- Change durable project direction.
- Create or promote memory without review.
- Expand beyond the active prompt or lane.
- Hide missing validation.
- Rewrite unrelated user work.
- Depend on vendor-specific assumptions not already accepted by the repo.

Stopping is an operating behavior, not a failure. The harness favors explicit
operator control over hidden autonomy.

## Escalation Record Shape

Escalation records should preserve context without dumping transcripts:

```md
## Escalation

- From:
- To:
- Prompt or lane:
- Decision needed:
- Evidence:
- Files or commands checked:
- Options:
- Risk of guessing:
- Recommended next action:
```

Use links to durable files and short summaries. Include transcript excerpts
only when the exact wording is the evidence.
