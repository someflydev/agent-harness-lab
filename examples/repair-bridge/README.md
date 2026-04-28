# Repair Bridge Example

This scenario shows when a transient bridge handoff is justified, following
`../../docs/runtime/bridge-and-reset.md`,
`../../docs/memory/handoff-lifecycle.md`, and
`../../runbooks/repair-session.md`.

The fictional prompt attempted to add a validation report, but the session
ended after creating only part of the required artifact set. The next session
needs exact state: what was completed, what failed validation, and the next
safe repair action. In that case, a temporary `tmp/HANDOFF.md` would be useful.

This example uses `artifacts/tmp-HANDOFF.example.md` instead of creating a real
`tmp/HANDOFF.md`.

## Artifacts

- `artifacts/tmp-HANDOFF.example.md` - an illustrative transient handoff for a
  blocked or incomplete prompt.

## What This Teaches

- A handoff is justified by a real blocker or non-trivial warning.
- The bridge carries continuation context, not doctrine or raw transcript.
- The repair session starts with a bounded next safe action.
- The handoff should be deleted or superseded after repair.
