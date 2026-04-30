# Permission Postures

Permission posture names what a session or command is allowed to do. The stable
labels are `read-only`, `workspace-write`, and `manual-required`.

## `read-only`

Use `read-only` for review, planning, audits, promptset inspection, and
preflight checks.

Allowed:

- read repo files
- inspect git status and diffs
- search and summarize files
- report findings or proposed changes

Not allowed:

- edit, create, or delete files
- install dependencies
- start services
- commit, push, deploy, or change external systems

## `workspace-write`

Use `workspace-write` for normal prompt implementation after the operator asks
for edits.

Allowed:

- edit files inside this repo
- add prompt-required docs, tests, templates, or small scripts
- run local validation
- create `tmp/HANDOFF.md` only when a real blocker or warning needs it

Not allowed without separate approval:

- edit outside the workspace
- edit local reference repos
- run destructive cleanup
- install dependencies or fetch from the network when approval is required
- commit, push, publish, deploy, or change external systems

## `manual-required`

Use `manual-required` for risky, destructive, external, or credential-related
operations. The operator must explicitly approve or perform the action.

Examples:

- deleting files or directories
- rewriting git history
- writing outside the repo
- pushing, publishing, deploying, or changing external services
- handling secrets, credentials, or private transcript exports
