# Portable Operator

The portable-operator extension is a planned local workflow layer for using
AHL from arbitrary project repositories that contain their own `.prompts/`
directory. It keeps the same human-governed loop as the AHL promptset:
one prompt, explicit context, validation, audit, next-prompt preflight, and a
fresh-session reset.

Most of this section is design guidance for later prompts, not a claim that the
full portable lifecycle exists. The implemented portable surface starts with
the read-only `project locate` discovery command. Current outer-loop helpers
still primarily operate inside the AHL repository.

## Start Here

- `extension-plan.md` - inventory of existing AHL helper behavior, missing
  portable-project behavior, and the remaining prompt arc.
- `invocation.md` - current supported `project locate` invocation forms,
  `AHL_HOME` behavior, target-project detection, and failure reporting.
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
- The extension must stay local, inspectable, standard-library-first, and free
  of provider credentials, network calls, daemons, and hidden state.
