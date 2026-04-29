# Future Runtime Path

`agent-harness-lab` should move toward automation only when repeated operator
work proves that automation will reduce errors without hiding judgment. The
path below is a gradual migration model, not a commitment to build every layer.

## Path

1. Documented routines
   - A recurring workflow is described in docs or runbooks.
   - The routine has named inputs, outputs, stop conditions, and validation
     evidence.
   - Move forward when different fresh sessions can follow the same routine
     without relying on private memory.

2. Templates and contracts
   - Repeated records get reusable markdown templates or contract shapes.
   - Required fields are stable enough that reviewers can compare runs.
   - Move forward when operators repeatedly create the same artifact by hand
     and the field set stops changing every run.

3. Small helper scripts
   - A dependency-light local script checks, scaffolds, or summarizes an
     already documented routine.
   - The script exposes inspectable output and refuses to become the authority
     for scope or completion.
   - Move forward when manual steps are mechanical, easy to test, and causing
     avoidable mistakes.

4. Structured run metadata
   - Runs can emit compact, schema-backed records such as changed paths,
     validation commands, audit status, readiness status, and handoff status.
   - Metadata stays derived from prompts, docs, commands, reports, and git.
   - Move forward when reports, audits, or commit packaging need the same facts
     often enough that free-form notes become noisy.

5. Optional local indexes
   - Disposable indexes may help find connected or similar durable artifacts.
   - Indexes must be rebuildable and subordinate to repo files and git history.
   - Move forward when manual navigation is too slow even though the durable
     docs are coherent.

6. Bounded automation hooks
   - Narrow hooks may connect validated scripts to operator-triggered flows.
   - Hooks should have explicit inputs, visible output, and clear failure
     modes.
   - Move forward when a scripted routine has deterministic tests, stable
     metadata, and a human approval point.

7. Richer orchestration
   - More capable orchestration may coordinate prompt runs, validation, and
     handoffs after the human-assisted model is proven.
   - This layer should preserve bounded prompts, visible artifacts, and human
     control over commits, promotion, and scope.
   - Move forward only after the lower layers have produced enough evidence to
     show that orchestration simplifies the workflow instead of obscuring it.

## Possible Outer Sequential Runner

A post-baseline candidate is an outer sequential runner that invokes external
assistant CLIs one prompt at a time. That runner would be an operator-facing
automation layer for a known promptset flow, not a foundation-phase feature and
not a provider abstraction layer. It should be considered only after prompt
execution, closeout, readiness, and handoff records are stable enough to define
the runner's contract.

The runner would still leave assistant work in fresh prompt-sized sessions,
would surface validation evidence, and would stop for human review at explicit
approval points.

## Signals To Stay Put

Do not climb the ladder when the routine is rare, judgment-heavy, unstable,
provider-specific, hard to validate, or better handled by a short checklist.
Do not automate around unclear docs; fix the routine first.
