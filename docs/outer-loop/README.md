# Outer Loop

The outer loop is a phase-two design area for a local sequential wrapper around
the existing fresh-session prompt workflow. It is requirements and boundary
documentation only until later prompts implement and validate concrete runner
code.

The goal is bounded orchestration of already-authenticated assistant tools, one
prompt at a time. The runner should make decisions visible through files,
structured output, validation evidence, completion audits, and explicit
operator approval points.

## Start Here

- `requirements.md` - target workflow, stop conditions, and the canonical
  batch-run example that is not implemented yet.
- `safety-boundary.md` - consent, dry-run, git, transcript, credential, and
  failure boundaries.
- `sequential-runner-model.md` - component model and current versus future
  implementation status.
- `assistant-driver-boundary.md` - vocabulary and provider boundary for
  subscription CLIs and API-backed runtimes.
- `non-goals.md` - explicit exclusions for the outer-loop design.
- `roadmap.md` - phase-two implementation sequence after this requirements
  layer.

## Current Status

This prompt creates the requirements layer. It does not add live assistant
invocation, provider credentials, a daemon, a TUI, an MCP server, a scheduler,
or dependency-backed runtime code.

