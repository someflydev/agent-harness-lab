# Sequential Runner Model

The sequential runner is a local wrapper around existing assistant tools. It
does not replace prompt files, assistant CLIs, validation gates, completion
audit, next-prompt readiness, git review, or operator approval.

## Components

| Component | Responsibility | Status |
| --- | --- | --- |
| Batch planner | Select a prompt range, inspect prompt files, build a dry-run batch plan, and define stop rules. | Implemented as `outer plan` |
| Assistant driver registry | List supported local drivers and their capability probes without hiding provider differences. | Implemented as `driver` registry helpers |
| Prompt payload builder | Assemble bounded startup context for a fresh assistant session. | Implemented inside `outer run` |
| Live runner | Invoke one assistant CLI session per prompt when explicitly authorized. | Implemented for supported local driver contracts through `outer run --execute` |
| Validation gate runner | Run prompt-required validation and AHL structural checks after each prompt. | Implemented as conservative `outer gate`; arbitrary prompt validation commands remain record-only |
| Completion auditor | Compare deliverables and evidence against the active prompt. | Exists now as a manual runbook and skill; later prompt may wire it into runner output |
| Next-prompt readiness checker | Inspect only the immediate next prompt for obvious blockers. | Exists now as a manual runbook and skill; later prompt may wire it into runner output |
| Run ledger | Record per-prompt inputs, outputs, validation, audit, readiness, stop reasons, and commit-plan references. | Implemented as `run-ledger.json` |
| Commit planner | Produce reviewable prompt-id commit packages without staging or committing by default. | Implemented as `commit plan` |
| Explicit commit executor | Stage and commit only after operator authorization. | Implemented as `commit execute --operator-approved` |
| Resume and failure handler | Resume from the last safe ledger entry or stop with a clear handoff when state is unsafe. | Implemented as `outer status`, `outer resume`, and `outer recovery-handoff` |

## Current Prompt Scope

The current phase-two layer includes planning, dry-run checks, gates, live
runner support behind explicit consent, commit planning and execution behind
operator approval, run ledgers, and resume planning. It still does not create a
daemon, scheduler, provider credential store, or transcript memory.

## Operating Shape

The MVP should run a single prompt at a time within a selected batch:

1. Inspect working tree state.
2. Build the prompt payload.
3. Invoke the selected driver only when `--execute` style consent is present.
4. Wait for the assistant session to finish.
5. Run validation gates.
6. Audit completion.
7. Check readiness for the immediate next prompt.
8. Record ledger output.
9. Stop on any blocker or continue to the next prompt only when all gates pass.
