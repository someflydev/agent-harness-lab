# Sequential Runner Model

The sequential runner is a local wrapper around existing assistant tools. It
does not replace prompt files, assistant CLIs, validation gates, completion
audit, next-prompt readiness, git review, or operator approval.

## Components

| Component | Responsibility | Status |
| --- | --- | --- |
| Batch planner | Select a prompt range, inspect prompt files, build a dry-run batch plan, and define stop rules. | Later phase-two prompt |
| Assistant driver registry | List supported local drivers and their capability probes without hiding provider differences. | Later phase-two prompt |
| Prompt payload builder | Assemble bounded startup context for a fresh assistant session. | Later phase-two prompt |
| Live runner | Invoke one assistant CLI session per prompt when explicitly authorized. | Later phase-two prompt |
| Validation gate runner | Run prompt-required validation and AHL structural checks after each prompt. | Later phase-two prompt |
| Completion auditor | Compare deliverables and evidence against the active prompt. | Exists now as a manual runbook and skill; later prompt may wire it into runner output |
| Next-prompt readiness checker | Inspect only the immediate next prompt for obvious blockers. | Exists now as a manual runbook and skill; later prompt may wire it into runner output |
| Run ledger | Record per-prompt inputs, outputs, validation, audit, readiness, stop reasons, and commit-plan references. | Later phase-two prompt |
| Commit planner | Produce reviewable prompt-id commit packages without staging or committing by default. | Exists now as manual guidance; later prompt may add structured planning |
| Explicit commit executor | Stage and commit only after operator authorization. | Later phase-two prompt |
| Resume and failure handler | Resume from the last safe ledger entry or stop with a clear handoff when state is unsafe. | Later phase-two prompt |

## Current Prompt Scope

This prompt creates the requirements layer for those components. It does not
create executable runner code or invoke assistant tools.

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

