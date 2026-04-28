# Anti-Patterns

These failure modes are common risks for a prompt-bounded harness. Each one
includes the preferred corrective behavior.

## Endless Session Accumulation

Keeping one session alive until it silently depends on unreviewed context makes
future work hard to reproduce.

Corrective behavior: finish the active prompt, audit it, preflight the next
prompt, and reset into a fresh session.

## Always-On Handoff Generation

Creating handoffs after every prompt adds noise and teaches future sessions to
trust routine churn.

Corrective behavior: create bridge artifacts only for real blockers,
non-trivial warnings, or context that will materially improve the next session.

## Vague Megaplanning

Large speculative plans can bury the immediate work unit under future
possibilities.

Corrective behavior: keep the active prompt concrete, inspect adjacent prompts
only when useful, and store future ideas in the right planning artifact when a
prompt asks for them.

## Conflating Implemented With Ready

A file can exist while the repo is still not ready for the next session because
navigation, terminology, or validation is missing.

Corrective behavior: run both a completion audit and a next-prompt preflight.

## Loading Too Many Future Prompts

Reading far ahead invites scope drift and accidental implementation of work
owned by later prompts.

Corrective behavior: read the active prompt and adjacent prompt only when the
startup or endcap asks for that context.

## Treating Raw Transcripts As Durable Truth

Assistant chatter may contain mistakes, partial decisions, or abandoned ideas.

Corrective behavior: promote only reviewed knowledge into explicit repo
artifacts with traceable evidence.

## Metadata Hoarding

Collecting fields, tags, indexes, and reports without a clear consumer creates
maintenance burden.

Corrective behavior: add metadata only when it supports a current routine,
validation gate, or operator decision.

## Premature Graph/Vector Infrastructure

Indexes can look powerful before the durable source material and promotion
rules are mature.

Corrective behavior: keep graph or vector systems as rebuildable derived
indexes, and add them only after human-operable routines prove the need.

## Hidden Autonomous Behavior

Background actions, implicit approvals, or opaque state changes weaken operator
control.

Corrective behavior: make commands, permissions, decisions, and outputs visible
through the operator control surface.

## Giant Framework Gravity

Importing a broad framework can force the repo to fit the tool instead of the
workflow.

Corrective behavior: start with markdown routines, templates, contracts, and
small scripts that match proven local needs.

## Patch-Loop Sprawl

Repeated unbounded fixes can turn a narrow prompt into a wandering repair
session.

Corrective behavior: identify the blocker, make the smallest coherent repair,
validate it, and leave a handoff only if risk remains.

## Reference-Repo Cloning

Copying a reference project's identity, structure, or assumptions blurs this
repo's purpose.

Corrective behavior: adapt compatible ideas selectively and keep
`agent-harness-lab` distinct in names, artifacts, and operating model.
