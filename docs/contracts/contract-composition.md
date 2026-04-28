# Contract Composition

Contracts are useful when they make manual orchestration clearer. They should
fit the role hierarchy and closeout rhythm without becoming paperwork for its
own sake.

## Hierarchy

1. The Orchestrator creates or approves lane-level task contracts.
2. Leads decompose lane contracts into Worker task contracts.
3. Workers execute bounded work and produce result contracts.
4. Leads or Reviewers produce review contracts for Worker outputs.
5. Leads summarize accepted lane results upward.
6. Completion Auditors produce completion audit reports for the active prompt.
7. Readiness Checkers produce immediate next-prompt readiness reports.
8. Handoff Composers create handoff records only when a blocker or
   non-trivial warning justifies temporary context.

## Downward Flow

Downward contracts should narrow context:

- Orchestrator to Lead: lane purpose, authoritative inputs, deliverables,
  boundaries, validation expectations, escalation triggers.
- Lead to Worker: exact task, files in scope, inputs to trust, outputs to
  produce, stop conditions, result format.

Do not send raw transcripts downward. Send durable files, prompt excerpts,
contract fields, and explicit assumptions.

## Upward Flow

Upward contracts should sharpen evidence:

- Worker to Lead: changed files, outputs, validation evidence, blockers,
  assumptions, and recommended next step.
- Lead to Orchestrator: lane status, accepted results, review findings,
  integration risks, and escalation requests.
- Orchestrator to operator: completion status, readiness status, validation
  summary, residual risk, and whether a handoff exists.

## Reviews And Escalations

Review contracts check a result against the original task contract and local
criteria. Escalation contracts are used when the reviewer or executor cannot
make a decision within their authority.

Escalate instead of guessing when the issue changes prompt scope, durable
project direction, permissions, validation claims, or memory promotion.

## Closeout Composition

Closeout combines several contracts in order:

1. Run manifest records expected scope and validation plan.
2. Result and review contracts provide evidence for completed work.
3. Completion audit report checks active-prompt deliverables.
4. Readiness report checks the immediate next prompt.
5. Session closeout record summarizes final status.
6. Handoff record is created only when the closeout identifies a real reason.

For small manual runs, these may be sections in one final answer rather than
separate files. Use the templates when the state needs to be preserved or
reviewed outside the chat.

## Memory Promotion

Contracts can propose promotion candidates, but they do not make temporary
facts durable by themselves. Use `templates/memory/promotion-record.md` when a
promotion decision needs an explicit record, then update the narrowest useful
durable artifact if accepted.
