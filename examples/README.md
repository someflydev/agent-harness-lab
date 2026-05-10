# Examples

These examples show how `agent-harness-lab` concepts look as inspectable
markdown artifacts. They are illustrative scenarios, not transcripts from real
assistant sessions and not a production runtime.

Use them with the operating docs in `../docs/`, the runbooks in `../runbooks/`,
and the reusable templates in `../templates/`.

## Scenario Index

- `sequential-prompt-run/` - a normal fresh-session prompt run from bounded
  execution through audit, next-prompt readiness, no-handoff decision, and
  reset.
- `org-lane-delegation/` - an Orchestrator -> Lead -> Worker lane with task,
  result, and review contracts.
- `memory-promotion/` - a temporary observation reviewed into durable memory
  only after evidence and rejection criteria are checked.
- `repair-bridge/` - a blocked prompt closeout where a transient
  `tmp/HANDOFF.md` bridge is justified.
- `portable-operator/` - offline portable workflow examples against fake
  external target-project fixtures.

## How To Read These

- Start with each scenario README for the narrative.
- Inspect the artifacts for the contract shape and evidence fields.
- Compare artifacts with `../templates/contracts/`,
  `../templates/reports/`, `../templates/runs/run-manifest.md`, and
  `../templates/handoffs/handoff.md`.
- Treat all dates, run ids, prompts, and tasks as small fictional examples.

## Boundaries

- The examples do not replace the runbooks.
- They do not imply that raw assistant chatter should be stored.
- They do not create provider-specific assumptions or background automation.
- They demonstrate the human-assisted, subscription-friendly workflow described
  in `../README.md` and `../docs/guardrails.md`.
