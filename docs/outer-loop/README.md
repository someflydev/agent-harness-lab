# Outer Loop

The outer loop is a phase-two design area for a local sequential wrapper around
the existing fresh-session prompt workflow. It now includes deterministic
planning, dry-run checks, post-prompt gate reports, and a conservative
dry-run-default live runner MVP.

The goal is bounded orchestration of already-authenticated assistant tools, one
prompt at a time. The runner should make decisions visible through files,
structured output, validation evidence, completion audits, and explicit
operator approval points.

## Start Here

- `requirements.md` - target workflow, stop conditions, and the canonical
  batch-run example that is not implemented yet.
- `safety-boundary.md` - consent, dry-run, git, transcript, credential, and
  failure boundaries.
- `sequential-runner-model.md` - component model and current versus future
  implementation status.
- `assistant-driver-boundary.md` - vocabulary and provider boundary for
  subscription CLIs and API-backed runtimes.
- `driver-contracts.md` - conservative local assistant driver record shape and
  live-run boundary.
- `capability-probes.md` - safe PATH and help-only probe behavior before live
  assistant invocation exists.
- `batch-planning.md` - inspectable prompt batch plan artifacts and range
  resolution rules.
- `dry-run-runner.md` - structural dry-run checks for batch plans before any
  future live execution.
- `gates.md` - post-prompt gate statuses, evidence fields, report format, and
  CLI boundary.
- `live-runner.md` - dry-run-default sequential runner behavior and live
  execution consent boundary.
- `prompt-payloads.md` - exact bounded payload shape sent to each fresh
  assistant session.
- `run-artifacts.md` - ledger, payload, summary, transcript, and commit-policy
  boundaries for outer runs.
- `completion-audit-integration.md` - how gate reports integrate deterministic
  checks with human or assistant semantic audit.
- `readiness-gate.md` - immediate next-prompt readiness checks and stop
  behavior.
- `non-goals.md` - explicit exclusions for the outer-loop design.
- `roadmap.md` - phase-two implementation sequence after this requirements
  layer.

## Current Status

The current layer includes requirements, safety boundaries, conservative driver
contracts, safe capability probes, plan artifacts, dry-run plan validation,
gate reports, prompt payload generation, run ledgers, and explicit
`--execute` live CLI invocation for supported local driver contracts. It does
not add provider credentials, a daemon, a TUI, an MCP server, a scheduler, or
dependency-backed runtime code.
