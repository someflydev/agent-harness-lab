# Claude Bootstrap Fixture

This fake project intentionally has `CLAUDE.md` and no `AGENT.md`.

Use it to test explicit Claude-style lifecycle snippet generation:

```sh
python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/claude-bootstrap --bootstrap CLAUDE.md --json
```

Do not call Claude Code or any provider CLI while using this fixture.
