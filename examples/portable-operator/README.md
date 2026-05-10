# Portable Operator Examples

These examples show the portable one-prompt workflow against the artificial
fixtures in `../../fixtures/portable-operator/`. They are dry-run oriented and
do not require a real private project, network access, credentials, provider
CLIs, or assistant quota.

## Examples

- `one-prompt-cycle.md` - status, lifecycle snippets, context-check,
  commit-plan boundary, explicit make-commits boundary, and post-commit
  commit-check for one prompt.
- `run-range-dry-run.md` - dry-run planning for a prompt range, including the
  fresh-session stop after each prompt and a gapped promptset diagnostic.

## Boundaries

The fixtures are fake target projects. In a real project, `human-notes.md` is
operator-owned: AHL may report that it exists, but examples should not ask an
assistant to edit or treat it as machine authority.
