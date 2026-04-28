# Contract Types

## Task Contract

- Purpose: define a bounded assignment before work begins.
- When to use it: for lane-level work, Worker tasks, repair slices, or any
  task where scope and stop conditions need to be explicit.
- Owner: Orchestrator for lane contracts; Lead for Worker contracts.
- Required fields: artifact id, owner role, scope, authoritative inputs,
  expected outputs, in-scope paths, out-of-scope paths, validation plan,
  escalation triggers, completion condition.
- Optional fields: run id, dependencies, permission posture, assumptions,
  reviewer, deadline.
- Lifecycle: drafted, approved or accepted, executed, reported through a
  result contract, closed or superseded.
- Relationship to memory promotion: may identify promotion candidates but does
  not approve durable memory.

## Result Contract

- Purpose: summarize what a Worker or lane produced with evidence.
- When to use it: after completing a task contract or stopping at a defined
  boundary.
- Owner: Worker for task results; Lead for lane results.
- Required fields: artifact id, source task, owner role, scope completed,
  outputs, changed files, validation evidence, open issues, next step.
- Optional fields: skipped checks, assumptions confirmed or rejected,
  recommended review focus, promotion candidates.
- Lifecycle: produced, reviewed, accepted, repaired, or escalated.
- Relationship to memory promotion: can propose candidate facts with evidence;
  acceptance requires review and a promotion decision.

## Review Contract

- Purpose: record review findings, decisions, and required fixes.
- When to use it: when a Lead, Reviewer, or operator evaluates a result,
  report, or template before accepting it.
- Owner: Lead, Reviewer, Completion Auditor, or operator.
- Required fields: artifact id, reviewed artifact, reviewer role, scope,
  criteria, findings, disposition, evidence checked, required follow-up.
- Optional fields: severity, non-blocking notes, files sampled, reviewer
  confidence, promotion candidates.
- Lifecycle: opened, findings recorded, disposition set, fixes verified, closed
  or escalated.
- Relationship to memory promotion: review may accept or reject a proposed
  promotion, but durable updates still belong in the target artifact.

## Escalation Contract

- Purpose: ask the next authority level for a decision instead of guessing.
- When to use it: when scope, authority, validation, permissions, or durable
  direction exceeds the current role.
- Owner: the role escalating: Worker, Lead, Orchestrator, or supporting role.
- Required fields: artifact id, from role, to role, prompt or lane, decision
  needed, evidence, files or commands checked, risk of guessing, recommended
  next action.
- Optional fields: options, urgency, blocked outputs, related contracts,
  temporary handoff need.
- Lifecycle: raised, routed, decided, recorded in result or closeout, closed.
- Relationship to memory promotion: escalation can request review of a
  promotion candidate but cannot bypass promotion rules.

## Promotion Record

- Purpose: document a decision to accept, reject, or defer a memory promotion.
- When to use it: when a temporary fact may deserve durable repo memory and the
  decision needs an explicit record.
- Owner: operator by default; Orchestrator or Lead may propose and route.
- Required fields: candidate fact, source evidence, proposed target artifact,
  proposed memory plane, reviewer or approver, decision, decision date,
  rationale, outcome.
- Optional fields: cleanup needed, superseded notes, follow-up, validation
  performed.
- Lifecycle: proposed, reviewed, accepted/rejected/deferred, durable update made
  if accepted, temporary notes cleaned up.
- Relationship to memory promotion: this is the canonical memory promotion
  contract; use `templates/memory/promotion-record.md`.

## Run Manifest

- Purpose: capture compact facts about a prompt session or command run.
- When to use it: when a run needs traceable scope, posture, deliverables, and
  validation evidence.
- Owner: Prompt Runner, Session Conductor, or operator.
- Required fields: prompt id, run id, assistant/tool, permission posture,
  target scope, expected deliverables, validation plan, changed files,
  completion audit status, next-prompt readiness status, handoff created.
- Optional fields: skipped checks, blockers, related reports, promotion
  candidates.
- Lifecycle: opened at run start, updated during execution, closed after audit
  and readiness preflight.
- Relationship to memory promotion: records run facts; durable memory still
  requires promotion review.

## Completion Audit Report

- Purpose: verify that the active prompt's required deliverables and
  constraints were satisfied.
- When to use it: during prompt closeout or review of a completed execution
  session.
- Owner: Completion Auditor.
- Required fields: artifact id, prompt id, owner role, scope, deliverable
  checklist, validation evidence, unmet requirements, disposition, next step.
- Optional fields: files sampled, command output summary, risks, repair
  recommendations.
- Lifecycle: opened after execution, checked against prompt, passed/failed or
  marked partial, repaired or escalated if needed.
- Relationship to memory promotion: may identify accepted facts but should not
  promote them without the promotion model.

## Readiness Report

- Purpose: assess whether the immediate next prompt can start safely.
- When to use it: after the active prompt audit and before closeout.
- Owner: Next-Prompt Readiness Checker.
- Required fields: artifact id, active prompt, next prompt, owner role,
  prerequisites checked, readiness label, blockers or warnings, evidence, next
  step.
- Optional fields: cheap bridge fixes applied, files to inspect first,
  handoff recommendation.
- Lifecycle: opened during preflight, labeled ready/risky/blocked, bridge fix
  applied if appropriate, closed in session closeout.
- Relationship to memory promotion: readiness warnings are temporary unless a
  reviewed durable rule should be promoted.

## Handoff Record

- Purpose: preserve short-lived continuation context for a fresh session.
- When to use it: only when a real blocker or non-trivial warning remains and
  final-answer context is not enough.
- Owner: Handoff Composer or Session Conductor.
- Required fields: artifact id or title, active prompt, status, handoff reason,
  blocker or warning, affected files, validation already performed, next safe
  action, out-of-scope boundaries.
- Optional fields: expiration or deletion trigger, related report, operator
  decision needed.
- Lifecycle: created in `tmp/HANDOFF.md`, consumed by repair or next session,
  deleted or superseded when no longer useful.
- Relationship to memory promotion: temporary by default; durable claims need a
  promotion record and target artifact update.

## Session Closeout Record

- Purpose: summarize final state after execution, audit, preflight, bridge, and
  reset.
- When to use it: at the end of a prompt-execution session.
- Owner: Session Conductor or Prompt Runner.
- Required fields: prompt id, run id or date, owner role, scope, completed
  outputs, validation performed, changed files, completion status, readiness
  status, handoff created, open issues, next step.
- Optional fields: skipped checks, commit status, promotion candidates, repair
  recommendation.
- Lifecycle: drafted at closeout, final answer or record produced, handoff
  created only if justified, repo left ready for the next session.
- Relationship to memory promotion: can list promotion candidates; acceptance
  follows the promotion model.
