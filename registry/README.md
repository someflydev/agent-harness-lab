# Registry

This directory contains curated navigation indexes for durable repo artifacts.
The JSON files are intentionally small, stable, and human-inspectable.

Registries are not a second source of truth. Checked-in markdown, templates,
scripts, schemas, examples, prompts, and git history remain authoritative. A
registry entry points a fresh session toward the relevant source file and adds
just enough metadata to support lightweight validation.

## Files

- `artifacts.json` - top-level artifact families and source-of-truth areas.
- `prompts.json` - every `.prompts/PROMPT_XX.txt` file in prompt order.
- `roles.json` - durable role documents and their boundaries.
- `routines.json` - command-backed and docs-only routines.
- `templates.json` - reusable templates and template groups.
- `examples.json` - example scenarios and evidence artifacts.
- `scripts.json` - helper script commands and script documentation.
- `assistant-drivers.json` - conservative local assistant driver contracts for
  phase-two outer-loop planning.

Release-readiness and maintenance guidance for these indexes lives in
`../docs/release-readiness.md` and `../docs/maintenance.md`.

## Update Rules

Update these registries when a prompt explicitly names a registry file in its
required deliverables or when the prompt introduces a durable artifact that
clearly belongs in one of the curated indexes.

Do not require every new repo file to appear here. These files are maps, not
mirrors.

## Validation

Use:

```sh
python3 scripts/ahl.py registry check
python3 scripts/ahl.py registry list --json
```

The check validates JSON parsing, required item fields, local path references,
and `prompts.json` ordering against the actual `.prompts/PROMPT_*.txt` files.
Driver-specific checks live in `python3 scripts/ahl.py driver check`.
