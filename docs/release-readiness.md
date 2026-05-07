# Release Readiness

This checklist defines the minimum local evidence required before calling
`agent-harness-lab` usable for a public or first-useful baseline. It is a
release-readiness gate for the human-assisted lab, not a production-readiness
claim.

## Required Checks

- Promptset lint passes:
  `python3 scripts/ahl.py promptset lint`
- Documentation link and navigation checks pass:
  `python3 scripts/ahl.py docs check`
- Registry checks pass:
  `python3 scripts/ahl.py registry check`
- Helper script tests pass:
  `python3 -m unittest tests/test_ahl.py`
- Dry-run checks pass:
  `python3 scripts/ahl.py dry-run check --all`
- Safety checks pass:
  `python3 scripts/ahl.py doctor`
- Domain pack checks pass when domain packs have changed:
  `python3 scripts/ahl.py domain-pack check`
- README and AGENT boot paths are current, concise, and aligned with the
  active workflow.
- Known limitations are documented in `docs/known-limitations.md`.
- Operating baseline and final audit docs are current when closing the initial
  baseline: `docs/capstone/operating-baseline.md`,
  `docs/capstone/final-audit.md`, and
  `docs/capstone/promptset-completion-report.md`.
- Phase-two outer-loop capstone docs are current when claiming bounded
  outer-loop support: `docs/outer-loop/capstone-audit.md`,
  `docs/outer-loop/operating-baseline.md`,
  `docs/outer-loop/smoke-test-plan.md`,
  `docs/outer-loop/known-limitations.md`, and
  `docs/outer-loop/future-work.md`.

## Console Sweep

When the Makefile exists, run the safe read-only console targets as a compact
operator sweep:

```sh
make help
make doctor
make promptset
make lint-prompts
make check-docs
make test
make domain-pack
make dry-run
make lane-check
make registry
make memory-check
make experiment-check
```

`make checkpoint` is intentionally omitted from this sweep because it can
create missing `context/*.md` files.

## Review Criteria

Before closing a release-readiness pass, verify:

- New docs are reachable from `README.md` or `docs/README.md`.
- Helper commands documented in `scripts/README.md`, `docs/operator-console.md`,
  and `Makefile` agree.
- Registry guidance remains clear that registries are navigation aids, not a
  second source of truth.
- Any remaining gaps are named as limitations instead of implied features.
- Capstone docs identify unavailable checks honestly and do not claim provider
  orchestration, autonomous runners, graph or vector retrieval, or production
  safety scanning unless those capabilities have actually been implemented and
  validated.
- Outer-loop release claims stay limited to bounded local support when checks
  pass and the operator explicitly enables live execution.
