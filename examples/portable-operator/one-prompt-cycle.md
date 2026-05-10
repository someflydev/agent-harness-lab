# One-Prompt Portable Cycle

This example uses the fake basic fixture:

```sh
python3 scripts/ahl.py project status --project fixtures/portable-operator/projects/basic --json
```

The status report should show a valid sequential promptset, `AGENT.md`,
`.context/`, no checked-in `.git/` directory, and likely next prompt
`PROMPT_03` based on the highest fixture prompt file.

Generate copy/paste instructions for the first prompt:

```sh
python3 scripts/ahl.py lifecycle snippets PROMPT_01 --project fixtures/portable-operator/projects/basic --json
```

The run snippet names `AGENT.md` and `.prompts/PROMPT_01.txt`. The audit
snippet asks whether implementation is complete, inspects only `PROMPT_02` for
readiness, and checks whether `AGENT.md` or `.context/` should change. If no
durable workflow, architecture, command, convention, or navigation knowledge
changed, the audit result is `no context update needed`.

Use the read-only context helper during closeout:

```sh
python3 scripts/ahl.py lifecycle context-check PROMPT_01 --project fixtures/portable-operator/projects/basic --json
```

Because the fixture has no `.git/` directory, the helper cannot infer changed
paths and reports that limitation instead of editing context files.

Commit planning and commit execution stay separate. First ask for grouped
commit suggestions, with subjects prefixed by `[PROMPT_01]` and Tim Pope style
multi-line messages. Only after operator approval should the assistant receive
the separate instruction to make commits.

After commits exist in a real target project, run:

```sh
python3 scripts/ahl.py commit check --project /path/to/project --prompt PROMPT_01 --json
```

That check is post-commit and read-only. It looks for prefix, message format,
literal `\n`, co-author trailers, generated boilerplate, and grouping hygiene.

If a real target project contains `human-notes.md`, treat it as
operator-owned. Report its presence when relevant, but do not edit it or use it
as authoritative machine state.
