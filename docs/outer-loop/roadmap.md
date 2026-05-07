# Outer Loop Roadmap

This roadmap maps the remaining phase-two work after the requirements and
safety boundary layer.

## Phase-Two Sequence

1. Driver contracts and capability probes. Implemented as conservative registry
   records, docs, fixtures, and read-only `scripts/ahl.py driver` checks.
2. Batch planning and dry-runs. Implemented as deterministic plan artifacts,
   JSON schemas, fixtures, docs, and `scripts/ahl.py outer plan` /
   `scripts/ahl.py outer dry-run` checks. This layer still performs no live
   assistant invocation.
3. Validation, audit, and readiness gate integration. Implemented as
   conservative gate docs, schema, fixtures, template, and
   `scripts/ahl.py outer gate` report generation. Prompt validation commands
   are recorded, not executed arbitrarily.
4. Live sequential runner. Implemented as a dry-run-default `outer run` MVP
   with prompt payloads, run ledgers, manual driver support, conservative
   Codex/Gemini CLI invocation, per-step gates, and stop conditions.
5. Commit planning and explicit commit execution. Implemented as plan-only
   commit grouping, schema, fixtures, templates, docs, and an explicit
   approval-gated executor that stages only listed files.
6. Resume and failure handling. Implemented as run-ledger semantics, failure
   classification docs, recovery handoff template, artificial ledger fixtures,
   and `outer status` / `outer resume` / `outer recovery-handoff` helpers.
7. Pi adapter experiment. Implemented as conservative adapter design docs,
   comparison docs, registry and fixture updates, help-only probe coverage,
   dry-run planning support, and guarded live invocation marked
   `manual-confirmation-required`.
8. Outer-loop capstone.

## Implementation Notes

- Start with dry-run artifacts before live invocation.
- Keep each prompt scoped to one layer of runner behavior.
- Validate structural docs and promptset health after each phase-two prompt.
- Do not add provider credentials or dependencies unless a later prompt
  explicitly authorizes and designs them.
- Keep API-backed provider work separate from subscription CLI drivers.
- Treat commit execution as a separate approval boundary from assistant
  invocation. Commit planning is default; execution requires operator approval.
- Use driver probes for local availability checks. Live assistant invocation is
  now available only through explicit `outer run --execute` consent and remains
  bounded by driver contracts.

## Exit Criteria

The outer-loop capstone should be able to show which parts are implemented,
which are still manual, which checks passed, and which provider or assistant
drivers have actually been validated locally. Until then, the outer loop should
be described as designed or partially implemented, not complete.
