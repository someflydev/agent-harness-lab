# Experiment Catalog

Use this catalog as the entry point for planned, active, closed, or abandoned
experiments. Keep rows compact and link to the plan, log, closeout, or related
report when those artifacts exist.

New experiment scaffolds are created under `active/<slug>/` by
`python3 scripts/ahl.py experiment new <slug>`. The helper does not edit this
catalog automatically; add rows manually after the operator confirms the
experiment should be tracked.

| Experiment id | Status | Question | Artifacts | Outcome |
| --- | --- | --- | --- | --- |
| EXAMPLE-001 | Example | Does a closeout checklist reduce missed next-prompt preflight steps? | `templates/experiment-plan.md`, `templates/experiment-closeout.md` | Example only; no evidence recorded. |
| EXAMPLE-002 | Example | Does a shorter prompt template improve fresh-session execution focus? | `templates/experiment-log.md` | Example only; no evidence recorded. |

## Status Values

- Planned: question and setup are defined, but work has not started.
- Active: evidence is being collected.
- Closed: closeout decision is recorded.
- Abandoned: the test is intentionally stopped without a result.
- Superseded: a newer experiment or accepted artifact replaced the need.
