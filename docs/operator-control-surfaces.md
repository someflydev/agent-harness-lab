# Operator Control Surfaces

This page names the controls an operator should be able to find, even when the
current implementation is still a runbook or assistant routine rather than a
scripted command. The goal is discoverability without pretending this repo has
a runtime engine.

## Surface Registry

| Surface | Current form | Purpose | Primary inputs | Expected outputs |
| --- | --- | --- | --- | --- |
| Run common local checks from a console | Makefile target | Make stable helper commands discoverable without memorizing subcommands. | `Makefile`, `scripts/ahl.py`, active prompt id for trace. | Human command output and normal exit codes. |
| Run current prompt only | Runbook | Execute one active prompt inside its stated scope. | `AGENT.md`, active prompt, required prompt docs, `git status --short`. | Prompt deliverables and validation notes. |
| Run current prompt then audit | Runbook | Execute one prompt and check delivered artifacts against requirements. | Active prompt, changed files, validation evidence. | Completion audit status and unmet requirements if any. |
| Run current prompt plus audit plus preflight next | Runbook | Add immediate next-prompt readiness after completion audit. | Active prompt, next prompt, changed files, docs indexes. | Completion audit plus ready, risky, or blocked readiness statement. |
| Run current prompt plus full endcap workflow | Runbook | Execute, audit, preflight, bridge if needed, and reset. | Active prompt, next prompt, runbooks, repo status. | Final closeout, readiness result, optional `tmp/HANDOFF.md`. |
| Generate handoff only | Helper-script command | Create a temporary handoff scaffold when a bridge decision says one is needed. | `templates/handoffs/handoff.md`, `--force` when intentionally replacing. | `tmp/HANDOFF.md`. |
| Inspect promptset health | Helper-script command | Check prompt file numbering and strict naming. | `.prompts/PROMPT_*.txt`. | Human summary or JSON promptset index. |
| Probe assistant driver records | Helper-script command | Check conservative local driver records and optional help-only executable probes. | `registry/assistant-drivers.json`, local `PATH`. | Driver summaries, warnings, and probe results. |
| Plan or dry-run an outer-loop sequence | Helper-script command | Build reviewable prompt payloads, plans, ledgers, and gates before any live step. | Prompt range, driver id, plan artifact. | `runs/outer-loop/` artifacts and JSON reports. |
| Use AHL from a target project | Helper-script command | Inspect another repo's promptset and print one-prompt lifecycle snippets. | Target project root, prompt id or range. | Read-only project status, snippets, context questions, and run-range plans. |
| Explain why next prompt is not ready | Runbook | Inspect the immediate next prompt for blockers or warnings without implementing it. | Current output, next prompt, docs navigation, validation state. | Readiness report or final-answer readiness explanation. |
| Collect prompt-to-commit traceability | Runbook/helper-script command | Connect prompt-bounded work to commit prefixes and changed files after the operator asks to commit. | Prompt id, git status, git log, commit messages, validation notes. | Traceability notes, commit plans, commit-check reports, and commit hash list when available. |
| Summarize current prompt scope and changed areas | Helper-script command | Provide a compact run-record-oriented view of scope and changed paths. | Active prompt id, `git status --short`, changed files. | Scope summary and candidate run record fields. |
| Retrieve similar prior prompts, handoffs, or doctrine chunks in the future | Future automation candidate | Help prompt authors and operators find relevant prior artifacts without storing raw transcripts. | Prompt ids, durable docs, run records, findings, handoffs that still exist. | Ranked artifact references with evidence paths. |

## Implementation Status

| Surface | Status |
| --- | --- |
| Run common local checks from a console | `make help`, backed by `python3 scripts/ahl.py help`. |
| Run current prompt only | `runbooks/fresh-session-prompt-run.md` and prompt startup instructions. |
| Run current prompt then audit | `runbooks/completion-audit.md`. |
| Run current prompt plus audit plus preflight next | `runbooks/next-prompt-preflight.md` plus completion audit. |
| Run current prompt plus full endcap workflow | `runbooks/run-closeout.md`, `docs/runtime/execute-audit-preflight-bridge-reset.md`, and `AGENT.md` endcap routine. |
| Generate handoff only | `python3 scripts/ahl.py new-handoff`. |
| Inspect promptset health | `python3 scripts/ahl.py promptset` and `python3 scripts/ahl.py promptset --json`. |
| Probe assistant driver records | `python3 scripts/ahl.py driver check` and help-only `driver probe`. |
| Plan or dry-run an outer-loop sequence | `python3 scripts/ahl.py outer plan`, `outer dry-run`, `outer run --dry-run`, `outer gate`, `outer status`, and `outer resume`; live local assistant CLI use requires explicit `outer run --execute`. |
| Use AHL from a target project | `python3 scripts/ahl.py project status`, `lifecycle snippets`, `lifecycle context-check`, `lifecycle run-range`, `commit check`, and `portable rehearsal`. |
| Explain why next prompt is not ready | Docs-only routine today, backed by the readiness report contract and schema. |
| Collect prompt-to-commit traceability | `runbooks/commit-packaging.md`, `python3 scripts/ahl.py trace`, `commit plan`, and `commit check`; `commit execute` requires explicit approval. |
| Summarize current prompt scope and changed areas | `python3 scripts/ahl.py trace PROMPT_XX`. |
| Retrieve similar prior prompts, handoffs, or doctrine chunks in the future | Future derived-index candidate only; no transcript indexing or service. |

## Boundaries

These surfaces are operator controls, not autonomous authority. Scripts may
inventory files, scaffold records, build dry-run plans, print JSON, and invoke
supported local assistant CLIs only through explicit `outer run --execute`, but
the operator still picks the prompt, approves commits, decides whether a
handoff is justified, and promotes durable memory.
