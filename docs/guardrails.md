# Guardrails

These guardrails define the foundation posture for `agent-harness-lab`.

## Project Boundaries

- Keep `agent-harness-lab` distinct from `agent-context-base`, `pi-mono`, and
  `claw-code`.
- Use cloned reference repos as inspiration and comparison material, not as
  implementation to copy.
- Do not import vendor-specific assumptions from any reference project unless a
  later prompt explicitly justifies them for this repo.

## Artifact Bias

- Prefer markdown, templates, small dependency-free scripts, and explicit
  operator routines before any heavy runtime.
- Make durable decisions inspectable in repo files.
- Treat repo files and git history as the source of truth.

## Memory And Indexes

- Treat graph or vector systems, if discussed later, as derived helper indexes
  only.
- Treat raw agent chatter as unvalidated data, not durable shared memory.
- Promote memory only through explicit review and durable artifacts.

## Workflow Posture

- Preserve the human-assisted, subscription-friendly workflow.
- Keep prompts bounded so they can run in fresh sessions.
- Validate before claiming completion.
- Leave bridge handoffs only when they materially improve the next session.
