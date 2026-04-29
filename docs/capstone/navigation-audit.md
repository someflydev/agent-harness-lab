# Navigation Audit

This audit checks whether a new operator can find the important docs without
knowing the prompt history.

## Entry Points

| Need | Primary path | Result |
| --- | --- | --- |
| Understand the repo purpose | `README.md` | Clear public identity and boundaries. |
| Start an assistant session | `AGENT.md` | Clear first-read order, guardrails, checks, and endcap loop. |
| Start as an operator | `docs/operator-start.md` | Clear human workflow entry. |
| Find documentation areas | `docs/README.md` | Broad index across doctrine, roles, routines, runbooks, runtime, memory, metadata, quality, scripts, examples, evidence, architecture, and capstone. |
| Run a prompt | `runbooks/fresh-session-prompt-run.md` | Clear one-prompt execution flow. |
| Audit completion | `runbooks/completion-audit.md` and `docs/quality/audit-protocol.md` | Clear audit routine and quality vocabulary. |
| Preflight the next prompt | `runbooks/next-prompt-preflight.md` and `docs/runtime/adjacent-prompt-readiness.md` | Clear readiness check without implementing future prompts. |
| Use helper scripts | `docs/scripts.md` and `scripts/README.md` | Clear command list, boundaries, and JSON fields. |
| Understand future architecture | `docs/architecture/README.md` | Clear future-facing architecture index. |

## Findings

- Main navigation is now reachable from `README.md`, `AGENT.md`,
  `docs/README.md`, and directory-level READMEs.
- The docs distinguish current helper scripts from future automation
  candidates.
- The foundation-phase capstone docs give reviewers a place to inspect gaps
  without reading every prompt file.

## Remaining Navigation Risks

- The amount of documentation is now high enough that stale indexes will be a
  recurring risk.
- Some directories have both operator-facing docs and templates, so future
  changes should keep index descriptions specific.
- Actual run records are still sparse; new operators may understand the
  intended flow before seeing many real completed runs.

## Recommended Maintenance

Review `README.md`, `AGENT.md`, `docs/README.md`, `scripts/README.md`, and
directory-level READMEs whenever a prompt adds a new durable doc family,
helper command, schema, or runbook. Navigation should point to current
artifacts and avoid promising future runtime capabilities.
