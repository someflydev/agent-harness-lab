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
3. Validation, audit, and readiness gate integration.
4. Live sequential runner.
5. Commit planning and explicit commit execution.
6. Resume and failure handling.
7. Pi adapter experiment.
8. Outer-loop capstone.

## Implementation Notes

- Start with dry-run artifacts before live invocation.
- Keep each prompt scoped to one layer of runner behavior.
- Validate structural docs and promptset health after each phase-two prompt.
- Do not add provider credentials or dependencies unless a later prompt
  explicitly authorizes and designs them.
- Keep API-backed provider work separate from subscription CLI drivers.
- Treat commit execution as a separate approval boundary from assistant
  invocation.
- Use driver probes only for local availability checks until a later prompt
  adds explicit live-run consent.

## Exit Criteria

The outer-loop capstone should be able to show which parts are implemented,
which are still manual, which checks passed, and which provider or assistant
drivers have actually been validated locally. Until then, the outer loop should
be described as designed or partially implemented, not complete.
