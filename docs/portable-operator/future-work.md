# Portable Operator Future Work

These items are candidates beyond the Prompt 42-53 portable baseline. They are
not required for current baseline use.

## Candidate Improvements

- Add an optional checked-in wrapper or installation recipe after the direct
  `python3 /path/to/agent-harness-lab/scripts/ahl.py ...` invocation proves
  too cumbersome in real projects.
- Add richer fixture scenarios for duplicate prompt ids, malformed prompt
  names, dirty git states, nested target projects, and multiple bootstrap
  conventions.
- Add optional report artifact output for `project status`, `lifecycle
  context-check`, and `commit check` when operators want durable review files.
- Add more precise context-update heuristics while keeping output advisory and
  read-only.
- Add shell completion or concise help examples for the portable namespace.
- Add a reviewed bridge between portable range plans and existing outer-loop
  planning only if the safety boundary remains explicit and one prompt at a
  time.

## Deferred Or Out Of Scope

- Provider API automation, browser subscription automation, credential
  storage, quota queries, and network-dependent helpers.
- Automatic multi-prompt scheduling or unattended continuation.
- Automatic edits to `human-notes.md` or treating private notes as machine
  state.
- Automatic commit creation, history rewriting, pushing, tagging, or
  publishing from portable helpers.
- Pi-specific portable extension material.
