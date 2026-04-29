# Open Questions

These questions remain unresolved after the foundation phase. They are not
immediate scope commitments.

## Design Questions

- Which manual closeout facts are common enough to deserve required run
  records rather than optional examples?
- When should `scripts/ahl.py validate` start checking navigation links or
  schema examples, and how strict should that become?
- Which routines should get deterministic tests before any automation hook is
  considered?
- What evidence would justify a local index, and which durable artifacts should
  be indexed first?
- How should future reports distinguish one-off session lessons from recurring
  findings that deserve promotion?
- What minimum contract would an outer sequential runner need before it could
  safely invoke external assistant CLIs one prompt at a time?
- How should prompt-authoring sessions record changes to later prompt files
  without blurring the boundary with prompt-execution sessions?
- What is the smallest useful commit traceability report after a prompt is
  committed?
- Should examples eventually be generated from real run records, or remain
  hand-written teaching artifacts?
- How should local-only operator notes be pruned when they are useful during a
  run but not worth durable promotion?

## Review Cadence

Revisit these questions during hardening and post-baseline prompt-authoring
work. A question should become implementation scope only when there is evidence
from repeated prompt runs, reports, findings, or validation gaps.
