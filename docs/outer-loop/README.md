# Outer Loop

The outer loop is a phase-two design area for a local sequential wrapper around
the existing fresh-session prompt workflow. It now includes deterministic
planning, dry-run checks, post-prompt gate reports, and a conservative
dry-run-default live runner MVP.

The goal is bounded orchestration of already-authenticated assistant tools, one
prompt at a time. The runner should make decisions visible through files,
structured output, validation evidence, completion audits, and explicit
operator approval points.

The portable-operator extension starts from this baseline but adds a separate
target project root. See `../portable-operator/README.md` for the planned
AHL-home versus target-project design; current outer-loop commands still
primarily operate on the AHL checkout.

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
- `pi-adapter.md` - bounded Pi external-harness adapter design and unknowns.
- `pi-vs-ahl.md` - comparison between Pi as a coding-agent harness and AHL as
  a promptset, validation, traceability, and orchestration lab.
- `provider-harness-comparison.md` - safety, auth, output, model-selection,
  and testing differences across current and future driver categories.
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
- `run-ledger.md` - durable ledger fields, resume pointer semantics, and
  transcript boundaries.
- `failure-classification.md` - failure classes, resume safety, repair needs,
  and automatic-action limits.
- `resume-and-recovery.md` - `outer status`, `outer resume`, and recovery
  handoff behavior.
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
- `../portable-operator/README.md` - planned extension for applying the
  one-prompt workflow from arbitrary project repositories.

## Current Status

The current layer includes requirements, safety boundaries, conservative driver
contracts, a guarded Pi external-harness adapter experiment, safe capability
probes, plan artifacts, dry-run plan validation, gate reports, prompt payload
generation, run ledgers, dry-run resume planning, recovery handoffs, and
explicit `--execute` live CLI invocation for supported local driver contracts.
It does not add provider credentials, a daemon, a TUI, an MCP server, a
scheduler, or dependency-backed runtime code.
