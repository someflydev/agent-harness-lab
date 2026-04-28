# Roles

Roles describe who is acting inside the `agent-harness-lab` operating model.
They set responsibility boundaries for human-assisted orchestration, fresh
assistant sessions, completion audits, next-prompt preflights, escalation, and
handoff decisions.

Roles are separate from skills. A role owns decisions, context limits, and
outputs. A skill is a reusable capability invoked by a role to perform a kind
of work.

## Core Hierarchy

The central hierarchy is:

1. `orchestrator` - interprets intent, plans lanes, assigns Leads, handles
   cross-lane review, and escalates to the operator when needed.
2. `lead` - owns one lane or workstream, decomposes bounded tasks, reviews
   Worker outputs, and summarizes upward.
3. `worker` - executes a narrow assignment with minimal necessary context and
   stops at clear boundaries.

This hierarchy can be enacted by one human operator using fresh assistant
sessions. The important property is not headcount; it is explicit role
separation.

## Role Documents

- `org-model.md` - organizational operating model and hierarchy rationale.
- `orchestrator.md` - Orchestrator responsibilities and boundaries.
- `lead.md` - Lead responsibilities and boundaries.
- `worker.md` - Worker responsibilities and boundaries.
- `supporting-roles.md` - supporting role families used by sessions and future
  automation.
- `boundary-matrix.md` - decision and authority matrix.
- `escalation-paths.md` - escalation paths and record expectations.

## How To Use These Docs

Use these files when defining contracts, templates, runbooks, examples, helper
scripts, or prompt language that needs a stable actor model. Keep references
domain-agnostic unless a later artifact is intentionally stack-specific.
