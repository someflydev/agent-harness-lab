# Promotion Review

## Purpose

Decide whether transient knowledge from a session, note, report, or repeated
observation should become accepted durable memory in repo artifacts.

## When To Use It

Use when a fact, lesson, or operating rule may deserve promotion from temporary
context into docs, runbooks, templates, or memory records. Use
`templates/memory/promotion-record.md` when a promotion decision needs a record.

## Required Context To Load

- Candidate fact or observation.
- Source evidence, such as files, validation output, review notes, or handoff.
- Target artifact boundary from `docs/doctrine/artifact-boundaries.md`.
- Memory guidance in `docs/memory/promotion-model.md`.
- Relevant existing durable docs to avoid duplicates.

## Roles Involved

- Operator: approves promotion when judgment or policy is involved.
- Orchestrator: checks artifact boundary and scope.
- Lead: proposes target durable location.
- Completion Auditor or Validator: supplies evidence when needed.

## Step-By-Step Procedure

1. State the candidate fact in one sentence.
2. Identify the source evidence and whether it is verified.
3. Decide the target artifact type: doctrine, runbook, template, report,
   memory record, or no durable artifact.
4. Check whether the candidate duplicates existing docs.
5. Classify the decision:
   - `promote`: evidence is strong, target boundary is clear, and the update
     helps future sessions.
   - `defer`: the idea may be useful but needs more evidence or repetition.
   - `reject`: the fact is unverified, too session-specific, or outside repo
     scope.
6. If promoting, update the smallest appropriate durable artifact or write the
   promotion record requested by the operator.
7. Link or cite the promoted artifact from the nearest index when needed.
8. Report the decision and evidence in closeout.

## Expected Artifacts

- Promotion, defer, or reject decision.
- Optional `templates/memory/promotion-record.md` record.
- Updated durable doc only when promotion is approved and in scope.

## Validation Or Evidence

- Source evidence is named and inspectable.
- The target artifact boundary is explicit.
- Existing docs were checked for duplication or conflict.
- Promoted content avoids raw transcript and unverified claims.

## Stop Conditions

- Evidence is weak or unavailable.
- The target artifact boundary is unclear.
- Promotion requires operator approval that has not been given.
- The candidate is a broad design change disguised as memory.

## Common Failure Modes

- Promoting raw assistant chatter.
- Treating a one-off note as durable doctrine.
- Writing memory into the wrong artifact type.
- Creating duplicate guidance instead of updating the existing source of truth.
