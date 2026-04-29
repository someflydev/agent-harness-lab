# Validation Gates

Validation gates describe the minimum proof expected before closeout. A prompt
may require additional checks; the prompt wins.

## Docs-Only Prompts

Expected checks:

- Required files exist.
- New docs are linked from the nearest index.
- Claims match current repo behavior.
- Constraints are checked against the diff.

Evidence:

- File inventory or read-back of changed sections.
- Relevant index path.
- Any command output used to confirm structure.

## Template Prompts

Expected checks:

- Required template paths exist.
- Placeholders are clear and reusable.
- Template fields match related contracts or runbooks.
- Generated examples, if any, do not overwrite local state.

Evidence:

- Template path list.
- Read-back of required fields.
- Script or manual scaffold check when a helper uses the template.

## Script Prompts

Expected checks:

- Behavior is documented.
- Standard-library-only constraints are preserved unless explicitly changed.
- JSON output remains compact and stable.
- Unit tests cover new CLI behavior.

Evidence:

- `python3 -m unittest tests/test_ahl.py`.
- Example command output such as `doctor`, `promptset`, or `validate`.
- Notes for checks that could not run.

## Example Prompts

Expected checks:

- Examples are discoverable from the relevant index.
- Examples are illustrative, not hidden runtime state.
- Referenced templates, runbooks, and docs exist.
- Example claims stay within implemented behavior.

Evidence:

- Example path inventory.
- Links from `examples/README.md` or the nearest index.
- Manual read-back of scenario steps and referenced artifacts.

## Metadata/Schema Prompts

Expected checks:

- Metadata files or schemas exist at required paths.
- Field names and required fields are documented.
- Fixtures or examples match the schema.
- Validation does not require paid model calls.

Evidence:

- Schema and fixture path list.
- Local parser or script output when available.
- Manual comparison when no validator exists.

## Capstone Audit Prompts

Expected checks:

- Prompt requirements are audited against actual repo state.
- Prior deliverables are sampled or inventoried with explicit criteria.
- Known gaps are classified instead of hidden.
- Next-prompt or release readiness is stated with reasons.

Evidence:

- Completion audit report or closeout summary.
- Commands run and their results.
- Finding list with severity and disposition.
