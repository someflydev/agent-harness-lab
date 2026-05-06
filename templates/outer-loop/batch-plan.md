# Outer Loop Batch Plan

- Plan id:
- Created at:
- Requested range:
- Driver:
- Model:
- Reasoning:
- Permission posture:
- Commit policy:
- Run artifact directory:

## Prompts

| Prompt | Path | Validation commands |
| --- | --- | --- |

## Required AHL Checks

- `python3 scripts/ahl.py promptset lint`
- `python3 scripts/ahl.py doctor`

## Stop Conditions

- Missing prompt file.
- Missing driver record.
- Missing or empty validation commands.
- Missing stop conditions.
- Failed prompt validation or AHL check.
- Unsafe git state.
- Operator approval boundary.

## Review Notes

- A plan is an artifact for review, not execution approval.
- Dry-run the plan before any live assistant invocation is implemented or used.
