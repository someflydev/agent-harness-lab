# Documentation

This directory is the navigation surface for `agent-harness-lab` docs. The repo
is early, so these pages focus on foundation, orientation, assistant usage,
guardrails, safety, doctrine, role boundaries, skills, routines, runbooks,
runtime session behavior, memory governance, contracts, quality gates, metadata,
optional domain packs, examples, deterministic dry-run harness checks,
experiments, reports, findings, lab method, capstone audits, lane simulations,
release-readiness, operating baseline, phase-two outer-loop requirements,
capstone audit, smoke tests, gate reports, run-ledger recovery, maintenance,
contributing guidance, known limitations, commit planning, explicit commit
execution, Pi adapter comparison, the planned portable-operator extension, and
future-facing architecture. Role packs and lane playbooks now provide
pasteable manual hierarchy routines. The committed memory workspace supports
reviewed promotion candidates and decision records. Helper scripts exist, but
heavier orchestration remains outside the baseline.

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
- `release-readiness.md` - checks required before calling the repo usable.
- `known-limitations.md` - honest current runtime, validation, and architecture
  limits.
- `outer-loop/README.md` - phase-two requirements, safety boundary docs, and
  the dry-run-default sequential runner MVP.
- `outer-loop/operating-baseline.md` - safe local outer-loop preparation,
  driver probes, planning, dry-run, one-step live run, gate, recovery, and
  commit-plan workflow.
- `outer-loop/capstone-audit.md` - phase-two outer-loop implementation audit,
  validation evidence, gaps, and baseline decision.
- `portable-operator/README.md` - planned portable workflow extension for
  using AHL from arbitrary project repos with their own `.prompts/` directory.
- `portable-operator/extension-plan.md` - inventory of current AHL-root
  assumptions and prompt arc for later portable CLI and docs work.
- `portable-operator/invocation.md` - supported `project locate` invocation
  from AHL or another repo, including `AHL_HOME` and `--project` behavior.
- `portable-operator/status.md` - supported `project status` report for
  target-project git state, promptset diagnostics, bootstrap/context files,
  and likely next prompt inference.
- `portable-operator/lifecycle-snippets.md` - supported `lifecycle snippets`
  output for reusable one-prompt assistant instructions.
- `portable-operator/context-update-policy.md` - context-update doctrine and
  read-only candidate-check support for portable prompt closeout.
- `portable-operator/non-goals.md` - explicit exclusions for the portable
  extension, including provider daemons, credentials, Pi-specific material,
  and autonomous execution.
- `outer-loop/smoke-test-plan.md` - offline-safe and opt-in real-assistant
  smoke tests for outer-loop helpers.
- `outer-loop/known-limitations.md` - outer-loop execution, validation, data,
  git, and architecture limits.
- `outer-loop/future-work.md` - backlog candidates beyond the phase-two
  baseline.
- `outer-loop/resume-and-recovery.md` - run-ledger status, dry-run resume
  planning, and recovery handoff behavior.
- `outer-loop/failure-classification.md` - failure classes, repair needs, and
  automatic-action limits.
- `maintenance.md` - how to update prompts, registries, templates, skills,
  scripts, domain packs, and release checks.
- `contributing.md` - scoped contribution guidance and validation
  expectations.
- `safety/README.md` - safety, permission posture, destructive action, data
  hygiene, secret, transcript, reference repo, and approval guidance.
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
- `capstone/operating-baseline.md` - supported baseline workflows, passing
  commands, manual responsibilities, and unimplemented automation.
- `capstone/final-audit.md` - final audit evidence across the full initial
  promptset.
- `capstone/promptset-completion-report.md` - prompt range, artifacts, checks,
  handoff status, and recommended next human action.
- `capstone/future-backlog.md` - backlog categories for post-baseline work.
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

## Safety

- `safety/README.md` - safety docs index and local doctor-check entry point.
- `safety/permission-postures.md` - `read-only`, `workspace-write`, and
  `manual-required` posture guidance.
- `safety/destructive-actions.md` - approval and inspection rules before
  destructive operations.
- `safety/data-hygiene.md` - handling for `tmp/`, handoffs, reports, memory
  candidates, and transient runtime files.
- `safety/secrets-and-transcripts.md` - boundaries for secrets, credentials,
  raw transcripts, and sanitized durable summaries.
