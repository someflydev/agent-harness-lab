# Architecture

Architecture notes describe possible future structure for
`agent-harness-lab` without making those ideas current requirements. They are
decision guides for later prompts, not implementation plans for the foundation
phase.

## Start Here

- `future-runtime-path.md` - gradual path from documented routines to richer
  orchestration after the human-assisted model is proven.
- `automation-readiness-ladder.md` - criteria for graduating a routine from
  prose to templates, scripts, structured output, tests, hooks, or runtime.
- `traceability-graph-and-semantic-retrieval.md` - future guidance for graph
  and semantic retrieval as derived indexes over durable artifacts.
- `non-goals.md` - foundation-phase boundaries that prevent premature runtime
  expansion.

## Current Posture

The current repo is a documentation-first lab with small local helper scripts.
Architecture docs may name future candidates such as local indexes or bounded
automation hooks, but repo files and git history remain the authoritative
record. Any richer runtime must earn its place through repeated manual use,
clear contracts, and deterministic validation.
