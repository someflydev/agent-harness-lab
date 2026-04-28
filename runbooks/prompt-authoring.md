# Prompt Authoring

## Purpose

Create or revise prompt files, promptsets, planning material, or sequencing
guidance in a dedicated prompt-authoring session.

## When To Use It

Use when the operator asks to draft, revise, split, repair, or review prompt
files. Do not use ordinary prompt-execution sessions to generate or revise
future prompt files unless the active prompt explicitly authorizes it.

## Required Context To Load

- Operator's authoring request.
- Existing prompt files directly affected by the request.
- `docs/runtime/prompt-authoring-vs-execution.md`.
- Relevant docs or plans named by the operator.
- `git status --short`.

## Roles Involved

- Operator: sets sequencing goals and accepts prompt changes.
- Prompt Author: writes or revises prompt files.
- Promptset Quality Inspector: checks dependencies, order, and scope.
- Orchestrator: prevents implementation work from slipping into authoring.

## Step-By-Step Procedure

1. Confirm the session is prompt authoring, not prompt execution.
2. Identify which prompt files or planning artifacts are in scope.
3. Load only the adjacent prompts and docs needed to preserve sequencing.
4. Draft or revise prompt text with explicit startup, deliverables,
   constraints, validation, and endcap guidance.
5. Check that each prompt can run in a fresh session.
6. Check that prompt execution is not being performed as part of authoring.
7. Update indexes or planning docs only if the authoring request requires it.
8. Close with changed prompt files, sequencing risks, and validation performed.

## Expected Artifacts

- New or revised prompt files when requested.
- Optional promptset health findings.
- No implementation deliverables from those prompts.

## Validation Or Evidence

- Prompt files contain clear scope, deliverables, constraints, validation, and
  closeout instructions.
- Adjacent prompt dependencies are internally consistent.
- Generated prompts do not require context that is unavailable from repo files.
- Git status is checked before closeout.

## Stop Conditions

- Authoring requires implementing the prompts to know what to write.
- Sequencing conflicts require operator direction.
- A prompt would depend on missing durable artifacts not covered by the
  authoring request.
- The work turns into broad promptset redesign without authorization.

## Common Failure Modes

- Executing a prompt while authoring it.
- Generating future prompts during ordinary prompt execution.
- Writing prompts that assume hidden chat context.
- Omitting validation or endcap instructions.
