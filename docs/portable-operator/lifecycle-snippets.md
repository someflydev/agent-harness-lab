# Lifecycle Snippet Generation

`lifecycle snippets` prints reusable copy/paste instructions for one prompt in
a target project. It is local, read-only, provider-agnostic helper output for
Codex, Claude Code, Gemini, or generic chat workflows.

## Invocation

From the AHL checkout:

```sh
python3 scripts/ahl.py lifecycle snippets 84 --project /path/to/project
python3 scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project --json
```

From another project, call the AHL script directly:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project
```

Prompt input may be a number, prompt id, or filename, such as `84`,
`PROMPT_84`, or `PROMPT_84.txt`.

## Generated Snippets

The default cluster includes:

- run the selected prompt;
- audit implementation, inspect only the next prompt for readiness, and check
  whether bootstrap or `.context/` files should be updated;
- suggest grouped Tim Pope style commit messages with heredoc guidance;
- ask the assistant to make commits after operator approval;
- inspect the just-created commits for formatting, prefix, grouping, literal
  `\n`, and co-author issues.

`--include-repair` adds a separate repair snippet. It is intentionally outside
the default cluster so routine prompt runs do not imply repair work.

The audit snippet includes the context-update sentence because prompt closeout
is the right moment to ask whether durable bootstrap or context knowledge
changed. The answer is often no. Assistants should report `no context update
needed` in the audit when no durable workflow, architecture, command,
convention, or repo-navigation knowledge changed, not edit files just to prove
the check happened.

When candidates exist, produce a short context-update candidate report before
editing. Name the changed paths, the possible durable knowledge, affected
targets such as `AGENT.md`, `CLAUDE.md`, `.context/`, or `context/`, and any
uncertainty. Prefer checked-in docs and templates for broad guidance; keep
bootstrap/context edits concise and only for future fresh-session needs.

## Configuration

By default, the run snippet uses `AGENT.md` when it is present in the target
project. Use `--bootstrap CLAUDE.md` for Claude-style projects, or
`--bootstrap none` when no bootstrap doc should be named.

`.context/` is mentioned with the default `AGENT.md` bootstrap doctrine and
when detected in the target project. Use `--context` to mention it even when
absent under other bootstrap choices, or `--no-context` to omit it from the
context update snippet.

Without `--project`, the command inspects the current working directory. If
that path is inside a git work tree, the target project root is the containing
git root; otherwise the requested directory is used.

## Boundaries

The command does not run assistants, execute validation commands, edit
`human-notes.md`, modify the target project, stage files, commit, fetch
network resources, or require provider credentials. Missing prompt or
bootstrap files are reported as warnings so the operator can decide whether to
proceed.

`lifecycle context-check` is a read-only companion command for the same audit
step:

```sh
python3 scripts/ahl.py lifecycle context-check PROMPT_84 --project /path/to/project --json
```

It inspects changed paths and suggests conservative review questions. It does
not create `.context/`, edit bootstrap files, edit `context/`, or change any
target-project file.
