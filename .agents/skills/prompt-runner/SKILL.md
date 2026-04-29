---
name: prompt-runner
description: Run exactly one .prompts/PROMPT_XX.txt in fresh-session style from startup through scoped implementation and closeout.
---

## When To Use

Use when the operator asks to run a specific implementation prompt. This skill
fits normal prompt-execution sessions, not prompt authoring, broad repair, or
unbounded review.

## Required Context

- `AGENT.md`
- `README.md`
- `docs/guardrails.md`
- The active `.prompts/PROMPT_XX.txt`
- Docs explicitly named by the active prompt
- Existing files that will be edited, especially hot spots
- `git status --short` before editing and near closeout

## Step-By-Step Behavior

1. Confirm the active prompt id and read the required startup context.
2. Record current repo state from `git status --short`.
3. Extract required deliverables, constraints, validation steps, and non-goals.
4. Edit only files needed for the active prompt.
5. Preserve unrelated modified or untracked files.
6. Run required or cheap relevant validation.
7. Audit deliverables against the prompt before claiming completion.
8. Inspect only the immediate next prompt for readiness.
9. Create `tmp/HANDOFF.md` only if a real blocker or non-trivial warning
   remains.
10. Do not stage or commit unless the operator explicitly asks.

## Expected Output

- Completed active-prompt deliverables
- Validation evidence or skipped-check explanation
- Completion audit summary
- Immediate next-prompt readiness statement
- Optional handoff only when justified

## Stop Conditions

- A prerequisite named by the prompt is missing.
- The work would implement a future prompt.
- Validation exposes a material blocker.
- The next step needs operator authority.

## Safety Notes

- Run one prompt per session unless the operator explicitly expands scope.
- Do not load local reference repos by default.
- Do not convert prompt execution into hidden automation.

## References

- `runbooks/fresh-session-prompt-run.md`
- `runbooks/completion-audit.md`
- `runbooks/next-prompt-preflight.md`
- `runbooks/run-closeout.md`
- `docs/runtime/execute-audit-preflight-bridge-reset.md`
- `prompt-templates/prompt-run.md`
