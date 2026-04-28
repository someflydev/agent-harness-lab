# Documentation

This directory is the navigation surface for `agent-harness-lab` docs. The repo
is early, so these pages focus on foundation, orientation, guardrails, initial
doctrine, role boundaries, skills, routines, runtime session behavior, memory
governance, and contracts. Later prompts will add runbooks, examples, reports,
and scripts.

## Start Here

- `guardrails.md` - reusable project guardrails for assistants and operators.
- `operator-start.md` - how a human operator starts, runs, and closes a fresh
  prompt session.
- `repo-layout.md` - intended top-level repo areas, including what exists now
  and what is planned.
- `reference-influences.md` - compatible ideas adapted from local reference
  repos without treating them as parent projects.

## Doctrine

- `doctrine/README.md` - doctrine index and usage guidance.
- `doctrine/principles.md` - core principles for prompt-bounded harness work.
- `doctrine/glossary.md` - repo-specific vocabulary for later prompts.
- `doctrine/anti-patterns.md` - failure modes and corrective behaviors.
- `doctrine/artifact-boundaries.md` - boundaries between doctrine, runtime
  state, roles, skills, routines, contracts, templates, reports, examples, and
  handoffs.
- `doctrine/design-filters.md` - practical filters for adding docs, scripts,
  metadata, automation, and compatible reference ideas.

## Roles

- `roles/README.md` - role taxonomy index and usage guidance.
- `roles/org-model.md` - Orchestrator -> Leads -> Workers organization model.
- `roles/orchestrator.md` - Orchestrator purpose, authority, outputs, and
  boundaries.
- `roles/lead.md` - Lead purpose, lane ownership, outputs, and boundaries.
- `roles/worker.md` - Worker purpose, bounded execution, outputs, and
  boundaries.
- `roles/supporting-roles.md` - supporting role families for orchestration,
  cognitive work, repo intelligence, and process review.
- `roles/boundary-matrix.md` - authority boundaries across roles.
- `roles/escalation-paths.md` - escalation triggers and record shape.

## Skills

- `skills/README.md` - skill taxonomy index and usage guidance.
- `skills/taxonomy.md` - skill areas, purpose, inputs, outputs, failure
  signals, and current support level.
- `skills/maturity-model.md` - maturity ladder for skills from named concepts
  through possible runtime automation.
- `skills/role-skill-map.md` - mapping between roles and common skill areas.

## Routines

- `routines/README.md` - routine catalog index and usage guidance.
- `routines/catalog.md` - initial routine catalog for prompt execution,
  closeout, repair, promotion, validation, and packaging behaviors.
- `routines/routine-record-format.md` - simple markdown record shape for future
  runbooks and scripts.

## Contracts

- `contracts/README.md` - contract overview and template library index.
- `contracts/contract-types.md` - task, result, review, escalation, promotion,
  run, audit, readiness, handoff, and closeout contract reference.
- `contracts/contract-composition.md` - practical composition flow through the
  Orchestrator -> Leads -> Workers hierarchy and closeout loop.

## Runtime

- `runtime/README.md` - runtime/session lifecycle index and usage guidance.
- `runtime/session-lifecycle.md` - phase model for prompt-bounded sessions from
  context briefing through reset.
- `runtime/execute-audit-preflight-bridge-reset.md` - operational closeout
  rhythm for prompt-execution sessions.
- `runtime/prompt-authoring-vs-execution.md` - separation between prompt
  authoring, prompt execution, and repair sessions.
- `runtime/adjacent-prompt-readiness.md` - immediate next-prompt readiness
  checks without future-prompt implementation.
- `runtime/bridge-and-reset.md` - bounded bridge decisions, temporary handoffs,
  and clean reset behavior.
- `runtime/permission-posture.md` - stable permission labels for prompts, run
  manifests, and operator notes.

## Memory

- `memory/README.md` - memory model index and usage guidance.
- `memory/planes.md` - memory planes, ownership, lifespan, storage location,
  and promotion paths.
- `memory/promotion-model.md` - review and evidence requirements for promoting
  temporary observations into durable memory.
- `memory/handoff-lifecycle.md` - lifecycle for temporary bridge handoffs such
  as `tmp/HANDOFF.md`.
- `memory/run-memory.md` - compact run fact model without transcript dumping.
- `memory/retention-and-pruning.md` - retention rules and cleanup triggers for
  temporary and durable memory.
