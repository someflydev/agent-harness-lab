# Skills

Skills describe reusable capabilities that a role can invoke while doing
prompt-bounded work. They are separate from roles: a role says who is
responsible, while a skill says what capability is being used.

This directory defines the early skill taxonomy for `agent-harness-lab`. It is
doctrine and navigation, not the package directory itself. Optional
project-level `.agents/skills/` packages now provide focused assistant-loadable
routine instructions while keeping provider-specific adapters and helper
automation out of scope.

## Documents

- `taxonomy.md` - skill areas, purpose, inputs, outputs, failure signals, and
  current support level.
- `maturity-model.md` - maturity ladder from named concept through possible
  runtime automation.
- `role-skill-map.md` - how Orchestrator, Lead, Worker, and supporting roles
  commonly invoke skill areas.
- `../project-skills.md` - how optional `.agents/skills/` packages differ from
  roles, routines, templates, and scripts.

## Use

Use these docs when writing prompt language, runbooks, templates, contracts,
examples, helper scripts, or reviews that need a stable capability vocabulary.
Do not treat a named skill as implemented automation unless its maturity level
explicitly says so.
