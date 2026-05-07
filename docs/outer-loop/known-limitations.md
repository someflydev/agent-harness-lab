# Outer Loop Known Limitations

The phase-two outer loop is bounded local helper tooling. These limitations are
part of the supported baseline.

## Execution Limits

- Live assistant runs can consume provider quota, change local assistant
  session state, and depend on local authentication outside AHL.
- AHL does not manage provider credentials, subscription state, rate limits,
  or model availability.
- Provider CLIs may change arguments, stdin behavior, help text, output shape,
  or authentication prompts.
- The `manual` driver does not invoke a model; it records the payload and the
  expected operator action.
- Pi support may remain probe and dry-run only unless the local print, JSON, or
  RPC behavior is verified and the registry contract is updated.
- Claude subscription automation is not supported outside Claude Code. AHL does
  not drive a generic Claude subscription web session.

## Validation Limits

- Structural checks do not prove semantic prompt completion.
- `outer gate` records arbitrary prompt validation commands instead of
  executing them, except for allowlisted AHL checks.
- Help-only probes do not prove authentication, quota, or safe unattended
  execution.
- Dry-runs validate plan structure and payload generation, not assistant
  quality.

## Data And Git Limits

- Transcript capture is intentionally limited. Raw assistant transcripts are
  not stored by default.
- Run ledgers and step summaries are durable evidence, but they are not a
  substitute for human review.
- Resume planning refuses dirty or unsafe worktrees; the operator must repair
  or review local changes first.
- Commit execution is opt-in and conservative. It requires a reviewed plan and
  explicit approval, stages only listed files, and refuses unsafe states.

## Architecture Limits

- The outer loop is not a daemon, scheduler, queue, TUI, server, MCP service,
  provider router, graph database, or vector retrieval system.
- Parallel lane experiments, richer semantic audit help, transcript
  summarization, metadata search, and API-backed providers remain future work.
