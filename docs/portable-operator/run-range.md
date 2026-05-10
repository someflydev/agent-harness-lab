# Portable Run Range

`lifecycle run-range` creates a dry-run plan for running a prompt range in an
arbitrary target project while keeping the actual work one prompt at a time.
It is a local planning command, not an assistant runner.

## Invocation

From the AHL checkout:

```sh
python3 scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --dry-run --json
```

From another project, call the AHL script directly:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --dry-run --json
```

When `--project` points at a directory that already contains `.prompts/`, that
directory is treated as the target project root even if it is nested inside
another git checkout. This keeps checked-in fixtures usable as artificial
target projects.

Prompt inputs may be numbers, ids, or filenames such as `18`, `PROMPT_18`, or
`PROMPT_18.txt`.

## What The Plan Contains

The JSON plan includes:

- AHL home and target project root discovery.
- Requested range and resolved prompt ids in strict sequential order.
- Missing prompt and malformed filename diagnostics.
- One step per prompt, each with run, audit/context review, optional repair,
  commit-plan, explicit-only make-commits, commit-check, fresh-session, and
  stop-boundary phases.
- Snippet payloads generated from the same lifecycle snippet rules used for a
  single prompt.
- Restart state with project root, prompt ids, planned artifact path, stop
  reason, and next prompt pointer.
- Safety notes for dirty worktrees, missing prompts, `human-notes.md`, and
  commit authority.

By default the plan is printed only. Use `--artifact <path>` to write JSON.
Relative artifact paths are resolved under the AHL checkout. Existing
artifacts are not overwritten unless `--force` is explicit.

## Boundaries

The command does not invoke assistant CLIs, call providers, execute validation
commands, edit target project files, edit `human-notes.md`, stage, commit,
amend, rebase, push, tag, or schedule automatic continuation.

Failures stop at planning time. A missing prompt, reversed range, duplicate
prompt number, or malformed prompt filename produces a failed plan with a
`stop_reason` instead of automatic repair or continuation.
