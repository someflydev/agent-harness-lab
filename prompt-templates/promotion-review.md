# Promotion Review

Purpose: decide whether a temporary observation should become durable repo
memory, documentation, or no artifact.

## Prompt

Review `<CANDIDATE_FACT>` for promotion using source evidence and artifact
boundaries, then decide `promote`, `defer`, or `reject`.

## Placeholders

- `<CANDIDATE_FACT>`: observation or lesson under review.
- `<SOURCE_EVIDENCE>`: files, reports, validation output, or handoff evidence.
- `<TARGET_BOUNDARY>`: likely artifact type or path.
- `<OPERATOR_APPROVAL>`: approval status if policy judgment is involved.

## Required Context To Load

- `runbooks/promotion-review.md`
- `docs/memory/promotion-model.md`
- `docs/doctrine/artifact-boundaries.md`
- `<SOURCE_EVIDENCE>`
- Existing docs near `<TARGET_BOUNDARY>` to avoid duplicates

## Expected Output

- Decision: `promote`, `defer`, or `reject`.
- Evidence summary.
- Target artifact path when promoted.
- Reason when deferred or rejected.

## Stop Conditions

- Evidence is weak or unavailable.
- Target artifact boundary is unclear.
- Promotion needs operator approval that has not been given.
- The candidate is broad design work disguised as memory.

