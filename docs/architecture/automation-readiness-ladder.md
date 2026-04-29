# Automation Readiness Ladder

Automation readiness is earned by repeated, inspectable use. A routine should
advance one step at a time, and it can stay at any level indefinitely.

## Ladder

| Level | Description | Graduation signal |
| --- | --- | --- |
| Named doc | The routine has a stable name and purpose. | Operators can point to the page instead of re-explaining the workflow. |
| Checklist | The routine has ordered steps and stop conditions. | Multiple sessions follow the same sequence with similar evidence. |
| Template | Repeated output has a reusable record shape. | Free-form notes repeatedly contain the same fields. |
| Helper script | Mechanical steps are scripted locally. | The step is deterministic, low judgment, and cheap to test. |
| Structured output | Script output has stable fields or schema coverage. | Downstream reports or audits need machine-readable facts. |
| Deterministic tests | The helper behavior has repeatable tests. | Failures can be caught without replaying an assistant session. |
| Optional automation hook | Operator-triggered automation connects tested pieces. | Inputs, outputs, approvals, and failure handling are explicit. |
| Runtime component | A durable runtime responsibility exists. | The component simplifies a proven workflow and has clear ownership. |

## Criteria For Moving Up

- The routine happens often enough to justify maintenance cost.
- Inputs and outputs are stable across different prompt sessions.
- The step is mostly mechanical or has clear human approval gates.
- Failures can be detected by checks, tests, schemas, or review.
- The automated form preserves visible artifacts and operator control.
- The change reduces missed steps, inconsistent records, or review burden.

## Criteria For Not Automating

Keep a routine as prose, a checklist, or a template when it is rare,
judgment-heavy, experimental, provider-specific, security-sensitive, or still
changing after each use. Do not automate a routine whose purpose is unclear, or
whose output would be trusted more than the durable repo evidence it summarizes.
