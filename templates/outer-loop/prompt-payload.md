# Fresh Prompt Execution Payload

Run exactly one prompt file: `{{ prompt_id }}` at `{{ prompt_path }}`.

## First Read

Read these local files before editing:

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- `{{ prompt_path }}`
- Any docs explicitly named by the active prompt

Do not paste the whole repository into context. Read only the files needed for
this prompt and any hot spots before editing them.

## Execution Rules

- Execute only the named prompt file.
- Preserve unrelated modified or untracked files.
- Do not commit, stage, push, tag, publish, or delete history unless the outer
  runner or authorized operator explicitly asks.
- Do not store raw transcripts, conversation dumps, credentials, or provider
  secrets.
- Keep changes scoped to the prompt's required deliverables and constraints.

## Validation

Run required or cheap relevant validation before claiming completion. Expected
commands from the plan:

{{ validation_commands }}

## Endcap

- Audit every required deliverable against the prompt.
- Inspect the immediate next prompt for readiness.
- Create `tmp/HANDOFF.md` only if a real blocker or non-trivial warning
  remains.
- Summarize changed files, validation evidence, residual risks, and
  next-prompt readiness.
