# Contributing

Contributions should preserve the lab's current posture: human-assisted,
prompt-bounded, dependency-light, and inspectable in git.

## Working Rules

- Start with `AGENT.md`, `README.md`, `docs/guardrails.md`, and the active
  prompt or issue.
- Keep changes scoped to the requested prompt or contribution.
- Preserve unrelated local changes and untracked files.
- Prefer markdown, templates, small scripts, and tests before runtime
  expansion.
- Do not add provider integrations, daemons, sequential runners, graph/vector
  infrastructure, or CI workflows unless explicitly requested and validated.

## Validation

Run the checks that match the files you changed. For broad documentation or
release-readiness work, use:

```sh
python3 scripts/ahl.py promptset lint
python3 scripts/ahl.py docs check
python3 scripts/ahl.py registry check
python3 -m unittest tests/test_ahl.py
python3 scripts/ahl.py doctor
```

For command, dry-run, domain-pack, memory, or experiment changes, run the
corresponding helper command documented in `scripts/README.md`.

## Commit Style

Do not commit from an assistant session unless the operator explicitly asks.
When commits are requested, group them by coherent change and prefix the
subject with the active prompt id when applicable, for example:

```text
[PROMPT_31] Add release readiness docs
```
