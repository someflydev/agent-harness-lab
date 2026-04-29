# Simulations

Simulations are deterministic workspaces for manually exercising harness
patterns without invoking model providers, spawning agents, or running parallel
processes.

Each simulation should be small enough for an operator to inspect in one pass.
It should use durable files to represent role inputs and outputs, then validate
those files with local checks.

## Available Simulations

- `lane-demo/` - a compact Orchestrator -> Lead -> Worker -> Reviewer ->
  Auditor lane for validating a fictional template documentation refresh.

## Adding A Simulation

1. Create a directory under `simulations/` with a short slug.
2. Include a `README.md`, role artifacts, a status JSON file, and any local
   validation notes.
3. Keep the task fictional or illustrative unless a prompt explicitly asks for
   real implementation work.
4. Run `python3 scripts/ahl.py lane check <simulation-dir>` when the workspace
   follows the lane simulation shape.

