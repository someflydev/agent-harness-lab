# Runtime

Runtime docs describe how a prompt-bounded session is started, executed,
validated, closed, and reset. They are operator-facing and tool-agnostic: the
same routines should work with Codex, Claude Code, Gemini, Pi, or similar
assistants.

This section does not define a runtime engine. It names the manual operating
model that later templates, runbooks, helper scripts, and run manifests may
support.

## Start Here

- `session-lifecycle.md` - full phase model for a prompt-bounded session.
- `execute-audit-preflight-bridge-reset.md` - the core closeout routine.
- `prompt-authoring-vs-execution.md` - boundaries between prompt creation,
  prompt execution, and repair sessions.
- `adjacent-prompt-readiness.md` - how to inspect the immediate next prompt
  without drifting into future work.
- `bridge-and-reset.md` - when to bridge, when to avoid handoffs, and how to
  reset cleanly.
- `permission-posture.md` - lightweight permission labels for run manifests,
  prompts, and operator notes.

## Relationship To Other Docs

- Doctrine explains why fresh sessions, human orchestration, and durable
  artifacts matter.
- Roles name who owns orchestration, audit, validation, repair, and handoff
  responsibilities.
- Routines name repeatable session behaviors in compact catalog form.
- Runtime docs explain how those ideas are applied during a live session.
