# Claude Code Usage Guide

This guide describes a Claude Code-style terminal assistant session for
`agent-harness-lab`. Keep product-specific assumptions light; the repo workflow
is based on files, prompts, commands, and operator review.

## Start A Fresh Session

Start a new assistant session in the repository root. Give a narrow instruction:

```text
Load AGENT.md, then run .prompts/PROMPT_29.txt
```

The assistant should check the working tree before edits and should not change
unrelated files.

## Load First

Use this startup set:

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- the active `.prompts/PROMPT_XX.txt`
- prompt-named docs and existing files that will be edited

Keep context loading narrow. Do not scan broad reference repos by default.

## Run One Prompt

Treat the numbered prompt as the session contract. Execute one prompt only,
including its deliverables, constraints, validation, and endcap instructions.

## Templates And Skills

If the local Claude Code setup supports Agent Skills-like packages, a matching
`.agents/skills/<name>/SKILL.md` file may be useful procedure. If not, read it
as normal markdown. Do not claim automatic discovery unless the operator's
environment provides it.

Use `prompt-templates/` only when the operator is launching a reusable routine,
such as an audit, repair session, or commit packaging task.

## Validation And Commands

Run prompt-required checks and cheap relevant checks. Common checks include:

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py docs check
python3 scripts/ahl.py promptset
python3 -m unittest tests/test_ahl.py
```

Report command failures directly. If a permission prompt is needed, ask before
continuing with the command.

## Closeout

Use the same closeout loop as every other assistant:

1. Execute the prompt.
2. Audit required deliverables and validation.
3. Preflight the immediate next prompt.
4. Bridge only if a blocker or non-trivial warning remains.
5. Reset with a concise final summary.

## Limitations

- Terminal command permissions depend on the operator's local setup.
- Skills and templates are repo artifacts, not guaranteed tool features.
- Assistant transcripts should not be stored as durable state by default.
