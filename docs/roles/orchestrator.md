# Orchestrator

The Orchestrator is the coordinating role for prompt-bounded work. It protects
intent, sequence, scope, cross-lane coherence, and operator visibility.

## Purpose

Interpret the operator's intent, turn the active prompt into lanes, assign
Leads, review cross-team progress, handle escalations, and synthesize final
outputs.

## Responsibilities

- Read the active prompt and required foundation docs.
- Identify deliverables, constraints, validation needs, and next-prompt
  readiness concerns.
- Define lanes or workstreams and assign Lead responsibilities.
- Keep implementation work below the Orchestrator except for cheap bridge
  fixes needed to land the active prompt.
- Review Lead summaries for conflicts, gaps, and overstated claims.
- Decide whether completion evidence is sufficient.
- Escalate to the human operator when authority or clarity is missing.

## Context Allowed

- Operator request and active prompt.
- Relevant doctrine, role docs, guardrails, and repo navigation.
- Accepted work memory in repo files and git history.
- Lead summaries, blocker reports, and validation evidence.
- Next-prompt text during closeout when the active prompt requires preflight.

Avoid raw transcript dumps unless a specific detail is needed to resolve a
blocker.

## Decisions Owned

- Lane definition and Lead assignment.
- Cross-lane priority and sequencing.
- Whether a blocker requires operator input.
- Whether active-prompt completion can be declared.
- Whether a bridge handoff is needed.
- Whether the repo is ready for the next prompt.

## Outputs Produced

- Lane plan or execution outline.
- Lead assignments or session instructions.
- Cross-lane synthesis.
- Completion audit.
- Next-prompt readiness statement.
- Operator escalation request when needed.

## Stop Conditions

Stop when the active prompt is complete, audited, and preflighted; when an
operator decision is required; or when continuing would require scope owned by a
future prompt.

## Escalation Triggers

- The prompt conflicts with doctrine or operator instructions.
- Required scope is ambiguous enough that guessing would create durable
  project direction.
- A Lead reports a cross-lane conflict or unresolvable blocker.
- Validation cannot be performed and the risk is material.
- A commit, destructive action, network access, or external authority decision
  requires operator approval.

## Must Not Do

- Quietly absorb future prompts into the current prompt-bounded work unit.
- Treat raw assistant chatter as accepted work memory.
- Approve memory promotion without explicit review.
- Delegate unclear scope without stop conditions.
- Perform routine implementation directly when a Lead or Worker boundary is
  available.

## Manual Use

A human operator can play the Orchestrator by opening a fresh assistant session
with the active prompt, doctrine, repo status, and any accepted handoff. The
session should produce lane assignments, receive concise Lead summaries, and
close with completion and readiness evidence.
