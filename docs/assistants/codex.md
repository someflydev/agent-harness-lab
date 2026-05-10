# Codex Usage Guide

This guide describes a Codex-style session for running one
`agent-harness-lab` prompt. Product details can vary by environment, so treat
repo files and the active prompt as authoritative. Codex can be used through a
local or manual subscription workflow when available; AHL prepares bounded
instructions and local checks, while the Codex tool executes the prompt work
under the operator's local permissions.

## Start A Fresh Session

Open the repo in a fresh Codex session from the repository root. Ask for one
bounded prompt, for example:

```text
Load AGENT.md, then run .prompts/PROMPT_29.txt
```

The assistant should inspect `git status --short` before editing and preserve
unrelated modified or untracked files.

## Load First

Start with:

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- the active prompt file
- any docs named by the prompt

Load hot-spot files before changing them. Avoid loading local reference repos
unless the prompt explicitly asks for comparison.

## Run One Prompt

Keep the session scoped to the active `.prompts/PROMPT_XX.txt`. Implement only
that prompt's deliverables, constraints, and validation requirements. Do not
quietly implement future prompt work.

## Templates And Skills

If project skills are available in the Codex environment, use the matching
skill for recurring routines such as prompt execution, completion audit, or
handoff composition. Otherwise read the relevant `.agents/skills/<name>/SKILL.md`
file as ordinary markdown.

Prompt templates in `prompt-templates/` are reusable manual starters. They are
not implementation prompts and should not replace the numbered promptset.

## Validation And Commands

Use local commands named by the prompt when available, such as:

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py docs check
python3 scripts/ahl.py validate
python3 -m unittest tests/test_ahl.py
```

If a command cannot run, report the reason and any residual risk. Do not invent
validation evidence.

## Closeout

Close every prompt run with:

1. Execute - finish the prompt-scoped edits.
2. Audit - compare deliverables against the prompt.
3. Preflight - inspect only the immediate next prompt for readiness.
4. Bridge - create `tmp/HANDOFF.md` only for a real blocker or warning.
5. Reset - leave a clear final summary and do not commit unless asked.

## Limitations

- Tool-specific skill discovery should not be assumed outside the active
  environment.
- Network access, shell permissions, and edit permissions may differ by setup.
- AHL does not query Codex subscription status, quota, or account limits.
- Codex chat context is not durable project memory unless promoted into repo
  artifacts.
