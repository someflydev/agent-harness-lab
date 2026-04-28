# Doctrine

This directory defines the shared doctrine and vocabulary for
`agent-harness-lab`. It is the foundation for later role, skill, memory,
template, runbook, script, example, and reporting work.

Doctrine in this repo is operational guidance. It names the working assumptions
that future prompts should preserve when adding new artifacts.

## Doctrine Files

- `principles.md` - core operating principles for prompt-bounded harness work.
- `glossary.md` - short repo-specific definitions for recurring terms.
- `anti-patterns.md` - concrete failure modes and their corrective behaviors.
- `artifact-boundaries.md` - boundaries between doctrine, runtime state,
  contracts, templates, reports, examples, and handoffs.
- `design-filters.md` - practical questions to ask before adding docs,
  scripts, metadata, or automation.

## How To Use This Doctrine

Read these files when a prompt introduces a new area of the harness or when a
session has to decide where an artifact belongs. Prefer updating doctrine when
the repo needs a durable rule, not when a single prompt needs a one-time note.

Doctrine should stay small enough to inspect in a fresh session. If an idea
needs detailed execution steps, it probably belongs in a later routine,
template, contract, or example rather than in doctrine.
