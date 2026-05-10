# Portable Operator Fixtures

These fixtures are small artificial target projects for testing portable
operator helpers without private repositories, provider credentials, network
access, or assistant quota. They are not real project histories and should not
be treated as examples of completed work.

## Projects

- `projects/basic/` - sequential `PROMPT_01` and `PROMPT_02`, an `AGENT.md`
  bootstrap file, and a tiny `.context/` example.
- `projects/claude-bootstrap/` - a Claude-style target with `CLAUDE.md` and no
  `AGENT.md`, useful for explicit bootstrap selection.
- `projects/gapped/` - a promptset with `PROMPT_01` and `PROMPT_03` so status
  and range dry-runs can report a missing `PROMPT_02`.

## Safe Use

The fixture projects contain no `.git/` directories, secrets, tokens, private
gist content, or personal notes. They are intended for read-only commands such
as:

```sh
python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/basic --json
python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/basic --json
python3 scripts/ahl.py lifecycle context-check PROMPT_01 --project fixtures/portable-operator/projects/basic --json
python3 scripts/ahl.py lifecycle run-range 1 2 --project fixtures/portable-operator/projects/basic --dry-run --json
python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/claude-bootstrap --bootstrap CLAUDE.md --json
python3 scripts/ahl.py lifecycle run-range 1 3 --project fixtures/portable-operator/projects/gapped --dry-run --json
```

`human-notes.md` remains operator-owned in real target projects. These fixtures
do not include one, and the examples describe the boundary without requiring
private notes.
