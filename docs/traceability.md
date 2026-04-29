# Traceability

Traceability in this repo is lightweight derived metadata that helps an
operator connect one prompt-bounded session to visible repo changes, validation
evidence, readiness decisions, handoffs, and later commits.

## Trace Command

Use:

```sh
python3 scripts/ahl.py trace PROMPT_20 --json
```

The command collects local facts that are safe and cheap:

- normalized prompt id and whether `.prompts/<prompt_id>.txt` exists
- current git branch and short HEAD commit when git can provide them
- `git status --short --untracked-files=all` lines and derived changed paths
- changed top-level directories
- whether docs, tests, or templates changed
- whether `tmp/HANDOFF.md` exists
- a run-record skeleton with fields still needing operator input

If git is unavailable or the command runs outside a git working tree, the JSON
result degrades instead of crashing. In that case, branch, HEAD, and changed
files are unknown or empty, and `git.degraded` plus `git.problems` explain why.

## What It Does Not Collect

The trace command does not inspect raw assistant transcripts, parse full diffs
by default, call provider APIs, write telemetry, create commits, stage files, or
store results outside the operator's chosen artifacts. It is a closeout helper,
not a database or runtime service.

## Commit Prefixes

Prompt-id commit prefixes such as `[PROMPT_20] Add trace collector` make later
analysis possible with normal git commands. They let reviewers connect a
prompt to its eventual commit group without relying on chat history. The trace
output can capture working-tree facts before packaging, and commit hashes can
be added later to a run record when the operator chooses to commit.

## Closeout Use

During closeout, run the trace command after implementation and validation.
Use the JSON output to fill the changed-file, changed-directory, handoff, and
derived boolean fields in a run record or final-answer checklist. Fill the
remaining suggested fields manually: assistant driver, model, reasoning or
thinking setting, permission posture, invocation command, validation commands,
audit status, readiness status, and any associated commits.

## Derived Metadata

Trace output is derived metadata. Git history, prompt files, docs, tests,
templates, validation output, and deliberate handoffs remain the source of
truth. A trace summary is useful because it is rebuildable from local repo
state and compact enough to audit.
