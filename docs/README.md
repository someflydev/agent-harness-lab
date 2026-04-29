# Documentation

This directory is the navigation surface for `agent-harness-lab` docs. The repo
is early, so these pages focus on foundation, orientation, guardrails, doctrine,
role boundaries, skills, routines, runbooks, runtime session behavior, memory
governance, contracts, quality gates, metadata, examples, experiments,
reports, findings, lab method, capstone audits, and future-facing architecture.
Role packs and lane playbooks now provide pasteable manual hierarchy routines.
Helper scripts exist, but richer orchestration remains future work.

## Start Here

- `guardrails.md` - reusable project guardrails for assistants and operators.
- `operator-start.md` - how a human operator starts, runs, and closes a fresh
  prompt session.
- `repo-layout.md` - intended top-level repo areas, including what exists now
  and what is planned.
- `reference-influences.md` - compatible ideas adapted from local reference
  repos without treating them as parent projects.
- `scripts.md` - lightweight helper script behavior, examples, JSON fields,
  and automation boundaries.
- `operator-control-surfaces.md` - operator-visible control surfaces, current
  status, and automation boundaries.
- `commands-and-routines.md` - registry of helper commands, docs-only
  routines, runbooks, inputs, outputs, status, and safety notes.
- `navigation-map.md` - start points, durable artifact areas, registry
  relationships, and source-of-truth boundaries.
- `prompt-templates.md` - reusable prompt template library guidance and
  boundaries.
- `project-skills.md` - optional project-level skill packages, boundaries, and
  safe addition rules.
- `lab-method.md` - experimental method for bounded trials, evidence,
  findings, and promotion decisions.
- `quality/README.md` - validation gates, audit protocol, promptset quality,
  severity, completion states, and failure classes.
- `architecture/README.md` - future-facing architecture guidance and
  automation boundaries.
- `capstone/phase-one-audit.md` - foundation-phase audit of covered areas,
  gaps, and next improvements.
- `../role-packs/README.md` - pasteable role startup briefs for manual
  Orchestrator, Lead, Worker, Reviewer, Auditor, and Repair Agent sessions.
- `../lane-playbooks/README.md` - manual lane routines for documentation,
  docs-and-scripts, repair, and promotion work.

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
- `../role-packs/README.md` - pasteable startup packs that turn role doctrine
  into bounded fresh-session instructions.
- `../lane-playbooks/README.md` - lane-level operating playbooks using role
  packs, templates, and validation points.

## Skills

- `skills/README.md` - skill taxonomy index and usage guidance.
- `skills/taxonomy.md` - skill areas, purpose, inputs, outputs, failure
  signals, and current support level.
- `skills/maturity-model.md` - maturity ladder for skills from named concepts
  through possible runtime automation.
- `skills/role-skill-map.md` - mapping between roles and common skill areas.
- `project-skills.md` - optional `.agents/skills/` package guidance for
  assistant-loadable routine instructions.

## Routines

- `routines/README.md` - routine catalog index and usage guidance.
- `routines/catalog.md` - initial routine catalog for prompt execution,
  closeout, repair, promotion, validation, and packaging behaviors.
- `routines/micro-routine-library.md` - detailed reusable micro-routines for
  scope checks, audits, readiness checks, handoffs, promotion, closeout, and
  repair triage.
- `routines/routine-record-format.md` - simple markdown record shape for future
  runbooks and scripts.

## Runbooks

- `../runbooks/README.md` - operator-facing runbook index.
- `../runbooks/fresh-session-prompt-run.md` - normal fresh-session prompt
  execution flow.
- `../runbooks/completion-audit.md` - prompt requirement and evidence audit.
- `../runbooks/next-prompt-preflight.md` - immediate next-prompt readiness
  check.
- `../runbooks/bridge-fix-session.md` - cheap bridge fix and handoff decision
  procedure.
- `../runbooks/repair-session.md` - bounded repair-session startup and
  execution.
- `../runbooks/promotion-review.md` - durable memory promotion decision
  procedure.
- `../runbooks/run-closeout.md` - final reset and closeout procedure.
- `../runbooks/prompt-authoring.md` - prompt authoring workflow separate from
  prompt execution.
- `../runbooks/commit-packaging.md` - commit hygiene and prompt-id packaging.

## Scripts

- `scripts.md` - operator-facing guide for `scripts/ahl.py`.
- `../scripts/README.md` - script directory README with command examples and
  JSON output expectations.

## Architecture

- `architecture/README.md` - architecture index and current posture.
- `architecture/future-runtime-path.md` - gradual migration path from
  documented routines to possible richer orchestration.
