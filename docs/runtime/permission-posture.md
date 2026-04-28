# Permission Posture

Permission posture is a lightweight label for what a session or command is
allowed to do. It is useful in prompts, run manifests, operator notes, and
future helper scripts. This repo defines labels and boundaries, not a
permission runtime.

## `read-only`

Use `read-only` for inspection, review, planning, and audits that should not
modify files or external systems.

Allowed:

- read repo files
- inspect git status and diffs
- search files
- summarize findings
- propose changes without applying them

Denied:

- edit files
- create or delete files
- install dependencies
- start long-running services
- commit, push, or rewrite git history
- change external systems

## `workspace-write`

Use `workspace-write` for normal implementation inside the repo when the
operator has asked for edits.

Allowed:

- create or edit files inside the workspace
- run local validation commands
- create prompt-required directories
- update docs navigation and nearby integration points
- create temporary handoffs when justified

Denied:

- modify files outside the workspace
- edit local reference repos
- perform destructive cleanup without approval
- commit unless explicitly requested
- install dependencies or use network access when approval is required
- push, deploy, or change external systems

## `manual-required`

Use `manual-required` when the action is risky, destructive, outside the
workspace, external, or policy-sensitive enough that the operator must approve
or perform it.

Allowed after explicit approval or manual operator action:

- destructive file operations
- git history rewrites
- dependency installation or network fetches that require approval
- writes outside the repo
- deployment, publishing, pushing, or external service changes
- operations involving secrets or credentials

Denied without approval:

- any destructive operation
- any external state change
- any command that bypasses the operator's permission boundary

## How To Use Labels

Prompts and future run manifests should record the posture as one of the stable
labels: `read-only`, `workspace-write`, or `manual-required`. Prose can explain
why the posture was chosen, but tools should key off the label rather than
parsing a paragraph.
