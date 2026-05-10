# Portable Operator Operating Baseline

This baseline describes the supported local path for using AHL from another
project repo that has its own `.prompts/` directory. AHL supplies local status,
snippets, dry-run plans, advisory context checks, and commit inspection. The
operator still runs one assistant session at a time and decides what changes
are accepted.

## Invoke AHL From A Target Project

From the AHL checkout:

```sh
python3 scripts/ahl.py project locate --project /path/to/project --json
```

From another project repo:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py project locate --json
```

`AHL_HOME` may point to the AHL checkout, but the default script-location
discovery is usually enough. Invalid AHL homes and missing project paths are
reported as command problems.

## Check Project Status

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py project status --project /path/to/project --json
```

Review git status, `.prompts/` diagnostics, prompt numbering, bootstrap files,
`.context/`, `human-notes.md` presence, recent prompt-prefixed commits, and
likely next-prompt inference. Missing optional context files are status for
human review, not automatic blockers.

## Generate One-Prompt Snippets

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project --bootstrap CLAUDE.md
```

Use the generated run snippet in a fresh Codex, Claude Code, Gemini, generic
chat, or manual assistant surface. The common run shape is:

```text
Load AGENT.md, then run .prompts/PROMPT_84.txt
```

The snippets are instructions only. They do not invoke assistants, edit files,
run validation, stage, commit, or call providers.

## Run And Audit Manually

Run exactly one prompt in the chosen assistant surface. After implementation,
use the generated audit snippet to compare deliverables, constraints,
validation evidence, and changed files against the prompt. Inspect only the
immediate next prompt for readiness and stop at that boundary.

Inline repair is appropriate only when the issue is small, fresh, and tied to
the active prompt. If the repair expands beyond that prompt, stop and use a
dedicated repair session or handoff.

## Check Context-Update Candidates

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle context-check PROMPT_84 --project /path/to/project --json
```

Use the report as advisory input. Update `AGENT.md`, `CLAUDE.md`, `.context/`,
or `context/` only when future fresh sessions need durable workflow,
architecture, command, convention, or navigation knowledge. If no durable
context changed, record `no context update needed` in closeout instead of
editing files.

`human-notes.md` is operator-owned and informational. AHL may report whether it
exists, but it is never machine-authoritative and is not edited by portable
helpers.

## Request Commit Suggestions Separately

Use the snippet-generated commit-plan text only after implementation and
validation are done. Commit suggestions are separate from commit execution.
Commits should use prompt-prefixed subjects such as:

```text
[PROMPT_84] Add import validation
```

Creating commits remains an explicit operator decision. AHL does not stage or
commit portable target-project changes by default.

## Inspect Commits Afterward

After commits exist, inspect them without rewriting history:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py commit check --project /path/to/project --prompt PROMPT_84 --json
python3 /path/to/agent-harness-lab/scripts/ahl.py commit check --project /path/to/project --last 7 --json
python3 /path/to/agent-harness-lab/scripts/ahl.py commit check --project /path/to/project --range HEAD~10..HEAD --json
```

The helper reports prompt-prefix, subject/body shape, wrapping, literal `\n`,
co-author trailer, generated-boilerplate, merge, and grouping issues. It may
suggest manual amend or rebase commands when there is a clear issue, but it
never runs them.

## Dry-Run A Prompt Range

For a request such as "run prompts 18 through 27", create an inspectable plan
first:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --dry-run --json
```

The plan contains one step per prompt with run, audit/context review, optional
repair, commit-plan, explicit-only make-commits, commit-check, fresh-session,
and stop-boundary phases. It does not invoke assistants or continue
automatically. Write a plan artifact only when needed:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle run-range 18 27 --project /path/to/project --artifact runs/portable-operator/run-range.json --json
```

Relative artifact paths are resolved under the AHL checkout and existing
artifacts require explicit `--force` to overwrite.

## Stop Cleanly

At the end of each prompt:

- Audit the active prompt.
- Record validation results or unavailable checks.
- Decide whether context updates are justified.
- Package commits only with operator approval.
- Run `commit check` after commits, when applicable.
- Inspect only the immediate next prompt for readiness.
- Stop before running the next prompt in the same assistant session.

No provider secrets, network access, expensive APIs, machine-readable
subscription quota checks, or background daemon are required for this baseline.
