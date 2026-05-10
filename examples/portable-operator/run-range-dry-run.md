# Run-Range Dry-Run

Dry-run a sequential range against the fake basic fixture:

```sh
python3 scripts/ahl.py lifecycle run-range 1 2 --project fixtures/portable-operator/projects/basic --dry-run --json
```

The plan should include `PROMPT_01` and `PROMPT_02`, reusable lifecycle
snippets for each prompt, commit-plan and make-commits as separate phases, a
commit-check phase after commits exist, and a fresh-session boundary after
each prompt.

The range plan is not a scheduler. It does not run assistants, execute target
validation commands, edit project files, edit `human-notes.md`, stage, commit,
amend, rebase, push, tag, or continue automatically.

Dry-run the gapped fixture to see a planning stop:

```sh
python3 scripts/ahl.py lifecycle run-range 1 3 --project fixtures/portable-operator/projects/gapped --dry-run --json
```

That plan should report missing `PROMPT_02`, set a range-validation stop
reason, and avoid presenting the range as ready to run.

For a Claude-style bootstrap surface, generate snippets with an explicit
bootstrap choice:

```sh
python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/claude-bootstrap --bootstrap CLAUDE.md --json
```

This selects `CLAUDE.md` without implying that AHL will invoke Claude Code or
any other provider CLI.
