# Documentation

This directory is the navigation surface for `agent-harness-lab` docs. The repo
is early, so these pages focus on foundation, orientation, assistant usage,
guardrails, doctrine, role boundaries, skills, routines, runbooks, runtime
session behavior, memory governance, contracts, quality gates, metadata,
optional domain packs, examples, deterministic dry-run harness checks,
experiments, reports, findings, lab method, capstone audits, lane simulations,
and future-facing architecture. Role packs and lane playbooks now provide
pasteable manual hierarchy routines. The committed memory workspace supports
reviewed promotion candidates and decision records. Helper scripts exist, but
richer orchestration remains future work.

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
- `traceability.md` - prompt-to-change trace command behavior, closeout use,
  and derived-metadata boundaries.
- `operator-console.md` - Makefile console purpose, targets, safety, recipes,
  and runtime boundaries.
- `operator-control-surfaces.md` - operator-visible control surfaces, current
  status, and automation boundaries.
- `commands-and-routines.md` - registry of helper commands, docs-only
  routines, runbooks, inputs, outputs, status, and safety notes.
- `navigation-map.md` - start points, durable artifact areas, registry
  relationships, and source-of-truth boundaries.
- `navigation-validation.md` - local markdown link checking, docs index
  coverage, checker limits, and registry relationship.
- `assistants/README.md` - practical usage guides for Codex, Claude Code,
  Gemini, Pi, generic chat, subscription workflows, and context loading.
- `prompt-templates.md` - reusable prompt template library guidance and
  boundaries.
- `promptset-linting.md` - promptset lint checks, readiness scoring, limits,
  and prompt-authoring use.
- `project-skills.md` - optional project-level skill packages, boundaries, and
  safe addition rules.
- `domain-packs.md` - optional domain pack purpose, use pattern, current
  starters, and boundaries.
- `dry-run-harness.md` - deterministic dry-run scenario purpose, limits,
  parity tracking, and addition workflow.
- `lane-simulation.md` - manual lane simulation purpose, role mapping,
  validation commands, and automation boundary.
- `lab-method.md` - experimental method for bounded trials, evidence,
  findings, and promotion decisions.
- `experiment-workflow.md` - helper-command workflow for starting, logging,
  closing, checking, and promoting experiment evidence.
- `memory/promotion-workflow.md` - reviewed memory candidate, evidence,
  decision, accepted-memory, and pruning workflow.
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
- `../memory/README.md` - curated memory workspace for promotion queue and
  decision records.
- `../domain-packs/README.md` - optional domain pack starter kit and examples.

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

## Assistants

- `assistants/README.md` - assistant usage guide index and common operating
  model.
- `assistants/codex.md` - Codex-style prompt execution sessions.
- `assistants/claude-code.md` - Claude Code-style terminal assistant sessions.
- `assistants/gemini.md` - Gemini-style coding assistant sessions.
- `assistants/pi.md` - Pi-style project-context assistant sessions.
- `assistants/generic-chat.md` - manual copy/paste assistant workflow.
- `assistants/subscription-workflow.md` - subscription-friendly workflow,
  quota control, rate-limit recovery, and runtime-mode boundaries.
- `assistants/context-loading.md` - context-loading matrix by session type.

## Domain Packs

- `domain-packs.md` - optional domain pack use pattern and boundaries.
- `../domain-packs/README.md` - domain pack index and validation guidance.
- `../domain-packs/_template/README.md` - reusable pack starter structure.
- `../domain-packs/software-docs/README.md` - modest example pack for
  documentation-heavy software-building work.

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
- `operator-console.md` - Makefile console wrapper around common helper
  commands.
- `promptset-linting.md` - details for `scripts/ahl.py promptset lint`.
- `navigation-validation.md` - details for `scripts/ahl.py docs check`.
- `dry-run-harness.md` - details for `scripts/ahl.py dry-run list` and
  `scripts/ahl.py dry-run check`.
- `lane-simulation.md` - details for `scripts/ahl.py lane check` and
  `scripts/ahl.py lane status`.
- `../scripts/README.md` - script directory README with command examples and
  JSON output expectations.
- `traceability.md` - closeout trace command guidance for prompt-related
  working tree summaries.
- `memory/promotion-workflow.md` - workflow details for
  `scripts/ahl.py memory propose`, `scripts/ahl.py memory check`, and
  `scripts/ahl.py memory decision`.
- `domain-packs.md` - workflow details for
  `scripts/ahl.py domain-pack check`.

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
- `../templates/memory/promotion-candidate.md` - queued memory promotion
  candidate template.
- `../templates/memory/promotion-decision.md` - accepted or rejected memory
  promotion decision template.

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
- `../schemas/lane-status.schema.json` - JSON Schema for manual lane
  simulation status files.
- `../schemas/traceability-record.schema.json` - JSON Schema for compact
  prompt-to-commit traceability records.
- `../schemas/domain-pack.schema.json` - JSON Schema for optional domain pack
  manifests.
- `../fixtures/README.md` - artificial JSON fixtures and lightweight fixture
  check limits.
- `../fixtures/traceability/working-tree-summary.json` - artificial
  `scripts/ahl.py trace --json` style working tree summary.

## Dry Runs

- `dry-run-harness.md` - dry-run scenario behavior, limits, and addition
  workflow.
- `../dry-runs/README.md` - dry-run directory index and command examples.
- `../dry-runs/PARITY.md` - canonical scenario-coverage tracker.
- `../dry-runs/scenarios/` - deterministic scenario manifests.
- `../dry-runs/expected/` - compact expected-output summaries.

## Simulations

- `lane-simulation.md` - lane simulation guidance and local command behavior.
- `../simulations/README.md` - simulation workspace index.
- `../simulations/lane-demo/README.md` - concrete manual lane demo using
  Orchestrator, Lead, Worker, Reviewer, and Auditor artifacts.

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
- `promptset-linting.md` - linter behavior and readiness score interpretation.
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
- `experiment-workflow.md` - operational workflow for experiment scaffolding,
  observation logging, closeout, finding creation, and prompt-authoring input.
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
- `memory/promotion-workflow.md` - command-backed workflow for proposing,
  reviewing, accepting, rejecting, and pruning memory candidates.
- `memory/handoff-lifecycle.md` - lifecycle for temporary bridge handoffs such
  as `tmp/HANDOFF.md`.
- `memory/run-memory.md` - compact run fact model without transcript dumping.
- `memory/retention-and-pruning.md` - retention rules and cleanup triggers for
  temporary and durable memory.
- `../memory/README.md` - curated committed memory workspace boundary.
- `../memory/promotion-queue/README.md` - queued candidate boundary and check
  expectations.
- `../memory/accepted/README.md` - accepted decision record boundary.
- `../memory/rejected/README.md` - rejected decision record boundary.
