# Pi Usage Guide

This guide describes a Pi-style assistant workflow for `agent-harness-lab`.
The repo can expose prompts, templates, docs, and skills as ordinary project
context, but the core operating model stays manual and inspectable.

## Start A Fresh Session

Start a new session for one bounded task. Use a direct instruction:

```text
Run .prompts/PROMPT_29.txt using AGENT.md startup guidance.
```

Keep the session focused on that prompt and reset after closeout.

## Load First

Use:

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- the active numbered prompt
- any docs named by the prompt

Avoid loading all templates, skills, or docs unless the session type requires
them.

## Run One Prompt

Treat `.prompts/PROMPT_XX.txt` as ordered implementation work. Run one prompt
per fresh session unless the operator explicitly expands scope.

## Templates And Skills

Pi-style project context may make prompt templates and skills convenient to
select. Use them conservatively:

- `prompt-templates/` contains reusable startup prompts for routines.
- `.agents/skills/` contains optional assistant procedure for recurring tasks.
- Numbered prompts remain the only implementation promptset.

If the tool does not automatically expose these files, copy or load them as
ordinary markdown.

## Validation And Commands

Run local checks through the available command surface, or ask the operator to
run them when shell access is not available. Prefer checks named by the active
prompt, then cheap repo checks such as:

```sh
python3 scripts/ahl.py doctor
python3 scripts/ahl.py docs check
python3 scripts/ahl.py promptset
```

## Closeout

Use Execute -> Audit -> Preflight -> Bridge -> Reset:

1. Finish prompt-scoped edits.
2. Audit deliverables and constraints.
3. Inspect the immediate next prompt.
4. Bridge only for real blockers or warnings.
5. Reset with validation evidence and residual risks.

## Limitations

- Project-context loading can make it easy to overread; keep context bounded.
- Skills are repo-authored instructions, not guaranteed runtime capabilities.
- Subscription quota and context limits still apply.
