# Portable Operator Non-Goals

The portable-operator extension should not turn AHL into an autonomous platform
or provider integration layer.

## Exclusions

- No provider daemon, background scheduler, API credential store, browser-cookie
  bridge, or network dependency.
- No automatic editing of `human-notes.md`; that file is operator-owned and
  informational.
- No Pi-specific context blob or Pi-specific extension track.
- No assumption that Claude can be automated through subscription APIs outside
  Claude Code or manual operator use.
- No raw transcript capture by default and no promotion of raw chat into
  durable state.
- No destructive git operations, staging, commits, pushes, tags, releases, or
  publishes without explicit operator authority.
- No parallel prompt execution in the portable baseline.
- No semantic completion oracle. Completion audit remains a human or
  assistant-reviewed judgment backed by local evidence.
- No duplicate command families that rename existing outer-loop capabilities
  without a real target-project distinction.

## Boundary

The extension may add local discovery, status reports, generated snippets,
dry-run plans, commit-message inspection, smoke fixtures, and documentation.
Those artifacts must remain inspectable files or structured command output.
They do not replace fresh-session prompt execution, local validation, operator
review, or git history.
