# Operator Approval

Operator approval is required when an action crosses the normal
`workspace-write` boundary or could remove, expose, publish, or externally
change state.

Ask before:

- destructive commands or cleanup
- git history rewrites
- commits, pushes, tags, releases, or deployments
- dependency installs or network fetches when approval is required
- writes outside the repo
- GUI/browser actions outside normal terminal validation
- handling secrets, credentials, private exports, or raw transcripts
- editing local reference repos

Approval should name the action and scope. A good approval request says what
command or path is involved, why it is needed, and what risk the operator is
accepting.

If approval is denied or unavailable, stop that action and leave a concise
handoff only when the next session needs blocker context that is not already in
repo files.
