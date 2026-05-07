# Outer Loop Future Work

These items are backlog candidates, not new required prompts for the phase-two
baseline.

- Richer driver adapters for verified local CLI contracts, including clearer
  final-message capture and failure classification.
- Stronger semantic audit assistance that helps a human compare prompt
  deliverables with repo changes without claiming autonomous completion.
- Opt-in transcript summarization with explicit redaction, retention, and
  review policy.
- Multi-worktree experiments for isolating prompt runs from unrelated local
  changes.
- Limited parallel lane experiments after the sequential runner proves stable.
- Local search over run metadata, ledgers, gate reports, and commit plans.
- API-backed providers when explicitly requested and designed as a separate
  capability from subscription CLI drivers.
- Better generated smoke fixtures for fake-driver failures, dirty worktree
  resume refusal, and commit executor refusal cases.
- More precise prompt registry status conventions for `outer plan --next`.
