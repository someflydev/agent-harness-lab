# Context Loading

Use the smallest context set that can complete the session safely. Add files
only when the active routine requires them or when validation output shows a
specific gap.

## Loading Matrix

| Session type | Load first | Add only when needed | Avoid |
| --- | --- | --- | --- |
| Prompt execution | `AGENT.md`, `README.md`, `docs/guardrails.md`, active `.prompts/PROMPT_XX.txt` | Prompt-named docs, hot-spot files, validation output | Future prompts, broad reference repos, whole doc tree |
| Completion audit | Active prompt, changed-file summary, validation output, `runbooks/completion-audit.md` | Changed files and related docs | New implementation work |
| Repair session | `AGENT.md`, blocker summary or `tmp/HANDOFF.md`, affected files, relevant runbook | Failing command output, prompt constraints | Unrelated cleanup |
| Prompt authoring | `AGENT.md`, `README.md`, prompt-authoring runbook, nearby prompt files, relevant registries | Prompt templates, quality docs | Executing the prompt being authored |
| Role-lane simulation | Role pack or lane playbook, lane template, assigned scope | Specific source files for the lane | Cross-lane files without coordination |
| Memory promotion review | Promotion candidate, evidence artifact, memory workflow docs | Related decision records | Raw transcript dumps as trusted state |

## General Rules

- Load the active contract before exploratory context.
- Prefer prompt-named docs over whole directories.
- Read hot-spot files before editing them.
- Treat `tmp/HANDOFF.md` as transient bridge context, not durable memory.
- Do not load local reference repos unless the active prompt explicitly asks
  for reference influence or a narrow comparison.
