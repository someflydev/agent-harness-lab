# Review Findings

Purpose: review changes for bugs, regressions, missing evidence, or scope
violations and report findings by severity.

## Prompt

Review `<REVIEW_SCOPE>` against `<REVIEW_BASELINE>` and report actionable
findings first, with file and line references where possible.

## Placeholders

- `<REVIEW_SCOPE>`: diff, branch, files, or artifact set under review.
- `<REVIEW_BASELINE>`: prompt, contract, runbook, or expected behavior.
- `<RISK_FOCUS>`: areas of concern, if any.
- `<VALIDATION_CONTEXT>`: checks already run.

## Required Context To Load

- `<REVIEW_SCOPE>`
- `<REVIEW_BASELINE>`
- Relevant validation output in `<VALIDATION_CONTEXT>`
- Nearby docs or tests needed to understand expected behavior

## Expected Output

- Findings ordered by severity, with concrete references.
- Open questions or assumptions.
- Brief change summary only after findings.
- Test or validation gaps.

## Stop Conditions

- Review scope is too broad to inspect reliably.
- Required baseline is missing.
- The review would require implementing fixes instead of reporting findings.

