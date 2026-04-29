# Dry Runs

Dry runs are deterministic local scenarios for checking whether
`agent-harness-lab` routines, examples, templates, and helper scripts remain
structurally coherent without live assistant or provider calls.

They are intentionally small. A dry-run scenario is a JSON manifest that names
input artifacts, a routine sequence, expected checks, expected output files, and
failure modes covered. The checker verifies that the manifest is shaped
correctly and that referenced files exist. It does not replay an assistant
session or judge prose quality beyond the explicit structural expectations.

## Contents

- `PARITY.md` - canonical scenario coverage tracker.
- `scenarios/` - deterministic scenario manifests.
- `expected/` - compact expected-output summaries used by scenarios.

## Commands

```sh
python3 scripts/ahl.py dry-run list
python3 scripts/ahl.py dry-run check sequential-prompt-run
python3 scripts/ahl.py dry-run check --all --json
```

Use these checks before changing runbooks, templates, examples, or helper
script behavior that dry-run scenarios reference.

## Adding A Scenario

1. Add a small JSON file under `dry-runs/scenarios/`.
2. Include `id`, `purpose`, `input_artifacts`, `routine_sequence`,
   `expected_checks`, `expected_outputs`, and `failure_modes_covered`.
3. Add or reference expected-output artifacts that already exist in the repo.
4. Update `dry-runs/PARITY.md` with the covered capability and evidence path.
5. Run `python3 scripts/ahl.py dry-run check --all`.
