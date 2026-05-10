# Gemini Usage Guide

This guide describes a Gemini-style coding assistant session for
`agent-harness-lab`. Use the local repo artifacts as the source of truth and
avoid assuming product features that are not visible in the current setup.
Gemini can be used manually or through local CLI behavior only where the
operator has verified that behavior locally.

## Start A Fresh Session

Open a fresh assistant session in the repo root and provide a bounded request:

```text
Load AGENT.md, then run .prompts/PROMPT_29.txt
```

The assistant should inspect `git status --short` before editing.

## Load First

Load:

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- the requested `.prompts/PROMPT_XX.txt`
- docs explicitly referenced by that prompt

Add local files only when the active prompt needs them.

## Run One Prompt

Execute only the requested numbered prompt. Do not treat nearby prompts,
architecture notes, or future automation ideas as implemented requirements.

## Templates And Skills

If the Gemini-style environment can load project files, read prompt templates
and skills as plain markdown. Prompt templates are copyable routine starters.
Project skills are optional focused procedure. Neither should be treated as
hidden automation.

## Validation And Commands

Use local validation commands when the environment supports shell execution.
If commands are not available, ask the operator to run them or clearly state
that validation was not run.

Useful commands include:

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py docs check
python3 scripts/ahl.py validate
```

## Closeout

End with Execute -> Audit -> Preflight -> Bridge -> Reset:

- Compare changed files to the active prompt.
- Record validation evidence or explain skipped checks.
- Inspect only the next prompt for readiness.
- Write `tmp/HANDOFF.md` only when it materially helps the next session.
- Do not commit unless the operator asks.

## Limitations

- File access, editing behavior, and command execution vary by setup.
- Automatic project skill discovery should not be assumed.
- Manual copy/paste may be needed when repository access is limited.
- AHL does not query Gemini subscription status, quota, or account limits, and
  it does not assume a local CLI supports headless execution until verified.
