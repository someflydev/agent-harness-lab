# Sequential Prompt Run Example

This scenario shows a normal fresh-session prompt execution using the loop in
`../../docs/runtime/execute-audit-preflight-bridge-reset.md` and
`../../runbooks/fresh-session-prompt-run.md`.

The fictional operator asks a fresh assistant session to run `PROMPT_04`, a
bounded documentation prompt. The session records a run manifest, completes the
requested docs, audits the result, checks `PROMPT_05` readiness, decides that
no handoff is needed, and resets cleanly.

## Artifacts

- `artifacts/run-manifest.md` - compact run facts, scope, permission posture,
  validation plan, and closeout status.
- `artifacts/completion-audit.md` - active-prompt deliverable audit.
- `artifacts/readiness-report.md` - immediate next-prompt preflight.
- `artifacts/handoff-not-created.md` - explicit no-handoff decision.

## What This Teaches

- A prompt run is bounded by one active prompt.
- Completion is checked against deliverables and constraints, not inferred from
  effort.
- Next-prompt preflight is adjacent; it does not implement future work.
- `tmp/HANDOFF.md` is omitted when repo files and final status are enough.
- Reset leaves the next session dependent on durable artifacts, not hidden chat
  context.
