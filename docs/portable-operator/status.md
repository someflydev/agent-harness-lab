# Portable Project Status

`project status` gives the operator a quick, local, read-only report for a
target project before starting a one-prompt assistant session. It does not run
assistants, execute prompt validation commands, edit project files, stage
changes, commit, fetch network resources, or require credentials.

## Invocation

From the AHL checkout:

```sh
python3 scripts/ahl.py project status --json
```

From another project, call the AHL script directly:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py project status --project /path/to/project --json
```

Without `--project`, the command inspects the current working directory. If the
requested directory is inside a git work tree and git is available, the
reported target project root is the containing git root. Otherwise the
requested directory is used as the project root.

## Reported State

The report includes:

- AHL home and target project root.
- Whether `.git/` exists, whether a git root was found, current branch when
  available, dirty count, untracked count, and raw short status lines.
- Whether `.prompts/` exists, prompt count, lowest and highest prompt numbers,
  gaps, duplicate numeric ids, malformed prompt filenames, and strict
  two-digit naming status.
- `next_after_highest_prompt_file`, recent prompt-prefixed commits, and a
  `likely_next_prompt` with confidence and reason.
- Presence of `AGENT.md`, `CLAUDE.md`, `.context/`, and `human-notes.md`.
- Warnings and problems that keep ordinary missing optional files from
  becoming tracebacks.

Prompt filename diagnostics reuse the same parser as `promptset`. The status
command distinguishes a missing `.prompts/` directory, an empty prompt
directory, a valid sequential promptset, prompt gaps, malformed filenames, and
duplicate numeric prompt ids.

## Next Prompt Inference

`next_after_highest_prompt_file` is derived only from the highest prompt file
number in `.prompts/`. Prompt-prefixed commit evidence is derived from recent
commit subjects such as `[PROMPT_44] ...`.

When prompt files and prompt-prefixed commit history agree, confidence is high.
When they disagree, `likely_next_prompt` uses commit progress as completed-work
evidence and explains the disagreement. When only prompt files are available,
the file-derived next prompt is reported with medium confidence. When neither
source is available, the likely next prompt is unknown.

## Boundaries

`human-notes.md` is reported only as present or absent. The command does not
parse it, update it, or treat it as authoritative machine state.

Missing `AGENT.md`, `CLAUDE.md`, `.context/`, `human-notes.md`, or `.prompts/`
is reported as status for human review. Invalid AHL home or invalid requested
project paths remain command problems.
