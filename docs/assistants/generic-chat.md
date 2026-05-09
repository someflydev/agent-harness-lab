# Generic Chat Usage Guide

This guide is for assistants that do not have direct repository access, shell
access, or file editing. The operator can still use the same prompt-bounded
workflow by copying the required files manually. This is the same file-backed
one-prompt loop used by Codex, Claude Code, Gemini, and other coding assistant
surfaces; only the transport changes.

## Start A Fresh Session

Open a new chat and paste a short instruction:

```text
You are helping with agent-harness-lab. I will paste the required repo files.
Run one prompt only and ask for missing files before making assumptions.
```

Then paste the startup context and active prompt.

## Load First

Paste only:

- `AGENT.md`
- the relevant parts of `README.md`
- `docs/guardrails.md`
- the active `.prompts/PROMPT_XX.txt`
- docs explicitly named by the prompt
- snippets from files that must be edited

For large files, paste the relevant section plus enough surrounding context to
make a safe edit.

## Run One Prompt

Ask the assistant to return patch-style edits or complete file sections. Apply
the changes locally, then run validation commands yourself.

Do not ask the assistant to infer hidden repo state. If it needs a file, paste
that file or a focused excerpt.

For portable target projects, use the same lifecycle snippets as terminal
assistant sessions:

```sh
python3 /path/to/agent-harness-lab/scripts/ahl.py lifecycle snippets PROMPT_84 --project /path/to/project
```

Paste the generated run, audit, commit-plan, make-commits, or commit-check
snippet into the chat when that step is actually in scope.

## Templates And Skills

Prompt templates and project skills are still useful in generic chat, but they
must be pasted manually. Use only the template or skill that matches the
current routine.

## Validation And Commands

Generic chat assistants usually cannot run local commands. The operator should
run checks such as:

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py docs check
python3 scripts/ahl.py validate
python3 -m unittest tests/test_ahl.py
```

Paste relevant failures back into the same bounded session if repair is needed.

## Closeout

Close with the same loop:

1. Execute - apply the intended edits.
2. Audit - compare edits to the prompt.
3. Preflight - inspect the next prompt.
4. Bridge - create `tmp/HANDOFF.md` only for material blockers.
5. Reset - start a new chat for the next prompt.

Keep private planning blobs and `human-notes.md` under operator control. Paste
only the safe excerpts needed for the current bounded task.

## Limitations

- The assistant sees only what the operator pastes.
- Patch application and validation are operator responsibilities.
- Long files can exceed context limits; use narrow excerpts and explicit file
  paths.
