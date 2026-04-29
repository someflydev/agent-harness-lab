# Lane Playbooks

Lane playbooks describe how an operator can manually simulate role-separated
work without a runtime. They use role packs, prompt templates, contracts, and
runbooks to keep each session bounded.

## Playbooks

- `single-lane-docs-work.md` - one documentation lane from brief to closeout.
- `parallel-lane-docs-and-scripts.md` - manual parallel lanes with separate
  doc and script ownership.
- `repair-lane.md` - bounded repair from a handoff or review finding.
- `promotion-lane.md` - memory or finding promotion review.

## Shared Rules

- Assign disjoint file ownership before work starts.
- Pass durable artifacts and summaries between roles, not raw transcripts.
- Keep Worker context smaller than Lead context and Lead context smaller than
  Orchestrator context.
- Validate before synthesis.
- Escalate instead of guessing about scope, authority, memory promotion, or
  destructive actions.

Useful companion templates live in `templates/lane/`.

