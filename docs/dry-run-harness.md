# Dry-Run Harness

Dry runs are deterministic local checks for the harness operating model. They
prove that selected runbooks, examples, templates, fixtures, and helper script
expectations can be named and checked without paid model calls or provider
runtime integration.

## What Dry Runs Prove

- Scenario manifests parse as JSON.
- Required scenario fields are present.
- Referenced input artifacts exist.
- Referenced expected-output artifacts exist.
- `dry-runs/PARITY.md` rows have backing scenario JSON files.

## What They Do Not Prove

- They do not replay assistant sessions.
- They do not validate model reasoning quality.
- They do not call provider APIs or test provider permissions.
- They do not prove that runtime automation or workflow engines are ready.
- They do not replace prompt-specific completion audits.

## How They Support Change

Dry runs provide a small regression surface for routine and artifact changes.
When a runbook, template, example, or fixture is renamed or retired, scenario
checks can catch stale references before an operator discovers them during a
fresh prompt session.

The canonical coverage list is `../dry-runs/PARITY.md`. Update it whenever a
scenario is added, retired, or materially changes capability coverage.

## Difference From Real Execution

Real execution is a human-assisted assistant session that edits files, runs
validation, audits deliverables, and performs next-prompt preflight. A dry run
only checks the scenario manifest and artifact references that represent that
flow.

This boundary keeps dry runs cheap, deterministic, and subscription-friendly.

## Adding New Scenarios

Add a compact JSON manifest under `../dry-runs/scenarios/` with these fields:

- `id`
- `purpose`
- `input_artifacts`
- `routine_sequence`
- `expected_checks`
- `expected_outputs`
- `failure_modes_covered`

Then add or reference expected-output artifacts, update
`../dry-runs/PARITY.md`, and run:

```sh
python3 scripts/ahl.py dry-run check --all
```
