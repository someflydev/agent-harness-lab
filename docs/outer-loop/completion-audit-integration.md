# Completion Audit Integration

The gate uses deterministic checks to decide whether a runner can continue
mechanically. It verifies prompt-file presence, git status readability,
next-prompt availability, plan linkage, recorded validation commands, and
allowlisted AHL structural checks such as promptset lint and doctor.

Semantic audit remains separate. The gate can record that a completion audit
artifact exists, but it does not infer that the artifact is correct and does
not promote structural checks into semantic proof. A `needs-human-review`
status is the honest default when no explicit audit artifact is supplied.

## Human Judgment

Use `runbooks/completion-audit.md` to compare prompt requirements against the
actual diff, validation evidence, docs claims, constraints, and adjacent
readiness. Project skills such as `trajectory-evaluator` can be used at
closeout when the operator wants a post-session audit of deliverables,
readiness, and commit grouping. Those skills should summarize inspected
evidence; they should not store raw transcripts as proof.

## State Representation

- Incomplete work should be represented as `needs-human-review` or `blocked`
  with concrete missing evidence.
- Blocked work should cite the missing prompt, missing plan artifact, missing
  next prompt, unsafe git state, or failed AHL check.
- Unknown semantic status should remain unknown. The gate should say that
  semantic completion is unclaimed instead of manufacturing confidence from
  passing structural checks.

This keeps the runner honest: deterministic checks can stop obvious bad
continuation, while humans and assistant closeout routines still decide
whether the prompt was actually completed.
