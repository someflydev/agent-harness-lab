# Portable Operator

The portable-operator extension is a planned local workflow layer for using
AHL from arbitrary project repositories that contain their own `.prompts/`
directory. It keeps the same human-governed loop as the AHL promptset:
one prompt, explicit context, validation, audit, next-prompt preflight, and a
fresh-session reset.

Most of this section is design guidance for later prompts, not a claim that the
full portable lifecycle exists. The implemented portable surface starts with
the read-only `project locate`, `project status`, `lifecycle snippets`,
`lifecycle context-check`, and `commit check` commands. Current outer-loop
helpers still primarily operate inside the AHL repository.

## Start Here

- `extension-plan.md` - inventory of existing AHL helper behavior, missing
  portable-project behavior, and the remaining prompt arc.
- `invocation.md` - current supported `project locate` invocation forms,
  `AHL_HOME` behavior, target-project detection, and failure reporting.
- `status.md` - read-only target-project status reporting for git state,
  promptset diagnostics, bootstrap/context files, prompt-prefixed commits, and
  likely next prompt inference.
- `lifecycle-snippets.md` - reusable prompt-run, audit, context-update,
  commit-plan, commit-check, and optional repair snippets for one prompt.
- `one-prompt-loop.md` - end-to-end portable one-prompt loop from planning
  blob and promptset creation through audit, commit packaging, commit check,
  and fresh-session reset.
- `context-update-policy.md` - doctrine for deciding when prompt closeout
  should update bootstrap or context files and when no edit is appropriate.
- `commit-check.md` - read-only recent-commit inspection for prompt-prefix,
  message-format, generated-boilerplate, and grouping hygiene.
- `human-notes-boundary.md` - explicit operator-owned boundary for
  `human-notes.md` scratch/control-zone content.
- `non-goals.md` - explicit exclusions for the portable-operator extension.

## Operating Posture

- AHL home is the checkout that contains `scripts/ahl.py`, AHL docs, templates,
  registries, schemas, fixtures, and tests.
- Target project root is the operator's current project repo. It may contain
  `.prompts/`, local assistant instructions, `.context/`, and
  `human-notes.md`.
- Portable commands should distinguish those roots in reports and file writes.
- The human operator remains scheduler, reviewer, validation authority, and
  commit authority.
- `human-notes.md` is operator-owned scratch content. AHL may report that it
  exists, but it must not edit it or treat it as authoritative state.
- The extension must stay local, inspectable, standard-library-first, and free
  of provider credentials, network calls, daemons, and hidden state.