- `safety/reference-repo-boundaries.md` - reference repo influence and
  non-target boundaries.
- `safety/operator-approval.md` - actions that require explicit operator
  approval.

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

## Outer Loop

- `outer-loop/README.md` - index for phase-two outer-loop requirements.
- `outer-loop/requirements.md` - target sequential workflow, stop conditions,
  outputs, and commit policy.
- `outer-loop/safety-boundary.md` - dry-run, consent, provider, data, git, and
  failure boundaries.
- `outer-loop/sequential-runner-model.md` - local wrapper component model and
  implementation status.
- `outer-loop/assistant-driver-boundary.md` - driver vocabulary and supported
  subscription CLI versus API runtime boundary.
- `outer-loop/driver-contracts.md` - assistant driver record fields,
  conservative initial drivers, and live-run boundary.
- `outer-loop/pi-adapter.md` - Pi external-harness adapter design, safe probe
  boundary, expected payload/result shape, and unverified areas.
- `outer-loop/pi-vs-ahl.md` - why Pi remains an external coding-agent harness
  while AHL remains a promptset, validation, traceability, and orchestration
  lab.
- `outer-loop/provider-harness-comparison.md` - safety, auth, output capture,
  model-selection, and testing tradeoffs across driver categories.
- `outer-loop/capability-probes.md` - safe executable and help-only probe
  behavior for driver planning.
- `outer-loop/batch-planning.md` - deterministic prompt batch plan artifacts,
  explicit range handling, driver settings, and commit policy boundaries.
- `outer-loop/dry-run-runner.md` - plan dry-run validation, limits, and review
  guidance before any future live execution path.
- `outer-loop/gates.md` - post-prompt gate statuses, expected evidence, report
  format, and command boundary.
- `outer-loop/live-runner.md` - dry-run-default `outer run` behavior, live
  execution consent, driver mapping, and stop conditions.
- `outer-loop/prompt-payloads.md` - exact bounded fresh-session payload
  requirements for each planned prompt step.
- `outer-loop/run-artifacts.md` - run ledger, payload, step-summary,
  transcript, and commit-policy artifact boundaries.
- `outer-loop/completion-audit-integration.md` - how deterministic gate checks
  connect to human or assistant completion audit.
- `outer-loop/commit-planning.md` - prompt-scoped commit grouping rules,
  examples, and plan artifacts.
- `outer-loop/commit-execution.md` - explicit approval boundary and executor
  safety rules.
- `outer-loop/readiness-gate.md` - immediate next-prompt readiness inspection,
  blockers, and stop behavior.
- `outer-loop/non-goals.md` - explicit exclusions from the outer-loop design.
- `outer-loop/roadmap.md` - rest of phase-two sequence toward an outer-loop
  capstone.
- `outer-loop/capstone-audit.md` - phase-two implementation audit and local
  validation evidence.
- `outer-loop/operating-baseline.md` - supported outer-loop operating path.
- `outer-loop/smoke-test-plan.md` - smoke test matrix for CI-safe and opt-in
  real assistant checks.
- `outer-loop/known-limitations.md` - limits specific to the outer-loop
  helper.
- `outer-loop/future-work.md` - future backlog after the capstone baseline.

## Portable Operator

- `portable-operator/README.md` - index for the planned portable-operator
  extension.
- `portable-operator/extension-plan.md` - inventory and prompt arc for adding
  explicit AHL-home versus target-project behavior.
- `portable-operator/invocation.md` - current portable invocation and
  discovery behavior.
- `portable-operator/status.md` - read-only target-project status reporting
  before a one-prompt run.
- `portable-operator/lifecycle-snippets.md` - read-only reusable lifecycle
  snippet generation for a single target-project prompt.
- `portable-operator/context-update-policy.md` - when to update context files,
  when to record no update needed, and how to review candidates.
- `portable-operator/non-goals.md` - non-goals and safety boundaries for the
  portable extension.

## Capstone

- `capstone/final-audit.md` - full final audit for the completed initial
  baseline.
- `capstone/operating-baseline.md` - baseline operating model for operators and
  fresh assistant sessions.
- `capstone/future-backlog.md` - future work categories that are not baseline
  requirements.
- `capstone/promptset-completion-report.md` - completion report for Prompts 01
  through 32.
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
