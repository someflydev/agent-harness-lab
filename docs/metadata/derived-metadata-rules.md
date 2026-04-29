# Derived Metadata Rules

Metadata must stay small, useful, and subordinate to durable artifacts.

## Rules

- Repo files and git history remain the source of truth.
- Generated metadata is derived helper data.
- Raw transcripts are not stored by default.
- Metadata must serve bounded execution, fresh-session bootstrap, prompt
  authoring quality, or cross-repo pattern reuse.
- Metadata should record facts that reviewers can verify from paths, commands,
  reports, handoffs, or commits.
- Metadata should not contain secrets, hidden runtime state, telemetry, or
  long-lived external identifiers unless a later prompt explicitly justifies
  them.
- Derived indexes must be disposable and rebuildable from durable artifacts.

## Acceptable Uses

- A run record that lists prompt id, changed files, validation, audit status,
  readiness status, handoff status, and associated commits.
- A readiness report that explains why the next prompt is ready, risky, or
  blocked.
- A promptset index that reflects prompt filenames and numbering.
- A reviewed pattern observation that points to concrete evidence.

## Unacceptable Uses

- A transcript archive treated as shared memory.
- A hidden database that becomes more authoritative than the repo.
- Telemetry about assistant behavior or operator activity.
- Speculative fields that no current review, bootstrap, or authoring workflow
  uses.
