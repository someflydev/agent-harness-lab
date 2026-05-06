# Future Backlog

This backlog lists future work as candidates, not as active baseline
requirements. Items should become prompts only in a dedicated prompt-authoring
session after evidence and scope are clear.

## Real-World Usage Findings

- Capture findings from actual fresh-session runs.
- Compare operator closeout behavior against the runbooks.
- Record repeated failure modes before changing doctrine or scripts.
- Add examples only when real runs expose clearer patterns.

## Stronger Semantic Validation

- Add checks that catch contradictions between key docs without claiming full
  semantic proof.
- Explore artifact-specific validation for contracts, handoffs, findings, and
  run records.
- Extend fixtures only where deterministic examples catch real regressions.

## Optional Local Search And Indexing

- Evaluate lightweight local search helpers after navigation friction is
  observed.
- Keep any index derived from checked-in files.
- Avoid hidden memory stores or unreviewed transcript ingestion.

## Post-Baseline Outer Sequential Runner

- Use `../outer-loop/README.md` as the phase-two requirements and safety
  boundary index.
- Define a dry-run-first outer loop for supported assistant CLIs.
- Plan prompt batches without executing them by default.
- Run prompts sequentially, not in parallel, unless a later design justifies a
  narrower exception.
- Stop on failed validation, unsafe git state, driver failure, or unclear
  permissions.
- Treat the current outer-loop docs as design inputs, not implemented runner
  behavior.

## Driver Adapters

- Use `../outer-loop/assistant-driver-boundary.md` for shared vocabulary and
  provider boundary rules.
- Consider Codex, Gemini, Pi, or other tool adapters only when their local
  invocation model can be inspected and safely bounded.
- Keep subscription CLI usage separate from API-backed provider runtimes.
- Avoid credential storage and hidden provider abstraction.
- Treat Claude subscription automation outside Claude Code as out of scope
  unless a later API-backed path is explicitly requested and designed.

## Richer Lane Orchestration

- Convert proven manual lane routines into structured plans.
- Add lane status validation only where it improves reviewability.
- Preserve operator authority over role assignment and escalation.

## Assistant-Specific Package Adapters

- Package startup context for specific assistants when repeated use proves the
  shape.
- Keep assistant guides tool-specific but avoid claims that need live product
  verification unless the update explicitly refreshes those docs.

## Additional Domain Packs

- Add packs only for recurring domains with clear validation needs.
- Keep packs optional and separate from default startup context.
- Reuse the `_template` manifest and check command.

## Derived Graph Or Vector Indexes

- Treat graph or vector retrieval as future derived indexes only.
- Require clear evidence that markdown navigation and local search are not
  enough.
- Keep repo files and git history authoritative over any index output.
