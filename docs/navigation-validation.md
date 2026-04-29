# Navigation Validation

Documentation navigation is part of fresh-session bootstrap. A new assistant
session should be able to start from `AGENT.md`, `README.md`, `docs/README.md`,
and the active prompt without chasing stale paths or guessing where an artifact
lives.

Use the lightweight docs checker before closeout when a prompt changes docs,
runbooks, templates, registries, fixtures, or examples:

```sh
python3 scripts/ahl.py docs check
python3 scripts/ahl.py docs check --json
```

## What It Covers

The checker scans markdown files in the main documentation surfaces:

- root bootstrap docs
- `docs/`
- `runbooks/`
- `templates/`
- `scripts/`
- `registry/`
- `examples/`
- `experiments/`
- `findings/`
- `reports/`
- `role-packs/`
- `lane-playbooks/`
- `prompt-templates/`

It reports local markdown links whose target files or directories are missing.
It also checks that `docs/README.md` exists and that it links the major
top-level documentation areas from a visible index. When registry JSON files
exist, the docs check reuses registry validation to catch stale registry paths.

## What It Does Not Cover

The checker intentionally stays dependency-free and conservative:

- It does not fetch external `http` or `https` links.
- It does not validate anchor fragments after `#`.
- It does not enforce prose style, naming style, or docs taxonomy rules.
- It does not scan local reference repos.
- It does not treat deliberately broken test fixtures as repo navigation
  failures.

Anchor validation is omitted because headings can be rendered differently by
different markdown hosts. If an anchor matters for operator flow, prefer a
nearby file-level link plus clear heading text.

## Fixing Failures

For a missing local link, inspect the source file and choose the smallest
accurate fix:

- update the target path if the destination moved
- restore or create the destination file if it is still part of the workflow
- remove the link if the destination is no longer a durable artifact

For a missing index page, create or restore `docs/README.md` before relying on
other navigation docs. For a missing top-level directory link, add the area to
`docs/README.md` only when it is a durable operator-facing surface.

For registry consistency failures, run:

```sh
python3 scripts/ahl.py registry check
```

Update the source document first when source and registry disagree. Then update
the relevant registry entry if it remains a useful curated navigation pointer.
