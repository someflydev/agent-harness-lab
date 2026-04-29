# Project Skills

This directory contains optional project-level skills for common
`agent-harness-lab` routines. Each skill is a small instruction package with a
`SKILL.md` file and no executable code.

Skills are on-demand context, not mandatory startup material. Load one when the
active task matches its description, then read only the required context named
by that skill.

## Available Skills

- `prompt-runner` - run one `.prompts/PROMPT_XX.txt` in fresh-session style.
- `completion-auditor` - compare prompt requirements with actual repo state.
- `readiness-checker` - inspect the immediate next prompt for readiness.
- `handoff-composer` - compose `tmp/HANDOFF.md` only when a bridge is justified.
- `memory-promoter` - decide whether a transient fact deserves durable memory.
- `promptset-inspector` - inspect prompt numbering, scope, and execution order.
- `role-lane-planner` - decompose work into Orchestrator, Lead, and Worker lanes.
- `trajectory-evaluator` - evaluate closeout trajectory after a prompt Endcap.

## Boundaries

- Do not treat skills as automation or provider-specific features.
- Do not load every skill during startup.
- Do not add scripts or hidden runtime behavior inside this directory unless a
  later prompt explicitly asks for it.
- Keep source-of-truth decisions in repo docs, templates, runbooks, registries,
  and git history.
