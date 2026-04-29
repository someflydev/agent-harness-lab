# Software Docs Routines

## Claim Check

- Trigger: A docs page describes a script, workflow, template, or validation
  behavior.
- Inputs: The changed docs, the referenced source files, and any command output
  claimed by the docs.
- Steps: Compare claims to source behavior, remove unsupported promises, and
  keep future-facing language clearly labeled.
- Outputs: Updated docs with accurate scope and any validation evidence.
- Stop conditions: The docs imply implemented behavior that does not exist, or
  the source behavior cannot be inspected.

## Navigation Check

- Trigger: A new docs area, pack, template, or repeated artifact family is
  added.
- Inputs: `docs/README.md`, nearby index pages, and the new files.
- Steps: Add only the navigation links needed for discoverability, then run the
  local docs checker when relevant.
- Outputs: Coherent navigation without turning the docs index into a changelog.
- Stop conditions: Navigation would advertise a capability as required when it
  is optional.

## Evidence Pairing

- Trigger: A prompt asks for validation evidence after docs or script changes.
- Inputs: Prompt validation section, changed files, and available local checks.
- Steps: Run required checks, record failures precisely, and keep prose aligned
  with the evidence.
- Outputs: Final notes that distinguish verified behavior from skipped checks.
- Stop conditions: A required check fails for a material reason.
