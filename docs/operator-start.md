# Operator Start

This page describes the basic human operator routine for a fresh clone or a
fresh assistant session.

## Fresh Clone

1. Review `README.md` for the project identity and current status.
2. Review `AGENT.md` for assistant bootstrap expectations.
3. Review `docs/guardrails.md` for boundaries that should hold across prompts.
4. Check the working tree with `git status --short`.
5. Confirm local reference repos, if present, are treated as ignored reference
   material.

There is no required setup command yet. Later prompts may add scripts or checks
when they are justified by the workflow.

## Fresh Prompt Session

1. Start a new assistant session.
2. Ask the assistant to run exactly one prompt, for example
   `Run .prompts/PROMPT_01.txt`.
3. Expect the assistant to inspect repo state before editing.
4. Keep the session scoped to that prompt unless a small repair is needed for
   the prompt's own readiness or closeout.

## Closing A Session

At closeout, the assistant should:

1. Audit the completed work against the prompt's required deliverables.
2. Run or explain relevant validation.
3. Inspect the next prompt and state whether the repo is ready for it.
4. Create `tmp/HANDOFF.md` only if a blocker or non-trivial next-session warning
   remains.
5. Avoid committing unless the operator explicitly asks.

The final answer should summarize changed files, validation evidence, next
prompt readiness, and any residual risks.
