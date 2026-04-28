# Contracts

Contracts define the expected shape of prompt-bounded work artifacts:
assignments, results, reviews, escalations, reports, handoffs, manifests, and
closeout records. They keep manual orchestration inspectable without requiring
a runtime engine.

Use contracts when a fresh session needs a clear agreement about scope,
inputs, outputs, owner, evidence, and stop conditions. Use templates when the
operator or assistant needs a reusable starting shape for a specific artifact.

## Start Here

- `contract-types.md` - contract type reference, owners, required fields, and
  relationship to memory promotion.
- `contract-composition.md` - how contracts move through the Orchestrator ->
  Leads -> Workers hierarchy and closeout loop.

## Template Library

- `../../templates/contracts/task-contract.md` - assignment contract for a
  lane, Lead, or Worker task.
- `../../templates/contracts/result-contract.md` - Worker or lane result
  summary.
- `../../templates/contracts/review-contract.md` - review findings and
  disposition.
- `../../templates/contracts/escalation-contract.md` - decision request when a
  role reaches its authority boundary.
- `../../templates/memory/promotion-record.md` - canonical promotion decision
  record.
- `../../templates/runs/run-manifest.md` - compact run facts and validation
  plan.
- `../../templates/reports/completion-audit.md` - active-prompt completion
  audit.
- `../../templates/reports/readiness-report.md` - immediate next-prompt
  readiness report.
- `../../templates/handoffs/handoff.md` - optional `tmp/HANDOFF.md` shape.
- `../../templates/handoffs/repair-checklist.md` - repair-session checklist
  for resolving a blocker or warning.
- `../../templates/session-closeout.md` - final closeout record for a prompt
  session.

## Operating Rules

- Keep contracts compact and evidence-based.
- Do not treat raw assistant chatter as a contract or durable memory.
- Create handoffs only when a real blocker or non-trivial warning remains.
- Promote memory only through the canonical promotion record or a reviewed
  durable artifact update.
- Prefer manual markdown fields until a later prompt proves script support is
  needed.
