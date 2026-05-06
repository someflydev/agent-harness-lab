# Prompt Payloads

The live runner sends a bounded payload to each fresh assistant session. The
template is `templates/outer-loop/prompt-payload.md`; generated payloads are
written under the run artifact directory before any live invocation.

## Required Payload Content

Each payload names exactly one prompt id and prompt path. It tells the assistant
to read:

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- the active prompt file
- docs explicitly named by the active prompt

The payload does not paste repository contents. It tells the assistant which
local files to inspect.

## Guardrails

Payloads require the assistant to preserve unrelated changes, avoid commits
unless the outer runner or authorized operator asks, avoid raw transcript
dumps, run relevant validation, audit deliverables, inspect next-prompt
readiness, and create `tmp/HANDOFF.md` only when a real blocker or meaningful
warning remains.
