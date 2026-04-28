# Artifact Boundaries

This repo should stay navigable as it grows. These boundaries define where
different kinds of artifacts belong and how they should relate.

## Doctrine

Doctrine states durable operating principles and vocabulary. It should explain
how the harness thinks, not provide long procedural steps for a specific task.

## Runtime State

Runtime state is the temporary condition of a session, command, or environment.
It should not become durable memory unless reviewed and promoted into a stable
artifact.

## Roles

Roles describe responsibilities and boundaries for human and assistant
participants. Role taxonomy belongs in `docs/roles/`; doctrine should only keep
the durable boundary that roles describe who is acting.

## Skills

Skills are reusable capability packages or instructions loaded for a specific
kind of task. Full skill taxonomy belongs to later skill-specific work.

## Routines

Routines are repeatable operator or assistant procedures. They should be
step-oriented and practical, and they belong outside doctrine once they become
detailed.

## Contracts

Contracts define expected inputs, outputs, fields, statuses, evidence, and
escalation points for commands, reports, prompts, or routines.

## Templates

Templates provide reusable starting shapes for prompts, handoffs, reviews,
reports, or other artifacts. They should not contain hidden decisions that
belong in doctrine or contracts.

## Run Manifests

Run manifests record what happened in a session or command run. They should
capture traceable evidence rather than become a second source of project truth.

## Reports And Findings

Reports and findings summarize evidence, risks, and decisions. They should link
back to the prompts, files, commands, or commits that support their claims.

## Examples

Examples demonstrate how the harness should be used. They should be clearly
marked as examples so future sessions do not confuse illustrative data with live
state.

## Temporary Handoffs

Temporary handoffs help the next fresh session when a blocker or non-trivial
warning remains. They should be rare, direct, and removable once the handoff is
no longer needed.

## Prompt-Authoring Artifacts

Prompt-authoring artifacts define or refine the promptset itself. They should
not quietly execute implementation work unless the operator asks.

## Prompt-Execution Artifacts

Prompt-execution artifacts are the durable outputs required by one active
prompt. They should stay within that prompt's scope and include validation
evidence during closeout.