- `architecture/automation-readiness-ladder.md` - criteria for graduating
  routines from prose to runtime components.
- `architecture/traceability-graph-and-semantic-retrieval.md` - future graph
  and semantic retrieval guidance as derived indexes.
- `architecture/non-goals.md` - foundation-phase non-goals and boundaries.

## Capstone

- `capstone/phase-one-audit.md` - audit across foundation-phase areas.
- `capstone/navigation-audit.md` - check that operators can find important
  docs without prompt history.
- `capstone/open-questions.md` - unresolved design questions for later review.

## Registries

- `../registry/README.md` - registry purpose, update rules, and validation
  commands.
- `../registry/artifacts.json` - curated index of durable artifact families.
- `../registry/prompts.json` - ordered index of every prompt file.
- `../registry/roles.json` - curated index of role documents.
- `../registry/routines.json` - curated index of routines and command-backed
  checks.
- `../registry/templates.json` - curated index of reusable template groups.
- `../registry/examples.json` - curated index of examples and evidence areas.
- `../registry/scripts.json` - curated index of helper scripts and commands.

## Prompt Templates

- `prompt-templates.md` - how reusable prompt templates differ from the
  implementation promptset and how operators should use them.
- `../prompt-templates/README.md` - index of copyable routine prompt
  templates.
- `../templates/lane/` - compact lane brief, lane status, and Worker
  assignment templates that complement contract templates.

## Metadata

- `metadata/README.md` - metadata purpose, document index, schema links, and
  acceptable uses.
- `metadata/run-record.md` - run record fields for prompt-bounded execution
  traceability.
- `metadata/prompt-to-commit-traceability.md` - use of prompt id commit
  prefixes for later git analysis.
- `metadata/derived-metadata-rules.md` - rules keeping metadata derived and
  subordinate to repo files and git history.
- `../schemas/run-record.schema.json` - JSON Schema for run records.
- `../schemas/readiness-report.schema.json` - JSON Schema for readiness
  reports.
- `../schemas/promptset-index.schema.json` - JSON Schema for
  `scripts/ahl.py promptset --json`.
- `../schemas/lane-record.schema.json` - JSON Schema for compact lane records.
- `../schemas/traceability-record.schema.json` - JSON Schema for compact
  prompt-to-commit traceability records.
- `../fixtures/README.md` - artificial JSON fixtures and lightweight fixture
  check limits.

## Contracts

- `contracts/README.md` - contract overview and template library index.
- `contracts/contract-types.md` - task, result, review, escalation, promotion,
  run, audit, readiness, handoff, and closeout contract reference.
- `contracts/contract-composition.md` - practical composition flow through the
  Orchestrator -> Leads -> Workers hierarchy and closeout loop.

## Quality

- `quality/README.md` - quality docs index and expected local checks.
- `quality/validation-gates.md` - checks and evidence by prompt type.
- `quality/promptset-quality.md` - execution-ready prompt criteria.
- `quality/audit-protocol.md` - implementation-to-prompt audit procedure.
- `quality/review-severity.md` - severity levels and finding disposition.
- `quality/definition-of-done.md` - `done`, `incomplete`, and `blocked`
  meanings.
- `quality/failure-classification.md` - common failure classes for audits.

## Examples

- `../examples/README.md` - illustrative scenario index for sequential prompt
  runs, org-lane delegation, memory promotion, and repair bridges.
- `../examples/sequential-prompt-run/README.md` - normal prompt execution with
  manifest, completion audit, readiness report, no-handoff decision, and clean
  reset.
- `../examples/org-lane-delegation/README.md` - compact Orchestrator -> Lead ->
  Worker contract flow.
- `../examples/memory-promotion/README.md` - reviewed promotion from temporary
  observation into durable memory.
- `../examples/repair-bridge/README.md` - justified transient handoff for an
  incomplete or blocked prompt.

## Lab Evidence

- `lab-method.md` - method for turning concrete workflow problems into bounded
  trials, reports, findings, and promotion candidates.
- `../experiments/README.md` - experiment purpose, boundaries, lifecycle, and
  promotion path.
- `../experiments/catalog.md` - compact catalog for planned, active, closed,
  abandoned, or superseded experiments.
- `../experiments/templates/` - experiment plan, log, and closeout templates.
- `../reports/README.md` - report types and evidence boundaries.
- `../reports/templates/` - session, promptset audit, and routine evaluation
  report templates.
- `../findings/README.md` - finding definition, evidence requirements, and
  relationship to memory promotion.
- `../findings/templates/` - finding record and pattern observation templates.

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
