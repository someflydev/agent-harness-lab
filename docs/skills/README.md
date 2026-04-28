# Skills

Skills describe reusable capabilities that a role can invoke while doing
prompt-bounded work. They are separate from roles: a role says who is
responsible, while a skill says what capability is being used.

This directory defines the early skill taxonomy for `agent-harness-lab`. It is
doctrine and navigation, not a tool package system. Project-level `.agents`
skill packages, provider-specific adapters, and helper scripts belong to later
work after the manual workflow is stable.

## Documents

- `taxonomy.md` - skill areas, purpose, inputs, outputs, failure signals, and
  current support level.
- `maturity-model.md` - maturity ladder from named concept through possible
  runtime automation.
- `role-skill-map.md` - how Orchestrator, Lead, Worker, and supporting roles
  commonly invoke skill areas.

## Use

Use these docs when writing prompt language, runbooks, templates, contracts,
examples, helper scripts, or reviews that need a stable capability vocabulary.
Do not treat a named skill as implemented automation unless its maturity level
explicitly says so.
