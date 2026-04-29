# Prompt-To-Commit Traceability

Prompt ids are stable handles for bounded work. Commit subjects should keep the
active prompt id prefix when the operator asks for commits, for example:

```text
[PROMPT_13] Add operator metadata surfaces
```

## Why Prefixes Matter

The prefix lets later reviewers answer practical questions with normal git
commands:

- Which commits came from a specific prompt?
- Which files changed during a prompt-bounded slice?
- Which prompts tended to require follow-up fixes?
- Which validation evidence should be checked before accepting a commit group?

## Collection Flow

1. During execution, record `prompt_id`, changed files, validation commands,
   audit status, and readiness status in a run record or closeout summary.
2. During commit packaging, inspect `git status --short` and `git diff`.
3. Stage only task-related files.
4. Use a commit subject prefixed with the active prompt id.
5. Add resulting commit hashes to `associated_commit_hashes` when a structured
   run record is maintained.

## Analysis Boundary

Git history and repo files remain authoritative. Derived traceability indexes
may summarize prompt ids, changed files, and commit hashes, but they should be
rebuildable from git plus durable repo artifacts.
