# Lane Demo

This lane demo shows hierarchical work as a manual file-based simulation. The
fictional task is to validate whether a small template documentation area is
ready for an operator-facing refresh.

No assistant sessions were spawned by this demo. The role files represent what
separate Orchestrator, Lead, Worker, Reviewer, and Auditor sessions would pass
through durable artifacts if an operator ran them one at a time.

## Flow

1. `orchestrator-brief.md` defines the intent, scope, and escalation rule.
2. `lead-plan.md` decomposes the lane into one bounded Worker task.
3. `worker-01-task.md` names the Worker assignment and stop conditions.
4. `worker-01-result.md` records a structured result.
5. `reviewer-report.md` checks the Worker result for findings.
6. `auditor-closeout.md` audits the lane against the simulation requirements.
7. `lane-status.json` records the current state and linked artifacts.

## Local Check

```sh
python3 scripts/ahl.py lane check simulations/lane-demo
python3 scripts/ahl.py lane status simulations/lane-demo --json
```

