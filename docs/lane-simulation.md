# Lane Simulation

Lane simulation is a deterministic way to practice hierarchical agent work
without building an agent runtime. It uses files to represent what separate
Orchestrator, Lead, Worker, Reviewer, and Auditor sessions would exchange if a
human operator ran them manually.

## Why It Exists

The project is intentionally human-assisted and subscription-friendly. A lane
simulation lets the repo test role boundaries, handoff contracts, review
points, stop conditions, and local validation before adding any expensive or
fragile automation.

The simulation is evidence for workflow shape. It is not evidence that live
multi-agent execution occurred.

## Manual Run

1. Pick a small fictional or documentation-only task.
2. Write an Orchestrator brief with intent, scope, non-goals, and escalation
   triggers.
3. Write a Lead plan that decomposes the work into bounded Worker assignments.
4. Write Worker task and result artifacts with explicit files in and out of
   scope.
5. Write a Reviewer report that records findings, severity, and disposition.
6. Write an Auditor closeout that checks the lane against the prompt or
   simulation requirements.
7. Update `lane-status.json` with the current state and artifact list.
8. Run the local lane checks.

```sh
python3 scripts/ahl.py lane check simulations/lane-demo
python3 scripts/ahl.py lane status simulations/lane-demo --json
```

## Role Mapping

- Orchestrator sets intent, scope, lane ownership, and escalation behavior.
- Lead owns one lane, breaks it into Worker-sized assignments, and defines
  review expectations.
- Worker executes one bounded assignment and returns a structured result.
- Reviewer checks the result for findings, risks, and missed stop conditions.
- Auditor verifies deliverables, validation evidence, and readiness for the
  next handoff.

## Automation Boundary

Lane simulation differs from actual parallel automation because it does not
spawn agents, invoke model providers, schedule concurrent processes, maintain
hidden state, or decide completion. The operator runs each role manually and
uses durable repo artifacts as the handoff surface.

The helper command only checks local structure: required files, parseable JSON,
referenced artifacts, and current state.

## Adding Future Lane Simulations

Future simulations should live under `simulations/<slug>/` and include a
README, role artifacts, a status JSON file, and clear validation commands. Keep
the scenario small and concrete. Prefer documentation, template validation, or
review exercises over real application implementation unless a prompt
explicitly asks for implementation.

Use `schemas/lane-status.schema.json` as the shape reference for status files.
When a simulation needs a new artifact type, document why it is needed before
adding script behavior.

